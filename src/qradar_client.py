"""IBM QRadar API Client"""
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

