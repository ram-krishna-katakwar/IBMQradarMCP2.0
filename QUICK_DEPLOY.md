# ⚡ Quick Deploy - 5 Minutes to Running

## IBM QRadar MCP - Ultra-Fast Setup

**Get up and running in 5 minutes!**

---

## 🚀 Step 1: Install Ollama (2 min)

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from ollama.com
```

---

## 🚀 Step 2: Download a Model (2 min)

```bash
# Start Ollama
ollama serve &

# Download model (choose one)
ollama pull llama3.1:8b     # Best balance (4.7GB)
# OR
ollama pull mistral:7b      # Fastest (4.1GB)
```

⏳ *While model downloads, continue to Step 3...*

---

## 🚀 Step 3: Configure QRadar (1 min)

**Get API Token from QRadar:**
1. Log into QRadar Console
2. Admin → Authorized Services → Create
3. Copy the token

**Create config file:**
```bash
cd /Users/I0986/Code/MCPs/IBMQradarMCP2

cat > .env << 'EOF'
QRADAR_HOST=your-qradar-host.com
QRADAR_API_TOKEN=paste-token-here
QRADAR_VERIFY_SSL=true
EOF
```

**Replace:** `your-qradar-host.com` and `paste-token-here`

---

## 🚀 Step 4: Install Dependencies (30 sec)

```bash
pip3 install -r requirements.txt
```

---

## 🚀 Step 5: Launch! (10 sec)

```bash
# Start the Web UI
./start_webui.sh

# Open browser to:
# http://localhost:5000
```

**OR start terminal client:**
```bash
python3 local_llm_client.py
```

---

## ✅ Verification

**Test it works:**
```
Show me all open offenses
```

**Expected:** List of offenses from your QRadar

---

## 🎉 That's It!

**You now have:**
- ✅ Local AI assistant for QRadar
- ✅ 41 powerful security tools
- ✅ Beautiful web interface
- ✅ Complete privacy (local LLM)

---

## 📚 Next Steps

**Learn More:**
- Full guide: [GETTING_STARTED.md](GETTING_STARTED.md)
- All tools: [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)
- Examples: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**Try These:**
```
"Search for failed login attempts in last 24 hours"
"What fields are available for events?"
"Get details for offense 42"
"Show me all log sources"
```

---

## 🆘 Troubleshooting

**Issue:** "Cannot connect to Ollama"  
**Fix:** `ollama serve`

**Issue:** "No models found"  
**Fix:** `ollama pull llama3.1:8b`

**Issue:** "QRadar connection failed"  
**Fix:** Check .env file, run `python3 test_connection.py`

**More help:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🎯 One-Liner Install (Advanced)

```bash
brew install ollama && \
ollama serve & \
ollama pull llama3.1:8b && \
pip3 install -r requirements.txt && \
echo "QRADAR_HOST=your-host.com
QRADAR_API_TOKEN=your-token
QRADAR_VERIFY_SSL=true" > .env && \
./start_webui.sh
```

*Replace `your-host.com` and `your-token` before running*

---

**Ready? Let's go! 🚀**

```bash
./start_webui.sh
```

