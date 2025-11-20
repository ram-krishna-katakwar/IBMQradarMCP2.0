# IBM QRadar MCP - Advanced Features

This document describes the advanced features and tools available in the IBM QRadar MCP server.

## Overview

In addition to the basic event querying, offense management, and log source monitoring, the QRadar MCP server now includes **25 additional advanced tools** for comprehensive security operations and incident response workflows.

## New Tool Categories

- **Saved Search Management** (3 tools)
- **Offense Management Enhancements** (5 tools)
- **Custom Properties** (2 tools)
- **Domain Management** (2 tools)
- **Network Hierarchy** (1 tool)
- **Ariel Database Introspection** (2 tools)
- **Event Category Discovery** (2 tools)
- **Building Blocks** (2 tools)
- **User Management** (2 tools)
- **Reports & Applications** (1 tool)

**Total Tools**: 41 (16 original + 25 new)

---

## Saved Search Management

### Overview
Saved searches are pre-configured AQL queries that can be reused for common investigations. These tools allow you to discover, inspect, and execute saved searches.

### Tools

#### `qradar_get_saved_searches`
List all saved Ariel searches configured in QRadar.

**Use Cases**:
- Discover available pre-configured queries
- Audit saved search inventory
- Find searches created by other analysts

**Example**:
```
Show me all saved searches in QRadar
```

**Response includes**:
- Search ID
- Search name
- AQL query
- Owner
- Last execution time

---

#### `qradar_get_saved_search_by_id`
Get detailed information about a specific saved search.

**Parameters**:
- `search_id` (required): The saved search ID

**Example**:
```
Get details for saved search ID "abc-123-def"
```

---

#### `qradar_execute_saved_search`
Execute a saved search and return results.

**Parameters**:
- `search_id` (required): The saved search ID to execute
- `max_wait` (optional): Maximum wait time in seconds (default: 300)

**Use Cases**:
- Run standardized compliance queries
- Execute scheduled investigation queries
- Reuse proven search patterns

**Example**:
```
Execute saved search "Failed_SSH_Logins_24h"
```

**Best Practices**:
- Use descriptive names for saved searches
- Document search purposes in descriptions
- Regularly review and update saved searches

---

## Offense Management Enhancements

### Overview
Enhanced offense management capabilities for full incident response workflows including note-taking, status updates, assignment, and closure.

### Tools

#### `qradar_get_offense_notes`
Retrieve all notes/annotations for a specific offense.

**Parameters**:
- `offense_id` (required): The offense ID

**Use Cases**:
- Review investigation history
- Understand previous analyst findings
- Audit incident response actions

**Example**:
```
Show me all notes for offense 42
```

**Response includes**:
- Note ID
- Note text
- Username (who added it)
- Creation timestamp

---

#### `qradar_add_offense_note`
Add a note/annotation to an offense.

**Parameters**:
- `offense_id` (required): The offense ID
- `note_text` (required): The note text to add

**Use Cases**:
- Document investigation findings
- Record actions taken
- Share context with team members
- Create audit trail

**Example**:
```
Add note to offense 42: "Confirmed false positive - employee VPN connection from home network"
```

**Best Practices**:
- Include timestamp references
- Document evidence reviewed
- Note actions taken and results
- Tag team members when needed
- Use structured format for consistency

---

#### `qradar_update_offense_status`
Update the status of an offense.

**Parameters**:
- `offense_id` (required): The offense ID
- `status` (required): New status (OPEN, HIDDEN, CLOSED)
- `closing_reason_id` (optional): Required when closing (status=CLOSED)

**Use Cases**:
- Close resolved incidents
- Hide false positives
- Reopen closed offenses for review

**Example**:
```
Close offense 42 with closing reason ID 3
```

**Status Options**:
- **OPEN**: Active investigation required
- **HIDDEN**: Acknowledged but deprioritized (false positive, low priority)
- **CLOSED**: Investigation complete

**Workflow**:
1. Get closing reasons: `qradar_get_closing_reasons`
2. Select appropriate reason ID
3. Update offense status with reason

