"""Jennifer — main orchestration entry point."""

import asyncio
import sys

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

from jennifer.agents import AGENTS
from jennifer.tools import TOOL_SERVERS


async def run(prompt: str | None = None) -> None:
    """Run Jennifer as an interactive orchestration agent."""
    options = ClaudeAgentOptions(
        allowed_tools=[
            "Read", "Write", "Edit", "Bash", "Glob", "Grep",
            "Agent",          # enables subagent dispatch
            "WebSearch", "WebFetch",
            *[f"mcp__{s.name}__*" for s in TOOL_SERVERS],
        ],
        agents=AGENTS,
        mcp_servers=TOOL_SERVERS,
        setting_sources=["project"],
        permission_mode="default",
    )

    async with ClaudeSDKClient(options=options) as client:
        if prompt:
            # One-shot mode
            async for message in client.query(prompt):
                if hasattr(message, "content"):
                    print(message.content, flush=True)
        else:
            # Interactive REPL
            print("Jennifer orchestration agent ready. Type 'exit' to quit.\n")
            while True:
                try:
                    user_input = input("jennifer> ")
                except (EOFError, KeyboardInterrupt):
                    break
                if user_input.strip().lower() in ("exit", "quit"):
                    break
                async for message in client.query(user_input):
                    if hasattr(message, "content"):
                        print(message.content, flush=True)
                print()


def main() -> None:
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    asyncio.run(run(prompt))


if __name__ == "__main__":
    main()
