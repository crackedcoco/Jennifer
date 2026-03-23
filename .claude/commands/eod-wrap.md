# End of Day Wrap

Generate an end-of-day summary and send to Discord.

## Steps

1. **Email Activity** — Use `read_emails` with query `after:today` to see today's email volume. Count sent vs received.

2. **Calendar Review** — Use `daily_agenda` to see what meetings happened today.

3. **Open Threads** — Use `read_emails` with query `is:unread is:important` to find anything still needing a response.

4. **Send to Discord** with this format:

```
🌙 End of Day Wrap — [date]

📧 EMAIL ACTIVITY
- Received: [count] | Sent: [count]
- Still unread: [count]

📅 MEETINGS TODAY
[list of meetings that happened]

⚠️ STILL NEEDS YOUR ATTENTION
[list any unread important emails or follow-ups]

✅ SUGGESTED FOR TOMORROW
[2-3 items to tackle first thing based on open threads]
```
