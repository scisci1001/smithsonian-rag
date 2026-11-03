"""Deterministic EDAN record mapping with original field labels preserved."""
from __future__ import annotations

from typing import Any

from smithsonian_rag.domain.models import (
    DateValue, Entity, Identifier, MediaAsset, RightsInfo, SmithsonianRecord,
    SourceMetadata, TextEntry,
)

NARRATIVE_LABELS = frozenset({
    "summary", "description", "description (brief)", "brief description",
    "long description", "impact or innovation", "key accomplishment(s)",
})
PHYSICAL_LABELS = frozenset({
    "physical description", "materials", "material", "dimensions", "measurements",
})


def mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def nonblank(value: Any) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def entries(free: dict[str, Any], category: str) -> list[TextEntry]:
    result = []
    for raw in items(free.get(category)):
        entry = mapping(raw)
        content = nonblank(entry.get("content"))
        if content:
            result.append(TextEntry(category=category, label=str(entry.get("label") or ""), content=content))
    return result


def texts(free: dict[str, Any]) -> tuple[list[TextEntry], list[TextEntry]]:
    narrative, physical = [], []
    for category in ("notes", "physicalDescription"):
        for entry in entries(free, category):
            label = entry.label.strip().casefold()
            if label in NARRATIVE_LABELS:
                narrative.append(entry)
            elif label in PHYSICAL_LABELS:
                physical.append(entry)
    return narrative, physical


def strings(value: Any) -> list[str]:
    return [s for s in items(value) if nonblank(s)]


def entities(free: dict[str, Any]) -> list[Entity]:
    return [Entity(name=e.content, role=e.label.strip().casefold(),
                   source_category=e.category, source_label=e.label)
            for e in entries(free, "name")]


def media_assets(dnr: dict[str, Any]) -> list[MediaAsset]:
    result = []
    for raw in items(mapping(dnr.get("online_media")).get("media")):
        asset = mapping(raw)
        if not asset:
            continue
        result.append(MediaAsset(
            media_id=nonblank(asset.get("id")),
            media_type=nonblank(asset.get("type")),
            url=nonblank(asset.get("content")),
            rights=RightsInfo(access=str(mapping(asset.get("usage")).get("access") or "UNKNOWN")),
        ))
    return result


def normalize(record: dict[str, Any], expected_unit: str | None = None) -> SmithsonianRecord:
    """Normalize one full EDAN search row; never mutate the raw record."""
    if not isinstance(record, dict):
        raise ValueError("EDAN record must be an object")
    content = mapping(record.get("content"))
    dnr = mapping(content.get("descriptiveNonRepeating"))
    free = mapping(content.get("freetext"))
    structured = mapping(content.get("indexedStructured"))
    unit = nonblank(record.get("unitCode")) or nonblank(dnr.get("unit_code")) or ""
    if expected_unit is not None and unit != expected_unit:
        raise ValueError(f"Expected unit {expected_unit}, got {unit}")
    narrative, physical = texts(free)
    raw_title = mapping(dnr.get("title")).get("content")
    dates = [DateValue(value=e.content, label=e.label) for e in entries(free, "date")]
    if not dates:
        dates = [DateValue(value=s, label="indexedStructured.date") for s in strings(structured.get("date"))]
    return SmithsonianRecord(
        record_id=nonblank(dnr.get("record_ID")) or "",
        unit_code=unit,
        title=nonblank(raw_title) or nonblank(record.get("title")) or "",
        guid=nonblank(dnr.get("guid")),
        source_url=nonblank(dnr.get("record_link")) or nonblank(dnr.get("guid")),
        narrative_texts=narrative,
        physical_descriptions=physical,
        object_types=strings(structured.get("object_type")) or [e.content for e in entries(free, "objectType")],
        topics=strings(structured.get("topic")),
        entities=entities(free),
        dates=dates,
        places=strings(structured.get("place")) or [e.content for e in entries(free, "place")],
        identifiers=[Identifier(value=e.content, label=e.label) for e in entries(free, "identifier")],
        media=media_assets(dnr),
        metadata_rights=RightsInfo(access=str(mapping(dnr.get("metadata_usage")).get("access") or "UNKNOWN")),
        source_metadata=SourceMetadata(
            data_source=nonblank(dnr.get("data_source")),
            source_record_url=nonblank(record.get("url")),
            record_link=nonblank(dnr.get("record_link")),
            hash=nonblank(record.get("hash")),
            doc_signature=nonblank(record.get("docSignature")),
            last_updated=str(record["lastTimeUpdated"]) if record.get("lastTimeUpdated") is not None else None,
        ),
    )
