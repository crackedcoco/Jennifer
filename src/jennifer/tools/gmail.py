"""Gmail tools for Jennifer — read, search, and categorize emails."""

import base64
import json
from email.utils import parsedate_to_datetime

from claude_agent_sdk import tool
from googleapiclient.discovery import build

from jennifer.tools.google_auth import get_google_credentials


def _get_gmail_service():
    creds = get_google_credentials()
    return build("gmail", "v1", credentials=creds)


def _parse_message(service, msg_id: str, include_body: bool = True) -> dict:
    """Parse a Gmail message into a clean dict."""
    msg = service.users().messages().get(
        userId="me", id=msg_id, format="full"
    ).execute()

    headers = {h["name"].lower(): h["value"] for h in msg["payload"]["headers"]}

    result = {
        "id": msg_id,
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "subject": headers.get("subject", ""),
        "date": headers.get("date", ""),
        "labels": msg.get("labelIds", []),
        "snippet": msg.get("snippet", ""),
        "has_attachments": False,
    }

    # Check for attachments
    parts = msg["payload"].get("parts", [])
    for part in parts:
        if part.get("filename"):
            result["has_attachments"] = True
            break

    # Extract body if requested
    if include_body:
        body = _extract_body(msg["payload"])
        result["body"] = body[:3000] if body else ""

    return result


def _extract_body(payload: dict) -> str:
    """Extract plain text body from message payload."""
    if payload.get("mimeType") == "text/plain" and payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")

    for part in payload.get("parts", []):
        text = _extract_body(part)
        if text:
            return text

    return ""


@tool(description=(
    "Search and read Gmail emails. Supports Gmail query syntax for filtering. "
    "Examples: 'is:unread', 'from:boss@co.com', 'subject:urgent', "
    "'has:attachment', 'after:2026/03/20', 'label:important'. "
    "Returns email summaries sorted by date."
))
async def read_emails(
    query: str = "is:unread",
    max_results: int = 20,
    include_body: bool = False,
) -> str:
    service = _get_gmail_service()

    results = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        return json.dumps({"count": 0, "emails": [], "query": query})

    emails = []
    for msg_ref in messages:
        email = _parse_message(service, msg_ref["id"], include_body=include_body)
        emails.append(email)

    return json.dumps({
        "count": len(emails),
        "query": query,
        "emails": emails,
    }, indent=2)


@tool(description=(
    "Get a categorized email digest. Reads recent unread emails and sorts them "
    "into priority categories based on your sorting rules in email_rules.yaml. "
    "Returns a structured summary ready for a Discord ping."
))
async def email_digest(
    hours_back: int = 1,
    max_results: int = 50,
) -> str:
    import yaml
    from pathlib import Path

    service = _get_gmail_service()

    # Load sorting rules
    rules_path = Path(__file__).parent.parent / "config" / "email_rules.yaml"
    rules = {}
    if rules_path.exists():
        rules = yaml.safe_load(rules_path.read_text()) or {}

    # Fetch recent unread
    results = service.users().messages().list(
        userId="me", q="is:unread", maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        return json.dumps({"summary": "No new unread emails.", "categories": {}})

    # Parse and categorize
    categories: dict[str, list] = {
        "urgent": [],
        "actionable": [],
        "fyi": [],
        "other": [],
    }

    urgent_senders = [s.lower() for s in rules.get("urgent_senders", [])]
    urgent_keywords = [k.lower() for k in rules.get("urgent_keywords", [])]
    fyi_senders = [s.lower() for s in rules.get("fyi_senders", [])]
    fyi_labels = [l.lower() for l in rules.get("fyi_labels", [])]

    for msg_ref in messages:
        email = _parse_message(service, msg_ref["id"], include_body=False)
        sender = email["from"].lower()
        subject = email["subject"].lower()

        # Categorize
        if any(s in sender for s in urgent_senders) or any(k in subject for k in urgent_keywords):
            categories["urgent"].append(email)
        elif any(s in sender for s in fyi_senders) or any(
            l in [lb.lower() for lb in email["labels"]] for l in fyi_labels
        ):
            categories["fyi"].append(email)
        elif email["has_attachments"] or "action" in subject or "review" in subject:
            categories["actionable"].append(email)
        else:
            categories["other"].append(email)

    summary_parts = []
    for cat, emails in categories.items():
        if emails:
            summary_parts.append(f"**{cat.upper()}** ({len(emails)})")
            for e in emails[:5]:
                summary_parts.append(f"  - {e['from']}: {e['subject']}")

    return json.dumps({
        "total_unread": len(messages),
        "summary": "\n".join(summary_parts),
        "categories": {k: len(v) for k, v in categories.items()},
        "emails": {k: v for k, v in categories.items() if v},
    }, indent=2)


@tool(description="Read a specific email by ID. Returns full message content.")
async def read_email_by_id(email_id: str) -> str:
    service = _get_gmail_service()
    email = _parse_message(service, email_id, include_body=True)
    return json.dumps(email, indent=2)
