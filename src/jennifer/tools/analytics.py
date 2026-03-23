"""Google Analytics tools for Jennifer — create properties, get reports, and inject tracking."""

import json
import re
from pathlib import Path

from claude_agent_sdk import tool
from googleapiclient.discovery import build

from jennifer.tools.google_auth import get_google_credentials


def _get_admin_service():
    creds = get_google_credentials()
    return build("analyticsadmin", "v1beta", credentials=creds)


def _get_data_service():
    creds = get_google_credentials()
    return build("analyticsdata", "v1beta", credentials=creds)


GA4_SNIPPET = """<!-- Google Analytics (GA4) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{measurement_id}');
</script>"""


@tool(description=(
    "List all GA4 accounts and properties you have access to. "
    "Returns account names, property names, measurement IDs, and industries."
))
async def list_ga4_properties() -> str:
    admin = _get_admin_service()
    accounts = admin.accounts().list().execute()

    results = []
    for acc in accounts.get("accounts", []):
        props = admin.properties().list(filter=f"parent:{acc['name']}").execute()
        for p in props.get("properties", []):
            # Try to get data streams for measurement ID
            prop_id = p["name"]
            streams = admin.properties().dataStreams().list(parent=prop_id).execute()
            web_streams = []
            for s in streams.get("dataStreams", []):
                if s.get("type") == "WEB_DATA_STREAM":
                    web_streams.append({
                        "measurement_id": s.get("webStreamData", {}).get("measurementId", ""),
                        "default_uri": s.get("webStreamData", {}).get("defaultUri", ""),
                        "stream_name": s.get("displayName", ""),
                    })

            results.append({
                "account": acc["displayName"],
                "account_id": acc["name"],
                "property": p["displayName"],
                "property_id": p["name"],
                "industry": p.get("industryCategory", ""),
                "time_zone": p.get("timeZone", ""),
                "web_streams": web_streams,
            })

    return json.dumps({"properties": results, "count": len(results)}, indent=2)


@tool(description=(
    "Create a new GA4 property and web data stream. "
    "Specify the account_id (e.g. 'accounts/289325839'), display_name, "
    "website_url, and optionally industry_category and time_zone. "
    "Returns the property ID and measurement ID (G-XXXXXXX)."
))
async def create_ga4_property(
    account_id: str,
    display_name: str,
    website_url: str,
    industry_category: str = "TECHNOLOGY",
    time_zone: str = "America/New_York",
) -> str:
    admin = _get_admin_service()

    # Create property
    property_body = {
        "displayName": display_name,
        "parent": account_id,
        "industryCategory": industry_category,
        "timeZone": time_zone,
    }
    prop = admin.properties().create(body=property_body).execute()
    property_id = prop["name"]

    # Create web data stream
    stream_body = {
        "type": "WEB_DATA_STREAM",
        "displayName": f"{display_name} Web",
        "webStreamData": {
            "defaultUri": website_url,
        },
    }
    stream = admin.properties().dataStreams().create(
        parent=property_id, body=stream_body
    ).execute()

    measurement_id = stream.get("webStreamData", {}).get("measurementId", "")

    return json.dumps({
        "status": "created",
        "property_id": property_id,
        "property_name": display_name,
        "measurement_id": measurement_id,
        "website_url": website_url,
        "snippet": GA4_SNIPPET.format(measurement_id=measurement_id),
    }, indent=2)


@tool(description=(
    "Inject the GA4 tracking snippet into an HTML file or all HTML files in a project directory. "
    "Provide a measurement_id (G-XXXXXXX) and a file or directory path. "
    "Inserts the gtag.js snippet just before </head> in each HTML file."
))
async def inject_ga4_tracking(
    measurement_id: str,
    path: str,
) -> str:
    target = Path(path).expanduser()
    snippet = GA4_SNIPPET.format(measurement_id=measurement_id)
    modified = []
    skipped = []

    if target.is_file():
        html_files = [target]
    elif target.is_dir():
        html_files = list(target.rglob("*.html"))
    else:
        return json.dumps({"error": f"Path not found: {path}"})

    for f in html_files:
        content = f.read_text(errors="replace")

        if measurement_id in content:
            skipped.append(str(f))
            continue

        if "</head>" in content:
            content = content.replace("</head>", f"{snippet}\n</head>", 1)
            f.write_text(content)
            modified.append(str(f))
        elif "</HEAD>" in content:
            content = content.replace("</HEAD>", f"{snippet}\n</HEAD>", 1)
            f.write_text(content)
            modified.append(str(f))
        else:
            skipped.append(str(f))

    return json.dumps({
        "measurement_id": measurement_id,
        "modified": modified,
        "modified_count": len(modified),
        "skipped": skipped,
        "skipped_count": len(skipped),
    }, indent=2)


@tool(description=(
    "Get a traffic report for a GA4 property. "
    "Specify property_id (e.g. 'properties/411489133') and days_back (default 7). "
    "Returns sessions, users, pageviews, top pages, and traffic sources."
))
async def ga4_traffic_report(
    property_id: str,
    days_back: int = 7,
) -> str:
    data = _get_data_service()
    # Strip 'properties/' prefix if included — the API wants just the number in the path
    prop_num = property_id.replace("properties/", "")

    # Overview metrics
    overview = data.properties().runReport(
        property=f"properties/{prop_num}",
        body={
            "dateRanges": [{"startDate": f"{days_back}daysAgo", "endDate": "today"}],
            "metrics": [
                {"name": "sessions"},
                {"name": "totalUsers"},
                {"name": "screenPageViews"},
                {"name": "averageSessionDuration"},
                {"name": "bounceRate"},
            ],
        },
    ).execute()

    metrics = {}
    if overview.get("rows"):
        row = overview["rows"][0]
        metric_headers = [h["name"] for h in overview["metricHeaders"]]
        for i, h in enumerate(metric_headers):
            metrics[h] = row["metricValues"][i]["value"]

    # Top pages
    pages = data.properties().runReport(
        property=f"properties/{prop_num}",
        body={
            "dateRanges": [{"startDate": f"{days_back}daysAgo", "endDate": "today"}],
            "dimensions": [{"name": "pagePath"}],
            "metrics": [{"name": "screenPageViews"}],
            "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
            "limit": 10,
        },
    ).execute()

    top_pages = []
    for row in pages.get("rows", []):
        top_pages.append({
            "page": row["dimensionValues"][0]["value"],
            "views": row["metricValues"][0]["value"],
        })

    # Traffic sources
    sources = data.properties().runReport(
        property=f"properties/{prop_num}",
        body={
            "dateRanges": [{"startDate": f"{days_back}daysAgo", "endDate": "today"}],
            "dimensions": [{"name": "sessionSource"}],
            "metrics": [{"name": "sessions"}],
            "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
            "limit": 10,
        },
    ).execute()

    top_sources = []
    for row in sources.get("rows", []):
        top_sources.append({
            "source": row["dimensionValues"][0]["value"],
            "sessions": row["metricValues"][0]["value"],
        })

    return json.dumps({
        "property_id": property_id,
        "days_back": days_back,
        "overview": metrics,
        "top_pages": top_pages,
        "top_sources": top_sources,
    }, indent=2)
