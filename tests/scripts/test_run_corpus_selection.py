"""Tests for versioned corpus-selection report filenames."""
from scripts.run_corpus_selection import report_filename


def test_policy_version_is_embedded_in_report_filename() -> None:
    assert report_filename("0.4") == "corpus-selection-report-v04.json"


def test_multi_component_policy_version_is_embedded_without_dots() -> None:
    assert report_filename("1.2.3") == "corpus-selection-report-v123.json"


def test_invalid_policy_version_is_rejected() -> None:
    try:
        report_filename("0.4-rc1")
    except ValueError:
        return
    raise AssertionError("Expected invalid policy version to raise ValueError")
