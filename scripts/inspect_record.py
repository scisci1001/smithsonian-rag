"""Compare a saved Smithsonian search row with its detail API response."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import urlopen

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_BASE = "https://api.si.edu/openaccess/api/v1.0"
DEFAULT_RECORDS = ("nmah_1203284", "nmah_1203285", "nmah_1203286")


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _record_id(record: dict[str, Any]) -> str | None:
    dnr = _dict(_dict(record.get("content")).get("descriptiveNonRepeating"))
    value = dnr.get("record_ID")
    return value if isinstance(value, str) and value else None


def _unwrap_detail(payload: dict[str, Any]) -> dict[str, Any]:
    """Accept a direct EDAN record or a common Smithsonian API response envelope."""
    candidate = payload
    for _ in range(3):
        if isinstance(candidate.get("content"), dict):
            return candidate
        response = candidate.get("response")
        if not isinstance(response, dict):
            break
        candidate = response
    raise ValueError("Detail response does not contain an EDAN record")


def summarize(record: dict[str, Any]) -> dict[str, Any]:
    content = _dict(record.get("content"))
    free = _dict(content.get("freetext"))
    dnr = _dict(content.get("descriptiveNonRepeating"))
    structured = _dict(content.get("indexedStructured"))
    labels: dict[str, int] = {}
    for entries in free.values():
        for item in _list(entries):
            if not isinstance(item, dict):
                continue
            label = str(item.get("label") or "(missing)")
            if isinstance(item.get("content"), str) and item["content"].strip():
                labels[label] = labels.get(label, 0) + 1
    media = _list(_dict(dnr.get("online_media")).get("media"))
    return {
        "record_id": _record_id(record),
        "title": record.get("title"),
        "freetext_labels": dict(sorted(labels.items())),
        "freetext_text_entries": sum(labels.values()),
        "declared_media_types": _list(structured.get("online_media_type")),
        "actual_media_count": len(media),
        "actual_media_types": sorted({str(m.get("type", "UNKNOWN")) for m in media if isinstance(m, dict)}),
        "metadata_rights": _dict(dnr.get("metadata_usage")).get("access"),
    }


def compare(search_record: dict[str, Any], detail_record: dict[str, Any]) -> dict[str, Any]:
    search = summarize(search_record)
    detail = summarize(detail_record)
    if search["record_id"] != detail["record_id"]:
        raise ValueError("Search and detail records have different record_ID values")
    return {
        "record_id": search["record_id"],
        "search": search,
        "detail": detail,
        "delta": {
            "freetext_text_entries": detail["freetext_text_entries"] - search["freetext_text_entries"],
            "actual_media_count": detail["actual_media_count"] - search["actual_media_count"],
            "new_freetext_labels": sorted(set(detail["freetext_labels"]) - set(search["freetext_labels"])),
        },
    }


def fetch_detail(record_url: str, api_key: str) -> dict[str, Any]:
    url = (
        f"{API_BASE}/content/"
        f"{quote(record_url, safe='')}?"
        f"{urlencode({'api_key': api_key})}"
    )
    try:
        with urlopen(url, timeout=30) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"Detail API HTTP {exc.code} for {record_url}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Detail API request failed for {record_url}: {type(exc).__name__}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Detail API response must be a JSON object")
    return _unwrap_detail(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record-id", action="append", dest="record_ids")
    parser.add_argument("--samples", type=Path, default=PROJECT_ROOT / "data" / "samples" / "nmah")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "build" / "record-inspection.json")
    args = parser.parse_args()
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.getenv("SMITHSONIAN_API_KEY")
    if not api_key:
        parser.error("SMITHSONIAN_API_KEY is missing")
    results = []
    for record_id in args.record_ids or DEFAULT_RECORDS:
        source = args.samples / f"{record_id}.json"
        if not source.is_file():
            parser.error(f"Missing local sample: {source}")
        search_record = json.loads(source.read_text(encoding="utf-8-sig"))
        record_url = search_record["url"]
        detail_record = fetch_detail(record_url, api_key)
        results.append(compare(search_record, detail_record))
        print(f"{record_id}: media {results[-1]['search']['actual_media_count']} -> {results[-1]['detail']['actual_media_count']}; text entries {results[-1]['search']['freetext_text_entries']} -> {results[-1]['detail']['freetext_text_entries']}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"records": results}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
