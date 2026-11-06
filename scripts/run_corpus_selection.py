import json
from pathlib import Path

from smithsonian_rag.normalization.nasm import normalize_nasm
from smithsonian_rag.normalization.nmah import normalize_nmah
from smithsonian_rag.selection import CorpusSelector

canonical_records = []

for path in sorted(Path("data/samples").rglob("*.json")):
    raw = json.loads(path.read_text(encoding="utf-8-sig"))

    content = raw.get("content", {})
    dnr = content.get("descriptiveNonRepeating", {})
    unit = raw.get("unitCode") or dnr.get("unit_code")

    if unit == "NASM":
        canonical = normalize_nasm(raw)
    elif unit == "NMAH":
        canonical = normalize_nmah(raw)
    else:
        raise ValueError(f"Unsupported unit in {path}: {unit}")

    canonical_records.append(canonical)

report = CorpusSelector().select_many(canonical_records)

output = Path("build/corpus-selection-report.json")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(
    report.model_dump_json(indent=2) + "\n",
    encoding="utf-8",
    )

print(f"Input: {report.input_records}")
print(f"Accepted: {report.accepted}")
print(f"Report: {output}")