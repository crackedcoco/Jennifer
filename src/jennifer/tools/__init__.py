"""Custom MCP tool servers for Jennifer."""

from claude_agent_sdk import create_sdk_mcp_server, tool

from jennifer.tools.api_client import api_get, api_post
from jennifer.tools.pipeline import run_pipeline
from jennifer.tools.gmail import read_emails, email_digest, read_email_by_id
from jennifer.tools.gmail_send import send_email, reply_to_email, list_send_as_aliases
from jennifer.tools.calendar import daily_agenda, upcoming_events, search_events
from jennifer.tools.analytics import list_ga4_properties, create_ga4_property, inject_ga4_tracking, ga4_traffic_report
from jennifer.tools.monitoring import check_endpoints


# Register tools into an in-process MCP server
jennifer_tools = create_sdk_mcp_server(
    name="jennifer",
    tools=[
        # API
        api_get, api_post, run_pipeline,
        # Gmail — read
        read_emails, email_digest, read_email_by_id,
        # Gmail — send
        send_email, reply_to_email, list_send_as_aliases,
        # Calendar
        daily_agenda, upcoming_events, search_events,
        # Analytics
        list_ga4_properties, create_ga4_property, inject_ga4_tracking, ga4_traffic_report,
        # Monitoring
        check_endpoints,
    ],
)

TOOL_SERVERS = [jennifer_tools]
