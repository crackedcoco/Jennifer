# Dependency Watch

Weekly security and update check for project dependencies.

## Steps

1. Find project dependency files in the current repo:
   - `package.json` / `package-lock.json` (Node)
   - `pyproject.toml` / `requirements.txt` (Python)
   - `Gemfile` / `Gemfile.lock` (Ruby)
   - `go.mod` (Go)

2. For each project found, run the appropriate audit command:
   - Node: `npm audit --json`
   - Python: `pip audit --format json` (if pip-audit installed)
   - Check for known CVEs via web search for any critical dependencies

3. Also check for outdated packages:
   - Node: `npm outdated --json`
   - Python: `pip list --outdated --format json`

4. **Send to Discord** in Jennifer's voice — appalled by the state of your dependencies:
   > I audited your dependencies. [X] security vulnerabilities. [X] of them are critical. You've been running [package] with a known CVE for [X] days. I'm not angry, I'm just disappointed. Actually, no — I am angry. Here's what needs updating before something embarrassing happens.

   Include CVE details, outdated packages, and prioritized actions.

   **If clean:**
   > Dependencies are secure. No vulnerabilities. I'm genuinely surprised. ...don't let it go to your head.
✅ No security issues. [X] packages could be updated (non-critical).

💡 RECOMMENDED ACTIONS
[prioritized list of what to update and why]
```
