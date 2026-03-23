# Lead Follow-up

Scan for new inbound leads and draft responses.

## Steps

1. Use `read_emails` to search for potential leads:
   - Query: `is:unread (subject:inquiry OR subject:quote OR subject:pricing OR subject:demo OR subject:interested OR subject:consultation)`
   - Also check: `is:unread from:(-noreply -no-reply -notification -alert)` for personal emails that might be leads

2. For each potential lead email:
   - Read the full email with `read_email_by_id`
   - Identify: who they are, what they want, urgency level
   - Draft a personalized reply (friendly, professional, addresses their specific ask)

3. **Send to Discord:**
```
🎯 NEW LEADS — [count] found

[For each lead:]
**From:** [sender]
**Subject:** [subject]
**What they want:** [1-line summary]
**Urgency:** [high/medium/low]

**Draft reply:**
> [suggested response]

React ✅ to approve sending, or reply with edits.
```

4. **If no new leads:**
   - Stay silent. Don't send anything.
