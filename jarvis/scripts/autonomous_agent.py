#!/usr/bin/env python3
"""
Enhanced Autonomous DeepSeek R1 Agent
Based on the JARVIS project: https://github.com/Phantomojo/JARVIS

This implementation follows the established architecture where:
- DeepSeek R1 = Brain (reasoning, planning, decision-making)
- Blackbox AI = Hands (generates code to execute tasks)
- System = Body (executes the generated code)

Hardware Target: Intel i7-12700H + RTX 3050 Ti (4GB VRAM) + 16GB RAM
"""

import json
import logging
import asyncio
import subprocess
import os
import sys
import time
import psutil
import GPUtil
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import requests
import ollama

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("jarvis_autonomous_agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("JarvisAgent")

class SafetyLevel(Enum):
    """Safety levels based on JARVIS project specifications"""
    GREEN = "green"      # Safe operations - no confirmation needed
    YELLOW = "yellow"    # Caution required - ask user first  
    RED = "red"          # Dangerous operations - explicit confirmation + warnings

class TaskType(Enum):
    """Task types that JARVIS can handle"""
    COMPUTER_CONTROL = "computer_control"
    WEB_BROWSING = "web_browsing"
    CODE_GENERATION = "code_generation"
    FILE_OPERATIONS = "file_operations"
    SYSTEM_MONITORING = "system_monitoring"
    COMMUNICATION = "communication"
    AUTOMATION = "automation"

@dataclass
class TaskStep:
    """Represents a single step in JARVIS execution plan"""
    step_id: int
    description: str
    task_type: TaskType
    blackbox_instructions: str  # Specific instructions for Blackbox AI
    expected_output: str
    safety_level: SafetyLevel
    hardware_requirements: Optional[Dict[str, Any]] = None

@dataclass
class ExecutionResult:
    """Result of executing a task step"""
    success: bool
    output: str
    error: Optional[str] = None
    generated_code: Optional[str] = None
    execution_time: float = 0.0
    vram_usage: float = 0.0
    cpu_usage: float = 0.0

class HardwareMonitor:
    """Monitor hardware constraints for RTX 3050 Ti + i7-12700H"""
    
    def __init__(self):
        self.max_vram_gb = 4.0  # RTX 3050 Ti constraint
        self.max_ram_gb = 16.0  # System RAM
        self.thermal_limit = 85  # Celsius
        
    def check_vram_usage(self) -> float:
        """Check current VRAM usage"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].memoryUsed / 1024  # Convert MB to GB
            return 0.0
        except:
            return 0.0
    
    def check_system_resources(self) -> Dict[str, float]:
        """Check system resource usage"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_percent": psutil.virtual_memory().percent,
            "ram_used_gb": psutil.virtual_memory().used / (1024**3),
            "vram_used_gb": self.check_vram_usage(),
            "temperature": self.get_cpu_temperature()
        }
    
    def get_cpu_temperature(self) -> float:
        """Get CPU temperature (if available)"""
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                return max([temp.current for temp in temps['coretemp']])
            return 0.0
        except:
            return 0.0
    
    def is_safe_to_proceed(self) -> Tuple[bool, str]:
        """Check if it's safe to proceed with resource-intensive operations"""
        resources = self.check_system_resources()
        
        if resources["vram_used_gb"] > 3.5:  # Leave 0.5GB safety margin
            return False, f"VRAM usage too high: {resources['vram_used_gb']:.1f}GB / 4.0GB"
        
        if resources["ram_percent"] > 90:
            return False, f"RAM usage too high: {resources['ram_percent']:.1f}%"
        
        if resources["temperature"] > self.thermal_limit:
            return False, f"CPU temperature too high: {resources['temperature']:.1f}°C"
        
        return True, "System resources within safe limits"

