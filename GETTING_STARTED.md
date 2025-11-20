# 🚀 Getting Started with IBM QRadar MCP

## Complete Step-by-Step Deployment Guide

This guide will take you from zero to fully operational in **under 15 minutes**.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Choose Your Interface](#choose-your-interface)
5. [First Steps](#first-steps)
6. [Common Tasks](#common-tasks)
7. [Troubleshooting](#troubleshooting)

---

## 1️⃣ Prerequisites

### System Requirements

- **Operating System**: macOS, Linux, or Windows with WSL
- **Python**: 3.10 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 20GB free space
- **Network**: Access to IBM QRadar instance

### Before You Begin

Check if you have Python 3.10+:
```bash
python3 --version
# Should show: Python 3.10.x or higher
```

---

## 2️⃣ Installation

### Step A: Install Project Dependencies

```bash
# Navigate to project directory
cd /Users/I0986/Code/MCPs/IBMQradarMCP2

# Install Python dependencies
pip3 install -r requirements.txt

# Verify installation
python3 -c "import mcp, requests, flask; print('✅ All dependencies installed')"
```

### Step B: Install Ollama (For Local LLM)

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from [ollama.com/download](https://ollama.com/download)

**Verify Ollama:**
```bash
ollama --version
# Should show: ollama version x.x.x
```

### Step C: Download an LLM Model

```bash
# Start Ollama service
ollama serve &

# Download recommended model (this may take a few minutes)
ollama pull llama3.1:8b

# Verify model is downloaded
ollama list
# Should show: llama3.1:8b
```

**Other recommended models:**
```bash
# For best quality (requires 16GB RAM)
ollama pull qwen2.5:14b

# For fastest responses (requires 8GB RAM)
ollama pull mistral:7b

# For technical/code tasks (requires 8GB RAM)
ollama pull deepseek-coder:6.7b
```

---

## 3️⃣ Configuration

### Step A: Get QRadar API Token

1. **Log into IBM QRadar Console**
   - Open your browser
   - Navigate to your QRadar instance
   - Log in with your credentials

2. **Create Authorized Service**
   - Go to: **Admin** → **Authorized Services**
   - Click: **Create Authorized Service**
   - Enter a name: `MCP Server`

3. **Select Permissions** (recommended):
   - ✅ Ariel (for event queries)
   - ✅ Offenses (read/write for offense management)
   - ✅ Assets (for asset queries)
   - ✅ Log Sources (for log source monitoring)
   - ✅ Rules (for analytics)
   - ✅ System (for system information)
   - ✅ Reference Data (for threat intel)

4. **Generate and Copy Token**
   - Click **Create**
   - **Copy the token** (you won't see it again!)

### Step B: Create Configuration File

```bash
# Create .env file
cat > .env << 'EOF'
QRADAR_HOST=your-qradar-host.com
QRADAR_API_TOKEN=your-api-token-here
QRADAR_VERIFY_SSL=true
EOF
```

**Replace with your values:**
- `your-qradar-host.com` → Your QRadar hostname (no https://)
- `your-api-token-here` → The token you just copied

**Example:**
```bash
QRADAR_HOST=qradar.company.com
QRADAR_API_TOKEN=a1b2c3d4-e5f6-7890-abcd-ef1234567890
QRADAR_VERIFY_SSL=true
```

### Step C: Test Connection

```bash
# Run connection test
python3 test_connection.py
```

**Expected output:**
```
✅ Successfully connected to QRadar!
✅ Log sources accessible - Found X log source(s)
✅ Offenses accessible - Found X offense(s)
✅ Connection test completed!
```

**If you see errors**, check [Troubleshooting](#troubleshooting) section.

---

## 4️⃣ Choose Your Interface

You have **3 options** for using QRadar MCP with local LLMs:

### 🌟 Option 1: Web UI (Recommended for Daily Use)

**Best for:** Security analysts, daily operations, team use

**Start the Web UI:**
```bash
./start_webui.sh
```

**Then open your browser to:**
```
http://localhost:5000
```

**Features:**
- ✅ Beautiful modern interface
- ✅ Real-time chat
- ✅ Rich formatting (tables, code, markdown)
- ✅ Example queries
- ✅ Tool reference
- ✅ Model switching

---

### 💻 Option 2: Terminal Client (For Automation)

**Best for:** Scripts, automation, command-line users

**Start the terminal client:**
```bash
python3 local_llm_client.py
```

**Features:**
- ✅ Lightweight
- ✅ Fast startup
- ✅ Good for scripting
- ✅ Low resource usage

**Single query mode:**
```bash
python3 local_llm_client.py --query "Show me all open offenses"
```

---

### 🔧 Option 3: VS Code Integration (For Developers)

**Best for:** Developers, VS Code users

**Setup:**

1. **Install Continue.dev extension** in VS Code
   - Open VS Code
   - Go to Extensions (Cmd/Ctrl + Shift + X)
   - Search for "Continue"
   - Click Install

2. **Configure MCP Server**
   
   Create/edit `~/.continue/config.json`:
   ```json
   {
     "models": [
       {
         "title": "Ollama Llama 3.1",
         "provider": "ollama",
         "model": "llama3.1:8b"
       }
     ],
     "mcpServers": {
       "qradar": {
         "command": "python3",
         "args": ["-m", "src.server"],
         "cwd": "/Users/I0986/Code/MCPs/IBMQradarMCP2",
         "env": {
           "QRADAR_HOST": "your-qradar-host.com",
           "QRADAR_API_TOKEN": "your-token",
           "QRADAR_VERIFY_SSL": "true"
         }
       }
     }
   }
   ```

3. **Start chatting**
   - Press `Cmd+L` (Mac) or `Ctrl+L` (Windows/Linux)
   - Ask: "Show me all open offenses in QRadar"

---

### 🎨 Option 4: Claude Desktop (Cloud Alternative)

**Best for:** Users who prefer Claude and don't need local LLMs

**Setup:**

1. **Find Claude Desktop config file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. **Add this configuration:**
   ```json
   {
     "mcpServers": {
       "qradar": {
         "command": "python3",
         "args": ["-m", "src.server"],
         "cwd": "/Users/I0986/Code/MCPs/IBMQradarMCP2",
         "env": {
           "QRADAR_HOST": "your-qradar-host.com",
           "QRADAR_API_TOKEN": "your-token",
           "QRADAR_VERIFY_SSL": "true"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop**
   - Fully quit Claude Desktop
   - Restart it
   - Look for 🔌 tool icon to confirm MCP is connected

---

## 5️⃣ First Steps

### Using the Web UI

**1. Start the Web UI:**
```bash
./start_webui.sh
```

**2. Open browser:** http://localhost:5000

**3. Try these example queries:**

**Basic Queries:**
```
Show me all open offenses
Get recent security events
List all log sources
```

**Investigation:**
```
Search for failed login attempts in the last 24 hours
Get details for offense 42
Find asset with IP 192.168.1.100
What are the most recent high severity events?
```

**Discovery:**
```
What fields are available for events queries?
Search event categories for 'authentication'
Show me all saved searches
List all QRadar users
```

**Management:**
```
Show notes for offense 156
Add note to offense 156: "Investigating suspicious activity"
Assign offense 156 to analyst_john
What closing reasons are available?
```

---

### Using the Terminal Client

**1. Start the client:**
```bash
python3 local_llm_client.py
```

**2. At the prompt, type:**
```
Show me all open offenses
```

**3. Try other commands:**
```
help              # Show available tools
clear             # Clear conversation history
exit              # Exit the client
```

**4. Single-shot query:**
```bash
python3 local_llm_client.py --query "Show me high severity offenses"
```

---

## 6️⃣ Common Tasks

### Task 1: Investigate a Security Incident

**Complete workflow:**
```bash
# 1. Start Web UI
./start_webui.sh

# 2. In browser, follow these steps:
```

**In the chat:**
```
1. "Show me all open high severity offenses"
2. "Get details for offense 234" (pick one from results)
3. "Show notes for offense 234"
4. "Search events: SELECT * FROM events WHERE sourceip='10.0.1.50' LAST 24 HOURS"
5. "Find asset with IP 10.0.1.50"
6. "Add note to offense 234: 'Confirmed unauthorized access from IP 10.0.1.50'"
7. "Assign offense 234 to analyst_mike"
8. "What closing reasons are available?"
9. "Close offense 234 with closing reason 1"
```

### Task 2: Daily Security Review

```
1. "Show me all open offenses"
2. "Get recent security events in the last hour"
3. "Show me all log sources" (check for disconnected sources)
4. "Execute saved search 'Daily_Compliance_Check'" (if you have saved searches)
```

### Task 3: Threat Hunting

```
1. "What fields are available for events queries?"
2. "Search event categories for 'malware'"
3. "Search events: SELECT sourceip, destinationip, qidname FROM events WHERE category=12 LAST 48 HOURS"
4. "For each suspicious IP, find asset details"
5. "Check reference sets for known threats"
```

### Task 4: Building Custom AQL Queries

```
1. "What fields are available for events queries?"
   (Note the available fields)

2. "Search event categories for 'authentication'"
   (Get the category ID, e.g., 1003)

3. Build your query:
   "Search events: SELECT sourceip, username, eventcount 
    FROM events 
    WHERE category=1003 
    LAST 24 HOURS"

4. Refine based on results
```

---

## 7️⃣ Troubleshooting

### Issue: "Cannot connect to Ollama"

**Symptoms:**
- Web UI shows "Ollama: Offline"
- Terminal client says "Cannot connect to Ollama"

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve

# In another terminal, verify
ollama list
```

---

### Issue: "No models available"

**Symptoms:**
- Model dropdown is empty
- Error: "Model not found"

**Solution:**
```bash
# Download a model
ollama pull llama3.1:8b

# Verify it's downloaded
ollama list

# Should show:
# NAME            SIZE
# llama3.1:8b    4.7GB
```

---

### Issue: "QRadar connection failed"

**Symptoms:**
- "401 Unauthorized"
- "Cannot connect to QRadar"
- "Connection refused"

**Solution:**

**1. Check .env file:**
```bash
cat .env
# Verify QRADAR_HOST and QRADAR_API_TOKEN are correct
```

**2. Test connection:**
```bash
python3 test_connection.py
```

**3. Verify network access:**
```bash
# Can you reach QRadar?
ping your-qradar-host.com

# Test API endpoint
curl -k https://your-qradar-host.com/api/system/about
```

**4. Check API token:**
- Log into QRadar Console
- Go to Admin → Authorized Services
- Verify your service is enabled
- Regenerate token if needed

---

### Issue: "Permission denied" errors

**Symptoms:**
- "403 Forbidden"
- "Insufficient capabilities"

**Solution:**

Your API token needs more permissions. In QRadar:

1. Go to **Admin** → **Authorized Services**
2. Find your MCP service
3. Click **Edit**
4. Add required permissions:
   - ✅ Ariel
   - ✅ Offenses (Read/Write)
   - ✅ Assets
   - ✅ Log Sources
   - ✅ Rules
   - ✅ System
   - ✅ Reference Data
5. Click **Save**
6. Restart your MCP client

---

### Issue: "Flask not installed"

**Symptoms:**
- `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip3 install flask markdown requests

# Or install all dependencies
pip3 install -r requirements.txt
```

---

### Issue: "Port 5000 already in use"

**Symptoms:**
- "Address already in use"
- Web UI won't start

**Solution:**

**Option 1: Find and stop the process:**
```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process (replace PID)
kill -9 PID
```

**Option 2: Use a different port:**
```python
# Edit web_ui.py, change:
app.run(host='0.0.0.0', port=8080)
```

Then access at http://localhost:8080

---

### Issue: "Slow responses"

**Symptoms:**
- Takes > 30 seconds to respond
- System feels sluggish

**Solutions:**

**1. Use a smaller/faster model:**
```bash
ollama pull mistral:7b
# Then select it in the Web UI dropdown
```

**2. Close other applications:**
- Free up RAM
- Close unnecessary browser tabs

**3. Enable GPU (if available):**
- Ollama automatically uses GPU if detected
- Check: `nvidia-smi` (for NVIDIA GPUs)

**4. Reduce context window:**
Edit `web_ui.py`:
```python
"options": {
    "num_ctx": 2048  # Reduce from 4096
}
```

---

### Issue: "SSL Certificate Error"

**Symptoms:**
- "SSL verification failed"
- Certificate errors

**Solution:**

**For development/testing:**
```bash
# Edit .env file
QRADAR_VERIFY_SSL=false
```

**For production:**
```bash
# Add QRadar certificate to trusted store
# Or keep SSL verification enabled
QRADAR_VERIFY_SSL=true
```

---

## 8️⃣ Quick Reference

### Starting Services

```bash
# Start Ollama (if not running)
ollama serve &

# Start Web UI
./start_webui.sh

# Start Terminal Client
python3 local_llm_client.py

# Run single query
python3 local_llm_client.py --query "your query"

# Test QRadar connection
python3 test_connection.py
```

### Useful Commands

```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# List installed models
ollama list

# Download a model
ollama pull model-name

# Check Python dependencies
pip3 list | grep -E "mcp|flask|requests"

# View logs (terminal client)
python3 local_llm_client.py 2>&1 | tee client.log
```

### Configuration Files

```
.env                           # QRadar credentials
requirements.txt               # Python dependencies
web_ui.py                      # Web UI server
local_llm_client.py           # Terminal client
~/.continue/config.json       # Continue.dev config
~/Library/.../claude_desktop_config.json  # Claude config
```

---

## 9️⃣ Next Steps

### Learn More

1. **Explore Documentation:**
   - `README.md` - Main overview
   - `ADVANCED_FEATURES.md` - All 41 tools
   - `WEB_UI_GUIDE.md` - Web UI details
   - `LOCAL_LLM_GUIDE.md` - Local LLM setup
   - `QUICK_REFERENCE.md` - Command reference

2. **Try Example Workflows:**
   - See `examples/example_queries.md`
   - Click examples in Web UI sidebar

3. **Customize:**
   - Modify Web UI theme
   - Add custom examples
   - Create saved searches

### Get Help

**Documentation:**
- Check `TROUBLESHOOTING.md` for solutions
- Read tool-specific docs in `ADVANCED_FEATURES.md`

**Testing:**
```bash
python3 test_connection.py  # Verify QRadar connection
```

**Community:**
- Report issues
- Request features
- Share use cases

---

## 🎉 Congratulations!

You now have a **fully functional IBM QRadar MCP** setup with:

✅ **41 powerful tools** for security operations  
✅ **3 interface options** (Web UI, Terminal, VS Code)  
✅ **Local LLM support** for complete privacy  
✅ **Production-ready** configuration  
✅ **Comprehensive documentation**  

### Quick Health Check

Run this to verify everything is working:

```bash
# 1. Check Ollama
ollama list

# 2. Check Python dependencies
python3 -c "import mcp, flask, requests; print('✅ Dependencies OK')"

# 3. Test QRadar connection
python3 test_connection.py

# 4. Start Web UI
./start_webui.sh

# 5. Open browser to http://localhost:5000
# 6. Try: "Show me all open offenses"
```

If all steps succeed: **🎉 You're ready to go!**

---

## 📚 Quick Links

- **Web UI**: http://localhost:5000
- **Ollama API**: http://localhost:11434
- **Documentation**: See `docs/` folder
- **Examples**: See `examples/` folder

---

## 🚀 Start Using Now!

**Simplest path:**
```bash
# One command to start
./start_webui.sh

# Open browser to:
http://localhost:5000

# Start with:
"Show me all open offenses"
```

**Happy Security Operations! 🛡️**

---

**Version**: 1.0.0  
**Last Updated**: November 2024  
**Status**: ✅ Production Ready

