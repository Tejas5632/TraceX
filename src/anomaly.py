from __future__ import annotations

from typing import Any, Dict, List

from src.ingestion import load_case


def detect_patterns(case_id: str) -> List[Dict[str, Any]]:
    case = load_case(case_id)
    records = case.get("records", [])
    patterns: List[Dict[str, Any]] = []

    # simplistic demo logic: flag if the case has both calls and payments
    if any(r.get("record_type") == "CDR" for r in records) and any(r.get("record_type") == "TRANSACTION" for r in records):
        patterns.append(
            {
                "pattern_type": "CALL_FOLLOWED_BY_TRANSACTION",
                "severity": "HIGH",
                "entities_involved": ["PERSON_001", "PERSON_002"],
                "why": "Calls and financial transfers co-occur in the same case window.",
                "evidence": {"call_record_id": "CDR_001", "payment_record_id": "TX_001"},
            }
        )

    if len(records) >= 8:
        patterns.append(
            {
                "pattern_type": "HIGH_CONNECTIVITY",
                "severity": "MEDIUM",
                "entities_involved": ["PERSON_001", "PERSON_002"],
                "why": "Multiple interactions indicate a dense connection cluster.",
                "evidence": {"sample_record_ids": [r.get("record_id") for r in records[:3] if r.get("record_id")]},
            }
        )

    return patterns
