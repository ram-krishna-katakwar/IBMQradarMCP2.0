# IBM QRadar MCP - Features Summary

Quick reference guide for all 41 tools available in the IBM QRadar MCP server.

## 📊 Quick Stats

- **Total Tools**: 41
- **API Endpoints**: 30+
- **Write Operations**: 3 tools
- **Discovery Tools**: 8 tools
- **Management Tools**: 15 tools

---

## 🗂️ Tool Categories

### 🔍 Event & Log Queries (3 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_search_events` | Execute custom AQL queries on events | No |
| `qradar_get_recent_events` | Get most recent security events | No |
| `qradar_search_flows` | Execute custom AQL queries on network flows | No |

**Common Use**: Threat hunting, compliance queries, incident investigation

---

### 🚨 Offense Management (7 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_offenses` | List all offenses with filtering | No |
| `qradar_get_offense_by_id` | Get specific offense details | No |
| `qradar_get_offense_notes` | View investigation notes | No |
| `qradar_add_offense_note` | Add investigation notes | **Yes** |
| `qradar_update_offense_status` | Update/close offenses | **Yes** |
| `qradar_get_closing_reasons` | Get available closing reasons | No |
| `qradar_assign_offense` | Assign offense to user | **Yes** |

**Common Use**: Incident response, offense triage, team collaboration

---

### 💾 Saved Searches (3 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_saved_searches` | List all saved AQL queries | No |
| `qradar_get_saved_search_by_id` | Get saved search details | No |
| `qradar_execute_saved_search` | Execute a saved search | No |

**Common Use**: Standardized investigations, compliance reporting, reusable queries

---

### 🖥️ Log Sources / Agents (3 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_log_sources` | List all log sources | No |
| `qradar_get_log_source_by_id` | Get log source details | No |
| `qradar_get_log_source_types` | Get available log source types | No |

**Common Use**: Data source monitoring, agent health checks, coverage analysis

---

### 🌐 Assets (2 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_assets` | List all discovered assets | No |
| `qradar_search_assets_by_ip` | Find assets by IP address | No |

**Common Use**: Asset inventory, IP investigation, network mapping

---

### 🗂️ Reference Data (2 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_reference_sets` | List all reference sets | No |
| `qradar_get_reference_set_data` | Get reference set contents | No |

**Common Use**: Threat intelligence, IOC checking, blocklist verification

---

### 📊 Analytics Rules (2 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_rules` | List all analytics rules | No |
| `qradar_get_rule_by_id` | Get rule details | No |

**Common Use**: Rule auditing, detection coverage, troubleshooting

---

### ⚙️ System Information (2 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_system_info` | Get QRadar system information | No |
| `qradar_get_servers` | Get server/host information | No |

**Common Use**: System monitoring, version checking, health status

---

### 🎨 Custom Properties (2 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_custom_properties` | List all custom properties | No |
| `qradar_get_custom_property_by_id` | Get custom property details | No |

**Common Use**: Data enrichment discovery, custom field queries, schema exploration

---

### 🏢 Domain Management (2 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_domains` | List all domains | No |
| `qradar_get_domain_by_id` | Get domain details | No |

**Common Use**: Multi-tenant management, data segregation, MSSP operations

---

### 🌐 Network Hierarchy (1 tool)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_network_hierarchy` | Get network topology | No |

**Common Use**: Network segmentation, subnet queries, topology analysis

---

### 🔍 Discovery & Introspection (4 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_ariel_databases` | List available databases | No |
| `qradar_get_ariel_fields` | Get queryable fields | No |
| `qradar_get_event_categories` | List all event categories | No |
| `qradar_search_event_categories` | Search categories by name | No |

**Common Use**: Query building, field discovery, category lookup

---

### 🧩 Building Blocks (2 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_building_blocks` | List all building blocks | No |
| `qradar_get_building_block_by_id` | Get building block details | No |

**Common Use**: Rule component discovery, detection logic review

---

### 👥 User Management (2 tools)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_users` | List all QRadar users | No |
| `qradar_get_user_by_id` | Get user details | No |

**Common Use**: User discovery for assignment, team coordination, access auditing

---

### 📊 Reports & Applications (1 tool)
| Tool | Description | Write |
|------|-------------|-------|
| `qradar_get_reports` | List available reports/apps | No |

**Common Use**: App inventory, report discovery, extension management

---

## 🎯 Common Workflows

### Incident Investigation
```
1. qradar_get_offenses (filter: status=OPEN, severity>=7)
2. qradar_get_offense_by_id
3. qradar_get_offense_notes
4. qradar_search_events (with AQL)
5. qradar_add_offense_note
6. qradar_update_offense_status
```

