# Invoice Chaser

Check for outstanding invoices needing follow-up.

## Steps

1. Use `read_emails` to search for invoice-related threads:
   - Query: `subject:(invoice OR payment OR receipt OR billing OR outstanding) older_than:7d`
   - Also: `subject:(invoice OR payment) is:unread`

2. Identify threads where:
   - You sent an invoice but haven't received payment confirmation
   - A payment is overdue based on email context
   - Someone asked about billing and you haven't replied

3. For each outstanding item, draft a polite follow-up email.

4. **Send to Discord:**
```
💰 Invoice Check — [date]

[For each outstanding:]
**[Client/Company]**
- Invoice sent: [date]
- Amount: [if visible]
- Days outstanding: [X]
- Last activity: [last email date]

**Draft follow-up:**
> [gentle reminder email]

React ✅ to send, or reply with changes.

[If nothing outstanding:]
✅ No overdue invoices found.
```
