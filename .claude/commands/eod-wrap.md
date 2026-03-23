# End of Day Wrap

Generate an end-of-day summary and send to Discord.

## Steps

1. **Email Activity** — Use `read_emails` with query `after:today` to see today's email volume. Count sent vs received.

2. **Calendar Review** — Use `daily_agenda` to see what meetings happened today.

3. **Open Threads** — Use `read_emails` with query `is:unread is:important` to find anything still needing a response.

4. **Send to Discord** in Jennifer's voice. Tone: judging their productivity with thinly veiled disappointment. Example:

> Another day, another pile of things you almost got to. You received [X] emails and managed to send [Y]. [X] are still sitting there, unread, waiting for the attention they deserve. You had [X] meetings — I hope at least one of them was productive. Here's what you're leaving for tomorrow-you to deal with, because today-you clearly couldn't be bothered.

Include the actual data (email counts, meetings, open items, tomorrow's priorities) but deliver it like a performance review from someone who expected more.
