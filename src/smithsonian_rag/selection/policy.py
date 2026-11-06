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
GUIDANCE_NAVIGATION_SYSTEM_TERM = "navigation system"
CONTROL_PANEL_TERM = "control panel"
CONTROL_SYSTEM_TERM = "control system"
CONTROL_FLIGHT_TERM = "flight control"


COMPUTING_FIELD_TERMS = {
    "title": ("computer", "processor", "calculator", "microcomputer"),
    "topics": ("computer", "computing", "processor", "calculator", "microcomputer"),
    "object_types": ("computer", "calculator", "microcomputer"),
    "narrative_texts": ("computer", "computing", "processor", "calculator", "microcomputer"),
    "physical_descriptions": ("computer", "processor", "calculator", "microcomputer"),
    "entities": ("computer", "processor", "calculator"),
}

ELECTRONICS_FIELD_TERMS = {
    "title": ("transistor", ELECTRONICS_INTEGRATED_CIRCUIT_TERM, "semiconductor"),
    "topics": ("transistor", ELECTRONICS_INTEGRATED_CIRCUIT_TERM, "semiconductor", "electronics"),
    "object_types": ("transistor", ELECTRONICS_INTEGRATED_CIRCUIT_TERM, "semiconductor"),
    "narrative_texts": ("transistor", ELECTRONICS_INTEGRATED_CIRCUIT_TERM, "semiconductor", "electronics"),
    "physical_descriptions": ("transistor", ELECTRONICS_INTEGRATED_CIRCUIT_TERM, "semiconductor"),
    "entities": ("transistor", "semiconductor"),
}

GUIDANCE_FIELD_TERMS = {
    "title": ("guidance", GUIDANCE_NAVIGATION_SYSTEM_TERM, "autopilot"),
    "topics": ("guidance", GUIDANCE_NAVIGATION_SYSTEM_TERM, "autopilot"),
    "object_types": ("guidance computer", GUIDANCE_NAVIGATION_SYSTEM_TERM, "autopilot"),
    "narrative_texts": ("guidance", GUIDANCE_NAVIGATION_SYSTEM_TERM, "autopilot"),
    "physical_descriptions": ("guidance computer", GUIDANCE_NAVIGATION_SYSTEM_TERM, "autopilot"),
    "entities": ("autopilot",),
}

CONTROL_FIELD_TERMS = {
    "title": (CONTROL_FLIGHT_TERM, CONTROL_PANEL_TERM, CONTROL_SYSTEM_TERM, "instrumentation"),
    "topics": (CONTROL_FLIGHT_TERM, CONTROL_PANEL_TERM, CONTROL_SYSTEM_TERM, "instrumentation"),
    "object_types": (CONTROL_PANEL_TERM, CONTROL_FLIGHT_TERM, "instrumentation"),
    "narrative_texts": (CONTROL_FLIGHT_TERM, CONTROL_PANEL_TERM, CONTROL_SYSTEM_TERM, "instrumentation"),
    "physical_descriptions": (CONTROL_FLIGHT_TERM, CONTROL_PANEL_TERM, CONTROL_SYSTEM_TERM, "instrumentation"),
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
)
HUMAN_MACHINE_INTERACTION_FIELD_TERMS = {
    "title": HUMAN_MACHINE_INTERACTION_TERMS,
    "topics": HUMAN_MACHINE_INTERACTION_TERMS,
    "object_types": (
        HUMAN_MACHINE_INTERACTION_KEYBOARD_TERM,
        HUMAN_MACHINE_INTERACTION_DISPLAY_UNIT_TERM,
        HUMAN_MACHINE_INTERACTION_TERMINAL_TERM,
    ),
    "narrative_texts": HUMAN_MACHINE_INTERACTION_TERMS,
    "physical_descriptions": (
        HUMAN_MACHINE_INTERACTION_KEYBOARD_TERM,
        HUMAN_MACHINE_INTERACTION_DISPLAY_UNIT_TERM,
        HUMAN_MACHINE_INTERACTION_TERMINAL_TERM,
    ),
    "entities": (),
}


DEFAULT_POLICY = CorpusSelectionPolicy(
    version="0.1",
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
