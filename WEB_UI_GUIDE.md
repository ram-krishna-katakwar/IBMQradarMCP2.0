## IBM QRadar MCP - Web UI Guide

# Beautiful Web Interface for Local LLM + QRadar MCP 🎨

A modern, professional web interface for interacting with your IBM QRadar SIEM through local LLMs.

---

## 🌟 Features

### Modern UI
- ✅ **Dark theme** optimized for security operations
- ✅ **Real-time status** monitoring
- ✅ **Syntax highlighting** for code and queries
- ✅ **Markdown support** for rich formatting
- ✅ **Responsive design** works on desktop and mobile
- ✅ **Keyboard shortcuts** for efficiency

### User Experience
- ✅ **Live typing indicators**
- ✅ **Example queries** for quick start
- ✅ **Tool reference** sidebar
- ✅ **Model switching** on the fly
- ✅ **Conversation history**
- ✅ **Auto-expanding input**

### Technical Features
- ✅ **Streaming responses** (optional)
- ✅ **Session management**
- ✅ **Error handling**
- ✅ **API monitoring**
- ✅ **Markdown rendering**
- ✅ **Code formatting**

---

## 🚀 Quick Start

### One-Line Start
```bash
./start_webui.sh
```

Then open your browser to: **http://localhost:5000**

### Manual Start
```bash
# Install dependencies
pip3 install flask markdown requests

# Start the server
python3 web_ui.py
```

---

## 📋 Prerequisites

### Required
- ✅ Python 3.10+
- ✅ Flask 3.0+
- ✅ Markdown 3.5+
- ✅ Requests 2.31+
- ✅ Ollama (running locally)

### Optional
- QRadar MCP server configured (for actual QRadar queries)
- `.env` file with QRadar credentials

---

## 🎯 Installation

### Step 1: Install Dependencies
```bash
pip3 install flask markdown requests
```

Or use the complete requirements:
```bash
pip3 install -r requirements.txt
```

### Step 2: Ensure Ollama is Running
```bash
# Start Ollama in another terminal
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### Step 3: Download a Model (if not already)
```bash
# Recommended models
ollama pull llama3.1:8b      # Best balance
ollama pull qwen2.5:14b      # Best quality
ollama pull mistral:7b       # Fastest
```

### Step 4: Start the Web UI
```bash
./start_webui.sh
```

---

## 🖥️ Interface Overview

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Left Sidebar         Main Chat Area           Right Sidebar    │
│                                                                  │
│  • Status             Chat Messages             Tool Reference  │
│  • Model Select       ↓↓↓↓↓↓↓↓↓↓↓↓↓              ──────────────  │
│  • Examples           [User messages]           • Events        │
│                       [AI responses]            • Offenses      │
│                                                 • Saved Searches│
│                       ──────────────            • Discovery     │
│                       Input Box                 • Assets        │
│                       [Send]                    • Management    │
└─────────────────────────────────────────────────────────────────┘
```

### Left Sidebar

**Status Card**
- 🟢 Ollama connection status
- 🤖 Current model
- 🔧 Number of tools (41)
- 📊 Model selector dropdown

**Example Queries**
- Click any example to use it
- Organized by category
- Covers all major use cases

### Main Chat Area

**Header**
- Security Operations Chat title
- Clear Chat button
- Help button

**Messages**
- User messages (blue accent)
- Assistant responses (green accent)
- Timestamps
- Code syntax highlighting
- Table formatting
- Markdown rendering

**Input**
- Auto-expanding textarea
- Shift+Enter for new line
- Enter to send
- Real-time resize

### Right Sidebar

**Tool Reference**
- All 41 tools listed
- Organized by category
- Tool descriptions
- Quick reference while chatting

---

## 💡 Usage Examples

### Basic Queries

**1. Check open offenses**
```
Show me all open offenses
```

**2. Search for events**
```
Search for failed login attempts in the last 24 hours
```

**3. Get system info**
```
Get QRadar system information
```

### Advanced Queries

**1. Build AQL queries**
```
What fields are available for events queries?
```

Then use the response to build a query:
```
Search events: SELECT sourceip, username, eventcount FROM events WHERE category=1003 LAST 24 HOURS
```

**2. Investigate offenses**
```
Get details for offense 42
Show notes for offense 42
Search events related to offense 42
```

**3. Discovery**
```
Search event categories for 'malware'
Show me all saved searches
List all QRadar users
```

### Management Operations

**1. Add notes**
```
Add note to offense 156: "Investigated - confirmed unauthorized access attempt from 192.168.1.50"
```

