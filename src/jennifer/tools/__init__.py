"""Custom MCP tool servers for Jennifer."""

from claude_agent_sdk import create_sdk_mcp_server, tool

from jennifer.tools.api_client import api_get, api_post
from jennifer.tools.pipeline import run_pipeline


# Register tools into an in-process MCP server
jennifer_tools = create_sdk_mcp_server(
    name="jennifer",
    tools=[api_get, api_post, run_pipeline],
)

TOOL_SERVERS = [jennifer_tools]
