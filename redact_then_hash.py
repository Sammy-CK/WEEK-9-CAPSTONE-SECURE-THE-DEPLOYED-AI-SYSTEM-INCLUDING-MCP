"""Stacked pipeline: redact the payload, then hash what remains for correlation."""
import hashlib
import json
from pathlib import Path

from redact import redact

LOG = Path("logs/audit_stacked.jsonl")


def write_redact_then_hash(
    actor: str,
    action: str,
    resource: str,
    payload: str,
    ok: bool = True,
    trace_id: str | None = None,
) -> dict:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    cleaned = redact(payload)
    row = {
        "actor": actor,
        "action": action,
        "resource": resource,
        "ok": ok,
        "trace_id": trace_id,
        "payload_redacted": cleaned,
        "payload_sha": hashlib.sha256(cleaned.encode()).hexdigest()[:16],
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return row


if __name__ == "__main__":
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("", encoding="utf-8")
    row = write_redact_then_hash(
        "partner_clinic",
        "check_stock",
        "KSM-01",
        "national id 87654321 Bearer eyJ.demo",
        trace_id="demo-trace",
    )
    assert "87654321" not in row["payload_redacted"]
    assert "eyJ" not in row["payload_redacted"]
    assert len(row["payload_sha"]) == 16
    print("redact_then_hash OK", row)
