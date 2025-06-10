# JARVIS Enhanced Setup Guide
## Building on the Existing JARVIS Project

Based on: https://github.com/Phantomojo/JARVIS

## 🎯 WHAT WE'RE BUILDING

**Goal**: Make DeepSeek R1 truly autonomous by having Blackbox AI generate the code that gives it "hands and feet"

**Architecture**:
- **DeepSeek R1** = Brain (reasoning, planning, decision-making)
- **Blackbox AI** = Hands (writes code to execute tasks)  
- **System** = Body (executes the generated code)

## 🔧 PREREQUISITES

### Hardware Requirements
- **CPU**: Intel i7-12700H (or equivalent)
- **GPU**: NVIDIA RTX 3050 Ti (4GB VRAM)
- **RAM**: 16GB system memory
- **OS**: Windows 11 + WSL2 Ubuntu 22.04

### Software Requirements
1. **Ollama** with DeepSeek R1 model
2. **VS Code** with Blackbox AI extension
3. **Python 3.11+** with required packages
4. **CUDA drivers** for GPU acceleration

## 📋 STEP-BY-STEP SETUP

### Step 1: Install Ollama and DeepSeek R1

```bash
# In WSL2 Ubuntu
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve &

# Pull DeepSeek R1 model (8B version for 4GB VRAM)
ollama pull deepseek-r1:8b

# Test the model
ollama run deepseek-r1:8b "Hello, I am JARVIS"
```

### Step 2: Install VS Code and Blackbox AI

1. **Install VS Code** on Windows
2. **Install Blackbox AI extension** from VS Code marketplace
3. **Configure Blackbox AI** for autonomous code generation
4. **Set up WSL2 integration** in VS Code

### Step 3: Install Python Dependencies

```bash
# In WSL2 Ubuntu
pip install -r requirements_jarvis.txt
```

Create `requirements_jarvis.txt`:
```
ollama>=0.1.0
requests>=2.31.0
psutil>=5.9.0
GPUtil>=1.4.0
asyncio>=3.4.3
dataclasses>=0.6
typing>=3.7.4
```

### Step 4: Download Enhanced JARVIS Files

```bash
# Create JARVIS directory
mkdir -p ~/jarvis-enhanced
cd ~/jarvis-enhanced

# Download the enhanced files (from this session)
# - jarvis_enhanced_agent.py
# - AI_ASSISTANT_QUICK_GUIDE.md
```

### Step 5: Configure Hardware Optimization

Create `hardware_config.py`:
```python
# Hardware optimization for RTX 3050 Ti + i7-12700H
import os
import psutil

# GPU Configuration
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['CUDA_MEMORY_FRACTION'] = '0.9'  # Use 90% of 4GB VRAM

# CPU Configuration  
def set_cpu_affinity():
    # Use P-cores (0-11) for AI inference
    # Use E-cores (12-19) for background tasks
    p = psutil.Process()
    p.cpu_affinity([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

# Thermal Management
def check_thermal_throttling():
    temps = psutil.sensors_temperatures()
    if 'coretemp' in temps:
        max_temp = max([temp.current for temp in temps['coretemp']])
        if max_temp > 85:
            print(f"⚠️ High CPU temperature: {max_temp}°C")
            return False
    return True
```

## 🚀 RUNNING JARVIS

### Basic Usage

```bash
cd ~/jarvis-enhanced
python jarvis_enhanced_agent.py
```

### Example Interaction

```
You: Take a screenshot and save it to my desktop

🧠 JARVIS analyzing request...

🤖 BLACKBOX AI CODE GENERATION
Task: Capture screenshot and save to desktop
File: /tmp/jarvis_blackbox/jarvis_step_1_1234567890.py
Please use Blackbox AI to generate the code, then press Enter...

🤖 JARVIS: Screenshot captured successfully and saved to ~/Desktop/screenshot_2025-06-08_22-15-30.png
```

## 🔄 HOW IT WORKS

### 1. User Request Processing
```
User: "Create a Python script to monitor CPU usage"
↓
DeepSeek R1: Analyzes request, creates execution plan
↓
Plan: [
  Step 1: Generate CPU monitoring code
  Step 2: Create the Python file
  Step 3: Test the script
]
```

### 2. Code Generation with Blackbox AI
```
JARVIS → Opens VS Code with detailed prompt
↓
Blackbox AI → Generates Python code for CPU monitoring
↓
JARVIS → Executes the generated code
↓
Result → Python script created and tested
```

