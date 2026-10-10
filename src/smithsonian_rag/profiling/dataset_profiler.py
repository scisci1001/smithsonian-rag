"""Deterministic profiling of raw Smithsonian EDAN search records."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any


def _items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _has_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _freetext_values(freetext: dict, category: str, labels: set[str] | None = None) -> list[str]:
    values = []
    for entry in _items(freetext.get(category)):
        if not isinstance(entry, dict):
            continue
        label = str(entry.get('label', '')).strip().casefold()
        if (labels is None or label in labels) and _has_text(entry.get('content')):
            values.append(entry['content'])
    return values


NARRATIVE_LABELS = {
    'summary', 'description', 'description (brief)', 'brief description',
    'long description', 'impact or innovation', 'key accomplishment(s)',
}
PHYSICAL_LABELS = {'physical description', 'materials', 'material', 'dimensions', 'measurements'}


def _semantic_text_flags(free: dict[str, Any]) -> dict[str, bool]:
    notes = _freetext_values(free, 'notes', NARRATIVE_LABELS)
    physical_notes = _freetext_values(free, 'notes', PHYSICAL_LABELS)
    physical_fields = _freetext_values(free, 'physicalDescription')
    return {
        'narrative_description': bool(notes),
        'physical_description': bool(physical_notes or physical_fields),
        'total_semantic_text': bool(notes or physical_notes or physical_fields),
    }


def _new_unit_stats() -> dict[str, Any]:
    return {
        'count': 0, 'fields': Counter(), 'freetext_categories': Counter(),
        'freetext_labels': defaultdict(Counter), 'identifier_labels': Counter(),
        'metadata_rights': Counter(), 'media_rights': Counter(),
        'media_types': Counter(), 'media_mismatch_examples': [],
    }


def _field_checks(record: dict[str, Any], dnr: dict[str, Any],
                  structured: dict[str, Any], free: dict[str, Any],
                  media: list[Any]) -> dict[str, bool]:
    declared = bool(_items(structured.get('online_media_type')))
    present = bool(media)
    return {
        **_semantic_text_flags(free),
        'record_id': _has_text(dnr.get('record_ID')),
        'title': _has_text(_mapping(dnr.get('title')).get('content')) or _has_text(record.get('title')),
        'description': bool(_freetext_values(free, 'notes', {'summary', 'description'})),
        'date': bool(_items(structured.get('date'))) or bool(_freetext_values(free, 'date')),
        'name': bool(_items(structured.get('name'))) or bool(_freetext_values(free, 'name')),
        'topic': bool(_items(structured.get('topic'))),
        'object_type': bool(_items(structured.get('object_type'))) or bool(_freetext_values(free, 'objectType')),
        'place': bool(_items(structured.get('place'))) or bool(_freetext_values(free, 'place')),
        'materials': bool(_freetext_values(free, 'physicalDescription', {'materials', 'material'})),
        'declared_media': declared,
        'actual_media': present,
        'declared_without_actual_media': declared and not present,
    }


def _collect_freetext(stats: dict[str, Any], free: dict[str, Any]) -> None:
    for category, entries in free.items():
        if not isinstance(entries, list):
            continue
        stats['freetext_categories'][category] += 1
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            label = str(entry.get('label') or '(missing)').strip()
            stats['freetext_labels'][category][label] += 1
            if category == 'identifier':
                stats['identifier_labels'][label] += 1


def _collect_media(stats: dict[str, Any], media: list[Any]) -> None:
    for asset in media:
        if not isinstance(asset, dict):
            continue
        stats['media_rights'][str(_mapping(asset.get('usage')).get('access') or 'MISSING')] += 1
        stats['media_types'][str(asset.get('type') or 'UNKNOWN')] += 1


def _collect_record(stats: dict[str, Any], record: dict[str, Any],
                    dnr: dict[str, Any], structured: dict[str, Any],
                    free: dict[str, Any]) -> None:
    stats['count'] += 1
    media = _items(_mapping(dnr.get('online_media')).get('media'))
    checks = _field_checks(record, dnr, structured, free, media)
    stats['fields'].update({key: int(value) for key, value in checks.items()})
    _collect_freetext(stats, free)
    stats['metadata_rights'][str(_mapping(dnr.get('metadata_usage')).get('access') or 'MISSING')] += 1
    _collect_media(stats, media)
    if checks['declared_without_actual_media'] and len(stats['media_mismatch_examples']) < 5:
        stats['media_mismatch_examples'].append(str(dnr.get('record_ID') or record.get('id') or 'UNKNOWN'))


def _format_unit_stats(stats: dict[str, Any]) -> dict[str, Any]:
    count = stats['count']
    return {
        'count': count,
        'field_coverage': {
            key: {'count': stats['fields'][key], 'percent': round(100 * stats['fields'][key] / count, 2)}
            for key in sorted(stats['fields'])
        },
        'freetext_categories': dict(sorted(stats['freetext_categories'].items())),
        'freetext_labels': {
            category: dict(sorted(labels.items()))
            for category, labels in sorted(stats['freetext_labels'].items())
        },
        'identifier_labels': dict(sorted(stats['identifier_labels'].items())),
        'metadata_rights': dict(sorted(stats['metadata_rights'].items())),
        'media_rights': dict(sorted(stats['media_rights'].items())),
        'media_types': dict(sorted(stats['media_types'].items())),
        'media_mismatch_examples': stats['media_mismatch_examples'],
    }


def profile_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize field coverage and label distributions per owning unit."""
    units: dict[str, dict[str, Any]] = {}
    seen_ids: set[str] = set()
    duplicate_ids = 0
    for record in records:
        if not isinstance(record, dict):
            raise ValueError('Every input record must be a JSON object')
        content = _mapping(record.get('content'))
        dnr = _mapping(content.get('descriptiveNonRepeating'))
        structured = _mapping(content.get('indexedStructured'))
        free = _mapping(content.get('freetext'))
        unit = str(record.get('unitCode') or dnr.get('unit_code') or 'UNKNOWN')
        stats = units.setdefault(unit, _new_unit_stats())
        rid = dnr.get('record_ID')
        if _has_text(rid):
            duplicate_ids += int(rid in seen_ids)
            seen_ids.add(rid)
        _collect_record(stats, record, dnr, structured, free)

    return {
        'total_records': len(records),
        'duplicate_record_ids': duplicate_ids,
        'units': {unit: _format_unit_stats(units[unit]) for unit in sorted(units)},
    }