**2. Assign offenses**
```
Show me all users
Assign offense 156 to analyst_john
```

**3. Close offenses**
```
What closing reasons are available?
Close offense 156 with closing reason 1
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# Ollama Configuration
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.1:8b

# Flask Configuration
export FLASK_ENV=development  # or production
export FLASK_PORT=5000

# QRadar (uses .env file)
# Create .env with:
# QRADAR_HOST=your-host.com
# QRADAR_API_TOKEN=your-token
# QRADAR_VERIFY_SSL=true
```

### Custom Port

```bash
# Edit web_ui.py, change:
app.run(host='0.0.0.0', port=5000)  # Change port here

# Or set environment variable
export FLASK_PORT=8080
```

### Different Ollama Instance

```bash
# If Ollama is on a different machine
export OLLAMA_URL=http://192.168.1.100:11434
python3 web_ui.py
```

---

## 🎨 Customization

### Theme Colors

Edit `templates/index.html` CSS variables:

```css
:root {
    --primary: #0f62fe;      /* Change primary color */
    --secondary: #24a148;    /* Change secondary color */
    --bg-primary: #161616;   /* Change background */
    /* ... */
}
```

### Add Custom Examples

Edit the examples in `web_ui.py`:

```python
examples = [
    {
        "category": "Your Category",
        "queries": [
            "Your custom query 1",
            "Your custom query 2"
        ]
    }
]
```

### Modify System Prompt

Edit `get_system_prompt()` in `web_ui.py`:

```python
def get_system_prompt() -> str:
    return """Your custom system prompt here..."""
```

---

## 🔧 Advanced Features

### Streaming Responses (Optional)

The Web UI supports streaming for real-time responses:

```javascript
// In templates/index.html, modify sendMessage() to use:
const response = await fetch('/api/chat/stream', {
    method: 'POST',
    // ... streaming implementation
});
```

### Session Management

Each browser session gets a unique ID. Conversations are isolated per session.

```javascript
const sessionId = 'session_' + Date.now();
```

### Custom API Endpoints

Add custom endpoints in `web_ui.py`:

```python
@app.route('/api/your-endpoint')
def your_endpoint():
    # Your custom logic
    return jsonify({"data": "your data"})
```

---

## 📊 Monitoring & Debugging

### Check Logs

```bash
# Web UI logs (in terminal)
python3 web_ui.py

# Ollama logs
# Check the terminal where ollama serve is running
```

### Debug Mode

```python
# In web_ui.py, the debug mode is enabled:
app.run(debug=True)  # Shows detailed errors
```

### API Testing

```bash
# Test status endpoint
curl http://localhost:5000/api/status

# Test models endpoint
curl http://localhost:5000/api/models

# Test tools endpoint
curl http://localhost:5000/api/tools
```

---

## 🔐 Security Considerations

### Production Deployment

**DO NOT use in production without**:

1. **Authentication**: Add user auth
2. **HTTPS**: Use SSL/TLS
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Sanitize inputs
5. **CORS**: Configure properly

### Basic Security Measures

```python
# Example: Add basic auth
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Implement your auth logic
    return True

@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')
```

### Network Security

```bash
# Run on localhost only (not exposed to network)
app.run(host='127.0.0.1', port=5000)

# Or with firewall rules
sudo ufw allow from 192.168.1.0/24 to any port 5000
```

---

## 🚢 Deployment Options

### Option 1: Local Development

```bash
python3 web_ui.py
# Access at http://localhost:5000
```

### Option 2: Docker Container

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "web_ui.py"]
```

Build and run:

```bash
docker build -t qradar-mcp-webui .
docker run -p 5000:5000 qradar-mcp-webui
```

### Option 3: Systemd Service

Create `/etc/systemd/system/qradar-webui.service`:

```ini
[Unit]
Description=IBM QRadar MCP Web UI
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/IBMQradarMCP2
ExecStart=/usr/bin/python3 web_ui.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable qradar-webui
sudo systemctl start qradar-webui
```

### Option 4: Production WSGI Server

Use Gunicorn:

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 web_ui:app
```

---

## 🎯 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Send message |
| **Shift + Enter** | New line in input |
| **Ctrl/Cmd + K** | Clear input (planned) |
| **Esc** | Clear input (planned) |

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to Ollama"

**Solution**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### Issue: "No models available"

**Solution**:
```bash
# Download a model
ollama pull llama3.1:8b

# Verify
ollama list
```

### Issue: "Module 'flask' not found"

**Solution**:
```bash
pip3 install flask markdown requests
```

### Issue: "Connection refused on port 5000"