### 3. Safety and Resource Management
```
Before each step:
✓ Check VRAM usage (< 3.5GB of 4GB)
✓ Check CPU temperature (< 85°C)
✓ Validate safety level (GREEN/YELLOW/RED)
✓ Request user confirmation if needed
```

## 🛡️ SAFETY PROTOCOLS

### Safety Levels
- **GREEN**: Safe operations (automatic execution)
  - File reading, calculations, web browsing
- **YELLOW**: Caution required (ask user first)
  - File writing, system commands, network operations
- **RED**: Dangerous operations (explicit warnings)
  - File deletion, system shutdown, registry changes

### Example Safety Check
```
⚠️ JARVIS CONFIRMATION REQUIRED ⚠️
Step: Delete temporary files in Downloads folder
Safety Level: YELLOW
Blackbox Instructions: Generate code to delete files older than 30 days...
Proceed with this step? (y/n):
```

## 🔧 CUSTOMIZATION

### Adding New Capabilities

1. **Define new TaskType** in `jarvis_enhanced_agent.py`
2. **Create Blackbox AI instructions** for the new capability
3. **Add safety validation** for the new operations
4. **Test with hardware constraints**

### Example: Adding Email Capability
```python
class TaskType(Enum):
    EMAIL_OPERATIONS = "email_operations"  # Add this

# In the system prompt, add:
# - Email operations (send, read, organize)

# Create Blackbox instructions:
blackbox_instructions = """
Generate Python code to send an email using SMTP.
Requirements:
- Use smtplib and email libraries
- Handle authentication securely
- Add error handling for network issues
- Log all operations
"""
```

## 📊 MONITORING AND DEBUGGING

### Resource Monitoring
```bash
# Check JARVIS logs
tail -f jarvis_autonomous_agent.log

# Monitor system resources
watch -n 1 'nvidia-smi && echo "---" && htop -n 1'
```

### Common Issues and Solutions

1. **VRAM Overflow**
   ```
   Error: VRAM usage too high: 3.8GB / 4.0GB
   Solution: Restart JARVIS or reduce model size
   ```

2. **Thermal Throttling**
   ```
   Error: CPU temperature too high: 87°C
   Solution: Improve cooling or reduce workload
   ```

3. **Blackbox AI Not Generating Code**
   ```
   Solution: Ensure VS Code is properly configured
   Check Blackbox AI extension is active
   Verify prompt file is opened correctly
   ```

## 🎯 NEXT STEPS

### Phase 1: Basic Automation (Current)
- ✅ Computer control (mouse, keyboard, screenshots)
- ✅ File operations (create, read, write)
- ✅ Basic system monitoring

### Phase 2: Advanced Features
- 🔄 Voice interaction with wake words
- 🔄 Web browsing and research automation
- 🔄 Application control and automation

### Phase 3: Intelligence Enhancement
- 🔄 Proactive assistance and learning
- 🔄 Multi-modal understanding
- 🔄 Emotional intelligence

### Phase 4: Fictional-Grade AI
- 🔄 Advanced reasoning and planning
- 🔄 Situational awareness
- 🔄 Autonomous problem-solving

## 📚 ADDITIONAL RESOURCES

### From the Original JARVIS Project
- **Complete Documentation**: https://github.com/Phantomojo/JARVIS
- **Hardware Optimization Guide**: `hardware_specific_blackbox_instructions.md`
- **System Readiness Checklist**: `SYSTEM_READINESS_CHECKLIST.md`
- **AI Collaboration Guide**: `ai_collaboration_guide.md`

### Key Files to Reference
1. `BLACKBOX_AI_IMPLEMENTATION_PROMPT.md` - Complete Blackbox AI instructions
2. `jarvis_enhancement_plan.md` - Technical architecture details
3. `additional_critical_resources.md` - Advanced tools and templates

## 🚨 IMPORTANT NOTES

1. **Hardware Constraints**: Everything must work within 4GB VRAM
2. **Safety First**: Always implement user confirmation for dangerous operations
3. **Local Operation**: No cloud dependencies, complete privacy
4. **Blackbox AI is Key**: The autonomous capabilities depend on Blackbox AI generating the right code
5. **Thermal Management**: Monitor CPU temperature to prevent throttling

## 🎉 SUCCESS METRICS

**You'll know JARVIS is working when**:
- User says "take a screenshot" → Screenshot appears on desktop automatically
- User says "create a Python script" → Script is generated and saved
- User says "check system resources" → Detailed report is provided
- All operations respect hardware constraints and safety protocols

**The ultimate goal**: Transform DeepSeek R1 from a chatbot into a true autonomous agent that can actually DO things, not just talk about them.

