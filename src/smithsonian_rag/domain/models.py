"""Canonical Smithsonian EDAN domain contracts (v0.1)."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DomainModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TextEntry(DomainModel):
    category: str
    label: str
    content: str


class Entity(DomainModel):
    name: str
    role: str
    source_category: str
    source_label: str


class DateValue(DomainModel):
    value: str
    label: str


class Identifier(DomainModel):
    value: str
    label: str


class RightsInfo(DomainModel):
    access: str = "UNKNOWN"


class MediaAsset(DomainModel):
    media_id: str | None = None
    media_type: str | None = None
    url: str | None = None
    rights: RightsInfo = Field(default_factory=RightsInfo)


class SourceMetadata(DomainModel):
    data_source: str | None = None
    source_record_url: str | None = None
    record_link: str | None = None
    hash: str | None = None
    doc_signature: str | None = None
    last_updated: str | None = None


class SmithsonianRecord(DomainModel):
    record_id: str
    unit_code: str
    title: str
    guid: str | None = None
    source_url: str | None = None
    narrative_texts: list[TextEntry] = Field(default_factory=list)
    physical_descriptions: list[TextEntry] = Field(default_factory=list)
    object_types: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)
    entities: list[Entity] = Field(default_factory=list)
    dates: list[DateValue] = Field(default_factory=list)
    places: list[str] = Field(default_factory=list)
    identifiers: list[Identifier] = Field(default_factory=list)
    media: list[MediaAsset] = Field(default_factory=list)
    metadata_rights: RightsInfo = Field(default_factory=RightsInfo)
    source_metadata: SourceMetadata = Field(default_factory=SourceMetadata)

    @field_validator("record_id", "unit_code", "title")
    @classmethod
    def nonempty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Required identity fields cannot be blank")
        return value
