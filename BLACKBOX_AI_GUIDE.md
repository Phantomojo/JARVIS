# Blackbox AI Integration Guide for Jarvis AI Assistant

## Project Overview

This document provides comprehensive information for Blackbox AI to understand and assist with the Jarvis AI Assistant project - a local autonomous AI agent that runs on Windows with WSL Linux, featuring computer control capabilities similar to Iron Man's Jarvis.

## Project Architecture

### Core Components

1. **Main Application** (`jarvis_agent_main.py`)
   - Tkinter-based GUI with dark theme
   - Chat interface for user interaction
   - System monitoring panel
   - Voice control integration
   - Quick action buttons

2. **DeepSeek Integration** (`deepseek_integration.py`)
   - Ollama API client for DeepSeek R1 model
   - Agent system with task planning
   - Conversation management
   - Streaming response handling

3. **System Control** (`system_control.py`)
   - PyAutoGUI for mouse/keyboard control
   - psutil for system monitoring
   - Application launching and management
   - Screenshot and file operations
   - Cross-platform compatibility (Windows/Linux)

4. **Voice Control** (`voice_control.py`)
   - SpeechRecognition for voice input
   - pyttsx3 for text-to-speech
   - Wake word detection ("Hey Jarvis")
   - Background listening capabilities

5. **Blackbox Integration** (`blackbox_integration.py`)
   - VS Code extension integration
   - Code generation and completion
   - Project analysis and suggestions

## Technical Stack

### Programming Language
- **Python 3.11+** (Primary language)
- **JavaScript** (For VS Code extension integration)
- **Bash** (Setup and automation scripts)

### Key Libraries and Dependencies

#### Core AI and ML
```python
import ollama                    # DeepSeek R1 model interface
import requests                  # HTTP client for API calls
import json                      # Data serialization
import threading                 # Concurrent processing
import queue                     # Thread-safe communication
```

#### GUI Framework
```python
import tkinter as tk             # Main GUI framework
from tkinter import scrolledtext # Text widgets
from tkinter import ttk          # Themed widgets
from tkinter import filedialog   # File operations
from tkinter import messagebox   # Dialog boxes
```

#### System Control
```python
import pyautogui                 # Mouse/keyboard automation
import psutil                    # System monitoring
import subprocess                # Process management
import os                        # Operating system interface
import platform                  # Platform detection
import time                      # Time operations
import datetime                  # Date/time handling
```

#### Voice Processing
```python
import speech_recognition as sr  # Voice recognition
import pyttsx3                   # Text-to-speech
import pyaudio                   # Audio I/O
import numpy as np               # Audio processing
import scipy.io.wavfile          # Audio file handling
```

#### Image Processing
```python
from PIL import Image, ImageTk   # Image manipulation
import cv2                       # Computer vision
import numpy as np               # Numerical operations
```

### Development Environment

#### Required Software
- **WSL2** with Ubuntu 22.04 LTS
- **Python 3.11+** with pip
- **Ollama** with DeepSeek R1 model
- **VS Code** with Blackbox AI extension
- **Git** for version control

#### System Requirements
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 15GB free space
- **CPU**: 64-bit processor with virtualization
- **Audio**: Microphone and speakers for voice interaction

## Code Structure and Patterns

### Main Application Pattern
```python
class JarvisAgentGUI:
    def __init__(self, root):
        # Initialize GUI components
        # Set up dark theme
        # Initialize AI components
        # Create interface elements
        
    def initialize_components(self):
        # DeepSeek integration
        # Blackbox integration  
        # System control
        # Voice assistant
        
    def create_main_interface(self):
        # Chat area
        # Input controls
        # System monitoring
        # Quick actions
```

### AI Integration Pattern
```python
class DeepSeekIntegration:
    def __init__(self, host="localhost", port=11434):
        # Initialize Ollama client
        # Set up model configuration
        
    def generate_response(self, prompt, stream=False):
        # Send request to DeepSeek R1
        # Handle streaming responses
        # Error handling and retries
        
    def chat_completion(self, messages):
        # Multi-turn conversation
        # Context management
        # Response formatting
```

