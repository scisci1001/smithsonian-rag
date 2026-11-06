"""Deterministic selector and aggregate report for canonical records."""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Any

from smithsonian_rag.domain.models import SmithsonianRecord
from smithsonian_rag.selection.models import (
    CorpusSelectionReport,
    EvidenceClass,
    MatchedTerm,
    ReasonCode,
    SelectionResult,
    UnitSelectionMetrics,
)
from smithsonian_rag.selection.policy import CorpusSelectionPolicy, DEFAULT_POLICY


def _plain_text(value: Any) -> str:
    """Extract searchable text from a canonical field value."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif hasattr(item, "content"):
                parts.append(str(item.content))
            elif hasattr(item, "name"):
                parts.append(str(item.name))
        return " ".join(parts)
    return ""


def _normalized(text: str) -> str:
    """Fold punctuation and case while retaining Unicode word characters."""
    return re.sub(r"[^\w]+", " ", text.casefold(), flags=re.UNICODE).strip()


def _has_term(text: str, term: str) -> bool:
    normalized_text = f" {_normalized(text)} "
    normalized_term = f" {_normalized(term)} "
    return normalized_term in normalized_text


def _has_evidence(value: Any) -> bool:
    """Return whether a canonical field value contains searchable evidence."""
    if isinstance(value, str):
        return bool(value.strip())
    if not isinstance(value, list):
        return False
    for item in value:
        if isinstance(item, str) and item.strip():
            return True
        if any(
            isinstance(text := getattr(item, attribute, None), str) and text.strip()
            for attribute in ("content", "name", "value")
        ):
            return True
    return False


class CorpusSelector:
    """Select records using a versioned policy with explicit reason codes."""

    def __init__(self, policy: CorpusSelectionPolicy = DEFAULT_POLICY) -> None:
        self.policy = policy

    def _matched_terms(self, record: SmithsonianRecord) -> list[MatchedTerm]:
        if record.unit_code not in self.policy.supported_units:
            return []
        matches: list[MatchedTerm] = []
        for rule in self.policy.domain_rules:
            for field_name, terms in rule.field_terms.items():
                value = _plain_text(getattr(record, field_name))
                matches.extend(
                    MatchedTerm(domain=rule.domain, field=field_name, term=term)
                    for term in terms
                    if _has_term(value, term)
                )
        return matches

    def _has_structured_evidence(self, record: SmithsonianRecord) -> bool:
        return any(
            _has_evidence(getattr(record, field_name))
            for field_name in self.policy.evidence_fields
        )

    def select(self, record: SmithsonianRecord) -> SelectionResult:
        """Classify and decide one canonical record."""
        matched_terms = self._matched_terms(record)
        domains = list(dict.fromkeys(match.domain for match in matched_terms))
        has_narrative = any(text.content.strip() for text in record.narrative_texts)
        has_structured = self._has_structured_evidence(record)
        if has_narrative:
            evidence_class = EvidenceClass.NARRATIVE
        elif has_structured:
            evidence_class = EvidenceClass.STRUCTURED
        else:
            evidence_class = EvidenceClass.INSUFFICIENT

        reasons: list[ReasonCode] = []
        if domains:
            reasons.append(ReasonCode.DOMAIN_MATCH)
            reasons.append({
                EvidenceClass.NARRATIVE: ReasonCode.NARRATIVE_EVIDENCE,
                EvidenceClass.STRUCTURED: ReasonCode.STRUCTURED_EVIDENCE,
                EvidenceClass.INSUFFICIENT: ReasonCode.INSUFFICIENT_EVIDENCE,
            }[evidence_class])
        else:
            reasons.append(ReasonCode.OUT_OF_DOMAIN)
        accepted = bool(domains) and evidence_class is not EvidenceClass.INSUFFICIENT
        return SelectionResult(
            record_id=record.record_id,
            unit_code=record.unit_code,
            accepted=accepted,
            evidence_class=evidence_class,
            matched_domains=domains,
            matched_terms=matched_terms,
            reason_codes=reasons,
            policy_version=self.policy.version,
        )

    def select_many(self, records: list[SmithsonianRecord]) -> CorpusSelectionReport:
        """Select records in input order and return corpus and unit metrics."""
        results = [self.select(record) for record in records]
        reason_counts: Counter[str] = Counter()
        by_unit_results: dict[str, list[SelectionResult]] = defaultdict(list)
        for result in results:
            by_unit_results[result.unit_code].append(result)
            reason_counts.update(code.value for code in result.reason_codes)

        def unit_metrics(unit_results: list[SelectionResult]) -> UnitSelectionMetrics:
            matched = sum(bool(result.matched_domains) for result in unit_results)
            accepted = sum(result.accepted for result in unit_results)
            narrative = sum(result.accepted and result.evidence_class is EvidenceClass.NARRATIVE for result in unit_results)
            structured = sum(result.accepted and result.evidence_class is EvidenceClass.STRUCTURED for result in unit_results)
            insufficient = sum(
                bool(result.matched_domains) and result.evidence_class is EvidenceClass.INSUFFICIENT
                for result in unit_results
            )
            out_of_domain = sum(not result.matched_domains for result in unit_results)
            total = len(unit_results)
            return UnitSelectionMetrics(
                input_records=total,
                domain_matched=matched,
                accepted=accepted,
                accepted_narrative=narrative,
                accepted_structured=structured,
                excluded_insufficient=insufficient,
                excluded_out_of_domain=out_of_domain,
                selection_rate=accepted / total if total else 0.0,
            )

        overall = unit_metrics(results)
        return CorpusSelectionReport(
            policy_version=self.policy.version,
            input_records=overall.input_records,
            domain_matched=overall.domain_matched,
            accepted=overall.accepted,
            accepted_narrative=overall.accepted_narrative,
            accepted_structured=overall.accepted_structured,
            excluded_insufficient=overall.excluded_insufficient,
            excluded_out_of_domain=overall.excluded_out_of_domain,
            selection_rate=overall.selection_rate,
            by_unit={unit: unit_metrics(items) for unit, items in sorted(by_unit_results.items())},
            reason_code_distribution=dict(sorted(reason_counts.items())),
            results=results,
        )
