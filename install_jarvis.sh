#!/bin/bash

# Jarvis AI Assistant - Automated Installation Script
# This script sets up the complete Jarvis AI Assistant on Windows with WSL Ubuntu

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
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Check if running on WSL
check_wsl() {
    if [[ ! -f /proc/version ]] || ! grep -q Microsoft /proc/version; then
        error "This script is designed to run on Windows Subsystem for Linux (WSL)"
        error "Please install WSL2 with Ubuntu and run this script from within WSL"
        exit 1
    fi
    log "WSL environment detected ✓"
}

# Check system requirements
check_requirements() {
    log "Checking system requirements..."
    
    # Check available memory
    MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
    if [ "$MEMORY_GB" -lt 8 ]; then
        warn "System has ${MEMORY_GB}GB RAM. 8GB+ recommended for optimal performance"
    else
        log "Memory check passed: ${MEMORY_GB}GB RAM ✓"
    fi
    
    # Check available disk space
    DISK_GB=$(df -BG / | awk 'NR==2{print $4}' | sed 's/G//')
    if [ "$DISK_GB" -lt 15 ]; then
        error "Insufficient disk space. Need at least 15GB free, have ${DISK_GB}GB"
        exit 1
    else
        log "Disk space check passed: ${DISK_GB}GB available ✓"
    fi
    
    # Check internet connectivity
    if ! ping -c 1 google.com &> /dev/null; then
        error "No internet connection. Please check your network and try again"
        exit 1
    else
        log "Internet connectivity check passed ✓"
    fi
}

# Update system packages
update_system() {
    log "Updating system packages..."
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y curl wget git build-essential software-properties-common
    log "System packages updated ✓"
}

# Install Python 3.11
install_python() {
    log "Installing Python 3.11..."
    
    # Add deadsnakes PPA for Python 3.11
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update
    
    # Install Python 3.11 and related packages
    sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
    
    # Set Python 3.11 as default
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
    
    # Install pip for Python 3.11
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
    
    log "Python 3.11 installed ✓"
    python3.11 --version
}

# Install audio dependencies
install_audio_deps() {
    log "Installing audio dependencies..."
    sudo apt install -y portaudio19-dev python3-pyaudio espeak espeak-data libespeak1 libespeak-dev
    sudo apt install -y pulseaudio pulseaudio-utils alsa-utils
    sudo apt install -y python3-tk python3-tkinter
    log "Audio dependencies installed ✓"
}

# Install system monitoring dependencies
install_system_deps() {
    log "Installing system monitoring dependencies..."
    sudo apt install -y lm-sensors
    log "System monitoring dependencies installed ✓"
}

# Install Ollama
install_ollama() {
    log "Installing Ollama..."
    
    # Download and install Ollama
    curl -fsSL https://ollama.ai/install.sh | sh
    
    # Create ollama user and systemd service
    sudo useradd -r -s /bin/false -m -d /usr/share/ollama ollama || true
    
    # Create systemd service file
    sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="OLLAMA_HOST=0.0.0.0"

[Install]
WantedBy=default.target
EOF
    
    # Enable and start Ollama service
    sudo systemctl daemon-reload
    sudo systemctl enable ollama
    sudo systemctl start ollama
    
    # Wait for Ollama to start
    sleep 5
    
    log "Ollama installed and started ✓"
}

# Download DeepSeek R1 model
download_deepseek() {
    log "Downloading DeepSeek R1 model (this may take a while)..."
    
    # Start Ollama if not running
    if ! pgrep -x "ollama" > /dev/null; then
        ollama serve &
        sleep 5
    fi
    
    # Download the model
    ollama pull deepseek-r1:8b
    
    # Test the model
    if ollama list | grep -q "deepseek-r1"; then
        log "DeepSeek R1 model downloaded successfully ✓"
    else
        error "Failed to download DeepSeek R1 model"
        exit 1
    fi
}

# Create project directory and virtual environment
setup_project() {
    log "Setting up Jarvis AI Assistant project..."
    
    # Create project directory
    PROJECT_DIR="$HOME/jarvis-ai-assistant"
    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"
    
    # Create virtual environment
    python3.11 -m venv jarvis-env
    source jarvis-env/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    log "Project directory created: $PROJECT_DIR ✓"
    echo "PROJECT_DIR=$PROJECT_DIR" > .env
}

