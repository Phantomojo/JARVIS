# DEDICATED DRIVE SETUP INSTRUCTIONS
## Complete A: Drive Configuration for JARVIS Project

**Created by:** Manus AI (Original Concept Creator)  
**Date:** June 8, 2025  
**Purpose:** Complete setup instructions for dedicated JARVIS A: drive including WSL2 relocation

---

## 🎯 MISSION: EVERYTHING ON A: DRIVE

**CRITICAL OBJECTIVE:** Move the entire JARVIS development environment, including WSL2, to the dedicated A: drive for maximum performance, organization, and storage optimization.

---

## 📋 PHASE 1: DRIVE PREPARATION

### **1.1 Drive Setup and Formatting**

**IMMEDIATE ACTIONS for Blackbox AI:**

```cmd
# Step 1: Backup any existing data from the 500GB drive
# (User should handle this manually if needed)

# Step 2: Open Disk Management as Administrator
# Windows Key + X, select "Disk Management"

# Step 3: Delete all partitions on the 500GB drive
# Right-click each partition → Delete Volume

# Step 4: Create new simple volume
# Right-click unallocated space → New Simple Volume

# Step 5: Format with optimal settings for AI workloads
# File system: NTFS
# Allocation unit size: 64KB (optimal for large AI files)
# Volume label: JARVIS_AI
# Assign drive letter: A:
```

**PowerShell Commands for Automation:**
```powershell
# Run as Administrator
# WARNING: This will erase all data on the target disk
# Identify the correct disk number first with Get-Disk

# List all disks to identify the 500GB drive
Get-Disk

# Format the drive (replace X with correct disk number)
# Clear-Disk -Number X -RemoveData -Confirm:$false
# New-Partition -DiskNumber X -UseMaximumSize -DriveLetter A
# Format-Volume -DriveLetter A -FileSystem NTFS -AllocationUnitSize 65536 -NewFileSystemLabel "JARVIS_AI" -Confirm:$false
```

### **1.2 Directory Structure Creation**

**Create Optimal JARVIS Directory Structure:**
```cmd
# Create main JARVIS directory structure
mkdir A:\JARVIS
mkdir A:\JARVIS\WSL2
mkdir A:\JARVIS\models
mkdir A:\JARVIS\development
mkdir A:\JARVIS\cache
mkdir A:\JARVIS\data
mkdir A:\JARVIS\backups
mkdir A:\JARVIS\logs
mkdir A:\JARVIS\scripts
mkdir A:\JARVIS\environments
mkdir A:\JARVIS\temp

# Create WSL2 specific directories
mkdir A:\JARVIS\WSL2\distributions
mkdir A:\JARVIS\WSL2\docker
mkdir A:\JARVIS\WSL2\cache

# Create model-specific directories
mkdir A:\JARVIS\models\language
mkdir A:\JARVIS\models\vision
mkdir A:\JARVIS\models\speech
mkdir A:\JARVIS\models\custom

# Create development environment directories
mkdir A:\JARVIS\development\python
mkdir A:\JARVIS\development\nodejs
mkdir A:\JARVIS\development\projects
mkdir A:\JARVIS\development\tools
```

---

## 🔄 PHASE 2: WSL2 RELOCATION TO A: DRIVE

### **2.1 Export Existing WSL2 Distribution**

**If WSL2 Ubuntu Already Exists:**
```cmd
# Check existing WSL distributions
wsl --list --verbose

# Export existing Ubuntu distribution
wsl --export Ubuntu A:\JARVIS\WSL2\ubuntu-backup.tar

# Unregister the existing distribution
wsl --unregister Ubuntu
```

### **2.2 Install Fresh WSL2 on A: Drive**

**Install Ubuntu on A: Drive:**
```cmd
# Download Ubuntu 22.04 LTS
curl -L -o A:\JARVIS\WSL2\ubuntu-22.04.appx https://aka.ms/wslubuntu2204

# Install Ubuntu to A: drive
wsl --import Ubuntu A:\JARVIS\WSL2\distributions\Ubuntu A:\JARVIS\WSL2\ubuntu-22.04.appx --version 2

# Set as default distribution
wsl --set-default Ubuntu

# Set WSL version to 2
wsl --set-version Ubuntu 2
```

