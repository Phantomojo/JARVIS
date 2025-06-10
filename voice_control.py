#!/usr/bin/env python3
"""
Voice Control Module for Local Autonomous AI Agent
This module provides voice recognition and speech synthesis capabilities.
"""

import os
import sys
import time
import threading
import logging
import queue
import json
from typing import Dict, List, Optional, Union, Tuple, Callable

# Third-party imports
try:
    import pyttsx3
    import speech_recognition as sr
    import numpy as np
    from scipy.io import wavfile
    import pyaudio
except ImportError:
    print("Please install required packages:")
    print("pip install pyttsx3 SpeechRecognition numpy scipy pyaudio")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("voice_control.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("VoiceControl")

class SpeechSynthesis:
    """
    Class for text-to-speech synthesis.
    """
    
    def __init__(self, voice_id: Optional[str] = None, rate: int = 150, volume: float = 1.0):
        """
        Initialize the speech synthesis engine.
        
        Args:
            voice_id (Optional[str], optional): ID of the voice to use. Defaults to None (system default).
            rate (int, optional): Speech rate (words per minute). Defaults to 150.
            volume (float, optional): Volume level (0.0 to 1.0). Defaults to 1.0.
        """
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Get available voices
        self.voices = self.engine.getProperty('voices')
        
        # Set voice if specified, otherwise use default
        if voice_id:
            self.engine.setProperty('voice', voice_id)
        elif len(self.voices) > 1:
            # Use female voice if available (usually index 1)
            self.engine.setProperty('voice', self.voices[1].id)
        
        # Set speech rate and volume
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        # Store current settings
        self.current_voice = self.engine.getProperty('voice')
        self.current_rate = rate
        self.current_volume = volume
        
        # Create a queue for speech tasks
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.stop_speaking = threading.Event()
        
        # Start the speech thread
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
        
        logger.info("Speech synthesis initialized")
        logger.info(f"Available voices: {len(self.voices)}")
        logger.info(f"Current voice: {self.current_voice}")
        logger.info(f"Current rate: {self.current_rate}")
        logger.info(f"Current volume: {self.current_volume}")
    
    def _speech_worker(self):
        """
        Worker thread for processing speech tasks from the queue.
        """
        while not self.stop_speaking.is_set():
            try:
                # Get a task from the queue with a timeout
                task = self.speech_queue.get(timeout=0.5)
                
                if task is None:
                    # None is a signal to stop
                    break
                
                text, callback = task
                
                # Set speaking flag
                self.is_speaking = True
                
                # Speak the text
                self.engine.say(text)
                self.engine.runAndWait()
                
                # Reset speaking flag
                self.is_speaking = False
                
                # Call the callback if provided
                if callback:
                    callback()
                
                # Mark the task as done
                self.speech_queue.task_done()
            
            except queue.Empty:
                # No tasks in the queue, continue waiting
                continue
            
            except Exception as e:
                logger.error(f"Error in speech worker: {e}")
                self.is_speaking = False
    
    def speak(self, text: str, block: bool = False, callback: Optional[Callable[[], None]] = None) -> bool:
        """
        Convert text to speech.
        
        Args:
            text (str): Text to speak.
            block (bool, optional): Whether to block until speech is complete. Defaults to False.
            callback (Optional[Callable[[], None]], optional): Function to call when speech is complete.
                                                             Defaults to None.
        
        Returns:
            bool: True if the speech task was queued successfully, False otherwise.
        """
        try:
            # Add the speech task to the queue
            self.speech_queue.put((text, callback))
            
            logger.info(f"Queued speech: {text}")
            
            if block:
                # Wait for the speech to complete
                self.speech_queue.join()
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to queue speech: {e}")
            return False
    
    def stop(self):
        """
        Stop the speech synthesis engine and worker thread.
        """
        # Signal the worker thread to stop
        self.stop_speaking.set()
        
        # Add None to the queue to ensure the worker thread exits
        self.speech_queue.put(None)
        
        # Wait for the worker thread to exit
        if self.speech_thread.is_alive():
            self.speech_thread.join(timeout=2)
        
        logger.info("Speech synthesis stopped")
    
    def is_busy(self) -> bool:
        """
        Check if the speech synthesis engine is currently speaking.
        
        Returns:
            bool: True if speaking, False otherwise.
        """
        return self.is_speaking or not self.speech_queue.empty()
    
    def get_voices(self) -> List[Dict[str, str]]:
        """
        Get a list of available voices.
        
        Returns:
            List[Dict[str, str]]: List of dictionaries with voice information.
        """
        voice_list = []
        for i, voice in enumerate(self.voices):
            voice_info = {
                "id": voice.id,
                "name": voice.name,
                "languages": voice.languages,
                "gender": "Male" if "male" in voice.name.lower() else "Female" if "female" in voice.name.lower() else "Unknown",
                "index": i
            }
            voice_list.append(voice_info)
        
        return voice_list
    
    def set_voice(self, voice_id: str) -> bool:
        """
        Set the voice by ID.
        
        Args:
            voice_id (str): ID of the voice to use.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.engine.setProperty('voice', voice_id)
            self.current_voice = voice_id
            logger.info(f"Set voice to {voice_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to set voice: {e}")
            return False
    
    def set_voice_by_index(self, index: int) -> bool:
        """
        Set the voice by index.
        
        Args:
            index (int): Index of the voice to use.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if 0 <= index < len(self.voices):
                voice_id = self.voices[index].id
                return self.set_voice(voice_id)
            else:
                logger.error(f"Invalid voice index: {index}. Available range: 0-{len(self.voices)-1}")
                return False
        except Exception as e:
            logger.error(f"Failed to set voice by index: {e}")
            return False
    
    def set_rate(self, rate: int) -> bool:
        """
        Set the speech rate.
        
        Args:
            rate (int): Speech rate (words per minute). Normal is around 150-200.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.engine.setProperty('rate', rate)
            self.current_rate = rate
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
            self.current_volume = volume
            logger.info(f"Set volume to {volume}")
            return True
        except Exception as e:
            logger.error(f"Failed to set volume: {e}")
            return False
    
    def save_to_file(self, text: str, file_path: str) -> bool:
        """
        Save speech to an audio file.
        
        Args:
            text (str): Text to convert to speech.
            file_path (str): Path to save the audio file.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # This is not directly supported by pyttsx3, but we can use a workaround
            # with a different TTS library like gTTS if needed
            logger.error("Saving speech to file is not supported by pyttsx3")
            return False
        except Exception as e:
            logger.error(f"Failed to save speech to file: {e}")
            return False

class SpeechRecognition:
    """
    Class for speech recognition.
    """
    
    def __init__(self, language: str = "en-US", energy_threshold: int = 300, 
                dynamic_energy_threshold: bool = True, pause_threshold: float = 0.8):
        """
        Initialize the speech recognition engine.
        
        Args:
            language (str, optional): Language code for recognition. Defaults to "en-US".
            energy_threshold (int, optional): Energy level for mic to detect. Defaults to 300.
            dynamic_energy_threshold (bool, optional): Whether to dynamically adjust energy threshold.
                                                     Defaults to True.
            pause_threshold (float, optional): Seconds of non-speaking audio before a phrase is considered complete.
                                             Defaults to 0.8.
        """
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.language = language
        
        # Configure recognizer
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = dynamic_energy_threshold
        self.recognizer.pause_threshold = pause_threshold
        
        # Initialize microphone
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.microphone_available = True
        except (sr.RequestError, OSError) as e:
            logger.error(f"Microphone initialization failed: {e}")
            self.microphone_available = False
        
        # Background listening variables
        self.is_listening = False
        self.stop_listening_event = threading.Event()
        self.listening_thread = None
        self.callback = None
        
        logger.info("Speech recognition initialized")
        logger.info(f"Language: {language}")
        logger.info(f"Microphone available: {self.microphone_available}")
        logger.info(f"Energy threshold: {self.recognizer.energy_threshold}")
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for speech and convert to text.
        
        Args:
            timeout (int, optional): How long to wait for speech to start (seconds). Defaults to 5.
            phrase_time_limit (int, optional): Maximum length of speech to process (seconds). Defaults to 10.
        
        Returns:
            Optional[str]: Recognized text, or None if no speech was detected or recognition failed.
        """
        if not self.microphone_available:
            logger.error("Microphone is not available")
            return None
        
        try:
            with sr.Microphone() as source:
                logger.info("Listening for speech...")
                
                # Listen for speech
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
                logger.info("Processing speech...")
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio, language=self.language)
                
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
    
    def start_listening_in_background(self, callback: Callable[[Optional[str]], None]) -> bool:
        """
        Start listening for speech in the background.
        
        Args:
            callback (Callable[[Optional[str]], None]): Function to call with recognized text.
        
        Returns:
            bool: True if background listening was started successfully, False otherwise.
        """
        if not self.microphone_available:
            logger.error("Microphone is not available")
            return False
        
        if self.is_listening:
            logger.warning("Already listening in background")
            return False
        
        self.callback = callback
        self.stop_listening_event.clear()
        self.listening_thread = threading.Thread(target=self._listen_in_background, daemon=True)
        self.listening_thread.start()
        self.is_listening = True
        
        logger.info("Started listening in background")
        return True
    
    def _listen_in_background(self):
        """
        Background thread for continuous speech recognition.
        """
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                while not self.stop_listening_event.is_set():
                    try:
                        # Listen for speech with a timeout
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                        
                        # Recognize speech using Google Speech Recognition
                        text = self.recognizer.recognize_google(audio, language=self.language)
                        
                        logger.info(f"Background recognized: {text}")
                        
                        # Call the callback with the recognized text
                        if self.callback:
                            self.callback(text)
                    
                    except sr.WaitTimeoutError:
                        # No speech detected, continue listening
                        continue
                    
                    except sr.UnknownValueError:
                        # Speech was detected but not understood
                        logger.warning("Could not understand audio")
                        if self.callback:
                            self.callback(None)
                    
                    except sr.RequestError as e:
                        logger.error(f"Could not request results from Google Speech Recognition service: {e}")
                        if self.callback:
                            self.callback(None)
                    
                    except Exception as e:
                        logger.error(f"Error in background listening: {e}")
                        if self.callback:
                            self.callback(None)
        
        except Exception as e:
            logger.error(f"Fatal error in background listening thread: {e}")
            self.is_listening = False
    
    def stop_listening(self) -> bool:
        """
        Stop background listening.
        
        Returns:
            bool: True if background listening was stopped successfully, False otherwise.
        """
        if not self.is_listening:
            logger.warning("Not currently listening in background")
            return False
        
        self.stop_listening_event.set()
        
        if self.listening_thread and self.listening_thread.is_alive():
            self.listening_thread.join(timeout=2)
        
        self.is_listening = False
        self.callback = None
        
        logger.info("Stopped listening in background")
        return True
    
    def adjust_for_ambient_noise(self, duration: float = 1) -> bool:
        """
        Adjust the recognizer's energy threshold for ambient noise.
        
        Args:
            duration (float, optional): Duration to sample ambient noise in seconds. Defaults to 1.
        
        Returns:
            bool: True if adjustment was successful, False otherwise.
        """
        if not self.microphone_available:
            logger.error("Microphone is not available")
            return False
        
        try:
            with sr.Microphone() as source:
                logger.info(f"Adjusting for ambient noise (duration: {duration}s)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
                logger.info(f"Adjusted energy threshold to {self.recognizer.energy_threshold}")
                return True
        
        except Exception as e:
            logger.error(f"Failed to adjust for ambient noise: {e}")
            return False
    
    def set_energy_threshold(self, threshold: int) -> bool:
        """
        Set the energy threshold for speech detection.
        
        Args:
            threshold (int): Energy threshold value.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.recognizer.energy_threshold = threshold
            logger.info(f"Set energy threshold to {threshold}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to set energy threshold: {e}")
            return False
    
    def set_dynamic_energy_threshold(self, dynamic: bool) -> bool:
        """
        Set whether to use dynamic energy threshold.
        
        Args:
            dynamic (bool): Whether to use dynamic energy threshold.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.recognizer.dynamic_energy_threshold = dynamic
            logger.info(f"Set dynamic energy threshold to {dynamic}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to set dynamic energy threshold: {e}")
            return False
    
    def set_pause_threshold(self, threshold: float) -> bool:
        """
        Set the pause threshold for speech detection.
        
        Args:
            threshold (float): Pause threshold in seconds.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.recognizer.pause_threshold = threshold
            logger.info(f"Set pause threshold to {threshold}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to set pause threshold: {e}")
            return False

class WakeWordDetector:
    """
    Class for wake word detection.
    """
    
    def __init__(self, wake_words: List[str] = None, threshold: float = 0.5):
        """
        Initialize the wake word detector.
        
        Args:
            wake_words (List[str], optional): List of wake words to detect. Defaults to ["jarvis", "hey jarvis"].
            threshold (float, optional): Confidence threshold for wake word detection. Defaults to 0.5.
        """
        self.wake_words = wake_words or ["jarvis", "hey jarvis"]
        self.threshold = threshold
        self.speech_recognizer = SpeechRecognition()
        
        # Background detection variables
        self.is_detecting = False
        self.stop_detecting_event = threading.Event()
        self.detecting_thread = None
        self.callback = None
        
        logger.info("Wake word detector initialized")
        logger.info(f"Wake words: {self.wake_words}")
        logger.info(f"Threshold: {self.threshold}")
    
    def detect_once(self, timeout: int = 5) -> Optional[str]:
        """
        Listen once for a wake word.
        
        Args:
            timeout (int, optional): How long to wait for speech to start (seconds). Defaults to 5.
        
        Returns:
            Optional[str]: Detected wake word, or None if no wake word was detected.
        """
        text = self.speech_recognizer.listen(timeout=timeout, phrase_time_limit=3)
        
        if text:
            text = text.lower()
            
            for wake_word in self.wake_words:
                if wake_word in text:
                    logger.info(f"Wake word detected: {wake_word}")
                    return wake_word
        
        return None
    
    def start_detection(self, callback: Callable[[str], None]) -> bool:
        """
        Start continuous wake word detection in the background.
        
        Args:
            callback (Callable[[str], None]): Function to call when a wake word is detected.
        
        Returns:
            bool: True if detection was started successfully, False otherwise.
        """
        if self.is_detecting:
            logger.warning("Already detecting wake words")
            return False
        
        self.callback = callback
        self.stop_detecting_event.clear()
        self.detecting_thread = threading.Thread(target=self._detect_in_background, daemon=True)
        self.detecting_thread.start()
        self.is_detecting = True
        
        logger.info("Started wake word detection")
        return True
    
    def _detect_in_background(self):
        """
        Background thread for continuous wake word detection.
        """
        def process_speech(text: Optional[str]):
            if text:
                text = text.lower()
                
                for wake_word in self.wake_words:
                    if wake_word in text:
                        logger.info(f"Wake word detected: {wake_word}")
                        
                        # Call the callback with the detected wake word
                        if self.callback:
                            self.callback(wake_word)
                        
                        break
        
        # Start background speech recognition
        self.speech_recognizer.start_listening_in_background(process_speech)
        
        # Wait for stop signal
        while not self.stop_detecting_event.is_set():
            time.sleep(0.1)
        
        # Stop background speech recognition
        self.speech_recognizer.stop_listening()
    
    def stop_detection(self) -> bool:
        """
        Stop wake word detection.
        
        Returns:
            bool: True if detection was stopped successfully, False otherwise.
        """
        if not self.is_detecting:
            logger.warning("Not currently detecting wake words")
            return False
        
        self.stop_detecting_event.set()
        
        if self.detecting_thread and self.detecting_thread.is_alive():
            self.detecting_thread.join(timeout=2)
        
        self.is_detecting = False
        self.callback = None
        
        logger.info("Stopped wake word detection")
        return True
    
    def add_wake_word(self, wake_word: str) -> bool:
        """
        Add a new wake word to the list.
        
        Args:
            wake_word (str): Wake word to add.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        wake_word = wake_word.lower()
        
        if wake_word in self.wake_words:
            logger.warning(f"Wake word '{wake_word}' already exists")
            return False
        
        self.wake_words.append(wake_word)
        logger.info(f"Added wake word: {wake_word}")
        return True
    
    def remove_wake_word(self, wake_word: str) -> bool:
        """
        Remove a wake word from the list.
        
        Args:
            wake_word (str): Wake word to remove.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        wake_word = wake_word.lower()
        
        if wake_word not in self.wake_words:
            logger.warning(f"Wake word '{wake_word}' does not exist")
            return False
        
        self.wake_words.remove(wake_word)
        logger.info(f"Removed wake word: {wake_word}")
        return True
    
    def set_threshold(self, threshold: float) -> bool:
        """
        Set the confidence threshold for wake word detection.
        
        Args:
            threshold (float): Confidence threshold (0.0 to 1.0).
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            threshold = max(0.0, min(1.0, threshold))  # Ensure threshold is between 0.0 and 1.0
            self.threshold = threshold
            logger.info(f"Set threshold to {threshold}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to set threshold: {e}")
            return False

class VoiceAssistant:
    """
    Main class for voice assistant functionality, combining speech synthesis, recognition, and wake word detection.
    """
    
    def __init__(self, name: str = "Jarvis", language: str = "en-US", use_wake_word: bool = True):
        """
        Initialize the voice assistant.
        
        Args:
            name (str, optional): Name of the assistant. Defaults to "Jarvis".
            language (str, optional): Language code for recognition. Defaults to "en-US".
            use_wake_word (bool, optional): Whether to use wake word detection. Defaults to True.
        """
        self.name = name
        self.language = language
        self.use_wake_word = use_wake_word
        
        # Initialize components
        self.speech_synthesis = SpeechSynthesis()
        self.speech_recognition = SpeechRecognition(language=language)
        
        if use_wake_word:
            self.wake_word_detector = WakeWordDetector(wake_words=[name.lower(), f"hey {name.lower()}"])
        else:
            self.wake_word_detector = None
        
        # State variables
        self.is_active = False
        self.is_listening = False
        self.command_callback = None
        
        logger.info(f"Voice assistant '{name}' initialized")
        logger.info(f"Language: {language}")
        logger.info(f"Use wake word: {use_wake_word}")
    
    def start(self) -> bool:
        """
        Start the voice assistant.
        
        Returns:
            bool: True if started successfully, False otherwise.
        """
        if self.is_active:
            logger.warning("Voice assistant is already active")
            return False
        
        self.is_active = True
        
        # Announce that the assistant is starting
        startup_message = f"{self.name} is now online. How can I help you?"
        self.speech_synthesis.speak(startup_message)
        
        # Start wake word detection if enabled
        if self.use_wake_word and self.wake_word_detector:
            self.wake_word_detector.start_detection(self._on_wake_word_detected)
        
        logger.info("Voice assistant started")
        return True
    
    def stop(self) -> bool:
        """
        Stop the voice assistant.
        
        Returns:
            bool: True if stopped successfully, False otherwise.
        """
        if not self.is_active:
            logger.warning("Voice assistant is not active")
            return False
        
        # Stop listening for commands if active
        if self.is_listening:
            self.stop_listening()
        
        # Stop wake word detection if enabled
        if self.use_wake_word and self.wake_word_detector:
            self.wake_word_detector.stop_detection()
        
        # Announce that the assistant is stopping
        shutdown_message = f"{self.name} is shutting down. Goodbye."
        self.speech_synthesis.speak(shutdown_message, block=True)
        
        # Stop speech synthesis
        self.speech_synthesis.stop()
        
        self.is_active = False
        
        logger.info("Voice assistant stopped")
        return True
    
    def _on_wake_word_detected(self, wake_word: str):
        """
        Callback function for wake word detection.
        
        Args:
            wake_word (str): Detected wake word.
        """
        logger.info(f"Wake word detected: {wake_word}")
        
        # Acknowledge the wake word
        self.speech_synthesis.speak(f"Yes?", block=True)
        
        # Start listening for a command
        self.start_listening()
    
    def start_listening(self) -> bool:
        """
        Start listening for commands.
        
        Returns:
            bool: True if started successfully, False otherwise.
        """
        if self.is_listening:
            logger.warning("Already listening for commands")
            return False
        
        # Define the callback function for speech recognition
        def on_speech_recognized(text: Optional[str]):
            if text:
                logger.info(f"Command recognized: {text}")
                
                # Process the command
                if self.command_callback:
                    response = self.command_callback(text)
                    
                    # Speak the response if provided
                    if response:
                        self.speech_synthesis.speak(response)
                
                # Stop listening after processing the command
                self.stop_listening()
            else:
                # If speech recognition failed, inform the user
                self.speech_synthesis.speak("I didn't catch that. Could you please repeat?")
                
                # Continue listening
                self.speech_recognition.stop_listening()
                time.sleep(0.5)
                self.speech_recognition.start_listening_in_background(on_speech_recognized)
        
        # Start listening for commands
        success = self.speech_recognition.start_listening_in_background(on_speech_recognized)
        
        if success:
            self.is_listening = True
            logger.info("Started listening for commands")
        
        return success
    
    def stop_listening(self) -> bool:
        """
        Stop listening for commands.
        
        Returns:
            bool: True if stopped successfully, False otherwise.
        """
        if not self.is_listening:
            logger.warning("Not currently listening for commands")
            return False
        
        success = self.speech_recognition.stop_listening()
        
        if success:
            self.is_listening = False
            logger.info("Stopped listening for commands")
        
        return success
    
    def set_command_callback(self, callback: Callable[[str], Optional[str]]) -> bool:
        """
        Set the callback function for command processing.
        
        Args:
            callback (Callable[[str], Optional[str]]): Function to call with recognized commands.
                                                     Should return a response string or None.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.command_callback = callback
            logger.info("Set command callback function")
            return True
        
        except Exception as e:
            logger.error(f"Failed to set command callback: {e}")
            return False
    
    def say(self, text: str, block: bool = False) -> bool:
        """
        Speak a message.
        
        Args:
            text (str): Text to speak.
            block (bool, optional): Whether to block until speech is complete. Defaults to False.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self.speech_synthesis.speak(text, block=block)
    
    def listen_once(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen once for a command.
        
        Args:
            timeout (int, optional): How long to wait for speech to start (seconds). Defaults to 5.
            phrase_time_limit (int, optional): Maximum length of speech to process (seconds). Defaults to 10.
        
        Returns:
            Optional[str]: Recognized text, or None if no speech was detected or recognition failed.
        """
        return self.speech_recognition.listen(timeout=timeout, phrase_time_limit=phrase_time_limit)
    
    def process_command(self, command: str) -> Optional[str]:
        """
        Process a command directly (without voice recognition).
        
        Args:
            command (str): Command to process.
        
        Returns:
            Optional[str]: Response to the command, or None if no response is needed.
        """
        if self.command_callback:
            return self.command_callback(command)
        else:
            logger.warning("No command callback function set")
            return "I'm not sure how to process that command."
    
    def change_voice(self, voice_index: int) -> bool:
        """
        Change the voice of the assistant.
        
        Args:
            voice_index (int): Index of the voice to use.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self.speech_synthesis.set_voice_by_index(voice_index)
    
    def get_available_voices(self) -> List[Dict[str, str]]:
        """
        Get a list of available voices.
        
        Returns:
            List[Dict[str, str]]: List of dictionaries with voice information.
        """
        return self.speech_synthesis.get_voices()
    
    def set_speech_rate(self, rate: int) -> bool:
        """
        Set the speech rate.
        
        Args:
            rate (int): Speech rate (words per minute). Normal is around 150-200.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self.speech_synthesis.set_rate(rate)
    
    def set_speech_volume(self, volume: float) -> bool:
        """
        Set the speech volume.
        
        Args:
            volume (float): Volume level (0.0 to 1.0).
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self.speech_synthesis.set_volume(volume)
    
    def add_wake_word(self, wake_word: str) -> bool:
        """
        Add a new wake word.
        
        Args:
            wake_word (str): Wake word to add.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.use_wake_word or not self.wake_word_detector:
            logger.warning("Wake word detection is not enabled")
            return False
        
        return self.wake_word_detector.add_wake_word(wake_word)
    
    def remove_wake_word(self, wake_word: str) -> bool:
        """
        Remove a wake word.
        
        Args:
            wake_word (str): Wake word to remove.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.use_wake_word or not self.wake_word_detector:
            logger.warning("Wake word detection is not enabled")
            return False
        
        return self.wake_word_detector.remove_wake_word(wake_word)
    
    def get_wake_words(self) -> List[str]:
        """
        Get the list of wake words.
        
        Returns:
            List[str]: List of wake words, or empty list if wake word detection is not enabled.
        """
        if not self.use_wake_word or not self.wake_word_detector:
            return []
        
        return self.wake_word_detector.wake_words

def main():
    """
    Main function for testing the voice control module.
    """
    # Initialize the voice assistant
    assistant = VoiceAssistant(name="Jarvis")
    
    # Define a simple command processor
    def process_command(command: str) -> str:
        command = command.lower()
        
        if "hello" in command or "hi" in command:
            return "Hello! How can I help you today?"
        
        elif "time" in command:
            current_time = time.strftime("%I:%M %p")
            return f"The current time is {current_time}."
        
        elif "date" in command:
            current_date = time.strftime("%A, %B %d, %Y")
            return f"Today is {current_date}."
        
        elif "weather" in command:
            # This would normally call a weather API
            return "I'm sorry, I don't have access to weather information at the moment."
        
        elif "goodbye" in command or "bye" in command:
            return "Goodbye! Have a great day!"
        
        else:
            return "I'm not sure how to help with that. Could you try a different command?"
    
    # Set the command processor
    assistant.set_command_callback(process_command)
    
    # Start the assistant
    assistant.start()
    
    try:
        # Keep the program running
        print("Voice assistant is running. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nStopping voice assistant...")
        assistant.stop()
        print("Voice assistant stopped.")

if __name__ == "__main__":
    main()

