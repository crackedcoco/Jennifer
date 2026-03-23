"""Gmail send tools for Jennifer — compose and send emails."""

import base64
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from claude_agent_sdk import tool
from googleapiclient.discovery import build

from jennifer.tools.google_auth import get_google_credentials


def _get_gmail_service():
    creds = get_google_credentials()
    return build("gmail", "v1", credentials=creds)


@tool(description=(
    "Send an email via Gmail. Optionally specify a 'from_address' to send from "
    "a different address (must be configured as a Send-As alias in Gmail settings). "
    "Supports plain text and HTML body."
))
async def send_email(
    to: str,
    subject: str,
    body: str,
    from_address: str | None = None,
    cc: str | None = None,
    bcc: str | None = None,
    html: bool = False,
) -> str:
    service = _get_gmail_service()

    if html:
        message = MIMEMultipart("alternative")
        message.attach(MIMEText(body, "html"))
    else:
        message = MIMEText(body)

    message["to"] = to
    message["subject"] = subject

    if from_address:
        message["from"] = from_address
    if cc:
        message["cc"] = cc
    if bcc:
        message["bcc"] = bcc

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    sent = service.users().messages().send(
        userId="me",
        body={"raw": raw},
    ).execute()

    return json.dumps({
        "status": "sent",
        "message_id": sent["id"],
        "to": to,
        "subject": subject,
        "from": from_address or "(default)",
    }, indent=2)


@tool(description=(
    "Reply to an existing email by message ID. Maintains the thread. "
    "Optionally specify a 'from_address' to reply from a different alias."
))
async def reply_to_email(
    message_id: str,
    body: str,
    from_address: str | None = None,
) -> str:
    service = _get_gmail_service()

    # Get the original message for threading info
    original = service.users().messages().get(
        userId="me", id=message_id, format="metadata",
        metadataHeaders=["Subject", "From", "To", "Message-ID"],
    ).execute()

    headers = {h["name"].lower(): h["value"] for h in original["payload"]["headers"]}
    thread_id = original["threadId"]

    # Build reply
    reply = MIMEText(body)
    reply["to"] = headers.get("from", "")
    reply["subject"] = "Re: " + headers.get("subject", "")
    reply["In-Reply-To"] = headers.get("message-id", "")
    reply["References"] = headers.get("message-id", "")

    if from_address:
        reply["from"] = from_address

    raw = base64.urlsafe_b64encode(reply.as_bytes()).decode()

    sent = service.users().messages().send(
        userId="me",
        body={"raw": raw, "threadId": thread_id},
    ).execute()

    return json.dumps({
        "status": "sent",
        "message_id": sent["id"],
        "thread_id": thread_id,
        "to": reply["to"],
        "subject": reply["subject"],
        "from": from_address or "(default)",
    }, indent=2)


@tool(description=(
    "List available Send-As aliases configured in Gmail. "
    "Shows which email addresses you can send from."
))
async def list_send_as_aliases() -> str:
    service = _get_gmail_service()

    aliases = service.users().settings().sendAs().list(userId="me").execute()

    results = []
    for alias in aliases.get("sendAs", []):
        results.append({
            "email": alias["sendAsEmail"],
            "display_name": alias.get("displayName", ""),
            "is_default": alias.get("isDefault", False),
            "is_primary": alias.get("isPrimary", False),
            "verified": alias.get("verificationStatus") == "accepted",
        })

    return json.dumps({"aliases": results}, indent=2)