### System Control Pattern
```python
class SystemControl:
    def __init__(self, safety_mode=True):
        # Initialize PyAutoGUI
        # Set up safety features
        # Detect operating system
        
    def execute_command(self, command):
        # Validate command (safety mode)
        # Execute system command
        # Return result and status
        
    def control_mouse(self, action, x=None, y=None):
        # Mouse movement and clicking
        # Coordinate validation
        # Action logging
```

### Voice Control Pattern
```python
class VoiceAssistant:
    def __init__(self, name="Jarvis"):
        # Initialize speech recognition
        # Set up text-to-speech
        # Configure wake word detection
        
    def start_listening(self):
        # Background speech recognition
        # Wake word detection
        # Command processing
        
    def speak(self, text):
        # Text-to-speech conversion
        # Voice customization
        # Queue management
```

## Key Features Implementation

### 1. Natural Language Processing
```python
def process_message(self, message: str):
    """Process user input with DeepSeek R1"""
    # System command detection
    if message.startswith("/"):
        return self.process_system_command(message[1:])
    
    # AI processing
    response = self.agent_system.process_request(message)
    
    # Voice output
    if self.is_voice_enabled:
        self.voice_assistant.say(response)
    
    return response
```

### 2. Computer Control
```python
def take_screenshot(self, save_path=None):
    """Capture screen and save to file"""
    try:
        screenshot = pyautogui.screenshot()
        if save_path:
            screenshot.save(save_path)
        return screenshot
    except Exception as e:
        logger.error(f"Screenshot failed: {e}")
        return None

def click_at_position(self, x, y, button='left'):
    """Click at specific coordinates"""
    if self.safety_mode:
        # Validate coordinates
        screen_width, screen_height = pyautogui.size()
        if not (0 <= x <= screen_width and 0 <= y <= screen_height):
            raise ValueError("Coordinates out of bounds")
    
    pyautogui.click(x, y, button=button)
```

### 3. Voice Recognition
```python
def listen_for_wake_word(self):
    """Continuous wake word detection"""
    with sr.Microphone() as source:
        while self.is_listening:
            try:
                audio = self.recognizer.listen(source, timeout=1)
                text = self.recognizer.recognize_google(audio)
                
                if any(wake_word in text.lower() for wake_word in self.wake_words):
                    self.process_voice_command()
                    
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                logger.error(f"Voice recognition error: {e}")
```

### 4. System Monitoring
```python
def get_system_status(self):
    """Comprehensive system information"""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory()._asdict(),
        'disk': psutil.disk_usage('/')._asdict(),
        'battery': psutil.sensors_battery()._asdict() if psutil.sensors_battery() else None,
        'processes': len(psutil.pids()),
        'uptime': time.time() - psutil.boot_time()
    }
```

## Blackbox AI Integration Points

### 1. Code Generation Assistance
```python
class BlackboxIntegration:
    def generate_code(self, prompt, language="python"):
        """Generate code using Blackbox AI"""
        # Interface with VS Code extension
        # Send code generation request
        # Return formatted code
        
    def explain_code(self, code_snippet):
        """Get code explanation from Blackbox"""
        # Analyze code structure
        # Generate explanation
        # Return documentation
        
    def suggest_improvements(self, code):
        """Get code improvement suggestions"""
        # Code analysis
        # Performance suggestions
        # Best practice recommendations
```

### 2. VS Code Integration
```python
def open_in_vscode(self, file_path, line_number=None):
    """Open file in VS Code with Blackbox"""
    command = f"code {file_path}"
    if line_number:
        command += f":{line_number}"
    
    subprocess.run(command, shell=True)
```

### 3. Project Analysis
```python
def analyze_project_structure(self, project_path):
    """Analyze project for Blackbox insights"""
    # Scan project files
    # Identify patterns and technologies
    # Generate project summary
    # Suggest improvements
```

## Configuration Management

### Configuration File Structure
```ini
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

[SYSTEM]
safety_mode = true
screenshot_dir = ~/Pictures/jarvis_screenshots
log_level = INFO

[BLACKBOX]
enabled = true
vscode_path = /mnt/c/Users/%USERNAME%/AppData/Local/Programs/Microsoft VS Code/Code.exe
api_key = your_blackbox_api_key
```

