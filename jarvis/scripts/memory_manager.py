#!/usr/bin/env python3
"""
JARVIS Intelligent Memory Management
Manages dynamic memory allocation and model loading/unloading within 16GB RAM constraint
"""

import psutil
import gc
import time
from typing import Dict, List

class MemoryManager:
    def __init__(self):
        self.ram_limit_mb = 16384  # 16GB
        self.system_reserved_mb = 4096  # 4GB reserved for system
        self.ai_available_mb = self.ram_limit_mb - self.system_reserved_mb
        self.loaded_models = {}
        self.model_usage_stats = {}

    def get_ram_usage_mb(self) -> float:
        """Get current RAM usage in MB"""
        mem = psutil.virtual_memory()
        used_mb = (mem.total - mem.available) / (1024 * 1024)
        return used_mb

    def can_load_model(self, model_name: str, model_size_mb: float) -> bool:
        """Check if there is enough RAM to load the model"""
        current_usage = self.get_ram_usage_mb()
        if current_usage + model_size_mb < self.ai_available_mb:
            return True
        return False

    def load_model(self, model_name: str, model_size_mb: float):
        """Load model if enough memory, else unload least used models"""
        if self.can_load_model(model_name, model_size_mb):
            self.loaded_models[model_name] = model_size_mb
            self.model_usage_stats[model_name] = time.time()
            print(f"Model {model_name} loaded.")
        else:
            self.unload_least_used_model()
            if self.can_load_model(model_name, model_size_mb):
                self.loaded_models[model_name] = model_size_mb
                self.model_usage_stats[model_name] = time.time()
                print(f"Model {model_name} loaded after unloading.")
            else:
                print(f"Insufficient memory to load model {model_name}.")

    def unload_least_used_model(self):
        """Unload the least recently used model"""
        if not self.loaded_models:
            print("No models to unload.")
            return
        lru_model = min(self.model_usage_stats.keys(), key=lambda k: self.model_usage_stats[k])
        del self.loaded_models[lru_model]
        del self.model_usage_stats[lru_model]
        gc.collect()
        print(f"Model {lru_model} unloaded to free memory.")

    def update_model_usage(self, model_name: str):
        """Update usage timestamp for a model"""
        if model_name in self.model_usage_stats:
            self.model_usage_stats[model_name] = time.time()

    def monitor_memory(self):
        """Continuously monitor memory and perform cleanup if needed"""
        while True:
            used_mb = self.get_ram_usage_mb()
            if used_mb > self.ai_available_mb:
                print("Memory usage high, performing cleanup.")
                self.unload_least_used_model()
            time.sleep(5)

if __name__ == "__main__":
    manager = MemoryManager()
    # Example usage
    manager.load_model("language_model", 4000)
    manager.load_model("vision_model", 1000)
    manager.load_model("speech_model", 500)
