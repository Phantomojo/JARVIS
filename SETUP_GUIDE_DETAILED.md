# Complete Setup Guide for Jarvis AI Assistant on Windows with WSL

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [WSL Setup](#wsl-setup)
3. [Python Environment Setup](#python-environment-setup)
4. [Ollama and DeepSeek R1 Installation](#ollama-and-deepseek-r1-installation)
5. [VS Code and Blackbox Setup](#vs-code-and-blackbox-setup)
6. [Jarvis AI Assistant Installation](#jarvis-ai-assistant-installation)
7. [Configuration](#configuration)
8. [Running the Application](#running-the-application)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Configuration](#advanced-configuration)

## Prerequisites

### System Requirements
- **Operating System**: Windows 10 version 2004 or higher, or Windows 11
- **RAM**: Minimum 8 GB (16 GB recommended for better performance)
- **Storage**: At least 15 GB free space
- **Processor**: 64-bit processor with virtualization support
- **Audio**: Microphone and speakers/headphones for voice interaction
- **Network**: Internet connection for initial setup

### Required Software
- Windows Subsystem for Linux 2 (WSL2)
- Ubuntu 22.04 LTS (or compatible Linux distribution)
- Python 3.8 or higher
- VS Code with Blackbox AI extension
- Git (for cloning repositories)

## WSL Setup

### Step 1: Enable WSL
1. Open PowerShell as Administrator
2. Run the following command:
```powershell
wsl --install
```

3. If WSL is already installed, update it:
```powershell
wsl --update
```

4. Restart your computer when prompted

### Step 2: Install Ubuntu
1. Open Microsoft Store
2. Search for "Ubuntu 22.04 LTS"
3. Click "Install"
4. Launch Ubuntu from the Start menu
5. Create a username and password when prompted

### Step 3: Update Ubuntu
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 4: Install Essential Tools
```bash
sudo apt install -y curl wget git build-essential software-properties-common
```

## Python Environment Setup

### Step 1: Install Python 3.11
```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
```

### Step 2: Set Python 3.11 as Default
```bash
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
```

### Step 3: Install pip for Python 3.11
```bash
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
```

### Step 4: Install Audio Dependencies
```bash
sudo apt install -y portaudio19-dev python3-pyaudio espeak espeak-data libespeak1 libespeak-dev
sudo apt install -y pulseaudio pulseaudio-utils alsa-utils
```

### Step 5: Install GUI Dependencies
```bash
sudo apt install -y python3-tk python3-tkinter
```

### Step 6: Install System Monitoring Dependencies
```bash
sudo apt install -y lm-sensors
```

## Ollama and DeepSeek R1 Installation

### Step 1: Install Ollama
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Start Ollama Service
```bash
# Start Ollama in the background
ollama serve &
```

### Step 3: Download DeepSeek R1 Model
```bash
# Download the 8B parameter model (recommended for most systems)
ollama pull deepseek-r1:8b

# For systems with more RAM (32GB+), you can use the larger model:
# ollama pull deepseek-r1:32b
```

### Step 4: Test Ollama Installation
```bash
ollama list
ollama run deepseek-r1:8b "Hello, how are you?"
```

### Step 5: Configure Ollama for API Access
Create a systemd service file for Ollama:
```bash
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
```

Create ollama user:
```bash
sudo useradd -r -s /bin/false -m -d /usr/share/ollama ollama
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
```

## VS Code and Blackbox Setup

### Step 1: Install VS Code on Windows
1. Download VS Code from https://code.visualstudio.com/
2. Install with default settings
3. Launch VS Code

### Step 2: Install WSL Extension
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "WSL"
4. Install the "WSL" extension by Microsoft

### Step 3: Install Blackbox AI Extension
1. In VS Code Extensions
2. Search for "Blackbox AI"
3. Install the "Blackbox AI Code Generation" extension
4. Sign up for a Blackbox account if prompted

### Step 4: Connect to WSL
1. Press Ctrl+Shift+P
2. Type "WSL: Connect to WSL"
3. Select your Ubuntu distribution

### Step 5: Install Python Extension in WSL
1. In the WSL VS Code window
2. Go to Extensions
3. Install "Python" extension by Microsoft

## Jarvis AI Assistant Installation

### Step 1: Create Project Directory
```bash
mkdir -p ~/jarvis-ai-assistant
cd ~/jarvis-ai-assistant
```

### Step 2: Create Virtual Environment
```bash
python3.11 -m venv jarvis-env
source jarvis-env/bin/activate
```

### Step 3: Upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```

### Step 4: Install Required Packages
Create requirements.txt:
```bash
cat > requirements.txt << 'EOF'
# Core dependencies
requests>=2.31.0
ollama>=0.1.7
psutil>=5.9.0
pyautogui>=0.9.54
pillow>=10.0.0
opencv-python>=4.8.0
numpy>=1.24.0
scipy>=1.11.0

# Voice recognition and synthesis
SpeechRecognition>=3.10.0
pyttsx3>=2.90
pyaudio>=0.2.11

# GUI framework
tkinter-tooltip>=2.0.0

# System integration
python-dotenv>=1.0.0
configparser>=6.0.0

# Optional: Enhanced features
openai>=1.3.0
anthropic>=0.7.0
google-generativeai>=0.3.0

# Development tools
black>=23.0.0
flake8>=6.0.0
pytest>=7.4.0
EOF
```

Install packages:
```bash
pip install -r requirements.txt
```

### Step 5: Download Jarvis Files
Copy all the Python files we created:
- `jarvis_agent_main.py`
- `deepseek_integration.py`
- `blackbox_integration.py`
- `system_control.py`
- `voice_control.py`

```bash
# If you have the files locally, copy them to the project directory
# Otherwise, create them manually using the provided code
```

### Step 6: Create Configuration File
```bash
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
```

### Step 7: Create Startup Script
```bash
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
```

## Configuration

### Step 1: Configure Audio for WSL
Add to ~/.bashrc:
```bash
echo 'export PULSE_RUNTIME_PATH="/mnt/wslg/runtime-dir/pulse"' >> ~/.bashrc
echo 'export PULSE_SERVER="unix:${PULSE_RUNTIME_PATH}/native"' >> ~/.bashrc
source ~/.bashrc
```

### Step 2: Test Audio
```bash
# Test speakers
speaker-test -t wav -c 2

# Test microphone (install if needed)
sudo apt install -y audacity
```

### Step 3: Configure Permissions
```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Set up udev rules for device access
sudo tee /etc/udev/rules.d/99-jarvis.rules > /dev/null <<EOF
# Allow access to input devices for Jarvis
SUBSYSTEM=="input", GROUP="input", MODE="0664"
SUBSYSTEM=="usb", ATTRS{idVendor}=="*", ATTRS{idProduct}=="*", GROUP="plugdev", MODE="0664"
EOF

sudo udevadm control --reload-rules
```

## Running the Application

### Step 1: Start Ollama (if not running)
```bash
ollama serve &
```

### Step 2: Activate Virtual Environment
```bash
cd ~/jarvis-ai-assistant
source jarvis-env/bin/activate
```

### Step 3: Launch Jarvis
```bash
python jarvis_agent_main.py
```

Or use the startup script:
```bash
./start_jarvis.sh
```

### Step 4: First Run Setup
1. The application will open with a dark-themed GUI
2. Check the status bar for connection status
3. Test voice recognition by clicking the Voice button
4. Try a simple command like "Hello Jarvis"

## Troubleshooting

### Common Issues and Solutions

#### 1. Ollama Connection Failed
```bash
# Check if Ollama is running
ps aux | grep ollama

# Restart Ollama
pkill ollama
ollama serve &

# Test connection
curl http://localhost:11434/api/tags
```

#### 2. Voice Recognition Not Working
```bash
# Check audio devices
arecord -l
aplay -l

# Test microphone
arecord -d 5 test.wav
aplay test.wav

# Install additional audio packages
sudo apt install -y pavucontrol
```

#### 3. PyAudio Installation Issues
```bash
# Install dependencies
sudo apt install -y portaudio19-dev python3-dev

# Reinstall PyAudio
pip uninstall pyaudio
pip install pyaudio
```

#### 4. GUI Not Displaying
```bash
# Check X11 forwarding
echo $DISPLAY

# Install X11 apps
sudo apt install -y x11-apps
xeyes  # Test X11

# For WSL2, ensure WSLg is enabled
```

#### 5. Permission Denied Errors
```bash
# Fix file permissions
chmod +x start_jarvis.sh
chmod 755 ~/jarvis-ai-assistant

# Add user to necessary groups
sudo usermod -a -G audio,input,video $USER
```

#### 6. DeepSeek Model Not Found
```bash
# List available models
ollama list

# Pull the model again
ollama pull deepseek-r1:8b

# Check model size and available space
df -h
```

### Performance Optimization

#### 1. Increase WSL Memory Limit
Create or edit `%USERPROFILE%\.wslconfig`:
```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
```

#### 2. Optimize Ollama Performance
```bash
# Set environment variables for better performance
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_FLASH_ATTENTION=1
```

#### 3. Reduce Model Size (if needed)
```bash
# Use smaller model for lower-end systems
ollama pull deepseek-r1:1.5b
```

## Advanced Configuration

### Custom Voice Commands
Edit the voice command processing in `jarvis_agent_main.py`:
```python
def process_voice_command(self, command: str) -> str:
    # Add your custom commands here
    command = command.lower()
    
    if "custom command" in command:
        return "Custom response"
    
    # ... existing code
```

### Custom System Controls
Add new system control functions in `system_control.py`:
```python
def custom_system_function(self):
    """Add your custom system control function"""
    pass
```

### Integration with Other AI Models
Modify `deepseek_integration.py` to support additional models:
```python
# Add support for other Ollama models
SUPPORTED_MODELS = [
    "deepseek-r1:8b",
    "llama2:7b",
    "codellama:7b",
    # Add more models as needed
]
```

### Blackbox AI Configuration
Configure Blackbox integration in `blackbox_integration.py`:
```python
# Customize Blackbox settings
BLACKBOX_CONFIG = {
    "auto_complete": True,
    "code_explanation": True,
    "code_generation": True,
    # Add more settings
}
```

## Security Considerations

### 1. Network Security
- Ollama runs on localhost by default
- Consider firewall rules if exposing to network
- Use VPN for remote access

### 2. Voice Privacy
- Voice recognition uses Google Speech API
- Consider offline alternatives for privacy
- Review voice data handling policies

### 3. System Access
- Jarvis has system control capabilities
- Review and limit permissions as needed
- Use safety mode for testing

### 4. File Access
- Jarvis can access files in WSL environment
- Consider sandboxing for production use
- Regular security updates

## Maintenance

### Regular Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Update Python packages
pip install --upgrade -r requirements.txt

# Update Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Update models
ollama pull deepseek-r1:8b
```

### Backup Configuration
```bash
# Backup configuration and chat history
tar -czf jarvis-backup-$(date +%Y%m%d).tar.gz ~/jarvis-ai-assistant
```

### Log Management
```bash
# View logs
tail -f ~/jarvis-ai-assistant/jarvis_agent.log

# Rotate logs
logrotate /etc/logrotate.d/jarvis
```

## Support and Resources

### Documentation
- Ollama: https://ollama.ai/docs
- DeepSeek: https://deepseek.com/
- Blackbox AI: https://blackbox.ai/
- WSL: https://docs.microsoft.com/en-us/windows/wsl/

### Community
- GitHub Issues: Report bugs and feature requests
- Discord/Forums: Community support
- Stack Overflow: Technical questions

### Professional Support
- Consider professional support for enterprise deployments
- Custom development services available
- Training and consultation services

---

This completes the comprehensive setup guide for Jarvis AI Assistant on Windows with WSL. Follow each step carefully, and don't hesitate to refer to the troubleshooting section if you encounter any issues.

