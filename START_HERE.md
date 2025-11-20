# 🚀 IBM QRadar MCP Server - START HERE

Welcome! This is your **IBM QRadar MCP (Model Context Protocol) Server**.

## What This Does

This server connects **Claude Desktop** (or other AI assistants) to your **IBM QRadar** security platform, allowing you to:

- 🔍 Query security events and logs
- 🚨 Investigate offenses and incidents  
- 🖥️ Monitor log sources (agents)
- 🌐 Analyze network assets and flows
- 📊 Review detection rules
- ⚙️ Check system health

All through natural language or AQL queries!

## Quick Start (5 Minutes)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Get QRadar API Token
1. Log into QRadar Console
2. Go to **Admin** → **Authorized Services**
3. Click **Create Authorized Service**
4. Copy the token

### 3️⃣ Configure Environment
```bash
cp .env.example .env
# Edit .env and add your QRadar host and token
```

### 4️⃣ Test Connection
```bash
python test_connection.py
```

### 5️⃣ Configure Claude Desktop
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "qradar": {
      "command": "python3",
      "args": ["-m", "src.server"],
      "cwd": "/FULL/PATH/TO/IBMQradarMCP",
      "env": {
        "QRADAR_HOST": "qradar.yourcompany.com",
        "QRADAR_API_TOKEN": "your-token-here",
        "QRADAR_VERIFY_SSL": "true"
      }
    }
  }
}
```

**Restart Claude Desktop** and you're ready!

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICK_START.md](QUICK_START.md)** | 5-minute setup guide |
| **[README.md](README.md)** | Complete documentation |
| **[SETUP.md](SETUP.md)** | Detailed setup instructions |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Problem solving |
| **[examples/example_queries.md](examples/example_queries.md)** | Query examples |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Technical overview |

## 🎯 Try These Commands

Once configured in Claude Desktop, try:

1. **"Get QRadar system information"**
2. **"Show me the 10 most recent security events"**
3. **"List all open offenses"**
4. **"Show all log sources in QRadar"**
5. **"Search for failed login attempts in the last 24 hours"**

## 🛠️ Available Tools

- **Events & Logs**: Query events/flows with AQL
- **Offenses**: List and investigate incidents
- **Log Sources**: Monitor agents and collectors
- **Assets**: Query network assets
- **Rules**: Browse detection rules
- **Reference Data**: Access threat intelligence
- **System**: Check health and status

## ⚡ Quick Commands

```bash
# Test connection
python test_connection.py

# Run server standalone
python -m src.server

# Check Python syntax
python -m py_compile src/*.py

# Verify installation
pip list | grep -E "(mcp|requests|dotenv)"
```

## 🔧 Troubleshooting

### Can't connect to QRadar?
- Check `QRADAR_HOST` (no `https://` prefix)
- Verify API token is valid
- Try `QRADAR_VERIFY_SSL=false` for testing

### Not showing in Claude?
- Use absolute paths in config
- Restart Claude Desktop completely
- Check JSON syntax

See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for detailed help.

## 📖 Next Steps

1. ✅ Complete quick start above
2. 📚 Read [README.md](README.md) for full capabilities
3. 💡 Try [example queries](examples/example_queries.md)
4. 🔍 Learn [AQL syntax](https://www.ibm.com/docs/en/qradar-common?topic=structure-aql-overview)

## 🎉 You're Ready!

Start querying QRadar through Claude Desktop!

---

**Need Help?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or [SETUP.md](SETUP.md)
