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

4. **Send to Discord:**
```
🔒 Dependency Watch — [date]

[For each project:]
**[project path]**

🚨 Security Issues: [count]
[list critical/high severity with CVE IDs]

📦 Outdated Packages: [count]
[list major version bumps — skip minor/patch unless security-related]

[If clean:]
✅ No security issues. [X] packages could be updated (non-critical).

💡 RECOMMENDED ACTIONS
[prioritized list of what to update and why]
```
