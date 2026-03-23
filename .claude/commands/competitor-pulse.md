# Competitor Pulse

Daily competitive intelligence scan.

## Steps

1. Read the competitor list from `src/jennifer/config/competitors.yaml`. If it doesn't exist, ask me to set it up.

2. For each competitor, search the web for:
   - New product launches or feature announcements
   - Pricing changes
   - New blog posts or content
   - Job postings (indicates growth areas)
   - Press mentions or news articles
   - Social media activity

3. **Filter for signal** — Only report things that are genuinely new (last 24h) and relevant. Skip noise.

4. **Send to Discord:**
```
🔍 Competitor Pulse — [date]

[For each competitor with news:]
**[Competitor Name]**
- [finding 1]
- [finding 2]

[If nothing notable:]
No significant competitor activity in the last 24h.

💡 STRATEGIC TAKEAWAY
[1-2 sentences on what this means for us]
```