---

#### `qradar_get_closing_reasons`
Get available offense closing reasons.

**Use Cases**:
- Discover available closing reason IDs
- Understand closure categories
- Standardize incident closure

**Example**:
```
What closing reasons are available for offenses?
```

**Common Closing Reasons**:
- False Positive (Tuned)
- Non-Issue
- Policy Violation
- Malicious Activity Confirmed
- Testing Activity

---

#### `qradar_assign_offense`
Assign an offense to a specific user.

**Parameters**:
- `offense_id` (required): The offense ID
- `assigned_to` (required): Username to assign to

**Use Cases**:
- Distribute workload among analysts
- Track ownership and accountability
- Escalate to senior analysts
- Handoff between shifts

**Example**:
```
Assign offense 42 to user "john.smith"
```

**Best Practices**:
- Assign based on expertise and workload
- Add assignment note explaining context
- Notify assigned user out-of-band if urgent
- Reassign if no progress after defined time

---

## Complete Incident Response Workflow Example

Here's a complete workflow using the enhanced offense management tools:

```
# 1. Discover open high-severity offenses
"Show me all open offenses with severity >= 7"

# 2. Get offense details
"Get details for offense 156"

# 3. Review investigation history
"Show me all notes for offense 156"

# 4. Investigate related events
"Search events related to offense 156 - SELECT * FROM events WHERE sourceip='10.0.1.45' LAST 24 HOURS"

# 5. Document findings
"Add note to offense 156: 'Investigated source IP 10.0.1.45. Found 247 failed authentication attempts from this IP. Confirmed unauthorized access attempt. Blocked IP at firewall level and reset affected user credentials.'"

# 6. Get available closing reasons
"What closing reasons are available?"

# 7. Close the offense
"Close offense 156 with closing reason ID 1 (Malicious Activity Confirmed)"

# 8. Verify closure
"Get details for offense 156"
```

---

## Custom Properties

### Overview
Custom properties are user-defined fields for events, flows, and offenses. These tools help you discover and work with custom data enrichments.

### Tools

#### `qradar_get_custom_properties`
Get all custom properties defined in QRadar.

**Use Cases**:
- Discover available custom fields
- Understand data enrichments
- Build queries using custom properties
- Audit custom property usage

**Example**:
```
Show me all custom properties in QRadar
```

**Response includes**:
- Property ID
- Property name
- Property type (STRING, NUMERIC, IP, etc.)
- Description
- Associated with (events, flows, offenses)

---

#### `qradar_get_custom_property_by_id`
Get details of a specific custom property.

**Parameters**:
- `property_id` (required): The custom property ID

**Example**:
```
Get details for custom property 1001
```

**Using Custom Properties in AQL**:
```sql
-- Query events using custom property
SELECT sourceip, destinationip, "Custom_Threat_Score" 
FROM events 
WHERE "Custom_Threat_Score" > 7 
LAST 24 HOURS
```

---

## Domain Management

### Overview
Domains provide multi-tenancy in QRadar, segregating data and users. These tools help you work with domain-separated deployments.

### Tools

#### `qradar_get_domains`
Get all domains configured in QRadar.

**Use Cases**:
- Understand tenant structure
- Identify data segregation boundaries
- Plan cross-domain investigations
- Audit multi-tenant configuration

**Example**:
```
Show me all domains in QRadar
```

**Response includes**:
- Domain ID
- Domain name
- Description
- Tenant ID

---

#### `qradar_get_domain_by_id`
Get details of a specific domain.

**Parameters**:
- `domain_id` (required): The domain ID

**Example**:
```
Get details for domain 2
```

**Multi-Tenant Use Cases**:
- MSSP with multiple customers
- Enterprise with business unit separation
- Regulatory compliance requirements
- Data residency requirements

---

## Network Hierarchy

### Overview
Network hierarchy defines how network segments and objects are organized in QRadar.

### Tools

#### `qradar_get_network_hierarchy`
Get network hierarchy configuration.

