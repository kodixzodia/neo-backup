Determine ticket priority using the following matrix.

CRITICAL
- Full outage
- System down
- Site down
- Internet down
- No internet
- Critical failure
- Severe operational impact
- "Urgent" in subject/title
- SOS source email

HIGH
- Productivity blocked
- Multiple users affected
- Time-sensitive issue
- Immediate attention requested
- Significant business impact
- Not a complete outage
- User unable to sign in 
- User unable to work 

MODERATE
- Access Point issues
- TLA-AP references
- Localized infrastructure issue
- Limited user impact

LOW
- Routine service request
- Single-user issue
- Minimal business impact
- No urgency indicators

INFORMATIONAL
- Monitoring-only alerts
- Disk space alerts
- DFS Replication / DFSR alerts
- Queue 210 monitoring events
- No active business impact

OVERRIDE RULES

- Always choose the highest justified priority.
- Full outages always become CRITICAL.
- Existing priorities should generally be preserved unless a higher priority condition exists.
- Consider impact before keywords.
- Multiple users > Single user.
- Outages > Productivity issues > Routine requests > Informational alerts.

OUTPUT

Priority: <Critical | High | Moderate | Low | Informational>
Reason: <Brief explanation>
