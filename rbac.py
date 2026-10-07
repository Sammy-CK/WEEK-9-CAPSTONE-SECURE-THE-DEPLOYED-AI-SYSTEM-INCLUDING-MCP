"""Application-level authorisation: which role may call which MCP tool."""
TOOLS_BY_ROLE = {
    "partner_clinic": {"check_stock"},
    "clinical_ops": {"check_stock", "list_low_stock", "plan_delivery_route"},
}


def allowed(role: str, tool: str) -> bool:
    return tool in TOOLS_BY_ROLE.get(role, set())


if __name__ == '__main__':
    assert allowed('partner_clinic', 'check_stock')
    assert not allowed('partner_clinic', 'plan_delivery_route')
    assert not allowed('unknown', 'check_stock')
    assert not allowed('clinical_ops', 'dump_all')
    print('rbac OK')