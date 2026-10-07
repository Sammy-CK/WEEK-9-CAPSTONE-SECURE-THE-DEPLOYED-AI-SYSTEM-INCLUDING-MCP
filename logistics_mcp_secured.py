"""Secured logistics MCP — allowlisted clinics, minimal tool payloads (Week 8 stdio + Week 9)."""
import logging

from mcp.server.fastmcp import FastMCP

from allowlist_stock import check_stock as allowlist_check_stock
from rbac import allowed

logging.basicConfig(
    filename="mcp_server.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

MCP_VERSION = "1.1.0-secured"
mcp = FastMCP("afyaplus-logistics-secured")

LOW_STOCK = {
    ("KSM-01", "ORS"): 40,
    ("VIH-01", "ORS"): 12,
    ("HBA-01", "ORS"): 7,
}
REORDER = 15


@mcp.resource("version://current")
def version_current() -> str:
    return MCP_VERSION


def _minimal_stock(clinic_id: str, item: str) -> dict:
    """Smallest useful dict — no environment dump, no national lists."""
    result = allowlist_check_stock(clinic_id, item)
    if result.get("code"):
        return {"error": result.get("error"), "code": result["code"]}
    return {
        "tool": "check_stock",
        "clinic_id": result["clinic_id"],
        "item": result["item"],
        "qty": result["qty"],
    }


@mcp.tool()
def check_stock(clinic_id: str, item: str = "ORS", caller_role: str = "partner_clinic") -> dict:
    """Check stock for one allowlisted clinic."""
    if not allowed(caller_role, "check_stock"):
        return {"error": "forbidden", "code": 403}
    logging.info("tool=check_stock clinic=%s role=%s", clinic_id, caller_role)
    return _minimal_stock(clinic_id, item)


@mcp.tool()
def list_low_stock(clinic_id: str, caller_role: str = "clinical_ops") -> dict:
    """Low stock for one clinic — clinical_ops only."""
    if not allowed(caller_role, "list_low_stock"):
        return {"error": "forbidden", "code": 403}
    base = _minimal_stock(clinic_id, "ORS")
    if base.get("code"):
        return base
    qty = base.get("qty", 0)
    low = [{"item": "ORS", "qty": qty}] if qty < REORDER else []
    return {"tool": "list_low_stock", "clinic_id": base["clinic_id"], "low_stock": low}


if __name__ == "__main__":
    mcp.run()