### Environment Variables
```bash
# Ollama configuration
export OLLAMA_HOST=localhost
export OLLAMA_PORT=11434

# Audio configuration for WSL
export PULSE_RUNTIME_PATH="/mnt/wslg/runtime-dir/pulse"
export PULSE_SERVER="unix:${PULSE_RUNTIME_PATH}/native"

# Python path
export PYTHONPATH="${PYTHONPATH}:/home/user/jarvis-ai-assistant"
```

## Error Handling and Logging

### Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("jarvis_agent.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("JarvisAgent")
```

### Error Handling Patterns
```python
def safe_execute(self, func, *args, **kwargs):
    """Execute function with comprehensive error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in {func.__name__}: {e}")
        if self.gui:
            self.gui.add_message("error", f"Operation failed: {str(e)}")
        return None
```

## Testing and Debugging

### Unit Testing Structure
```python
import unittest
from unittest.mock import Mock, patch

class TestJarvisAgent(unittest.TestCase):
    def setUp(self):
        self.agent = JarvisAgent()
        
    def test_voice_recognition(self):
        # Test voice input processing
        pass
        
    def test_system_control(self):
        # Test system control functions
        pass
        
    def test_ai_integration(self):
        # Test DeepSeek integration
        pass
```

### Debug Mode Configuration
```python
DEBUG_MODE = os.getenv('JARVIS_DEBUG', 'False').lower() == 'true'

if DEBUG_MODE:
    logging.getLogger().setLevel(logging.DEBUG)
    pyautogui.PAUSE = 1  # Slow down automation for debugging
    pyautogui.FAILSAFE = True  # Enable failsafe
```

## Performance Optimization

### Memory Management
```python
import gc
import psutil

def monitor_memory_usage(self):
    """Monitor and optimize memory usage"""
    process = psutil.Process()
    memory_info = process.memory_info()
    
    if memory_info.rss > self.memory_threshold:
        gc.collect()  # Force garbage collection
        logger.warning(f"High memory usage: {memory_info.rss / 1024 / 1024:.1f} MB")
```

### Threading Optimization
```python
from concurrent.futures import ThreadPoolExecutor

class ThreadManager:
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
    def submit_task(self, func, *args, **kwargs):
        """Submit task to thread pool"""
        return self.executor.submit(func, *args, **kwargs)
```

## Security Considerations

### Safety Mode Implementation
```python
class SafetyManager:
    def __init__(self):
        self.dangerous_commands = [
            'rm -rf', 'del /f', 'format', 'shutdown', 'reboot'
        ]
        
    def validate_command(self, command):
        """Validate command for safety"""
        if any(dangerous in command.lower() for dangerous in self.dangerous_commands):
            raise SecurityError(f"Dangerous command blocked: {command}")
        return True
```

### Permission Management
```python
def check_permissions(self, operation):
    """Check if operation is permitted"""
    permissions = {
        'file_access': True,
        'system_control': True,
        'network_access': False,
        'admin_commands': False
    }
    
    return permissions.get(operation, False)
```

## Deployment and Distribution

### Package Structure
```
jarvis-ai-assistant/
├── src/
│   ├── jarvis_agent_main.py
│   ├── deepseek_integration.py
│   ├── blackbox_integration.py
│   ├── system_control.py
│   └── voice_control.py
├── config/
│   ├── config.ini
│   └── logging.conf
├── scripts/
│   ├── start_jarvis.sh
│   ├── install_dependencies.sh
│   └── setup_wsl.sh
├── docs/
│   ├── SETUP_GUIDE_DETAILED.md
│   ├── API_REFERENCE.md
│   └── TROUBLESHOOTING.md
├── tests/
│   ├── test_jarvis_agent.py
│   ├── test_system_control.py
│   └── test_voice_control.py
├── requirements.txt
├── setup.py
└── README.md
```

### Installation Script
```bash
#!/bin/bash
# install_jarvis.sh

set -e

echo "Installing Jarvis AI Assistant..."

# Check system requirements
python3 --version
ollama --version

# Create virtual environment
python3 -m venv jarvis-env
source jarvis-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download DeepSeek model
ollama pull deepseek-r1:8b

# Set up configuration
cp config/config.ini.example config/config.ini

echo "Installation complete!"
echo "Run './start_jarvis.sh' to launch the assistant."
```

## API Reference for Blackbox Integration

### Core Classes and Methods

#### JarvisAgentGUI
```python
class JarvisAgentGUI:
    """Main GUI application class"""
    
    def __init__(self, root: tk.Tk)
    def send_message(self) -> None
    def process_message(self, message: str) -> None
    def add_message(self, sender: str, message: str) -> None
    def take_screenshot(self) -> bool
    def start_voice_control(self) -> bool
    def stop_voice_control(self) -> bool
```

#### DeepSeekIntegration
```python
class DeepSeekIntegration:
    """DeepSeek R1 model integration"""
    
    def __init__(self, host: str = "localhost", port: int = 11434)
    def generate_response(self, prompt: str, stream: bool = False) -> str
    def chat_completion(self, messages: List[Dict]) -> str
    def is_available(self) -> bool
```

#### SystemControl
```python
class SystemControl:
    """System control and automation"""
    
    def __init__(self, safety_mode: bool = True)
    def take_screenshot(self, save_path: str = None) -> bool
    def click_at_position(self, x: int, y: int, button: str = 'left') -> None
    def type_text(self, text: str) -> None
    def get_system_info(self) -> Dict
    def execute_command(self, command: str) -> Dict
```

#### VoiceAssistant
```python
class VoiceAssistant:
    """Voice recognition and synthesis"""
    
    def __init__(self, name: str = "Jarvis", language: str = "en-US")
    def start(self) -> bool
    def stop(self) -> bool
    def say(self, text: str, block: bool = False) -> bool
    def listen_once(self, timeout: int = 5) -> Optional[str]
    def set_command_callback(self, callback: Callable) -> bool
```

## Common Use Cases for Blackbox AI

### 1. Code Generation
```python
# Example: Generate a new system control function
def generate_system_function(self, description: str) -> str:
    """Generate system control function based on description"""
    prompt = f"""
    Generate a Python function for system control with the following description:
    {description}
    
    The function should:
    - Follow the existing SystemControl class pattern
    - Include proper error handling
    - Have comprehensive docstrings
    - Use appropriate libraries (pyautogui, psutil, subprocess)
    """
    
    return self.blackbox.generate_code(prompt, language="python")
```

### 2. Code Explanation
```python
# Example: Explain complex voice processing code
def explain_voice_processing(self, code_snippet: str) -> str:
    """Get explanation of voice processing code"""
    return self.blackbox.explain_code(code_snippet)
```

### 3. Bug Detection and Fixes
```python
# Example: Analyze code for potential issues
def analyze_for_bugs(self, file_path: str) -> List[Dict]:
    """Analyze code file for potential bugs"""
    with open(file_path, 'r') as f:
        code = f.read()
    
    return self.blackbox.analyze_code(code, check_types=['bugs', 'performance', 'security'])
```

### 4. Feature Enhancement
```python
# Example: Suggest improvements for existing features
def suggest_feature_improvements(self, feature_name: str) -> List[str]:
    """Get suggestions for improving existing features"""
    current_implementation = self.get_feature_code(feature_name)
    return self.blackbox.suggest_improvements(current_implementation)
```

## Integration Testing

### Test Cases for Blackbox Integration
```python
class TestBlackboxIntegration(unittest.TestCase):
    def test_code_generation(self):
        """Test code generation functionality"""
        prompt = "Create a function to get CPU temperature"
        result = self.blackbox.generate_code(prompt)
        self.assertIn("def", result)
        self.assertIn("cpu", result.lower())
    
    def test_code_explanation(self):
        """Test code explanation functionality"""
        code = "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"
        explanation = self.blackbox.explain_code(code)
        self.assertIn("recursive", explanation.lower())
    
    def test_vscode_integration(self):
        """Test VS Code integration"""
        file_path = "/tmp/test.py"
        result = self.blackbox.open_in_vscode(file_path)
        self.assertTrue(result)
```

This comprehensive guide provides Blackbox AI with all the necessary information to understand and assist with the Jarvis AI Assistant project. The modular architecture, clear patterns, and extensive documentation make it easy to extend and enhance the system with AI-powered code generation and analysis capabilities.

