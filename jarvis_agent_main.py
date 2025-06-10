#!/usr/bin/env python3
"""
Enhanced Local Autonomous AI Agent with Jarvis-like Computer Control
This is the main application that integrates DeepSeek R1, Blackbox code generator,
system control, and voice interaction capabilities.
"""

import os
import sys
import time
import threading
import json
import logging
from typing import Dict, List, Optional, Union, Tuple, Callable
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog, Menu, messagebox

# Import our custom modules
try:
    from deepseek_integration import DeepSeekIntegration, AgentSystem
    from blackbox_integration import BlackboxIntegration
    from system_control import SystemControl, JarvisAssistant
    from voice_control import VoiceAssistant
except ImportError as e:
    print(f"Error importing custom modules: {e}")
    print("Please ensure all required modules are in the same directory.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("jarvis_agent.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("JarvisAgent")

class JarvisAgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis - Local Autonomous AI Agent")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set theme colors (Dark theme inspired by Iron Man's Jarvis)
        self.bg_color = "#0A0A0A"
        self.text_bg = "#1A1A1A"
        self.text_fg = "#00D4FF"
        self.accent_color = "#00A8CC"
        self.warning_color = "#FFB000"
        self.error_color = "#FF4444"
        self.success_color = "#00FF88"
        
        self.root.configure(bg=self.bg_color)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Initialize components
        self.initialize_components()
        
        # Create GUI elements
        self.create_menu_bar()
        self.create_main_interface()
        self.create_status_bar()
        
        # Initialize state
        self.is_voice_enabled = True
        self.is_listening = False
        self.current_task = None
        self.conversation_history = []
        
        # Start the agent
        self.start_agent()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def configure_styles(self):
        """Configure ttk styles for the dark theme"""
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TButton', 
                           background=self.accent_color, 
                           foreground='black',
                           font=('Helvetica', 10))
        self.style.map('TButton', 
                      background=[('active', '#0088AA'),
                                ('pressed', '#006688')])
        
        self.style.configure('TLabel', 
                           background=self.bg_color, 
                           foreground=self.text_fg,
                           font=('Helvetica', 10))
        
        self.style.configure('Title.TLabel', 
                           background=self.bg_color, 
                           foreground=self.text_fg,
                           font=('Helvetica', 14, 'bold'))
        
        self.style.configure('Status.TLabel', 
                           background=self.bg_color, 
                           foreground=self.success_color,
                           font=('Helvetica', 9))

    def initialize_components(self):
        """Initialize all the AI and system control components"""
        try:
            # Initialize DeepSeek integration
            self.deepseek = DeepSeekIntegration()
            self.agent_system = AgentSystem()
            
            # Initialize Blackbox integration
            self.blackbox = BlackboxIntegration()
            
            # Initialize system control
            self.system_control = SystemControl(safety_mode=True)
            
            # Initialize voice assistant
            self.voice_assistant = VoiceAssistant(name="Jarvis", use_wake_word=True)
            self.voice_assistant.set_command_callback(self.process_voice_command)
            
            # Initialize Jarvis assistant (combines system control and voice)
            self.jarvis = JarvisAssistant(use_voice=True, safety_mode=True)
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            messagebox.showerror("Initialization Error", 
                               f"Failed to initialize AI components:\n{e}\n\nPlease check your setup.")

    def create_menu_bar(self):
        """Create the application menu bar"""
        menu_bar = Menu(self.root, bg=self.bg_color, fg=self.text_fg)
        self.root.config(menu=menu_bar)
        
        # File menu
        file_menu = Menu(menu_bar, tearoff=0, bg=self.text_bg, fg=self.text_fg)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Chat", command=self.save_chat)
        file_menu.add_command(label="Load Chat", command=self.load_chat)
        file_menu.add_command(label="Clear Chat", command=self.clear_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Export System Report", command=self.export_system_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Agent menu
        agent_menu = Menu(menu_bar, tearoff=0, bg=self.text_bg, fg=self.text_fg)
        menu_bar.add_cascade(label="Agent", menu=agent_menu)
        agent_menu.add_command(label="Model Settings", command=self.show_model_settings)
        agent_menu.add_command(label="Voice Settings", command=self.show_voice_settings)
        agent_menu.add_command(label="System Control Settings", command=self.show_system_settings)
        agent_menu.add_separator()
        agent_menu.add_command(label="Start Voice Control", command=self.start_voice_control)
        agent_menu.add_command(label="Stop Voice Control", command=self.stop_voice_control)
        
        # Tools menu
        tools_menu = Menu(menu_bar, tearoff=0, bg=self.text_bg, fg=self.text_fg)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Code Generator", command=self.open_code_generator)
        tools_menu.add_command(label="System Monitor", command=self.open_system_monitor)
        tools_menu.add_command(label="File Manager", command=self.open_file_manager)
        tools_menu.add_command(label="Screenshot Tool", command=self.take_screenshot)
        tools_menu.add_separator()
        tools_menu.add_command(label="Test Voice Recognition", command=self.test_voice_recognition)
        tools_menu.add_command(label="Test System Control", command=self.test_system_control)
        
        # Help menu
        help_menu = Menu(menu_bar, tearoff=0, bg=self.text_bg, fg=self.text_fg)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        help_menu.add_command(label="Voice Commands", command=self.show_voice_commands)
        help_menu.add_command(label="System Requirements", command=self.show_system_requirements)
        help_menu.add_separator()
        help_menu.add_command(label="About Jarvis", command=self.show_about)

    def create_main_interface(self):
        """Create the main interface"""
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left panel (chat and controls)
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Create right panel (system info and tools)
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        right_panel.configure(width=300)
        
        # Create chat area in left panel
        self.create_chat_area(left_panel)
        
        # Create input area in left panel
        self.create_input_area(left_panel)
        
        # Create control panel in left panel
        self.create_control_panel(left_panel)
        
        # Create system info panel in right panel
        self.create_system_info_panel(right_panel)
        
        # Create tools panel in right panel
        self.create_tools_panel(right_panel)

    def create_chat_area(self, parent):
        """Create the chat display area"""
        # Chat frame with title
        chat_frame = ttk.Frame(parent)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Title
        title_label = ttk.Label(chat_frame, text="Jarvis AI Assistant", style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            bg=self.text_bg, 
            fg=self.text_fg,
            font=("Consolas", 11),
            insertbackground=self.text_fg,
            selectbackground=self.accent_color
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure tags for different message types
        self.chat_display.tag_configure("user", foreground=self.success_color, font=("Consolas", 11, "bold"))
        self.chat_display.tag_configure("jarvis", foreground=self.text_fg, font=("Consolas", 11))
        self.chat_display.tag_configure("system", foreground=self.warning_color, font=("Consolas", 11, "italic"))
        self.chat_display.tag_configure("error", foreground=self.error_color, font=("Consolas", 11, "bold"))
        self.chat_display.tag_configure("success", foreground=self.success_color, font=("Consolas", 11))
        self.chat_display.tag_configure("timestamp", foreground="#666666", font=("Consolas", 9))

    def create_input_area(self, parent):
        """Create the user input area"""
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Input field
        self.input_field = scrolledtext.ScrolledText(
            input_frame, 
            height=4, 
            wrap=tk.WORD, 
            bg=self.text_bg, 
            fg=self.text_fg,
            font=("Consolas", 11),
            insertbackground=self.text_fg,
            selectbackground=self.accent_color
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_field.bind("<Control-Return>", self.on_send_message)
        self.input_field.bind("<Shift-Return>", lambda e: None)  # Allow Shift+Enter for new line
        
        # Button frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Send button
        self.send_button = ttk.Button(
            button_frame, 
            text="Send\n(Ctrl+Enter)", 
            command=self.send_message
        )
        self.send_button.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Voice button
        self.voice_button = ttk.Button(
            button_frame, 
            text="🎤 Voice", 
            command=self.toggle_voice_listening
        )
        self.voice_button.pack(fill=tk.X)

    def create_control_panel(self, parent):
        """Create the control panel"""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        ttk.Label(control_frame, text="Quick Controls", style='Title.TLabel').pack(anchor=tk.W)
        
        # Button grid
        button_grid = ttk.Frame(control_frame)
        button_grid.pack(fill=tk.X, pady=5)
        
        # Row 1
        ttk.Button(button_grid, text="Take Screenshot", 
                  command=self.take_screenshot).grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        ttk.Button(button_grid, text="System Info", 
                  command=self.show_system_info).grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        ttk.Button(button_grid, text="Open Calculator", 
                  command=self.open_calculator).grid(row=0, column=2, padx=2, pady=2, sticky="ew")
        
        # Row 2
        ttk.Button(button_grid, text="Open Notepad", 
                  command=self.open_notepad).grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        ttk.Button(button_grid, text="File Explorer", 
                  command=self.open_file_explorer).grid(row=1, column=1, padx=2, pady=2, sticky="ew")
        ttk.Button(button_grid, text="Task Manager", 
                  command=self.open_task_manager).grid(row=1, column=2, padx=2, pady=2, sticky="ew")
        
        # Configure grid weights
        for i in range(3):
            button_grid.columnconfigure(i, weight=1)

    def create_system_info_panel(self, parent):
        """Create the system information panel"""
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        ttk.Label(info_frame, text="System Status", style='Title.TLabel').pack(anchor=tk.W)
        
        # System info display
        self.system_info_text = scrolledtext.ScrolledText(
            info_frame,
            height=12,
            width=35,
            wrap=tk.WORD,
            bg=self.text_bg,
            fg=self.text_fg,
            font=("Consolas", 9),
            state=tk.DISABLED
        )
        self.system_info_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Refresh button
        ttk.Button(info_frame, text="Refresh", command=self.update_system_info).pack(fill=tk.X)
        
        # Start automatic updates
        self.update_system_info()
        self.schedule_system_update()

    def create_tools_panel(self, parent):
        """Create the tools panel"""
        tools_frame = ttk.Frame(parent)
        tools_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(tools_frame, text="AI Tools", style='Title.TLabel').pack(anchor=tk.W)
        
        # Tools list
        tools_list_frame = ttk.Frame(tools_frame)
        tools_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Tool buttons
        tools = [
            ("🤖 Code Generator", self.open_code_generator),
            ("📊 System Monitor", self.open_system_monitor),
            ("📁 File Manager", self.open_file_manager),
            ("🎤 Voice Test", self.test_voice_recognition),
            ("⚙️ System Control", self.test_system_control),
            ("📸 Screenshot", self.take_screenshot),
            ("🌐 Open Browser", self.open_browser),
            ("📝 Open Editor", self.open_text_editor)
        ]
        
        for i, (text, command) in enumerate(tools):
            btn = ttk.Button(tools_list_frame, text=text, command=command)
            btn.pack(fill=tk.X, pady=2)

    def create_status_bar(self):
        """Create the status bar at the bottom"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        # Connection status
        self.connection_status = ttk.Label(
            self.status_frame, 
            text="Initializing...",
            style='Status.TLabel'
        )
        self.connection_status.pack(side=tk.LEFT)
        
        # Voice status
        self.voice_status = ttk.Label(
            self.status_frame, 
            text="Voice: Ready",
            style='Status.TLabel'
        )
        self.voice_status.pack(side=tk.LEFT, padx=(20, 0))
        
        # Model info
        self.model_info = ttk.Label(
            self.status_frame, 
            text="Model: DeepSeek R1",
            style='Status.TLabel'
        )
        self.model_info.pack(side=tk.RIGHT)

    def start_agent(self):
        """Start the Jarvis agent"""
        try:
            # Initialize the agent system
            if self.agent_system.initialize():
                self.connection_status.config(text="✅ DeepSeek R1: Connected")
                
                # Start voice assistant
                if self.is_voice_enabled:
                    self.voice_assistant.start()
                    self.voice_status.config(text="🎤 Voice: Active")
                
                # Add welcome message
                welcome_msg = """🤖 Jarvis AI Assistant is now online!

I'm your personal AI assistant with advanced capabilities:
• Natural language conversation powered by DeepSeek R1
• Voice recognition and speech synthesis
• Complete computer control (mouse, keyboard, applications)
• Code generation with Blackbox AI
• System monitoring and automation
• File management and screenshot tools

You can interact with me through:
• Text chat (type your message and press Ctrl+Enter)
• Voice commands (click the Voice button or say "Hey Jarvis")
• Quick control buttons for common tasks

Try saying "Hey Jarvis, what can you do?" or type a command below!"""
                
                self.add_message("system", welcome_msg)
                
                # Start Jarvis assistant
                self.jarvis.start()
                
                logger.info("Jarvis agent started successfully")
                
            else:
                self.connection_status.config(text="❌ DeepSeek R1: Failed to connect")
                self.add_message("error", "Failed to connect to DeepSeek R1. Please check your Ollama installation.")
                
        except Exception as e:
            logger.error(f"Failed to start agent: {e}")
            self.connection_status.config(text="❌ Agent: Error")
            self.add_message("error", f"Failed to start Jarvis agent: {e}")

    def add_message(self, sender: str, message: str):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = time.strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add sender and message with appropriate tag
        if sender == "user":
            self.chat_display.insert(tk.END, "You: ", "user")
            self.chat_display.insert(tk.END, f"{message}\n\n", "user")
        elif sender == "jarvis":
            self.chat_display.insert(tk.END, "Jarvis: ", "jarvis")
            self.chat_display.insert(tk.END, f"{message}\n\n", "jarvis")
        elif sender == "error":
            self.chat_display.insert(tk.END, "Error: ", "error")
            self.chat_display.insert(tk.END, f"{message}\n\n", "error")
        elif sender == "success":
            self.chat_display.insert(tk.END, "Success: ", "success")
            self.chat_display.insert(tk.END, f"{message}\n\n", "success")
        else:
            self.chat_display.insert(tk.END, "System: ", "system")
            self.chat_display.insert(tk.END, f"{message}\n\n", "system")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Store in conversation history
        self.conversation_history.append({
            "timestamp": timestamp,
            "sender": sender,
            "message": message
        })

    def send_message(self):
        """Send user message to the AI"""
        message = self.input_field.get("1.0", tk.END).strip()
        if not message:
            return
        
        # Clear input field
        self.input_field.delete("1.0", tk.END)
        
        # Add user message to chat
        self.add_message("user", message)
        
        # Process message in a separate thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()

    def on_send_message(self, event):
        """Handle Ctrl+Enter key press in the input field"""
        self.send_message()
        return "break"  # Prevent default behavior

    def process_message(self, message: str):
        """Process user message and get AI response"""
        try:
            # Check if it's a system command
            if message.lower().startswith("/"):
                response = self.process_system_command(message[1:])
                if response:
                    self.add_message("system", response)
                return
            
            # Process with the agent system
            def response_callback(chunk):
                # This would be used for streaming responses
                pass
            
            response = self.agent_system.process_request(message)
            
            if response:
                self.add_message("jarvis", response)
                
                # Speak the response if voice is enabled
                if self.is_voice_enabled and hasattr(self, 'voice_assistant'):
                    self.voice_assistant.say(response)
            else:
                self.add_message("error", "I'm having trouble processing your request. Please try again.")
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            self.add_message("error", f"Error processing message: {str(e)}")

    def process_system_command(self, command: str) -> str:
        """Process system commands (commands starting with /)"""
        command = command.lower().strip()
        
        if command == "help":
            return """Available system commands:
/help - Show this help message
/status - Show system status
/screenshot - Take a screenshot
/clear - Clear chat history
/voice on/off - Enable/disable voice
/restart - Restart the agent
/quit - Exit the application"""
        
        elif command == "status":
            cpu = self.system_control.get_cpu_usage()
            memory = self.system_control.get_memory_usage()
            return f"System Status:\nCPU: {cpu:.1f}%\nMemory: {memory['percent']:.1f}%\nAgent: Running\nVoice: {'Enabled' if self.is_voice_enabled else 'Disabled'}"
        
        elif command == "screenshot":
            self.take_screenshot()
            return "Screenshot taken and saved to Pictures folder."
        
        elif command == "clear":
            self.clear_chat()
            return "Chat history cleared."
        
        elif command.startswith("voice "):
            setting = command.split(" ", 1)[1]
            if setting == "on":
                self.start_voice_control()
                return "Voice control enabled."
            elif setting == "off":
                self.stop_voice_control()
                return "Voice control disabled."
            else:
                return "Usage: /voice on or /voice off"
        
        elif command == "restart":
            self.restart_agent()
            return "Agent restarted."
        
        elif command == "quit":
            self.on_closing()
            return "Goodbye!"
        
        else:
            return f"Unknown command: /{command}. Type /help for available commands."

    def process_voice_command(self, command: str) -> str:
        """Process voice commands"""
        # Remove wake words
        command = command.lower()
        for wake_word in ["jarvis", "hey jarvis", "hey"]:
            command = command.replace(wake_word, "").strip()
        
        if not command:
            return "Yes, how can I help you?"
        
        # Process the command through the normal message processing
        threading.Thread(target=self.process_message, args=(command,), daemon=True).start()
        
        return "Processing your request..."

    def toggle_voice_listening(self):
        """Toggle voice listening on/off"""
        if self.is_listening:
            self.stop_voice_listening()
        else:
            self.start_voice_listening()

    def start_voice_listening(self):
        """Start listening for voice commands"""
        if not self.is_voice_enabled:
            self.add_message("system", "Voice control is disabled. Enable it in the Agent menu.")
            return
        
        try:
            self.voice_assistant.start_listening()
            self.is_listening = True
            self.voice_button.config(text="🔴 Stop")
            self.voice_status.config(text="🎤 Voice: Listening...")
            self.add_message("system", "Voice listening started. Speak your command.")
            
        except Exception as e:
            logger.error(f"Failed to start voice listening: {e}")
            self.add_message("error", f"Failed to start voice listening: {e}")

    def stop_voice_listening(self):
        """Stop listening for voice commands"""
        try:
            self.voice_assistant.stop_listening()
            self.is_listening = False
            self.voice_button.config(text="🎤 Voice")
            self.voice_status.config(text="🎤 Voice: Ready")
            self.add_message("system", "Voice listening stopped.")
            
        except Exception as e:
            logger.error(f"Failed to stop voice listening: {e}")
            self.add_message("error", f"Failed to stop voice listening: {e}")

    def start_voice_control(self):
        """Start voice control"""
        try:
            if not self.is_voice_enabled:
                self.voice_assistant.start()
                self.is_voice_enabled = True
                self.voice_status.config(text="🎤 Voice: Active")
                self.add_message("success", "Voice control started.")
            else:
                self.add_message("system", "Voice control is already active.")
                
        except Exception as e:
            logger.error(f"Failed to start voice control: {e}")
            self.add_message("error", f"Failed to start voice control: {e}")

    def stop_voice_control(self):
        """Stop voice control"""
        try:
            if self.is_voice_enabled:
                self.voice_assistant.stop()
                self.is_voice_enabled = False
                self.is_listening = False
                self.voice_button.config(text="🎤 Voice")
                self.voice_status.config(text="🎤 Voice: Disabled")
                self.add_message("system", "Voice control stopped.")
            else:
                self.add_message("system", "Voice control is already disabled.")
                
        except Exception as e:
            logger.error(f"Failed to stop voice control: {e}")
            self.add_message("error", f"Failed to stop voice control: {e}")

    def update_system_info(self):
        """Update the system information display"""
        try:
            # Get system information
            cpu = self.system_control.get_cpu_usage()
            memory = self.system_control.get_memory_usage()
            disk = self.system_control.get_disk_usage()
            battery = self.system_control.get_battery_status()
            
            # Format the information
            info_text = f"""CPU Usage: {cpu:.1f}%
Memory: {memory['percent']:.1f}%
  Used: {memory['used'] / (1024**3):.1f} GB
  Total: {memory['total'] / (1024**3):.1f} GB

Disk Usage: {disk['percent']:.1f}%
  Used: {disk['used'] / (1024**3):.1f} GB
  Free: {disk['free'] / (1024**3):.1f} GB

"""
            
            if battery:
                status = "Charging" if battery['power_plugged'] else "Discharging"
                info_text += f"Battery: {battery['percent']}% ({status})\n"
            else:
                info_text += "Battery: Not available\n"
            
            # Get running processes count
            processes = self.system_control.get_running_processes()
            info_text += f"\nRunning Processes: {len(processes)}"
            
            # Update the display
            self.system_info_text.config(state=tk.NORMAL)
            self.system_info_text.delete("1.0", tk.END)
            self.system_info_text.insert("1.0", info_text)
            self.system_info_text.config(state=tk.DISABLED)
            
        except Exception as e:
            logger.error(f"Failed to update system info: {e}")

    def schedule_system_update(self):
        """Schedule the next system info update"""
        # Update every 5 seconds
        self.root.after(5000, lambda: (self.update_system_info(), self.schedule_system_update()))

    def restart_agent(self):
        """Restart the agent"""
        try:
            self.add_message("system", "Restarting agent...")
            
            # Stop current components
            if self.is_voice_enabled:
                self.voice_assistant.stop()
            
            # Reinitialize components
            self.initialize_components()
            
            # Restart agent
            self.start_agent()
            
            self.add_message("success", "Agent restarted successfully.")
            
        except Exception as e:
            logger.error(f"Failed to restart agent: {e}")
            self.add_message("error", f"Failed to restart agent: {e}")

    # Tool functions
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"jarvis_screenshot_{timestamp}.png"
            home_dir = os.path.expanduser("~")
            save_path = os.path.join(home_dir, "Pictures", filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            screenshot = self.system_control.take_screenshot(save_path=save_path)
            if screenshot:
                self.add_message("success", f"Screenshot saved to {save_path}")
            else:
                self.add_message("error", "Failed to take screenshot")
                
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            self.add_message("error", f"Failed to take screenshot: {e}")

    def open_calculator(self):
        """Open calculator"""
        try:
            if self.system_control.os_type == 'Windows':
                self.system_control.execute_command("calc")
            else:
                self.system_control.execute_command("gnome-calculator")
            self.add_message("success", "Calculator opened")
        except Exception as e:
            self.add_message("error", f"Failed to open calculator: {e}")

    def open_notepad(self):
        """Open notepad/text editor"""
        try:
            if self.system_control.os_type == 'Windows':
                self.system_control.execute_command("notepad")
            else:
                self.system_control.execute_command("gedit")
            self.add_message("success", "Text editor opened")
        except Exception as e:
            self.add_message("error", f"Failed to open text editor: {e}")

    def open_file_explorer(self):
        """Open file explorer"""
        try:
            if self.system_control.os_type == 'Windows':
                self.system_control.execute_command("explorer")
            else:
                self.system_control.execute_command("nautilus")
            self.add_message("success", "File explorer opened")
        except Exception as e:
            self.add_message("error", f"Failed to open file explorer: {e}")

    def open_task_manager(self):
        """Open task manager"""
        try:
            if self.system_control.os_type == 'Windows':
                self.system_control.execute_command("taskmgr")
            else:
                self.system_control.execute_command("gnome-system-monitor")
            self.add_message("success", "Task manager opened")
        except Exception as e:
            self.add_message("error", f"Failed to open task manager: {e}")

    def open_browser(self):
        """Open web browser"""
        try:
            self.system_control.open_url("https://www.google.com")
            self.add_message("success", "Web browser opened")
        except Exception as e:
            self.add_message("error", f"Failed to open browser: {e}")

    def open_text_editor(self):
        """Open text editor"""
        self.open_notepad()

    # Dialog functions (placeholders for now)
    def show_model_settings(self):
        """Show model settings dialog"""
        messagebox.showinfo("Model Settings", "Model settings dialog will be implemented here.")

    def show_voice_settings(self):
        """Show voice settings dialog"""
        messagebox.showinfo("Voice Settings", "Voice settings dialog will be implemented here.")

    def show_system_settings(self):
        """Show system settings dialog"""
        messagebox.showinfo("System Settings", "System settings dialog will be implemented here.")

    def open_code_generator(self):
        """Open code generator tool"""
        messagebox.showinfo("Code Generator", "Code generator tool will be implemented here.")

    def open_system_monitor(self):
        """Open system monitor tool"""
        messagebox.showinfo("System Monitor", "System monitor tool will be implemented here.")

    def open_file_manager(self):
        """Open file manager tool"""
        messagebox.showinfo("File Manager", "File manager tool will be implemented here.")

    def test_voice_recognition(self):
        """Test voice recognition"""
        try:
            self.add_message("system", "Voice recognition test started. Please speak...")
            
            def test_callback():
                text = self.voice_assistant.listen_once(timeout=5)
                if text:
                    self.add_message("success", f"Voice recognition test successful! You said: '{text}'")
                else:
                    self.add_message("error", "Voice recognition test failed. No speech detected.")
            
            threading.Thread(target=test_callback, daemon=True).start()
            
        except Exception as e:
            self.add_message("error", f"Voice recognition test failed: {e}")

    def test_system_control(self):
        """Test system control"""
        try:
            # Get mouse position as a simple test
            x, y = self.system_control.get_mouse_position()
            self.add_message("success", f"System control test successful! Mouse position: ({x}, {y})")
        except Exception as e:
            self.add_message("error", f"System control test failed: {e}")

    def show_system_info(self):
        """Show detailed system information"""
        try:
            info = self.system_control.get_system_info()
            cpu = self.system_control.get_cpu_usage()
            memory = self.system_control.get_memory_usage()
            
            info_text = f"""System Information:
OS: {info['system']} {info['release']}
Machine: {info['machine']}
Processor: {info['processor']}
Python: {info['python_version']}

Current Usage:
CPU: {cpu:.1f}%
Memory: {memory['percent']:.1f}%"""
            
            self.add_message("system", info_text)
            
        except Exception as e:
            self.add_message("error", f"Failed to get system info: {e}")

    # File operations
    def save_chat(self):
        """Save chat history to file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
            )
            if file_path:
                if file_path.endswith('.json'):
                    with open(file_path, "w", encoding="utf-8") as file:
                        json.dump(self.conversation_history, file, indent=2, ensure_ascii=False)
                else:
                    with open(file_path, "w", encoding="utf-8") as file:
                        for entry in self.conversation_history:
                            file.write(f"[{entry['timestamp']}] {entry['sender']}: {entry['message']}\n\n")
                
                self.add_message("success", f"Chat history saved to {file_path}")
        except Exception as e:
            self.add_message("error", f"Failed to save chat: {e}")

    def load_chat(self):
        """Load chat history from file"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                if file_path.endswith('.json'):
                    with open(file_path, "r", encoding="utf-8") as file:
                        self.conversation_history = json.load(file)
                    
                    # Rebuild chat display
                    self.chat_display.config(state=tk.NORMAL)
                    self.chat_display.delete("1.0", tk.END)
                    self.chat_display.config(state=tk.DISABLED)
                    
                    for entry in self.conversation_history:
                        self.add_message(entry['sender'], entry['message'])
                    
                    self.add_message("success", f"Chat history loaded from {file_path}")
                else:
                    self.add_message("error", "Only JSON files are supported for loading chat history.")
        except Exception as e:
            self.add_message("error", f"Failed to load chat: {e}")

    def clear_chat(self):
        """Clear chat history"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.conversation_history.clear()
        self.add_message("system", "Chat history cleared.")

    def export_system_report(self):
        """Export a comprehensive system report"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                # Generate comprehensive system report
                report = self.generate_system_report()
                
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(report)
                
                self.add_message("success", f"System report exported to {file_path}")
        except Exception as e:
            self.add_message("error", f"Failed to export system report: {e}")

    def generate_system_report(self) -> str:
        """Generate a comprehensive system report"""
        try:
            # Get system information
            sys_info = self.system_control.get_system_info()
            cpu = self.system_control.get_cpu_usage()
            memory = self.system_control.get_memory_usage()
            disk = self.system_control.get_disk_usage()
            battery = self.system_control.get_battery_status()
            processes = self.system_control.get_running_processes()
            
            # Generate report
            report = f"""JARVIS AI ASSISTANT - SYSTEM REPORT
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

SYSTEM INFORMATION:
OS: {sys_info['system']} {sys_info['release']}
Version: {sys_info['version']}
Machine: {sys_info['machine']}
Processor: {sys_info['processor']}
Python Version: {sys_info['python_version']}

CURRENT SYSTEM USAGE:
CPU Usage: {cpu:.1f}%
Memory Usage: {memory['percent']:.1f}%
  Total Memory: {memory['total'] / (1024**3):.2f} GB
  Used Memory: {memory['used'] / (1024**3):.2f} GB
  Available Memory: {memory['available'] / (1024**3):.2f} GB

Disk Usage: {disk['percent']:.1f}%
  Total Disk: {disk['total'] / (1024**3):.2f} GB
  Used Disk: {disk['used'] / (1024**3):.2f} GB
  Free Disk: {disk['free'] / (1024**3):.2f} GB

"""
            
            if battery:
                status = "Charging" if battery['power_plugged'] else "Discharging"
                report += f"Battery: {battery['percent']}% ({status})\n"
            else:
                report += "Battery: Not available\n"
            
            report += f"\nRUNNING PROCESSES: {len(processes)} total\n"
            
            # Add top 10 processes by CPU usage
            top_processes = sorted(processes, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:10]
            report += "\nTOP 10 PROCESSES BY CPU USAGE:\n"
            for proc in top_processes:
                report += f"  {proc['name']} (PID: {proc['pid']}) - CPU: {proc.get('cpu_percent', 0):.1f}%\n"
            
            report += f"\nJARVIS AGENT STATUS:\n"
            report += f"DeepSeek R1: {'Connected' if self.deepseek.is_available else 'Disconnected'}\n"
            report += f"Voice Control: {'Enabled' if self.is_voice_enabled else 'Disabled'}\n"
            report += f"Voice Listening: {'Active' if self.is_listening else 'Inactive'}\n"
            report += f"Blackbox Integration: {'Available' if self.blackbox.is_installed else 'Not Available'}\n"
            
            report += f"\nCONVERSATION HISTORY: {len(self.conversation_history)} messages\n"
            
            return report
            
        except Exception as e:
            return f"Error generating system report: {e}"

    # Help and info dialogs
    def show_user_guide(self):
        """Show user guide"""
        guide_text = """JARVIS AI ASSISTANT - USER GUIDE

GETTING STARTED:
1. Type messages in the input field and press Ctrl+Enter to send
2. Click the Voice button to start voice commands
3. Use quick control buttons for common tasks
4. Monitor system status in the right panel

VOICE COMMANDS:
- Say "Hey Jarvis" followed by your command
- Examples: "Hey Jarvis, take a screenshot"
- "Hey Jarvis, what's my CPU usage?"
- "Hey Jarvis, open calculator"

TEXT COMMANDS:
- Type naturally: "Take a screenshot"
- System commands start with /: "/help", "/status"
- Ask questions: "What can you do?"

FEATURES:
- Natural language conversation
- Voice recognition and speech synthesis
- Complete computer control
- System monitoring
- File management
- Code generation (with Blackbox AI)
- Screenshot tools
- Application launching

KEYBOARD SHORTCUTS:
- Ctrl+Enter: Send message
- Shift+Enter: New line in input field

For more help, visit the documentation or ask Jarvis directly!"""
        
        messagebox.showinfo("User Guide", guide_text)

    def show_voice_commands(self):
        """Show voice commands help"""
        commands_text = """JARVIS VOICE COMMANDS

WAKE WORDS:
- "Hey Jarvis"
- "Jarvis"

SYSTEM COMMANDS:
- "Take a screenshot"
- "What's my CPU usage?"
- "What's my memory usage?"
- "Show system information"
- "Open calculator"
- "Open notepad"
- "Open file explorer"
- "Open task manager"
- "Open browser"

CONTROL COMMANDS:
- "Click here" (clicks current mouse position)
- "Right click"
- "Double click"
- "Scroll up/down"
- "Type [text]"

VOICE CONTROL:
- "Stop listening"
- "Start listening"

GENERAL:
- "What can you do?"
- "Help"
- "Goodbye"

You can also ask questions or give instructions in natural language!"""
        
        messagebox.showinfo("Voice Commands", commands_text)

    def show_system_requirements(self):
        """Show system requirements"""
        requirements_text = """JARVIS AI ASSISTANT - SYSTEM REQUIREMENTS

MINIMUM REQUIREMENTS:
- Windows 10/11 with WSL2 Ubuntu
- 8 GB RAM (16 GB recommended)
- 10 GB free disk space
- Microphone for voice commands
- Speakers/headphones for voice responses

SOFTWARE REQUIREMENTS:
- Python 3.8 or higher
- Ollama with DeepSeek R1 model
- VS Code with Blackbox extension
- Required Python packages (see requirements.txt)

RECOMMENDED HARDWARE:
- 16 GB RAM or more
- SSD storage
- Dedicated GPU (for faster AI processing)
- Good quality microphone
- External speakers

NETWORK:
- Internet connection for initial setup
- Local network access for Ollama API

PERMISSIONS:
- Microphone access
- System control permissions
- File system access

For detailed setup instructions, see the README.md file."""
        
        messagebox.showinfo("System Requirements", requirements_text)

    def show_about(self):
        """Show about dialog"""
        about_text = """JARVIS - LOCAL AUTONOMOUS AI ASSISTANT

Version: 1.0.0
Created: 2025

DESCRIPTION:
Jarvis is a local autonomous AI assistant inspired by the AI from Iron Man. 
It combines the power of DeepSeek R1 language model with advanced computer 
control capabilities, voice recognition, and system automation.

FEATURES:
✓ Natural language conversation
✓ Voice recognition and synthesis
✓ Complete computer control
✓ System monitoring and automation
✓ Code generation with Blackbox AI
✓ File management tools
✓ Screenshot and screen capture
✓ Application launching and control

TECHNOLOGY STACK:
- DeepSeek R1 (via Ollama)
- Python with Tkinter GUI
- PyAutoGUI for system control
- SpeechRecognition for voice input
- pyttsx3 for text-to-speech
- psutil for system monitoring
- Blackbox AI for code generation

PRIVACY:
All processing happens locally on your machine. 
No data is sent to external servers except for 
voice recognition (Google Speech API).

© 2025 - Built with ❤️ for AI enthusiasts"""
        
        messagebox.showinfo("About Jarvis", about_text)

    def on_closing(self):
        """Handle application closing"""
        try:
            # Stop voice control
            if self.is_voice_enabled:
                self.voice_assistant.stop()
            
            # Stop Jarvis assistant
            if hasattr(self, 'jarvis'):
                self.jarvis.stop()
            
            # Stop system control
            if hasattr(self, 'system_control'):
                pass  # SystemControl doesn't need explicit stopping
            
            logger.info("Jarvis agent shutting down")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
        
        finally:
            self.root.destroy()

def main():
    """Main function to start the Jarvis AI Assistant"""
    # Create the main window
    root = tk.Tk()
    
    # Create the application
    app = JarvisAgentGUI(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()