**Use Cases**:
- Understand network topology
- Identify network segments
- Plan network-based queries
- Validate network object definitions

**Example**:
```
Show me the network hierarchy
```

**Response includes**:
- Network object ID
- Network name
- CIDR notation
- Description
- Domain assignment

**Using Network Objects in AQL**:
```sql
-- Query events from specific network segment
SELECT * FROM events 
WHERE sourceip IN '10.0.0.0/8' 
LAST 24 HOURS
```

---

## Ariel Database Introspection

### Overview
These tools help you understand what data is available for querying and what fields can be used in AQL queries.

### Tools

#### `qradar_get_ariel_databases`
Get available Ariel databases.

**Use Cases**:
- Discover available data sources
- Understand query capabilities
- Validate database names for queries

**Example**:
```
What Ariel databases are available?
```

**Typical Databases**:
- `events` - Security events
- `flows` - Network flows

---

#### `qradar_get_ariel_fields`
Get available fields for Ariel queries.

**Parameters**:
- `database_name` (optional): Database name (default: "events")

**Use Cases**:
- Build correct AQL queries
- Discover available fields
- Understand field data types
- Validate field names

**Example**:
```
What fields are available for events queries?
```

**Response includes**:
- Field name
- Field type (STRING, NUMERIC, IP, etc.)
- Description
- Is indexed (for performance)

**Building Queries**:
```
1. "What fields are available for events?"
2. Review available fields
3. "Search events: SELECT sourceip, username, qidname FROM events WHERE severity >= 5 LAST 1 HOURS"
```

---

## Event Category Discovery

### Overview
Event categories classify events by type (authentication, network activity, malware, etc.). These tools help you find the right categories for your queries.

### Tools

#### `qradar_get_event_categories`
Get all event categories.

**Use Cases**:
- Discover available categories
- Understand event classification
- Find category IDs for queries
- Analyze event distribution

**Example**:
```
Show me all event categories
```

**Response includes**:
- QID (unique event identifier)
- Category ID
- Category name
- Severity
- Description

---

#### `qradar_search_event_categories`
Search event categories by name.

**Parameters**:
- `search_term` (required): Term to search for

**Use Cases**:
- Find authentication-related categories
- Discover malware detection categories
- Locate specific event types
- Build targeted queries

**Example**:
```
Search event categories for "authentication"
```

**Common Categories**:
- **1003**: Authentication failures
- **12**: Malware detection
- **18**: System notifications
- **2**: Network activity

**Using Categories in AQL**:
```sql
-- Query authentication events
SELECT * FROM events 
WHERE category=1003 
LAST 24 HOURS

-- Query malware events
SELECT * FROM events 
WHERE category=12 
LAST 7 DAYS
```

---

## Building Blocks

### Overview
Building blocks are reusable rule components used to create complex detection rules. They represent logical conditions that can be shared across multiple rules.

### Tools

#### `qradar_get_building_blocks`
Get all building blocks.

**Parameters**:
- `filter` (optional): Filter string (e.g., "enabled=true")

**Use Cases**:
- Discover reusable rule components
- Understand detection logic
- Audit rule dependencies
- Find building blocks for rule creation

**Example**:
```
Show me all enabled building blocks
```

**Response includes**:
- Building block ID
- Name
- Description
- Enabled status
- Tests performed

---

#### `qradar_get_building_block_by_id`
Get details of a specific building block.

**Parameters**:
- `block_id` (required): The building block ID

**Example**:
```
Get details for building block 100
```

**Use Cases**:
- Understand detection logic
- Review rule components
- Plan rule modifications
- Troubleshoot false positives

---

## User Management

### Overview
User management tools help you work with QRadar users for offense assignment, access auditing, and collaboration.

### Tools

#### `qradar_get_users`
Get all QRadar users.

**Use Cases**:
- Discover available users for assignment
- Audit user access
- Plan team structure
- Verify user accounts

**Example**:
```
Show me all QRadar users
```

