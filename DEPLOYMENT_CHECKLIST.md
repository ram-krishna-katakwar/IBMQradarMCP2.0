# 📋 Deployment Checklist

## IBM QRadar MCP - Complete Deployment Checklist

Use this checklist to ensure proper deployment and configuration.

---

## ✅ Pre-Deployment Checklist

### System Requirements
- [ ] Python 3.10 or higher installed
- [ ] 8GB RAM minimum (16GB recommended)
- [ ] 20GB free disk space
- [ ] Network access to IBM QRadar instance
- [ ] macOS, Linux, or Windows with WSL

### Verify Python Installation
```bash
python3 --version  # Should show 3.10.x or higher
pip3 --version     # Should be available
```

---

## ✅ Installation Checklist

### 1. Install Python Dependencies
```bash
cd /Users/I0986/Code/MCPs/IBMQradarMCP2
pip3 install -r requirements.txt
```

**Verify:**
- [ ] `mcp` package installed
- [ ] `requests` package installed
- [ ] `python-dotenv` package installed
- [ ] `flask` package installed (for Web UI)
- [ ] `markdown` package installed (for Web UI)

**Test:**
```bash
python3 -c "import mcp, requests, flask, markdown; print('✅ All packages installed')"
```

### 2. Install Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from ollama.com
```

**Verify:**
- [ ] Ollama installed successfully
- [ ] Ollama version displayed: `ollama --version`

### 3. Start Ollama Service
```bash
ollama serve
```

**Verify:**
- [ ] Ollama service running
- [ ] API accessible: `curl http://localhost:11434/api/tags`

### 4. Download LLM Model
```bash
# Choose one or more:
ollama pull llama3.1:8b      # Recommended: Balanced
ollama pull qwen2.5:14b      # Best quality (16GB RAM)
ollama pull mistral:7b       # Fastest (8GB RAM)
ollama pull deepseek-coder   # Best for technical
```

**Verify:**
- [ ] At least one model downloaded
- [ ] Model listed in: `ollama list`

---

## ✅ Configuration Checklist

### 1. QRadar API Token

**In QRadar Console:**
- [ ] Logged into QRadar Console
- [ ] Navigated to Admin → Authorized Services
- [ ] Created new Authorized Service named "MCP Server"
- [ ] Selected required permissions:
  - [ ] Ariel (events/flows)
  - [ ] Offenses (read/write)
  - [ ] Assets
  - [ ] Log Sources
  - [ ] Rules
  - [ ] System
  - [ ] Reference Data
- [ ] Generated and **copied** API token

### 2. Create .env File

```bash
cat > .env << 'EOF'
QRADAR_HOST=your-qradar-host.com
QRADAR_API_TOKEN=your-token-here
QRADAR_VERIFY_SSL=true
EOF
```