# Install Python dependencies
install_python_deps() {
    log "Installing Python dependencies..."
    
    cd "$HOME/jarvis-ai-assistant"
    source jarvis-env/bin/activate
    
    # Create a minimal requirements.txt for core functionality
    cat > requirements.txt << 'EOF'
# Core dependencies
requests>=2.31.0
ollama>=0.1.7
psutil>=5.9.0
pyautogui>=0.9.54
pillow>=10.0.0
numpy>=1.24.0

# Voice recognition and synthesis
SpeechRecognition>=3.10.0
pyttsx3>=2.90
pyaudio>=0.2.11

# System integration
python-dotenv>=1.0.0
configparser>=6.0.0

# Development tools
black>=23.0.0
flake8>=6.0.0
EOF
    
    # Install packages
    pip install -r requirements.txt
    
    log "Python dependencies installed ✓"
}

# Configure audio for WSL
configure_audio() {
    log "Configuring audio for WSL..."
    
    # Add audio environment variables to bashrc
    if ! grep -q "PULSE_RUNTIME_PATH" ~/.bashrc; then
        echo 'export PULSE_RUNTIME_PATH="/mnt/wslg/runtime-dir/pulse"' >> ~/.bashrc
        echo 'export PULSE_SERVER="unix:${PULSE_RUNTIME_PATH}/native"' >> ~/.bashrc
    fi
    
    # Add user to audio group
    sudo usermod -a -G audio $USER
    
    log "Audio configuration completed ✓"
}

# Create configuration files
create_config() {
    log "Creating configuration files..."
    
    cd "$HOME/jarvis-ai-assistant"
    
    # Create config.ini
    cat > config.ini << 'EOF'
[DEFAULT]
# Jarvis AI Assistant Configuration

[OLLAMA]
host = localhost
port = 11434
model = deepseek-r1:8b
timeout = 30

[VOICE]
enabled = true
language = en-US
wake_words = jarvis,hey jarvis
speech_rate = 150
speech_volume = 1.0
energy_threshold = 300

[SYSTEM]
safety_mode = true
screenshot_dir = ~/Pictures/jarvis_screenshots
log_level = INFO
auto_save_chat = true

[BLACKBOX]
enabled = true
vscode_path = /mnt/c/Users/%USERNAME%/AppData/Local/Programs/Microsoft VS Code/Code.exe

[GUI]
theme = dark
window_size = 1200x800
font_family = Consolas
font_size = 11
EOF
    
    log "Configuration files created ✓"
}

# Create startup script
create_startup_script() {
    log "Creating startup script..."
    
    cd "$HOME/jarvis-ai-assistant"
    
    cat > start_jarvis.sh << 'EOF'
#!/bin/bash

# Jarvis AI Assistant Startup Script

echo "Starting Jarvis AI Assistant..."

# Activate virtual environment
source ~/jarvis-ai-assistant/jarvis-env/bin/activate

# Change to project directory
cd ~/jarvis-ai-assistant

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 5
fi

# Check if DeepSeek model is available
if ! ollama list | grep -q "deepseek-r1"; then
    echo "DeepSeek R1 model not found. Please install it first:"
    echo "ollama pull deepseek-r1:8b"
    exit 1
fi

# Set up audio for WSL
export PULSE_RUNTIME_PATH="/mnt/wslg/runtime-dir/pulse"
export PULSE_SERVER="unix:${PULSE_RUNTIME_PATH}/native"

# Start Jarvis
echo "Launching Jarvis AI Assistant..."
python jarvis_agent_main.py

echo "Jarvis AI Assistant stopped."
EOF
    
    chmod +x start_jarvis.sh
    
    log "Startup script created ✓"
}