**Alternative Method - Import from Backup:**
```cmd
# If you exported existing Ubuntu
wsl --import Ubuntu A:\JARVIS\WSL2\distributions\Ubuntu A:\JARVIS\WSL2\ubuntu-backup.tar --version 2
```

### **2.3 Configure WSL2 for A: Drive Operation**

**Create WSL Configuration File:**
```cmd
# Create .wslconfig in user profile
echo [wsl2] > %USERPROFILE%\.wslconfig
echo memory=12GB >> %USERPROFILE%\.wslconfig
echo processors=16 >> %USERPROFILE%\.wslconfig
echo swap=4GB >> %USERPROFILE%\.wslconfig
echo swapFile=A:\JARVIS\WSL2\swap.vhdx >> %USERPROFILE%\.wslconfig
echo localhostForwarding=true >> %USERPROFILE%\.wslconfig
echo nestedVirtualization=true >> %USERPROFILE%\.wslconfig

# Create wsl.conf inside WSL2
wsl -d Ubuntu -u root bash -c "cat > /etc/wsl.conf << 'EOF'
[boot]
systemd=true

[automount]
enabled=true
root=/mnt/
options=metadata,umask=22,fmask=11

[network]
hostname=jarvis-ai
generateHosts=true
generateResolvConf=true

[interop]
enabled=true
appendWindowsPath=true
EOF"
```

### **2.4 Move Docker Desktop to A: Drive**

**Relocate Docker Desktop Data:**
```cmd
# Stop Docker Desktop
# Close Docker Desktop application

# Move Docker Desktop data to A: drive
robocopy "%USERPROFILE%\AppData\Local\Docker" "A:\JARVIS\WSL2\docker" /E /MOVE

# Create symbolic link
mklink /D "%USERPROFILE%\AppData\Local\Docker" "A:\JARVIS\WSL2\docker"

# Restart Docker Desktop
```

---

## 🐍 PHASE 3: PYTHON ENVIRONMENT SETUP ON A: DRIVE

### **3.1 Python Installation and Configuration**

**Install Python on A: Drive:**
```cmd
# Download Python 3.11 installer
curl -o A:\JARVIS\temp\python-3.11-installer.exe https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe

# Install Python to A: drive
A:\JARVIS\temp\python-3.11-installer.exe /quiet InstallAllUsers=0 TargetDir=A:\JARVIS\environments\python311 PrependPath=1

# Set environment variables
setx PYTHONHOME "A:\JARVIS\environments\python311"
setx PYTHONPATH "A:\JARVIS\environments\python311;A:\JARVIS\environments\python311\Lib;A:\JARVIS\environments\python311\Scripts"
```

**Configure pip for A: Drive:**
```cmd
# Create pip configuration
mkdir A:\JARVIS\environments\python311\pip
echo [global] > A:\JARVIS\environments\python311\pip\pip.conf
echo cache-dir = A:\JARVIS\cache\pip >> A:\JARVIS\environments\python311\pip\pip.conf
echo trusted-host = pypi.org >> A:\JARVIS\environments\python311\pip\pip.conf
echo trusted-host = pypi.python.org >> A:\JARVIS\environments\python311\pip\pip.conf
echo trusted-host = files.pythonhosted.org >> A:\JARVIS\environments\python311\pip\pip.conf

# Set pip cache environment variable
setx PIP_CACHE_DIR "A:\JARVIS\cache\pip"
```

### **3.2 Virtual Environment Setup**

**Create JARVIS Virtual Environment:**
```cmd
# Create virtual environment on A: drive
A:\JARVIS\environments\python311\python.exe -m venv A:\JARVIS\environments\jarvis_env

# Activate virtual environment
A:\JARVIS\environments\jarvis_env\Scripts\activate.bat

# Upgrade pip
python -m pip install --upgrade pip

# Install core AI packages
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers accelerate bitsandbytes
pip install nvidia-ml-py3 psutil opencv-python
pip install ultralytics whisper openai-whisper
pip install flask fastapi uvicorn
pip install numpy pandas matplotlib seaborn plotly
pip install jupyter notebook ipykernel
```

---

## 🤖 PHASE 4: AI MODEL SETUP ON A: DRIVE

### **4.1 Configure Model Cache Locations**

