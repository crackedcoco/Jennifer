"""Data pipeline tools for Jennifer."""

import json
import subprocess

from claude_agent_sdk import tool


@tool(description="Run a named data pipeline by executing its script. Returns stdout/stderr.")
async def run_pipeline(
    pipeline_name: str,
    args: list[str] | None = None,
) -> str:
    """Execute a pipeline script from the pipelines directory."""
    script = f"src/jennifer/pipelines/{pipeline_name}.py"
    cmd = ["python", script, *(args or [])]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300,
    )

    output = {
        "returncode": result.returncode,
        "stdout": result.stdout[-5000:] if result.stdout else "",
        "stderr": result.stderr[-2000:] if result.stderr else "",
    }
    return json.dumps(output, indent=2)
