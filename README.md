# IBM QRadar MCP Server

A Model Context Protocol (MCP) server that provides comprehensive access to IBM QRadar security intelligence platform. Query logs, events, offenses, agents (log sources), assets, and more directly from your AI assistant.

## Features

### 🔍 Event & Log Queries
- **Custom AQL Queries**: Execute Ariel Query Language (AQL) queries against events and flows
- **Recent Events**: Quickly retrieve the latest security events
- **Network Flows**: Query network traffic data

### 🚨 Offense Management
- **List Offenses**: Get all security offenses with filtering options
- **Offense Details**: Retrieve detailed information about specific offenses
- **Filter by Status**: Query open, closed, or offenses by severity

### 🖥️ Log Sources (Agents)
- **List Log Sources**: View all agents/collectors sending data to QRadar
- **Log Source Details**: Get configuration and status of specific log sources
- **Log Source Types**: Browse available log source types

### 🌐 Asset Management
- **List Assets**: Query discovered network assets
- **Search by IP**: Find assets by IP address
- **Asset Details**: Get detailed asset information

### 📊 Analytics & Rules
- **List Rules**: Browse detection rules
- **Rule Details**: View rule configuration and logic
- **Filter Rules**: Find enabled/disabled rules

### 🗂️ Reference Data
- **Reference Sets**: Access threat intelligence lists
- **Reference Data**: Query specific reference set contents

### ⚙️ System Information
- **System Info**: QRadar version and configuration
- **Server Status**: Check QRadar server health

## Installation

### Prerequisites
- Python 3.10 or higher
- IBM QRadar instance with API access
- API authentication token from QRadar

### Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd IBMQradarMCP
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
cp .env.example .env
```

Edit `.env` file with your QRadar credentials:
```env
QRADAR_HOST=your-qradar-host.com
QRADAR_API_TOKEN=your-api-token-here
QRADAR_VERIFY_SSL=true
```

### Getting QRadar API Token

1. Log into your QRadar console
2. Navigate to **Admin** > **Authorized Services**
3. Click **Create Authorized Service**
4. Provide a name and select appropriate permissions
5. Copy the generated token to your `.env` file

## Usage

### Running the MCP Server

```bash
python -m src.server
```

The server will start and communicate via stdio (standard input/output) as per the MCP protocol.

### Configuration with Claude Desktop

Add this configuration to your Claude Desktop config file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "qradar": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/IBMQradarMCP",
      "env": {
        "QRADAR_HOST": "your-qradar-host.com",
        "QRADAR_API_TOKEN": "your-api-token",
        "QRADAR_VERIFY_SSL": "true"
      }
    }
  }
}
```

## Available Tools

### Event & Log Query Tools

#### `qradar_search_events`
Search events using AQL (Ariel Query Language).

**Parameters**:
- `query` (required): AQL query string
- `timeout` (optional): Query timeout in seconds (default: 60)
- `max_wait` (optional): Maximum wait time for results (default: 300)

**Example**:
```
Search for failed login attempts in the last 24 hours:
SELECT sourceip, username, eventcount FROM events WHERE category=1003 LAST 24 HOURS
```

#### `qradar_get_recent_events`
Get the most recent security events.

**Parameters**:
- `limit` (optional): Number of events to return (default: 50)
- `fields` (optional): Array of field names to return

#### `qradar_search_flows`
Search network flows using AQL.

**Parameters**:
- `query` (required): AQL query string for flows
- `timeout` (optional): Query timeout in seconds
- `max_wait` (optional): Maximum wait time for results

### Offense Tools

#### `qradar_get_offenses`
Get offenses (security incidents) from QRadar.

**Parameters**:
- `filter` (optional): Filter string (e.g., "status=OPEN")
- `fields` (optional): Comma-separated list of fields
- `range` (optional): Result range (e.g., "0-49")

#### `qradar_get_offense_by_id`
Get detailed information about a specific offense.

**Parameters**:
- `offense_id` (required): The offense ID

### Log Source (Agent) Tools

#### `qradar_get_log_sources`
List all log sources (agents/collectors).

**Parameters**:
- `filter` (optional): Filter string (e.g., "enabled=true")
- `fields` (optional): Comma-separated list of fields

#### `qradar_get_log_source_by_id`
Get details of a specific log source.

**Parameters**:
- `log_source_id` (required): The log source ID

#### `qradar_get_log_source_types`
Get available log source types.

### Asset Tools

#### `qradar_get_assets`
List network assets discovered by QRadar.

**Parameters**:
- `filter` (optional): Filter string
- `fields` (optional): Comma-separated list of fields

