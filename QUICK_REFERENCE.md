# IBM QRadar MCP - Quick Reference Card

## 🎯 Most Used Commands

### Offense Management
```
"Show me all open offenses"
"Show high severity offenses"
"Get details for offense [ID]"
"Show notes for offense [ID]"
"Add note to offense [ID]: [your note]"
"Assign offense [ID] to [username]"
"Close offense [ID] with closing reason [ID]"
```

### Event Queries
```
"Show me recent security events"
"Search for failed login attempts in the last 24 hours"
"Show high severity events in the last hour"
"Search events: [AQL query]"
```

### Discovery
```
"What fields are available for events?"
"Search event categories for 'malware'"
"Show me all saved searches"
"Show me all users"
```

### Investigation
```
"Find the asset with IP [IP address]"
"Show log sources"
"Show reference sets"
"Check if IP [IP] is in reference set [name]"
```

---

## 📋 Common AQL Patterns

### Failed Authentication
```sql
SELECT sourceip, username, eventcount 
FROM events 
WHERE category=1003 
LAST 24 HOURS
```

### High Severity Events
```sql
SELECT sourceip, destinationip, qidname 
FROM events 
WHERE severity >= 7 
LAST 1 HOURS
```

### Top Bandwidth Consumers
```sql
SELECT sourceip, SUM(sourcebytes) as total 
FROM flows 
GROUP BY sourceip 
ORDER BY total DESC 
LIMIT 10
LAST 1 HOURS
```

### Events from Specific IP
```sql
SELECT * 
FROM events 
WHERE sourceip='192.168.1.100' 
LAST 7 DAYS
```

### Malware Detection
```sql
SELECT sourceip, destinationip, qidname 
FROM events 
WHERE category=12 
LAST 48 HOURS
```

---

## 🔄 Complete Workflows

### Incident Response
1. `"Show me open high severity offenses"`
2. `"Get details for offense [ID]"`
3. `"Show notes for offense [ID]"`
4. `"Search events: [custom AQL based on offense]"`
5. `"Add note to offense [ID]: [findings]"`
6. `"Close offense [ID] with closing reason [ID]"`

### Threat Hunting
1. `"What fields are available for events?"`
2. `"Search event categories for [threat type]"`
3. `"Search events: [custom hunt query]"`
4. `"Find asset with IP [suspicious IP]"`
5. `"Show reference sets"` (check against IOCs)

### Daily Review
1. `"Show me open offenses"`
2. `"Show recent security events"`
3. `"Show log sources"` (check health)
4. `"Execute saved search '[daily check name]'"`

---

## 🔑 Key Category IDs

| Category | ID | Description |
|----------|-----|-------------|
| Authentication Failure | 1003 | Failed logins |
| Malware | 12 | Malware detection |
| System | 18 | System events |
| Network | 2 | Network activity |
| Access | 6 | Access control |

---

## 🎨 Tool Categories

- **Events** (3): Search, recent, flows
- **Offenses** (7): List, details, notes, update, assign
- **Saved Searches** (3): List, details, execute
- **Log Sources** (3): List, details, types
- **Assets** (2): List, search by IP
- **Reference Data** (2): Sets, data
- **Rules** (2): List, details
- **System** (2): Info, servers
- **Custom Properties** (2): List, details
- **Domains** (2): List, details
- **Network** (1): Hierarchy
- **Discovery** (4): Databases, fields, categories
- **Building Blocks** (2): List, details
- **Users** (2): List, details
- **Reports** (1): List

**Total: 41 tools**

---

## 📖 Documentation Index

- `README.md` - Setup & overview
- `QUICK_START.md` - 5-min setup
- `ADVANCED_FEATURES.md` - All 25 new tools
- `FEATURES_SUMMARY.md` - Tool reference
- `SETUP.md` - Detailed setup
- `TROUBLESHOOTING.md` - Problem solving
- `examples/example_queries.md` - Query examples

---

## 🚨 Important Notes

### Write Operations (Use Carefully)
- `qradar_add_offense_note`
- `qradar_update_offense_status`
- `qradar_assign_offense`

### Time Ranges
- `LAST N HOURS`
- `LAST N DAYS`
- `START 'YYYY-MM-DD HH:MM:SS' STOP 'YYYY-MM-DD HH:MM:SS'`

### Best Practices
- Always add notes when investigating
- Use filters to narrow results
- Start with small time ranges
- Check closing reasons before closing
- Assign offenses for accountability

---

## 🔧 Troubleshooting

**Issue**: No results  
**Fix**: Check time range, broaden filters

**Issue**: Query timeout  
**Fix**: Reduce time range, add filters, increase `max_wait`

**Issue**: Permission error  
**Fix**: Check API token permissions in QRadar

**Issue**: Tool not found  
**Fix**: Restart MCP server, check configuration

---

## 📞 Quick Help

```
"What tools are available?" - List all tools
"How do I [task]?" - Get help with specific task
"Show me an example of [query type]" - Get examples
```

---

**Version**: 0.2.0  
**Tools**: 41  
**Updated**: November 2024

