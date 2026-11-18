"""Create a reproducible human-review sample from a corpus-selection report."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LABELS = ("RELEVANT", "NOT_RELEVANT", "UNCERTAIN")
HEADERS = (
    "record_id", "unit_code", "title", "accepted", "evidence_class",
    "matched_domains", "matched_terms", "reason_codes",
    "text_preview", "human_label", "review_notes",
)


def _rank(record: dict[str, Any], seed: str) -> str:
    identifier = str(record["record_id"])
    return hashlib.sha256(f"{seed}:{identifier}".encode("utf-8")).hexdigest()


def _allocate(groups: dict[tuple[str, str], list[dict[str, Any]]], count: int) -> dict[tuple[str, str], int]:
    """Allocate sample slots proportionally using largest remainders."""
    available = sum(len(items) for items in groups.values())
    if available < count:
        raise ValueError(f"Requested {count} records, only {available} available")
    quotas = {key: count * len(items) / available for key, items in groups.items()}
    allocations = {key: int(quota) for key, quota in quotas.items()}
    remaining = count - sum(allocations.values())
    order = sorted(groups, key=lambda key: (-(quotas[key] - allocations[key]), key))
    for key in order[:remaining]:
        allocations[key] += 1
    return allocations


def sample_results(results: list[dict[str, Any]], per_decision: int = 20, seed: str = "smithsonian-v05") -> list[dict[str, Any]]:
    """Sample accepted and excluded independently, stratified by unit and evidence class."""
    if per_decision <= 0:
        raise ValueError("per_decision must be positive")
    identifiers = [str(item["record_id"]) for item in results]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Duplicate record IDs in selection report")
    selected: list[dict[str, Any]] = []
    for accepted in (True, False):
        groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for item in results:
            if item["accepted"] is accepted:
                groups[(str(item["unit_code"]), str(item["evidence_class"]))].append(item)
        allocation = _allocate(groups, per_decision)
        for key in sorted(groups):
            ranked = sorted(groups[key], key=lambda item: (_rank(item, seed), item["record_id"]))
            selected.extend(ranked[:allocation[key]])
    return sorted(selected, key=lambda item: (not item["accepted"], item["unit_code"], item["evidence_class"], _rank(item, seed)))


def _source_index(samples: Path) -> dict[str, Path]:
    """Index local raw files by stem, without loading every JSON document."""
    return {path.stem: path for path in sorted(samples.rglob("*.json"))} if samples.is_dir() else {}


def _raw_preview(path: Path | None) -> tuple[str, str]:
    if path is None:
        return "", ""
    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    content = raw.get("content") or {}
    free = content.get("freetext") or {}
    notes = free.get("notes") or []
    excerpts = [str(item["content"]).strip() for item in notes
                if isinstance(item, dict) and isinstance(item.get("content"), str) and item["content"].strip()]
    title = str(raw.get("title") or "")
    return title, " | ".join(excerpts)[:500]


def build_review_rows(selected: list[dict[str, Any]], samples: Path) -> list[dict[str, str]]:
    index = _source_index(samples)
    rows = []
    for item in selected:
        title, preview = _raw_preview(index.get(item["record_id"]))
        rows.append({
            "record_id": item["record_id"],
            "unit_code": item["unit_code"],
            "title": title,
            "accepted": str(item["accepted"]).lower(),
            "evidence_class": item["evidence_class"],
            "matched_domains": "; ".join(item["matched_domains"]),
            "matched_terms": "; ".join(f"{m['field']}:{m['term']}" for m in item["matched_terms"]),
            "reason_codes": "; ".join(item["reason_codes"]),
            "text_preview": preview,
            "human_label": "",
            "review_notes": "",
        })
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=PROJECT_ROOT / "build" / "corpus-selection-report-v05.json")
    parser.add_argument("--samples", type=Path, default=PROJECT_ROOT / "data" / "samples")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "build" / "selection-review-v05.csv")
    parser.add_argument("--per-decision", type=int, default=20)
    parser.add_argument("--seed", default="smithsonian-v05")
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8-sig"))
        selected = sample_results(report["results"], args.per_decision, args.seed)
        rows = build_review_rows(selected, args.samples)
        write_csv(args.output, rows)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"Evaluation sample failed: {exc}\n")
    counts = Counter((row["accepted"], row["unit_code"]) for row in rows)
    print(f"Review sample: {len(rows)} records; policy {report['policy_version']}")
    for (accepted, unit), count in sorted(counts.items()):
        print(f"  {unit} accepted={accepted}: {count}")
    print(f"CSV: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
