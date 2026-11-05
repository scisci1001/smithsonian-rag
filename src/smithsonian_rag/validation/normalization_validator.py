"""Validate canonical normalization over local Smithsonian EDAN samples."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from smithsonian_rag.normalization.nasm import normalize_nasm
from smithsonian_rag.normalization.nmah import normalize_nmah

NORMALIZERS = {"NASM": normalize_nasm, "NMAH": normalize_nmah}
PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _unit(raw: dict[str, Any]) -> str:
    content = raw.get("content")
    dnr = content.get("descriptiveNonRepeating") if isinstance(content, dict) else None
    fallback = dnr.get("unit_code") if isinstance(dnr, dict) else None
    return str(raw.get("unitCode") or fallback or "UNKNOWN")


def _record_id(raw: dict[str, Any]) -> str:
    content = raw.get("content")
    if not isinstance(content, dict):
        return "UNKNOWN"
    dnr = content.get("descriptiveNonRepeating")
    if not isinstance(dnr, dict):
        return "UNKNOWN"
    return str(dnr.get("record_ID") or "UNKNOWN")


def _failure(source: str, raw: Any, unit: str, exc: Exception) -> dict[str, str]:
    record_id = _record_id(raw) if isinstance(raw, dict) else "UNKNOWN"
    return {
        "source": source,
        "record_id": record_id,
        "unit_code": unit,
        "error_type": type(exc).__name__,
        "message": str(exc),
    }


def _add_coverage(coverage: dict[str, Counter[str]], unit: str, canonical: Any) -> None:
    stats = coverage.setdefault(unit, Counter())
    for key, value in (
        ("narrative_records", canonical.narrative_texts),
        ("physical_records", canonical.physical_descriptions),
        ("media_records", canonical.media),
        ("entity_records", canonical.entities),
        ("date_records", canonical.dates),
        ("topic_records", canonical.topics),
    ):
        stats[key] += bool(value)


def validate_records(records: list[tuple[str, Any]]) -> dict[str, Any]:
    """Return counts and record-level failures without stopping on bad records."""
    units: Counter[str] = Counter()
    successful: Counter[str] = Counter()
    coverage: dict[str, Counter[str]] = {}
    failures: list[dict[str, str]] = []
    for source, raw in records:
        unit = _unit(raw) if isinstance(raw, dict) else "UNKNOWN"
        units[unit] += 1
        try:
            if not isinstance(raw, dict):
                raise ValueError("EDAN record must be an object")
            normalizer = NORMALIZERS.get(unit)
            if normalizer is None:
                raise ValueError(f"Unsupported owning unit: {unit}")
            canonical = normalizer(raw)
            successful[unit] += 1
            _add_coverage(coverage, unit, canonical)
        except (ValueError, TypeError, ValidationError) as exc:
            failures.append(_failure(source, raw, unit, exc))
    return {
        "total_records": len(records),
        "normalized": sum(successful.values()),
        "failed": len(failures),
        "units": {
            unit: {
                "total": units[unit],
                "normalized": successful[unit],
                "failed": units[unit] - successful[unit],
                "coverage_counts": dict(sorted(coverage.get(unit, Counter()).items())),
            }
            for unit in sorted(units)
        },
        "failures": failures,
    }


def load_samples(directory: Path) -> list[tuple[str, Any]]:
    if not directory.is_dir():
        raise ValueError(f"Sample directory does not exist: {directory}")
    files = sorted(directory.rglob("*.json"))
    if not files:
        raise ValueError(f"No JSON files found under {directory}")
    result = []
    for file in files:
        try:
            raw = json.loads(file.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot read {file}: {exc}") from exc
        result.append((str(file.relative_to(directory)), raw))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=Path, default=PROJECT_ROOT / "data" / "samples")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "build" / "normalization-validation.json")
    args = parser.parse_args()
    try:
        report = validate_records(load_samples(args.samples))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Validation failed: {exc}\n")
    print(f"Total: {report['total_records']} | Normalized: {report['normalized']} | Failed: {report['failed']}")
    for unit, stats in report["units"].items():
        print(f"{unit}: {stats['normalized']}/{stats['total']} normalized")
    print(f"Report: {args.output}")
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
