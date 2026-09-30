from pathlib import Path

import pytest

from scripts.download_sample import (
    SmithsonianApiError,
    build_search_url,
    extract_rows,
    get_record_id,
    validate_unit,
    write_record, DEFAULT_OUTPUT_DIR, PROJECT_ROOT,
)


def sample_record(
        *,
        unit_code: str = "NASM",
        record_id: str = "nasm_A123",
) -> dict:
    return {
        "id": "example-id",
        "title": "Example object",
        "unitCode": unit_code,
        "type": "edanmdm",
        "content": {
            "descriptiveNonRepeating": {
                "record_ID": record_id,
                "unit_code": unit_code,
            }
        },
    }


def test_build_search_url_contains_expected_parameters() -> None:
    url = build_search_url(
        "secret-key",
        "NASM",
        start=0,
        rows=100,
    )

    assert "/search?" in url
    assert "q=unit_code%3ANASM" in url
    assert "start=0" in url
    assert "rows=100" in url
    assert "sort=id" in url
    assert "api_key=secret-key" in url


def test_extract_rows_returns_rows() -> None:
    rows = [sample_record()]

    payload = {
        "status": 200,
        "responseCode": 1,
        "response": {
            "rows": rows,
            "rowCount": 1,
            "message": "content found",
        },
    }

    assert extract_rows(payload) == rows


def test_extract_rows_rejects_invalid_status() -> None:
    payload = {
        "status": 500,
        "response": {
            "rows": [],
        },
    }

    with pytest.raises(
            SmithsonianApiError,
            match="Unexpected Smithsonian API status",
    ):
        extract_rows(payload)


def test_get_record_id() -> None:
    assert get_record_id(sample_record()) == "nasm_A123"


def test_get_record_id_rejects_missing_id() -> None:
    record = sample_record()
    del record["content"]["descriptiveNonRepeating"]["record_ID"]

    with pytest.raises(
            SmithsonianApiError,
            match="does not contain record_ID",
    ):
        get_record_id(record)


def test_validate_unit_accepts_expected_unit() -> None:
    validate_unit(sample_record(), "NASM")


def test_validate_unit_rejects_wrong_unit() -> None:
    with pytest.raises(
            SmithsonianApiError,
            match="Expected unit",
    ):
        validate_unit(sample_record(unit_code="NMAH"), "NASM")


def test_write_record_preserves_raw_record(tmp_path: Path) -> None:
    record = sample_record()

    path = write_record(
        record,
        tmp_path / "nasm",
    )

    assert path == tmp_path / "nasm" / "nasm_A123.json"
    assert path.exists()

    import json

    stored = json.loads(path.read_text(encoding="utf-8"))

    assert stored == record


def test_default_output_dir_is_inside_project_root() -> None:
    assert DEFAULT_OUTPUT_DIR == PROJECT_ROOT / "data" / "samples"