**Update with your values:**
- [ ] `QRADAR_HOST` set to your QRadar hostname (no https://)
- [ ] `QRADAR_API_TOKEN` set to your API token
- [ ] `QRADAR_VERIFY_SSL` set to `true` or `false`

**Example:**
```
QRADAR_HOST=qradar.company.com
QRADAR_API_TOKEN=a1b2c3d4-e5f6-7890-abcd-ef1234567890
QRADAR_VERIFY_SSL=true
```

### 3. Test QRadar Connection

```bash
python3 test_connection.py
```

**Expected Results:**
- [ ] "✅ Successfully connected to QRadar!"
- [ ] "✅ Log sources accessible"
- [ ] "✅ Offenses accessible"
- [ ] "✅ Connection test completed!"

**If errors occur:**
- [ ] Check QRADAR_HOST is correct
- [ ] Verify QRADAR_API_TOKEN is valid
- [ ] Confirm network access to QRadar
- [ ] Verify API token has required permissions

---

## ✅ Interface Selection Checklist

### Choose Your Interface(s)

#### Option 1: Web UI (Recommended)
- [ ] Run: `./start_webui.sh`
- [ ] Web UI accessible at http://localhost:5000
- [ ] Ollama status shows "Online"
- [ ] Model selector shows available models
- [ ] Example queries visible in sidebar
- [ ] Tools reference shows 41 tools

**Test:**
- [ ] Click example: "Show me all open offenses"
- [ ] Response received successfully
- [ ] Formatting looks correct

---

#### Option 2: Terminal Client
- [ ] Run: `python3 local_llm_client.py`
- [ ] Client starts without errors
- [ ] Ollama status shows "Ready"
- [ ] Prompt appears: `👤 You:`

**Test:**
- [ ] Enter: "Show me all open offenses"
- [ ] Response received
- [ ] Try: `help` command works
- [ ] Try: `clear` command works
- [ ] Try: `exit` command works

---

#### Option 3: VS Code Integration
- [ ] Continue.dev extension installed in VS Code
- [ ] Config file created: `~/.continue/config.json`
- [ ] MCP server configured in Continue settings
- [ ] Ollama model configured

**Test:**
- [ ] Press Cmd+L (Mac) or Ctrl+L (Windows/Linux)
- [ ] Continue sidebar opens
- [ ] Ask: "Show me all open offenses"
- [ ] Response received from QRadar

---

#### Option 4: Claude Desktop
- [ ] Claude Desktop installed
- [ ] Config file found and edited
- [ ] MCP server configuration added
- [ ] Claude Desktop restarted

**Test:**
- [ ] Open Claude Desktop
- [ ] Look for 🔌 tool icon
- [ ] Ask: "Show me all open offenses from QRadar"
- [ ] Tools are used in response

---

## ✅ Functional Testing Checklist

### Basic Queries
- [ ] "Show me all open offenses" - Returns offense list
- [ ] "Get recent security events" - Returns events
- [ ] "List all log sources" - Returns log sources
- [ ] "Show me all QRadar users" - Returns users

### Event Queries
- [ ] "Search for failed login attempts in last 24 hours" - Returns results
- [ ] "What fields are available for events?" - Returns field list
- [ ] Custom AQL query executes successfully

### Offense Management
- [ ] "Get details for offense X" - Returns offense details
- [ ] "Show notes for offense X" - Returns notes
- [ ] "Add note to offense X: test note" - Note added (if permissions)
- [ ] "What closing reasons are available?" - Returns reasons

### Discovery
- [ ] "Search event categories for 'authentication'" - Returns categories
- [ ] "Show me all saved searches" - Returns searches
- [ ] "Show me all domains" - Returns domains (if multi-tenant)

### Assets & Sources
- [ ] "Find asset with IP x.x.x.x" - Returns asset
- [ ] "List all log sources" - Returns sources
- [ ] "Show log source types" - Returns types

---

## ✅ Performance Testing Checklist

### Response Time
- [ ] Simple queries respond in < 5 seconds
- [ ] Complex AQL queries respond in < 15 seconds
- [ ] Acceptable for your use case

### Resource Usage
- [ ] CPU usage acceptable
- [ ] RAM usage acceptable
- [ ] Disk space sufficient
- [ ] No memory leaks after extended use

### Stability
- [ ] No crashes after 1 hour of use
- [ ] Can handle multiple queries in sequence
- [ ] Recovers from network errors gracefully

---

## ✅ Security Checklist

### API Security
- [ ] API token stored in .env (not in code)
- [ ] .env file in .gitignore
- [ ] API token has minimal required permissions
- [ ] SSL verification enabled (QRADAR_VERIFY_SSL=true)

### Network Security
- [ ] Web UI only accessible from localhost (default)
- [ ] Or: Proper firewall rules if exposed to network
- [ ] Or: Authentication added if exposed to network

### Data Privacy
- [ ] All data stays local (if using local LLM)
- [ ] No external API calls (verified)
- [ ] Sensitive data not logged

---

## ✅ Documentation Checklist

### Available Documentation
- [ ] README.md - Main overview
- [ ] GETTING_STARTED.md - This guide
- [ ] ADVANCED_FEATURES.md - All 41 tools
- [ ] WEB_UI_GUIDE.md - Web UI documentation
- [ ] LOCAL_LLM_GUIDE.md - Local LLM setup
- [ ] QUICK_REFERENCE.md - Command reference
- [ ] TROUBLESHOOTING.md - Problem resolution
- [ ] examples/example_queries.md - Query examples

### Team Documentation (If Applicable)
- [ ] Team members know how to access
- [ ] Team members trained on basic usage
- [ ] Internal documentation created
- [ ] Support process defined

---

## ✅ Production Readiness Checklist

### For Production Use
- [ ] All tests passing
- [ ] Performance acceptable
- [ ] Security measures in place
- [ ] Monitoring configured (if needed)
- [ ] Backup/recovery plan (for configs)
- [ ] Team training completed
- [ ] Support contacts identified

### For Production Web UI
- [ ] Authentication added (recommended)
- [ ] HTTPS/SSL configured (recommended)
- [ ] Rate limiting implemented (recommended)
- [ ] Access logs enabled (recommended)
- [ ] Error reporting configured
- [ ] Health check endpoint working

---

## ✅ Maintenance Checklist

### Regular Maintenance
- [ ] Update Ollama: `brew upgrade ollama` (macOS)
- [ ] Update Python packages: `pip3 install --upgrade -r requirements.txt`
- [ ] Update LLM models: `ollama pull model-name`
- [ ] Rotate QRadar API tokens (quarterly recommended)
- [ ] Review and archive logs (if applicable)
- [ ] Check disk space usage

### Monitor
- [ ] Ollama service running
- [ ] Web UI accessible (if using)
- [ ] QRadar API token valid
- [ ] Disk space sufficient
- [ ] Performance acceptable

---

## ✅ Troubleshooting Verification

### Common Issues Resolved
- [ ] Know how to restart Ollama: `ollama serve`
- [ ] Know how to check logs
- [ ] Know how to test QRadar connection: `python3 test_connection.py`
- [ ] Know where to find documentation
- [ ] Can recover from common errors

### Documentation
- [ ] TROUBLESHOOTING.md reviewed
- [ ] Common issues documented
- [ ] Team knows where to get help

---

## ✅ Final Verification

### All Systems Go
- [ ] ✅ Python dependencies installed
- [ ] ✅ Ollama installed and running
- [ ] ✅ At least one LLM model downloaded
- [ ] ✅ QRadar API token configured
- [ ] ✅ Connection test successful
- [ ] ✅ At least one interface working
- [ ] ✅ Basic queries successful
- [ ] ✅ All tools accessible
- [ ] ✅ Documentation reviewed
- [ ] ✅ Team trained (if applicable)

### Quick Health Check
```bash
# Run this comprehensive test:

# 1. Check Ollama
ollama list

# 2. Check Python
python3 -c "import mcp, flask, requests; print('✅ Python OK')"

# 3. Test QRadar
python3 test_connection.py

# 4. Start Web UI
./start_webui.sh

# 5. Test in browser
# Open http://localhost:5000
# Try: "Show me all open offenses"
```

**If all tests pass: 🎉 Deployment Complete!**

---

## 📊 Deployment Summary

### Quick Stats
- **Total Setup Time**: 10-15 minutes
- **Python Dependencies**: 5 packages
- **LLM Model Size**: 4-15GB (model dependent)
- **Available Tools**: 41
- **Interface Options**: 4
- **Documentation Pages**: 10+

### What You Have
✅ Complete QRadar MCP server  
✅ Local LLM support (private)  
✅ Multiple interface options  
✅ 41 powerful security tools  
✅ Comprehensive documentation  
✅ Production-ready setup  

---

## 🎯 Next Steps

1. **Start using it!**
   ```bash
   ./start_webui.sh
   ```

2. **Try example workflows:**
   - Incident investigation
   - Daily security review
   - Threat hunting
   - Query building

3. **Customize:**
   - Add custom examples
   - Modify Web UI theme
   - Create saved searches in QRadar
   - Document your workflows

4. **Share with team:**
   - Train team members
   - Document internal processes
   - Set up team access (if needed)

---

## 📞 Getting Help

If you encounter issues:

1. **Check documentation:**
   - TROUBLESHOOTING.md
   - GETTING_STARTED.md
   - Relevant guide for your interface

2. **Run diagnostics:**
   ```bash
   python3 test_connection.py
   ```

3. **Verify configuration:**
   ```bash
   cat .env  # Check QRadar config
   ollama list  # Check models
   curl http://localhost:11434/api/tags  # Check Ollama
   ```

4. **Review logs:**
   - Terminal output
   - Web UI console (browser F12)
   - Ollama logs

---

## ✨ Success!

**If you've completed this checklist, you have successfully deployed IBM QRadar MCP!**

🎉 **Congratulations!** You're ready for world-class security operations with AI assistance!

---

**Checklist Version**: 1.0.0  
**Last Updated**: November 2024  
**Status**: ✅ Production Ready

