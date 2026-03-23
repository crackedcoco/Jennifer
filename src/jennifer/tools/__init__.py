"""Custom MCP tool servers for Jennifer."""

from claude_agent_sdk import create_sdk_mcp_server, tool

from jennifer.tools.api_client import api_get, api_post
from jennifer.tools.pipeline import run_pipeline
from jennifer.tools.gmail import read_emails, email_digest, read_email_by_id
from jennifer.tools.calendar import daily_agenda, upcoming_events, search_events


# Register tools into an in-process MCP server
jennifer_tools = create_sdk_mcp_server(
    name="jennifer",
    tools=[
        # API
        api_get, api_post, run_pipeline,
        # Gmail
        read_emails, email_digest, read_email_by_id,
        # Calendar
        daily_agenda, upcoming_events, search_events,
    ],
)

TOOL_SERVERS = [jennifer_tools]
