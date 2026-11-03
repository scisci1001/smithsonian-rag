"""Offline canonical model and normalization regression tests."""
import copy
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from smithsonian_rag.domain.models import SmithsonianRecord
from smithsonian_rag.normalization.nasm import normalize_nasm
from smithsonian_rag.normalization.nmah import normalize_nmah

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_nasm_fields_and_rights():
    raw = fixture("nasm.json")
    snapshot = copy.deepcopy(raw)
    result = normalize_nasm(raw)
    assert result.record_id == "nasm_A19710896000"
    assert result.unit_code == "NASM"
    assert result.title.startswith("Wright XR-2120")
    assert any(e.role == "manufacturer" and e.name == "Wright Aeronautical" for e in result.entities)
    assert result.narrative_texts
    assert result.physical_descriptions
    assert result.media[0].rights.access == "CC0"
    assert result.metadata_rights.access == "CC0"
    assert result.source_metadata.source_record_url == "edanmdm:nasm_A19710896000"
    assert raw == snapshot


def test_nmah_labels_and_missing_media():
    result = normalize_nmah(fixture("nmah.json"))
    assert result.record_id == "nmah_1347189"
    assert result.entities[0].source_label == "maker"
    assert {i.label for i in result.identifiers} >= {"ID Number", "catalog number", "accession number"}
    assert result.media == []
    assert result.metadata_rights.access == "CC0"


def test_rejects_wrong_unit():
    raw = fixture("nmah.json")
    with pytest.raises(ValueError, match="Expected unit NASM"):
        normalize_nasm(raw)


def test_rejects_blank_required_fields():
    with pytest.raises(ValidationError):
        SmithsonianRecord(record_id=" ", unit_code="NASM", title="Valid")


def test_missing_optional_fields_are_safe():
    raw = {"unitCode": "NASM", "title": "Example", "content": {
        "descriptiveNonRepeating": {"record_ID": "nasm_1"}}}
    result = normalize_nasm(raw)
    assert result.narrative_texts == []
    assert result.media == []
    assert result.metadata_rights.access == "UNKNOWN"
    assert result.source_metadata.source_record_url is None
