# COMPLETE JARVIS INSTALLATION GUIDE
## From Zero to Autonomous AI Assistant

**Target System**: Windows 11 + WSL2 + RTX 3050 Ti + i7-12700H  
**Goal**: Complete autonomous AI assistant using DeepSeek R1 + Blackbox AI

---

## 🎯 OVERVIEW

This guide will install and configure:
- ✅ WSL2 Ubuntu 22.04
- ✅ NVIDIA CUDA drivers and GPU passthrough
- ✅ Ollama AI runtime
- ✅ DeepSeek R1 model (8B quantized for 4GB VRAM)
- ✅ Python environment with all dependencies
- ✅ VS Code with Blackbox AI extension
- ✅ JARVIS autonomous agent system

**Estimated Time**: 2-3 hours  
**Skill Level**: Beginner-friendly with detailed steps

---

## 📋 PHASE 1: WINDOWS PREPARATION

### Step 1.1: Enable WSL2
```powershell
# Run PowerShell as Administrator
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart Windows
shutdown /r /t 0
```

### Step 1.2: Install WSL2 Kernel Update
1. Download: https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi
2. Run the installer
3. Set WSL2 as default:
```powershell
wsl --set-default-version 2
```

### Step 1.3: Install Ubuntu 22.04
```powershell
# Install Ubuntu 22.04 LTS
wsl --install -d Ubuntu-22.04

# Or from Microsoft Store: search "Ubuntu 22.04"
```

### Step 1.4: Initial Ubuntu Setup
```bash
# First time setup - create username and password
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl wget git build-essential software-properties-common
```

---

## 🎮 PHASE 2: NVIDIA CUDA SETUP

### Step 2.1: Install NVIDIA Drivers (Windows)
1. Download latest drivers: https://www.nvidia.com/drivers
2. Install with "Custom Installation" → Check "Perform clean installation"
3. Restart Windows

### Step 2.2: Install CUDA in WSL2
```bash
# Remove any existing CUDA installations
sudo apt remove --purge '^nvidia-.*' '^libnvidia-.*' '^cuda-.*'

# Add NVIDIA package repository
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb

# Update package list
sudo apt update

# Install CUDA Toolkit (version 12.x)
sudo apt install -y cuda-toolkit-12-4

# Add CUDA to PATH
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

### Step 2.3: Verify CUDA Installation
```bash
# Check CUDA version
nvcc --version

# Check GPU visibility
nvidia-smi

# Expected output: RTX 3050 Ti with 4GB memory
```

---

## 🐍 PHASE 3: PYTHON ENVIRONMENT SETUP

### Step 3.1: Install Python 3.11
```bash
# Add deadsnakes PPA for latest Python
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Set Python 3.11 as default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
```

### Step 3.2: Create JARVIS Virtual Environment
```bash
# Create project directory
mkdir -p ~/jarvis-ai-system
cd ~/jarvis-ai-system

# Create virtual environment
python3.11 -m venv jarvis-env

# Activate environment
source jarvis-env/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Step 3.3: Install PyTorch with CUDA Support
```bash
# Install PyTorch with CUDA 12.1 support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Verify PyTorch CUDA
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

---

## 🤖 PHASE 4: OLLAMA INSTALLATION

### Step 4.1: Install Ollama
```bash
# Download and install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
ollama --version
```

### Step 4.2: Configure Ollama for GPU
```bash
# Create Ollama service directory
sudo mkdir -p /etc/systemd/system/ollama.service.d

# Create GPU configuration
sudo tee /etc/systemd/system/ollama.service.d/override.conf > /dev/null <<EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_GPU_OVERHEAD=0.5"
Environment="OLLAMA_MAX_VRAM=3.5"
EOF

# Reload systemd and restart Ollama
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

### Step 4.3: Start Ollama Service
```bash
# Start Ollama in background
ollama serve &

# Wait for service to start
sleep 5

# Check if Ollama is running
curl http://localhost:11434/api/version
```

