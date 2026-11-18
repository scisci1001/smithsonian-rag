"""Targeted v0.6 checks: do not discard substantive aircraft evidence."""
from smithsonian_rag.domain.models import SmithsonianRecord, TextEntry
from smithsonian_rag.selection import CorpusSelector


def aircraft(description: str, *, object_types=None, title="Historic aircraft"):
    return SmithsonianRecord(
        record_id="nasm_test", unit_code="NASM", title=title,
        object_types=object_types or ["Aircraft"],
        narrative_texts=[TextEntry(category="notes", label="Summary", content=description)],
    )


def test_incidental_gauges_on_aircraft_do_not_qualify():
    result = CorpusSelector().select(aircraft("It carried oil pressure, oil temperature and a tachometer."))
    assert not result.accepted
    assert result.reason_codes == ["OUT_OF_DOMAIN"]


def test_substantive_onboard_autopilot_is_retained():
    result = CorpusSelector().select(aircraft("An autopilot was installed and tested in flight."))
    assert result.accepted
    assert "guidance" in result.matched_domains


def test_primary_instrument_artifact_remains_in_scope():
    result = CorpusSelector().select(aircraft("An oil pressure gauge.", object_types=["Flight instruments"], title="Oil pressure indicator"))
    assert result.accepted


def test_aircraft_with_primary_technology_match_remains_in_scope():
    result = CorpusSelector().select(aircraft("The oil pressure gauge was installed.", title="Aircraft radar testbed", object_types=["Aircraft"]))
    assert result.accepted
    assert "electronics" in result.matched_domains


def test_contextual_control_system_not_automatically_removed():
    result = CorpusSelector().select(aircraft("The aircraft incorporated an innovative control system."))
    assert result.accepted


def test_version_is_updated():
    assert CorpusSelector().policy.version == "0.6"
