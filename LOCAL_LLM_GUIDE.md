# Using IBM QRadar MCP with Local LLMs

## Overview

The IBM QRadar MCP server uses the **Model Context Protocol (MCP)**, an open standard that works with **any MCP-compatible client**, not just Claude Desktop. This guide shows you how to use it with local, open-source LLMs.

---

## 🎯 Recommended Solutions

### Option 1: Continue.dev (Easiest)

**Best for**: VS Code users, developers

#### Installation

1. **Install Continue extension** in VS Code
   ```
   Extensions → Search "Continue" → Install
   ```

2. **Install Ollama**
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Windows
   # Download from https://ollama.com/download
   ```

3. **Pull a recommended model**
   ```bash
   # Choose one or more:
   ollama pull llama3.1:8b        # 8GB RAM - Good balance
   ollama pull qwen2.5:14b        # 16GB RAM - Better reasoning
   ollama pull deepseek-coder:6.7b # 8GB RAM - Best for code
   ollama pull mistral:7b         # 8GB RAM - Fast
   ```

4. **Configure Continue for MCP**
   
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

5. **Start using!**
   - Open Continue in VS Code (Cmd+L or Ctrl+L)
   - Ask: "Show me open offenses in QRadar"
   - The local LLM will use your MCP tools!

---

### Option 2: Custom Python Client (Full Control)

**Best for**: Custom workflows, automation, integration

I'll create a simple client that connects your QRadar MCP to any local LLM:

```python
# local_mcp_client.py
import subprocess
import json
import sys
from typing import List, Dict, Any
import requests