### Step 4.4: Download DeepSeek R1 Model
```bash
# Pull DeepSeek R1 8B model (optimized for 4GB VRAM)
ollama pull deepseek-r1:8b

# This will take 10-20 minutes depending on internet speed
# Model size: ~4.7GB

# Verify model installation
ollama list
```

### Step 4.5: Test DeepSeek R1
```bash
# Test the model
ollama run deepseek-r1:8b "Hello, I am JARVIS. Please introduce yourself."

# Expected: Detailed response from DeepSeek R1
# If you get a response, the model is working correctly!
```

---

## 💻 PHASE 5: VS CODE AND BLACKBOX AI SETUP

### Step 5.1: Install VS Code (Windows)
1. Download: https://code.visualstudio.com/
2. Install with default settings
3. Launch VS Code

### Step 5.2: Install Required Extensions
```
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Install these extensions:
   - "WSL" by Microsoft
   - "Python" by Microsoft  
   - "Blackbox AI Code Generation" by Blackbox AI
   - "Remote - WSL" by Microsoft
```

### Step 5.3: Configure WSL Integration
```
1. Press Ctrl+Shift+P
2. Type "WSL: Connect to WSL"
3. Select Ubuntu-22.04
4. VS Code will restart in WSL mode
```

### Step 5.4: Configure Blackbox AI
```
1. In VS Code, press Ctrl+Shift+P
2. Type "Blackbox: Login"
3. Create account or login
4. Configure for autonomous code generation:
   - Enable "Auto-complete"
   - Enable "Code generation"
   - Set language preference to Python
```

---

## 🔧 PHASE 6: JARVIS SYSTEM INSTALLATION

### Step 6.1: Install Python Dependencies
```bash
# Activate virtual environment
cd ~/jarvis-ai-system
source jarvis-env/bin/activate

# Create requirements file
cat > requirements.txt << EOF
# Core AI and ML libraries
torch>=2.1.0
transformers>=4.35.0
accelerate>=0.24.0
bitsandbytes>=0.41.0

# Ollama and API clients
ollama>=0.1.7
requests>=2.31.0
httpx>=0.25.0

# System monitoring and control
psutil>=5.9.6
GPUtil>=1.4.0
pyautogui>=0.9.54
opencv-python>=4.8.1
Pillow>=10.1.0

# Audio processing
pyaudio>=0.2.11
SpeechRecognition>=3.10.0
pyttsx3>=2.90

# Async and utilities
asyncio>=3.4.3
aiohttp>=3.9.0
python-dotenv>=1.0.0

# Development and debugging
ipython>=8.17.0
jupyter>=1.0.0
pytest>=7.4.3
EOF

# Install all dependencies
pip install -r requirements.txt
```

### Step 6.2: Install Additional System Dependencies
```bash
# Audio system dependencies
sudo apt install -y portaudio19-dev python3-pyaudio alsa-utils pulseaudio

# Computer vision dependencies  
sudo apt install -y libopencv-dev python3-opencv

# System control dependencies
sudo apt install -y xdotool wmctrl scrot

# Network and web dependencies
sudo apt install -y curl wget firefox-esr
```

### Step 6.3: Download JARVIS Files
```bash
# Create JARVIS directory structure
mkdir -p ~/jarvis-ai-system/{src,config,logs,temp,scripts}

# Download the enhanced JARVIS files
# (Copy the files from our previous session)
# - jarvis_enhanced_agent.py → ~/jarvis-ai-system/src/
# - AI_ASSISTANT_QUICK_GUIDE.md → ~/jarvis-ai-system/
# - JARVIS_ENHANCED_SETUP_GUIDE.md → ~/jarvis-ai-system/
```

