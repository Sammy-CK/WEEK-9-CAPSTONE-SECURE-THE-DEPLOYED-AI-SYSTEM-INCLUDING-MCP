"""Secured AfyaPlus triage API — Week 6 JWT, Week 8 health, Week 9 guard + audit."""
import hashlib
import uuid
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from auth import current_user
from injection_guard import triage_or_reject
from redact_then_hash import write_redact_then_hash

PROMPTS_DIR = Path("prompts")
PROMPT_VERSION = "1.2.0"
SERVICE_VERSION = "9.0.0-secured"

app = FastAPI(title="AfyaPlus Triage (secured)", version=SERVICE_VERSION)


def prompt_sha() -> str:
    path = PROMPTS_DIR / f"triage_system_v{PROMPT_VERSION}.txt"
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        return hashlib.sha256(text.encode()).hexdigest()
    return "missing"


class TriageIn(BaseModel):
    patient_message: str = Field(..., min_length=1, max_length=2000)


class LoginIn(BaseModel):
    username: str
    password: str


@app.get("/health")
def health():
    pin_path = Path("prompts/pin.json")
    pin_sha = None
    if pin_path.is_file():
        import json

        pin_sha = json.loads(pin_path.read_text(encoding="utf-8")).get("prompt_sha256")
    sha = prompt_sha()
    return {
        "status": "ok",
        "service": "afyaplus-triage-secured",
        "prompt_version": PROMPT_VERSION,
        "prompt_sha256": sha,
        "prompt_pin_match": pin_sha == sha if pin_sha else None,
        "mcp_server": "logistics_mcp_secured.py",
        "image_tag": "afyaplus-triage-secured:9.0.0",
    }


@app.post("/login")
def login(body: LoginIn):
    from auth import check_password, create_token

    if not check_password(body.username, body.password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return {"access_token": create_token(body.username), "token_type": "bearer"}


@app.post("/triage")
def triage(body: TriageIn, user: dict = Depends(current_user)):
    gate = triage_or_reject(body.patient_message)
    if gate.get("code") == 400:
        write_redact_then_hash(
            user.get("mcp_role", "unknown"),
            "triage_rejected",
            "triage_messages",
            body.patient_message,
            ok=False,
        )
        raise HTTPException(status_code=400, detail="Message rejected by injection guard.")
    trace = str(uuid.uuid4())
    write_redact_then_hash(
        user.get("mcp_role", "unknown"),
        "triage_stub",
        "triage_messages",
        body.patient_message,
        ok=True,
        trace_id=trace,
    )
    return {
        "advice": "(stub — no live model call in Week 9 capstone)",
        "prompt_version": PROMPT_VERSION,
        "trace_id": trace,
        "disclaimer": "Not a diagnosis.",
    }