**Response includes**:
- User ID
- Username
- Email
- Role
- Last login
- Status (enabled/disabled)

---

#### `qradar_get_user_by_id`
Get details of a specific user.

**Parameters**:
- `user_id` (required): The user ID

**Example**:
```
Get details for user 5
```

**User Assignment Workflow**:
```
1. "Show me all QRadar users"
2. Identify appropriate analyst
3. "Assign offense 42 to user 'analyst_name'"
4. "Add note to offense 42: 'Assigned to analyst_name for investigation'"
```

---

## Reports & Applications

### Overview
Discover installed applications and report templates in QRadar.

### Tools

#### `qradar_get_reports`
Get all available reports and applications.

**Use Cases**:
- Discover installed apps
- Find available report templates
- Understand QRadar extensions
- Plan report generation

**Example**:
```
What reports and applications are available?
```

**Response includes**:
- Application ID
- Application name
- Version
- Description
- Installed date

---

## Advanced Query Patterns

### Pattern 1: Complete Incident Investigation

```
# Start with high-priority offense
"Show me open offenses with severity >= 8"

# Get offense details
"Get details for offense 234"

# Review notes
"Show notes for offense 234"

# Get related user info
"Get user details for the assigned analyst"

# Check related events with custom properties
"What custom properties are available?"

# Query with custom enrichment
"Search events: SELECT sourceip, 'Custom_GeoLocation', 'Custom_Threat_Intel' FROM events WHERE sourceip='192.168.1.50' LAST 48 HOURS"

# Add investigation note
"Add note to offense 234: 'Reviewed custom threat intel - IP confirmed in malicious actor database'"

# Close offense
"Close offense 234 with appropriate closing reason"
```

### Pattern 2: AQL Query Building

```
# Discover available fields
"What fields are available for events queries?"

# Find relevant event categories
"Search event categories for 'malware'"

# Build query using discovered information
"Search events: SELECT sourceip, destinationip, qidname, category FROM events WHERE category=12 LAST 24 HOURS"

# Export or save results
"Execute this search and save results"
```

### Pattern 3: Multi-Domain Investigation

```
# Check domain structure
"Show me all domains"

# Get domain details
"Get details for domain 3"

# Query domain-specific data
"Show offenses in domain 3"

# Check network hierarchy for domain
"Show network hierarchy"

# Query using network segments
"Search events from network segment '10.3.0.0/16' in the last day"
```

### Pattern 4: Saved Search Workflow

```
# Discover saved searches
"Show me all saved searches"

# Review specific search
"Get details for saved search 'Daily_Auth_Failures'"

# Execute saved search
"Execute saved search 'Daily_Auth_Failures'"

# Add findings to related offense
"Add note to offense 156: 'Executed daily auth failures search - found 15 new failed attempts from same IP'"
```

### Pattern 5: Building Block Analysis

```
# Find building blocks
"Show me all enabled building blocks"

# Get building block details
"Get details for building block 205"

# Find rules using this building block
"Show me rules that use building block 205"

# Review rule logic
"Get details for rule 1042"
```

---

## Best Practices

### Offense Management
1. **Always add notes** when investigating offenses
2. **Use closing reasons consistently** for reporting and metrics
3. **Assign offenses promptly** to ensure accountability
4. **Review notes** before taking action to avoid duplicate work
5. **Update status regularly** to reflect investigation progress

### Query Optimization
1. **Use field introspection** before building complex queries
2. **Leverage saved searches** for repeated investigations
3. **Filter by category** to narrow results efficiently
4. **Use custom properties** when available for enriched context
5. **Start with small time ranges** and expand as needed

### Multi-Tenancy
1. **Verify domain context** before cross-domain queries
2. **Respect domain boundaries** in multi-tenant environments
3. **Use network hierarchy** to understand topology
4. **Document domain-specific** configurations

### Collaboration
1. **Assign offenses** to distribute workload
2. **Add detailed notes** for team visibility
3. **Reference building blocks** and rules in notes
4. **Use saved searches** for team consistency
5. **Review user activity** for audit and optimization

