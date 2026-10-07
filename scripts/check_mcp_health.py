"""MCP health: stdio handshake on secured logistics server."""
import asyncio
import sys

EXPECTED_TOOLS = {"check_stock", "list_low_stock"}
EXPECTED_VERSION_PREFIX = "1."


async def handshake() -> int:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(
        command=sys.executable,
        args=["logistics_mcp_secured.py"],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = {t.name for t in (await session.list_tools()).tools}
            ver = await session.read_resource("version://current")
            text = ver.contents[0].text if ver.contents else str(ver)
            print("tools", sorted(tools), "version", text)
            if not EXPECTED_TOOLS.issubset(tools):
                return 1
            if not str(text).strip().startswith(EXPECTED_VERSION_PREFIX):
                return 1
            return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(handshake()))
