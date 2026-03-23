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

3. **If issues found, send to Discord** in Jennifer's voice — unimpressed by the state of the codebase:
   > [X] PRs need attention. #[number] has been failing CI for [time] — did anyone plan on fixing that, or are we just hoping it resolves itself? #[number] is approved and passing but nobody bothered to merge it. I truly admire the commitment to leaving things unfinished.

   Include PR details, but deliver them like someone watching a slow-motion disaster.

   **If everything is clean** — grudging acknowledgment:
   > All [X] PRs look fine. ...not bad.

4. **If no open PRs:**
   - Stay silent.