**Set Environment Variables for Model Caching:**
```cmd
# Hugging Face cache
setx HF_HOME "A:\JARVIS\cache\huggingface"
setx TRANSFORMERS_CACHE "A:\JARVIS\cache\huggingface\transformers"
setx HF_DATASETS_CACHE "A:\JARVIS\cache\huggingface\datasets"

# PyTorch cache
setx TORCH_HOME "A:\JARVIS\cache\torch"

# OpenAI Whisper cache
setx WHISPER_CACHE "A:\JARVIS\cache\whisper"

# Create cache directories
mkdir A:\JARVIS\cache\huggingface
mkdir A:\JARVIS\cache\huggingface\transformers
mkdir A:\JARVIS\cache\huggingface\datasets
mkdir A:\JARVIS\cache\torch
mkdir A:\JARVIS\cache\whisper
```

### **4.2 Download and Configure AI Models**

**Download Core Models to A: Drive:**
```python
# Create: A:\JARVIS\scripts\download_models.py
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import whisper

# Set cache directories
os.environ['HF_HOME'] = 'A:\\JARVIS\\cache\\huggingface'
os.environ['TORCH_HOME'] = 'A:\\JARVIS\\cache\\torch'

def download_language_model():
    """Download and cache language model"""
    model_name = "microsoft/DialoGPT-medium"  # Smaller model for testing
    
    print("Downloading language model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir="A:\\JARVIS\\models\\language")
    model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir="A:\\JARVIS\\models\\language")
    
    print("Language model downloaded successfully")

def download_speech_model():
    """Download Whisper speech model"""
    print("Downloading Whisper model...")
    model = whisper.load_model("small", download_root="A:\\JARVIS\\models\\speech")
    print("Speech model downloaded successfully")

def download_vision_models():
    """Download computer vision models"""
    print("Downloading vision models...")
    # YOLOv8 will be downloaded automatically when first used
    from ultralytics import YOLO
    model = YOLO('yolov8n.pt')  # Downloads to A:\JARVIS\cache\torch
    print("Vision models downloaded successfully")

if __name__ == "__main__":
    download_language_model()
    download_speech_model()
    download_vision_models()
    print("All models downloaded to A: drive successfully!")
```

**Run Model Download:**
```cmd
# Activate virtual environment
A:\JARVIS\environments\jarvis_env\Scripts\activate.bat

# Run model download script
python A:\JARVIS\scripts\download_models.py
```

---

## 🔧 PHASE 5: WSL2 UBUNTU CONFIGURATION ON A: DRIVE

### **5.1 Configure Ubuntu for A: Drive Operation**

**Inside WSL2 Ubuntu:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y build-essential curl wget git vim nano htop

# Install Python development tools
sudo apt install -y python3-pip python3-venv python3-dev

# Install NVIDIA drivers for WSL2
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda

# Mount A: drive in WSL2
sudo mkdir -p /mnt/jarvis
sudo mount -t drvfs A: /mnt/jarvis

# Add to fstab for automatic mounting
echo "A: /mnt/jarvis drvfs defaults,uid=1000,gid=1000,umask=022 0 0" | sudo tee -a /etc/fstab

# Create symlinks for easy access
ln -s /mnt/jarvis/JARVIS ~/jarvis
ln -s /mnt/jarvis/JARVIS/models ~/jarvis_models
ln -s /mnt/jarvis/JARVIS/development ~/jarvis_dev
ln -s /mnt/jarvis/JARVIS/data ~/jarvis_data
```

### **5.2 Python Environment in WSL2**

**Configure Python in WSL2 to Use A: Drive:**
```bash
# Create Python virtual environment on A: drive
python3 -m venv /mnt/jarvis/JARVIS/environments/wsl_jarvis_env

# Activate virtual environment
source /mnt/jarvis/JARVIS/environments/wsl_jarvis_env/bin/activate

# Install AI packages
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers accelerate bitsandbytes
pip install nvidia-ml-py3 psutil opencv-python
pip install ultralytics whisper openai-whisper

# Set environment variables in .bashrc
echo 'export JARVIS_HOME="/mnt/jarvis/JARVIS"' >> ~/.bashrc
echo 'export HF_HOME="/mnt/jarvis/JARVIS/cache/huggingface"' >> ~/.bashrc
echo 'export TORCH_HOME="/mnt/jarvis/JARVIS/cache/torch"' >> ~/.bashrc
echo 'alias jarvis="cd /mnt/jarvis/JARVIS"' >> ~/.bashrc
echo 'alias activate_jarvis="source /mnt/jarvis/JARVIS/environments/wsl_jarvis_env/bin/activate"' >> ~/.bashrc

