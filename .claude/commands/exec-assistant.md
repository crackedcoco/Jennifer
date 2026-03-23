# Executive Assistant

Smart check-in that combines email + calendar context. If a meeting is coming up, prep a brief with relevant email context from those attendees.

## Steps

1. Use `upcoming_events` with `hours_ahead=1` to check if any meetings are coming up in the next hour.

2. **If a meeting is within 30 minutes:**
   - Get the attendee list from the event
   - For each attendee, use `read_emails` to search for recent email threads: `from:[attendee] OR to:[attendee]` (last 7 days)
   - Summarize the key discussion points and open items with each person
   - Send a **meeting prep brief** to Discord:
   ```
   📋 MEETING PREP — [meeting title] in [X] min

   👥 Attendees: [list]
   📍 [location or meeting link]

   📧 RECENT CONTEXT
   [For each attendee with recent emails:]
   **[Name]** — [summary of recent threads, open items, what they last asked about]

   🎯 SUGGESTED TALKING POINTS
   [2-3 items based on email context]
   ```

3. **Also run inbox push** — Check for urgent/actionable emails (same as inbox-push command).

4. **If no upcoming meetings and no urgent emails:**
   - Stay silent.
