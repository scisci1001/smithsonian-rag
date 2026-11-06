import json
from pathlib import Path

from smithsonian_rag.normalization.nasm import normalize_nasm
from smithsonian_rag.normalization.nmah import normalize_nmah
from smithsonian_rag.selection import CorpusSelector


def report_filename(policy_version: str) -> str:
    """Build a stable report filename from a dotted numeric policy version."""
    version_parts = policy_version.split(".")
    if not version_parts or any(not part.isdigit() for part in version_parts):
        raise ValueError(f"Invalid policy version: {policy_version}")
    return f"corpus-selection-report-v{''.join(version_parts)}.json"


def main() -> None:
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

    output = Path("build") / report_filename(report.policy_version)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        report.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Input: {report.input_records}")
    print(f"Accepted: {report.accepted}")
    print(f"Report: {output}")


if __name__ == "__main__":
    main()
