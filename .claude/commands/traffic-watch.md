# Traffic Watch

Check GA4 traffic and alert on anomalies.

## Steps

1. Use `ga4_traffic_report` to pull traffic data for the last 2 hours.

2. Compare against the same window yesterday (use the tool's comparison feature or pull both periods).

3. **Flag anomalies:**
   - Traffic drop > 30% from same period yesterday
   - Traffic spike > 50% from same period yesterday
   - Any page returning errors (if available)

4. **If anomaly detected** — Send Discord alert:
```
🚨 TRAFFIC ALERT
[metric] is [up/down] [X]% vs yesterday
Current: [value] | Yesterday: [value]
Top affected pages: [list]
```

5. **If normal** — Send brief update:
```
📊 Traffic normal — [X] sessions in last 2h ([+/-]% vs yesterday)
```

Keep it short. Only send details when something is off.
