"""Deterministic corpus-selection policy and reporting."""

from smithsonian_rag.selection.corpus_selector import CorpusSelector
from smithsonian_rag.selection.models import (
    CorpusSelectionReport,
    EvidenceClass,
    MatchedTerm,
    ReasonCode,
    SelectionResult,
)
from smithsonian_rag.selection.policy import DEFAULT_POLICY, CorpusSelectionPolicy

__all__ = [
    "CorpusSelectionPolicy",
    "CorpusSelectionReport",
    "CorpusSelector",
    "DEFAULT_POLICY",
    "EvidenceClass",
    "MatchedTerm",
    "ReasonCode",
    "SelectionResult",
]
