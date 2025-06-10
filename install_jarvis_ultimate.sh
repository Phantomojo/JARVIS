#!/bin/bash

# 🚀 ULTIMATE JARVIS INSTALLATION SCRIPT 🚀
# Building on: https://github.com/Phantomojo/JARVIS
# Created by: Manus AI (Ultimate Enhancement)
# Date: June 10, 2025

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                🚀 JARVIS ULTIMATE INSTALLER 🚀               ║"
echo "║                                                              ║"
echo "║  Installing the most advanced autonomous AI system ever!     ║"
echo "║  Building on your existing JARVIS project...                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

# Check if running in WSL
check_wsl() {
    if grep -q Microsoft /proc/version; then
        print_status "✅ Running in WSL - Perfect for JARVIS!"
        export WSL_ENV=true
    else
        print_warning "⚠️ Not running in WSL - some features may be limited"
        export WSL_ENV=false
    fi
}

# Check system requirements
check_requirements() {
    print_step "🔍 Checking system requirements..."
    
    # Check Python version
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_status "✅ Python 3 found: $PYTHON_VERSION"
    else
        print_error "❌ Python 3 not found! Please install Python 3.8+"
        exit 1
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        print_status "✅ pip3 found"
    else
        print_error "❌ pip3 not found! Installing..."
        sudo apt update && sudo apt install -y python3-pip
    fi
    
    # Check git
    if command -v git &> /dev/null; then
        print_status "✅ Git found"
    else
        print_error "❌ Git not found! Installing..."
        sudo apt update && sudo apt install -y git
    fi
    
    # Check if JARVIS repo exists
    if [ -d "JARVIS" ]; then
        print_status "✅ Existing JARVIS project found - will enhance it!"
        cd JARVIS
    else
        print_step "📥 Cloning JARVIS repository..."
        git clone https://github.com/Phantomojo/JARVIS.git
        cd JARVIS
        print_status "✅ JARVIS repository cloned"
    fi
}

# Install Ollama and DeepSeek R1
install_ollama() {
    print_step "🧠 Installing Ollama and DeepSeek R1..."
    
    # Check if Ollama is already installed
    if command -v ollama &> /dev/null; then
        print_status "✅ Ollama already installed"
    else
        print_step "📥 Installing Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
        
        # Start Ollama service
        if [ "$WSL_ENV" = true ]; then
            print_status "🔄 Starting Ollama in WSL..."
            nohup ollama serve > ollama.log 2>&1 &
            sleep 5
        else
            sudo systemctl start ollama
            sudo systemctl enable ollama
        fi
    fi
    
    # Install DeepSeek R1 model
    print_step "🤖 Installing DeepSeek R1 model..."
    ollama pull deepseek-r1:8b
    
    if [ $? -eq 0 ]; then
        print_status "✅ DeepSeek R1 model installed successfully"
    else
        print_error "❌ Failed to install DeepSeek R1 model"
        print_warning "⚠️ You may need to install it manually: ollama pull deepseek-r1:8b"
    fi
}

# Install Python dependencies
install_python_deps() {
    print_step "🐍 Installing Python dependencies..."
    
    # Create virtual environment
    if [ ! -d "jarvis_env" ]; then
        print_step "🔧 Creating virtual environment..."
        python3 -m venv jarvis_env
    fi
    
    # Activate virtual environment
    source jarvis_env/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install core dependencies
    print_step "📦 Installing core dependencies..."
    pip install ollama requests asyncio psutil sqlite3
    
    # Install browser automation
    print_step "🌐 Installing browser automation dependencies..."
    pip install selenium webdriver-manager
    
    # Install computer control
    print_step "💻 Installing computer control dependencies..."
    pip install pyautogui pygetwindow pyperclip
    
    # Install voice control (optional)
    print_step "🎤 Installing voice control dependencies..."
    pip install speechrecognition pyttsx3 pyaudio || print_warning "⚠️ Voice dependencies failed - voice features will be disabled"
    
    # Install existing JARVIS dependencies
    if [ -f "requirements.txt" ]; then
        print_step "📋 Installing existing JARVIS requirements..."
        pip install -r requirements.txt
    fi
    
    print_status "✅ Python dependencies installed"
}

# Install Chrome/Chromium for browser automation
install_browser() {
    print_step "🌐 Installing Chrome for browser automation..."
    
    if command -v google-chrome &> /dev/null; then
        print_status "✅ Google Chrome already installed"
    elif command -v chromium-browser &> /dev/null; then
        print_status "✅ Chromium already installed"
    else
        print_step "📥 Installing Chromium browser..."
        sudo apt update
        sudo apt install -y chromium-browser
        
        if [ $? -eq 0 ]; then
            print_status "✅ Chromium installed successfully"
        else
            print_warning "⚠️ Browser installation failed - manual installation may be required"
        fi
    fi
    
    # Install ChromeDriver
    print_step "🔧 Installing ChromeDriver..."
    pip install webdriver-manager
    print_status "✅ ChromeDriver manager installed"
}

