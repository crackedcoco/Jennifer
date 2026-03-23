# Jennifer — Orchestration Agent

Jennifer is a multi-agent orchestration system powered by the Claude Agent SDK.

## Architecture

- **Entry point**: `src/jennifer/main.py` — runs as interactive REPL or one-shot via CLI args
- **Subagents**: defined in `src/jennifer/agents/` (programmatic) and `.claude/agents/` (filesystem)
- **Custom tools**: MCP tool servers in `src/jennifer/tools/` (API client, data pipelines)
- **Pipelines**: data pipeline scripts in `src/jennifer/pipelines/`
- **Hooks**: event callbacks in `src/jennifer/hooks/`

## Subagents

| Agent | Purpose | Model |
|-------|---------|-------|
| researcher | Web/codebase research | sonnet |
| coder | Write and debug code | sonnet |
| devops | CI/CD and infrastructure | sonnet |
| analyst | Data processing and ETL | sonnet |
| reviewer | Code review and security | opus |

## Conventions

- Python 3.11+, async-first
- Use `claude-agent-sdk` for all agent orchestration
- Custom tools use the `@tool` decorator and register via `create_sdk_mcp_server`
- Run `ruff check` before committing
- Tests go in `tests/` using pytest + pytest-asyncio
