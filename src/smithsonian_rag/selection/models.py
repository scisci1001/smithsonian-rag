"""Pydantic contracts for explainable corpus-selection results."""
from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class SelectionModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvidenceClass(StrEnum):
    NARRATIVE = "A"
    STRUCTURED = "B"
    INSUFFICIENT = "C"


class ReasonCode(StrEnum):
    DOMAIN_MATCH = "DOMAIN_MATCH"
    NARRATIVE_EVIDENCE = "NARRATIVE_EVIDENCE"
    STRUCTURED_EVIDENCE = "STRUCTURED_EVIDENCE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    OUT_OF_DOMAIN = "OUT_OF_DOMAIN"


class MatchedTerm(SelectionModel):
    domain: str
    field: str
    term: str


class SelectionResult(SelectionModel):
    record_id: str
    unit_code: str
    accepted: bool
    evidence_class: EvidenceClass
    matched_domains: list[str]
    matched_terms: list[MatchedTerm]
    reason_codes: list[ReasonCode]
    policy_version: str


class UnitSelectionMetrics(SelectionModel):
    input_records: int
    domain_matched: int
    accepted: int
    accepted_narrative: int
    accepted_structured: int
    excluded_insufficient: int
    excluded_out_of_domain: int
    selection_rate: float


class CorpusSelectionReport(SelectionModel):
    policy_version: str
    input_records: int
    domain_matched: int
    accepted: int
    accepted_narrative: int
    accepted_structured: int
    excluded_insufficient: int
    excluded_out_of_domain: int
    selection_rate: float
    by_unit: dict[str, UnitSelectionMetrics]
    reason_code_distribution: dict[str, int]
    results: list[SelectionResult]
