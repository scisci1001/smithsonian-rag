import importlib.util
from pathlib import Path
import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "inspect_record.py"
spec = importlib.util.spec_from_file_location("inspect_record", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def record(rid, labels=(), media=()):
    return {"title": "Object", "content": {
        "freetext": {"notes": [{"label": k, "content": v} for k, v in labels]},
        "indexedStructured": {"online_media_type": ["Images"]},
        "descriptiveNonRepeating": {"record_ID": rid, "online_media": {"media": list(media)}, "metadata_usage": {"access": "CC0"}},
    }}


def test_compare_detects_new_media_and_text():
    before = record("nmah_1", [("Description", "a")])
    after = record("nmah_1", [("Description", "a"), ("Summary", "b")], [{"type": "Images"}])
    delta = module.compare(before, after)["delta"]
    assert delta == {"freetext_text_entries": 1, "actual_media_count": 1, "new_freetext_labels": ["Summary"]}


def test_compare_rejects_mismatched_ids():
    left = record("nmah_1")
    right = record("nmah_2")
    with pytest.raises(ValueError, match="different record_ID"):
        module.compare(left, right)


def test_unwrap_detail_accepts_envelopes():
    item = record("nmah_1")
    assert module._unwrap_detail({"response": item}) == item
    assert module._unwrap_detail({"response": {"response": item}}) == item


def test_missing_media_is_distinct_from_declared_media():
    summary = module.summarize(record("nmah_1"))
    assert summary["declared_media_types"] == ["Images"]
    assert summary["actual_media_count"] == 0
