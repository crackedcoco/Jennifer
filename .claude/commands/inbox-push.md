# Inbox Push

Check for new unread emails, categorize them, and send me a Discord ping if anything needs attention.

## Steps

1. Use `email_digest` to get categorized unread emails from the last 30 minutes.

2. **If there are urgent or actionable emails:**
   - Send a Discord message with:
     - Sender, subject, and a 1-line summary of each urgent/actionable email
     - For emails that look like they need a reply, draft a suggested response (don't send it)

3. **If only FYI/other emails:**
   - Send a brief Discord message: "📧 [count] new emails — nothing urgent"

4. **If no new emails:**
   - Don't send anything. Stay silent.

Keep messages concise. Don't send walls of text.