# Reload bashrc
source ~/.bashrc
```

---

## 🚀 PHASE 6: JARVIS PROJECT SETUP ON A: DRIVE

### **6.1 Clone JARVIS Repository to A: Drive**

```cmd
# Clone repository to A: drive
cd A:\JARVIS\development\projects
git clone https://github.com/Phantomojo/JARVIS.git

# Set up project structure
cd A:\JARVIS\development\projects\JARVIS
mkdir src
mkdir tests
mkdir configs
mkdir logs
mkdir models_local
```

### **6.2 Create JARVIS Configuration Files**

**Main Configuration File:**
```python
# Create: A:\JARVIS\development\projects\JARVIS\configs\jarvis_config.py
import os

class JARVISConfig:
    # Base paths
    JARVIS_HOME = "A:\\JARVIS"
    MODELS_PATH = "A:\\JARVIS\\models"
    CACHE_PATH = "A:\\JARVIS\\cache"
    DATA_PATH = "A:\\JARVIS\\data"
    LOGS_PATH = "A:\\JARVIS\\logs"
    
    # Model configurations
    LANGUAGE_MODEL_PATH = os.path.join(MODELS_PATH, "language")
    VISION_MODEL_PATH = os.path.join(MODELS_PATH, "vision")
    SPEECH_MODEL_PATH = os.path.join(MODELS_PATH, "speech")
    
    # Hardware constraints
    MAX_VRAM_GB = 3.5  # Leave 0.5GB safety margin
    MAX_RAM_GB = 12    # Leave 4GB for system
    CPU_CORES_AI = 16  # Use most cores for AI processing
    
    # Performance targets
    LANGUAGE_RESPONSE_TIME = 3.0  # seconds
    VISION_FPS_TARGET = 20        # frames per second
    SPEECH_LATENCY_MS = 200       # milliseconds
    
    # WSL2 integration
    WSL_JARVIS_PATH = "/mnt/jarvis/JARVIS"
    WSL_PYTHON_ENV = "/mnt/jarvis/JARVIS/environments/wsl_jarvis_env"
```

### **6.3 Create Startup Scripts**

**Windows Startup Script:**
```cmd
# Create: A:\JARVIS\scripts\start_jarvis_windows.bat
@echo off
echo Starting JARVIS AI Assistant...

# Activate Python environment
call A:\JARVIS\environments\jarvis_env\Scripts\activate.bat

# Set environment variables
set JARVIS_HOME=A:\JARVIS
set HF_HOME=A:\JARVIS\cache\huggingface
set TORCH_HOME=A:\JARVIS\cache\torch

# Start JARVIS main application
cd A:\JARVIS\development\projects\JARVIS
python src\jarvis_main.py

pause
```

**WSL2 Startup Script:**
```bash
# Create: A:\JARVIS\scripts\start_jarvis_wsl.sh
#!/bin/bash
echo "Starting JARVIS AI Assistant in WSL2..."

# Activate Python environment
source /mnt/jarvis/JARVIS/environments/wsl_jarvis_env/bin/activate

# Set environment variables
export JARVIS_HOME="/mnt/jarvis/JARVIS"
export HF_HOME="/mnt/jarvis/JARVIS/cache/huggingface"
export TORCH_HOME="/mnt/jarvis/JARVIS/cache/torch"

# Start JARVIS main application
cd /mnt/jarvis/JARVIS/development/projects/JARVIS
python src/jarvis_main.py
```

---

## 📊 PHASE 7: PERFORMANCE OPTIMIZATION FOR A: DRIVE

### **7.1 Drive Performance Optimization**

**Optimize A: Drive for AI Workloads:**
```cmd
# Disable indexing for better performance
fsutil behavior set DisableLastAccess 1

# Optimize for large files
fsutil behavior set MemoryUsage 2

# Disable compression (better for AI files)
compact /u A:\JARVIS /s /i

