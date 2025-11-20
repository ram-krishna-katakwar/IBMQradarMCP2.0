# IBM QRadar MCP Server - Setup Guide

This guide will walk you through setting up the IBM QRadar MCP server step by step.

## Step 1: Prerequisites

Before you begin, ensure you have:

- [ ] Python 3.10 or higher installed
- [ ] Access to an IBM QRadar instance
- [ ] Network connectivity to QRadar API (typically port 443)
- [ ] Admin or API access permissions in QRadar

Verify Python version:
```bash
python --version
# or
python3 --version
```

## Step 2: Get QRadar API Token

### Creating an Authorized Service in QRadar

1. **Log into QRadar Console**
   - Open your web browser
   - Navigate to your QRadar console URL
   - Log in with admin credentials

2. **Navigate to Authorized Services**
   - Click **Admin** tab at the top
   - Click **Authorized Services** in the left menu

3. **Create New Authorized Service**
   - Click **Create Authorized Service** button
   - Fill in the form:
     - **Name**: `MCP Server` (or any descriptive name)
     - **Authentication Type**: Select "Token Authentication"
     - **User**: Select your admin user or service account

4. **Set Permissions**
   
   Select the following permissions (minimum required):
   - [ ] **Ariel**: Read access for event/flow queries
   - [ ] **Assets**: Read access for asset information
   - [ ] **Log Sources**: Read access for log source management
   - [ ] **Offenses**: Read access for offense data
   - [ ] **Reference Data**: Read access for reference sets
   - [ ] **Rules**: Read access for analytics rules
   - [ ] **System**: Read access for system information

5. **Generate Token**
   - Click **Create Service**
   - **Important**: Copy the generated token immediately
   - Store it securely - you won't be able to see it again

## Step 3: Install the MCP Server

### Clone or Download

If you have the code in a repository:
```bash
git clone <repository-url>
cd IBMQradarMCP
```

Or if you have the code locally, navigate to the directory:
```bash
cd /path/to/IBMQradarMCP
```

### Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment

### Create .env File

```bash
cp .env.example .env
```

### Edit .env File

Open `.env` in your text editor and fill in your values:

```env
# Your QRadar hostname or IP (without https://)
QRADAR_HOST=qradar.yourcompany.com

# The API token you created in Step 2
QRADAR_API_TOKEN=your-very-long-api-token-here

# SSL verification (use 'true' for production)
QRADAR_VERIFY_SSL=true
```

**Notes**:
- `QRADAR_HOST`: Do NOT include `https://` or trailing slash
  - ✅ Good: `qradar.company.com`
  - ✅ Good: `192.168.1.100`
  - ❌ Bad: `https://qradar.company.com/`
  
- `QRADAR_VERIFY_SSL`: 
  - Use `true` for production with valid certificates
  - Use `false` for development with self-signed certificates

## Step 5: Test the Server

### Standalone Test

Run the server directly to test:

```bash
python -m src.server
```

The server should start without errors. You should see:
```
INFO:qradar-mcp:IBM QRadar MCP Server starting...
```

Press `Ctrl+C` to stop.

### Test QRadar Connection

Create a simple test script `test_connection.py`:

```python
import os
from dotenv import load_dotenv
from src.qradar_client import QRadarClient

load_dotenv()

host = os.getenv("QRADAR_HOST")
token = os.getenv("QRADAR_API_TOKEN")
verify_ssl = os.getenv("QRADAR_VERIFY_SSL", "true").lower() == "true"

print(f"Testing connection to {host}...")

try:
    client = QRadarClient(host, token, verify_ssl)
    info = client.get_system_info()
    print("✅ Connection successful!")
    print(f"QRadar Version: {info.get('external_version', 'Unknown')}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run it:
```bash
python test_connection.py
```

## Step 6: Configure with Claude Desktop

### Locate Configuration File

**macOS**:
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows**:
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux**:
```bash
~/.config/Claude/claude_desktop_config.json
```

### Edit Configuration

Open the file in a text editor and add the MCP server configuration:

```json
{
  "mcpServers": {
    "qradar": {
      "command": "python3",
      "args": ["-m", "src.server"],
      "cwd": "/absolute/path/to/IBMQradarMCP",
      "env": {
        "QRADAR_HOST": "qradar.yourcompany.com",
        "QRADAR_API_TOKEN": "your-api-token-here",
        "QRADAR_VERIFY_SSL": "true"
      }
    }
  }
}
```

**Important**: 
- Replace `/absolute/path/to/IBMQradarMCP` with the actual full path
- If using virtual environment, use full path to Python:
  - macOS/Linux: `/path/to/IBMQradarMCP/venv/bin/python3`
  - Windows: `C:\path\to\IBMQradarMCP\venv\Scripts\python.exe`

### Restart Claude Desktop

1. Quit Claude Desktop completely
2. Restart Claude Desktop
3. The QRadar MCP server should now be available

## Step 7: Verify Integration

In Claude Desktop, try these commands:

1. **Check if MCP is loaded**:
   ```
   What MCP tools do you have access to?
   ```
   
   You should see QRadar tools listed.

2. **Test system info**:
   ```
   Get QRadar system information
   ```

3. **Test event query**:
   ```
   Show me the 10 most recent security events from QRadar
   ```

## Troubleshooting

### Issue: "Module not found" error

**Solution**: Make sure you're using the correct Python interpreter
```bash
# Check which Python
which python3

