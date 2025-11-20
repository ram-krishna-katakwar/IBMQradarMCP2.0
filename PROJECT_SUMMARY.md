# IBM QRadar MCP Server - Project Summary

## Overview

This project provides a **Model Context Protocol (MCP)** server for **IBM QRadar**, enabling AI assistants like Claude to query security logs, events, offenses, and agents directly from your QRadar deployment.

## What This Does

The IBM QRadar MCP server bridges AI assistants with your QRadar security platform, allowing you to:

- 🔍 **Query security events** using natural language or AQL
- 🚨 **Investigate offenses** and security incidents  
- 🖥️ **Monitor log sources** (agents/collectors)
- 🌐 **Analyze network assets** and traffic flows
- 📊 **Review detection rules** and reference data
- ⚙️ **Check system status** and health

## Key Features

### Comprehensive API Coverage

- **Events & Logs**: Query events and flows with AQL (Ariel Query Language)
- **Offenses**: List and investigate security incidents
- **Log Sources**: Monitor agents, collectors, and data sources
- **Assets**: Discover and query network assets
- **Rules**: Browse analytics and detection rules
- **Reference Data**: Access threat intelligence lists
- **System Info**: Check QRadar version and server status

### Easy Integration

- Works seamlessly with Claude Desktop
- Simple environment-based configuration
- Comprehensive error handling
- Automatic retry logic for reliability

### Developer-Friendly

- Well-documented API client
- Type hints throughout
- Clean MCP server implementation
- Extensive examples and documentation

## Project Structure

```
IBMQradarMCP/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── __main__.py              # Entry point
│   ├── qradar_client.py         # QRadar API client (500+ lines)
│   └── server.py                # MCP server implementation (600+ lines)
│
├── examples/                     # Examples and guides
│   └── example_queries.md       # Query examples and patterns
│
├── README.md                     # Main documentation (400+ lines)
├── QUICK_START.md               # 5-minute setup guide
├── SETUP.md                     # Detailed setup instructions (600+ lines)
├── TROUBLESHOOTING.md           # Problem resolution guide (500+ lines)
├── PROJECT_SUMMARY.md           # This file
│
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project metadata
├── LICENSE                      # MIT License
│
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── claude_desktop_config.example.json  # Claude config template
└── test_connection.py          # Connection test script
```

## Technical Details

### Technology Stack

- **Language**: Python 3.10+
- **MCP SDK**: Model Context Protocol for AI integration
- **HTTP Client**: Requests with retry logic
- **API**: IBM QRadar REST API v15.0
- **Config**: python-dotenv for environment management

### Architecture

```
┌─────────────────┐
│  Claude Desktop │
│   (AI Client)   │
└────────┬────────┘
         │ MCP Protocol (stdio)
         ↓
┌─────────────────┐
│   MCP Server    │
│   (server.py)   │
└────────┬────────┘
         │ Python API
         ↓
┌─────────────────┐
│  QRadar Client  │
│(qradar_client.py)│
└────────┬────────┘
         │ REST API
         ↓
┌─────────────────┐
│   IBM QRadar    │
│     Console     │
└─────────────────┘
```

### Components

#### 1. QRadar Client (`qradar_client.py`)

Comprehensive Python client for QRadar REST API:

- **Connection Management**: Session handling, SSL verification, retries
- **Event Queries**: AQL search for events and flows with polling
- **Offense Management**: List, filter, and retrieve offense details
- **Log Sources**: Query agents, collectors, and log source types
- **Assets**: Asset discovery and IP-based searching
- **Reference Data**: Access threat intelligence lists
- **Rules**: Browse detection rules and configurations
- **System APIs**: Health checks and system information

**Key Methods**:
- `search_events()` - Execute AQL queries on events
- `search_flows()` - Execute AQL queries on network flows
- `get_offenses()` - List security offenses
- `get_log_sources()` - List log sources (agents)
- `get_assets()` - Query network assets
- `get_reference_sets()` - Access threat intel data

#### 2. MCP Server (`server.py`)

MCP protocol implementation with **41 tools**:

**Event & Log Tools** (3 tools):
- `qradar_search_events` - Custom AQL event queries
- `qradar_get_recent_events` - Latest security events
- `qradar_search_flows` - Network flow queries

**Offense Tools** (7 tools):
- `qradar_get_offenses` - List offenses with filters
- `qradar_get_offense_by_id` - Offense details
- `qradar_get_offense_notes` - View investigation notes 🆕
- `qradar_add_offense_note` - Add investigation notes 🆕
- `qradar_update_offense_status` - Update/close offenses 🆕
- `qradar_get_closing_reasons` - Get closure options 🆕
- `qradar_assign_offense` - Assign to analysts 🆕

