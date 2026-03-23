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

5. **Send to Discord** in Jennifer's voice — disappointed but dutiful. Example:
   > Pipeline update. [X] active, [X] going cold because — and I cannot stress this enough — nobody followed up. I've drafted messages for the ones you're about to lose. React ✅ before they forget you exist. Which, at this rate, shouldn't take long.

   Include the full pipeline breakdown with deal statuses and draft follow-ups. Deliver it like someone watching money walk out the door because of neglect.
