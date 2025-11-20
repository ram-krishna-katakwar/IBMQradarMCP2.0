#!/bin/bash
# Setup script for local LLM with QRadar MCP

echo "================================================"
echo "IBM QRadar MCP - Local LLM Setup"
echo "================================================"
echo ""

# Check if Ollama is installed
echo "🔍 Checking for Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    OLLAMA_VERSION=$(ollama --version 2>&1 | head -n 1)
    echo "   Version: $OLLAMA_VERSION"
else
    echo "❌ Ollama is not installed"
    echo ""
    echo "To install Ollama:"
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  brew install ollama"
    else
        echo "  curl -fsSL https://ollama.com/install.sh | sh"
    fi
    echo ""
    echo "Or visit: https://ollama.com/download"
    exit 1
fi

echo ""

# Check if Ollama is running
echo "🔍 Checking if Ollama is running..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama is not running"
    echo ""
    echo "Starting Ollama..."
    echo "  Run in another terminal: ollama serve"
    echo ""
    read -p "Press Enter when Ollama is running..."
fi

echo ""

# Check for recommended models
echo "🔍 Checking for recommended models..."
MODELS=$(ollama list 2>/dev/null | tail -n +2 | awk '{print $1}')

if echo "$MODELS" | grep -q "llama3.1"; then
    echo "✅ Llama 3.1 is installed"
    RECOMMENDED_MODEL="llama3.1:8b"
elif echo "$MODELS" | grep -q "qwen2.5"; then
    echo "✅ Qwen 2.5 is installed"
    RECOMMENDED_MODEL="qwen2.5:14b"
elif echo "$MODELS" | grep -q "mistral"; then
    echo "✅ Mistral is installed"
    RECOMMENDED_MODEL="mistral:7b"
else
    echo "⚠️  No recommended model found"
    echo ""
    echo "Available models:"
    if [ -z "$MODELS" ]; then
        echo "  (none)"
    else
        echo "$MODELS" | while read model; do
            echo "  - $model"
        done
    fi
    echo ""
    echo "Recommended models for QRadar MCP:"
    echo "  1. llama3.1:8b      (8GB RAM) - Balanced"
    echo "  2. qwen2.5:14b      (16GB RAM) - Best reasoning"
    echo "  3. deepseek-coder   (8GB RAM) - Technical/code"
    echo "  4. mistral:7b       (8GB RAM) - Fast"
    echo ""
    read -p "Enter model name to download (or press Enter to skip): " MODEL_TO_DOWNLOAD
    
    if [ ! -z "$MODEL_TO_DOWNLOAD" ]; then
        echo ""
        echo "📥 Downloading $MODEL_TO_DOWNLOAD..."
        ollama pull "$MODEL_TO_DOWNLOAD"
        RECOMMENDED_MODEL="$MODEL_TO_DOWNLOAD"
    else
        echo "⚠️  Skipping model download"
        echo "   You can download later with: ollama pull llama3.1:8b"
        RECOMMENDED_MODEL="llama3.1:8b"
    fi
fi

echo ""

# Check Python dependencies
echo "🔍 Checking Python dependencies..."
if python3 -c "import requests" 2>/dev/null; then
    echo "✅ Python requests library is installed"
else
    echo "⚠️  Python requests library not found"
    echo ""
    read -p "Install with pip? (y/n): " INSTALL_DEPS
    if [[ "$INSTALL_DEPS" == "y" ]]; then
        pip3 install requests
    fi
fi

echo ""

# Check QRadar MCP configuration
echo "🔍 Checking QRadar MCP configuration..."
if [ -f ".env" ]; then
    echo "✅ .env file found"
    if grep -q "QRADAR_HOST" .env && grep -q "QRADAR_API_TOKEN" .env; then
        echo "✅ QRadar credentials configured"
    else
        echo "⚠️  .env file incomplete"
        echo "   Make sure QRADAR_HOST and QRADAR_API_TOKEN are set"
    fi
else
    echo "⚠️  .env file not found"
    echo ""
    echo "Create .env file with:"
    echo "  QRADAR_HOST=your-qradar-host.com"
    echo "  QRADAR_API_TOKEN=your-api-token"
    echo "  QRADAR_VERIFY_SSL=true"
fi

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "To start the local LLM client:"
echo ""
echo "  python3 local_llm_client.py"
echo ""
echo "Or specify a model:"
echo ""
echo "  python3 local_llm_client.py --model $RECOMMENDED_MODEL"
echo ""
echo "For single query:"
echo ""
echo "  python3 local_llm_client.py --query \"Show me open offenses\""
echo ""
echo "For help:"
echo ""
echo "  python3 local_llm_client.py --help"
echo ""
echo "================================================"
echo ""
echo "📚 Documentation:"
echo "  - LOCAL_LLM_GUIDE.md - Complete guide"
echo "  - ADVANCED_FEATURES.md - All tools"
echo "  - QUICK_REFERENCE.md - Quick commands"
echo ""
echo "================================================"

