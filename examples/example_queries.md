# IBM QRadar MCP - Example Queries

This document contains example queries you can use with the IBM QRadar MCP server through Claude or other AI assistants.

## Getting Started

### Basic Queries

**Check system status**:
```
Get QRadar system information
```

**List servers**:
```
Show me all QRadar servers
```

**Get recent events**:
```
Show me the 20 most recent security events
```

## Event Queries

### Failed Authentication

**Recent failed logins**:
```
Search QRadar events for failed login attempts in the last 24 hours
```

**AQL Query**:
```
SELECT sourceip, username, eventcount FROM events WHERE category=1003 LAST 24 HOURS
```

### Network Activity

**Events from specific IP**:
```
Show me all events from IP address 192.168.1.100 in the last 7 days
```

**AQL Query**:
```
SELECT * FROM events WHERE sourceip='192.168.1.100' LAST 7 DAYS
```

**High severity events**:
```
Search for high severity events (severity >= 7) in the last hour
```

**AQL Query**:
```
SELECT sourceip, destinationip, qid, severity FROM events WHERE severity >= 7 LAST 1 HOURS
```

### Malware and Threats

**Malware detection events**:
```
Find malware-related events in the last 48 hours
```

**AQL Query**:
```
SELECT sourceip, destinationip, username, qidname FROM events WHERE category=12 LAST 48 HOURS
```

**Suspicious file downloads**:
```
Show events related to suspicious downloads
```

## Flow Queries

### Network Traffic Analysis

**Top talkers by bandwidth**:
```
Show me the top source IPs by network traffic in the last hour
```

**AQL Query**:
```
SELECT sourceip, destinationip, SUM(sourcebytes) as total_bytes 
FROM flows 
GROUP BY sourceip, destinationip 
ORDER BY total_bytes DESC 
LIMIT 10
LAST 1 HOURS
```

**HTTPS connections**:
```
Show all HTTPS connections in the last 24 hours
```

**AQL Query**:
```
SELECT sourceip, destinationip, destinationport FROM flows WHERE destinationport=443 LAST 24 HOURS
```

**Unusual ports**:
```
Find connections to unusual high-numbered ports
```

**AQL Query**:
```
SELECT sourceip, destinationip, destinationport FROM flows WHERE destinationport > 10000 LAST 2 HOURS
```

## Offense Management

### Active Investigations

**Open offenses**:
```
Show me all open offenses
```

**With filter**: Use `filter` parameter: `status=OPEN`

**High priority offenses**:
```
List high severity open offenses
```

**With filter**: `status=OPEN AND severity >= 7`

**Recent offenses**:
```
Show offenses created in the last 24 hours
```

**Offense details**:
```
Get details for offense ID 42
```

## Log Source (Agent) Queries

### Agent Status

**All log sources**:
```
List all log sources in QRadar
```

**Active log sources only**:
```
Show only enabled log sources
```

**With filter**: `enabled=true`

**Disconnected sources**:
```
Find log sources that are disconnected
```

**With filter**: `status=ERROR`

**Specific log source**:
```
Get details for log source ID 123
```

### Log Source Types

**Available types**:
```
What types of log sources can QRadar collect from?
```

**Find specific type**:
```
Show me information about Windows log source types
```

## Asset Queries

### Asset Discovery

**All assets**:
```
List all assets discovered by QRadar
```

**Search by IP**:
```
Find the asset with IP address 10.0.1.50
```

**Server assets**:
```
Show me all server assets
```

**Workstation assets**:
```
List all workstation assets
```

## Reference Data

### Threat Intelligence

**List reference sets**:
```
Show all reference data sets in QRadar
```

**Check IP in reference set**:
```
Get data from the reference set named "Blocked_IPs"
```

**Threat indicators**:
```
Show me the "Known_Malicious_IPs" reference set
```

## Rules and Analytics

### Detection Rules

**All rules**:
```
List all analytics rules in QRadar
```

**Enabled rules only**:
```
Show only enabled rules
```

**With filter**: `enabled=true`

**Specific rule**:
```
Get details for rule ID 100042
```

**Custom rules**:
```
Show me custom rules (not built-in)
```

**With filter**: `origin=USER`

## Complex Scenarios

### Investigating Suspicious Activity

**Scenario 1: Investigating a suspicious IP**

```
1. Find the asset: "Search for assets with IP 192.168.1.100"
2. Check events: "Show all events from IP 192.168.1.100 in last 24 hours"
3. Check flows: "Show network flows from 192.168.1.100"
4. Related offenses: "Show offenses involving IP 192.168.1.100"
```

**Scenario 2: Failed login investigation**