### Threat Hunting
```
1. qradar_get_ariel_fields (discover available fields)
2. qradar_search_event_categories (find relevant categories)
3. qradar_search_events (execute hunt query)
4. qradar_get_reference_sets (check IOCs)
5. qradar_search_assets_by_ip (identify affected hosts)
```

### Compliance Reporting
```
1. qradar_get_saved_searches (find compliance queries)
2. qradar_execute_saved_search
3. qradar_get_log_sources (verify coverage)
4. qradar_get_assets (inventory)
```

### Team Coordination
```
1. qradar_get_users (discover team members)
2. qradar_assign_offense (distribute work)
3. qradar_add_offense_note (document progress)
4. qradar_get_offense_notes (review status)
```

### Multi-Tenant Operations
```
1. qradar_get_domains (list tenants)
2. qradar_get_domain_by_id (tenant details)
3. qradar_get_network_hierarchy (tenant networks)
4. qradar_get_offenses (filter by domain)
```

---

## 🔐 Security Notes

### Tools with Write Permissions
These tools **modify data** in QRadar:
1. `qradar_add_offense_note` - Adds notes to offenses
2. `qradar_update_offense_status` - Changes offense status
3. `qradar_assign_offense` - Assigns offenses to users

**Recommendation**: Use dedicated service account with minimal required permissions.

### Required QRadar Permissions
| Category | Required Permission |
|----------|-------------------|
| Events/Flows | Ariel |
| Offenses (Read) | Offenses |
| Offenses (Write) | Offenses + Write |
| Log Sources | Configuration |
| Assets | Asset Management |
| Rules | Analytics |
| Users | Admin |
| System Info | System |

---

## 📚 Documentation

- **[README.md](README.md)** - Main documentation and setup
- **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
- **[ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)** - Detailed advanced features guide
- **[SETUP.md](SETUP.md)** - Complete setup instructions
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Problem resolution
- **[examples/example_queries.md](examples/example_queries.md)** - Query examples

---

## 🚀 Getting Started

### Basic Usage
```
"Show me high severity open offenses"
"Search for failed login attempts in the last 24 hours"
"List all log sources"
```

### Advanced Usage
```
"Execute saved search 'Daily_Compliance_Check'"
"Add note to offense 42: 'Investigated and confirmed false positive'"
"Close offense 42 with closing reason 2"
"Assign offense 156 to user 'analyst_john'"
```

### Query Building
```
"What fields are available for events queries?"
"Search event categories for 'authentication'"
"Search events: SELECT sourceip, username FROM events WHERE category=1003 LAST 24 HOURS"
```

---

## 🆚 Comparison with Other Tools

### vs. QRadar Web Console
| Feature | MCP Server | Web Console |
|---------|-----------|-------------|
| Natural Language | ✅ Yes | ❌ No |
| AI-Assisted | ✅ Yes | ❌ No |
| Bulk Operations | ⚠️ Limited | ✅ Yes |
| Custom Workflows | ✅ Yes | ⚠️ Limited |
| API Access | ✅ Direct | ⚠️ Manual |
| Automation | ✅ Easy | ⚠️ Complex |

### vs. QRadar API Direct
| Feature | MCP Server | Direct API |
|---------|-----------|-----------|
| Ease of Use | ✅ High | ⚠️ Low |
| Authentication | ✅ Configured | ⚠️ Manual |
| Error Handling | ✅ Built-in | ❌ Manual |
| Documentation | ✅ Extensive | ⚠️ Technical |
| AI Integration | ✅ Native | ❌ None |
| Learning Curve | ✅ Easy | ⚠️ Steep |

---

## 📈 Version History

### v0.2.0 (Current)
- 41 total tools (25 new)
- Advanced offense management
- Saved search execution
- Discovery and introspection tools
- User and domain management
- Complete workflows

### v0.1.0
- 16 core tools
- Basic event queries
- Offense listing
- Log source monitoring

---

## 🔮 Roadmap

### Planned Features
- Reference set modification (add/remove IOCs)
- Bulk offense operations
- Event streaming/monitoring
- Custom rule creation
- Data export formats
- Multiple instance support

---

## 🤝 Support

- **Issues**: Report bugs or request features
- **Documentation**: Comprehensive guides available
- **Community**: Share workflows and patterns
- **Updates**: Regular feature additions

---

**Last Updated**: November 2024  
**Version**: 0.2.0  
**Status**: Production Ready ✅

