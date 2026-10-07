# Week 9 local evidence

| Gate | Result |
|------|--------|
| pytest | 11 passed |
| check_inventory.py | OK |
| check_brief.py | OK |
| check_corpus_pin.py | OK |
| check_gitignore.py | OK |
| check_mcp_health.py | OK |
| resolve_secrets (no JWT) | exit 1 — `resolve_secrets_fail.log` |
| transit cleartext host | `tests/test_transit_policy.py` |
| injection 400 | `tests/test_injection_guard.py` |

## GitHub

- **Repository:** https://github.com/Sammy-CK/WEEK-9-CAPSTONE-SECURE-THE-DEPLOYED-AI-SYSTEM-INCLUDING-MCP
- **Actions (all runs):** https://github.com/Sammy-CK/WEEK-9-CAPSTONE-SECURE-THE-DEPLOYED-AI-SYSTEM-INCLUDING-MCP/actions

After the first push, open the latest **ci-security** run on that page and confirm green (job-level env uses the documented CI test JWT only).
