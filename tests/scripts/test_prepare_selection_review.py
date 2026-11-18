import csv
import json
from pathlib import Path

import pytest

from scripts.prepare_selection_review import build_review_rows, sample_results, write_csv


def item(index, accepted, unit, evidence):
    return {
        "record_id": f"{unit}_{index}", "unit_code": unit,
        "accepted": accepted, "evidence_class": evidence,
        "matched_domains": ["computing"] if accepted else [],
        "matched_terms": [{"field": "title", "term": "computer"}] if accepted else [],
        "reason_codes": ["DOMAIN_MATCH"] if accepted else ["OUT_OF_DOMAIN"],
    }


def fixture():
    return (
        [item(i, True, "NASM", "A") for i in range(16)]
        + [item(i + 100, True, "NMAH", "B") for i in range(12)]
        + [item(i + 200, False, "NASM", "A") for i in range(28)]
        + [item(i + 300, False, "NMAH", "B") for i in range(24)]
    )


def test_exact_counts_and_reproducibility():
    data = fixture()
    first = sample_results(data, per_decision=20)
    assert first == sample_results(data, per_decision=20)
    assert len(first) == 40
    assert sum(x["accepted"] for x in first) == 20
    assert sum(not x["accepted"] for x in first) == 20
    assert len({x["record_id"] for x in first}) == 40


def test_order_independent_sampling():
    data = fixture()
    assert sample_results(data, 20) == sample_results(list(reversed(data)), 20)


def test_missing_group_capacity():
    data = [item(1, True, "NASM", "A")]
    with pytest.raises(ValueError, match="only 1 available"):
        sample_results(data, per_decision=20)


def test_duplicate_ids_rejected():
    data = [item(1, True, "NASM", "A"), item(1, False, "NASM", "A")]
    with pytest.raises(ValueError, match="Duplicate record IDs"):
        sample_results(data, per_decision=1)


def test_review_rows_include_local_title_and_blank_labels(tmp_path: Path):
    sample_dir = tmp_path / "samples" / "nasm"
    sample_dir.mkdir(parents=True)
    raw = {
        "title": "Apollo computer",
        "content": {"freetext": {"notes": [{"label": "Summary", "content": "A real description."}]}}
    }
    (sample_dir / "NASM_1.json").write_text(json.dumps(raw), encoding="utf-8")
    rows = build_review_rows([item(1, True, "NASM", "A")], tmp_path / "samples")
    assert rows[0]["title"] == "Apollo computer"
    assert rows[0]["text_preview"] == "A real description."
    assert rows[0]["human_label"] == ""
    output = tmp_path / "review.csv"
    write_csv(output, rows)
    with output.open(encoding="utf-8-sig", newline="") as stream:
        assert list(csv.DictReader(stream))[0]["record_id"] == "NASM_1"


def test_missing_raw_record_keeps_review_row(tmp_path: Path):
    rows = build_review_rows([item(1, False, "NMAH", "B")], tmp_path)
    assert rows[0]["title"] == ""
    assert rows[0]["record_id"] == "NMAH_1"