# Set optimal prefetch
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters" /v EnablePrefetcher /t REG_DWORD /d 3 /f
```

### **7.2 Memory and Cache Optimization**

**Configure System for A: Drive Operation:**
```cmd
# Set virtual memory to A: drive
# Control Panel → System → Advanced → Performance Settings → Advanced → Virtual Memory
# Set custom size on A: drive: Initial 4096MB, Maximum 8192MB

# Configure Windows to optimize for background services
reg add "HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 24 /f
```

---

## 🔍 PHASE 8: VERIFICATION AND TESTING

### **8.1 System Verification Checklist**

**Verify A: Drive Setup:**
```cmd
# Check drive space and health
dir A:\ /s
chkdsk A: /f

# Verify WSL2 on A: drive
wsl --list --verbose
wsl -d Ubuntu -e df -h /mnt/jarvis

# Test Python environments
A:\JARVIS\environments\jarvis_env\Scripts\python.exe --version
wsl -d Ubuntu -e /mnt/jarvis/JARVIS/environments/wsl_jarvis_env/bin/python --version

# Test GPU access
A:\JARVIS\environments\jarvis_env\Scripts\python.exe -c "import torch; print(torch.cuda.is_available())"
wsl -d Ubuntu -e /mnt/jarvis/JARVIS/environments/wsl_jarvis_env/bin/python -c "import torch; print(torch.cuda.is_available())"
```

### **8.2 Performance Baseline**

**Establish Performance Baselines:**
```python
# Create: A:\JARVIS\scripts\performance_test.py
import time
import torch
import psutil
import nvidia_ml_py3 as nvml

def test_drive_performance():
    """Test A: drive performance"""
    print("Testing A: drive performance...")
    
    # Write test
    start_time = time.time()
    with open("A:\\JARVIS\\temp\\test_file.dat", "wb") as f:
        f.write(b"0" * (100 * 1024 * 1024))  # 100MB
    write_time = time.time() - start_time
    
    # Read test
    start_time = time.time()
    with open("A:\\JARVIS\\temp\\test_file.dat", "rb") as f:
        data = f.read()
    read_time = time.time() - start_time
    
    print(f"Write speed: {100/write_time:.2f} MB/s")
    print(f"Read speed: {100/read_time:.2f} MB/s")
    
    # Cleanup
    import os
    os.remove("A:\\JARVIS\\temp\\test_file.dat")

def test_gpu_performance():
    """Test GPU performance"""
    if torch.cuda.is_available():
        device = torch.device("cuda")
        x = torch.randn(1000, 1000, device=device)
        
        start_time = time.time()
        for _ in range(100):
            y = torch.matmul(x, x)
        torch.cuda.synchronize()
        gpu_time = time.time() - start_time
        
        print(f"GPU performance: {gpu_time*1000:.2f}ms for 100 operations")
    else:
        print("CUDA not available")

if __name__ == "__main__":
    test_drive_performance()
    test_gpu_performance()
```

---

## ✅ COMPLETION CHECKLIST

### **A: Drive Setup Verification:**
- [ ] 500GB drive formatted as A: with NTFS and 64KB clusters
- [ ] Complete JARVIS directory structure created
- [ ] WSL2 Ubuntu installed and running from A: drive
- [ ] Docker Desktop data moved to A: drive
- [ ] Python environments created on A: drive
- [ ] AI models downloaded and cached on A: drive
- [ ] All environment variables pointing to A: drive
- [ ] Performance optimization applied
- [ ] Startup scripts created and tested

### **Integration Verification:**
- [ ] WSL2 can access A: drive at /mnt/jarvis
- [ ] Python environments work in both Windows and WSL2
- [ ] GPU accessible from both environments
- [ ] AI frameworks installed and functional
- [ ] Model loading works from A: drive
- [ ] Performance meets targets

### **Project Readiness:**
- [ ] JARVIS repository cloned to A: drive
- [ ] Configuration files created
- [ ] Startup scripts functional
- [ ] Development environment ready
- [ ] All documentation accessible on A: drive

---

## 🚀 NEXT STEPS AFTER A: DRIVE SETUP

1. **Run System Readiness Checklist** from A: drive
2. **Begin JARVIS implementation** using Blackbox AI prompt
3. **Monitor performance** and optimize as needed
4. **Backup critical configurations** regularly

**The A: drive is now the complete JARVIS command center with everything needed for fictional-grade AI development!** 🎯

