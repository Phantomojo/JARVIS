#!/usr/bin/env python3
"""
DeepSeek R1 Integration Module
This script provides functions to interact with DeepSeek R1 through Ollama.
"""

import os
import sys
import json
import requests
import time
import threading
from typing import Dict, List, Optional, Union, Callable, Generator

class DeepSeekIntegration:
    def __init__(self, model_name: str = "deepseek-r1:8b", ollama_host: str = "http://localhost:11434"):
        """
        Initialize the DeepSeek R1 integration.
        
        Args:
            model_name (str, optional): The name of the DeepSeek model to use. Defaults to "deepseek-r1:8b".
            ollama_host (str, optional): The Ollama host URL. Defaults to "http://localhost:11434".
        """
        self.model_name = model_name
        self.ollama_host = ollama_host.rstrip("/")
        self.generate_url = f"{self.ollama_host}/api/generate"
        self.chat_url = f"{self.ollama_host}/api/chat"
        self.models_url = f"{self.ollama_host}/api/tags"
        
        # Check if Ollama is running and the model is available
        self.is_available = self._check_model_availability()
    
    def _check_model_availability(self) -> bool:
        """
        Check if Ollama is running and the specified model is available.
        
        Returns:
            bool: True if the model is available, False otherwise.
        """
        try:
            response = requests.get(self.models_url)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                
                # Check if the model is available (exact match or prefix match)
                model_prefix = self.model_name.split(":")[0]
                for name in model_names:
                    if name == self.model_name or name.startswith(f"{model_prefix}:"):
                        return True
                
                print(f"Model {self.model_name} not found. Available models: {', '.join(model_names)}")
                return False
            else:
                print(f"Failed to get models list: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("Ollama is not running. Please start Ollama and try again.")
            return False
        except Exception as e:
            print(f"Error checking model availability: {e}")
            return False
    
    def pull_model(self) -> bool:
        """
        Pull the specified model if it's not already available.
        
        Returns:
            bool: True if the model was pulled successfully or is already available, False otherwise.
        """
        if self.is_available:
            return True
        
        try:
            print(f"Pulling model {self.model_name}...")
            response = requests.post(
                f"{self.ollama_host}/api/pull",
                json={"name": self.model_name}
            )
            
            if response.status_code == 200:
                print(f"Model {self.model_name} pulled successfully.")
                self.is_available = True
                return True
            else:
                print(f"Failed to pull model: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error pulling model: {e}")
            return False
    
    def generate(self, prompt: str, **kwargs) -> Optional[str]:
        """
        Generate a response for a single prompt.
        
        Args:
            prompt (str): The prompt to send to the model.
            **kwargs: Additional parameters to pass to the model.
                - temperature (float): Controls randomness. Higher values (e.g., 0.8) make output more random, 
                  lower values (e.g., 0.2) make it more deterministic. Default is 0.7.
                - max_tokens (int): Maximum number of tokens to generate. Default is 2048.
                - top_p (float): Controls diversity via nucleus sampling. Default is 0.9.
                - top_k (int): Controls diversity via top-k sampling. Default is 40.
                - stop (List[str]): List of strings that stop generation when encountered.
        
        Returns:
            Optional[str]: The generated response or None if generation failed.
        """
        if not self.is_available and not self.pull_model():
            return None
        
        try:
            # Prepare request data
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            
            # Add optional parameters
            if "temperature" in kwargs:
                data["temperature"] = kwargs["temperature"]
            if "max_tokens" in kwargs:
                data["max_tokens"] = kwargs["max_tokens"]
            if "top_p" in kwargs:
                data["top_p"] = kwargs["top_p"]
            if "top_k" in kwargs:
                data["top_k"] = kwargs["top_k"]
            if "stop" in kwargs:
                data["stop"] = kwargs["stop"]
            
            # Send request
            response = requests.post(self.generate_url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                print(f"Generation failed with status code {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def generate_stream(self, prompt: str, callback: Callable[[str], None], **kwargs) -> bool:
        """
        Generate a response for a single prompt with streaming output.
        
        Args:
            prompt (str): The prompt to send to the model.
            callback (Callable[[str], None]): Function to call with each chunk of the response.
            **kwargs: Additional parameters to pass to the model.
        
        Returns:
            bool: True if generation was successful, False otherwise.
        """
        if not self.is_available and not self.pull_model():
            return False
        
        try:
            # Prepare request data
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": True
            }
            
            # Add optional parameters
            if "temperature" in kwargs:
                data["temperature"] = kwargs["temperature"]
            if "max_tokens" in kwargs:
                data["max_tokens"] = kwargs["max_tokens"]
            if "top_p" in kwargs:
                data["top_p"] = kwargs["top_p"]
            if "top_k" in kwargs:
                data["top_k"] = kwargs["top_k"]
            if "stop" in kwargs:
                data["stop"] = kwargs["stop"]
            
            # Send request
            response = requests.post(self.generate_url, json=data, stream=True)
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            if "response" in chunk:
                                callback(chunk["response"])
                        except json.JSONDecodeError:
                            print(f"Failed to decode JSON: {line}")
                return True
            else:
                print(f"Streaming generation failed with status code {response.status_code}")
                print(response.text)
                return False
        except Exception as e:
            print(f"Error in streaming generation: {e}")
            return False
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Optional[Dict[str, str]]:
        """
        Generate a response for a chat conversation.
        
        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content' keys.
                Example: [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]
            **kwargs: Additional parameters to pass to the model.
        
        Returns:
            Optional[Dict[str, str]]: The generated response message or None if generation failed.
        """
        if not self.is_available and not self.pull_model():
            return None
        
        try:
            # Prepare request data
            data = {
                "model": self.model_name,
                "messages": messages,
                "stream": False
            }
            
            # Add optional parameters
            if "temperature" in kwargs:
                data["temperature"] = kwargs["temperature"]
            if "max_tokens" in kwargs:
                data["max_tokens"] = kwargs["max_tokens"]
            if "top_p" in kwargs:
                data["top_p"] = kwargs["top_p"]
            if "top_k" in kwargs:
                data["top_k"] = kwargs["top_k"]
            if "stop" in kwargs:
                data["stop"] = kwargs["stop"]
            
            # Send request
            response = requests.post(self.chat_url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {})
            else:
                print(f"Chat generation failed with status code {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"Error in chat generation: {e}")
            return None
    
    def chat_stream(self, messages: List[Dict[str, str]], callback: Callable[[str], None], **kwargs) -> bool:
        """
        Generate a response for a chat conversation with streaming output.
        
        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content' keys.
            callback (Callable[[str], None]): Function to call with each chunk of the response.
            **kwargs: Additional parameters to pass to the model.
        
        Returns:
            bool: True if generation was successful, False otherwise.
        """
        if not self.is_available and not self.pull_model():
            return False
        
        try:
            # Prepare request data
            data = {
                "model": self.model_name,
                "messages": messages,
                "stream": True
            }
            
            # Add optional parameters
            if "temperature" in kwargs:
                data["temperature"] = kwargs["temperature"]
            if "max_tokens" in kwargs:
                data["max_tokens"] = kwargs["max_tokens"]
            if "top_p" in kwargs:
                data["top_p"] = kwargs["top_p"]
            if "top_k" in kwargs:
                data["top_k"] = kwargs["top_k"]
            if "stop" in kwargs:
                data["stop"] = kwargs["stop"]
            
            # Send request
            response = requests.post(self.chat_url, json=data, stream=True)
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            if "message" in chunk and "content" in chunk["message"]:
                                callback(chunk["message"]["content"])
                        except json.JSONDecodeError:
                            print(f"Failed to decode JSON: {line}")
                return True
            else:
                print(f"Streaming chat generation failed with status code {response.status_code}")
                print(response.text)
                return False
        except Exception as e:
            print(f"Error in streaming chat generation: {e}")
            return False

class AgentSystem:
    """
    A simple agent system that uses DeepSeek R1 for autonomous task execution.
    """
    
    def __init__(self, model_name: str = "deepseek-r1:8b"):
        """
        Initialize the agent system.
        
        Args:
            model_name (str, optional): The name of the DeepSeek model to use. Defaults to "deepseek-r1:8b".
        """
        self.deepseek = DeepSeekIntegration(model_name)
        self.conversation_history = []
        self.system_prompt = """You are an autonomous AI agent that can help users with various tasks. 
You can understand complex instructions and break them down into steps.
You should always think step by step and explain your reasoning.
When you need to perform a specific action, clearly indicate what you're doing.
"""
    
    def add_message(self, role: str, content: str):
        """
        Add a message to the conversation history.
        
        Args:
            role (str): The role of the message sender ("system", "user", or "assistant").
            content (str): The content of the message.
        """
        self.conversation_history.append({"role": role, "content": content})
    
    def reset_conversation(self):
        """
        Reset the conversation history, keeping only the system prompt.
        """
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
    
    def initialize(self):
        """
        Initialize the agent system.
        
        Returns:
            bool: True if initialization was successful, False otherwise.
        """
        if not self.deepseek.is_available and not self.deepseek.pull_model():
            return False
        
        # Reset conversation and add system prompt
        self.reset_conversation()
        return True
    
    def process_request(self, user_request: str, callback: Optional[Callable[[str], None]] = None) -> Optional[str]:
        """
        Process a user request and generate a response.
        
        Args:
            user_request (str): The user's request.
            callback (Optional[Callable[[str], None]], optional): Function to call with each chunk of the response
                                                                 if streaming is desired.
        
        Returns:
            Optional[str]: The generated response or None if processing failed.
        """
        # Add user message to conversation history
        self.add_message("user", user_request)
        
        # If callback is provided, use streaming
        if callback:
            success = self.deepseek.chat_stream(
                self.conversation_history,
                callback,
                temperature=0.7,
                max_tokens=2048
            )
            
            if success:
                # We need to get the full response to add to history
                # This is a bit inefficient but necessary for maintaining context
                response = self.deepseek.chat(
                    self.conversation_history,
                    temperature=0.7,
                    max_tokens=2048
                )
                
                if response and "content" in response:
                    self.add_message("assistant", response["content"])
                    return response["content"]
                return None
            else:
                return None
        else:
            # Non-streaming response
            response = self.deepseek.chat(
                self.conversation_history,
                temperature=0.7,
                max_tokens=2048
            )
            
            if response and "content" in response:
                self.add_message("assistant", response["content"])
                return response["content"]
            return None
    
    def execute_task(self, task_description: str, callback: Optional[Callable[[str], None]] = None) -> Optional[str]:
        """
        Execute a specific task.
        
        Args:
            task_description (str): Description of the task to execute.
            callback (Optional[Callable[[str], None]], optional): Function to call with progress updates.
        
        Returns:
            Optional[str]: The result of the task execution or None if execution failed.
        """
        # Construct a prompt that instructs the model to execute the task
        prompt = f"""I need to execute the following task: {task_description}

Please help me break this down into steps and execute it. For each step, explain what you're doing and why.
"""
        
        return self.process_request(prompt, callback)

def main():
    """
    Main function for testing the DeepSeek R1 integration.
    """
    # Test the basic integration
    deepseek = DeepSeekIntegration()
    
    if deepseek.is_available:
        print("DeepSeek R1 model is available.")
        
        # Test simple generation
        prompt = "Explain the concept of autonomous AI agents in 3 sentences."
        print(f"\nGenerating response for prompt: {prompt}")
        
        response = deepseek.generate(prompt)
        if response:
            print("Generated response:")
            print(response)
        else:
            print("Generation failed.")
        
        # Test chat
        print("\nTesting chat functionality:")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What are the key components of an autonomous AI agent?"}
        ]
        
        response = deepseek.chat(messages)
        if response and "content" in response:
            print("Chat response:")
            print(response["content"])
        else:
            print("Chat generation failed.")
        
        # Test agent system
        print("\nTesting agent system:")
        agent = AgentSystem()
        
        if agent.initialize():
            print("Agent system initialized successfully.")
            
            # Test processing a request
            request = "Create a plan for building a simple weather app."
            print(f"\nProcessing request: {request}")
            
            def print_chunk(chunk):
                print(chunk, end="", flush=True)
            
            response = agent.process_request(request, print_chunk)
            if response:
                print("\n\nFull response stored in conversation history.")
            else:
                print("\n\nRequest processing failed.")
        else:
            print("Failed to initialize agent system.")
    else:
        print("DeepSeek R1 model is not available.")
        print("Please make sure Ollama is running and the model is installed.")
        print("You can install the model with: ollama pull deepseek-r1:8b")

if __name__ == "__main__":
    main()

