"""
Performance Monitoring Dashboard for JARVIS AI System
Collects and displays real-time metrics from GPU, CPU, and Memory optimizers
"""

import time
import threading
from typing import Dict, Any

from jarvis.scripts.gpu_optimizer import JARVISGPUOptimizer
from jarvis.scripts.cpu_optimizer import JARVISCPUOptimizer
from jarvis.scripts.memory_manager import MemoryManager

class PerformanceDashboard:
    def __init__(self, refresh_interval: float = 2.0):
        self.gpu_optimizer = JARVISGPUOptimizer()
        self.cpu_optimizer = JARVISCPUOptimizer()
        self.memory_manager = MemoryManager()
        self.refresh_interval = refresh_interval
        self.running = False

    def collect_metrics(self) -> Dict[str, Any]:
        gpu_status = self.gpu_optimizer.get_gpu_status()
        cpu_status = self.cpu_optimizer.monitor_cpu_performance()
        ram_usage = self.memory_manager.get_ram_usage_mb()
        return {
            "GPU Memory Used (GB)": round(gpu_status['memory_used_gb'], 2),
            "GPU Utilization (%)": gpu_status['gpu_utilization'],
            "GPU Temperature (C)": gpu_status['temperature_c'],
            "CPU P-Core Avg Usage (%)": round(cpu_status['p_core_avg_usage'], 2),
            "CPU E-Core Avg Usage (%)": round(cpu_status['e_core_avg_usage'], 2),
            "Total CPU Usage (%)": round(cpu_status['total_cpu_usage'], 2),
            "RAM Usage (MB)": round(ram_usage, 2)
        }

    def display_metrics(self):
        while self.running:
            metrics = self.collect_metrics()
            print("\n=== JARVIS Performance Dashboard ===")
            for key, value in metrics.items():
                print(f"{key}: {value}")
            time.sleep(self.refresh_interval)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.display_metrics)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

if __name__ == "__main__":
    dashboard = PerformanceDashboard()
    try:
        dashboard.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        dashboard.stop()
        print("\nPerformance dashboard stopped.")
