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
    assert result.policy_version == "0.4"
    assert {match.term for match in result.matched_terms} == {"computer", "guidance"}


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


def test_automatic_pilot_synonym_matches_guidance() -> None:
    item = record(
        "nasm_autopilot",
        title="Automatic Pilot, Mechanical Mike",
        object_types=["Autopilots"],
        narrative_texts=[TextEntry(category="notes", label="Description", content="An automatic pilot for an aircraft.")],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is True
    assert result.matched_domains == ["guidance"]
    assert {match.term for match in result.matched_terms} >= {"automatic pilot", "autopilots"}


def test_separated_auto_pilot_variant_matches_guidance() -> None:
    item = record(
        "nasm_auto_pilot",
        title="Wiley Post aircraft",
        narrative_texts=[TextEntry(category="notes", label="Summary", content="An auto pilot was installed.")],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is True
    assert result.matched_domains == ["guidance"]
    assert any(match.term == "auto pilot" for match in result.matched_terms)


def test_radar_and_radio_equipment_match_electronics() -> None:
    item = record(
        "nasm_radar",
        title="Northrop P-61",
        object_types=["Aircraft"],
        narrative_texts=[TextEntry(category="notes", label="Summary", content="The aircraft used airborne radar.")],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is True
    assert result.matched_domains == ["electronics"]
    assert any(match.term == "radar" and match.field == "narrative_texts" for match in result.matched_terms)


def test_radio_receiver_matches_electronics_with_its_source_field() -> None:
    item = record(
        "nasm_receiver",
        title="Western Wireless Type 7 Receiver",
        object_types=["Communication systems", "Avionics"],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is True
    assert "electronics" in result.matched_domains
    assert any(
        match.term == "receiver" and match.field == "title"
        for match in result.matched_terms
    )


def test_instrument_panel_matches_control_and_is_explainable() -> None:
    item = record(
        "nasm_test_panel",
        title="Experimental aircraft",
        narrative_texts=[TextEntry(category="notes", label="Summary", content="An instrument panel was added to record flight-test data.")],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is True
    assert "control" in result.matched_domains
    assert any(
        match.term == "instrument panel" and match.field == "narrative_texts"
        for match in result.matched_terms
    )


def test_directional_gyro_matches_guidance_with_navigational_object_type() -> None:
    item = record(
        "nasm_gyro",
        title="Directional Gyro",
        object_types=["Navigational instruments"],
        topics=["Navigation"],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is True
    assert "guidance" in result.matched_domains
    assert result.evidence_class is EvidenceClass.STRUCTURED


def test_generic_navigational_object_type_does_not_select_signal_flare() -> None:
    item = record(
        "nasm_A19360009000",
        title="Flare, Drift, NC-3",
        object_types=["Navigational instruments"],
        narrative_texts=[TextEntry(
            category="notes",
            label="Summary",
            content="Aircrew used surface flares to signal their position to rescuers.",
        )],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is False
    assert result.matched_domains == []
    assert result.reason_codes == [ReasonCode.OUT_OF_DOMAIN]


def test_specific_compass_and_drift_meter_artifacts_match_guidance() -> None:
    compass = record(
        "nasm_compass",
        title="Aperiodic Compass",
        object_types=["Navigational instruments"],
    )
    drift_meter = record(
        "nasm_drift_meter",
        title="Drift Meter, B-3",
        object_types=["Navigational instruments"],
    )

    results = [CorpusSelector().select(item) for item in (compass, drift_meter)]

    assert all(result.accepted for result in results)
    assert all(result.matched_domains == ["guidance"] for result in results)
    assert any(match.term == "compass" for match in results[0].matched_terms)
    assert any(match.term == "drift meter" for match in results[1].matched_terms)


def test_electric_wristwatch_variants_match_electronics() -> None:
    watch_records = [
        record(
            "nmah_1203283",
            unit_code="NMAH",
            title="wristwatch model, electric",
            object_types=["wristwatch model, electric", "model of Hamilton electric wristwatch"],
        ),
        record(
            "nmah_1203284",
            unit_code="NMAH",
            title="wristwatch, electric",
            object_types=["wristwatch, electric", "electric wristwatch prototype, Hamilton"],
        ),
        record(
            "nmah_1203287",
            unit_code="NMAH",
            title="Ventura",
            object_types=["wristwatch, electric", "Watch, Electric, Large Model Of"],
        ),
    ]

    results = [CorpusSelector().select(item) for item in watch_records]

    assert all(result.accepted for result in results)
    assert all(result.matched_domains == ["electronics"] for result in results)
    assert all(result.evidence_class is EvidenceClass.STRUCTURED for result in results)


def test_aircraft_panel_instruments_match_control_or_electronics() -> None:
    cases = [
        (
            "nasm_oil_fuel_indicator",
            "Indicator, Combined, Oil Temperature / Oil Pressure / Fuel Pressure, Navy",
            ["Engines"],
            "control",
        ),
        (
            "nasm_dual_temperature_indicator",
            "Indicator, Temperature, Dual",
            ["Engines"],
            "control",
        ),
        (
            "nasm_tachometer",
            "Indicator, Tachometer, Japanese Army, Type-100",
            ["Engines"],
            "control",
        ),
        (
            "nasm_fuel_quantity_indicator",
            "Indicator, Fuel Quantity, Japanese Army, Type-100",
            ["Engines"],
            "control",
        ),
        (
            "nasm_voltmeter_ammeter",
            "Voltmeter / Ammeter, Japanese Army",
            ["Instruments"],
            "electronics",
        ),
    ]

    for record_id, title, object_types, expected_domain in cases:
        result = CorpusSelector().select(
            record(record_id, title=title, object_types=object_types)
        )
        assert result.accepted is True
        assert result.matched_domains == [expected_domain]
        assert result.evidence_class is EvidenceClass.STRUCTURED


def test_g_meter_is_classified_as_control_instrumentation() -> None:
    item = record(
        "nasm_A19480159000",
        title="G-Meter / Accelerometer",
        object_types=["Flight Instruments"],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is True
    assert result.matched_domains == ["control"]


def test_navigation_topic_alone_does_not_select_a_pendulum_clock() -> None:
    item = record(
        "nmah_clock",
        unit_code="NMAH",
        title="Galileo Pendulum Clock Model, Replica",
        topics=["Navigation"],
        object_types=["Models"],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is False
    assert result.matched_domains == []


def test_typewriter_is_included_as_structured_hmi_evidence() -> None:
    item = record(
        "nmah_typewriter",
        unit_code="NMAH",
        title="Smith Premier No. 10 Typewriter",
        object_types=["Typewriters", "Typewriter; Standard; Manual"],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is True
    assert result.evidence_class is EvidenceClass.STRUCTURED
    assert result.matched_domains == ["human_machine_interaction"]


def test_aircraft_stabilizer_component_does_not_match_by_itself() -> None:
    item = record(
        "nasm_stabilizer",
        title="Curtiss D-III with Horizontal Stabilizer",
        narrative_texts=[TextEntry(category="notes", label="Description", content="A fixed horizontal stabilizer was fitted to the aircraft.")],
    )

    result = CorpusSelector().select(item)

    assert result.accepted is False
    assert result.matched_domains == []
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
