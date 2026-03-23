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

4. **Send to Discord** in Jennifer's voice — incredulous that people haven't paid:
   > [X] invoices are overdue. [Client] owes you [amount] and it's been [X] days. I've drafted a follow-up that's considerably more polite than what I'd send if it were up to me. React ✅ to send before I lose my patience on your behalf.

   > [If nothing outstanding:] Everyone's paid up. Miracles do happen.

   Include invoice details and draft follow-ups. The drafts themselves should be professional (it's going to real clients) but Jennifer's commentary about them should drip with disdain.
```