# Use absolute path in Claude config
"command": "/usr/local/bin/python3"
```

### Issue: "Connection refused" or "Timeout"

**Possible causes**:
1. QRadar host is incorrect
2. Firewall blocking connection
3. QRadar API service is down

**Solutions**:
- Verify host with: `ping your-qradar-host`
- Check firewall rules
- Verify you can access QRadar web interface

### Issue: "401 Unauthorized"

**Cause**: Invalid or expired API token

**Solution**:
1. Go back to QRadar Authorized Services
2. Delete the old service
3. Create a new one
4. Update `.env` with new token

### Issue: "SSL Certificate verification failed"

**For Development**:
```env
QRADAR_VERIFY_SSL=false
```

**For Production**:
1. Get QRadar certificate
2. Add to system trust store
3. Keep `QRADAR_VERIFY_SSL=true`

### Issue: MCP server not showing in Claude

**Solutions**:
1. Check Claude Desktop logs
2. Verify JSON syntax in config file
3. Ensure absolute paths are used
4. Restart Claude Desktop completely

## Next Steps

Once setup is complete:

1. Read the [README.md](README.md) for available tools
2. Try the example queries
3. Learn AQL for custom event queries
4. Explore QRadar API documentation

## Security Checklist

- [ ] API token stored securely (not in code)
- [ ] `.env` file in `.gitignore`
- [ ] SSL verification enabled for production
- [ ] Minimal permissions set on authorized service
- [ ] Network connection to QRadar is secure
- [ ] Token rotation policy established

## Getting Help

If you encounter issues:

1. Check the logs in Claude Desktop
2. Run the standalone test (`python -m src.server`)
3. Verify QRadar API access through browser or curl
4. Review QRadar API documentation
5. Check GitHub issues

## Maintenance

### Regular Tasks

1. **Rotate API tokens** every 90 days
2. **Update dependencies**: `pip install --upgrade -r requirements.txt`
3. **Review permissions** in QRadar authorized services
4. **Check logs** for any errors or warnings

### Updates

To update the MCP server:

```bash
git pull  # If using git
pip install --upgrade -r requirements.txt
# Restart Claude Desktop
```

## Advanced Configuration

### Using with Virtual Environment

If Claude Desktop has issues with venv:

```json
{
  "mcpServers": {
    "qradar": {
      "command": "/absolute/path/to/venv/bin/python3",
      "args": ["-m", "src.server"],
      "cwd": "/absolute/path/to/IBMQradarMCP"
    }
  }
}
```

### Custom Logging

Set log level via environment:

```json
"env": {
  "QRADAR_HOST": "...",
  "QRADAR_API_TOKEN": "...",
  "LOG_LEVEL": "DEBUG"
}
```

### Multiple QRadar Instances

You can configure multiple instances:

```json
{
  "mcpServers": {
    "qradar-prod": {
      "command": "python3",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/IBMQradarMCP",
      "env": {
        "QRADAR_HOST": "qradar-prod.company.com",
        "QRADAR_API_TOKEN": "prod-token"
      }
    },
    "qradar-dev": {
      "command": "python3",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/IBMQradarMCP",
      "env": {
        "QRADAR_HOST": "qradar-dev.company.com",
        "QRADAR_API_TOKEN": "dev-token"
      }
    }
  }
}
```

---

**Congratulations! 🎉** Your IBM QRadar MCP server is now set up and ready to use.