**Solution**:
```bash
# Check if port is in use
lsof -i :5000

# Use different port
# Edit web_ui.py and change port
```

### Issue: "Slow responses"

**Solutions**:
1. Use a smaller model (mistral:7b)
2. Reduce context length
3. Use GPU acceleration
4. Close other applications

### Issue: "QRadar tools not working"

**Solution**:
```bash
# Verify QRadar MCP server config
python3 test_connection.py

# Check .env file
cat .env
```

---

## 📈 Performance Tips

### 1. Use Appropriate Model Size

```bash
# Fast but basic
ollama pull mistral:7b

# Balanced
ollama pull llama3.1:8b

# Best quality
ollama pull qwen2.5:14b
```

### 2. Enable GPU

Ollama automatically uses GPU if available. Verify:

```bash
# Check GPU usage while querying
nvidia-smi  # For NVIDIA GPUs
```

### 3. Optimize Context Window

```python
# In web_ui.py, reduce context for speed:
"options": {
    "num_ctx": 2048  # Reduce from 4096
}
```

### 4. Use Streaming

Streaming provides better perceived performance:

```javascript
// Switch to /api/chat/stream endpoint
// Responses appear character-by-character
```

---

## 🎓 Tips & Best Practices

### For Best Results

1. **Be specific**: "Show me open high severity offenses" vs "Show offenses"
2. **Use examples**: Click sidebar examples to learn
3. **Ask follow-ups**: Build on previous responses
4. **Use discovery tools**: Ask "What fields are available?" before building queries
5. **Save good queries**: Document successful AQL patterns

### Workflow Optimization

1. **Start broad**: "Show me all offenses"
2. **Narrow down**: "Show me offense 42 details"
3. **Investigate**: "Search events from IP X"
4. **Document**: "Add note to offense 42: [findings]"
5. **Resolve**: "Close offense 42 with reason 1"

### Chat Management

- Clear chat regularly to free memory
- Use new sessions for different investigations
- Bookmark good responses
- Export important findings

---

## 🆚 Comparison: Web UI vs Terminal Client

| Feature | Web UI | Terminal Client |
|---------|--------|-----------------|
| **Interface** | Modern, visual | Text-based |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Features** | Rich (markdown, tables) | Basic |
| **Setup** | Slightly more complex | Very simple |
| **Remote Access** | Possible | SSH required |
| **Multi-user** | Yes (sessions) | No |
| **Resource Usage** | Higher | Lower |
| **Best For** | Daily use, teams | Scripts, automation |

---

## 📚 Additional Resources

### Documentation
- [LOCAL_LLM_GUIDE.md](LOCAL_LLM_GUIDE.md) - Complete local LLM guide
- [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md) - All 41 tools
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick commands

### API Documentation
- Flask: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- Ollama API: [github.com/ollama/ollama/blob/main/docs/api.md](https://github.com/ollama/ollama/blob/main/docs/api.md)

### Frontend
- IBM Design: [carbondesignsystem.com](https://carbondesignsystem.com)
- Markdown: [daringfireball.net/projects/markdown](https://daringfireball.net/projects/markdown/)

---

## 🎉 Features Roadmap

### Planned Enhancements

- [ ] **Authentication**: User login system
- [ ] **Multi-session**: Tab-based conversations
- [ ] **Export**: Save conversations to PDF/HTML
- [ ] **Themes**: Light mode, custom themes
- [ ] **Voice**: Voice input/output
- [ ] **Dashboards**: Quick stats widgets
- [ ] **Collaboration**: Share conversations
- [ ] **Mobile App**: Native mobile interface

---

## 🆘 Getting Help

### In the Web UI
1. Click "Help" button in header
2. View example queries in sidebar
3. Check tool reference (right sidebar)

### Documentation
1. Read this guide
2. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. Review [LOCAL_LLM_GUIDE.md](LOCAL_LLM_GUIDE.md)

### Community
- Report issues
- Request features
- Share customizations

---

## ✨ Summary

The IBM QRadar MCP Web UI provides a **beautiful, modern interface** for interacting with QRadar through local LLMs.

### Key Benefits
- ✅ **Easy to use** - No command line required
- ✅ **Professional** - Polished, security-focused design
- ✅ **Powerful** - Full access to all 41 tools
- ✅ **Private** - Runs completely locally
- ✅ **Flexible** - Customizable and extensible

### Quick Start
```bash
./start_webui.sh
# Open http://localhost:5000
```

---

**Enjoy your new Web UI! 🎉**

*For questions or issues, check the documentation or create an issue on GitHub.*

---

**Version**: 1.0.0  
**Last Updated**: November 2024  
**License**: MIT

