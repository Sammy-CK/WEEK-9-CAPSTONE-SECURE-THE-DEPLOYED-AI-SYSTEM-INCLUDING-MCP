# Security summary for managers — AfyaPlus (Week 9)

Plain-language packet for BenkiYetu security and clinic leadership. **Legal review pending** on lawful-basis labels in `data_inventory.json`.

## Risks

- Patient triage messages could leak if logs store full text or ID numbers.
- Weak transport (plain HTTP to partners) could expose tokens in transit.
- Secrets in git or Docker files could let attackers forge clinic access.
- The logistics MCP could return too much data (for example every clinic or server secrets).
- Prompt-injection text could trick the model into unsafe advice.
- Credit or payment decisions must not be automated from triage output.

## Mitigations

- **HTTPS for partners:** `transit_policy.py` blocks cleartext production URLs; lab localhost HTTP is documented only.
- **Secrets out of git:** `check_gitignore.py` and `compose.secrets.yml` use `${JWT_SECRET}`; values load via `resolve_secrets.py` and `secret_refs.yaml` / `kms_twin.json`.
- **Encryption at rest (design):** `encrypt_at_rest.py` and `envelope_notes.md` describe volume encryption with keys in Key Vault or AWS KMS (twin card in repo; we use local env in this capstone).
- **Login still required:** `auth.py` and `secure_triage_app.py` require JWT on `/triage` (Week 6 pattern retained).
- **Role limits:** `rbac.py` separates partner tools from operations tools; unknown roles are denied.
- **MCP allowlist:** `clinics_allowlist.json`, `allowlist_stock.py`, and `logistics_mcp_secured.py` return small dictionaries; compare `mcp_tool_response_fixed.json` vs the leak sample.
- **Injection blocked early:** `injection_guard.py` returns 400 before any stub model call.
- **Safe audit logs:** `redact_then_hash.py` writes `logs/audit_stacked.jsonl` with redacted text and a hash, not raw Bearer tokens.
- **Kenya DPA records:** `data_inventory.json`, `retention.json`, `retention_sweep.py`, `deletion_records.jsonl`, and `rights_lookup.py` (access/erasure owner: **Data Protection Lead — Sammy / clinical_ops delegate**).

## Kenya DPA alignment

We mapped personal and health-adjacent data in `data_inventory.json`, set retention in `retention.json`, and run a **stub sweeper** (`retention_sweep.py`) that drops expired triage rows and **appends** a deletion record (the sweep never deletes those records). Subject access counts use `rights_lookup.py` without returning message content. Lawful basis fields are **teaching labels only** — not legal sign-off.

## What we will not claim

- We do **not** claim the system is immune to all attacks or fully certified by ODPC.
- We do **not** store live production patient data in this repository.
- We do **not** auto-approve loans or credit: triage is advisory only.

### Finance and credit (recommend, not decide)

AfyaPlus may **recommend** that a partner review a case for follow-up finance products, but **only a licensed human credit officer decides** approval, limits, and terms. The AI output must not trigger transfers or credit on its own.
