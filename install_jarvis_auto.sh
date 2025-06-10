#!/bin/bash

# JARVIS Auto-Installer Script
# Automated installation of the complete JARVIS AI system
# Target: Windows 11 + WSL2 + RTX 3050 Ti + i7-12700H

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Check if running in WSL2
check_wsl2() {
    if [[ ! -f /proc/version ]] || ! grep -q "microsoft" /proc/version; then
        error "This script must be run in WSL2 Ubuntu. Please install WSL2 first."
    fi
    
    if ! grep -q "WSL2" /proc/version; then
        warn "WSL version detection unclear. Continuing anyway..."
    fi
    
    log "✅ Running in WSL2 environment"
}

# Update system packages
update_system() {
    log "📦 Updating system packages..."
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y curl wget git build-essential software-properties-common
    log "✅ System packages updated"
}

# Install CUDA
install_cuda() {
    log "🎮 Installing NVIDIA CUDA..."
    
    # Remove existing CUDA installations
    sudo apt remove --purge '^nvidia-.*' '^libnvidia-.*' '^cuda-.*' 2>/dev/null || true
    
    # Add NVIDIA repository
    wget -q https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.0-1_all.deb
    sudo dpkg -i cuda-keyring_1.0-1_all.deb
    sudo apt update
    
    # Install CUDA toolkit
    sudo apt install -y cuda-toolkit-12-4
    
    # Add to PATH
    if ! grep -q "cuda" ~/.bashrc; then
        echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
        echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
    fi
    
    source ~/.bashrc
    log "✅ CUDA installed"
}

# Install Python 3.11
install_python() {
    log "🐍 Installing Python 3.11..."
    
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update
    sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
    
    # Set as default
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
    
    log "✅ Python 3.11 installed"
}

# Create JARVIS environment
create_environment() {
    log "🏗️ Creating JARVIS environment..."
    
    # Create directory structure
    mkdir -p ~/jarvis-ai-system/{src,config,logs,temp,scripts}
    cd ~/jarvis-ai-system
    
    # Create virtual environment
    python3.11 -m venv jarvis-env
    source jarvis-env/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    log "✅ JARVIS environment created"
}

# Install PyTorch with CUDA
install_pytorch() {
    log "🔥 Installing PyTorch with CUDA support..."
    
    cd ~/jarvis-ai-system
    source jarvis-env/bin/activate
    
    # Install PyTorch with CUDA 12.1
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    
    # Verify installation
    python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')" || warn "PyTorch CUDA verification failed"
    
    log "✅ PyTorch with CUDA installed"
}

# Install Ollama
install_ollama() {
    log "🤖 Installing Ollama..."
    
    # Download and install Ollama
    curl -fsSL https://ollama.ai/install.sh | sh
    
    # Configure for GPU
    sudo mkdir -p /etc/systemd/system/ollama.service.d
    sudo tee /etc/systemd/system/ollama.service.d/override.conf > /dev/null <<EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_GPU_OVERHEAD=0.5"
Environment="OLLAMA_MAX_VRAM=3.5"
EOF
    
    # Reload and start service
    sudo systemctl daemon-reload
    sudo systemctl enable ollama
    sudo systemctl start ollama
    
    # Wait for service to start
    sleep 10
    
    log "✅ Ollama installed and configured"
}

# Download DeepSeek R1 model
download_deepseek() {
    log "🧠 Downloading DeepSeek R1 model..."
    
    # Start Ollama if not running
    if ! pgrep -x "ollama" > /dev/null; then
        ollama serve &
        sleep 10
    fi
    
    # Pull DeepSeek R1 model
    info "This may take 10-20 minutes depending on internet speed..."
    ollama pull deepseek-r1:8b
    
    # Verify model
    if ollama list | grep -q "deepseek-r1"; then
        log "✅ DeepSeek R1 model downloaded successfully"
    else
        error "Failed to download DeepSeek R1 model"
    fi
}

# Install Python dependencies
install_python_deps() {
    log "📚 Installing Python dependencies..."
    
    cd ~/jarvis-ai-system
    source jarvis-env/bin/activate
    
    # Create requirements file
    cat > requirements.txt << 'EOF'
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
    
    # Install dependencies
    pip install -r requirements.txt
    
    log "✅ Python dependencies installed"
}

# Install system dependencies
install_system_deps() {
    log "🔧 Installing system dependencies..."
    
    # Audio system
    sudo apt install -y portaudio19-dev python3-pyaudio alsa-utils pulseaudio
    
    # Computer vision
    sudo apt install -y libopencv-dev python3-opencv
    
    # System control
    sudo apt install -y xdotool wmctrl scrot
    
    # Network and web
    sudo apt install -y curl wget firefox-esr
    
    log "✅ System dependencies installed"
}

# Create configuration files
create_config() {
    log "⚙️ Creating configuration files..."
    
    cd ~/jarvis-ai-system
    
    # Main config
    cat > config/jarvis_config.yaml << 'EOF'
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
    
    log "✅ Configuration files created"
}

# Create system check script
create_system_check() {
    log "🔍 Creating system check script..."
    
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
    
    chmod +x ~/jarvis-ai-system/scripts/system_check.py
    log "✅ System check script created"
}

# Create launch script
create_launch_script() {
    log "🚀 Creating launch script..."
    
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
    
    chmod +x ~/jarvis-ai-system/start_jarvis.sh
    log "✅ Launch script created"
}

# Run final verification
run_verification() {
    log "🧪 Running final verification..."
    
    cd ~/jarvis-ai-system
    source jarvis-env/bin/activate
    
    # Run system check
    if python scripts/system_check.py; then
        log "✅ All systems verified and ready!"
        return 0
    else
        warn "Some systems need attention. Check the output above."
        return 1
    fi
}

# Main installation function
main() {
    echo "🤖 JARVIS Auto-Installer"
    echo "======================="
    echo "Installing complete JARVIS AI system..."
    echo "Target: RTX 3050 Ti + i7-12700H + WSL2"
    echo ""
    
    # Confirmation
    read -p "This will install JARVIS AI system. Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    
    # Installation steps
    check_wsl2
    update_system
    install_cuda
    install_python
    create_environment
    install_pytorch
    install_ollama
    download_deepseek
    install_python_deps
    install_system_deps
    create_config
    create_system_check
    create_launch_script
    
    echo ""
    echo "🎉 JARVIS Installation Complete!"
    echo "================================"
    echo ""
    echo "Next steps:"
    echo "1. Install VS Code on Windows with Blackbox AI extension"
    echo "2. Copy JARVIS source files to ~/jarvis-ai-system/src/"
    echo "3. Run: cd ~/jarvis-ai-system && ./start_jarvis.sh"
    echo ""
    echo "For detailed instructions, see COMPLETE_JARVIS_INSTALLATION_GUIDE.md"
    echo ""
    
    # Final verification
    if run_verification; then
        echo "🚀 JARVIS is ready to launch!"
    else
        echo "⚠️ Please resolve any issues before launching JARVIS."
    fi
}

# Run main function
main "$@"

