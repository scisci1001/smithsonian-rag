"""Download a reproducible NASM/NMAH sample from Smithsonian Open Access.

The downloader will be implemented after validating the current Smithsonian
API request/response contract with a registered API key. Generated records
belong under data/samples and are intentionally excluded from Git.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from dotenv import load_dotenv


API_BASE_URL = "https://api.si.edu/openaccess/api/v1.0"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "samples"
DEFAULT_SAMPLE_SIZE = 100
DEFAULT_UNITS = ("NASM", "NMAH")


class SmithsonianApiError(RuntimeError):
    """Raised when the Smithsonian API cannot provide a valid response."""


def build_search_url(
    api_key: str,
    unit_code: str,
    *,
    start: int,
    rows: int,
) -> str:
    params = {
        "q": f"unit_code:{unit_code}",
        "start": start,
        "rows": rows,
        "sort": "id",
        "api_key": api_key,
    }

    return f"{API_BASE_URL}/search?{urlencode(params)}"


def fetch_json(url: str) -> dict[str, Any]:
    try:
        with urlopen(url, timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        raise SmithsonianApiError(
            f"Smithsonian API returned HTTP {exc.code}: {exc.reason}"
        ) from exc
    except URLError as exc:
        raise SmithsonianApiError(
            f"Could not reach Smithsonian API: {exc.reason}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise SmithsonianApiError(
            "Smithsonian API returned invalid JSON."
        ) from exc


def extract_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if payload.get("status") != 200:
        raise SmithsonianApiError(
            f"Unexpected Smithsonian API status: {payload.get('status')!r}"
        )

    response = payload.get("response")

    if not isinstance(response, dict):
        raise SmithsonianApiError("Response object is missing.")

    rows = response.get("rows")

    if not isinstance(rows, list):
        raise SmithsonianApiError("Response rows are missing or invalid.")

    return rows


def get_record_id(record: dict[str, Any]) -> str:
    try:
        record_id = record["content"]["descriptiveNonRepeating"]["record_ID"]
    except (KeyError, TypeError) as exc:
        raise SmithsonianApiError(
            "Smithsonian record does not contain record_ID."
        ) from exc

    if not isinstance(record_id, str) or not record_id:
        raise SmithsonianApiError(
            "Smithsonian record contains an invalid record_ID."
        )

    return record_id


def validate_unit(record: dict[str, Any], expected_unit: str) -> None:
    unit_code = record.get("unitCode")

    if unit_code != expected_unit:
        raise SmithsonianApiError(
            f"Expected unit {expected_unit!r}, got {unit_code!r}."
        )


def write_record(
    record: dict[str, Any],
    output_dir: Path,
) -> Path:
    record_id = get_record_id(record)

    output_dir.mkdir(parents=True, exist_ok=True)

    path = output_dir / f"{record_id}.json"

    path.write_text(
        json.dumps(
            record,
            indent=2,
            ensure_ascii=False,
            sort_keys=False,
        )
        + "\n",
        encoding="utf-8",
    )

    return path


def download_unit(
    api_key: str,
    unit_code: str,
    *,
    count: int,
    output_root: Path,
) -> int:
    url = build_search_url(
        api_key,
        unit_code,
        start=0,
        rows=count,
    )

    payload = fetch_json(url)
    rows = extract_rows(payload)

    if len(rows) < count:
        raise SmithsonianApiError(
            f"Requested {count} {unit_code} records, "
            f"but API returned only {len(rows)}."
        )

    output_dir = output_root / unit_code.lower()

    written = 0

    for record in rows[:count]:
        validate_unit(record, unit_code)
        write_record(record, output_dir)
        written += 1

    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a reproducible Smithsonian sample dataset."
    )

    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_SAMPLE_SIZE,
        help="Number of records to download per Smithsonian unit.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Root directory for downloaded sample records.",
    )

    return parser.parse_args()


def main() -> int:
    load_dotenv()

    args = parse_args()

    if args.count <= 0:
        print("--count must be greater than zero.", file=sys.stderr)
        return 2

    api_key = os.getenv("SMITHSONIAN_API_KEY")

    if not api_key:
        print(
            "SMITHSONIAN_API_KEY is not configured.",
            file=sys.stderr,
        )
        return 2

    try:
        for unit_code in DEFAULT_UNITS:
            written = download_unit(
                api_key,
                unit_code,
                count=args.count,
                output_root=args.output,
            )

            print(
                f"{unit_code}: downloaded {written} records "
                f"to {args.output / unit_code.lower()}"
            )

    except SmithsonianApiError as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())