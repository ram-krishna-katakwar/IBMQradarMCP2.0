"""IBM QRadar API Client

Author: Ram Krishna Katakwar
Version: 0.2.0
License: MIT
"""
import json
import time
from typing import Dict, List, Optional, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class QRadarClient:
    """Client for interacting with IBM QRadar REST API"""

    def __init__(self, host: str, api_token: str, verify_ssl: bool = True):
        """
        Initialize QRadar client
        
        Args:
            host: QRadar console hostname or IP
            api_token: API authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self.host = host.rstrip('/')
        self.api_token = api_token
        self.verify_ssl = verify_ssl
        self.base_url = f"https://{self.host}/api"
        
        # Configure session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            "SEC": api_token,
            "Version": "15.0",  # QRadar API version
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to QRadar API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Form data
            json_data: JSON data
            
        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                verify=self.verify_ssl,
                timeout=30
            )
            response.raise_for_status()
            
            # Handle empty responses
            if not response.content:
                return {}
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            error_msg = f"QRadar API request failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_details = e.response.json()
                    error_msg += f" - {json.dumps(error_details)}"
                except:
                    error_msg += f" - {e.response.text}"
            raise Exception(error_msg)

    # ==================== Event and Log Queries ====================
    
    def search_events(
        self, 
        query: str, 
        timeout: int = 60,
        max_wait: int = 300
    ) -> Dict[str, Any]:
        """
        Search events using AQL (Ariel Query Language)
        
        Args:
            query: AQL query string
            timeout: Query timeout in seconds
            max_wait: Maximum time to wait for results
            
        Returns:
            Search results
        """
        # Step 1: Create search
        search_data = {
            "query_expression": query
        }
        
        search_response = self._make_request(
            "POST",
            "/ariel/searches",
            params={"query_expression": query}
        )
        
        search_id = search_response.get("search_id")
        if not search_id:
            raise Exception("Failed to create search - no search_id returned")
        
        # Step 2: Wait for search to complete
        start_time = time.time()
        while True:
            if time.time() - start_time > max_wait:
                raise Exception(f"Search timed out after {max_wait} seconds")
            
            status_response = self._make_request(
                "GET",
                f"/ariel/searches/{search_id}"
            )
            
            status = status_response.get("status")
            
            if status == "COMPLETED":
                break
            elif status == "ERROR":
                raise Exception(f"Search failed: {status_response.get('error_messages', [])}")
            elif status in ["CANCELED", "CANCELLED"]:
                raise Exception("Search was canceled")
            
            time.sleep(2)  # Poll every 2 seconds
        
        # Step 3: Retrieve results
        results_response = self._make_request(
            "GET",
            f"/ariel/searches/{search_id}/results"
        )
        
        return {
            "search_id": search_id,
            "status": status,
            "events": results_response.get("events", []),
            "record_count": len(results_response.get("events", []))
        }

    def get_recent_events(
        self, 
        limit: int = 50,
        fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get recent events from QRadar
        
        Args:
            limit: Maximum number of events to return
            fields: List of fields to return
            
        Returns:
            Recent events
        """
        # Build AQL query
        field_list = ", ".join(fields) if fields else "*"
        query = f"SELECT {field_list} FROM events ORDER BY starttime DESC LIMIT {limit}"
        
        return self.search_events(query)

    def search_flows(
        self, 
        query: str,
        timeout: int = 60,
        max_wait: int = 300
    ) -> Dict[str, Any]:
        """
        Search network flows using AQL
        
        Args:
            query: AQL query string
            timeout: Query timeout in seconds
            max_wait: Maximum time to wait for results
            
        Returns:
            Search results
        """
        # Similar to search_events but for flows
        search_response = self._make_request(
            "POST",
            "/ariel/searches",
            params={"query_expression": query}
        )
        
        search_id = search_response.get("search_id")
        if not search_id:
            raise Exception("Failed to create flow search - no search_id returned")
        
        # Wait for completion
        start_time = time.time()
        while True:
            if time.time() - start_time > max_wait:
                raise Exception(f"Flow search timed out after {max_wait} seconds")
            
            status_response = self._make_request(
                "GET",
                f"/ariel/searches/{search_id}"
            )
            
            status = status_response.get("status")
            
            if status == "COMPLETED":
                break
            elif status == "ERROR":
                raise Exception(f"Flow search failed: {status_response.get('error_messages', [])}")
            elif status in ["CANCELED", "CANCELLED"]:
                raise Exception("Flow search was canceled")
            
            time.sleep(2)
        
        # Retrieve results
        results_response = self._make_request(
            "GET",
            f"/ariel/searches/{search_id}/results"
        )
        
        return {
            "search_id": search_id,
            "status": status,
            "flows": results_response.get("flows", []),
            "record_count": len(results_response.get("flows", []))
        }

    # ==================== Offenses ====================
    
    def get_offenses(
        self,
        filter_query: Optional[str] = None,
        fields: Optional[str] = None,
        range_header: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get offenses from QRadar
        
        Args:
            filter_query: Filter string (e.g., "status=OPEN")
            fields: Comma-separated list of fields to return
            range_header: Range of results to return (e.g., "0-49")
            
        Returns:
            List of offenses
        """
        params = {}
        if filter_query:
            params["filter"] = filter_query
        if fields:
            params["fields"] = fields
        
        headers = {}
        if range_header:
            headers["Range"] = f"items={range_header}"
        
        # Temporarily add range header if provided
        if headers:
            original_headers = self.session.headers.copy()
            self.session.headers.update(headers)
        
        try:
            offenses = self._make_request("GET", "/siem/offenses", params=params)
            return offenses if isinstance(offenses, list) else [offenses]
        finally:
            if headers:
                self.session.headers = original_headers

    def get_offense_by_id(self, offense_id: int) -> Dict[str, Any]:
        """
        Get specific offense by ID
        
        Args:
            offense_id: Offense ID
            
        Returns:
            Offense details
        """
        return self._make_request("GET", f"/siem/offenses/{offense_id}")

    # ==================== Log Sources (Agents) ====================
    
    def get_log_sources(
        self,
        filter_query: Optional[str] = None,
        fields: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get log sources (agents) from QRadar
        
        Args:
            filter_query: Filter string
            fields: Comma-separated list of fields to return
            
        Returns:
            List of log sources
        """
        params = {}
        if filter_query:
            params["filter"] = filter_query
        if fields:
            params["fields"] = fields
        
        log_sources = self._make_request("GET", "/config/event_sources/log_source_management/log_sources", params=params)
        return log_sources if isinstance(log_sources, list) else [log_sources]

    def get_log_source_by_id(self, log_source_id: int) -> Dict[str, Any]:
        """
        Get specific log source by ID
        
        Args:
            log_source_id: Log source ID
            
        Returns:
            Log source details
        """
        return self._make_request(
            "GET", 
            f"/config/event_sources/log_source_management/log_sources/{log_source_id}"
        )

    def get_log_source_types(self) -> List[Dict[str, Any]]:
        """
        Get available log source types
        
        Returns:
            List of log source types
        """
        types = self._make_request("GET", "/config/event_sources/log_source_management/log_source_types")
        return types if isinstance(types, list) else [types]

    # ==================== Assets ====================
    
    def get_assets(
        self,
        filter_query: Optional[str] = None,
        fields: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get assets from QRadar
        
        Args:
            filter_query: Filter string
            fields: Comma-separated list of fields to return
            
        Returns:
            List of assets
        """
        params = {}
        if filter_query:
            params["filter"] = filter_query
        if fields:
            params["fields"] = fields
        
        assets = self._make_request("GET", "/asset_model/assets", params=params)
        return assets if isinstance(assets, list) else [assets]

    def search_assets(self, ip_address: str) -> List[Dict[str, Any]]:
        """
        Search for assets by IP address
        
        Args:
            ip_address: IP address to search for
            
        Returns:
            List of matching assets
        """
        filter_query = f"interfaces contains ip_addresses contains value='{ip_address}'"
        return self.get_assets(filter_query=filter_query)

    # ==================== Reference Data ====================
    
    def get_reference_sets(self) -> List[Dict[str, Any]]:
        """
        Get reference data sets
        
        Returns:
            List of reference sets
        """
        ref_sets = self._make_request("GET", "/reference_data/sets")
        return ref_sets if isinstance(ref_sets, list) else [ref_sets]

    def get_reference_set_data(self, ref_set_name: str) -> Dict[str, Any]:
        """
        Get data from a specific reference set
        
        Args:
            ref_set_name: Name of the reference set
            
        Returns:
            Reference set data
        """
        return self._make_request("GET", f"/reference_data/sets/{ref_set_name}")

    # ==================== System Information ====================
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get QRadar system information
        
        Returns:
            System information
        """
        return self._make_request("GET", "/system/about")

    def get_servers(self) -> List[Dict[str, Any]]:
        """
        Get QRadar servers/hosts
        
        Returns:
            List of servers
        """
        servers = self._make_request("GET", "/system/servers")
        return servers if isinstance(servers, list) else [servers]

    # ==================== Rules ====================
    
    def get_rules(
        self,
        filter_query: Optional[str] = None,
        fields: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get rules from QRadar
        
        Args:
            filter_query: Filter string
            fields: Comma-separated list of fields to return
            
        Returns:
            List of rules
        """
        params = {}
        if filter_query:
            params["filter"] = filter_query
        if fields:
            params["fields"] = fields
        
        rules = self._make_request("GET", "/analytics/rules", params=params)
        return rules if isinstance(rules, list) else [rules]

    def get_rule_by_id(self, rule_id: int) -> Dict[str, Any]:
        """
        Get specific rule by ID
        
        Args:
            rule_id: Rule ID
            
        Returns:
            Rule details
        """
        return self._make_request("GET", f"/analytics/rules/{rule_id}")

    # ==================== Saved Searches ====================
    
    def get_saved_searches(self) -> List[Dict[str, Any]]:
        """
        Get all saved Ariel searches
        
        Returns:
            List of saved searches
        """
        searches = self._make_request("GET", "/ariel/saved_searches")
        return searches if isinstance(searches, list) else [searches]
    
    def get_saved_search_by_id(self, search_id: str) -> Dict[str, Any]:
        """
        Get specific saved search by ID
        
        Args:
            search_id: Saved search ID
            
        Returns:
            Saved search details
        """
        return self._make_request("GET", f"/ariel/saved_searches/{search_id}")
    
    def execute_saved_search(
        self, 
        search_id: str,
        max_wait: int = 300
    ) -> Dict[str, Any]:
        """
        Execute a saved search
        
        Args:
            search_id: Saved search ID
            max_wait: Maximum time to wait for results
            
        Returns:
            Search results
        """
        # Get saved search details to get the query
        saved_search = self.get_saved_search_by_id(search_id)
        query = saved_search.get("aql")
        
        if not query:
            raise Exception(f"Saved search {search_id} does not have an AQL query")
        
        # Execute the query
        return self.search_events(query, max_wait=max_wait)

    # ==================== Offense Notes ====================
    
    def get_offense_notes(self, offense_id: int) -> List[Dict[str, Any]]:
        """
        Get notes for a specific offense
        
        Args:
            offense_id: Offense ID
            
        Returns:
            List of offense notes
        """
        notes = self._make_request("GET", f"/siem/offenses/{offense_id}/notes")
        return notes if isinstance(notes, list) else [notes]
    
    def add_offense_note(self, offense_id: int, note_text: str) -> Dict[str, Any]:
        """
        Add a note to an offense
        
        Args:
            offense_id: Offense ID
            note_text: Note text to add
            
        Returns:
            Created note details
        """
        return self._make_request(
            "POST",
            f"/siem/offenses/{offense_id}/notes",
            params={"note_text": note_text}
        )
    
    def update_offense_status(
        self, 
        offense_id: int, 
        status: str,
        closing_reason_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Update offense status
        
        Args:
            offense_id: Offense ID
            status: New status (OPEN, HIDDEN, CLOSED)
            closing_reason_id: Required if status is CLOSED
            
        Returns:
            Updated offense details
        """
        params = {"status": status}
        if closing_reason_id is not None:
            params["closing_reason_id"] = closing_reason_id
        
        return self._make_request(
            "POST",
            f"/siem/offenses/{offense_id}",
            params=params
        )
    
    def get_closing_reasons(self) -> List[Dict[str, Any]]:
        """
        Get available offense closing reasons
        
        Returns:
            List of closing reasons
        """
        reasons = self._make_request("GET", "/siem/offense_closing_reasons")
        return reasons if isinstance(reasons, list) else [reasons]
    
    def assign_offense(self, offense_id: int, assigned_to: str) -> Dict[str, Any]:
        """
        Assign an offense to a user
        
        Args:
            offense_id: Offense ID
            assigned_to: Username to assign to
            
        Returns:
            Updated offense details
        """
        return self._make_request(
            "POST",
            f"/siem/offenses/{offense_id}",
            params={"assigned_to": assigned_to}
        )

    # ==================== Custom Properties ====================
    
    def get_custom_properties(self) -> List[Dict[str, Any]]:
        """
        Get all custom properties (event, flow, and offense properties)
        
        Returns:
            List of custom properties
        """
        # Get event properties
        event_props = self._make_request("GET", "/config/event_sources/custom_properties/property_expressions")
        return event_props if isinstance(event_props, list) else [event_props]
    
    def get_custom_property_by_id(self, property_id: int) -> Dict[str, Any]:
        """
        Get specific custom property by ID
        
        Args:
            property_id: Custom property ID
            
        Returns:
            Custom property details
        """
        return self._make_request(
            "GET",
            f"/config/event_sources/custom_properties/property_expressions/{property_id}"
        )

    # ==================== Domains ====================
    
    def get_domains(self) -> List[Dict[str, Any]]:
        """
        Get all domains (for multi-tenancy)
        
        Returns:
            List of domains
        """
        domains = self._make_request("GET", "/config/domain_management/domains")
        return domains if isinstance(domains, list) else [domains]
    
    def get_domain_by_id(self, domain_id: int) -> Dict[str, Any]:
        """
        Get specific domain by ID
        
        Args:
            domain_id: Domain ID
            
        Returns:
            Domain details
        """
        return self._make_request("GET", f"/config/domain_management/domains/{domain_id}")

    # ==================== Network Hierarchy ====================
    
    def get_network_hierarchy(self) -> List[Dict[str, Any]]:
        """
        Get network hierarchy (network objects/groups)
        
        Returns:
            List of network objects
        """
        networks = self._make_request("GET", "/config/network_hierarchy/networks")
        return networks if isinstance(networks, list) else [networks]

    # ==================== Search Filters ====================
    
    def get_ariel_databases(self) -> List[Dict[str, Any]]:
        """
        Get available Ariel databases
        
        Returns:
            List of databases (events, flows)
        """
        databases = self._make_request("GET", "/ariel/databases")
        return databases if isinstance(databases, list) else [databases]
    
    def get_ariel_fields(self, database_name: str = "events") -> List[Dict[str, Any]]:
        """
        Get available fields for Ariel queries
        
        Args:
            database_name: Database name (events or flows)
            
        Returns:
            List of available fields
        """
        fields = self._make_request("GET", f"/ariel/databases/{database_name}/fields")
        return fields if isinstance(fields, list) else [fields]

    # ==================== Event and Flow Categories ====================
    
    def get_event_categories(self) -> List[Dict[str, Any]]:
        """
        Get all event categories
        
        Returns:
            List of event categories
        """
        categories = self._make_request("GET", "/data_classification/qid_records")
        return categories if isinstance(categories, list) else [categories]
    
    def search_event_categories(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search event categories by name
        
        Args:
            search_term: Term to search for in category names
            
        Returns:
            Matching categories
        """
        categories = self.get_event_categories()
        search_lower = search_term.lower()
        return [
            cat for cat in categories 
            if search_lower in cat.get("name", "").lower()
        ]

    # ==================== Building Blocks ====================
    
    def get_building_blocks(
        self,
        filter_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get building blocks (rule building blocks)
        
        Args:
            filter_query: Filter string
            
        Returns:
            List of building blocks
        """
        params = {}
        if filter_query:
            params["filter"] = filter_query
        
        blocks = self._make_request("GET", "/analytics/building_blocks", params=params)
        return blocks if isinstance(blocks, list) else [blocks]
    
    def get_building_block_by_id(self, block_id: int) -> Dict[str, Any]:
        """
        Get specific building block by ID
        
        Args:
            block_id: Building block ID
            
        Returns:
            Building block details
        """
        return self._make_request("GET", f"/analytics/building_blocks/{block_id}")

    # ==================== User Management ====================
    
    def get_users(self) -> List[Dict[str, Any]]:
        """
        Get all QRadar users
        
        Returns:
            List of users
        """
        users = self._make_request("GET", "/config/access/users")
        return users if isinstance(users, list) else [users]
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """
        Get specific user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User details
        """
        return self._make_request("GET", f"/config/access/users/{user_id}")

    # ==================== Reports ====================
    
    def get_reports(self) -> List[Dict[str, Any]]:
        """
        Get all reports
        
        Returns:
            List of reports
        """
        reports = self._make_request("GET", "/gui_app_framework/applications")
        return reports if isinstance(reports, list) else [reports]

