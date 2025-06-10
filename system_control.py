#!/usr/bin/env python3
"""
System Control Module for Local Autonomous AI Agent
This module provides functions for controlling the computer system, including:
- Mouse and keyboard control
- System monitoring
- Application launching and control
- File operations
- System commands execution
"""

import os
import sys
import time
import subprocess
import platform
import json
import threading
import logging
from typing import Dict, List, Optional, Union, Tuple, Callable

# Third-party imports
try:
    import pyautogui
    import psutil
    import pyttsx3
    import speech_recognition as sr
    from PIL import Image, ImageGrab
except ImportError:
    print("Please install required packages:")
    print("pip install pyautogui psutil pyttsx3 SpeechRecognition pillow")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("system_control.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("SystemControl")

class SystemControl:
    """
    Main class for controlling the computer system.
    """
    
    def __init__(self, safety_mode: bool = True):
        """
        Initialize the system control module.
        
        Args:
            safety_mode (bool, optional): If True, enables safety features to prevent accidental actions.
                                         Defaults to True.
        """
        self.safety_mode = safety_mode
        self.os_type = platform.system()  # 'Windows', 'Linux', or 'Darwin' (macOS)
        
        # Initialize mouse and keyboard control
        pyautogui.PAUSE = 0.5  # Add a 0.5 second pause after each PyAutoGUI call
        if safety_mode:
            pyautogui.FAILSAFE = True  # Move mouse to upper-left corner to abort
        else:
            pyautogui.FAILSAFE = False
        
        # Screen size
        self.screen_width, self.screen_height = pyautogui.size()
        
        logger.info(f"System Control initialized for {self.os_type}")
        logger.info(f"Screen size: {self.screen_width}x{self.screen_height}")
        logger.info(f"Safety mode: {safety_mode}")
    
    #--------------------------------------------------
    # Mouse Control Functions
    #--------------------------------------------------
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> bool:
        """
        Move the mouse to the specified coordinates.
        
        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
            duration (float, optional): Duration of the movement in seconds. Defaults to 0.5.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Ensure coordinates are within screen bounds
            x = max(0, min(x, self.screen_width - 1))
            y = max(0, min(y, self.screen_height - 1))
            
            pyautogui.moveTo(x, y, duration=duration)
            logger.info(f"Moved mouse to ({x}, {y})")
            return True
        except Exception as e:
            logger.error(f"Failed to move mouse: {e}")
            return False
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = 'left', clicks: int = 1, interval: float = 0.25) -> bool:
        """
        Click at the current or specified position.
        
        Args:
            x (Optional[int], optional): X-coordinate. If None, uses current position. Defaults to None.
            y (Optional[int], optional): Y-coordinate. If None, uses current position. Defaults to None.
            button (str, optional): Mouse button to click ('left', 'right', 'middle'). Defaults to 'left'.
            clicks (int, optional): Number of clicks. Defaults to 1.
            interval (float, optional): Interval between clicks in seconds. Defaults to 0.25.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if x is not None and y is not None:
                # Move to position first
                self.move_mouse(x, y)
            
            pyautogui.click(button=button, clicks=clicks, interval=interval)
            
            if x is not None and y is not None:
                logger.info(f"Clicked {button} button at ({x}, {y}), {clicks} times")
            else:
                current_x, current_y = pyautogui.position()
                logger.info(f"Clicked {button} button at current position ({current_x}, {current_y}), {clicks} times")
            
            return True
        except Exception as e:
            logger.error(f"Failed to click: {e}")
            return False
    
    def double_click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = 'left') -> bool:
        """
        Double-click at the current or specified position.
        
        Args:
            x (Optional[int], optional): X-coordinate. If None, uses current position. Defaults to None.
            y (Optional[int], optional): Y-coordinate. If None, uses current position. Defaults to None.
            button (str, optional): Mouse button to click ('left', 'right', 'middle'). Defaults to 'left'.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self.click(x, y, button, clicks=2)
    
    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """
        Right-click at the current or specified position.
        
        Args:
            x (Optional[int], optional): X-coordinate. If None, uses current position. Defaults to None.
            y (Optional[int], optional): Y-coordinate. If None, uses current position. Defaults to None.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self.click(x, y, button='right')
    
    def scroll(self, amount: int) -> bool:
        """
        Scroll the mouse wheel.
        
        Args:
            amount (int): Amount to scroll. Positive values scroll up, negative values scroll down.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            pyautogui.scroll(amount)
            logger.info(f"Scrolled {amount} units")
            return True
        except Exception as e:
            logger.error(f"Failed to scroll: {e}")
            return False
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5, button: str = 'left') -> bool:
        """
        Drag from one position to another.
        
        Args:
            start_x (int): Starting X-coordinate.
            start_y (int): Starting Y-coordinate.
            end_x (int): Ending X-coordinate.
            end_y (int): Ending Y-coordinate.
            duration (float, optional): Duration of the drag in seconds. Defaults to 0.5.
            button (str, optional): Mouse button to use for dragging. Defaults to 'left'.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Ensure coordinates are within screen bounds
            start_x = max(0, min(start_x, self.screen_width - 1))
            start_y = max(0, min(start_y, self.screen_height - 1))
            end_x = max(0, min(end_x, self.screen_width - 1))
            end_y = max(0, min(end_y, self.screen_height - 1))
            
            # Move to start position
            pyautogui.moveTo(start_x, start_y, duration=0.2)
            
            # Drag to end position
            pyautogui.dragTo(end_x, end_y, duration=duration, button=button)
            
            logger.info(f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
            return True
        except Exception as e:
            logger.error(f"Failed to drag: {e}")
            return False
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """
        Get the current mouse position.
        
        Returns:
            Tuple[int, int]: (x, y) coordinates of the mouse.
        """
        x, y = pyautogui.position()
        logger.info(f"Mouse position: ({x}, {y})")
        return (x, y)
    
    #--------------------------------------------------
    # Keyboard Control Functions
    #--------------------------------------------------
    
    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """
        Type text at the current cursor position.
        
        Args:
            text (str): Text to type.
            interval (float, optional): Interval between keypresses in seconds. Defaults to 0.05.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            pyautogui.write(text, interval=interval)
            logger.info(f"Typed text: {text}")
            return True
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            return False
    
    def press_key(self, key: str) -> bool:
        """
        Press a single key.
        
        Args:
            key (str): Key to press. Can be a single character or a key name like 'enter', 'tab', etc.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            pyautogui.press(key)
            logger.info(f"Pressed key: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to press key: {e}")
            return False
    
    def hotkey(self, *keys) -> bool:
        """
        Press a combination of keys.
        
        Args:
            *keys: Variable number of keys to press simultaneously.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            pyautogui.hotkey(*keys)
            logger.info(f"Pressed hotkey: {' + '.join(keys)}")
            return True
        except Exception as e:
            logger.error(f"Failed to press hotkey: {e}")
            return False
    
    def copy(self) -> bool:
        """
        Press Ctrl+C (Command+C on macOS) to copy.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.os_type == 'Darwin':  # macOS
            return self.hotkey('command', 'c')
        else:  # Windows or Linux
            return self.hotkey('ctrl', 'c')
    
    def paste(self) -> bool:
        """
        Press Ctrl+V (Command+V on macOS) to paste.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.os_type == 'Darwin':  # macOS
            return self.hotkey('command', 'v')
        else:  # Windows or Linux
            return self.hotkey('ctrl', 'v')
    
    def select_all(self) -> bool:
        """
        Press Ctrl+A (Command+A on macOS) to select all.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.os_type == 'Darwin':  # macOS
            return self.hotkey('command', 'a')
        else:  # Windows or Linux
            return self.hotkey('ctrl', 'a')
    
    #--------------------------------------------------
    # Screen Capture Functions
    #--------------------------------------------------
    
    def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None, 
                       save_path: Optional[str] = None) -> Optional[Image.Image]:
        """
        Take a screenshot of the entire screen or a specific region.
        
        Args:
            region (Optional[Tuple[int, int, int, int]], optional): Region to capture (left, top, width, height).
                                                                   Defaults to None (entire screen).
            save_path (Optional[str], optional): Path to save the screenshot. Defaults to None (don't save).
        
        Returns:
            Optional[Image.Image]: Screenshot as a PIL Image object, or None if failed.
        """
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
                logger.info(f"Took screenshot of region {region}")
            else:
                screenshot = pyautogui.screenshot()
                logger.info("Took screenshot of entire screen")
            
            if save_path:
                screenshot.save(save_path)
                logger.info(f"Saved screenshot to {save_path}")
            
            return screenshot
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None
    
    def locate_on_screen(self, image_path: str, confidence: float = 0.9) -> Optional[Tuple[int, int, int, int]]:
        """
        Locate an image on the screen.
        
        Args:
            image_path (str): Path to the image file to locate.
            confidence (float, optional): Confidence threshold for the match (0-1). Defaults to 0.9.
        
        Returns:
            Optional[Tuple[int, int, int, int]]: Region (left, top, width, height) where the image was found,
                                               or None if not found.
        """
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                logger.info(f"Found image {image_path} at {location}")
            else:
                logger.info(f"Image {image_path} not found on screen")
            return location
        except Exception as e:
            logger.error(f"Failed to locate image on screen: {e}")
            return None
    
    def click_image(self, image_path: str, confidence: float = 0.9) -> bool:
        """
        Locate an image on the screen and click on it.
        
        Args:
            image_path (str): Path to the image file to locate and click.
            confidence (float, optional): Confidence threshold for the match (0-1). Defaults to 0.9.
        
        Returns:
            bool: True if the image was found and clicked, False otherwise.
        """
        try:
            location = self.locate_on_screen(image_path, confidence)
            if location:
                x, y = pyautogui.center(location)
                return self.click(x, y)
            else:
                logger.warning(f"Could not click image {image_path} because it was not found on screen")
                return False
        except Exception as e:
            logger.error(f"Failed to click image: {e}")
            return False
    
    #--------------------------------------------------
    # System Monitoring Functions
    #--------------------------------------------------
    
    def get_cpu_usage(self) -> float:
        """
        Get the current CPU usage percentage.
        
        Returns:
            float: CPU usage percentage (0-100).
        """
        cpu_percent = psutil.cpu_percent(interval=0.5)
        logger.info(f"CPU usage: {cpu_percent}%")
        return cpu_percent
    
    def get_memory_usage(self) -> Dict[str, Union[int, float]]:
        """
        Get the current memory usage.
        
        Returns:
            Dict[str, Union[int, float]]: Dictionary with memory usage information.
        """
        memory = psutil.virtual_memory()
        memory_info = {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percent": memory.percent
        }
        logger.info(f"Memory usage: {memory_info['percent']}% ({memory_info['used'] / (1024**3):.2f} GB used)")
        return memory_info
    
    def get_disk_usage(self, path: str = "/") -> Dict[str, Union[int, float]]:
        """
        Get the disk usage for a specific path.
        
        Args:
            path (str, optional): Path to check disk usage for. Defaults to "/" (root).
        
        Returns:
            Dict[str, Union[int, float]]: Dictionary with disk usage information.
        """
        disk = psutil.disk_usage(path)
        disk_info = {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
        logger.info(f"Disk usage for {path}: {disk_info['percent']}% ({disk_info['used'] / (1024**3):.2f} GB used)")
        return disk_info
    
    def get_battery_status(self) -> Optional[Dict[str, Union[int, float, bool]]]:
        """
        Get the battery status (if available).
        
        Returns:
            Optional[Dict[str, Union[int, float, bool]]]: Dictionary with battery information,
                                                        or None if no battery is available.
        """
        if not hasattr(psutil, "sensors_battery") or psutil.sensors_battery() is None:
            logger.info("No battery available")
            return None
        
        battery = psutil.sensors_battery()
        battery_info = {
            "percent": battery.percent,
            "power_plugged": battery.power_plugged,
            "seconds_left": battery.secsleft if battery.secsleft != -1 else None
        }
        
        status = "Charging" if battery_info["power_plugged"] else "Discharging"
        time_left = ""
        if battery_info["seconds_left"] is not None:
            hours, remainder = divmod(battery_info["seconds_left"], 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left = f", {hours:02d}:{minutes:02d}:{seconds:02d} remaining"
        
        logger.info(f"Battery: {battery_info['percent']}%, {status}{time_left}")
        return battery_info
    
    def get_running_processes(self) -> List[Dict[str, Union[int, str, float]]]:
        """
        Get a list of running processes.
        
        Returns:
            List[Dict[str, Union[int, str, float]]]: List of dictionaries with process information.
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                proc_info = proc.info
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        logger.info(f"Found {len(processes)} running processes")
        return processes
    
    def find_process_by_name(self, name: str) -> List[Dict[str, Union[int, str, float]]]:
        """
        Find processes by name.
        
        Args:
            name (str): Name of the process to find (case-insensitive).
        
        Returns:
            List[Dict[str, Union[int, str, float]]]: List of dictionaries with process information.
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                if name.lower() in proc.info['name'].lower():
                    processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        logger.info(f"Found {len(processes)} processes matching '{name}'")
        return processes
    
    def kill_process(self, pid: int) -> bool:
        """
        Kill a process by its PID.
        
        Args:
            pid (int): Process ID to kill.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            process.terminate()
            logger.info(f"Terminated process {process_name} (PID: {pid})")
            return True
        except psutil.NoSuchProcess:
            logger.error(f"No process found with PID {pid}")
            return False
        except psutil.AccessDenied:
            logger.error(f"Access denied when trying to terminate process with PID {pid}")
            return False
        except Exception as e:
            logger.error(f"Failed to kill process with PID {pid}: {e}")
            return False
    
    #--------------------------------------------------
    # Application Control Functions
    #--------------------------------------------------
    
    def launch_application(self, app_path: str, args: List[str] = None) -> Optional[subprocess.Popen]:
        """
        Launch an application.
        
        Args:
            app_path (str): Path to the application executable.
            args (List[str], optional): Command-line arguments for the application. Defaults to None.
        
        Returns:
            Optional[subprocess.Popen]: Subprocess object if successful, None otherwise.
        """
        try:
            cmd = [app_path]
            if args:
                cmd.extend(args)
            
            process = subprocess.Popen(cmd)
            logger.info(f"Launched application: {app_path} with PID {process.pid}")
            return process
        except Exception as e:
            logger.error(f"Failed to launch application {app_path}: {e}")
            return None
    
    def open_file(self, file_path: str) -> bool:
        """
        Open a file with the default application.
        
        Args:
            file_path (str): Path to the file to open.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if self.os_type == 'Windows':
                os.startfile(file_path)
            elif self.os_type == 'Darwin':  # macOS
                subprocess.run(['open', file_path], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', file_path], check=True)
            
            logger.info(f"Opened file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to open file {file_path}: {e}")
            return False
    
    def open_url(self, url: str) -> bool:
        """
        Open a URL in the default web browser.
        
        Args:
            url (str): URL to open.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            import webbrowser
            webbrowser.open(url)
            logger.info(f"Opened URL: {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to open URL {url}: {e}")
            return False
    
    #--------------------------------------------------
    # System Command Functions
    #--------------------------------------------------
    
    def execute_command(self, command: str, shell: bool = True, timeout: Optional[int] = None) -> Dict[str, Union[int, str]]:
        """
        Execute a system command.
        
        Args:
            command (str): Command to execute.
            shell (bool, optional): Whether to use shell execution. Defaults to True.
            timeout (Optional[int], optional): Timeout in seconds. Defaults to None (no timeout).
        
        Returns:
            Dict[str, Union[int, str]]: Dictionary with command output and return code.
        """
        try:
            logger.info(f"Executing command: {command}")
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
            if result.returncode == 0:
                logger.info(f"Command executed successfully")
            else:
                logger.warning(f"Command returned non-zero exit code: {result.returncode}")
                logger.warning(f"Error output: {result.stderr}")
            
            return output
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout} seconds")
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds"
            }
        except Exception as e:
            logger.error(f"Failed to execute command: {e}")
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e)
            }
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Get system information.
        
        Returns:
            Dict[str, str]: Dictionary with system information.
        """
        info = {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }
        
        logger.info(f"System info: {info}")
        return info
    
    #--------------------------------------------------
    # File Operations
    #--------------------------------------------------
    
    def list_directory(self, path: str = ".") -> List[str]:
        """
        List files and directories in a directory.
        
        Args:
            path (str, optional): Path to list. Defaults to "." (current directory).
        
        Returns:
            List[str]: List of files and directories.
        """
        try:
            files = os.listdir(path)
            logger.info(f"Listed directory {path}: {len(files)} items")
            return files
        except Exception as e:
            logger.error(f"Failed to list directory {path}: {e}")
            return []
    
    def create_directory(self, path: str) -> bool:
        """
        Create a directory.
        
        Args:
            path (str): Path of the directory to create.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Created directory: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {e}")
            return False
    
    def delete_file(self, path: str) -> bool:
        """
        Delete a file.
        
        Args:
            path (str): Path of the file to delete.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            os.remove(path)
            logger.info(f"Deleted file: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete file {path}: {e}")
            return False
    
    def copy_file(self, source: str, destination: str) -> bool:
        """
        Copy a file.
        
        Args:
            source (str): Source file path.
            destination (str): Destination file path.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            import shutil
            shutil.copy2(source, destination)
            logger.info(f"Copied file from {source} to {destination}")
            return True
        except Exception as e:
            logger.error(f"Failed to copy file from {source} to {destination}: {e}")
            return False
    
    def move_file(self, source: str, destination: str) -> bool:
        """
        Move a file.
        
        Args:
            source (str): Source file path.
            destination (str): Destination file path.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            import shutil
            shutil.move(source, destination)
            logger.info(f"Moved file from {source} to {destination}")
            return True
        except Exception as e:
            logger.error(f"Failed to move file from {source} to {destination}: {e}")
            return False
    
    def read_file(self, path: str) -> Optional[str]:
        """
        Read a text file.
        
        Args:
            path (str): Path of the file to read.
        
        Returns:
            Optional[str]: File contents as a string, or None if failed.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"Read file: {path}")
            return content
        except Exception as e:
            logger.error(f"Failed to read file {path}: {e}")
            return None
    
    def write_file(self, path: str, content: str) -> bool:
        """
        Write to a text file.
        
        Args:
            path (str): Path of the file to write.
            content (str): Content to write.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Wrote to file: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to write to file {path}: {e}")
            return False
    
    def append_to_file(self, path: str, content: str) -> bool:
        """
        Append to a text file.
        
        Args:
            path (str): Path of the file to append to.
            content (str): Content to append.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Appended to file: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to append to file {path}: {e}")
            return False

class VoiceControl:
    """
    Class for voice recognition and speech synthesis.
    """
    
    def __init__(self):
        """
        Initialize the voice control module.
        """
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Get available voices
        self.voices = self.engine.getProperty('voices')
        
        # Set default voice (usually index 0 is male, 1 is female)
        if len(self.voices) > 1:
            self.engine.setProperty('voice', self.voices[1].id)  # Set to female voice by default
        
        # Set default speech rate and volume
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
        logger.info("Voice Control initialized")
        logger.info(f"Available voices: {len(self.voices)}")
    
    def speak(self, text: str, block: bool = True) -> bool:
        """
        Convert text to speech.
        
        Args:
            text (str): Text to speak.
            block (bool, optional): Whether to block until speech is complete. Defaults to True.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if block:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # Run in a separate thread to avoid blocking
                def speak_thread():
                    self.engine.say(text)
                    self.engine.runAndWait()
                
                threading.Thread(target=speak_thread, daemon=True).start()
            
            logger.info(f"Speaking: {text}")
            return True
        except Exception as e:
            logger.error(f"Failed to speak: {e}")
            return False
    
    def set_voice(self, index: int) -> bool:
        """
        Set the voice by index.
        
        Args:
            index (int): Index of the voice to use.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if 0 <= index < len(self.voices):
                self.engine.setProperty('voice', self.voices[index].id)
                logger.info(f"Set voice to index {index}: {self.voices[index].name}")
                return True
            else:
                logger.error(f"Invalid voice index: {index}. Available range: 0-{len(self.voices)-1}")
                return False
        except Exception as e:
            logger.error(f"Failed to set voice: {e}")
            return False
    
    def set_speech_rate(self, rate: int) -> bool:
        """
        Set the speech rate.
        
        Args:
            rate (int): Speech rate (words per minute). Normal is around 150-200.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.engine.setProperty('rate', rate)
            logger.info(f"Set speech rate to {rate}")
            return True
        except Exception as e:
            logger.error(f"Failed to set speech rate: {e}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """
        Set the speech volume.
        
        Args:
            volume (float): Volume level (0.0 to 1.0).
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            volume = max(0.0, min(1.0, volume))  # Ensure volume is between 0.0 and 1.0
            self.engine.setProperty('volume', volume)
            logger.info(f"Set volume to {volume}")
            return True
        except Exception as e:
            logger.error(f"Failed to set volume: {e}")
            return False
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 5) -> Optional[str]:
        """
        Listen for speech and convert to text.
        
        Args:
            timeout (int, optional): How long to wait for speech to start (seconds). Defaults to 5.
            phrase_time_limit (int, optional): Maximum length of speech to process (seconds). Defaults to 5.
        
        Returns:
            Optional[str]: Recognized text, or None if no speech was detected or recognition failed.
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening for speech...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for speech
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
                logger.info("Processing speech...")
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                
                logger.info(f"Recognized: {text}")
                return text
        except sr.WaitTimeoutError:
            logger.warning("No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            logger.warning("Speech recognition could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to recognize speech: {e}")
            return None
    
    def listen_in_background(self, callback: Callable[[Optional[str]], None], 
                            stop_event: threading.Event) -> threading.Thread:
        """
        Listen for speech in the background and call a callback function when speech is recognized.
        
        Args:
            callback (Callable[[Optional[str]], None]): Function to call with recognized text.
            stop_event (threading.Event): Event to signal when to stop listening.
        
        Returns:
            threading.Thread: Background thread that is listening for speech.
        """
        def listen_thread():
            try:
                with sr.Microphone() as source:
                    logger.info("Background listening started")
                    
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    while not stop_event.is_set():
                        try:
                            # Listen for speech with a timeout
                            audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                            
                            # Recognize speech using Google Speech Recognition
                            text = self.recognizer.recognize_google(audio)
                            
                            logger.info(f"Background recognized: {text}")
                            callback(text)
                        except sr.WaitTimeoutError:
                            # No speech detected, continue listening
                            continue
                        except sr.UnknownValueError:
                            # Speech was detected but not understood
                            callback(None)
                        except sr.RequestError as e:
                            logger.error(f"Could not request results from Google Speech Recognition service: {e}")
                            callback(None)
                        except Exception as e:
                            logger.error(f"Error in background listening: {e}")
                            callback(None)
                
                logger.info("Background listening stopped")
            except Exception as e:
                logger.error(f"Fatal error in background listening thread: {e}")
        
        thread = threading.Thread(target=listen_thread, daemon=True)
        thread.start()
        return thread

class JarvisAssistant:
    """
    Main class for the Jarvis-like assistant that integrates system control and voice control.
    """
    
    def __init__(self, use_voice: bool = True, safety_mode: bool = True):
        """
        Initialize the Jarvis assistant.
        
        Args:
            use_voice (bool, optional): Whether to use voice control. Defaults to True.
            safety_mode (bool, optional): Whether to enable safety features. Defaults to True.
        """
        # Initialize system control
        self.system = SystemControl(safety_mode=safety_mode)
        
        # Initialize voice control if enabled
        self.use_voice = use_voice
        if use_voice:
            self.voice = VoiceControl()
        else:
            self.voice = None
        
        # Initialize state
        self.is_listening = False
        self.stop_listening_event = threading.Event()
        self.listening_thread = None
        
        logger.info(f"Jarvis Assistant initialized (voice: {use_voice}, safety: {safety_mode})")
    
    def start(self):
        """
        Start the Jarvis assistant.
        """
        if self.use_voice:
            self.voice.speak("Jarvis assistant is now online. How can I help you?")
        
        logger.info("Jarvis Assistant started")
    
    def stop(self):
        """
        Stop the Jarvis assistant.
        """
        if self.is_listening:
            self.stop_listening()
        
        if self.use_voice:
            self.voice.speak("Jarvis assistant is shutting down. Goodbye.")
        
        logger.info("Jarvis Assistant stopped")
    
    def start_listening(self):
        """
        Start listening for voice commands in the background.
        """
        if not self.use_voice:
            logger.warning("Voice control is disabled")
            return
        
        if self.is_listening:
            logger.warning("Already listening")
            return
        
        self.stop_listening_event.clear()
        self.listening_thread = self.voice.listen_in_background(self.process_voice_command, self.stop_listening_event)
        self.is_listening = True
        
        self.voice.speak("I'm listening.")
        logger.info("Started listening for voice commands")
    
    def stop_listening(self):
        """
        Stop listening for voice commands.
        """
        if not self.is_listening:
            logger.warning("Not currently listening")
            return
        
        self.stop_listening_event.set()
        if self.listening_thread:
            self.listening_thread.join(timeout=2)
        
        self.is_listening = False
        
        if self.use_voice:
            self.voice.speak("I've stopped listening.")
        
        logger.info("Stopped listening for voice commands")
    
    def process_voice_command(self, text: Optional[str]):
        """
        Process a voice command.
        
        Args:
            text (Optional[str]): Recognized text from voice command, or None if recognition failed.
        """
        if text is None:
            return
        
        # Convert to lowercase for easier matching
        text = text.lower()
        
        # Log the command
        logger.info(f"Processing voice command: {text}")
        
        # Process the command
        response = self.process_command(text)
        
        # Speak the response
        if response and self.use_voice:
            self.voice.speak(response)
    
    def process_command(self, command: str) -> Optional[str]:
        """
        Process a command (from voice or text).
        
        Args:
            command (str): Command to process.
        
        Returns:
            Optional[str]: Response to the command, or None if no response is needed.
        """
        # Convert to lowercase for easier matching
        command = command.lower()
        
        # Basic wake word detection
        if "jarvis" not in command and "hey jarvis" not in command and "hey" not in command:
            return None
        
        # Remove wake words
        command = command.replace("jarvis", "").replace("hey", "").strip()
        
        # System information commands
        if "system info" in command or "system information" in command:
            info = self.system.get_system_info()
            return f"You are running {info['system']} {info['release']} on a {info['machine']} machine."
        
        elif "cpu usage" in command:
            cpu = self.system.get_cpu_usage()
            return f"CPU usage is currently {cpu:.1f} percent."
        
        elif "memory usage" in command or "ram usage" in command:
            memory = self.system.get_memory_usage()
            used_gb = memory["used"] / (1024**3)
            total_gb = memory["total"] / (1024**3)
            return f"Memory usage is {memory['percent']:.1f} percent. {used_gb:.1f} gigabytes used out of {total_gb:.1f} gigabytes total."
        
        elif "disk usage" in command or "storage" in command:
            disk = self.system.get_disk_usage()
            used_gb = disk["used"] / (1024**3)
            total_gb = disk["total"] / (1024**3)
            return f"Disk usage is {disk['percent']:.1f} percent. {used_gb:.1f} gigabytes used out of {total_gb:.1f} gigabytes total."
        
        elif "battery" in command:
            battery = self.system.get_battery_status()
            if battery:
                status = "charging" if battery["power_plugged"] else "discharging"
                return f"Battery is at {battery['percent']}% and {status}."
            else:
                return "No battery information available."
        
        # Application control commands
        elif "open" in command:
            # Extract what to open
            parts = command.split("open", 1)
            if len(parts) > 1:
                target = parts[1].strip()
                
                # Check if it's a URL
                if target.startswith("http") or ".com" in target or ".org" in target or ".net" in target:
                    if not target.startswith("http"):
                        target = "https://" + target
                    success = self.system.open_url(target)
                    return f"Opening {target}." if success else f"Failed to open {target}."
                
                # Otherwise, try to open as an application or file
                # This is simplified and would need to be expanded for a real implementation
                return f"I'll try to open {target}, but application launching requires more specific implementation."
        
        # Mouse and keyboard control commands
        elif "click" in command:
            if "right click" in command:
                self.system.right_click()
                return "Right clicked."
            else:
                self.system.click()
                return "Clicked."
        
        elif "double click" in command:
            self.system.double_click()
            return "Double clicked."
        
        elif "scroll" in command:
            amount = 5  # Default amount
            if "up" in command:
                self.system.scroll(amount)
                return "Scrolled up."
            elif "down" in command:
                self.system.scroll(-amount)
                return "Scrolled down."
            else:
                return "Please specify scroll direction (up or down)."
        
        elif "type" in command:
            parts = command.split("type", 1)
            if len(parts) > 1:
                text_to_type = parts[1].strip()
                self.system.type_text(text_to_type)
                return f"Typed: {text_to_type}"
            else:
                return "What would you like me to type?"
        
        # System control commands
        elif "screenshot" in command:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            home_dir = os.path.expanduser("~")
            save_path = os.path.join(home_dir, "Pictures", filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            screenshot = self.system.take_screenshot(save_path=save_path)
            if screenshot:
                return f"Screenshot saved to {save_path}"
            else:
                return "Failed to take screenshot."
        
        # Voice control commands
        elif "stop listening" in command:
            self.stop_listening()
            return "I've stopped listening."
        
        elif "start listening" in command:
            self.start_listening()
            return "I'm listening."
        
        # Help command
        elif "help" in command or "what can you do" in command:
            return """
            I can help you with various tasks, including:
            - System information (system info, CPU usage, memory usage, disk usage, battery status)
            - Opening websites and applications
            - Mouse control (click, right click, double click, scroll)
            - Keyboard control (typing text)
            - Taking screenshots
            - Voice control (start listening, stop listening)
            
            Just ask me what you need!
            """
        
        # Fallback
        else:
            return "I'm not sure how to help with that. Try asking for help to see what I can do."

def main():
    """
    Main function for testing the system control module.
    """
    # Initialize the system control module
    system = SystemControl()
    
    # Test mouse control
    print("Testing mouse control...")
    screen_width, screen_height = pyautogui.size()
    system.move_mouse(screen_width // 2, screen_height // 2)
    time.sleep(1)
    
    # Test keyboard control
    print("Testing keyboard control...")
    # Uncomment to test typing (be careful where this runs!)
    # system.type_text("Hello, world!")
    
    # Test system monitoring
    print("Testing system monitoring...")
    cpu = system.get_cpu_usage()
    memory = system.get_memory_usage()
    disk = system.get_disk_usage()
    
    print(f"CPU Usage: {cpu}%")
    print(f"Memory Usage: {memory['percent']}%")
    print(f"Disk Usage: {disk['percent']}%")
    
    # Test voice control if available
    try:
        print("Testing voice control...")
        voice = VoiceControl()
        voice.speak("Hello, I am Jarvis, your personal assistant.")
        
        print("Say something...")
        text = voice.listen()
        if text:
            print(f"You said: {text}")
            voice.speak(f"You said: {text}")
    except Exception as e:
        print(f"Voice control test failed: {e}")
    
    print("System control module test complete.")

if __name__ == "__main__":
    main()

