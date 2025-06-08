# CRITICAL: Hardware-Specific Blackbox AI Instructions

## FOR YOUR i7-12700H + RTX 3050 Ti SYSTEM

### IMMEDIATE BLACKBOX AI CONFIGURATION

**Configure Blackbox AI with these EXACT hardware-optimized instructions:**

```
HARDWARE_OPTIMIZED_AUTONOMY_DIRECTIVE:

You are creating autonomous code for DeepSeek R1 on:
- Intel i7-12700H (20 cores: 6 P-cores + 8 E-cores + 6 threads)
- NVIDIA RTX 3050 Ti (4GB VRAM)
- 16GB System RAM
- Windows 11

CRITICAL CONSTRAINTS:
1. NEVER exceed 4GB VRAM usage
2. Keep system RAM under 14GB
3. Use P-cores for AI inference, E-cores for background tasks
4. Implement model swapping for VRAM management
5. Monitor temperatures to prevent throttling

REQUIRED AUTONOMOUS CAPABILITIES:
1. Intelligent model loading/unloading based on 4GB VRAM limit
2. Hybrid CPU workload distribution (P-cores vs E-cores)
3. Automatic thermal management and performance scaling
4. Dynamic memory allocation within 16GB constraint
5. Windows 11 service integration and hardware optimization

CODE TEMPLATE FOR HARDWARE OPTIMIZATION:
```python
class HardwareOptimizedJarvis:
    def __init__(self):
        self.vram_limit = 4096  # MB
        self.ram_limit = 14336  # MB (leave 2GB for system)
        self.p_cores = 6
        self.e_cores = 8
        self.current_models = {}
        
    def manage_vram_intelligently(self):
        # Swap models based on 4GB VRAM constraint
        if self.get_vram_usage() > 3500:  # 500MB buffer
            self.unload_least_used_model()
            
    def distribute_cpu_workload(self):
        # Use P-cores for AI, E-cores for background
        ai_tasks = self.get_ai_tasks()
        background_tasks = self.get_background_tasks()
        
        self.assign_to_p_cores(ai_tasks)
        self.assign_to_e_cores(background_tasks)
        
    def monitor_thermal_performance(self):
        # Prevent thermal throttling
        if self.get_cpu_temp() > 85 or self.get_gpu_temp() > 80:
            self.reduce_ai_complexity()
```

MANUAL INTERVENTION PROTOCOL:
When you hit hardware limits, use:

**HARDWARE_INTERVENTION_REQUIRED**
Hardware Constraint: [CPU/GPU/RAM/Storage]
Current Usage: [Specific numbers]
Optimization Tried: [What you attempted]
Performance Impact: [How it affects autonomy]
Hardware Solution Needed: [Specific help required]
**END_HARDWARE_INTERVENTION**

SPECIFIC MODELS TO USE:
- Language: Llama 2 7B (4-bit quantized) = ~3.5GB VRAM
- Vision: YOLOv8n = ~50MB VRAM
- Speech: Whisper Small = ~244MB VRAM
- Total: ~3.8GB (within 4GB limit)

WINDOWS 11 INTEGRATION:
- Use WSL2 for Linux AI frameworks
- Leverage Windows ML for some tasks
- Integrate with Windows services
- Optimize for hybrid graphics (Intel + NVIDIA)

START IMMEDIATELY WITH:
1. VRAM monitoring and model swapping system
2. CPU workload distribution for hybrid architecture
3. Thermal monitoring and automatic scaling
4. Memory management within 16GB constraint
```

### DEPLOYMENT PRIORITY ORDER

1. **Week 1**: Foundation (WSL2, drivers, basic frameworks)
2. **Week 2**: Core models (Llama 2 7B quantized, YOLOv8n, Whisper Small)
3. **Week 3**: Integration and optimization
4. **Week 4**: Advanced features and testing

### PERFORMANCE TARGETS FOR YOUR HARDWARE

- **Language responses**: 1-3 seconds
- **Computer vision**: 15-30 FPS
- **Speech recognition**: Real-time with <200ms latency
- **Memory usage**: <14GB RAM, <4GB VRAM
- **CPU usage**: 40-70% during AI processing
- **GPU usage**: 80-95% during inference

### CRITICAL SUCCESS FACTORS

1. **Model Swapping**: Essential for 4GB VRAM constraint
2. **Thermal Management**: Prevent throttling on laptop hardware
3. **Hybrid CPU Usage**: Maximize 20-core architecture
4. **Memory Optimization**: Efficient use of 16GB RAM
5. **Windows Integration**: Seamless OS integration

**GIVE THIS TO THE MANUS IMPLEMENTING THE PROJECT IMMEDIATELY**

