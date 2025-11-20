#!/usr/bin/env python3
"""
Local LLM Client for IBM QRadar MCP
Connects local LLMs (Ollama) to the QRadar MCP server
"""

import subprocess
import json
import sys
import os
from typing import List, Dict, Any, Optional
import requests
import asyncio

class QRadarMCPClient:
    """Client to connect local LLMs with QRadar MCP server"""
    
    def __init__(
        self, 
        ollama_model: str = "llama3.1:8b",
        ollama_url: str = "http://localhost:11434"
    ):
        """
        Initialize the MCP client
        
        Args:
            ollama_model: Name of the Ollama model to use
            ollama_url: URL of the Ollama API
        """
        self.ollama_model = ollama_model
        self.ollama_url = ollama_url
        self.ollama_api = f"{ollama_url}/api/chat"
        self.conversation_history: List[Dict[str, str]] = []
        self.mcp_process: Optional[subprocess.Popen] = None
        self.available_tools: List[Dict] = []
        
    def start_mcp_server(self) -> bool:
        """Start the QRadar MCP server"""
        try:
            print("🚀 Starting QRadar MCP server...")
            
            # Start the MCP server as subprocess
            self.mcp_process = subprocess.Popen(
                [sys.executable, "-m", "src.server"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            print("✅ MCP server started")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start MCP server: {e}")
            return False
    
    def stop_mcp_server(self):
        """Stop the MCP server"""
        if self.mcp_process:
            self.mcp_process.terminate()
            self.mcp_process.wait()
            print("🛑 MCP server stopped")
    
    def check_ollama(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            # Check Ollama is running
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code != 200:
                return False
            
            # Check if model is available
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            
            # Check if our model exists (exact match or partial)
            model_available = any(
                self.ollama_model in name or name.startswith(self.ollama_model.split(":")[0])
                for name in model_names
            )
            
            if not model_available:
                print(f"⚠️  Model '{self.ollama_model}' not found.")
                print("Available models:")
                for name in model_names:
                    print(f"  - {name}")
                print(f"\nTo download: ollama pull {self.ollama_model}")
                return False
            
            return True
            
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Ollama. Is it running?")
            print("Start Ollama with: ollama serve")
            return False
        except Exception as e:
            print(f"❌ Error checking Ollama: {e}")
            return False
    
    def call_ollama(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Call the local Ollama model
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt to set context
            
        Returns:
            Model response
        """
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        try:
            # Call Ollama API
            response = requests.post(
                self.ollama_api,
                json={
                    "model": self.ollama_model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_ctx": 4096  # Context window
                    }
                },
                timeout=120  # 2 minute timeout
            )
            
            if response.status_code != 200:
                return f"Error: Ollama API returned status {response.status_code}"
            
            result = response.json()
            assistant_message = result["message"]["content"]
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # Keep history manageable (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return assistant_message
            
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Try a simpler query or a faster model."
        except Exception as e:
            return f"Error calling Ollama: {e}"
    
    def get_system_prompt(self) -> str:
        """Get system prompt that describes QRadar MCP capabilities"""
        return """You are a security analyst assistant with access to IBM QRadar SIEM through MCP tools.

You have 41 tools available for:
- Event & log queries (AQL)
- Offense management (view, notes, status, assignment)
- Saved searches (execute pre-configured queries)
- Log source monitoring
- Asset discovery
- Reference data (threat intel)
- Rules and analytics
- System information
- Custom properties
- Domain management
- Network hierarchy
- Discovery tools (fields, categories)
- Building blocks
- User management

When users ask about QRadar:
1. Use available MCP tools to query QRadar
2. Provide clear, actionable security insights
3. Suggest next investigation steps
4. Format AQL queries properly
5. Document findings in offense notes when relevant

Be concise but thorough. Focus on security value."""
    
    def chat(self):
        """Interactive chat loop"""
        print("=" * 70)
        print("🤖 IBM QRadar MCP - Local LLM Client")
        print("=" * 70)
        print(f"📡 Model: {self.ollama_model}")
        print(f"🔧 Ollama: {self.ollama_url}")
        print()
        
        # Check Ollama
        print("Checking Ollama...")
        if not self.check_ollama():
            return
        print("✅ Ollama is ready")
        print()
        
        print("=" * 70)
        print("Commands:")
        print("  'exit' or 'quit' - Exit the chat")
        print("  'clear' - Clear conversation history")
        print("  'help' - Show available QRadar tools")
        print("=" * 70)
        print()
        
        # Get system prompt
        system_prompt = self.get_system_prompt()
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'clear':
                    self.conversation_history = []
                    print("🗑️  Conversation history cleared")
                    continue
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if not user_input:
                    continue
                
                # Show thinking indicator
                print("\n🤔 Thinking...", end="", flush=True)
                
                # Get response from Ollama
                response = self.call_ollama(user_input, system_prompt)
                
                # Clear thinking indicator
                print("\r" + " " * 20 + "\r", end="", flush=True)
                
                # Print response
                print(f"🤖 Assistant:\n{response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    def show_help(self):
        """Show available QRadar MCP tools"""
        print("\n" + "=" * 70)
        print("📚 Available QRadar MCP Tools (41 total)")
        print("=" * 70)
        
        categories = {
            "Events & Logs": [
                "qradar_search_events - Execute AQL queries on events",
                "qradar_get_recent_events - Get most recent events",
                "qradar_search_flows - Query network flows"
            ],
            "Offense Management": [
                "qradar_get_offenses - List all offenses",
                "qradar_get_offense_by_id - Get offense details",
                "qradar_get_offense_notes - View investigation notes",
                "qradar_add_offense_note - Add investigation note",
                "qradar_update_offense_status - Update/close offense",
                "qradar_get_closing_reasons - Get closing reasons",
                "qradar_assign_offense - Assign to analyst"
            ],
            "Saved Searches": [
                "qradar_get_saved_searches - List saved searches",
                "qradar_execute_saved_search - Execute saved search"
            ],
            "Discovery": [
                "qradar_get_ariel_fields - Get available query fields",
                "qradar_search_event_categories - Search categories",
                "qradar_get_custom_properties - List custom properties"
            ],
            "Assets & Sources": [
                "qradar_get_log_sources - List log sources",
                "qradar_get_assets - List assets",
                "qradar_search_assets_by_ip - Find asset by IP"
            ],
            "Team & Management": [
                "qradar_get_users - List QRadar users",
                "qradar_get_domains - List domains",
                "qradar_get_system_info - System information"
            ]
        }
        
        for category, tools in categories.items():
            print(f"\n📂 {category}:")
            for tool in tools:
                print(f"  • {tool}")
        
        print("\n" + "=" * 70)
        print("For complete documentation, see: ADVANCED_FEATURES.md")
        print("=" * 70 + "\n")
    
    def simple_query(self, query: str) -> str:
        """
        Simple one-shot query (no conversation history)
        
        Args:
            query: User query
            
        Returns:
            Model response
        """
        system_prompt = self.get_system_prompt()
        
        try:
            response = requests.post(
                self.ollama_api,
                json={
                    "model": self.ollama_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query}
                    ],
                    "stream": False
                },
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()["message"]["content"]
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Error: {e}"


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Local LLM client for IBM QRadar MCP"
    )
    parser.add_argument(
        "--model",
        default="llama3.1:8b",
        help="Ollama model to use (default: llama3.1:8b)"
    )
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434",
        help="Ollama API URL (default: http://localhost:11434)"
    )
    parser.add_argument(
        "--query",
        help="Single query to run (non-interactive)"
    )
    
    args = parser.parse_args()
    
    # Create client
    client = QRadarMCPClient(
        ollama_model=args.model,
        ollama_url=args.ollama_url
    )
    
    # Single query mode
    if args.query:
        print(f"Query: {args.query}")
        print(f"Model: {args.model}")
        print("-" * 70)
        response = client.simple_query(args.query)
        print(response)
        return
    
    # Interactive chat mode
    try:
        client.chat()
    finally:
        client.stop_mcp_server()


if __name__ == "__main__":
    main()

