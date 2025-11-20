#!/bin/bash
# Start IBM QRadar MCP Web UI

echo "================================================"
echo "IBM QRadar MCP - Web UI Launcher"
echo "================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Check dependencies
echo ""
echo "🔍 Checking dependencies..."

MISSING_DEPS=0

if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask not installed"
    MISSING_DEPS=1
fi

if ! python3 -c "import markdown" 2>/dev/null; then
    echo "❌ Markdown not installed"
    MISSING_DEPS=1
fi

if ! python3 -c "import requests" 2>/dev/null; then
    echo "❌ Requests not installed"
    MISSING_DEPS=1
fi

if [ $MISSING_DEPS -eq 1 ]; then
    echo ""
    echo "⚠️  Missing dependencies detected"
    echo ""
    read -p "Install missing dependencies? (y/n): " INSTALL
    if [[ "$INSTALL" == "y" ]]; then
        echo ""
        echo "📦 Installing dependencies..."
        pip3 install flask markdown requests
    else
        echo ""
        echo "❌ Cannot start without dependencies"
        echo "   Install manually: pip3 install flask markdown requests"
        exit 1
    fi
fi

echo "✅ All dependencies installed"

# Check Ollama
echo ""
echo "🔍 Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
    
    # Count models
    MODEL_COUNT=$(curl -s http://localhost:11434/api/tags | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('models', [])))" 2>/dev/null)
    if [ ! -z "$MODEL_COUNT" ] && [ "$MODEL_COUNT" -gt 0 ]; then
        echo "✅ Found $MODEL_COUNT model(s)"
    else
        echo "⚠️  No models found"
        echo "   Download a model: ollama pull llama3.1:8b"
    fi
else
    echo "⚠️  Ollama is not running"
    echo ""
    echo "To start Ollama:"
    echo "  Run in another terminal: ollama serve"
    echo ""
    read -p "Continue anyway? (y/n): " CONTINUE
    if [[ "$CONTINUE" != "y" ]]; then
        exit 1
    fi
fi

# Check QRadar config
echo ""
echo "🔍 Checking QRadar configuration..."
if [ -f ".env" ]; then
    if grep -q "QRADAR_HOST" .env && grep -q "QRADAR_API_TOKEN" .env; then
        echo "✅ QRadar configuration found"
    else
        echo "⚠️  QRadar configuration incomplete"
        echo "   Make sure .env has QRADAR_HOST and QRADAR_API_TOKEN"
    fi
else
    echo "⚠️  No .env file found"
    echo "   The web UI works but won't be able to connect to QRadar"
    echo "   Create .env file with your QRadar credentials"
fi

# Start server
echo ""
echo "================================================"
echo "🚀 Starting Web UI..."
echo "================================================"
echo ""
echo "Web UI will be available at:"
echo "  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "================================================"
echo ""

# Set environment variables if needed
export OLLAMA_URL=${OLLAMA_URL:-http://localhost:11434}
export OLLAMA_MODEL=${OLLAMA_MODEL:-llama3.1:8b}

# Start the web UI
python3 web_ui.py

