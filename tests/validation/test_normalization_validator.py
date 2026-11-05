from smithsonian_rag.validation.normalization_validator import validate_records


def record(unit="NASM", record_id="nasm_A1", title="Example"):
    return {
        "unitCode": unit,
        "title": title,
        "content": {
            "descriptiveNonRepeating": {"record_ID": record_id, "unit_code": unit},
            "freetext": {"notes": [{"label": "Summary", "content": "Test narrative"}]},
            "indexedStructured": {"object_type": ["Instrument"]},
        },
    }


def test_valid_records():
    report = validate_records([
        ("nasm/1.json", record()),
        ("nmah/2.json", record("NMAH", "nmah_2")),
    ])
    assert report["total_records"] == 2
    assert report["normalized"] == 2
    assert report["failed"] == 0
    assert report["units"]["NASM"]["coverage_counts"]["narrative_records"] == 1


def test_invalid_record_does_not_stop_batch():
    report = validate_records([
        ("bad.json", record(title="  ")),
        ("good.json", record()),
    ])
    assert report["normalized"] == 1
    assert report["failed"] == 1
    assert report["failures"][0]["record_id"] == "nasm_A1"


def test_unsupported_unit():
    report = validate_records([("other.json", record("OTHER"))])
    assert report["failed"] == 1
    assert "Unsupported owning unit" in report["failures"][0]["message"]


def test_non_object_record():
    report = validate_records([("bad.json", [])])
    assert report["failed"] == 1
    assert report["failures"][0]["record_id"] == "UNKNOWN"
