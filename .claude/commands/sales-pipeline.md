# Sales Pipeline

Track prospect communications, update deal status, and draft follow-ups for cold threads.

## Steps

1. Read the prospect list from `src/jennifer/config/prospects.yaml`. If it doesn't exist, ask me to set it up.

2. For each prospect, search emails:
   - `from:[prospect email] OR to:[prospect email]`
   - Note the last email date and who sent it (them or us)

3. **Categorize each deal:**
   - 🟢 **Active** — replied within last 3 days
   - 🟡 **Cooling** — last reply 3-7 days ago
   - 🔴 **Cold** — no reply in 7+ days
   - ✅ **Won** — payment/contract language detected
   - ❌ **Lost** — rejection language detected

4. For cooling/cold prospects, draft a follow-up email tailored to the last conversation.

5. **Send to Discord:**
```
📊 Sales Pipeline — [date]

🟢 ACTIVE ([count])
[list with last activity]

🟡 COOLING ([count])
[list — draft follow-ups ready]

🔴 COLD ([count])
[list — re-engagement drafts ready]

✅ WON: [count] | ❌ LOST: [count]

📝 FOLLOW-UPS DRAFTED
[For each cooling/cold:]
**[Prospect]** — last contact [X] days ago
> [draft message preview]
React ✅ to send.
```