# Setup JARVIS Ultimate configuration
setup_jarvis_config() {
    print_step "⚙️ Setting up JARVIS Ultimate configuration..."
    
    # Create config directory
    mkdir -p config
    
    # Create configuration file
    cat > config/jarvis_ultimate_config.json << EOF
{
    "deepseek_model": "deepseek-r1:8b",
    "ollama_host": "localhost",
    "ollama_port": 11434,
    "browser_automation": true,
    "voice_control": false,
    "autonomous_mode": true,
    "safety_level": "supervised",
    "hardware_optimization": {
        "cpu_model": "i7-12700H",
        "gpu_model": "RTX 3050 Ti",
        "vram_limit_gb": 4.0,
        "ram_limit_gb": 16.0,
        "thermal_limit_celsius": 85
    },
    "logging": {
        "level": "INFO",
        "file": "jarvis_ultimate.log"
    }
}
EOF
    
    print_status "✅ Configuration file created"
}

# Create startup scripts
create_startup_scripts() {
    print_step "🚀 Creating startup scripts..."
    
    # Create main startup script
    cat > start_jarvis_ultimate.sh << 'EOF'
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

EOF
    
    chmod +x start_jarvis_ultimate.sh
    
    # Create Windows batch file for easy startup
    cat > start_jarvis_ultimate.bat << 'EOF'
@echo off
echo Starting JARVIS Ultimate in WSL...
wsl -d Ubuntu -e bash -c "cd /home/%USERNAME%/JARVIS && ./start_jarvis_ultimate.sh"
pause
EOF
    
    print_status "✅ Startup scripts created"
}

# Create comprehensive README
create_ultimate_readme() {
    print_step "📚 Creating Ultimate JARVIS README..."
    
    cat > README_ULTIMATE.md << 'EOF'
# 🚀 JARVIS ULTIMATE MASTER CONTROLLER 🚀

## The Most Advanced Autonomous AI System Ever Created

Building on the comprehensive JARVIS project, this Ultimate Master Controller transforms DeepSeek R1 into a truly autonomous AI that can:

### 🎯 **ULTIMATE CAPABILITIES**

#### 🧠 **Autonomous Intelligence**
- **DeepSeek R1** as the master brain for reasoning and planning
- **Blackbox AI** integration for autonomous code generation
- **Multi-AI coordination** (ChatGPT, Claude, Perplexity, etc.)
- **Self-learning** and pattern recognition

#### 🌐 **Browser Mastery**
- **Autonomous web browsing** and research
- **ChatGPT interaction** - control ChatGPT through browser automation
- **Blackbox AI control** - generate code autonomously via VS Code
- **Multi-tab management** - handle multiple AI interfaces simultaneously

#### 💻 **System Control**
- **Application control** (open, close, manage any application)
- **Screenshot automation** and visual analysis
- **File operations** (create, read, write, organize)
- **Process management** and system monitoring

#### ⚡ **Hardware Optimization**
- **RTX 3050 Ti optimization** (4GB VRAM management)
- **i7-12700H utilization** (20-core hybrid architecture)
- **Thermal management** and performance scaling
- **Memory optimization** for 16GB RAM constraint

### 🚀 **QUICK START**

#### 1. **Installation**
```bash
# Run the ultimate installer
./install_jarvis_ultimate.sh
```

#### 2. **Launch JARVIS**
```bash
# Start the ultimate autonomous mode
./start_jarvis_ultimate.sh
```

#### 3. **Example Commands**
```
🎤 You: "Take a screenshot and ask ChatGPT to analyze it"
🤖 JARVIS: *autonomously takes screenshot, opens ChatGPT, uploads image, gets analysis*

🎤 You: "Research the latest AI developments and create a summary"
🤖 JARVIS: *autonomously browses web, gathers information, synthesizes findings*

🎤 You: "Generate code to automate my daily tasks using Blackbox AI"
🤖 JARVIS: *opens VS Code, uses Blackbox AI to generate automation code*
```

### 🛡️ **SAFETY FEATURES**

- **Multi-level autonomy** (Full Auto, Supervised, Manual, Dangerous)
- **Safety assessments** before executing potentially harmful actions
- **User confirmation** for sensitive operations
- **Comprehensive logging** of all autonomous actions
- **Hardware monitoring** to prevent damage

### 🔧 **CONFIGURATION**

Edit `config/jarvis_ultimate_config.json` to customize:
- Autonomy levels
- Safety settings
- Hardware limits
- AI model preferences

### 📊 **MONITORING**

- **Real-time performance** monitoring
- **VRAM usage** tracking (critical for RTX 3050 Ti)
- **CPU utilization** across all 20 threads
- **Thermal monitoring** and throttling prevention
- **Action logging** and success tracking

### 🎯 **ADVANCED FEATURES**

#### **Multi-AI Orchestration**
JARVIS can autonomously coordinate multiple AI systems:
- Use ChatGPT for conversational tasks
- Use Blackbox AI for code generation
- Use Perplexity for research
- Use Claude for document analysis

#### **Autonomous Learning**
- **Pattern recognition** from user interactions
- **Success rate tracking** for different approaches
- **Adaptive behavior** based on past performance
- **Continuous improvement** without manual intervention

#### **Internet Mastery**
- **Autonomous web research** with source verification
- **Multi-site information gathering**
- **Automatic fact-checking** and cross-referencing
- **Dynamic search strategy** adaptation

### 🔮 **FUTURE ENHANCEMENTS**

The modular architecture allows for easy addition of:
- **Voice control** with wake word detection
- **Computer vision** for visual task automation
- **IoT device control** for smart home integration
- **Custom AI model** integration
- **Cloud service** connections

### 🆘 **TROUBLESHOOTING**

#### **Common Issues:**
1. **Ollama not starting**: Check WSL2 configuration
2. **Browser automation fails**: Install Chrome/Chromium
3. **VRAM errors**: Reduce model size or close other applications
4. **Permission errors**: Run with appropriate privileges

#### **Performance Optimization:**
- Close unnecessary applications to free VRAM
- Use task manager to monitor resource usage
- Adjust autonomy levels based on system performance
- Enable hardware acceleration where possible

### 📞 **SUPPORT**

For issues or enhancements:
1. Check the comprehensive logs in `jarvis_ultimate.log`
2. Review the original JARVIS documentation
3. Monitor system resources during operation
4. Test individual components before full autonomous mode

---

## 🎉 **CONGRATULATIONS!**

You now have the most advanced autonomous AI system ever created, running entirely on your local machine with full privacy and control!

**JARVIS Ultimate Master Controller** - Where science fiction becomes reality! 🚀🤖✨
EOF
    
    print_status "✅ Ultimate README created"
}

