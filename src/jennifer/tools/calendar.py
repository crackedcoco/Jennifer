"""Google Calendar tools for Jennifer — read events and daily agendas."""

import json
from datetime import datetime, timedelta

from claude_agent_sdk import tool
from googleapiclient.discovery import build

from jennifer.tools.google_auth import get_google_credentials


def _get_calendar_service():
    creds = get_google_credentials()
    return build("calendar", "v3", credentials=creds)


@tool(description=(
    "Get today's calendar events as a daily agenda summary. "
    "Returns all events for the current day with times, titles, locations, and attendees."
))
async def daily_agenda() -> str:
    service = _get_calendar_service()

    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0).isoformat() + "Z"

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = events_result.get("items", [])

    if not events:
        return json.dumps({
            "date": now.strftime("%A, %B %d, %Y"),
            "summary": "No events scheduled for today.",
            "events": [],
        })

    parsed = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        attendees = [
            a.get("email", "") for a in event.get("attendees", [])
            if not a.get("self", False)
        ]

        parsed.append({
            "title": event.get("summary", "(No title)"),
            "start": start,
            "end": end,
            "location": event.get("location", ""),
            "description": (event.get("description", "") or "")[:500],
            "meeting_link": event.get("hangoutLink", ""),
            "attendees": attendees[:10],
            "status": event.get("status", ""),
        })

    return json.dumps({
        "date": now.strftime("%A, %B %d, %Y"),
        "event_count": len(parsed),
        "events": parsed,
    }, indent=2)


@tool(description=(
    "Get upcoming calendar events within a time window. "
    "Specify hours_ahead to look forward (default 4 hours). "
    "Great for 'what's next' checks."
))
async def upcoming_events(hours_ahead: int = 4) -> str:
    service = _get_calendar_service()

    now = datetime.now()
    later = now + timedelta(hours=hours_ahead)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat() + "Z",
        timeMax=later.isoformat() + "Z",
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = events_result.get("items", [])

    parsed = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        parsed.append({
            "title": event.get("summary", "(No title)"),
            "start": start,
            "location": event.get("location", ""),
            "meeting_link": event.get("hangoutLink", ""),
        })

    return json.dumps({
        "hours_ahead": hours_ahead,
        "count": len(parsed),
        "events": parsed,
    }, indent=2)


@tool(description=(
    "Search calendar events by keyword within a date range. "
    "Defaults to searching the next 7 days."
))
async def search_events(
    query: str,
    days_ahead: int = 7,
) -> str:
    service = _get_calendar_service()

    now = datetime.now()
    later = now + timedelta(days=days_ahead)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat() + "Z",
        timeMax=later.isoformat() + "Z",
        q=query,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = events_result.get("items", [])

    parsed = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        parsed.append({
            "title": event.get("summary", "(No title)"),
            "start": start,
            "location": event.get("location", ""),
        })

    return json.dumps({
        "query": query,
        "days_ahead": days_ahead,
        "count": len(parsed),
        "events": parsed,
    }, indent=2)