```
1. Find events: Search events for failed logins
   AQL: SELECT sourceip, username, eventcount FROM events WHERE category=1003 LAST 24 HOURS
2. Group by user: "Show me which users have the most failed logins"
3. Check source IPs: "What IPs are these failed logins coming from?"
4. Check offenses: "Are there any offenses related to these IPs?"
```

**Scenario 3: Data exfiltration check**

```
1. Large transfers: Show flows with high byte counts
   AQL: SELECT sourceip, destinationip, SUM(sourcebytes) as total 
        FROM flows 
        GROUP BY sourceip, destinationip 
        HAVING total > 1000000000 
        LAST 24 HOURS
2. External connections: Check if destinations are external
3. Off-hours activity: Filter by time range
4. User correlation: Match IPs to assets and users
```

## Advanced AQL Patterns

### Time-based Queries

**Specific time range**:
```sql
SELECT * FROM events 
START '2024-01-01 00:00:00' 
STOP '2024-01-01 23:59:59'
```

**Last N hours/days**:
```sql
LAST 6 HOURS
LAST 7 DAYS
LAST 30 DAYS
```

### Aggregations

**Count by field**:
```sql
SELECT sourceip, COUNT(*) as event_count 
FROM events 
GROUP BY sourceip 
ORDER BY event_count DESC 
LAST 24 HOURS
```

**Sum and average**:
```sql
SELECT sourceip, 
       SUM(eventcount) as total_events,
       AVG(magnitude) as avg_magnitude
FROM events 
GROUP BY sourceip 
LAST 24 HOURS
```

### Filtering

**Multiple conditions**:
```sql
SELECT * FROM events 
WHERE severity >= 5 
  AND category IN (1003, 1004) 
  AND sourceip NOT IN ('10.0.0.1', '10.0.0.2')
LAST 24 HOURS
```

**String matching**:
```sql
SELECT * FROM events 
WHERE username LIKE '%admin%' 
LAST 24 HOURS
```

### Joins (Advanced)

**Events with asset information**:
```sql
SELECT events.sourceip, assets.hostname, events.qidname
FROM events
JOIN assets ON events.sourceip = assets.ipaddress
LAST 24 HOURS
```

## Tips for Effective Queries

### Performance Tips

1. **Use time ranges**: Always specify a reasonable time range
   - ✅ Good: `LAST 24 HOURS`
   - ❌ Bad: `LAST 365 DAYS` (very slow)

2. **Limit results**: Use LIMIT clause for large result sets
   - `LIMIT 100` for quick overview
   - `LIMIT 1000` for detailed analysis

3. **Select specific fields**: Don't use `SELECT *` unless necessary
   - ✅ Good: `SELECT sourceip, destinationip`
   - ❌ Bad: `SELECT *` (returns all fields)

4. **Use filters early**: Filter data before aggregation
   - ✅ Good: `WHERE severity >= 7 GROUP BY...`
   - ❌ Bad: `GROUP BY... HAVING severity >= 7`

### Query Building

1. **Start simple**: Begin with basic query, then add complexity
2. **Test incrementally**: Test each condition separately
3. **Use aliases**: Make output readable with `AS` keyword
4. **Check field names**: Verify field names in QRadar documentation

### Common Fields

**Event fields**:
- `sourceip`, `destinationip`
- `username`
- `qid`, `qidname` (rule identifiers)
- `category`, `categoryname`
- `severity`, `magnitude`
- `eventcount`
- `starttime`, `endtime`

**Flow fields**:
- `sourceip`, `destinationip`
- `sourceport`, `destinationport`
- `sourcebytes`, `destinationbytes`
- `protocol`
- `starttime`, `endtime`

## Troubleshooting Queries

### Query Takes Too Long

**Problem**: Query timeout or very slow

**Solutions**:
1. Reduce time range: `LAST 1 HOURS` instead of `LAST 7 DAYS`
2. Add more specific filters
3. Use LIMIT clause
4. Increase `max_wait` parameter

### No Results Returned

**Problem**: Query returns empty results

**Solutions**:
1. Verify time range includes events
2. Check filter conditions aren't too restrictive
3. Verify field names are correct
4. Check data exists for the queried category/type

### Query Error

**Problem**: AQL syntax error

**Solutions**:
1. Check field names spelling
2. Verify parentheses are balanced
3. Ensure quotes are proper (single quotes for strings)
4. Check keyword spelling (SELECT, FROM, WHERE, etc.)

## Resources

- [QRadar AQL Guide](https://www.ibm.com/docs/en/qradar-common?topic=structure-aql-overview)
- [QRadar API Documentation](https://www.ibm.com/docs/en/qradar-common)
- [Event Categories Reference](https://www.ibm.com/docs/en/qradar-common?topic=overview-qid-event-categories)

---

**Note**: Replace example IPs, usernames, and IDs with actual values from your environment.

