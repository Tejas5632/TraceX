from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def get_available_cases() -> List[str]:
    if not DATA_DIR.exists():
        return []
    return sorted([p.stem for p in DATA_DIR.glob("*.json")])


def load_case(case_id: str) -> Dict[str, Any]:
    path = DATA_DIR / f"{case_id}.json"
    if not path.exists():
        return {
            "case_id": case_id,
            "counts": {"fir": 0, "cdr": 0, "transactions": 0, "social": 0},
            "records": [],
        }

    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    if "counts" not in data:
        data["counts"] = {"fir": 0, "cdr": 0, "transactions": 0, "social": 0}
    if "records" not in data:
        data["records"] = []
    return data
