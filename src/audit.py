from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

AUDIT_LOG = Path(__file__).resolve().parent.parent / ".audit_log.jsonl"


def append_audit_event(action: str, case_id: str, actor: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    record = {
        "timestamp": __import__("datetime").datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "action": action,
        "case_id": case_id,
        "actor": actor,
        "payload": payload,
    }
    if AUDIT_LOG.exists():
        previous = AUDIT_LOG.read_text(encoding="utf-8").strip().splitlines()[-1:]
        if previous:
            prev = json.loads(previous[0])
            record["previous_hash"] = prev.get("hash")
    record["hash"] = hashlib.sha256(json.dumps(record, sort_keys=True).encode("utf-8")).hexdigest()
    with AUDIT_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def get_audit_log(limit: int = 20) -> List[Dict[str, Any]]:
    if not AUDIT_LOG.exists():
        return []
    lines = AUDIT_LOG.read_text(encoding="utf-8").strip().splitlines()
    result = []
    for line in lines[-limit:]:
        if line.strip():
            result.append(json.loads(line))
    return result


def verify_audit_chain() -> bool:
    logs = get_audit_log(1000)
    previous_hash = None
    for entry in logs:
        if previous_hash is not None and entry.get("previous_hash") != previous_hash:
            return False
        candidate = {
            key: value for key, value in entry.items() if key != "hash"
        }
        digest = hashlib.sha256(json.dumps(candidate, sort_keys=True).encode("utf-8")).hexdigest()
        previous_hash = entry.get("hash")
        if entry.get("hash") != digest:
            return False
    return True
