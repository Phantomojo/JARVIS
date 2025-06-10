#!/usr/bin/env python3
"""
Blackbox Code Generator Integration Module
This script provides functions to interact with the Blackbox AI code generator in VS Code.
"""

import os
import sys
import json
import subprocess
import requests
import tempfile
import time
from pathlib import Path

class BlackboxIntegration:
    def __init__(self, vscode_path=None):
        """
        Initialize the Blackbox integration.
        
        Args:
            vscode_path (str, optional): Path to VS Code executable. If None, will try to detect automatically.
        """
        self.vscode_path = vscode_path or self._detect_vscode_path()
        self.extension_id = "Blackboxapp.blackbox"
        self.temp_dir = tempfile.mkdtemp(prefix="blackbox_integration_")
        
        # Check if Blackbox extension is installed
        self.is_installed = self._check_extension_installed()
        
        if not self.is_installed:
            print("Blackbox extension is not installed in VS Code.")
            print("Please install it from: https://marketplace.visualstudio.com/items?itemName=Blackboxapp.blackbox")
    
    def _detect_vscode_path(self):
        """
        Detect the path to VS Code executable based on the operating system.
        
        Returns:
            str: Path to VS Code executable or None if not found.
        """
        if sys.platform == "win32":
            # Windows
            possible_paths = [
                os.path.expandvars("%LOCALAPPDATA%\\Programs\\Microsoft VS Code\\Code.exe"),
                os.path.expandvars("%ProgramFiles%\\Microsoft VS Code\\Code.exe"),
                os.path.expandvars("%ProgramFiles(x86)%\\Microsoft VS Code\\Code.exe")
            ]
        elif sys.platform == "darwin":
            # macOS
            possible_paths = [
                "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
            ]
        else:
            # Linux
            possible_paths = [
                "/usr/bin/code",
                "/usr/local/bin/code",
                os.path.expanduser("~/.local/bin/code")
            ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _check_extension_installed(self):
        """
        Check if the Blackbox extension is installed in VS Code.
        
        Returns:
            bool: True if installed, False otherwise.
        """
        if not self.vscode_path:
            return False
        
        try:
            # Run VS Code with --list-extensions flag
            result = subprocess.run(
                [self.vscode_path, "--list-extensions"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Check if Blackbox extension is in the list
            return self.extension_id in result.stdout
        except subprocess.SubprocessError:
            return False
    
    def generate_code(self, prompt, language="python", timeout=30):
        """
        Generate code using Blackbox AI.
        
        This method creates a temporary file and opens it in VS Code with the Blackbox extension.
        It then uses the extension's code completion feature to generate code based on the prompt.
        
        Args:
            prompt (str): The prompt describing the code to generate.
            language (str, optional): The programming language. Defaults to "python".
            timeout (int, optional): Timeout in seconds. Defaults to 30.
        
        Returns:
            str: The generated code or None if generation failed.
        """
        if not self.is_installed or not self.vscode_path:
            return None
        
        # Create a temporary file with the prompt
        file_extension = self._get_file_extension(language)
        temp_file = os.path.join(self.temp_dir, f"code_gen{file_extension}")
        
        with open(temp_file, "w") as f:
            f.write(f"// {prompt}\n\n")
        
        # Open the file in VS Code
        subprocess.Popen([self.vscode_path, temp_file])
        
        # Wait for VS Code to open and Blackbox to initialize
        time.sleep(5)
        
        # Simulate keyboard shortcut to trigger Blackbox code completion
        # Note: This is a simplified approach and may not work reliably
        # In a real implementation, you would use the VS Code extension API
        self._simulate_keyboard_shortcut()
        
        # Wait for code generation to complete
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Check if the file has been updated with generated code
            with open(temp_file, "r") as f:
                content = f.read()
                if len(content) > len(prompt) + 10:  # Assuming code has been generated
                    # Remove the prompt comment
                    generated_code = content.split("\n\n", 1)[1] if "\n\n" in content else content
                    return generated_code
            
            time.sleep(1)
        
        return None
    
    def _get_file_extension(self, language):
        """
        Get the file extension for a given programming language.
        
        Args:
            language (str): The programming language.
        
        Returns:
            str: The file extension including the dot.
        """
        extensions = {
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts",
            "java": ".java",
            "c": ".c",
            "cpp": ".cpp",
            "csharp": ".cs",
            "go": ".go",
            "ruby": ".rb",
            "php": ".php",
            "swift": ".swift",
            "rust": ".rs",
            "html": ".html",
            "css": ".css",
            "sql": ".sql"
        }
        
        return extensions.get(language.lower(), ".txt")
    
    def _simulate_keyboard_shortcut(self):
        """
        Simulate keyboard shortcut to trigger Blackbox code completion.
        
        Note: This is a placeholder. In a real implementation, you would use
        platform-specific methods to simulate keyboard input or use the VS Code API.
        """
        # This is a simplified approach and may not work reliably
        # In a real implementation, you would use platform-specific methods
        # such as pyautogui, pynput, or xdotool (Linux)
        print("Simulating keyboard shortcut to trigger Blackbox code completion")
        
        if sys.platform == "win32":
            # Windows
            try:
                import pyautogui
                pyautogui.hotkey('ctrl', 'shift', 'p')
                time.sleep(0.5)
                pyautogui.write("Enable Blackbox Autocomplete")
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(1)
                pyautogui.press('enter')  # Trigger completion
            except ImportError:
                print("pyautogui not installed. Cannot simulate keyboard shortcut.")
        elif sys.platform == "darwin":
            # macOS
            try:
                import pyautogui
                pyautogui.hotkey('command', 'shift', 'p')
                time.sleep(0.5)
                pyautogui.write("Enable Blackbox Autocomplete")
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(1)
                pyautogui.press('enter')  # Trigger completion
            except ImportError:
                print("pyautogui not installed. Cannot simulate keyboard shortcut.")
        else:
            # Linux
            try:
                subprocess.run(["xdotool", "key", "ctrl+shift+p"], check=False)
                time.sleep(0.5)
                subprocess.run(["xdotool", "type", "Enable Blackbox Autocomplete"], check=False)
                time.sleep(0.5)
                subprocess.run(["xdotool", "key", "Return"], check=False)
                time.sleep(1)
                subprocess.run(["xdotool", "key", "Return"], check=False)  # Trigger completion
            except (subprocess.SubprocessError, FileNotFoundError):
                print("xdotool not installed or failed. Cannot simulate keyboard shortcut.")
    
    def cleanup(self):
        """
        Clean up temporary files.
        """
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except (OSError, IOError) as e:
            print(f"Error cleaning up temporary files: {e}")

class BlackboxAPIIntegration:
    """
    Alternative integration using Blackbox API if available.
    Note: This is a placeholder implementation and may not work with the actual Blackbox API.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the Blackbox API integration.
        
        Args:
            api_key (str, optional): Blackbox API key. If None, will try to get from environment variable.
        """
        self.api_key = api_key or os.environ.get("BLACKBOX_API_KEY")
        self.api_url = "https://api.blackbox.ai/v1/generate"  # Placeholder URL
    
    def generate_code(self, prompt, language="python"):
        """
        Generate code using Blackbox API.
        
        Args:
            prompt (str): The prompt describing the code to generate.
            language (str, optional): The programming language. Defaults to "python".
        
        Returns:
            str: The generated code or None if generation failed.
        """
        if not self.api_key:
            print("Blackbox API key not provided.")
            return None
        
        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": prompt,
                    "language": language,
                    "max_tokens": 1000
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("code")
            else:
                print(f"API request failed with status code {response.status_code}")
                print(response.text)
                return None
        
        except Exception as e:
            print(f"Error calling Blackbox API: {e}")
            return None

def main():
    """
    Main function for testing the Blackbox integration.
    """
    # Test the VS Code integration
    blackbox = BlackboxIntegration()
    
    if blackbox.is_installed:
        print("Blackbox extension is installed in VS Code.")
        
        # Test code generation
        prompt = "Create a function that calculates the Fibonacci sequence up to n terms"
        print(f"Generating code for prompt: {prompt}")
        
        code = blackbox.generate_code(prompt)
        if code:
            print("Generated code:")
            print(code)
        else:
            print("Code generation failed or timed out.")
        
        # Clean up
        blackbox.cleanup()
    else:
        print("Blackbox extension is not installed in VS Code.")
        print("Please install it from: https://marketplace.visualstudio.com/items?itemName=Blackboxapp.blackbox")
    
    # Test the API integration (placeholder)
    api_key = os.environ.get("BLACKBOX_API_KEY")
    if api_key:
        print("\nTesting Blackbox API integration:")
        blackbox_api = BlackboxAPIIntegration(api_key)
        
        prompt = "Create a function that sorts a list of integers using quicksort"
        print(f"Generating code for prompt: {prompt}")
        
        code = blackbox_api.generate_code(prompt)
        if code:
            print("Generated code:")
            print(code)
        else:
            print("API code generation failed.")
    else:
        print("\nBlackbox API key not found in environment variables.")
        print("Set the BLACKBOX_API_KEY environment variable to test API integration.")

if __name__ == "__main__":
    main()

