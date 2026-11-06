"""Tests for deterministic, explainable corpus selection."""
from smithsonian_rag.domain.models import SmithsonianRecord, TextEntry
from smithsonian_rag.selection.corpus_selector import CorpusSelector
from smithsonian_rag.selection.models import EvidenceClass, ReasonCode


def record(record_id: str, **kwargs) -> SmithsonianRecord:
    unit_code = kwargs.pop("unit_code", "NASM")
    title = kwargs.pop("title", "Test object")
    return SmithsonianRecord(record_id=record_id, unit_code=unit_code, title=title, **kwargs)


def test_narrative_domain_record_is_accepted_with_reasons() -> None:
    item = record(
        "nasm_1",
        title="Apollo guidance computer",
        narrative_texts=[TextEntry(category="notes", label="Summary", content="A digital computer used for guidance.")],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is True
    assert result.evidence_class is EvidenceClass.NARRATIVE
    assert result.matched_domains == ["computing", "guidance"]
    assert result.reason_codes == [ReasonCode.DOMAIN_MATCH, ReasonCode.NARRATIVE_EVIDENCE]
    assert result.policy_version == "0.1"


def test_structured_domain_record_is_accepted_without_narrative_threshold() -> None:
    item = record("nmah_1", unit_code="NMAH", title="Keyboard", object_types=["keyboard"])

    result = CorpusSelector().select(item)

    assert result.accepted is True
    assert result.evidence_class is EvidenceClass.STRUCTURED
    assert result.reason_codes == [ReasonCode.DOMAIN_MATCH, ReasonCode.STRUCTURED_EVIDENCE]


def test_generic_display_and_control_do_not_match() -> None:
    item = record("nasm_2", title="Display and control components")

    result = CorpusSelector().select(item)

    assert result.matched_domains == []
    assert result.accepted is False
    assert result.reason_codes == [ReasonCode.OUT_OF_DOMAIN]


def test_domain_match_without_evidence_is_excluded_as_insufficient() -> None:
    item = record("nasm_3", title="Microcomputer")

    result = CorpusSelector().select(item)

    assert result.evidence_class is EvidenceClass.INSUFFICIENT
    assert result.accepted is False
    assert result.reason_codes == [ReasonCode.DOMAIN_MATCH, ReasonCode.INSUFFICIENT_EVIDENCE]


def test_blank_structured_values_do_not_count_as_evidence() -> None:
    item = record("nasm_5", title="Microcomputer", topics=[" "])

    result = CorpusSelector().select(item)

    assert result.evidence_class is EvidenceClass.INSUFFICIENT
    assert result.accepted is False


def test_multiple_fields_and_punctuation_match_deterministically() -> None:
    item = record(
        "nasm_4",
        title="Flight-control system",
        topics=["integrated circuit"],
        physical_descriptions=[TextEntry(category="physicalDescription", label="Materials", content="Metal case")],
    )
    selector = CorpusSelector()

    first = selector.select(item)
    second = selector.select(item)

    assert first == second
    assert first.matched_domains == ["electronics", "control"]
    assert first.accepted is True


def test_report_includes_separate_unit_metrics_and_reason_counts() -> None:
    nasm_record = record(
        "nasm_1",
        title="Computer",
        narrative_texts=[TextEntry(category="notes", label="Summary", content="A computer.")],
    )
    nmah_record = record("nmah_1", unit_code="NMAH", title="Terminal", object_types=["terminal"])
    out_of_domain = record("nasm_2", title="Chair")

    report = CorpusSelector().select_many([nasm_record, nmah_record, out_of_domain])

    assert report.input_records == 3
    assert report.accepted == 2
    assert report.accepted_narrative == 1
    assert report.accepted_structured == 1
    assert report.excluded_out_of_domain == 1
    assert report.by_unit["NASM"].accepted == 1
    assert report.by_unit["NMAH"].accepted == 1
    assert report.reason_code_distribution["DOMAIN_MATCH"] == 2
    assert report.reason_code_distribution["OUT_OF_DOMAIN"] == 1
