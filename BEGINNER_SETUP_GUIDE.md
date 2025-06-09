# BEGINNER-FRIENDLY JARVIS SETUP GUIDE
## Simple Step-by-Step Instructions for Cybersecurity Students

**Created for:** New cybersecurity students  
**Difficulty:** Beginner-friendly  
**Time:** 2-3 hours total setup  

---

## 🎯 WHAT WE'RE BUILDING

**JARVIS = Your Personal AI Assistant** that can:
- Talk to you naturally (like Iron Man's JARVIS)
- See and understand images/video
- Control your computer
- Learn from your habits
- Work autonomously

**Components:**
- **DeepSeek R1** = The brain (thinking and reasoning)
- **Blackbox AI** = The hands (writes code and does tasks)
- **AutoGPT** = The autonomous agent (works independently)
- **Ollama** = Runs AI models locally on your computer

---

## 📋 STEP 1: PREPARE YOUR COMPUTER (15 minutes)

### **1.1 Check Your Hardware**
```
Your specs are perfect:
✅ Intel i7-12700H (20 cores) - Excellent for AI
✅ RTX 3050 Ti (4GB VRAM) - Good for local AI models
✅ 16GB RAM - Sufficient for our setup
✅ 500GB drive - Perfect for dedicated JARVIS storage
```

### **1.2 Format Your 500GB Drive as A: Drive**
```
1. Press Windows Key + X
2. Click "Disk Management"
3. Find your 500GB drive
4. Right-click → Delete all partitions
5. Right-click empty space → New Simple Volume
6. Choose drive letter: A
7. Format as NTFS
8. Label: JARVIS_AI
```

---

## 🔧 STEP 2: INSTALL BASIC SOFTWARE (30 minutes)

### **2.1 Install WSL2 (Windows Subsystem for Linux)**
```
1. Open PowerShell as Administrator
2. Copy and paste: wsl --install
3. Restart your computer when prompted
4. Open Ubuntu from Start menu
5. Create username and password when asked
```

### **2.2 Install Python**
```
1. Go to python.org
2. Download Python 3.11 (latest version)
3. Run installer
4. ✅ CHECK "Add Python to PATH"
5. Click "Install Now"
```

### **2.3 Install Git**
```
1. Go to git-scm.com
2. Download Git for Windows
3. Install with default settings
```

### **2.4 Install Ollama**
```
1. Go to ollama.ai
2. Click "Download for Windows"
3. Run the installer
4. Ollama will start automatically
```

---

## 🤖 STEP 3: SETUP AI MODELS (45 minutes)

### **3.1 Install DeepSeek R1 Model**
```
1. Open Command Prompt (cmd)
2. Type: ollama pull deepseek-r1
3. Wait for download (this takes 15-30 minutes)
4. Test it: ollama run deepseek-r1 "Hello, are you working?"
```

### **3.2 Move Everything to A: Drive**
```
1. Open Command Prompt as Administrator
2. Copy these commands one by one:

# Stop Ollama
taskkill /f /im ollama.exe

# Create JARVIS folders
mkdir A:\JARVIS
mkdir A:\JARVIS\ollama
mkdir A:\JARVIS\models
mkdir A:\JARVIS\projects

# Move Ollama to A: drive
robocopy "%USERPROFILE%\.ollama" "A:\JARVIS\ollama" /E /MOVE

# Create link so Ollama finds its files
mklink /D "%USERPROFILE%\.ollama" "A:\JARVIS\ollama"

# Restart Ollama
ollama serve
```

---

## 🚀 STEP 4: SETUP JARVIS PROJECT (30 minutes)

### **4.1 Download JARVIS Project**
```
1. Open Command Prompt
2. Type: cd A:\JARVIS\projects
3. Type: git clone https://github.com/Phantomojo/JARVIS.git
4. Type: cd JARVIS
```

### **4.2 Install Python Packages**
```
Copy and paste this into Command Prompt:

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers accelerate bitsandbytes
pip install openai-whisper opencv-python
pip install flask fastapi uvicorn
pip install autogpt
```

### **4.3 Setup AutoGPT Integration**
```
1. In Command Prompt, type: cd A:\JARVIS\projects
2. Type: git clone https://github.com/Significant-Gravitas/AutoGPT.git
3. Type: cd AutoGPT
4. Type: pip install -r requirements.txt
```

---

## 🔗 STEP 5: CONNECT EVERYTHING (20 minutes)

### **5.1 Create Simple Startup Script**
```
1. Open Notepad
2. Copy this code:

@echo off
echo Starting JARVIS AI Assistant...
cd A:\JARVIS\projects\JARVIS
python simple_jarvis.py
pause

3. Save as: A:\JARVIS\start_jarvis.bat
```

### **5.2 Create Simple JARVIS Program**
```
1. Open Notepad
2. Copy this code:

import subprocess
import time

def talk_to_deepseek(message):
    """Talk to DeepSeek R1"""
    try:
        result = subprocess.run(['ollama', 'run', 'deepseek-r1', message], 
                              capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return "Sorry, I couldn't process that."

def main():
    print("🤖 JARVIS AI Assistant Started!")
    print("Type 'quit' to exit")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'quit':
            break
            
        print("🧠 JARVIS is thinking...")
        response = talk_to_deepseek(user_input)
        print(f"🤖 JARVIS: {response}")

if __name__ == "__main__":
    main()

3. Save as: A:\JARVIS\projects\JARVIS\simple_jarvis.py
```

---

## ✅ STEP 6: TEST EVERYTHING (10 minutes)

### **6.1 Test Basic Setup**
```
1. Double-click: A:\JARVIS\start_jarvis.bat
2. Type: "Hello JARVIS, can you help me?"
3. You should get a response from DeepSeek R1
```

### **6.2 Test AutoGPT**
```
1. Open Command Prompt
2. Type: cd A:\JARVIS\projects\AutoGPT
3. Type: python -m autogpt
4. Follow the setup prompts
```

---

## 🎯 WHAT YOU CAN DO NOW

### **Basic Commands to Try:**
```
"Explain cybersecurity concepts to me"
"Help me understand network security"
"What are the latest cybersecurity threats?"
"Write a Python script for password checking"
"Explain how firewalls work"
```

### **Advanced Features (Coming Soon):**
- Voice activation ("Hey JARVIS")
- Computer vision (see your screen)
- Autonomous task execution
- Integration with cybersecurity tools

---

## 🆘 TROUBLESHOOTING

### **If Ollama Won't Start:**
```
1. Open Task Manager (Ctrl+Shift+Esc)
2. End any "ollama.exe" processes
3. Open Command Prompt as Administrator
4. Type: ollama serve
```

### **If Python Packages Won't Install:**
```
1. Open Command Prompt as Administrator
2. Type: python -m pip install --upgrade pip
3. Try installing packages again
```

### **If DeepSeek Model is Slow:**
```
This is normal! The model is large and your GPU has 4GB VRAM.
First responses take 10-30 seconds, then it gets faster.
```

---

## 🚀 NEXT STEPS FOR CYBERSECURITY STUDENTS

### **Week 1: Basic Usage**
- Practice talking to JARVIS
- Ask cybersecurity questions
- Learn basic AI concepts

### **Week 2: Customization**
- Modify the simple_jarvis.py script
- Add cybersecurity-specific commands
- Integrate with your study materials

### **Week 3: Advanced Features**
- Set up voice activation
- Add computer vision capabilities
- Create automated security scanning

### **Week 4: Professional Use**
- Integrate with penetration testing tools
- Automate security report generation
- Create custom cybersecurity AI workflows

---

## 📚 LEARNING RESOURCES

### **For Cybersecurity Students:**
- Use JARVIS to explain complex security concepts
- Ask it to generate practice scenarios
- Have it help with homework and projects
- Practice Python scripting with AI assistance

### **Commands for Learning:**
```
"Explain SQL injection in simple terms"
"Generate a network security checklist"
"Help me understand encryption algorithms"
"Create a cybersecurity study plan"
"Write a script to check password strength"
```

---

## 🎯 SUCCESS CRITERIA

**You'll know it's working when:**
- ✅ You can start JARVIS with the .bat file
- ✅ DeepSeek R1 responds to your questions
- ✅ AutoGPT can run autonomous tasks
- ✅ Everything is stored on your A: drive
- ✅ You can ask cybersecurity questions and get helpful answers

**This setup gives you a powerful AI assistant perfect for cybersecurity learning and eventually professional use!** 🚀

---

**Total Setup Time: 2-3 hours**  
**Difficulty: Beginner-friendly**  
**Perfect for: Cybersecurity students who want AI assistance**