class JarvisAgent:
    """
    Main JARVIS autonomous agent following the established architecture
    """
    
    def __init__(self, ollama_host="localhost", ollama_port=11434):
        self.ollama_client = ollama.Client(host=f"http://{ollama_host}:{ollama_port}")
        self.model_name = "deepseek-r1:8b"
        self.conversation_history = []
        self.hardware_monitor = HardwareMonitor()
        self.blackbox_controller = BlackboxController()
        self.safety_monitor = SafetyMonitor()
        
        # JARVIS system prompt optimized for the established architecture
        self.system_prompt = """You are JARVIS, an autonomous AI assistant. Your role is to:

1. UNDERSTAND user requests and break them into actionable steps
2. PLAN execution using available tools and capabilities  
3. GENERATE specific instructions for Blackbox AI to write code
4. COORDINATE execution while monitoring safety and resources
5. SYNTHESIZE results and provide clear feedback

HARDWARE CONSTRAINTS (CRITICAL):
- RTX 3050 Ti: 4GB VRAM maximum
- i7-12700H: 20 threads (6 P-cores + 8 E-cores)
- 16GB RAM total
- Thermal management required

CAPABILITIES:
- Computer control (mouse, keyboard, screenshots, applications)
- Internet access (browsing, downloads, API calls, research)
- File operations (create, read, write, organize, analyze)
- System monitoring (performance, processes, resources)
- Code generation and execution via Blackbox AI
- Voice interaction and speech synthesis

SAFETY PROTOCOL:
- GREEN: Safe operations (proceed automatically)
- YELLOW: Caution required (ask user confirmation)
- RED: Dangerous operations (explicit warnings + confirmation)

For each request, respond in JSON format:
{
    "understanding": "Clear summary of what user wants",
    "resource_check": "Assessment of hardware requirements",
    "plan": [
        {
            "step_id": 1,
            "description": "What this step accomplishes",
            "task_type": "computer_control|web_browsing|code_generation|etc",
            "blackbox_instructions": "Detailed instructions for Blackbox AI to generate code",
            "expected_output": "What should happen when code executes",
            "safety_level": "green|yellow|red",
            "hardware_requirements": {"vram_gb": 0.5, "cpu_cores": 2}
        }
    ],
    "overall_goal": "Summary of complete objective",
    "estimated_time": "Expected completion time"
}"""

    async def process_request(self, user_input: str) -> str:
        """Main entry point for processing user requests"""
        logger.info(f"JARVIS processing request: {user_input}")
        
        try:
            # Check system resources first
            safe, message = self.hardware_monitor.is_safe_to_proceed()
            if not safe:
                return f"⚠️ System resources constrained: {message}. Please wait or restart JARVIS."
            
            # Use DeepSeek R1 to understand and plan
            plan = await self.create_execution_plan(user_input)
            if not plan:
                return "I couldn't understand your request. Could you please rephrase it?"
            
            # Execute the plan using Blackbox AI
            results = await self.execute_plan(plan)
            
            # Synthesize results
            final_result = await self.synthesize_results(user_input, plan, results)
            if final_result is None:
                final_result = "No summary available."
            
            # Store in history
            self.conversation_history.append({
                "user_input": user_input,
                "plan": plan,
                "results": results,
                "final_result": final_result,
                "timestamp": time.time(),
                "resources_used": self.hardware_monitor.check_system_resources()
            })
            
            return final_result
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return f"⚠️ I encountered an error: {str(e)}. Please try again."

    async def create_execution_plan(self, user_input: str) -> Optional[List[TaskStep]]:
        """Use DeepSeek R1 to create detailed execution plan"""
        logger.info("Creating execution plan with DeepSeek R1")
        
        # Get current system status
        resources = self.hardware_monitor.check_system_resources()
        context = self.build_context()
        
        prompt = f"""
{self.system_prompt}

CURRENT SYSTEM STATUS:
- VRAM Usage: {resources['vram_used_gb']:.1f}GB / 4.0GB
- RAM Usage: {resources['ram_used_gb']:.1f}GB / 16.0GB ({resources['ram_percent']:.1f}%)
- CPU Usage: {resources['cpu_percent']:.1f}%
- Temperature: {resources['temperature']:.1f}°C

CONVERSATION CONTEXT:
{context}

USER REQUEST: {user_input}

Create a detailed execution plan that respects hardware constraints and follows safety protocols.
"""

        try:
            response = self.ollama_client.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = response['message']['content']
            logger.info(f"DeepSeek R1 planning response: {response_text[:200]}...")
            
            # Parse JSON response
            plan_data = self.extract_json_from_response(response_text)
            if not plan_data or 'plan' not in plan_data:
                logger.error("Invalid plan format from DeepSeek R1")
                return None
            
            # Convert to TaskStep objects
            task_steps = []
            for step_data in plan_data['plan']:
                task_step = TaskStep(
                    step_id=step_data.get('step_id', len(task_steps) + 1),
                    description=step_data.get('description', ''),
                    task_type=TaskType(step_data.get('task_type', 'code_generation')),
                    blackbox_instructions=step_data.get('blackbox_instructions', ''),
                    expected_output=step_data.get('expected_output', ''),
                    safety_level=SafetyLevel(step_data.get('safety_level', 'green')),
                    hardware_requirements=step_data.get('hardware_requirements', {})
                )
                task_steps.append(task_step)
            
            logger.info(f"Created execution plan with {len(task_steps)} steps")
            return task_steps
            
        except Exception as e:
            logger.error(f"Error creating execution plan: {e}")
            return None

    async def execute_plan(self, plan: List[TaskStep]) -> List[ExecutionResult]:
        """Execute plan using Blackbox AI for code generation"""
        logger.info(f"Executing plan with {len(plan)} steps")
        results = []
        
        for step in plan:
            logger.info(f"Executing step {step.step_id}: {step.description}")
            
            # Check hardware requirements
            if not self.check_hardware_requirements(step):
                result = ExecutionResult(
                    success=False,
                    output="",
                    error="Insufficient hardware resources for this step"
                )
                results.append(result)
                continue
            
            # Safety validation
            if not self.safety_monitor.validate_step(step):
                result = ExecutionResult(
                    success=False,
                    output="",
                    error="Step blocked by safety monitor"
                )
                results.append(result)
                continue
            
            # User confirmation for non-green operations
            if step.safety_level != SafetyLevel.GREEN:
                if not await self.request_user_confirmation(step):
                    result = ExecutionResult(
                        success=False,
                        output="",
                        error="Step cancelled by user"
                    )
                    results.append(result)
                    continue
            
            # Generate and execute code with Blackbox AI
            start_time = time.time()
            start_resources = self.hardware_monitor.check_system_resources()
            
            execution_result = await self.blackbox_controller.generate_and_execute(step)
            
            # Record resource usage
            end_resources = self.hardware_monitor.check_system_resources()
            execution_result.execution_time = time.time() - start_time
            execution_result.vram_usage = end_resources["vram_used_gb"]
            execution_result.cpu_usage = end_resources["cpu_percent"]
            
            results.append(execution_result)
            
            # Check if we should continue after failure
            if not execution_result.success:
                logger.warning(f"Step {step.step_id} failed: {execution_result.error}")
                # For now, continue with remaining steps
        
        return results

    def check_hardware_requirements(self, step: TaskStep) -> bool:
        """Check if hardware can handle the step requirements"""
        if not step.hardware_requirements:
            return True
        
        resources = self.hardware_monitor.check_system_resources()
        required_vram = step.hardware_requirements.get('vram_gb', 0)
        
        if resources["vram_used_gb"] + required_vram > 3.5:  # 0.5GB safety margin
            logger.warning(f"Insufficient VRAM for step {step.step_id}")
            return False
        
        return True

    async def request_user_confirmation(self, step: TaskStep) -> bool:
        """Request user confirmation for potentially dangerous operations"""
        print(f"\n⚠️  JARVIS CONFIRMATION REQUIRED ⚠️")
        print(f"Step: {step.description}")
        print(f"Safety Level: {step.safety_level.value.upper()}")
        print(f"Blackbox Instructions: {step.blackbox_instructions[:100]}...")
        
        if step.safety_level == SafetyLevel.RED:
            print("🚨 WARNING: This operation could be dangerous!")
            print("🚨 Please review carefully before proceeding!")
        
        response = input("Proceed with this step? (y/n): ").lower().strip()
        return response in ['y', 'yes']

    def build_context(self) -> str:
        """Build context from recent conversation history"""
        if not self.conversation_history:
            return "No previous conversation."
        
        recent = self.conversation_history[-2:]  # Last 2 interactions
        context_parts = []
        
        for interaction in recent:
            context_parts.append(f"User: {interaction['user_input']}")
            context_parts.append(f"Result: {interaction['final_result'][:150]}...")
        
        return "\n".join(context_parts)

    def extract_json_from_response(self, response_text: str) -> Optional[Dict]:
        """Extract JSON from DeepSeek R1 response"""
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                logger.error("No JSON found in response")
                return None
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return None

    async def synthesize_results(self, user_input: str, plan: List[TaskStep], results: List[ExecutionResult]) -> Optional[str]:
        """Use DeepSeek R1 to synthesize results into user-friendly response"""
        logger.info("Synthesizing results with DeepSeek R1")
        
        # Prepare execution summary
        execution_summary = []
        for i, (step, result) in enumerate(zip(plan, results)):
            execution_summary.append({
                "step": step.description,
                "success": result.success,
                "output": result.output[:300] if result.output else "",
                "error": result.error,
                "execution_time": f"{result.execution_time:.2f}s",
                "vram_usage": f"{result.vram_usage:.1f}GB"
            })
        
        synthesis_prompt = f"""
Based on the execution results, provide a clear JARVIS-style response.

User request: {user_input}

Execution summary:
{json.dumps(execution_summary, indent=2)}

Provide a response that:
1. Confirms what was accomplished
2. Highlights any important outputs or files created
3. Notes any issues encountered
4. Suggests next steps if applicable

Be conversational and helpful, like JARVIS from Iron Man.
"""

        try:
            response = self.ollama_client.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are JARVIS. Provide clear, conversational responses about task results."},
                    {"role": "user", "content": synthesis_prompt}
                ]
            )
            
            content = response['message']['content']
            if content is None:
                return None
            return content
            
        except Exception as e:
            logger.error(f"Error synthesizing results: {e}")
            # Fallback summary
            successful = sum(1 for r in results if r.success)
            total = len(results)
            return f"Task completed. {successful}/{total} steps executed successfully."

