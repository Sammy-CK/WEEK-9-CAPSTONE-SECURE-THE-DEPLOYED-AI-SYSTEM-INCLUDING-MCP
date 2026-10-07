# Week 9: AI Security and Compliance

## Overview

This capstone **locks the AfyaPlus triage API and logistics MCP** built in Weeks 6–8: TLS and secret hygiene, JWT on `/triage`, injection blocking, RBAC and clinic allowlists on MCP tools, redacted audit logs, and Kenya **Data Protection Act** teaching artefacts. The manager-facing summary is in [manager_brief.md](manager_brief.md).

## Encryption

- **transit_ok / TLS evidence:** [transit_policy.py](transit_policy.py); pytest denies `http://api.afyaplus.ke/...`; localhost HTTP documented as lab-only.
- **gitignore / resolve_secrets:** [check_gitignore.py](check_gitignore.py), [docker-compose.yml](docker-compose.yml) uses `${JWT_SECRET}`; [resolve_secrets.py](resolve_secrets.py) exits **1** without secret — see `evidence/resolve_secrets_fail.log`.
- **Key Vault or KMS fallback:** [secret_refs.yaml](secret_refs.yaml), [kms_twin.json](kms_twin.json) (Azure **and** AWS columns), [encrypt_at_rest.py](encrypt_at_rest.py), [envelope_notes.md](envelope_notes.md).

## Access control (including MCP)

- **rbac.py roles:** `partner_clinic` → `check_stock`; `clinical_ops` → `check_stock`, `list_low_stock`, `plan_delivery_route`; unknown denied — [tests/test_rbac.py](tests/test_rbac.py).
- **injection_guard:** [injection_guard.py](injection_guard.py) → **400** before model/tools; wired in [secure_triage_app.py](secure_triage_app.py).
- **clinic allowlist:** [clinics_allowlist.json](clinics_allowlist.json), [allowlist_stock.py](allowlist_stock.py), stdio [logistics_mcp_secured.py](logistics_mcp_secured.py); safe sample [mcp_tool_response_fixed.json](mcp_tool_response_fixed.json) vs leak sample.

**Week 6–8 reuse:** JWT login pattern from Week 6 `auth.py`; `/health` and prompt **1.2.0** from Week 8; MCP stdio pattern from Week 8 with Week 9 hardening.

## Versioned prompts (Week 8 lineage)

- Production: [prompts/triage_system_v1.2.0.txt](prompts/triage_system_v1.2.0.txt) — full AfyaPlus triage rules (never diagnose, urgency bands, injection-aware).
- Candidate: [prompts/triage_system_v1.3.0-candidate.txt](prompts/triage_system_v1.3.0-candidate.txt) for staged A/B only.
- Pin: [prompts/pin.json](prompts/pin.json); `/health` reports SHA and pin match.

## Logging

- **jsonl path:** `logs/audit_stacked.jsonl` (gitignored); sample line in [evidence/audit_sample.json](evidence/audit_sample.json).
- **redact and hash:** [redact_then_hash.py](redact_then_hash.py) stacks [redact.py](redact.py) then SHA-256 prefix; includes `actor`, `action`, `resource`, `ok`, `trace_id`.

## Kenya DPA

- **inventory:** [data_inventory.json](data_inventory.json) — triage messages, jwt subjects, MCP queries, audit logs.
- **retention:** [retention.json](retention.json); sweeper [retention_sweep.py](retention_sweep.py) → [deletion_records.jsonl](deletion_records.jsonl) (deletion records are never removed by the sweep).
- **rights stub / owner:** [rights_lookup.py](rights_lookup.py) + [fixtures/subjects.json](fixtures/subjects.json); access/erasure owner named in [manager_brief.md](manager_brief.md). **Legal review pending** on `lawful_basis` teaching labels.

## Manager brief

[manager_brief.md](manager_brief.md) — headings **Risks**, **Mitigations**, **Kenya DPA alignment**, **What we will not claim**. Word **unhackable** does not appear ([check_brief.py](check_brief.py)).

## Fallbacks declared

- [x] no Azure Key Vault (local-env plus the twin JSON)
- [x] no AWS account (twin JSON only)
- [x] secured stdio MCP (not a separate cloud MCP host)
- [x] legal review pending on lawful_basis

## Checklist

- [x] Secrets not in git
- [x] MCP cannot dump the environment or every clinic
- [x] The brief is readable by a non-engineer

## Evidence

Local and CI: `pytest`, `check_inventory.py`, `check_brief.py`, `check_corpus_pin.py`, `check_gitignore.py`, `scripts/check_mcp_health.py`. GitHub Actions: [workflows](https://github.com/Sammy-CK/WEEK-9-CAPSTONE-SECURE-THE-DEPLOYED-AI-SYSTEM-INCLUDING-MCP/actions) (job **ci-security**).

**CI and secrets:** `.github/workflows/ci.yml` sets a **disposable test** `JWT_SECRET` in job `env` so pytest can run on GitHub — this is not a production key and is not stored in `.env` or git history as a real credential. Production uses `secret_refs.yaml` + host/Key Vault injection; `check_gitignore.py` blocks committing `.env`.

## Author

Sammy — Week 9 security capstone.
