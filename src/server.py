"""IBM QRadar MCP Server

This MCP server provides tools to interact with IBM QRadar for querying logs, events, and agents.

Author: Ram Krishna Katakwar
Version: 0.2.0
License: MIT
"""
import os
import json
import logging
from typing import Any, Sequence
from dotenv import load_dotenv

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from .qradar_client import QRadarClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qradar-mcp")

# Initialize QRadar client
qradar_host = os.getenv("QRADAR_HOST")
qradar_token = os.getenv("QRADAR_API_TOKEN")
verify_ssl = os.getenv("QRADAR_VERIFY_SSL", "true").lower() == "true"

if not qradar_host or not qradar_token:
    raise ValueError("QRADAR_HOST and QRADAR_API_TOKEN must be set in environment variables")

qradar_client = QRadarClient(qradar_host, qradar_token, verify_ssl)

# Initialize MCP server
app = Server("ibm-qradar-mcp")


def format_response(data: Any, success: bool = True, message: str = "") -> list[TextContent]:
    """Format API response as MCP TextContent"""
    response = {
        "success": success,
        "message": message,
        "data": data
    }
    return [TextContent(
        type="text",
        text=json.dumps(response, indent=2, default=str)
    )]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available QRadar tools"""
    return [
        # ==================== Event and Log Query Tools ====================
        Tool(
            name="qradar_search_events",
            description=(
                "Search QRadar events using AQL (Ariel Query Language). "
                "Use this to query security events with custom AQL queries. "
                "Example query: 'SELECT sourceip, destinationip, username FROM events WHERE eventcount > 10 LAST 24 HOURS'"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "AQL query string to search events"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Query timeout in seconds (default: 60)",
                        "default": 60
                    },
                    "max_wait": {
                        "type": "integer",
                        "description": "Maximum time to wait for results in seconds (default: 300)",
                        "default": 300
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="qradar_get_recent_events",
            description=(
                "Get recent events from QRadar. Returns the most recent security events. "
                "You can specify the number of events and which fields to return."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of events to return (default: 50)",
                        "default": 50
                    },
                    "fields": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of fields to return (e.g., ['sourceip', 'destinationip', 'username'])"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="qradar_search_flows",
            description=(
                "Search network flows using AQL. Use this to query network traffic data. "
                "Example query: 'SELECT sourceip, destinationip, sourceport, destinationport FROM flows LAST 1 HOURS'"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "AQL query string to search network flows"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Query timeout in seconds (default: 60)",
                        "default": 60
                    },
                    "max_wait": {
                        "type": "integer",
                        "description": "Maximum time to wait for results in seconds (default: 300)",
                        "default": 300
                    }
                },
                "required": ["query"]
            }
        ),
        
        # ==================== Offense Tools ====================
        Tool(
            name="qradar_get_offenses",
            description=(
                "Get offenses (security incidents) from QRadar. Offenses are collections of events "
                "that QRadar has determined may require investigation. You can filter by status, "
                "time range, and other criteria."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "description": "Filter string (e.g., 'status=OPEN' or 'severity >= 7')"
                    },
                    "fields": {
                        "type": "string",
                        "description": "Comma-separated list of fields to return"
                    },
                    "range": {
                        "type": "string",
                        "description": "Range of results to return (e.g., '0-49' for first 50 results)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="qradar_get_offense_by_id",
            description="Get detailed information about a specific offense by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "offense_id": {
                        "type": "integer",
                        "description": "The offense ID to retrieve"
                    }
                },
                "required": ["offense_id"]
            }
        ),
        
        # ==================== Log Source (Agent) Tools ====================
        Tool(
            name="qradar_get_log_sources",
            description=(
                "Get log sources (agents/collectors) from QRadar. Log sources are the systems "
                "sending security data to QRadar (firewalls, servers, applications, etc.)"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "description": "Filter string (e.g., 'enabled=true' or 'status=CONNECTED')"
                    },
                    "fields": {
                        "type": "string",
                        "description": "Comma-separated list of fields to return"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="qradar_get_log_source_by_id",
            description="Get detailed information about a specific log source by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "log_source_id": {
                        "type": "integer",
                        "description": "The log source ID to retrieve"
                    }
                },
                "required": ["log_source_id"]
            }
        ),
        Tool(
            name="qradar_get_log_source_types",
            description=(
                "Get available log source types. This shows what types of systems "
                "QRadar can collect logs from (e.g., Cisco ASA, Windows, Linux, etc.)"
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        
        # ==================== Asset Tools ====================
        Tool(
            name="qradar_get_assets",
            description=(
                "Get assets from QRadar. Assets are hosts, servers, and devices "
                "that QRadar has discovered on your network."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "description": "Filter string for assets"
                    },
                    "fields": {
                        "type": "string",
                        "description": "Comma-separated list of fields to return"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="qradar_search_assets_by_ip",
            description="Search for assets by IP address",
            inputSchema={
                "type": "object",
                "properties": {
                    "ip_address": {
                        "type": "string",
                        "description": "IP address to search for"
                    }
                },
                "required": ["ip_address"]
            }
        ),
        
        # ==================== Reference Data Tools ====================
        Tool(
            name="qradar_get_reference_sets",
            description=(
                "Get reference data sets. Reference sets are lists of data (IPs, domains, etc.) "
                "used in QRadar rules and for threat intelligence."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="qradar_get_reference_set_data",
            description="Get data from a specific reference set by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "ref_set_name": {
                        "type": "string",
                        "description": "Name of the reference set"
                    }
                },
                "required": ["ref_set_name"]
            }
        ),
        
        # ==================== System Information Tools ====================
        Tool(
            name="qradar_get_system_info",
            description="Get QRadar system information (version, license, etc.)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="qradar_get_servers",
            description="Get QRadar servers/hosts information",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        
        # ==================== Rules Tools ====================
        Tool(
            name="qradar_get_rules",
            description=(
                "Get analytics rules from QRadar. Rules define how QRadar processes "
                "and correlates events to detect security threats."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "description": "Filter string (e.g., 'enabled=true')"
                    },
                    "fields": {
                        "type": "string",
                        "description": "Comma-separated list of fields to return"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="qradar_get_rule_by_id",
            description="Get detailed information about a specific rule by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "rule_id": {
                        "type": "integer",
                        "description": "The rule ID to retrieve"
                    }
                },
                "required": ["rule_id"]
            }
        ),
        
        # ==================== Saved Search Tools ====================
        Tool(
            name="qradar_get_saved_searches",
            description=(
                "Get all saved Ariel searches. Saved searches are pre-defined AQL queries "
                "that can be reused for common investigations."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="qradar_get_saved_search_by_id",
            description="Get details of a specific saved search by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_id": {
                        "type": "string",
                        "description": "The saved search ID"
                    }
                },
                "required": ["search_id"]
            }
        ),
        Tool(
            name="qradar_execute_saved_search",
            description=(
                "Execute a saved search by ID. This will run the pre-configured AQL query "
                "and return the results."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "search_id": {
                        "type": "string",
                        "description": "The saved search ID to execute"
                    },
                    "max_wait": {
                        "type": "integer",
                        "description": "Maximum time to wait for results in seconds (default: 300)",
                        "default": 300
                    }
                },
                "required": ["search_id"]
            }
        ),
        
        # ==================== Offense Note Tools ====================
        Tool(
            name="qradar_get_offense_notes",
            description=(
                "Get all notes/annotations for a specific offense. Notes provide context "
                "and investigation details about security incidents."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "offense_id": {
                        "type": "integer",
                        "description": "The offense ID"
                    }
                },
                "required": ["offense_id"]
            }
        ),
        Tool(
            name="qradar_add_offense_note",
            description=(
                "Add a note/annotation to an offense. Use this to document investigation "
                "findings, actions taken, or analysis results."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "offense_id": {
                        "type": "integer",
                        "description": "The offense ID"
                    },
                    "note_text": {
                        "type": "string",
                        "description": "The note text to add"
                    }
                },
                "required": ["offense_id", "note_text"]
            }
        ),
        Tool(
            name="qradar_update_offense_status",
            description=(
                "Update the status of an offense (OPEN, HIDDEN, CLOSED). "
                "When closing an offense, a closing reason ID must be provided."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "offense_id": {
                        "type": "integer",
                        "description": "The offense ID"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status: OPEN, HIDDEN, or CLOSED",
                        "enum": ["OPEN", "HIDDEN", "CLOSED"]
                    },
                    "closing_reason_id": {
                        "type": "integer",
                        "description": "Closing reason ID (required when status is CLOSED)"
                    }
                },
                "required": ["offense_id", "status"]
            }
        ),
        Tool(
            name="qradar_get_closing_reasons",
            description=(
                "Get available offense closing reasons. Use these IDs when closing offenses."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="qradar_assign_offense",
            description=(
                "Assign an offense to a specific user for investigation. "
                "This helps with workload distribution and tracking."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "offense_id": {
                        "type": "integer",
                        "description": "The offense ID"
                    },
                    "assigned_to": {
                        "type": "string",
                        "description": "Username to assign the offense to"
                    }
                },
                "required": ["offense_id", "assigned_to"]
            }
        ),
        
        # ==================== Custom Property Tools ====================
        Tool(
            name="qradar_get_custom_properties",
            description=(
                "Get all custom properties defined in QRadar. Custom properties are "
                "user-defined fields for events, flows, and offenses."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="qradar_get_custom_property_by_id",
            description="Get details of a specific custom property by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "property_id": {
                        "type": "integer",
                        "description": "The custom property ID"
                    }
                },
                "required": ["property_id"]
            }
        ),
        
        # ==================== Domain Management Tools ====================
        Tool(
            name="qradar_get_domains",
            description=(
                "Get all domains configured in QRadar. Domains are used for multi-tenancy "
                "to segregate data and users."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="qradar_get_domain_by_id",
            description="Get details of a specific domain by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain_id": {
                        "type": "integer",
                        "description": "The domain ID"
                    }
                },
                "required": ["domain_id"]
            }
        ),
        
        # ==================== Network Hierarchy Tools ====================
        Tool(
            name="qradar_get_network_hierarchy",
            description=(
                "Get network hierarchy configuration. This shows how network segments "
                "and objects are organized in QRadar."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        
        # ==================== Ariel Database Tools ====================
        Tool(
            name="qradar_get_ariel_databases",
            description=(
                "Get available Ariel databases (events, flows). This helps understand "
                "what data sources are available for querying."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="qradar_get_ariel_fields",
            description=(
                "Get available fields for Ariel queries. This is useful for building "
                "AQL queries by knowing what fields can be queried."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "database_name": {
                        "type": "string",
                        "description": "Database name (events or flows)",
                        "default": "events"
                    }
                },
                "required": []
            }
        ),
        
        # ==================== Event Category Tools ====================
        Tool(
            name="qradar_get_event_categories",
            description=(
                "Get all event categories. Categories classify events by type "
                "(authentication, network activity, malware, etc.)."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="qradar_search_event_categories",
            description=(
                "Search event categories by name. Useful for finding the right "
                "category ID to use in AQL queries."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "Term to search for in category names"
                    }
                },
                "required": ["search_term"]
            }
        ),
        
        # ==================== Building Block Tools ====================
        Tool(
            name="qradar_get_building_blocks",
            description=(
                "Get building blocks. Building blocks are reusable rule components "
                "that can be used to create complex detection rules."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "description": "Filter string (e.g., 'enabled=true')"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="qradar_get_building_block_by_id",
            description="Get detailed information about a specific building block by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "block_id": {
                        "type": "integer",
                        "description": "The building block ID"
                    }
                },
                "required": ["block_id"]
            }
        ),
        
        # ==================== User Management Tools ====================
        Tool(
            name="qradar_get_users",
            description=(
                "Get all QRadar users. This shows who has access to the system "
                "and can be used for offense assignment."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="qradar_get_user_by_id",
            description="Get details of a specific user by their ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The user ID"
                    }
                },
                "required": ["user_id"]
            }
        ),
        
        # ==================== Reports Tools ====================
        Tool(
            name="qradar_get_reports",
            description=(
                "Get all available reports and applications in QRadar. "
                "This shows installed apps and report templates."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool execution"""
    
    try:
        # ==================== Event and Log Query Tools ====================
        
        if name == "qradar_search_events":
            query = arguments.get("query")
            timeout = arguments.get("timeout", 60)
            max_wait = arguments.get("max_wait", 300)
            
            logger.info(f"Searching events with query: {query}")
            result = qradar_client.search_events(query, timeout, max_wait)
            return format_response(result, message=f"Found {result.get('record_count', 0)} events")
        
        elif name == "qradar_get_recent_events":
            limit = arguments.get("limit", 50)
            fields = arguments.get("fields")
            
            logger.info(f"Getting {limit} recent events")
            result = qradar_client.get_recent_events(limit, fields)
            return format_response(result, message=f"Retrieved {result.get('record_count', 0)} events")
        
        elif name == "qradar_search_flows":
            query = arguments.get("query")
            timeout = arguments.get("timeout", 60)
            max_wait = arguments.get("max_wait", 300)
            
            logger.info(f"Searching flows with query: {query}")
            result = qradar_client.search_flows(query, timeout, max_wait)
            return format_response(result, message=f"Found {result.get('record_count', 0)} flows")
        
        # ==================== Offense Tools ====================
        
        elif name == "qradar_get_offenses":
            filter_query = arguments.get("filter")
            fields = arguments.get("fields")
            range_header = arguments.get("range")
            
            logger.info("Getting offenses")
            result = qradar_client.get_offenses(filter_query, fields, range_header)
            return format_response(result, message=f"Retrieved {len(result)} offenses")
        
        elif name == "qradar_get_offense_by_id":
            offense_id = arguments.get("offense_id")
            
            logger.info(f"Getting offense {offense_id}")
            result = qradar_client.get_offense_by_id(offense_id)
            return format_response(result, message=f"Retrieved offense {offense_id}")
        
        # ==================== Log Source (Agent) Tools ====================
        
        elif name == "qradar_get_log_sources":
            filter_query = arguments.get("filter")
            fields = arguments.get("fields")
            
            logger.info("Getting log sources")
            result = qradar_client.get_log_sources(filter_query, fields)
            return format_response(result, message=f"Retrieved {len(result)} log sources")
        
        elif name == "qradar_get_log_source_by_id":
            log_source_id = arguments.get("log_source_id")
            
            logger.info(f"Getting log source {log_source_id}")
            result = qradar_client.get_log_source_by_id(log_source_id)
            return format_response(result, message=f"Retrieved log source {log_source_id}")
        
        elif name == "qradar_get_log_source_types":
            logger.info("Getting log source types")
            result = qradar_client.get_log_source_types()
            return format_response(result, message=f"Retrieved {len(result)} log source types")
        
        # ==================== Asset Tools ====================
        
        elif name == "qradar_get_assets":
            filter_query = arguments.get("filter")
            fields = arguments.get("fields")
            
            logger.info("Getting assets")
            result = qradar_client.get_assets(filter_query, fields)
            return format_response(result, message=f"Retrieved {len(result)} assets")
        
        elif name == "qradar_search_assets_by_ip":
            ip_address = arguments.get("ip_address")
            
            logger.info(f"Searching assets by IP: {ip_address}")
            result = qradar_client.search_assets(ip_address)
            return format_response(result, message=f"Found {len(result)} assets with IP {ip_address}")
        
        # ==================== Reference Data Tools ====================
        
        elif name == "qradar_get_reference_sets":
            logger.info("Getting reference sets")
            result = qradar_client.get_reference_sets()
            return format_response(result, message=f"Retrieved {len(result)} reference sets")
        
        elif name == "qradar_get_reference_set_data":
            ref_set_name = arguments.get("ref_set_name")
            
            logger.info(f"Getting reference set data: {ref_set_name}")
            result = qradar_client.get_reference_set_data(ref_set_name)
            return format_response(result, message=f"Retrieved data for reference set '{ref_set_name}'")
        
        # ==================== System Information Tools ====================
        
        elif name == "qradar_get_system_info":
            logger.info("Getting system info")
            result = qradar_client.get_system_info()
            return format_response(result, message="Retrieved system information")
        
        elif name == "qradar_get_servers":
            logger.info("Getting servers")
            result = qradar_client.get_servers()
            return format_response(result, message=f"Retrieved {len(result)} servers")
        
        # ==================== Rules Tools ====================
        
        elif name == "qradar_get_rules":
            filter_query = arguments.get("filter")
            fields = arguments.get("fields")
            
            logger.info("Getting rules")
            result = qradar_client.get_rules(filter_query, fields)
            return format_response(result, message=f"Retrieved {len(result)} rules")
        
        elif name == "qradar_get_rule_by_id":
            rule_id = arguments.get("rule_id")
            
            logger.info(f"Getting rule {rule_id}")
            result = qradar_client.get_rule_by_id(rule_id)
            return format_response(result, message=f"Retrieved rule {rule_id}")
        
        # ==================== Saved Search Tools ====================
        
        elif name == "qradar_get_saved_searches":
            logger.info("Getting saved searches")
            result = qradar_client.get_saved_searches()
            return format_response(result, message=f"Retrieved {len(result)} saved searches")
        
        elif name == "qradar_get_saved_search_by_id":
            search_id = arguments.get("search_id")
            
            logger.info(f"Getting saved search {search_id}")
            result = qradar_client.get_saved_search_by_id(search_id)
            return format_response(result, message=f"Retrieved saved search {search_id}")
        
        elif name == "qradar_execute_saved_search":
            search_id = arguments.get("search_id")
            max_wait = arguments.get("max_wait", 300)
            
            logger.info(f"Executing saved search {search_id}")
            result = qradar_client.execute_saved_search(search_id, max_wait)
            return format_response(result, message=f"Executed saved search {search_id}")
        
        # ==================== Offense Note Tools ====================
        
        elif name == "qradar_get_offense_notes":
            offense_id = arguments.get("offense_id")
            
            logger.info(f"Getting notes for offense {offense_id}")
            result = qradar_client.get_offense_notes(offense_id)
            return format_response(result, message=f"Retrieved {len(result)} notes for offense {offense_id}")
        
        elif name == "qradar_add_offense_note":
            offense_id = arguments.get("offense_id")
            note_text = arguments.get("note_text")
            
            logger.info(f"Adding note to offense {offense_id}")
            result = qradar_client.add_offense_note(offense_id, note_text)
            return format_response(result, message=f"Added note to offense {offense_id}")
        
        elif name == "qradar_update_offense_status":
            offense_id = arguments.get("offense_id")
            status = arguments.get("status")
            closing_reason_id = arguments.get("closing_reason_id")
            
            logger.info(f"Updating offense {offense_id} status to {status}")
            result = qradar_client.update_offense_status(offense_id, status, closing_reason_id)
            return format_response(result, message=f"Updated offense {offense_id} status to {status}")
        
        elif name == "qradar_get_closing_reasons":
            logger.info("Getting closing reasons")
            result = qradar_client.get_closing_reasons()
            return format_response(result, message=f"Retrieved {len(result)} closing reasons")
        
        elif name == "qradar_assign_offense":
            offense_id = arguments.get("offense_id")
            assigned_to = arguments.get("assigned_to")
            
            logger.info(f"Assigning offense {offense_id} to {assigned_to}")
            result = qradar_client.assign_offense(offense_id, assigned_to)
            return format_response(result, message=f"Assigned offense {offense_id} to {assigned_to}")
        
        # ==================== Custom Property Tools ====================
        
        elif name == "qradar_get_custom_properties":
            logger.info("Getting custom properties")
            result = qradar_client.get_custom_properties()
            return format_response(result, message=f"Retrieved {len(result)} custom properties")
        
        elif name == "qradar_get_custom_property_by_id":
            property_id = arguments.get("property_id")
            
            logger.info(f"Getting custom property {property_id}")
            result = qradar_client.get_custom_property_by_id(property_id)
            return format_response(result, message=f"Retrieved custom property {property_id}")
        
        # ==================== Domain Management Tools ====================
        
        elif name == "qradar_get_domains":
            logger.info("Getting domains")
            result = qradar_client.get_domains()
            return format_response(result, message=f"Retrieved {len(result)} domains")
        
        elif name == "qradar_get_domain_by_id":
            domain_id = arguments.get("domain_id")
            
            logger.info(f"Getting domain {domain_id}")
            result = qradar_client.get_domain_by_id(domain_id)
            return format_response(result, message=f"Retrieved domain {domain_id}")
        
        # ==================== Network Hierarchy Tools ====================
        
        elif name == "qradar_get_network_hierarchy":
            logger.info("Getting network hierarchy")
            result = qradar_client.get_network_hierarchy()
            return format_response(result, message=f"Retrieved {len(result)} network objects")
        
        # ==================== Ariel Database Tools ====================
        
        elif name == "qradar_get_ariel_databases":
            logger.info("Getting Ariel databases")
            result = qradar_client.get_ariel_databases()
            return format_response(result, message=f"Retrieved {len(result)} databases")
        
        elif name == "qradar_get_ariel_fields":
            database_name = arguments.get("database_name", "events")
            
            logger.info(f"Getting Ariel fields for {database_name}")
            result = qradar_client.get_ariel_fields(database_name)
            return format_response(result, message=f"Retrieved {len(result)} fields for {database_name}")
        
        # ==================== Event Category Tools ====================
        
        elif name == "qradar_get_event_categories":
            logger.info("Getting event categories")
            result = qradar_client.get_event_categories()
            return format_response(result, message=f"Retrieved {len(result)} event categories")
        
        elif name == "qradar_search_event_categories":
            search_term = arguments.get("search_term")
            
            logger.info(f"Searching event categories for: {search_term}")
            result = qradar_client.search_event_categories(search_term)
            return format_response(result, message=f"Found {len(result)} matching categories")
        
        # ==================== Building Block Tools ====================
        
        elif name == "qradar_get_building_blocks":
            filter_query = arguments.get("filter")
            
            logger.info("Getting building blocks")
            result = qradar_client.get_building_blocks(filter_query)
            return format_response(result, message=f"Retrieved {len(result)} building blocks")
        
        elif name == "qradar_get_building_block_by_id":
            block_id = arguments.get("block_id")
            
            logger.info(f"Getting building block {block_id}")
            result = qradar_client.get_building_block_by_id(block_id)
            return format_response(result, message=f"Retrieved building block {block_id}")
        
        # ==================== User Management Tools ====================
        
        elif name == "qradar_get_users":
            logger.info("Getting users")
            result = qradar_client.get_users()
            return format_response(result, message=f"Retrieved {len(result)} users")
        
        elif name == "qradar_get_user_by_id":
            user_id = arguments.get("user_id")
            
            logger.info(f"Getting user {user_id}")
            result = qradar_client.get_user_by_id(user_id)
            return format_response(result, message=f"Retrieved user {user_id}")
        
        # ==================== Reports Tools ====================
        
        elif name == "qradar_get_reports":
            logger.info("Getting reports")
            result = qradar_client.get_reports()
            return format_response(result, message=f"Retrieved {len(result)} reports")
        
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        return format_response(
            {"error": str(e)},
            success=False,
            message=f"Error executing {name}: {str(e)}"
        )


async def main():
    """Main entry point for the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        logger.info("IBM QRadar MCP Server starting...")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