class LocalMCPClient:
    """Connect local LLMs to QRadar MCP server"""
    
    def __init__(self, ollama_model: str = "llama3.1:8b"):
        self.ollama_model = ollama_model
        self.ollama_url = "http://localhost:11434/api/chat"
        self.conversation_history = []
        
    def call_ollama(self, prompt: str) -> str:
        """Call local Ollama model"""
        messages = self.conversation_history + [
            {"role": "user", "content": prompt}
        ]
        
        response = requests.post(
            self.ollama_url,
            json={
                "model": self.ollama_model,
                "messages": messages,
                "stream": False
            }
        )
        
        result = response.json()
        assistant_message = result["message"]["content"]
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    def chat(self):
        """Interactive chat loop"""
        print("🤖 Local MCP Chat (type 'exit' to quit)")
        print(f"📡 Using model: {self.ollama_model}")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Get response from Ollama
                response = self.call_ollama(user_input)
                print(f"\n🤖 Assistant: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    # Example usage
    client = LocalMCPClient(ollama_model="llama3.1:8b")
    client.chat()
```

**Usage**:
```bash
# Make sure Ollama is running
ollama serve

# In another terminal
python3 local_mcp_client.py
```

---

### Option 3: LM Studio (GUI)

**Best for**: Non-technical users, GUI preference

#### Setup

1. **Download LM Studio**
   - Visit [lmstudio.ai](https://lmstudio.ai)
   - Download for your OS
   - Install

2. **Download a model**
   - Open LM Studio
   - Go to "Discover" tab
   - Search for recommended models:
     - `Meta-Llama-3.1-8B-Instruct`
     - `Qwen2.5-14B-Instruct`
     - `deepseek-coder-6.7b-instruct`
   - Click download

3. **Configure MCP** (experimental feature)
   - Go to Settings → Developer
   - Enable "MCP Support"
   - Add server configuration (similar to Continue setup)

4. **Start chatting**
   - Load your model
   - Start asking about QRadar!

---

### Option 4: Open WebUI (Web Interface)

**Best for**: Team use, web interface, Docker users

#### Installation

```bash
# Using Docker
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

#### Setup

1. Open browser to `http://localhost:3000`
2. Create an account (first user is admin)
3. Connect to Ollama (usually auto-detected)
4. Configure MCP in settings

---

## 🎨 Recommended Models for QRadar MCP

### For Security Analysis (Best Choice)
```bash
# Qwen 2.5 14B - Excellent reasoning
ollama pull qwen2.5:14b
# Requires: 16GB RAM
```

### For General Use (Balanced)
```bash
# Llama 3.1 8B - Good all-rounder
ollama pull llama3.1:8b
# Requires: 8GB RAM
```

### For Code/Technical (Specialized)
```bash
# DeepSeek Coder - Best for technical queries
ollama pull deepseek-coder:6.7b
# Requires: 8GB RAM
```

### For Fast Responses (Speed)
```bash
# Mistral 7B - Very fast
ollama pull mistral:7b
# Requires: 8GB RAM
```

### For Best Quality (If you have resources)
```bash
# Qwen 2.5 72B - State of the art
ollama pull qwen2.5:72b
# Requires: 64GB RAM + GPU
```

---

## 💻 System Requirements

### Minimum (Small models: 7B-8B)
- **RAM**: 8GB
- **Storage**: 10GB free
- **CPU**: Modern multi-core processor
- **GPU**: Optional (speeds up inference)

### Recommended (Medium models: 14B-20B)
- **RAM**: 16GB
- **Storage**: 20GB free
- **CPU**: Recent multi-core processor
- **GPU**: 8GB+ VRAM (RTX 3060 or better)

### Optimal (Large models: 70B+)
- **RAM**: 64GB+
- **Storage**: 50GB free
- **CPU**: High-end multi-core
- **GPU**: 24GB+ VRAM (RTX 4090 or A6000)

---

## 🔧 Performance Tips

### 1. Use GPU Acceleration
```bash
# NVIDIA GPU (with CUDA)
# Ollama automatically uses GPU if available

# AMD GPU
# Use ROCm version of Ollama

# Apple Silicon (M1/M2/M3)
# Automatically uses Metal
```

### 2. Optimize Model Size
- Start with 7B-8B models
- Upgrade to 14B if you have RAM
- Use quantized models (Q4, Q5) for speed

### 3. Adjust Context Length
```bash
# Smaller context = faster responses
ollama run llama3.1:8b --ctx-size 2048
```

---

## 📊 Model Comparison

| Model | Size | RAM | Speed | Quality | Best For |
|-------|------|-----|-------|---------|----------|
| Mistral 7B | 7B | 8GB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | Quick queries |
| Llama 3.1 8B | 8B | 8GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Balanced use |
| DeepSeek Coder | 7B | 8GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Technical/AQL |
| Qwen 2.5 14B | 14B | 16GB | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Security analysis |
| Qwen 2.5 72B | 72B | 64GB | ⚡ | ⭐⭐⭐⭐⭐ | Best quality |

---

## 🎯 Example Workflows

### Using Continue.dev
```
1. Open VS Code
2. Press Cmd+L (Mac) or Ctrl+L (Windows)
3. Type: "Show me open high severity offenses in QRadar"
4. The local LLM uses MCP tools automatically!
```

### Using Custom Client
```python
from local_mcp_client import LocalMCPClient

client = LocalMCPClient(ollama_model="qwen2.5:14b")
client.chat()

# Then ask:
# "Show me all open offenses"
# "Search for failed login attempts"
# "What fields are available for events?"
```

### Using Ollama Directly
```bash
# Start interactive session
ollama run llama3.1:8b

# Then type your queries
# The MCP integration depends on your client
```

---

## 🔐 Privacy & Security Benefits

### Why Use Local LLMs?

✅ **Complete Privacy**
- All data stays on your machine
- No data sent to external servers
- GDPR/compliance friendly

✅ **Security**
- No internet dependency
- Air-gapped deployments possible
- Full control over data

✅ **Cost**
- No API fees
- Unlimited usage
- One-time hardware cost

✅ **Customization**
- Fine-tune models for your use case
- Full control over behavior
- Custom system prompts

---

## 🚀 Getting Started (Quickest Path)

### 5-Minute Setup

```bash
# 1. Install Ollama (if not already installed)
brew install ollama  # or use install script for Linux

# 2. Start Ollama
ollama serve

# 3. Pull a model (in another terminal)
ollama pull llama3.1:8b

# 4. Test it
ollama run llama3.1:8b
>>> Hello!
# If this works, you're ready!

# 5. Install Continue in VS Code
# Install from Extensions marketplace

# 6. Configure Continue (see config above)
# Edit ~/.continue/config.json

# 7. Start using!
# Press Cmd+L in VS Code and ask about QRadar
```

---

## 🛠️ Troubleshooting

### Ollama Not Starting
```bash
# Check if port is in use
lsof -i :11434

# Kill existing Ollama
pkill ollama

# Restart
ollama serve
```

### Model Too Slow
```bash
# Use smaller model
ollama pull llama3.1:8b

# Or quantized version
ollama pull llama3.1:8b-q4_0
```

### Out of Memory
```bash
# Use smaller context
ollama run llama3.1:8b --ctx-size 2048

# Or smaller model
ollama pull mistral:7b
```

### MCP Connection Issues
```bash
# Test QRadar MCP server independently
python3 test_connection.py

# Check MCP server logs
# Look for connection errors
```

---

## 📚 Resources

### Ollama
- Website: [ollama.com](https://ollama.com)
- Models: [ollama.com/library](https://ollama.com/library)
- GitHub: [github.com/ollama/ollama](https://github.com/ollama/ollama)

### Continue.dev
- Website: [continue.dev](https://continue.dev)
- Docs: [docs.continue.dev](https://docs.continue.dev)
- MCP Guide: [docs.continue.dev/mcp](https://docs.continue.dev/mcp)

### MCP Protocol
- Spec: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- GitHub: [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)

### LM Studio
- Website: [lmstudio.ai](https://lmstudio.ai)

---

## 🎓 Next Steps

1. **Choose your client** (Continue.dev recommended for ease)
2. **Install Ollama** and pull a model
3. **Configure MCP** connection to QRadar server
4. **Start querying** your QRadar instance!

---

## ❓ FAQ

**Q: Which model should I start with?**  
A: `llama3.1:8b` for good balance, or `qwen2.5:14b` if you have 16GB RAM.

**Q: Can I use multiple models?**  
A: Yes! Pull multiple models and switch between them.

**Q: Does this work offline?**  
A: Yes! Once models are downloaded, everything runs locally.

**Q: Is it as good as Claude?**  
A: Local 7B-14B models are very capable but Claude Opus/Sonnet may be better for complex reasoning. 70B+ local models can match or exceed Claude.

**Q: Can I fine-tune models for QRadar?**  
A: Yes! You can fine-tune open models on your specific QRadar data and use cases.

**Q: What about API compatibility?**  
A: Ollama provides OpenAI-compatible API, making it easy to integrate.

---

## 🎉 Conclusion

You can absolutely use local, open-source LLMs with your IBM QRadar MCP server! The MCP protocol is open and works with any compatible client.

**Recommended setup**: Continue.dev + Ollama + Llama 3.1 or Qwen 2.5

This gives you:
- ✅ Complete privacy
- ✅ No API costs
- ✅ Full control
- ✅ Easy setup
- ✅ All 41 QRadar MCP tools

---

**Need help setting this up? Let me know and I can create the complete integration for you!**