### Step 6.4: Create Configuration Files
```bash
# Create main config file
cat > ~/jarvis-ai-system/config/jarvis_config.yaml << EOF
# JARVIS Configuration
system:
  name: "JARVIS"
  version: "1.0.0"
  
hardware:
  gpu_model: "RTX 3050 Ti"
  vram_limit_gb: 4.0
  vram_safety_margin_gb: 0.5
  cpu_model: "i7-12700H"
  ram_limit_gb: 16.0
  thermal_limit_celsius: 85

ollama:
  host: "localhost"
  port: 11434
  model: "deepseek-r1:8b"
  
safety:
  confirmation_required:
    - file_deletion
    - system_commands
    - network_changes
    - process_termination
  
  blocked_operations:
    - format_disk
    - system_shutdown
    - registry_modification

blackbox:
  vscode_path: "/mnt/c/Users/*/AppData/Local/Programs/Microsoft VS Code/Code.exe"
  auto_execute: false
  timeout_seconds: 120
EOF
```

---

## 🧪 PHASE 7: TESTING AND VERIFICATION

### Step 7.1: System Health Check
```bash
# Create system check script
cat > ~/jarvis-ai-system/scripts/system_check.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import sys
import torch
import ollama
import psutil
import GPUtil

def check_cuda():
    print("🔍 Checking CUDA...")
    if torch.cuda.is_available():
        print(f"✅ CUDA available: {torch.version.cuda}")
        print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
        return True
    else:
        print("❌ CUDA not available")
        return False

def check_ollama():
    print("\n🔍 Checking Ollama...")
    try:
        client = ollama.Client()
        models = client.list()
        if any('deepseek-r1' in model['name'] for model in models['models']):
            print("✅ Ollama running with DeepSeek R1")
            return True
        else:
            print("❌ DeepSeek R1 model not found")
            return False
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return False

def check_resources():
    print("\n🔍 Checking System Resources...")
    
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_percent}%")
    
    # RAM
    ram = psutil.virtual_memory()
    print(f"RAM: {ram.used/1024**3:.1f}GB / {ram.total/1024**3:.1f}GB ({ram.percent}%)")
    
    # GPU
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            print(f"GPU: {gpu.name}")
            print(f"VRAM: {gpu.memoryUsed}MB / {gpu.memoryTotal}MB ({gpu.memoryUtil*100:.1f}%)")
        else:
            print("❌ No GPU detected")
            return False
    except:
        print("❌ GPU monitoring not available")
        return False
    
    return True

def main():
    print("🤖 JARVIS System Health Check")
    print("=" * 40)
    
    checks = [
        check_cuda(),
        check_ollama(), 
        check_resources()
    ]
    
    if all(checks):
        print("\n🎉 All systems ready! JARVIS can be started.")
        return True
    else:
        print("\n⚠️ Some systems need attention before starting JARVIS.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
EOF

# Make executable and run
chmod +x ~/jarvis-ai-system/scripts/system_check.py
python ~/jarvis-ai-system/scripts/system_check.py
```

### Step 7.2: Test DeepSeek R1 Integration
```bash
# Create test script
cat > ~/jarvis-ai-system/scripts/test_deepseek.py << 'EOF'
#!/usr/bin/env python3
import ollama
import json

def test_deepseek():
    print("🧠 Testing DeepSeek R1 Integration...")
    
    try:
        client = ollama.Client()
        
        # Test basic response
        response = client.chat(
            model='deepseek-r1:8b',
            messages=[
                {
                    'role': 'user', 
                    'content': 'You are JARVIS. Respond with a JSON object containing: {"status": "online", "message": "JARVIS systems operational", "capabilities": ["reasoning", "planning", "code_generation"]}'
                }
            ]
        )
        
        print("Response:", response['message']['content'])
        
        # Try to parse JSON from response
        content = response['message']['content']
        if '{' in content and '}' in content:
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            parsed = json.loads(json_str)
            print("✅ JSON parsing successful:", parsed)
        
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek R1 test failed: {e}")
        return False

if __name__ == "__main__":
    test_deepseek()
EOF

python ~/jarvis-ai-system/scripts/test_deepseek.py
```

