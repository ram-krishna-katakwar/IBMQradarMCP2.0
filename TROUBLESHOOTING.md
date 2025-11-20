# Troubleshooting Guide - IBM QRadar MCP

This guide helps you resolve common issues with the IBM QRadar MCP server.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Connection Problems](#connection-problems)
3. [Authentication Errors](#authentication-errors)
4. [Query Issues](#query-issues)
5. [Claude Desktop Integration](#claude-desktop-integration)
6. [Performance Problems](#performance-problems)
7. [API Errors](#api-errors)

---

## Installation Issues

### Problem: `pip install` fails

**Error**: 
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solutions**:

1. **Check Python version**:
```bash
python --version  # Should be 3.10+
```

2. **Upgrade pip**:
```bash
pip install --upgrade pip
```

3. **Use Python 3.10+**:
```bash
python3.10 -m pip install -r requirements.txt
```

### Problem: Module not found when running

**Error**:
```
ModuleNotFoundError: No module named 'mcp'
```

**Solution**:

Ensure you're using the correct Python interpreter:

```bash
# Check which python
which python3

# Install in that Python
python3 -m pip install -r requirements.txt
```

---

## Connection Problems

### Problem: Cannot connect to QRadar

**Error**:
```
QRadar API request failed: Connection refused
```

**Solutions**:

1. **Verify host is reachable**:
```bash
ping your-qradar-host.com
```

2. **Check port is open**:
```bash
telnet your-qradar-host.com 443
# or
nc -zv your-qradar-host.com 443
```

3. **Verify QRADAR_HOST format**:
   - ✅ Correct: `qradar.company.com`
   - ✅ Correct: `192.168.1.100`
   - ❌ Wrong: `https://qradar.company.com`
   - ❌ Wrong: `qradar.company.com/console`

4. **Check firewall rules**:
   - Ensure your machine can reach QRadar on port 443
   - Check any corporate firewalls or proxies

### Problem: Timeout errors

**Error**:
```
requests.exceptions.Timeout: Request timed out
```

**Solutions**:

1. **Check network latency**:
```bash
ping -c 5 your-qradar-host.com
```

2. **Increase timeout in client** (edit `qradar_client.py`):
```python
timeout=60  # Increase from 30
```

3. **Check QRadar server load**:
   - High CPU/memory on QRadar can cause delays
   - Check QRadar system health

---

## Authentication Errors

### Problem: 401 Unauthorized

**Error**:
```
401 Unauthorized
```

**Solutions**:

1. **Verify token is correct**:
   - Check `.env` file
   - Ensure no extra spaces or quotes
   - Token should be one long string

2. **Check token hasn't expired**:
   - Log into QRadar console
   - Go to **Admin** → **Authorized Services**
   - Verify your service is active
   - Create new token if needed

3. **Verify token has permissions**:
   - Token needs read access to APIs you're using
   - Check authorized service permissions

4. **Test token with curl**:
```bash
curl -k -H "SEC: your-token-here" \
  https://your-qradar-host.com/api/system/about
```

### Problem: 403 Forbidden

**Error**:
```
403 Forbidden
```

**Solutions**:

1. **Check API permissions**:
   - Token doesn't have permission for that endpoint
   - Update authorized service permissions in QRadar

2. **Verify user role**:
   - Ensure QRadar user has appropriate role
   - Some APIs require admin access

---

## Query Issues

### Problem: Query returns no results

**Symptoms**: Query succeeds but returns empty results

**Solutions**:

1. **Verify time range**:
```sql
-- Make sure events exist in time range
SELECT * FROM events LAST 24 HOURS
```

2. **Check filters aren't too restrictive**:
```sql
-- Remove filters one by one to isolate issue
SELECT * FROM events WHERE severity >= 5 LAST 1 HOURS
```

3. **Verify data exists**:
   - Log into QRadar console
   - Check if events exist for your query criteria

### Problem: Query timeout

**Error**:
```
Search timed out after 300 seconds
```

**Solutions**:

1. **Reduce time range**:
```sql
-- Instead of LAST 7 DAYS
SELECT * FROM events LAST 1 HOURS
```

2. **Add more specific filters**:
```sql
-- Add WHERE clause to limit data
SELECT * FROM events 
WHERE sourceip='192.168.1.100' 
LAST 24 HOURS
```

3. **Use LIMIT clause**:
```sql
SELECT * FROM events 
LAST 24 HOURS 
LIMIT 100
```

4. **Increase max_wait parameter**:
```
Search events with max_wait of 600 seconds
```

### Problem: AQL syntax error

**Error**:
```
Query failed: Invalid AQL syntax
```

**Solutions**:

1. **Check common syntax issues**:
   - Field names are correct
   - Quotes are balanced
   - Keywords are spelled correctly

2. **Test in QRadar console first**:
   - Go to **Log Activity** in QRadar
   - Test your AQL query there
   - Then use it in MCP

3. **Common mistakes**:
```sql
-- ❌ Wrong
SELECT * FROM events WHERE sourceip=192.168.1.100

-- ✅ Correct (quotes for IPs)
SELECT * FROM events WHERE sourceip='192.168.1.100'

-- ❌ Wrong
SELECT * FROM events LAST 24hours

-- ✅ Correct (space before time unit)
SELECT * FROM events LAST 24 HOURS
```

---

## Claude Desktop Integration

### Problem: MCP server not showing in Claude

**Symptoms**: QRadar tools not available in Claude

**Solutions**:

1. **Verify config file location**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Check JSON syntax**:
```bash
# Validate JSON
python -m json.tool < claude_desktop_config.json
```

3. **Use absolute paths**:
```json
{
  "mcpServers": {
    "qradar": {
      "command": "/usr/local/bin/python3",
      "cwd": "/Users/username/Code/IBMQradarMCP"
    }
  }
}
```

4. **Fully restart Claude**:
   - Quit Claude Desktop completely
   - On macOS: Cmd+Q
   - On Windows: Close from system tray
   - Restart Claude Desktop

5. **Check Claude logs**:
   - **macOS**: `~/Library/Logs/Claude/mcp.log`
   - Look for error messages

### Problem: Python not found

**Error in Claude logs**:
```
command not found: python3
```

**Solutions**:

1. **Find Python path**:
```bash
which python3
# /usr/local/bin/python3
```

2. **Use full path in config**:
```json
"command": "/usr/local/bin/python3"
```

3. **If using virtual environment**:
```json
"command": "/full/path/to/venv/bin/python3"
```

### Problem: Working directory not found

**Error**:
```
Cannot change to directory: /path/to/IBMQradarMCP
```

**Solutions**:

1. **Verify path exists**:
```bash
ls -la /path/to/IBMQradarMCP
```

2. **Use absolute path** (no `~` or `$HOME`):
   - ❌ Wrong: `~/Code/IBMQradarMCP`
   - ✅ Correct: `/Users/yourname/Code/IBMQradarMCP`

3. **Check permissions**:
```bash
# Ensure directory is readable
chmod 755 /path/to/IBMQradarMCP
```

---

## Performance Problems

### Problem: Queries are very slow

**Symptoms**: Queries take minutes to complete

**Solutions**:

1. **Optimize query**:
   - Use shorter time ranges
   - Add specific filters early
   - Select only needed fields
   - Use LIMIT clause

2. **Check QRadar performance**:
   - High CPU/memory usage
   - Many concurrent searches
   - Large index size

3. **Best practices**:
```sql
-- ✅ Good: Specific, short time range
SELECT sourceip, destinationip 
FROM events 
WHERE severity >= 7 
LAST 1 HOURS 
LIMIT 100

-- ❌ Bad: Everything, long time range
SELECT * 
FROM events 
LAST 30 DAYS
```

### Problem: Too many results

**Symptoms**: Query returns thousands of results

**Solutions**:

1. **Use LIMIT**:
```sql
SELECT * FROM events LAST 24 HOURS LIMIT 100
```

2. **Use aggregation**:
```sql
SELECT sourceip, COUNT(*) as count 
FROM events 
GROUP BY sourceip 
LAST 24 HOURS
```

3. **Be more specific**:
   - Add WHERE filters
   - Narrow time range
   - Select specific fields

---

## API Errors

### Problem: SSL Certificate verification failed

**Error**:
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions**:

**For Development/Testing**:
```env
QRADAR_VERIFY_SSL=false
```

**For Production**:

1. **Add certificate to trust store**:
```bash
# Get certificate
openssl s_client -connect qradar.company.com:443 \
  -showcerts < /dev/null 2>/dev/null | \
  openssl x509 -outform PEM > qradar.crt

# Add to Python certifi
python -m certifi  # Shows cert location
# Copy qradar.crt to that location
```

2. **Use valid certificate**:
   - Install proper SSL certificate on QRadar
   - Use certificate signed by trusted CA

### Problem: API version mismatch

**Error**:
```
API version not supported
```

**Solutions**:

1. **Check QRadar version**:
```bash
curl -k -H "SEC: token" \
  https://qradar.company.com/api/system/about
```

2. **Update API version in client** (`qradar_client.py`):
```python
self.session.headers.update({
    "Version": "16.0",  # Or your QRadar version
})
```

### Problem: Rate limiting

**Error**:
```
429 Too Many Requests
```

**Solutions**:

1. **Add delays between requests**
2. **Reduce query frequency**
3. **Check QRadar API rate limits**

---

## Diagnostic Commands

### Test connection
```bash
python test_connection.py
```

### Test Python imports
```bash
python -c "from src.qradar_client import QRadarClient; print('OK')"
```

### Test with curl
```bash
curl -k \
  -H "SEC: your-token" \
  -H "Version: 15.0" \
  https://your-qradar-host.com/api/system/about
```

### Check Python packages
```bash
pip list | grep -E "(mcp|requests|dotenv)"
```

### Validate environment
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('QRADAR_HOST'))"
```

---

## Getting Help

If you're still experiencing issues:

1. **Check logs**:
   - Claude Desktop logs
   - Run server standalone to see output

2. **Enable debug logging**:
   - Set `LOG_LEVEL=DEBUG` in environment
   - Check detailed error messages

3. **Test components separately**:
   - Test QRadar connection with curl
   - Test Python client standalone
   - Test MCP server independently

4. **Review documentation**:
   - [README.md](README.md) - Overview
   - [SETUP.md](SETUP.md) - Setup guide
   - [QUICK_START.md](QUICK_START.md) - Quick start

5. **IBM QRadar resources**:
   - [QRadar API Documentation](https://www.ibm.com/docs/en/qradar-common)
   - [QRadar API Samples](https://github.com/IBM/api-samples)

---

## Common Error Messages Reference

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| Connection refused | QRadar not reachable | Check network, host, port |
| 401 Unauthorized | Invalid token | Verify token in .env |
| 403 Forbidden | No permission | Check API permissions |
| 404 Not Found | Wrong endpoint | Check QRadar version/API |
| 429 Too Many Requests | Rate limit | Add delays, reduce requests |
| 500 Server Error | QRadar issue | Check QRadar logs, health |
| Timeout | Query too slow | Optimize query, increase timeout |
| SSL Error | Certificate issue | Disable SSL verify or fix cert |

---

## Still Need Help?

1. Run diagnostics: `python test_connection.py`
2. Check all prerequisites in [SETUP.md](SETUP.md)
3. Review [QUICK_START.md](QUICK_START.md)
4. Search IBM QRadar documentation
5. Open an issue with:
   - Error message
   - Python version
   - QRadar version
   - Steps to reproduce

