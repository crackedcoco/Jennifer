# PR Babysitter

Check GitHub for PRs needing attention.

## Steps

1. Run `gh pr list --state open --json number,title,author,createdAt,reviewDecision,statusCheckRollup,isDraft,url` to get all open PRs.

2. For each PR, check:
   - **Failing checks** — any CI/CD failures?
   - **Stale reviews** — requested review but no response for 24h+?
   - **Ready to merge** — approved + passing checks but not merged?
   - **Draft PRs** — older than 3 days without update?
   - **Merge conflicts** — any PRs with conflicts?

3. **If issues found, send to Discord:**
```
🔧 PR Status — [count] open PRs

[For each PR needing attention:]
⚠️ **#[number]** — [title]
Author: [author] | Opened: [relative time]
Issue: [failing checks / needs review / ready to merge / stale]
[url]

[If everything is clean:]
✅ All [count] open PRs look good.
```

4. **If no open PRs:**
   - Stay silent.