**Saved Search Tools** (3 tools) 🆕:
- `qradar_get_saved_searches` - List saved queries
- `qradar_get_saved_search_by_id` - View search details
- `qradar_execute_saved_search` - Run saved query

**Log Source Tools** (3 tools):
- `qradar_get_log_sources` - List agents/collectors
- `qradar_get_log_source_by_id` - Agent details
- `qradar_get_log_source_types` - Available types

**Asset Tools** (2 tools):
- `qradar_get_assets` - List network assets
- `qradar_search_assets_by_ip` - Find by IP

**Reference Data Tools** (2 tools):
- `qradar_get_reference_sets` - List threat intel
- `qradar_get_reference_set_data` - Set contents

**Rule Tools** (2 tools):
- `qradar_get_rules` - List detection rules
- `qradar_get_rule_by_id` - Rule details

**System Tools** (2 tools):
- `qradar_get_system_info` - System information
- `qradar_get_servers` - Server status

**Custom Property Tools** (2 tools) 🆕:
- `qradar_get_custom_properties` - List custom fields
- `qradar_get_custom_property_by_id` - Property details

**Domain Management Tools** (2 tools) 🆕:
- `qradar_get_domains` - List tenants
- `qradar_get_domain_by_id` - Domain details

**Network Tools** (1 tool) 🆕:
- `qradar_get_network_hierarchy` - Network topology

**Discovery Tools** (4 tools) 🆕:
- `qradar_get_ariel_databases` - List data sources
- `qradar_get_ariel_fields` - List query fields
- `qradar_get_event_categories` - List event types
- `qradar_search_event_categories` - Find categories

**Building Block Tools** (2 tools) 🆕:
- `qradar_get_building_blocks` - List rule components
- `qradar_get_building_block_by_id` - Block details

**User Tools** (2 tools) 🆕:
- `qradar_get_users` - List QRadar users
- `qradar_get_user_by_id` - User details

**Report Tools** (1 tool) 🆕:
- `qradar_get_reports` - List apps/reports

#### 3. Test Connection Script (`test_connection.py`)

Diagnostic script to verify:
- Environment configuration
- QRadar connectivity
- API authentication
- Basic API functionality

## Configuration

### Environment Variables

```env
QRADAR_HOST=qradar.company.com
QRADAR_API_TOKEN=your-token-here
QRADAR_VERIFY_SSL=true
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "qradar": {
      "command": "python3",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/IBMQradarMCP",
      "env": {
        "QRADAR_HOST": "qradar.company.com",
        "QRADAR_API_TOKEN": "token",
        "QRADAR_VERIFY_SSL": "true"
      }
    }
  }
}
```

## Use Cases

### Security Operations

- Monitor recent security events
- Investigate active offenses
- Check log source health
- Analyze network traffic patterns
- Review threat intelligence

### Incident Response

- Query events during incident investigation
- Correlate events across time ranges
- Identify affected assets
- Check detection rule triggers
- Search for indicators of compromise

### Compliance & Reporting

- Query events for compliance requirements
- Check system configuration
- Review detection coverage
- Analyze log source status

### Threat Hunting

- Execute complex AQL queries
- Search for suspicious patterns
- Correlate multiple data sources
- Investigate unknown threats

## Example Usage

### Natural Language Queries

```
"Show me high severity events in the last hour"
"List all disconnected log sources"
"Find assets with IP 192.168.1.100"
"What offenses are currently open?"
"Search for failed login attempts"
```

### AQL Queries

```sql
-- Failed authentications
SELECT sourceip, username, eventcount 
FROM events 
WHERE category=1003 
LAST 24 HOURS

-- Top bandwidth consumers
SELECT sourceip, SUM(sourcebytes) as total 
FROM flows 
GROUP BY sourceip 
ORDER BY total DESC 
LAST 1 HOURS

-- High severity events
SELECT * 
FROM events 
WHERE severity >= 7 
LAST 2 HOURS
```

## Documentation

### Quick Start
- **QUICK_START.md** - Get running in 5 minutes
- **README.md** - Comprehensive overview
- **SETUP.md** - Detailed setup guide

### Reference
- **examples/example_queries.md** - Query patterns and examples
- **TROUBLESHOOTING.md** - Problem resolution
- **claude_desktop_config.example.json** - Config template

