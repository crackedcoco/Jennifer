"""Smoke tests for Jennifer agent definitions."""

from jennifer.agents import AGENTS


def test_all_agents_have_required_fields():
    assert len(AGENTS) > 0
    for name, agent in AGENTS.items():
        assert agent.description, f"{name} missing description"
        assert agent.prompt, f"{name} missing prompt"
        assert agent.tools, f"{name} missing tools"
        assert agent.model in ("sonnet", "opus", "haiku", "inherit"), (
            f"{name} has invalid model: {agent.model}"
        )


def test_researcher_has_web_tools():
    researcher = AGENTS["researcher"]
    assert "WebSearch" in researcher.tools
    assert "WebFetch" in researcher.tools


def test_reviewer_is_read_only():
    reviewer = AGENTS["reviewer"]
    assert "Write" not in reviewer.tools
    assert "Edit" not in reviewer.tools
    assert "Bash" not in reviewer.tools
