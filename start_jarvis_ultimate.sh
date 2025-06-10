#!/bin/bash

echo "🚀 Starting JARVIS Ultimate Master Controller..."

# Activate virtual environment
source jarvis_env/bin/activate

# Start Ollama if not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🔄 Starting Ollama service..."
    nohup ollama serve > ollama.log 2>&1 &
    sleep 5
fi

# Check if DeepSeek R1 is available
echo "🧠 Checking DeepSeek R1 availability..."
ollama list | grep deepseek-r1 || {
    echo "📥 Installing DeepSeek R1 model..."
    ollama pull deepseek-r1:8b
}

# Start JARVIS Ultimate
echo "🤖 Launching JARVIS Ultimate Master Controller..."
python3 jarvis_ultimate_master.py

