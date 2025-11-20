# Quick Start Guide - IBM QRadar MCP

Get up and running with the IBM QRadar MCP server in 5 minutes.

## Prerequisites

- ✅ Python 3.10+
- ✅ IBM QRadar access
- ✅ QRadar API token

## Installation (5 steps)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
QRADAR_HOST=your-qradar-host.com
QRADAR_API_TOKEN=your-token-here
QRADAR_VERIFY_SSL=true
```

### 3. Test Connection

```bash
python test_connection.py
```

You should see: ✅ Connection test completed successfully!

### 4. Configure Claude Desktop

**macOS**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "qradar": {
      "command": "python3",
      "args": ["-m", "src.server"],
      "cwd": "/FULL/PATH/TO/IBMQradarMCP",
      "env": {
        "QRADAR_HOST": "your-qradar-host.com",
        "QRADAR_API_TOKEN": "your-token-here",
        "QRADAR_VERIFY_SSL": "true"
      }
    }
  }
}
```

⚠️ **Important**: Use FULL absolute path for `cwd`!

### 5. Restart Claude Desktop

Quit and restart Claude Desktop completely.

## First Commands

Try these in Claude:

### 1. Check Connection
```
Get QRadar system information
```

### 2. Recent Events
```
Show me the 10 most recent security events
```

### 3. List Log Sources
```
Show all log sources in QRadar
```

### 4. Open Offenses
```
List all open offenses
```

## Common Issues

### ❌ Connection Failed

**Check**:
- Is `QRADAR_HOST` correct? (no `https://`)
- Is API token valid?
- Can you ping the host?
- Try `QRADAR_VERIFY_SSL=false` for testing

### ❌ Module Not Found

**Solution**:
```bash
pip install -r requirements.txt
```

### ❌ 401 Unauthorized

**Solution**: 
- Create new API token in QRadar
- Update `.env` file

### ❌ MCP Not Showing in Claude

**Solution**:
1. Check JSON syntax in config file
2. Use absolute paths (no `~` or `$HOME`)
3. Fully quit and restart Claude Desktop
4. Check Claude Desktop logs

## Getting QRadar API Token

1. Log into QRadar Console
2. **Admin** → **Authorized Services**
3. **Create Authorized Service**
4. Copy the token immediately!
5. Paste into `.env` file

## Example Queries

### Security Monitoring

**Failed logins**:
```
Search for failed login attempts in the last 24 hours
```

**High severity events**:
```
Show events with severity 7 or higher in the last hour
```

**Suspicious IPs**:
```
Show all events from IP 192.168.1.100
```

### Network Analysis

**Top bandwidth users**:
```
Show the top 10 source IPs by network traffic
```

**Unusual ports**:
```
Find connections to high-numbered ports (>10000)
```

### Asset Management

**Find asset**:
```
Search for asset with IP 10.0.1.50
```

**List all assets**:
```
Show all assets discovered by QRadar
```

### Investigations

**Investigate offense**:
```
Get details for offense ID 42
```

**Check log source status**:
```
Show all disconnected log sources
```

## AQL Queries

You can use custom AQL (Ariel Query Language) for advanced searches:

### Basic Event Query
```
Search QRadar events with query: SELECT sourceip, destinationip FROM events LAST 1 HOURS
```

### Failed Authentication
```
Search QRadar events with query: SELECT sourceip, username, eventcount FROM events WHERE category=1003 LAST 24 HOURS
```

### Network Flows
```
Search QRadar flows with query: SELECT sourceip, destinationip, destinationport FROM flows WHERE destinationport=443 LAST 2 HOURS
```

## Next Steps

1. 📖 Read full [README.md](README.md)
2. 🔧 See detailed [SETUP.md](SETUP.md)
3. 💡 Check [examples/example_queries.md](examples/example_queries.md)
4. 📚 Learn AQL: [IBM QRadar AQL Guide](https://www.ibm.com/docs/en/qradar-common?topic=structure-aql-overview)

## Available Tools

The MCP server provides these tools:

**Events & Logs**:
- `qradar_search_events` - Custom AQL event queries
- `qradar_get_recent_events` - Latest events
- `qradar_search_flows` - Network flow queries

**Offenses**:
- `qradar_get_offenses` - List offenses
- `qradar_get_offense_by_id` - Offense details

**Log Sources**:
- `qradar_get_log_sources` - List agents/collectors
- `qradar_get_log_source_by_id` - Agent details
- `qradar_get_log_source_types` - Available types

**Assets**:
- `qradar_get_assets` - List assets
- `qradar_search_assets_by_ip` - Find by IP

**Reference Data**:
- `qradar_get_reference_sets` - Threat intel lists
- `qradar_get_reference_set_data` - Reference set contents

**Rules**:
- `qradar_get_rules` - List detection rules
- `qradar_get_rule_by_id` - Rule details

**System**:
- `qradar_get_system_info` - System information
- `qradar_get_servers` - Server status

## Tips

✅ **DO**:
- Use specific time ranges (LAST 24 HOURS)
- Start with simple queries
- Use LIMIT for large results
- Filter data early in queries

❌ **DON'T**:
- Query very long time ranges (LAST 365 DAYS)
- Use SELECT * for everything
- Skip filters on large datasets

## Need Help?

- 📖 Check [SETUP.md](SETUP.md) for detailed instructions
- 🐛 Run `python test_connection.py` to test
- 📝 Review [examples/example_queries.md](examples/example_queries.md)
- 🔗 IBM QRadar API docs: https://www.ibm.com/docs/en/qradar-common

## Security

⚠️ **Never commit** `.env` file or tokens to git!

✅ **Do**:
- Use strong API tokens
- Enable SSL verification in production
- Use minimal required permissions
- Rotate tokens regularly
- Keep tokens secure

---

**Ready to go!** 🚀 Start querying QRadar through Claude Desktop!

