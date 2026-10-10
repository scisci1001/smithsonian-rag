import json
from pathlib import Path

import pytest
from smithsonian_rag.profiling.dataset_profiler import load_records, profile_records


def test_empty_profile():
    assert profile_records([]) == {'total_records': 0, 'duplicate_record_ids': 0, 'units': {}}


def test_schema_and_media_mismatch():
    record = {
        'unitCode': 'NMAH', 'title': 'Example',
        'content': {
            'descriptiveNonRepeating': {'record_ID': 'nmah_1', 'metadata_usage': {'access': 'CC0'}},
            'indexedStructured': {'online_media_type': ['Images'], 'object_type': ['computer']},
            'freetext': {'name': [{'label': 'maker', 'content': 'Example Co'}],
                         'identifier': [{'label': 'accession number', 'content': '42'}]},
        },
    }
    result = profile_records([record, record])
    stats = result['units']['NMAH']
    assert result['duplicate_record_ids'] == 1
    assert stats['field_coverage']['declared_without_actual_media']['count'] == 2
    assert stats['field_coverage']['actual_media']['count'] == 0
    assert stats['freetext_labels']['name']['maker'] == 2
    assert stats['identifier_labels']['accession number'] == 2
    assert stats['metadata_rights']['CC0'] == 2


def test_load_records(tmp_path: Path):
    folder = tmp_path / 'nasm'
    folder.mkdir()
    (folder / 'sample.json').write_text(json.dumps({'unitCode': 'NASM'}), encoding='utf-8')
    assert load_records(tmp_path) == [{'unitCode': 'NASM'}]


def test_missing_directory(tmp_path: Path):
    with pytest.raises(ValueError, match='does not exist'):
        load_records(tmp_path / 'missing')



def make_record(unit, rid, notes, physical=None, declared=False, media=None):
    return {
        "unitCode": unit,
        "title": rid,
        "content": {
            "freetext": {
                "notes": [{"label": label, "content": value} for label, value in notes],
                "physicalDescription": physical or [],
            },
            "indexedStructured": {"online_media_type": ["Images"] if declared else []},
            "descriptiveNonRepeating": {
                "record_ID": rid,
                "metadata_usage": {"access": "CC0"},
                "online_media": {"media": media or []},
            },
        },
    }


def test_extended_narrative_labels_and_physical_text():
    records = [
        make_record("NMAH", "nmah_1", [("Description (Brief)", "Useful text")]),
        make_record("NMAH", "nmah_2", [("Physical Description", "Wood and steel")]),
        make_record("NMAH", "nmah_3", [], [{"label": "Measurements", "content": "20 cm"}]),
    ]
    report = profile_records(records)["units"]["NMAH"]["field_coverage"]
    assert report["narrative_description"]["count"] == 1
    assert report["physical_description"]["count"] == 2
    assert report["total_semantic_text"]["count"] == 3


def test_media_mismatch_examples_limited_and_deterministic():
    records = [make_record("NMAH", f"nmah_{i}", [], declared=True) for i in range(7)]
    stats = profile_records(records)["units"]["NMAH"]
    assert stats["field_coverage"]["declared_without_actual_media"]["count"] == 7
    assert stats["media_mismatch_examples"] == [f"nmah_{i}" for i in range(5)]


def test_existing_fields_and_duplicate_detection():
    record = make_record("NASM", "nasm_1", [("Summary", "Flight")])
    report = profile_records([record, record])
    assert report["duplicate_record_ids"] == 1
    assert report["units"]["NASM"]["field_coverage"]["description"]["count"] == 2


def test_real_uploaded_examples_are_parseable():
    # No network or external dataset required for this test.
    record = make_record("NASM", "nasm_1", [("Long Description", "Long text")])
    assert profile_records([record])["units"]["NASM"]["field_coverage"]["narrative_description"]["percent"] == 100.0