#### `qradar_search_assets_by_ip`
Search for assets by IP address.

**Parameters**:
- `ip_address` (required): IP address to search

### Reference Data Tools

#### `qradar_get_reference_sets`
List all reference data sets.

#### `qradar_get_reference_set_data`
Get data from a specific reference set.

**Parameters**:
- `ref_set_name` (required): Name of the reference set

### System Information Tools

#### `qradar_get_system_info`
Get QRadar system information.

#### `qradar_get_servers`
Get QRadar server/host information.

### Rules Tools

#### `qradar_get_rules`
List analytics rules.

**Parameters**:
- `filter` (optional): Filter string
- `fields` (optional): Comma-separated list of fields

#### `qradar_get_rule_by_id`
Get details of a specific rule.

**Parameters**:
- `rule_id` (required): The rule ID

## Example Queries

Here are some example queries you can ask your AI assistant once the MCP server is configured:

### Security Monitoring
- "Show me all open offenses with high severity"
- "What are the most recent security events in the last hour?"
- "Search for failed SSH login attempts in the last 24 hours"

### Network Analysis
- "Show me all network flows from IP 192.168.1.100"
- "What are the top source IPs in network traffic today?"

### Asset Management
- "List all assets in my network"
- "Find information about the asset with IP 10.0.0.50"
- "What log sources are currently connected?"

### Threat Investigation
- "Show me details of offense ID 1234"
- "What reference sets contain the IP 8.8.8.8?"
- "List all enabled detection rules"

## AQL Query Examples

### Event Queries

**Failed login attempts**:
```sql
SELECT sourceip, username, eventcount 
FROM events 
WHERE category=1003 
LAST 24 HOURS
```

**High severity events**:
```sql
SELECT sourceip, destinationip, qid 
FROM events 
WHERE severity >= 7 
LAST 1 HOURS
```

**Events from specific IP**:
```sql
SELECT * 
FROM events 
WHERE sourceip='192.168.1.100' 
LAST 7 DAYS
```

### Flow Queries

**Top talkers by bytes**:
```sql
SELECT sourceip, destinationip, SUM(sourcebytes) as total_bytes 
FROM flows 
GROUP BY sourceip, destinationip 
ORDER BY total_bytes DESC 
LAST 1 HOURS
```

**Connections to specific port**:
```sql
SELECT sourceip, destinationip, destinationport 
FROM flows 
WHERE destinationport=443 
LAST 24 HOURS
```

## Security Considerations

1. **API Token Security**: Never commit your API token to version control
2. **SSL Verification**: Keep `QRADAR_VERIFY_SSL=true` in production
3. **Least Privilege**: Use QRadar authorized services with minimal required permissions
4. **Network Security**: Ensure secure network connection to QRadar
5. **Token Rotation**: Regularly rotate API tokens

## Troubleshooting

### Connection Issues
```
Error: QRadar API request failed
```
- Verify `QRADAR_HOST` is correct (without https://)
- Check firewall rules allow connection to QRadar
- Ensure API port (typically 443) is accessible

### Authentication Errors
```
Error: 401 Unauthorized
```
- Verify `QRADAR_API_TOKEN` is correct
- Check token hasn't expired in QRadar
- Ensure authorized service has required permissions

### SSL Certificate Errors
```
Error: SSL verification failed
```
- For development, set `QRADAR_VERIFY_SSL=false`
- For production, add QRadar certificate to trusted certificates

### Query Timeout
```
Error: Search timed out
```
- Increase `max_wait` parameter
- Narrow your query time range
- Use more specific filters in AQL

## Development

### Project Structure
```
IBMQradarMCP/
├── src/
│   ├── __init__.py
│   ├── qradar_client.py    # QRadar API client
│   └── server.py            # MCP server implementation
├── pyproject.toml           # Project metadata
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
└── README.md               # Documentation
```

### Testing

Run the server in debug mode:
```bash
python -m src.server
```

Test with sample MCP client or integrate with Claude Desktop.

## API Reference

This MCP server uses IBM QRadar REST API v15.0. For more information:
- [QRadar API Documentation](https://www.ibm.com/docs/en/qradar-common)
- [QRadar API Samples](https://github.com/IBM/api-samples)
- [AQL Guide](https://www.ibm.com/docs/en/qradar-common?topic=structure-aql-overview)

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review QRadar API documentation
3. Open an issue on GitHub

## Changelog

### Version 0.1.0
- Initial release
- Event and flow queries with AQL support
- Offense management
- Log source (agent) information
- Asset queries
- Reference data access
- System information
- Rules browsing

