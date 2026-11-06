"""Versioned, deterministic matching terms for the V1 corpus policy."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class DomainRule(BaseModel):
    """A domain and the canonical fields where its terms may match."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    domain: str
    field_terms: dict[str, tuple[str, ...]]


class CorpusSelectionPolicy(BaseModel):
    """Immutable-in-practice policy definition; update the version on edits."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    version: str
    supported_units: tuple[str, ...] = ("NASM", "NMAH")
    domain_rules: tuple[DomainRule, ...]
    evidence_fields: tuple[str, ...] = (
        "physical_descriptions",
        "object_types",
        "topics",
        "entities",
        "dates",
        "places",
        "identifiers",
    )


ELECTRONICS_INTEGRATED_CIRCUIT_TERM = "integrated circuit"
ELECTRONICS_RADAR_TERM = "radar"
ELECTRONICS_RECEIVER_TERM = "receiver"
ELECTRONICS_TRANSMITTER_TERM = "transmitter"
ELECTRONICS_ANTENNA_TERM = "antenna"
ELECTRONICS_AVIONICS_TERM = "avionics"
ELECTRONICS_COMMUNICATION_SYSTEMS_TERM = "communication systems"
ELECTRONICS_RADIO_RECEIVER_TERM = "radio receiver"
ELECTRONICS_RADIO_TRANSMITTER_TERM = "radio transmitter"
ELECTRONICS_VOLTMETER_TERM = "voltmeter"
ELECTRONICS_AMMETER_TERM = "ammeter"
ELECTRONICS_ELECTRIC_WATCH_TERMS = (
    "electric watch",
    "watch electric",
    "electric wristwatch",
    "wristwatch electric",
    "wristwatch model electric",
)
GUIDANCE_NAVIGATION_SYSTEM_TERM = "navigation system"
GUIDANCE_AUTOPILOT_TERMS = ("autopilot", "automatic pilot", "auto pilot")
GUIDANCE_DIRECTIONAL_GYRO_TERM = "directional gyro"
GUIDANCE_GYROSCOPE_TERM = "gyroscope"
GUIDANCE_RADIO_COMPASS_TERM = "radio compass"
GUIDANCE_MAGNETIC_COMPASS_TERM = "magnetic compass"
GUIDANCE_COMPASS_TERM = "compass"
GUIDANCE_DRIFT_METER_TERM = "drift meter"
GUIDANCE_INCLINOMETER_TERM = "inclinometer"
GUIDANCE_ASTRODOME_TERM = "astrodome"
GUIDANCE_NAVIGATION_EQUIPMENT_TERM = "navigation equipment"
CONTROL_PANEL_TERM = "control panel"
CONTROL_SYSTEM_TERM = "control system"
CONTROL_FLIGHT_TERM = "flight control"
CONTROL_INSTRUMENT_PANEL_TERM = "instrument panel"
CONTROL_FLIGHT_INSTRUMENTS_TERM = "flight instruments"
CONTROL_G_METER_TERM = "g-meter"
CONTROL_ACCELEROMETER_TERM = "accelerometer"
CONTROL_FLIGHT_INSTRUMENT_TERMS = (
    "oil temperature",
    "oil pressure",
    "fuel pressure",
    "indicator temperature",
    "tachometer",
    "fuel quantity",
    "temperature sensing",
    "controllable pitch propeller",
)
HUMAN_MACHINE_INTERACTION_TYPEWRITER_TERM = "typewriter"


COMPUTING_FIELD_TERMS = {
    "title": ("computer", "processor", "calculator", "microcomputer"),
    "topics": ("computer", "computing", "processor", "calculator", "microcomputer"),
    "object_types": ("computer", "calculator", "microcomputer"),
    "narrative_texts": ("computer", "computing", "processor", "calculator", "microcomputer"),
    "physical_descriptions": ("computer", "processor", "calculator", "microcomputer"),
    "entities": ("computer", "processor", "calculator"),
}

ELECTRONICS_FIELD_TERMS = {
    "title": (
        "transistor", ELECTRONICS_INTEGRATED_CIRCUIT_TERM, "semiconductor",
        ELECTRONICS_RADAR_TERM, ELECTRONICS_RECEIVER_TERM,
        ELECTRONICS_TRANSMITTER_TERM, ELECTRONICS_ANTENNA_TERM,
        ELECTRONICS_VOLTMETER_TERM, ELECTRONICS_AMMETER_TERM,
        *ELECTRONICS_ELECTRIC_WATCH_TERMS,
    ),
    "topics": (
        "transistor", ELECTRONICS_INTEGRATED_CIRCUIT_TERM, "semiconductor",
        "electronics", ELECTRONICS_RADAR_TERM,
        *ELECTRONICS_ELECTRIC_WATCH_TERMS,
    ),
    "object_types": (
        "transistor", ELECTRONICS_INTEGRATED_CIRCUIT_TERM, "semiconductor",
        ELECTRONICS_RADAR_TERM, ELECTRONICS_RECEIVER_TERM,
        ELECTRONICS_TRANSMITTER_TERM, ELECTRONICS_ANTENNA_TERM,
        ELECTRONICS_AVIONICS_TERM, ELECTRONICS_COMMUNICATION_SYSTEMS_TERM,
        ELECTRONICS_VOLTMETER_TERM, ELECTRONICS_AMMETER_TERM,
        *ELECTRONICS_ELECTRIC_WATCH_TERMS,
    ),
    "narrative_texts": (
        "transistor", ELECTRONICS_INTEGRATED_CIRCUIT_TERM, "semiconductor", "electronics",
        ELECTRONICS_RADAR_TERM, ELECTRONICS_RADIO_RECEIVER_TERM,
        ELECTRONICS_RADIO_TRANSMITTER_TERM, ELECTRONICS_VOLTMETER_TERM,
        ELECTRONICS_AMMETER_TERM, *ELECTRONICS_ELECTRIC_WATCH_TERMS,
    ),
    "physical_descriptions": (
        "transistor", ELECTRONICS_INTEGRATED_CIRCUIT_TERM, "semiconductor",
        ELECTRONICS_RADAR_TERM, ELECTRONICS_RADIO_RECEIVER_TERM,
        ELECTRONICS_RADIO_TRANSMITTER_TERM, ELECTRONICS_VOLTMETER_TERM,
        ELECTRONICS_AMMETER_TERM, *ELECTRONICS_ELECTRIC_WATCH_TERMS,
    ),
    "entities": ("transistor", "semiconductor"),
}

GUIDANCE_FIELD_TERMS = {
    "title": (
        "guidance", GUIDANCE_NAVIGATION_SYSTEM_TERM, *GUIDANCE_AUTOPILOT_TERMS,
        GUIDANCE_DIRECTIONAL_GYRO_TERM, GUIDANCE_GYROSCOPE_TERM,
        GUIDANCE_RADIO_COMPASS_TERM, GUIDANCE_MAGNETIC_COMPASS_TERM,
        GUIDANCE_COMPASS_TERM, GUIDANCE_DRIFT_METER_TERM,
        GUIDANCE_INCLINOMETER_TERM, GUIDANCE_ASTRODOME_TERM,
    ),
    "topics": (
        "guidance", GUIDANCE_NAVIGATION_SYSTEM_TERM, *GUIDANCE_AUTOPILOT_TERMS,
        GUIDANCE_DIRECTIONAL_GYRO_TERM, GUIDANCE_RADIO_COMPASS_TERM,
        GUIDANCE_COMPASS_TERM, GUIDANCE_DRIFT_METER_TERM,
    ),
    "object_types": (
        "guidance computer", GUIDANCE_NAVIGATION_SYSTEM_TERM, "autopilots",
    ),
    "narrative_texts": (
        "guidance", GUIDANCE_NAVIGATION_SYSTEM_TERM, GUIDANCE_NAVIGATION_EQUIPMENT_TERM,
        *GUIDANCE_AUTOPILOT_TERMS, GUIDANCE_DIRECTIONAL_GYRO_TERM,
        GUIDANCE_GYROSCOPE_TERM, GUIDANCE_RADIO_COMPASS_TERM,
        GUIDANCE_MAGNETIC_COMPASS_TERM, GUIDANCE_COMPASS_TERM,
        GUIDANCE_DRIFT_METER_TERM, GUIDANCE_INCLINOMETER_TERM,
        GUIDANCE_ASTRODOME_TERM,
    ),
    "physical_descriptions": (
        "guidance computer", GUIDANCE_NAVIGATION_SYSTEM_TERM,
        *GUIDANCE_AUTOPILOT_TERMS, GUIDANCE_DIRECTIONAL_GYRO_TERM,
        GUIDANCE_GYROSCOPE_TERM, GUIDANCE_RADIO_COMPASS_TERM,
        GUIDANCE_MAGNETIC_COMPASS_TERM, GUIDANCE_COMPASS_TERM,
        GUIDANCE_DRIFT_METER_TERM, GUIDANCE_INCLINOMETER_TERM,
        GUIDANCE_ASTRODOME_TERM,
    ),
    "entities": (*GUIDANCE_AUTOPILOT_TERMS, GUIDANCE_GYROSCOPE_TERM, "compass"),
}

CONTROL_FIELD_TERMS = {
    "title": (
        CONTROL_FLIGHT_TERM, CONTROL_PANEL_TERM, CONTROL_SYSTEM_TERM,
        "instrumentation", CONTROL_INSTRUMENT_PANEL_TERM,
        CONTROL_G_METER_TERM, CONTROL_ACCELEROMETER_TERM,
        *CONTROL_FLIGHT_INSTRUMENT_TERMS,
    ),
    "topics": (
        CONTROL_FLIGHT_TERM, CONTROL_PANEL_TERM, CONTROL_SYSTEM_TERM,
        "instrumentation", CONTROL_INSTRUMENT_PANEL_TERM,
        CONTROL_G_METER_TERM, CONTROL_ACCELEROMETER_TERM,
        *CONTROL_FLIGHT_INSTRUMENT_TERMS,
    ),
    "object_types": (
        CONTROL_PANEL_TERM, CONTROL_FLIGHT_TERM, CONTROL_FLIGHT_INSTRUMENTS_TERM,
        "instrumentation",
        CONTROL_G_METER_TERM, CONTROL_ACCELEROMETER_TERM,
        *CONTROL_FLIGHT_INSTRUMENT_TERMS,
    ),
    "narrative_texts": (
        CONTROL_FLIGHT_TERM, CONTROL_PANEL_TERM, CONTROL_SYSTEM_TERM,
        "instrumentation", CONTROL_INSTRUMENT_PANEL_TERM,
        CONTROL_G_METER_TERM, CONTROL_ACCELEROMETER_TERM,
        *CONTROL_FLIGHT_INSTRUMENT_TERMS,
    ),
    "physical_descriptions": (
        CONTROL_FLIGHT_TERM, CONTROL_PANEL_TERM, CONTROL_SYSTEM_TERM,
        "instrumentation", CONTROL_INSTRUMENT_PANEL_TERM,
        CONTROL_G_METER_TERM, CONTROL_ACCELEROMETER_TERM,
        *CONTROL_FLIGHT_INSTRUMENT_TERMS,
    ),
    "entities": ("instrumentation",),
}

HUMAN_MACHINE_INTERACTION_KEYBOARD_TERM = "keyboard"
HUMAN_MACHINE_INTERACTION_DISPLAY_UNIT_TERM = "display unit"
HUMAN_MACHINE_INTERACTION_TERMINAL_TERM = "terminal"
HUMAN_MACHINE_INTERACTION_TERMS = (
    HUMAN_MACHINE_INTERACTION_KEYBOARD_TERM,
    "computer display",
    "flight display",
    "cockpit display",
    "electronic display",
    "crt display",
    HUMAN_MACHINE_INTERACTION_DISPLAY_UNIT_TERM,
    "human machine interface",
    "human computer interface",
    "user interface",
    "computer interface",
    HUMAN_MACHINE_INTERACTION_TERMINAL_TERM,
    HUMAN_MACHINE_INTERACTION_TYPEWRITER_TERM,
)
HUMAN_MACHINE_INTERACTION_FIELD_TERMS = {
    "title": HUMAN_MACHINE_INTERACTION_TERMS,
    "topics": HUMAN_MACHINE_INTERACTION_TERMS,
    "object_types": (
        HUMAN_MACHINE_INTERACTION_KEYBOARD_TERM,
        HUMAN_MACHINE_INTERACTION_DISPLAY_UNIT_TERM,
        HUMAN_MACHINE_INTERACTION_TERMINAL_TERM,
        HUMAN_MACHINE_INTERACTION_TYPEWRITER_TERM,
    ),
    "narrative_texts": HUMAN_MACHINE_INTERACTION_TERMS,
    "physical_descriptions": (
        HUMAN_MACHINE_INTERACTION_KEYBOARD_TERM,
        HUMAN_MACHINE_INTERACTION_DISPLAY_UNIT_TERM,
        HUMAN_MACHINE_INTERACTION_TERMINAL_TERM,
        HUMAN_MACHINE_INTERACTION_TYPEWRITER_TERM,
    ),
    "entities": (),
}


DEFAULT_POLICY = CorpusSelectionPolicy(
    version="0.5",
    domain_rules=(
        DomainRule(domain="computing", field_terms=COMPUTING_FIELD_TERMS),
        DomainRule(domain="electronics", field_terms=ELECTRONICS_FIELD_TERMS),
        DomainRule(domain="guidance", field_terms=GUIDANCE_FIELD_TERMS),
        DomainRule(domain="control", field_terms=CONTROL_FIELD_TERMS),
        DomainRule(
            domain="human_machine_interaction",
            field_terms=HUMAN_MACHINE_INTERACTION_FIELD_TERMS,
        ),
    ),
)
