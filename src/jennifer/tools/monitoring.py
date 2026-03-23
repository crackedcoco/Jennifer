"""Uptime and endpoint monitoring tools for Jennifer."""

import json
import time

import httpx
from claude_agent_sdk import tool


@tool(description=(
    "Check if a list of URLs are responding. Returns status codes and response times. "
    "Use for uptime monitoring and health checks."
))
async def check_endpoints(
    urls: list[str],
    timeout_seconds: int = 10,
) -> str:
    results = []

    async with httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=True) as client:
        for url in urls:
            start = time.monotonic()
            try:
                resp = await client.get(url)
                elapsed = round((time.monotonic() - start) * 1000)
                results.append({
                    "url": url,
                    "status": resp.status_code,
                    "ok": 200 <= resp.status_code < 400,
                    "response_time_ms": elapsed,
                })
            except httpx.TimeoutException:
                results.append({
                    "url": url,
                    "status": "TIMEOUT",
                    "ok": False,
                    "response_time_ms": timeout_seconds * 1000,
                })
            except Exception as e:
                results.append({
                    "url": url,
                    "status": f"ERROR: {type(e).__name__}",
                    "ok": False,
                    "response_time_ms": None,
                })

    all_ok = all(r["ok"] for r in results)
    down = [r for r in results if not r["ok"]]

    return json.dumps({
        "all_ok": all_ok,
        "total": len(results),
        "down_count": len(down),
        "results": results,
    }, indent=2)
