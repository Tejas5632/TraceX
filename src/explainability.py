from __future__ import annotations

from typing import Any, Dict, List

from src.anomaly import detect_patterns
from src.ingestion import load_case


def explain_patterns(case_id: str) -> List[Dict[str, Any]]:
    case = load_case(case_id)
    records = case.get("records", [])
    result = []

    for pattern in detect_patterns(case_id):
        ptype = pattern["pattern_type"]
        entities = pattern.get("entities_involved", [])
        result.append(
            {
                "pattern_type": ptype,
                "severity": pattern.get("severity", "LOW"),
                "entities_involved": entities,
                "why": pattern.get("why", "Pattern observed during review."),
                "explanation": f"This lead was generated from {len(records)} records and is intended for investigative screening.",
                "evidence": pattern.get("evidence", []),
            }
        )

    return result


def get_investigation_timeline(case_id: str) -> List[Dict[str, Any]]:
    case = load_case(case_id)
    events = []
    for record in case.get("records", []):
        events.append(
            {
                "timestamp": record.get("timestamp", "2026-08-01T00:00:00"),
                "event_type": str(record.get("record_type", "EVENT")).upper(),
                "entities": [
                    value for value in [
                        record.get("person"),
                        record.get("caller"),
                        record.get("receiver"),
                        record.get("merchant"),
                        record.get("organization"),
                        record.get("location"),
                    ] if value
                ],
                "description": f"{record.get('record_type', 'Record')} identified in the case file.",
                "record_id": record.get("record_id", "N/A"),
            }
        )
    return sorted(events, key=lambda e: str(e.get("timestamp")))
