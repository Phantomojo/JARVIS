#!/usr/bin/env python3
"""
Local Autonomous AI Agent - Basic Implementation
This script demonstrates the integration of DeepSeek R1 with Ollama and a simple Tkinter interface.
"""

import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog, Menu
import threading
import json
import requests
import os
import sys
import time

class AutoAgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Local Autonomous AI Agent")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set theme colors
        self.bg_color = "#2E3440"
        self.text_bg = "#3B4252"
        self.text_fg = "#ECEFF4"
        self.accent_color = "#88C0D0"
        self.root.configure(bg=self.bg_color)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TButton', background=self.accent_color, foreground='black')
        self.style.map('TButton', background=[('active', '#81A1C1')])
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create chat area
        self.create_chat_area()
        
        # Create input area
        self.create_input_area()
        
        # Create status bar
        self.create_status_bar()
        
        # Initialize Ollama connection
        self.model_name = "deepseek-r1:8b"  # Default model
        self.ollama_url = "http://localhost:11434/api/generate"
        self.is_connected = False
        self.check_ollama_connection()
        
        # Initialize task system
        self.tasks = []
        self.current_task = None
        
        # Add welcome message
        self.add_message("system", "Welcome to Local Autonomous AI Agent. I'm powered by DeepSeek R1 running locally on your machine. How can I assist you today?")

    def create_menu_bar(self):
        """Create the application menu bar"""
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        
        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Chat", command=self.save_chat)
        file_menu.add_command(label="Clear Chat", command=self.clear_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Settings menu
        settings_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Model Settings", command=self.show_model_settings)
        settings_menu.add_command(label="Preferences", command=self.show_preferences)
        
        # Tools menu
        tools_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Code Generator", command=self.open_code_generator)
        tools_menu.add_command(label="File Browser", command=self.open_file_browser)
        
        # Help menu
        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_documentation)

    def create_chat_area(self):
        """Create the chat display area"""
        # Create chat frame
        chat_frame = ttk.Frame(self.main_frame)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            bg=self.text_bg, 
            fg=self.text_fg,
            font=("Helvetica", 10)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure tags for different message types
        self.chat_display.tag_configure("user", foreground="#A3BE8C", font=("Helvetica", 10, "bold"))
        self.chat_display.tag_configure("assistant", foreground="#88C0D0", font=("Helvetica", 10))
        self.chat_display.tag_configure("system", foreground="#B48EAD", font=("Helvetica", 10, "italic"))
        self.chat_display.tag_configure("error", foreground="#BF616A", font=("Helvetica", 10, "bold"))

    def create_input_area(self):
        """Create the user input area"""
        # Create input frame
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create input field
        self.input_field = scrolledtext.ScrolledText(
            input_frame, 
            height=4, 
            wrap=tk.WORD, 
            bg=self.text_bg, 
            fg=self.text_fg,
            font=("Helvetica", 10)
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", self.on_enter_pressed)
        self.input_field.bind("<Shift-Return>", lambda e: None)  # Allow Shift+Enter for new line
        
        # Create send button
        self.send_button = ttk.Button(
            input_frame, 
            text="Send", 
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT, padx=5)

    def create_status_bar(self):
        """Create the status bar at the bottom"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        # Connection status
        self.connection_status = ttk.Label(
            self.status_bar, 
            text="Connecting to DeepSeek R1...",
            foreground="#BF616A"
        )
        self.connection_status.pack(side=tk.LEFT)
        
        # Model info
        self.model_info = ttk.Label(
            self.status_bar, 
            text=f"Model: {self.model_name}",
            foreground=self.text_fg
        )
        self.model_info.pack(side=tk.RIGHT)

    def check_ollama_connection(self):
        """Check if Ollama is running and the model is available"""
        def check():
            try:
                response = requests.get("http://localhost:11434/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [model["name"] for model in models]
                    
                    if self.model_name.split(":")[0] in [m.split(":")[0] for m in model_names]:
                        self.is_connected = True
                        self.connection_status.config(
                            text="Connected to DeepSeek R1",
                            foreground="#A3BE8C"
                        )
                    else:
                        self.add_message("system", f"DeepSeek R1 model not found. Please run 'ollama pull {self.model_name}' in your terminal.")
                        self.connection_status.config(
                            text=f"Model {self.model_name} not found",
                            foreground="#BF616A"
                        )
                else:
                    self.add_message("error", "Failed to connect to Ollama API.")
                    self.connection_status.config(
                        text="Failed to connect to Ollama",
                        foreground="#BF616A"
                    )
            except requests.exceptions.ConnectionError:
                self.add_message("error", "Ollama is not running. Please start Ollama and try again.")
                self.connection_status.config(
                    text="Ollama not running",
                    foreground="#BF616A"
                )
        
        # Run the check in a separate thread to avoid blocking the UI
        threading.Thread(target=check, daemon=True).start()

    def add_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = time.strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "system")
        
        # Add sender and message with appropriate tag
        if sender == "user":
            self.chat_display.insert(tk.END, "You: ", "user")
        elif sender == "assistant":
            self.chat_display.insert(tk.END, "Assistant: ", "assistant")
        elif sender == "error":
            self.chat_display.insert(tk.END, "Error: ", "error")
        else:
            self.chat_display.insert(tk.END, "System: ", "system")
        
        self.chat_display.insert(tk.END, f"{message}\n\n", sender)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

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

    def on_enter_pressed(self, event):
        """Handle Enter key press in the input field"""
        if not event.state & 0x1:  # Check if Shift key is not pressed
            self.send_message()
            return "break"  # Prevent default behavior (newline)
        return None  # Allow default behavior for Shift+Enter

    def process_message(self, message):
        """Process user message and get AI response"""
        if not self.is_connected:
            self.add_message("error", "Not connected to DeepSeek R1. Please check your connection.")
            return
        
        try:
            # Prepare the request
            data = {
                "model": self.model_name,
                "prompt": message,
                "stream": False
            }
            
            # Send the request to Ollama
            response = requests.post(self.ollama_url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get("response", "No response received.")
                self.add_message("assistant", ai_response)
            else:
                self.add_message("error", f"Failed to get response: {response.status_code}")
        except Exception as e:
            self.add_message("error", f"Error processing message: {str(e)}")

    def save_chat(self):
        """Save the chat history to a file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.chat_display.get("1.0", tk.END))
                self.add_message("system", f"Chat saved to {file_path}")
            except Exception as e:
                self.add_message("error", f"Failed to save chat: {str(e)}")

    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_message("system", "Chat cleared.")

    def show_model_settings(self):
        """Show model settings dialog"""
        # Create a new top-level window
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Model Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg=self.bg_color)
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Create settings frame
        settings_frame = ttk.Frame(settings_window)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Model selection
        ttk.Label(settings_frame, text="Model:").grid(row=0, column=0, sticky=tk.W, pady=5)
        model_var = tk.StringVar(value=self.model_name)
        model_options = ["deepseek-r1:1.5b", "deepseek-r1:7b", "deepseek-r1:8b", "deepseek-r1:14b", "deepseek-r1:32b", "deepseek-r1:70b"]
        model_dropdown = ttk.Combobox(settings_frame, textvariable=model_var, values=model_options)
        model_dropdown.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Temperature setting
        ttk.Label(settings_frame, text="Temperature:").grid(row=1, column=0, sticky=tk.W, pady=5)
        temp_var = tk.DoubleVar(value=0.7)
        temp_scale = ttk.Scale(settings_frame, from_=0.1, to=1.0, variable=temp_var, orient=tk.HORIZONTAL)
        temp_scale.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        ttk.Label(settings_frame, textvariable=temp_var).grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # Max tokens setting
        ttk.Label(settings_frame, text="Max Tokens:").grid(row=2, column=0, sticky=tk.W, pady=5)
        tokens_var = tk.IntVar(value=2048)
        tokens_entry = ttk.Entry(settings_frame, textvariable=tokens_var)
        tokens_entry.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Save", command=lambda: self.save_model_settings(model_var.get(), temp_var.get(), tokens_var.get(), settings_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side=tk.LEFT, padx=5)

    def save_model_settings(self, model, temperature, max_tokens, window):
        """Save model settings and close the window"""
        self.model_name = model
        self.model_info.config(text=f"Model: {self.model_name}")
        self.add_message("system", f"Model settings updated: {model}, temp={temperature}, max_tokens={max_tokens}")
        window.destroy()
        
        # Check if the selected model is available
        self.check_ollama_connection()

    def show_preferences(self):
        """Show preferences dialog"""
        # Placeholder for preferences dialog
        self.add_message("system", "Preferences dialog not implemented yet.")

    def open_code_generator(self):
        """Open the code generator tool"""
        # Placeholder for code generator tool
        self.add_message("system", "Code generator tool not implemented yet.")

    def open_file_browser(self):
        """Open the file browser tool"""
        # Placeholder for file browser tool
        self.add_message("system", "File browser tool not implemented yet.")

    def show_about(self):
        """Show about dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("400x300")
        about_window.configure(bg=self.bg_color)
        about_window.transient(self.root)
        about_window.grab_set()
        
        about_frame = ttk.Frame(about_window)
        about_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(about_frame, text="Local Autonomous AI Agent", font=("Helvetica", 14, "bold")).pack(pady=10)
        ttk.Label(about_frame, text="Version 0.1.0").pack()
        ttk.Label(about_frame, text="A local autonomous AI agent powered by DeepSeek R1").pack(pady=10)
        ttk.Label(about_frame, text="© 2025").pack(pady=20)
        
        ttk.Button(about_frame, text="Close", command=about_window.destroy).pack()

    def show_documentation(self):
        """Show documentation"""
        # Placeholder for documentation
        self.add_message("system", "Documentation not implemented yet.")

def main():
    """Main function to start the application"""
    root = tk.Tk()
    app = AutoAgentGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

