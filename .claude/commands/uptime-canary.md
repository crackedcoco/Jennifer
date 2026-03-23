# Uptime Canary

Hit all monitored endpoints and alert if anything is down.

## Steps

1. Read endpoint list from `src/jennifer/config/endpoints.yaml`. If it doesn't exist, ask me to set it up.

2. Use the `check_endpoints` tool to hit every URL.

3. **If anything is down or slow (>3s):**
```
🚨 UPTIME ALERT

[For each problem:]
🔴 [url] — [status code or TIMEOUT] ([response_time]ms)

All other [X] endpoints OK.
```

4. **If everything is fine:**
   - Stay silent. Don't send anything. Only alert on problems.