def load_records(directory: Path) -> list[dict[str, Any]]:
    if not directory.is_dir():
        raise ValueError(f'Sample directory does not exist: {directory}')
    files = sorted(directory.rglob('*.json'))
    if not files:
        raise ValueError(f'No JSON files found in {directory}')
    records = []
    for file in files:
        try:
            data = json.loads(file.read_text(encoding='utf-8-sig'))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f'Cannot load {file}: {exc}') from exc
        if not isinstance(data, dict):
            raise ValueError(f'Expected one JSON object in {file}')
        records.append(data)
    return records


def main() -> int:
    project_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('samples', nargs='?', type=Path, default=project_root / 'data' / 'samples')
    parser.add_argument('--output', type=Path, default=project_root / 'build' / 'dataset-profile.json')
    args = parser.parse_args()
    try:
        report = profile_records(load_records(args.samples))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Profiling failed: {exc}\n')
    print(f"Total records: {report['total_records']}; duplicate IDs: {report['duplicate_record_ids']}")
    for unit, stats in report['units'].items():
        print(f'\n{unit}: {stats["count"]} records')
        for field, coverage in stats['field_coverage'].items():
            print(f'  {field:30s} {coverage["count"]:4d} ({coverage["percent"]:6.2f}%)')
    print(f'\nJSON report: {args.output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
