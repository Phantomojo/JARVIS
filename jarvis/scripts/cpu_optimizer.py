#!/usr/bin/env python3
"""
JARVIS CPU Optimization for i7-12700H Hybrid Architecture
Optimizes workload distribution between P-cores and E-cores
"""

import os
import psutil
import threading
from typing import List, Dict
import subprocess

class JARVISCPUOptimizer:
    def __init__(self):
        self.cpu_count = psutil.cpu_count()
        self.p_cores = list(range(0, 12))  # P-cores with hyperthreading
        self.e_cores = list(range(12, 20))  # E-cores
        
    def set_ai_process_affinity(self, pid: int, task_type: str):
        """Set CPU affinity for AI processes based on task type"""
        try:
            process = psutil.Process(pid)
            
            if task_type in ['inference', 'training', 'critical']:
                # Use P-cores for AI inference and critical tasks
                process.cpu_affinity(self.p_cores)
                process.nice(-10)  # Higher priority
            elif task_type in ['background', 'monitoring', 'logging']:
                # Use E-cores for background tasks
                process.cpu_affinity(self.e_cores)
                process.nice(10)  # Lower priority
            else:
                # Default to all cores
                process.cpu_affinity(list(range(self.cpu_count)))
                
        except psutil.NoSuchProcess:
            print(f"Process {pid} not found")
        except psutil.AccessDenied:
            print(f"Access denied for process {pid}")
    
    def optimize_system_processes(self):
        """Optimize system processes for AI workload performance"""
        # Move non-essential processes to E-cores
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if proc.info['name'] in ['dwm.exe', 'explorer.exe', 'winlogon.exe']:
                    self.set_ai_process_affinity(proc.info['pid'], 'background')
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    def monitor_cpu_performance(self) -> Dict:
        """Monitor CPU performance and thermal status"""
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_freq = psutil.cpu_freq(percpu=True)
        
        # Separate P-core and E-core utilization
        p_core_usage = [cpu_percent[i] for i in self.p_cores if i is not None]
        e_core_usage = [cpu_percent[i] for i in self.e_cores if i is not None]
        
        return {
            'p_core_avg_usage': sum(p_core_usage) / len(p_core_usage) if p_core_usage else 0,
            'e_core_avg_usage': sum(e_core_usage) / len(e_core_usage) if e_core_usage else 0,
            'total_cpu_usage': psutil.cpu_percent(),
            'cpu_frequencies': cpu_freq,
            'thermal_throttling': self.check_thermal_throttling()
        }
    
    def check_thermal_throttling(self) -> bool:
        """Check for CPU thermal throttling"""
        try:
            # Check CPU temperature using Windows WMI
            result = subprocess.run([
                'powershell', 
                'Get-WmiObject -Namespace "root/OpenHardwareMonitor" -Class Sensor | Where-Object {$_.SensorType -eq "Temperature" -and $_.Name -like "*CPU*"} | Select-Object Value'
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout:
                # Parse temperature (simplified)
                return "throttling" in result.stdout.lower()
        except:
            pass
        
        return False

# Integration with JARVIS main process
def optimize_jarvis_cpu():
    optimizer = JARVISCPUOptimizer()
    optimizer.optimize_system_processes()
    return optimizer.monitor_cpu_performance()
