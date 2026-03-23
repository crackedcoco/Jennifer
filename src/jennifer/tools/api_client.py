"""External API tools for Jennifer."""

import json

import httpx
from claude_agent_sdk import tool


@tool(description="Make a GET request to an external API. Returns the response body as JSON or text.")
async def api_get(url: str, headers: dict[str, str] | None = None) -> str:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(url, headers=headers or {})
        resp.raise_for_status()
        try:
            return json.dumps(resp.json(), indent=2)
        except Exception:
            return resp.text


@tool(description="Make a POST request to an external API with a JSON body. Returns the response.")
async def api_post(url: str, body: dict, headers: dict[str, str] | None = None) -> str:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, json=body, headers=headers or {})
        resp.raise_for_status()
        try:
            return json.dumps(resp.json(), indent=2)
        except Exception:
            return resp.text
