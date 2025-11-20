#!/usr/bin/env python3
"""
Web UI for IBM QRadar MCP with Local LLM
Beautiful, modern interface for interacting with QRadar through local LLMs

Author: Ram Krishna Katakwar
Version: 1.0.0
License: MIT
"""

from flask import Flask, render_template, request, jsonify, stream_with_context, Response
import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import markdown
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# Store conversation history per session (in-memory, simple implementation)
conversations: Dict[str, List[Dict]] = {}

def get_system_prompt() -> str:
    """Get system prompt for QRadar MCP"""
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
1. Provide clear, actionable security insights
2. Suggest next investigation steps
3. Format AQL queries properly with syntax highlighting
4. Use tables for structured data
5. Highlight critical security findings

Be concise but thorough. Focus on security value. Use markdown formatting for better readability."""

def check_ollama() -> tuple[bool, str]:
    """Check if Ollama is available"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return True, f"Connected - {len(models)} models available"
        return False, "Ollama not responding"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to Ollama"
    except Exception as e:
        return False, str(e)

def get_available_models() -> List[Dict]:
    """Get list of available Ollama models"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [
                {
                    "name": m.get("name", ""),
                    "size": m.get("size", 0),
                    "modified": m.get("modified_at", "")
                }
                for m in models
            ]
    except:
        pass
    return []

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """Get system status"""
    ollama_ok, ollama_msg = check_ollama()
    models = get_available_models()
    
    return jsonify({
        "ollama": {
            "status": "online" if ollama_ok else "offline",
            "message": ollama_msg,
            "url": OLLAMA_URL
        },
        "models": models,
        "default_model": DEFAULT_MODEL,
        "tools": 41
    })

@app.route('/api/models')
def models():
    """Get available models"""
    return jsonify({
        "models": get_available_models()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat message"""
    data = request.json
    user_message = data.get('message', '').strip()
    model = data.get('model', DEFAULT_MODEL)
    session_id = data.get('session_id', 'default')
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    # Initialize conversation history for session
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add user message to history
    conversations[session_id].append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Prepare messages for Ollama
    messages = [
        {"role": "system", "content": get_system_prompt()}
    ]
    
    # Add conversation history (last 20 messages)
    for msg in conversations[session_id][-20:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    try:
        # Call Ollama API
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_ctx": 4096
                }
            },
            timeout=120
        )
        
        if response.status_code != 200:
            return jsonify({"error": f"Ollama error: {response.status_code}"}), 500
        
        result = response.json()
        assistant_message = result["message"]["content"]
        
        # Add assistant message to history
        conversations[session_id].append({
            "role": "assistant",
            "content": assistant_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            assistant_message,
            extensions=['fenced_code', 'tables', 'nl2br']
        )
        
        return jsonify({
            "message": assistant_message,
            "html": html_content,
            "timestamp": datetime.now().isoformat()
        })
        
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Handle streaming chat message"""
    data = request.json
    user_message = data.get('message', '').strip()
    model = data.get('model', DEFAULT_MODEL)
    session_id = data.get('session_id', 'default')
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    # Initialize conversation history
    if session_id not in conversations:
        conversations[session_id] = []
    
    conversations[session_id].append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    
    def generate():
        """Generate streaming response"""
        messages = [{"role": "system", "content": get_system_prompt()}]
        
        for msg in conversations[session_id][-20:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": True,
                    "options": {"temperature": 0.7, "num_ctx": 4096}
                },
                stream=True,
                timeout=120
            )
            
            full_message = ""
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "message" in chunk:
                            content = chunk["message"].get("content", "")
                            if content:
                                full_message += content
                                yield f"data: {json.dumps({'content': content})}\n\n"
                    except json.JSONDecodeError:
                        pass
            
            # Save complete message to history
            conversations[session_id].append({
                "role": "assistant",
                "content": full_message,
                "timestamp": datetime.now().isoformat()
            })
            
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/api/history/<session_id>')
def get_history(session_id):
    """Get conversation history"""
    return jsonify({
        "history": conversations.get(session_id, [])
    })

@app.route('/api/history/<session_id>', methods=['DELETE'])
def clear_history(session_id):
    """Clear conversation history"""
    if session_id in conversations:
        del conversations[session_id]
    return jsonify({"success": True})

@app.route('/api/tools')
def get_tools():
    """Get available QRadar MCP tools"""
    tools = {
        "Events & Logs": [
            {"name": "qradar_search_events", "desc": "Execute AQL queries on events"},
            {"name": "qradar_get_recent_events", "desc": "Get most recent events"},
            {"name": "qradar_search_flows", "desc": "Query network flows"}
        ],
        "Offense Management": [
            {"name": "qradar_get_offenses", "desc": "List all offenses"},
            {"name": "qradar_get_offense_by_id", "desc": "Get offense details"},
            {"name": "qradar_get_offense_notes", "desc": "View investigation notes"},
            {"name": "qradar_add_offense_note", "desc": "Add investigation note"},
            {"name": "qradar_update_offense_status", "desc": "Update/close offense"},
            {"name": "qradar_get_closing_reasons", "desc": "Get closing reasons"},
            {"name": "qradar_assign_offense", "desc": "Assign to analyst"}
        ],
        "Saved Searches": [
            {"name": "qradar_get_saved_searches", "desc": "List saved searches"},
            {"name": "qradar_get_saved_search_by_id", "desc": "Get search details"},
            {"name": "qradar_execute_saved_search", "desc": "Execute saved search"}
        ],
        "Discovery": [
            {"name": "qradar_get_ariel_fields", "desc": "Get available query fields"},
            {"name": "qradar_search_event_categories", "desc": "Search event categories"},
            {"name": "qradar_get_event_categories", "desc": "List all categories"},
            {"name": "qradar_get_ariel_databases", "desc": "List Ariel databases"}
        ],
        "Assets & Sources": [
            {"name": "qradar_get_log_sources", "desc": "List log sources"},
            {"name": "qradar_get_assets", "desc": "List assets"},
            {"name": "qradar_search_assets_by_ip", "desc": "Find asset by IP"}
        ],
        "Team & Management": [
            {"name": "qradar_get_users", "desc": "List QRadar users"},
            {"name": "qradar_get_domains", "desc": "List domains"},
            {"name": "qradar_get_system_info", "desc": "System information"}
        ]
    }
    
    return jsonify({"tools": tools})

@app.route('/api/examples')
def get_examples():
    """Get example queries"""
    examples = [
        {
            "category": "Basic Queries",
            "queries": [
                "Show me all open offenses",
                "Show me high severity offenses",
                "Get recent security events",
                "List all log sources"
            ]
        },
        {
            "category": "Investigation",
            "queries": [
                "Search for failed login attempts in the last 24 hours",
                "Show events from IP 192.168.1.100",
                "Find assets by IP address",
                "Get details for offense 42"
            ]
        },
        {
            "category": "Advanced",
            "queries": [
                "What fields are available for events queries?",
                "Search event categories for 'malware'",
                "Execute saved search 'Daily_Security_Check'",
                "Show me all QRadar users"
            ]
        },
        {
            "category": "Offense Management",
            "queries": [
                "Show notes for offense 156",
                "Add note to offense 156: 'Investigating suspicious activity'",
                "Assign offense 156 to analyst_john",
                "What closing reasons are available?"
            ]
        }
    ]
    
    return jsonify({"examples": examples})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("=" * 70)
    print("🚀 IBM QRadar MCP - Web UI")
    print("=" * 70)
    print(f"🌐 Server: http://localhost:5000")
    print(f"📡 Ollama: {OLLAMA_URL}")
    print(f"🤖 Default Model: {DEFAULT_MODEL}")
    print("=" * 70)
    print()
    
    # Check Ollama status
    ollama_ok, ollama_msg = check_ollama()
    if ollama_ok:
        print(f"✅ Ollama: {ollama_msg}")
    else:
        print(f"⚠️  Ollama: {ollama_msg}")
        print("   Make sure Ollama is running: ollama serve")
    
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

