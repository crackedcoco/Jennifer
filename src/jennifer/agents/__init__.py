"""Subagent definitions for Jennifer."""

from claude_agent_sdk import AgentDefinition

AGENTS: dict[str, AgentDefinition] = {
    "researcher": AgentDefinition(
        description="Research agent for gathering information from the web and codebase.",
        prompt=(
            "You are a research specialist. Gather information from web searches, "
            "documentation, and codebases. Return structured findings with sources."
        ),
        tools=["WebSearch", "WebFetch", "Read", "Glob", "Grep"],
        model="sonnet",
    ),
    "coder": AgentDefinition(
        description="Coding agent for writing, editing, and debugging code.",
        prompt=(
            "You are an expert software engineer. Write clean, tested code. "
            "Follow existing patterns in the codebase. Run tests after changes."
        ),
        tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
        model="sonnet",
    ),
    "devops": AgentDefinition(
        description="DevOps agent for CI/CD, deployment, and infrastructure tasks.",
        prompt=(
            "You are a DevOps specialist. Handle CI/CD pipelines, Docker, "
            "cloud infrastructure, and deployment workflows. Be cautious with "
            "destructive operations — always confirm before proceeding."
        ),
        tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
        model="sonnet",
    ),
    "analyst": AgentDefinition(
        description="Data analyst agent for processing data and building pipelines.",
        prompt=(
            "You are a data analysis specialist. Process data, build ETL pipelines, "
            "generate reports, and create visualizations. Use pandas, polars, or "
            "similar tools as appropriate."
        ),
        tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
        model="sonnet",
    ),
    "reviewer": AgentDefinition(
        description="Code review agent for quality, security, and performance analysis.",
        prompt=(
            "You are a senior code reviewer. Analyze code for bugs, security "
            "vulnerabilities, performance issues, and style violations. Return "
            "actionable feedback with file paths and line numbers."
        ),
        tools=["Read", "Glob", "Grep"],
        model="opus",
    ),
}