---

## Security Considerations

### Write Operations
The following tools **modify data** and should be used with caution:
- `qradar_add_offense_note`
- `qradar_update_offense_status`
- `qradar_assign_offense`

**Recommendations**:
- Use service accounts with minimal required permissions
- Audit all write operations
- Implement approval workflows for closure
- Train users on proper usage

### Permissions Required
Different tools require different QRadar API permissions:

| Tool Category | Required Permission |
|--------------|-------------------|
| Saved Searches | Ariel |
| Offense Notes | Offenses (Read/Write) |
| Offense Status | Offenses (Write) |
| Custom Properties | System |
| Domains | System |
| Users | Admin |
| Building Blocks | Analytics Rules |

---

## Troubleshooting

### Permission Errors
**Error**: `403 Forbidden` or "insufficient capabilities"

**Solution**:
1. Check API token permissions in QRadar Console
2. Go to Admin → Authorized Services
3. Add required permissions for specific tool
4. Generate new token if needed

### Tool Not Found
**Error**: `Unknown tool: qradar_xxx`

**Solution**:
1. Verify you're running the latest version
2. Restart the MCP server
3. Check Claude Desktop configuration
4. Review server logs

### Timeout Errors
**Error**: Search or query timeout

**Solution**:
1. Increase `max_wait` parameter
2. Narrow time range in queries
3. Add more specific filters
4. Check QRadar server load

---

## Tool Summary Table

| Tool | Category | Write | Key Use Case |
|------|----------|-------|--------------|
| `qradar_get_saved_searches` | Saved Searches | No | List saved queries |
| `qradar_get_saved_search_by_id` | Saved Searches | No | View search details |
| `qradar_execute_saved_search` | Saved Searches | No | Run saved query |
| `qradar_get_offense_notes` | Offenses | No | View investigation history |
| `qradar_add_offense_note` | Offenses | **Yes** | Document findings |
| `qradar_update_offense_status` | Offenses | **Yes** | Close/hide offenses |
| `qradar_get_closing_reasons` | Offenses | No | Get closure options |
| `qradar_assign_offense` | Offenses | **Yes** | Assign to analyst |
| `qradar_get_custom_properties` | Config | No | List custom fields |
| `qradar_get_custom_property_by_id` | Config | No | View property details |
| `qradar_get_domains` | Config | No | List tenants |
| `qradar_get_domain_by_id` | Config | No | View domain details |
| `qradar_get_network_hierarchy` | Config | No | View network topology |
| `qradar_get_ariel_databases` | Discovery | No | List data sources |
| `qradar_get_ariel_fields` | Discovery | No | List query fields |
| `qradar_get_event_categories` | Discovery | No | List event types |
| `qradar_search_event_categories` | Discovery | No | Find categories |
| `qradar_get_building_blocks` | Analytics | No | List rule components |
| `qradar_get_building_block_by_id` | Analytics | No | View block details |
| `qradar_get_users` | Users | No | List QRadar users |
| `qradar_get_user_by_id` | Users | No | View user details |
| `qradar_get_reports` | Reports | No | List apps/reports |

---

## Version History

### Version 0.2.0 (Current)
- Added 25 new tools
- Enhanced offense management
- Added saved search capabilities
- Added domain and user management
- Added discovery and introspection tools
- Improved incident response workflows

### Version 0.1.0
- Initial release
- 16 core tools
- Basic event queries
- Offense listing
- Log source monitoring

---

## Resources

- [QRadar API Documentation](https://www.ibm.com/docs/en/qradar-common)
- [AQL Reference Guide](https://www.ibm.com/docs/en/qradar-common?topic=structure-aql-overview)
- [Offense Management Best Practices](https://www.ibm.com/docs/en/qradar-common?topic=offenses-managing)
- [Custom Properties Guide](https://www.ibm.com/docs/en/qradar-common?topic=properties-custom)

---

**For basic usage and setup, see [README.md](README.md) and [QUICK_START.md](QUICK_START.md)**