### Step 7.3: Test Blackbox AI Integration
```bash
# Create simple test file for Blackbox AI
cat > ~/jarvis-ai-system/temp/blackbox_test.py << 'EOF'
"""
BLACKBOX AI TEST

Please generate a simple Python function that:
1. Takes a screenshot of the current screen
2. Saves it to ~/Desktop/test_screenshot.png
3. Returns the file path

Requirements:
- Use pyautogui or similar library
- Add error handling
- Include logging
"""

# Generated code will go here
EOF

echo "📝 Test file created: ~/jarvis-ai-system/temp/blackbox_test.py"
echo "Open this file in VS Code and use Blackbox AI to generate the code"
```

---

## 🚀 PHASE 8: LAUNCH JARVIS

### Step 8.1: Create Launch Script
```bash
# Create main launch script
cat > ~/jarvis-ai-system/start_jarvis.sh << 'EOF'
#!/bin/bash

echo "🤖 Starting JARVIS Autonomous AI Assistant"
echo "=========================================="

# Activate virtual environment
cd ~/jarvis-ai-system
source jarvis-env/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 5
fi

# Run system check
echo "Running system health check..."
python scripts/system_check.py

if [ $? -eq 0 ]; then
    echo "✅ All systems operational"
    echo "🚀 Launching JARVIS..."
    python src/jarvis_enhanced_agent.py
else
    echo "❌ System check failed. Please resolve issues before starting JARVIS."
    exit 1
fi
EOF

# Make executable
chmod +x ~/jarvis-ai-system/start_jarvis.sh
```

### Step 8.2: Create Desktop Shortcut (Optional)
```bash
# Create desktop shortcut
cat > ~/Desktop/JARVIS.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=JARVIS AI Assistant
Comment=Autonomous AI Assistant with DeepSeek R1
Exec=gnome-terminal -- bash -c "cd ~/jarvis-ai-system && ./start_jarvis.sh"
Icon=applications-science
Terminal=true
Categories=Development;Science;
EOF

chmod +x ~/Desktop/JARVIS.desktop
```

### Step 8.3: First Launch
```bash
# Launch JARVIS for the first time
cd ~/jarvis-ai-system
./start_jarvis.sh
```

---

## 🎯 VERIFICATION CHECKLIST

Before considering the installation complete, verify:

- [ ] WSL2 Ubuntu 22.04 is running
- [ ] NVIDIA drivers installed and GPU visible in WSL2
- [ ] CUDA toolkit installed and working
- [ ] Python 3.11 virtual environment created
- [ ] PyTorch with CUDA support installed
- [ ] Ollama service running
- [ ] DeepSeek R1 model downloaded and tested
- [ ] VS Code with Blackbox AI extension configured
- [ ] All Python dependencies installed
- [ ] System health check passes
- [ ] JARVIS launches without errors

---

## 🚨 TROUBLESHOOTING

### Common Issues:

**1. CUDA not detected in WSL2**
```bash
# Check Windows NVIDIA driver version
nvidia-smi.exe

# Reinstall CUDA in WSL2
sudo apt remove --purge '^cuda-.*'
# Follow CUDA installation steps again
```

**2. Ollama service won't start**
```bash
# Check logs
journalctl -u ollama -f

# Restart service
sudo systemctl restart ollama
```

**3. DeepSeek R1 model download fails**
```bash
# Check disk space
df -h

# Clear Ollama cache and retry
ollama rm deepseek-r1:8b
ollama pull deepseek-r1:8b
```

**4. Python dependencies fail to install**
```bash
# Update pip and try again
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir
```

**5. VS Code can't connect to WSL2**
```bash
# Restart WSL2
wsl --shutdown
wsl

# Reinstall WSL extension in VS Code
```

---

## 🎉 SUCCESS!

If all steps completed successfully, you now have:

✅ **Complete JARVIS AI System** running locally  
✅ **DeepSeek R1** for reasoning and planning  
✅ **Blackbox AI** for autonomous code generation  
✅ **Hardware-optimized** for your RTX 3050 Ti + i7-12700H  
✅ **Safety protocols** to prevent dangerous operations  
✅ **Autonomous capabilities** - JARVIS can actually DO things!

**Test it with**: "Take a screenshot and save it to my desktop"

Welcome to the future of autonomous AI assistants! 🚀