# Download Jarvis source files
download_jarvis_files() {
    log "Setting up Jarvis source files..."
    
    cd "$HOME/jarvis-ai-assistant"
    
    # Create placeholder files (user will need to copy the actual files)
    cat > README.md << 'EOF'
# Jarvis AI Assistant

## Setup Complete!

Your Jarvis AI Assistant has been set up successfully. To complete the installation:

1. Copy the following Python files to this directory:
   - jarvis_agent_main.py
   - deepseek_integration.py
   - blackbox_integration.py
   - system_control.py
   - voice_control.py

2. Run the assistant:
   ```bash
   ./start_jarvis.sh
   ```

## Features

- Natural language conversation with DeepSeek R1
- Voice recognition and speech synthesis
- Complete computer control (mouse, keyboard, applications)
- System monitoring and automation
- Integration with VS Code and Blackbox AI

## Voice Commands

Say "Hey Jarvis" followed by your command:
- "Take a screenshot"
- "What's my CPU usage?"
- "Open calculator"
- "Show system information"

## Troubleshooting

If you encounter issues:
1. Check that Ollama is running: `ollama list`
2. Test voice recognition: Click the Voice button in the GUI
3. Check the log file: `tail -f jarvis_agent.log`

For more help, see the detailed setup guide.
EOF
    
    log "Jarvis source files setup completed ✓"
}

# Test installation
test_installation() {
    log "Testing installation..."
    
    cd "$HOME/jarvis-ai-assistant"
    source jarvis-env/bin/activate
    
    # Test Python
    if python --version | grep -q "3.11"; then
        log "Python test passed ✓"
    else
        error "Python test failed"
        exit 1
    fi
    
    # Test Ollama
    if ollama list | grep -q "deepseek-r1"; then
        log "Ollama test passed ✓"
    else
        error "Ollama test failed"
        exit 1
    fi
    
    # Test Python packages
    if python -c "import requests, psutil, pyautogui, speech_recognition, pyttsx3" 2>/dev/null; then
        log "Python packages test passed ✓"
    else
        error "Python packages test failed"
        exit 1
    fi
    
    log "All tests passed ✓"
}

# Create desktop shortcut (optional)
create_desktop_shortcut() {
    log "Creating desktop shortcut..."
    
    DESKTOP_DIR="$HOME/Desktop"
    if [ -d "$DESKTOP_DIR" ]; then
        cat > "$DESKTOP_DIR/Jarvis AI Assistant.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Jarvis AI Assistant
Comment=Local Autonomous AI Agent
Exec=bash -c "cd $HOME/jarvis-ai-assistant && ./start_jarvis.sh"
Icon=computer
Terminal=true
Categories=Development;
EOF
        chmod +x "$DESKTOP_DIR/Jarvis AI Assistant.desktop"
        log "Desktop shortcut created ✓"
    fi
}

# Main installation function
main() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    JARVIS AI ASSISTANT                      ║"
    echo "║                  Installation Script                        ║"
    echo "║                                                              ║"
    echo "║  This script will install and configure Jarvis AI Assistant ║"
    echo "║  on your Windows WSL Ubuntu system.                         ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    info "Starting installation process..."
    
    # Run installation steps
    check_wsl
    check_requirements
    update_system
    install_python
    install_audio_deps
    install_system_deps
    install_ollama
    download_deepseek
    setup_project
    install_python_deps
    configure_audio
    create_config
    create_startup_script
    download_jarvis_files
    test_installation
    create_desktop_shortcut
    
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                   INSTALLATION COMPLETE!                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    log "Jarvis AI Assistant has been successfully installed!"
    echo ""
    info "Next steps:"
    echo "1. Copy the Jarvis Python files to: $HOME/jarvis-ai-assistant/"
    echo "2. Run: cd $HOME/jarvis-ai-assistant && ./start_jarvis.sh"
    echo "3. Say 'Hey Jarvis' to start voice interaction"
    echo ""
    info "Installation directory: $HOME/jarvis-ai-assistant"
    info "Configuration file: $HOME/jarvis-ai-assistant/config.ini"
    info "Startup script: $HOME/jarvis-ai-assistant/start_jarvis.sh"
    echo ""
    warn "Please restart your terminal or run 'source ~/.bashrc' to apply audio settings"
    echo ""
    log "Enjoy your new AI assistant! 🤖"
}

# Run main function
main "$@"