### API Resources
- [IBM QRadar API Docs](https://www.ibm.com/docs/en/qradar-common)
- [AQL Reference](https://www.ibm.com/docs/en/qradar-common?topic=structure-aql-overview)
- [QRadar API Samples](https://github.com/IBM/api-samples)

## Security Considerations

### Authentication
- Uses QRadar API token authentication
- Tokens stored in environment variables
- Never committed to version control

### Network Security
- SSL/TLS verification configurable
- Secure HTTPS communication
- Support for custom certificates

### Least Privilege
- Recommend minimal required API permissions
- Read-only access sufficient for most operations
- Token-based authorization

### Best Practices
- ✅ Rotate API tokens regularly
- ✅ Use SSL verification in production
- ✅ Limit token permissions
- ✅ Secure .env file
- ✅ Never commit credentials

## Installation Summary

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Configure .env**: Set QRadar host and token
3. **Test connection**: `python test_connection.py`
4. **Configure Claude**: Add to `claude_desktop_config.json`
5. **Restart Claude**: Fully quit and restart

## Requirements

### System Requirements
- Python 3.10 or higher
- Network access to QRadar API (port 443)
- 50MB disk space

### QRadar Requirements
- QRadar 7.3.0 or higher
- API access enabled
- Authorized service token with read permissions

### Permissions Required
- Ariel (events/flows)
- Offenses
- Log sources
- Assets
- Reference data
- Rules
- System information

## Metrics

- **Total Lines of Code**: ~2,800
- **Tools Provided**: 41 (16 core + 25 advanced)
- **API Endpoints Covered**: 30+
- **Documentation Pages**: 4,500+ lines
- **Example Queries**: 50+
- **Advanced Workflows**: 10+ complete patterns

## Recent Enhancements (v0.2.0)

**Completed**:
- ✅ Write operations (offense notes, status updates, assignment)
- ✅ Saved search execution
- ✅ Custom property management
- ✅ Domain management for multi-tenancy
- ✅ Building block access
- ✅ User management
- ✅ Event category discovery
- ✅ Field introspection
- ✅ Network hierarchy access
- ✅ Complete incident response workflows

## Future Enhancements

Potential additions:
- Reference set modification (add/remove IOCs)
- Streaming event monitoring via websockets
- Custom alert/rule creation
- Bulk operations for offense management
- Data export in multiple formats
- Integration with external threat intel
- Multiple QRadar instance support
- Async query execution for better performance
- Watchlist and monitoring capabilities

## License

MIT License - See [LICENSE](LICENSE) file

## Contributing

Contributions welcome! Areas for improvement:
- Additional API endpoint coverage
- Performance optimizations
- More example queries
- Enhanced error handling
- Additional documentation

## Support

### Documentation
1. Check [QUICK_START.md](QUICK_START.md)
2. Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. See [SETUP.md](SETUP.md) for details
4. Browse [examples/example_queries.md](examples/example_queries.md)

### Testing
- Run: `python test_connection.py`
- Check Claude Desktop logs
- Verify QRadar API access

### Resources
- IBM QRadar API documentation
- MCP protocol specification
- Python requests library docs

## Changelog

### Version 0.2.0 (Current - Advanced Features Release)

**Features**:
- 🎉 **25 new advanced tools** (total: 41 tools)
- 📝 Enhanced offense management with notes, status updates, assignment
- 💾 Saved search execution and management
- 🎨 Custom property discovery and querying
- 🏢 Domain management for multi-tenancy
- 🌐 Network hierarchy access
- 🔍 Discovery tools: fields, categories, databases
- 🧩 Building block management for rule components
- 👥 User management for offense assignment
- 📊 Reports and applications listing
- ✨ Complete incident response workflows

**Documentation**:
- New ADVANCED_FEATURES.md (2,000+ lines)
- Updated README with new capabilities
- Complete workflow examples
- Best practices guide
- Tool comparison tables
- Security considerations

**API Coverage**:
- 30+ API endpoints
- Write operations (notes, status, assignment)
- Configuration and discovery APIs
- User and domain management

### Version 0.1.0 (Initial Release)

**Features**:
- Complete QRadar API client implementation
- MCP server with 16 tools
- Event and flow queries with AQL
- Offense management
- Log source monitoring
- Asset queries
- Reference data access
- Rules browsing
- System information

**Documentation**:
- Comprehensive README
- Quick start guide
- Detailed setup instructions
- Troubleshooting guide
- Example queries
- API documentation

**Testing**:
- Connection test script
- Error handling
- Retry logic

## Acknowledgments

- IBM QRadar API team for comprehensive API
- Anthropic for MCP specification
- Python community for excellent libraries

---

**Status**: ✅ Production Ready

**Last Updated**: November 2024

**Maintained By**: Community

**Version**: 0.1.0

