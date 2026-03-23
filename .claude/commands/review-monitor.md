# Review Monitor

Search for new reviews and brand mentions.

## Steps

1. Read brand info from `src/jennifer/config/brand.yaml`. If it doesn't exist, ask me to set it up.

2. Search the web for:
   - New reviews on Google, Trustpilot, G2, Capterra, Yelp (whichever are relevant)
   - Brand mentions on Reddit, Twitter/X, HackerNews
   - Blog posts or articles mentioning the brand
   - Forum discussions

3. For each mention found in the last 4 hours:
   - Classify sentiment: positive, neutral, negative
   - Extract key quote
   - Note the platform and link

4. **Send to Discord:**
```
👁️ Brand Mentions — [date]

[For each mention:]
[🟢/🟡/🔴] **[Platform]** — [sentiment]
"[key quote]"
[link]

📊 SENTIMENT SUMMARY
Positive: [X] | Neutral: [X] | Negative: [X]

[If negative reviews found:]
⚠️ NEEDS RESPONSE
[list negative ones with suggested replies]

[If nothing found:]
No new mentions in the last 4 hours.
```