class BlackboxController:
    """Enhanced controller for Blackbox AI integration following JARVIS architecture"""
    
    def __init__(self):
        self.vscode_path = self.find_vscode_path()
        self.temp_dir = "/tmp/jarvis_blackbox"
        os.makedirs(self.temp_dir, exist_ok=True)
        
    def find_vscode_path(self) -> str:
        """Find VS Code installation path"""
        possible_paths = [
            "/mnt/c/Users/*/AppData/Local/Programs/Microsoft VS Code/Code.exe",
            "/usr/bin/code",
            "/snap/bin/code"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return "code"  # Fallback to PATH

    async def generate_and_execute(self, step: TaskStep) -> ExecutionResult:
        """Generate code with Blackbox AI and execute it"""
        logger.info(f"Generating code with Blackbox AI for: {step.description}")
        
        try:
            # Create Blackbox AI prompt file
            prompt_file = self.create_blackbox_prompt_file(step)
            
            # Open in VS Code for Blackbox AI generation
            subprocess.run([self.vscode_path, prompt_file], check=False)
            
            # Wait for user to generate code
            print(f"\n🤖 BLACKBOX AI CODE GENERATION")
            print(f"Task: {step.description}")
            print(f"File: {prompt_file}")
            print("Please use Blackbox AI to generate the code, then press Enter...")
            input()
            
            # Read and execute generated code
            with open(prompt_file, 'r') as f:
                content = f.read()
            
            generated_code = self.extract_generated_code(content)
            if not generated_code:
                return ExecutionResult(
                    success=False,
                    output="",
                    error="No code generated by Blackbox AI"
                )
            
            # Execute the code
            result = await self.execute_code(generated_code, step)
            result.generated_code = generated_code
            
            return result
            
        except Exception as e:
            logger.error(f"Error in Blackbox AI generation: {e}")
            return ExecutionResult(
                success=False,
                output="",
                error=str(e)
            )

    def create_blackbox_prompt_file(self, step: TaskStep) -> str:
        """Create detailed prompt file for Blackbox AI"""
        timestamp = int(time.time())
        filename = f"{self.temp_dir}/jarvis_step_{step.step_id}_{timestamp}.py"
        
        prompt = f'''"""
JARVIS AUTONOMOUS AGENT - BLACKBOX AI CODE GENERATION

Task: {step.description}
Type: {step.task_type.value}
Safety Level: {step.safety_level.value}
Expected Output: {step.expected_output}

HARDWARE CONSTRAINTS (CRITICAL):
- RTX 3050 Ti: 4GB VRAM maximum
- i7-12700H: 20 threads total
- 16GB RAM system memory
- Thermal management required

BLACKBOX AI INSTRUCTIONS:
{step.blackbox_instructions}

REQUIREMENTS:
1. Write complete, executable Python code
2. Include all necessary imports
3. Add comprehensive error handling
4. Implement logging for debugging
5. Respect hardware constraints
6. Add safety checks where appropriate
7. Make code robust and production-ready

TEMPLATE:
```python
#!/usr/bin/env python3
import os
import sys
import logging
import time
import subprocess
# Add other imports as needed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting JARVIS task: {step.description}")
        
        # Your implementation here
        
        logger.info("Task completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error: {{e}}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

GENERATE THE COMPLETE CODE BELOW THIS LINE:
"""

# Generated code will be added here by Blackbox AI
'''
        
        with open(filename, 'w') as f:
            f.write(prompt)
        
        return filename

    def extract_generated_code(self, content: str) -> Optional[str]:
        """Extract generated code from the prompt file"""
        lines = content.split('\n')
        
        # Find the start of generated code
        start_idx = -1
        for i, line in enumerate(lines):
            if "# Generated code will be added here" in line:
                start_idx = i + 1
                break
        
        if start_idx == -1:
            # Look for Python code blocks
            for i, line in enumerate(lines):
                if line.strip().startswith('#!/usr/bin/env python3') and i > 10:
                    start_idx = i
                    break
        
        if start_idx != -1:
            generated_lines = lines[start_idx:]
            return '\n'.join(generated_lines).strip()
        
        return None

    async def execute_code(self, code: str, step: TaskStep) -> ExecutionResult:
        """Execute the generated code safely"""
        logger.info(f"Executing generated code for step {step.step_id}")
        
        try:
            # Create temporary execution file
            exec_file = f"{self.temp_dir}/exec_{step.step_id}_{int(time.time())}.py"
            
            with open(exec_file, 'w') as f:
                f.write(code)
            
            # Execute with timeout
            process = subprocess.run(
                [sys.executable, exec_file],
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            # Clean up
            os.remove(exec_file)
            
            if process.returncode == 0:
                return ExecutionResult(
                    success=True,
                    output=process.stdout,
                    error=process.stderr if process.stderr else None
                )
            else:
                return ExecutionResult(
                    success=False,
                    output=process.stdout,
                    error=process.stderr
                )
                
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="",
                error="Code execution timed out (120s limit)"
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=str(e)
            )

class SafetyMonitor:
    """Enhanced safety monitor following JARVIS safety protocols"""
    
    def __init__(self):
        self.dangerous_keywords = [
            'rm -rf', 'del /f /q', 'format', 'shutdown', 'reboot',
            'registry', 'system32', 'sudo rm', 'dd if=', 'mkfs',
            'fdisk', 'diskpart', 'bcdedit'
        ]
        
        self.sensitive_paths = [
            '/system', '/etc', '/boot', '/usr/bin', '/bin',
            'C:\\Windows', 'C:\\System32', 'C:\\Program Files'
        ]

    def validate_step(self, step: TaskStep) -> bool:
        """Validate step safety following JARVIS protocols"""
        instructions_lower = step.blackbox_instructions.lower()
        desc_lower = step.description.lower()
        
        # Check for dangerous keywords
        for keyword in self.dangerous_keywords:
            if keyword in instructions_lower or keyword in desc_lower:
                logger.warning(f"Dangerous keyword detected: {keyword}")
                if step.safety_level == SafetyLevel.GREEN:
                    step.safety_level = SafetyLevel.RED
        
        # Check for sensitive paths
        for path in self.sensitive_paths:
            if path.lower() in instructions_lower or path.lower() in desc_lower:
                logger.warning(f"Sensitive path detected: {path}")
                if step.safety_level == SafetyLevel.GREEN:
                    step.safety_level = SafetyLevel.YELLOW
        
        return True  # Always return True but adjust safety level

# Main execution
async def main():
    """Main JARVIS interface"""
    print("🤖 JARVIS - Autonomous AI Assistant")
    print("Based on: https://github.com/Phantomojo/JARVIS")
    print("=" * 50)
    
    agent = JarvisAgent()
    
    # Check system readiness
    safe, message = agent.hardware_monitor.is_safe_to_proceed()
    if not safe:
        print(f"⚠️ System not ready: {message}")
        return
    
    resources = agent.hardware_monitor.check_system_resources()
    print(f"System Status:")
    print(f"  VRAM: {resources['vram_used_gb']:.1f}GB / 4.0GB")
    print(f"  RAM: {resources['ram_used_gb']:.1f}GB / 16.0GB ({resources['ram_percent']:.1f}%)")
    print(f"  CPU: {resources['cpu_percent']:.1f}%")
    print(f"  Temperature: {resources['temperature']:.1f}°C")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'goodbye']:
                print("JARVIS: Goodbye! Powering down...")
                break
            
            if not user_input:
                continue
            
            print("\n🧠 JARVIS analyzing request...")
            result = await agent.process_request(user_input)
            print(f"\n🤖 JARVIS: {result}")
            
        except KeyboardInterrupt:
            print("\nJARVIS: Goodbye!")
            break
        except Exception as e:
            print(f"JARVIS Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