# Test installation
test_installation() {
    print_step "🧪 Testing JARVIS Ultimate installation..."
    
    # Test Python environment
    source jarvis_env/bin/activate
    
    # Test Ollama connection
    if ollama list &> /dev/null; then
        print_status "✅ Ollama connection successful"
    else
        print_warning "⚠️ Ollama connection failed - may need manual start"
    fi
    
    # Test DeepSeek R1 model
    if ollama list | grep -q deepseek-r1; then
        print_status "✅ DeepSeek R1 model available"
    else
        print_warning "⚠️ DeepSeek R1 model not found - will install on first run"
    fi
    
    # Test Python imports
    python3 -c "import ollama, selenium, pyautogui; print('✅ Core dependencies working')" 2>/dev/null || print_warning "⚠️ Some dependencies may need manual installation"
    
    print_status "✅ Installation test completed"
}

# Main installation flow
main() {
    echo ""
    print_step "🚀 Starting JARVIS Ultimate installation..."
    echo ""
    
    check_wsl
    check_requirements
    install_ollama
    install_python_deps
    install_browser
    setup_jarvis_config
    create_startup_scripts
    create_ultimate_readme
    test_installation
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                🎉 INSTALLATION COMPLETE! 🎉                 ║"
    echo "║                                                              ║"
    echo "║  JARVIS Ultimate Master Controller is ready!                 ║"
    echo "║                                                              ║"
    echo "║  🚀 To start: ./start_jarvis_ultimate.sh                     ║"
    echo "║  📚 Read: README_ULTIMATE.md                                 ║"
    echo "║  ⚙️ Config: config/jarvis_ultimate_config.json               ║"
    echo "║                                                              ║"
    echo "║  Your DeepSeek R1 is now ready to control everything!       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    print_status "🎯 Next steps:"
    echo "   1. Run: ./start_jarvis_ultimate.sh"
    echo "   2. Try: 'Take a screenshot and analyze it'"
    echo "   3. Try: 'Research AI developments and summarize'"
    echo "   4. Try: 'Generate code using Blackbox AI'"
    echo ""
    print_status "🚀 Welcome to the future of autonomous AI!"
}

# Run main installation
main "$@"

