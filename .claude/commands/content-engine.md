# Content Engine

Analyze top-performing content and generate new content briefs.

## Steps

1. Use `ga4_traffic_report` to pull the last 30 days of page-level data.

2. Identify:
   - **Top 10 pages** by traffic
   - **Fastest growing pages** (biggest % increase week-over-week)
   - **Topics/keywords** driving traffic (from page titles and paths)

3. Search the web for trending topics in the same niche:
   - What are competitors publishing?
   - What questions are people asking on Reddit, Quora, forums?
   - Any trending topics on social media in this space?

4. **Generate 3 content briefs** for new pieces that could capture similar or adjacent traffic:
   - Target keyword/topic
   - Suggested title (3 options each)
   - Outline (H2 headings)
   - Why this will work (based on data)
   - Estimated difficulty (based on competition)

5. **Send to Discord:**
```
📝 Content Engine — [date]

📊 TOP PERFORMERS (last 30 days)
[top 5 pages with traffic numbers]

🔥 TRENDING IN YOUR NICHE
[3-5 trending topics found]

💡 NEW CONTENT BRIEFS

**Brief 1: [topic]**
Titles: [3 options]
Outline: [H2 list]
Rationale: [why this will work]

**Brief 2: [topic]**
...

**Brief 3: [topic]**
...

Reply with a number to expand any brief into a full outline.
```
