"""NASM-specific normalization entrypoint."""
from typing import Any
from smithsonian_rag.domain.models import SmithsonianRecord
from smithsonian_rag.normalization.common import normalize


def normalize_nasm(record: dict[str, Any]) -> SmithsonianRecord:
    return normalize(record, expected_unit="NASM")
