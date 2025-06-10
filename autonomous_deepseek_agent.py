#!/usr/bin/env python3
"""
Autonomous DeepSeek R1 Agent Core
This is the main autonomous agent that uses DeepSeek R1 for reasoning and Blackbox AI for code generation.

Architecture:
User Request → DeepSeek R1 (Planning) → Blackbox AI (Code Generation) → System (Execution) → Result
"""

import json
import logging
import asyncio
import subprocess
import os
import sys
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import requests
import ollama

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("autonomous_agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AutonomousAgent")

class TaskType(Enum):
    """Types of tasks the agent can handle"""
    COMPUTER_CONTROL = "computer_control"
    WEB_BROWSING = "web_browsing"
    CODE_GENERATION = "code_generation"
    FILE_OPERATIONS = "file_operations"
    SYSTEM_MONITORING = "system_monitoring"
    DATA_PROCESSING = "data_processing"
    COMMUNICATION = "communication"
    RESEARCH = "research"
    AUTOMATION = "automation"

class SafetyLevel(Enum):
    """Safety levels for operations"""
    SAFE = "safe"           # No confirmation needed
    CAUTION = "caution"     # Ask for confirmation
    DANGEROUS = "dangerous" # Require explicit confirmation with warnings

@dataclass
class TaskStep:
    """Represents a single step in a task execution plan"""
    step_id: int
    description: str
    task_type: TaskType
    code_to_generate: str
    expected_output: str
    safety_level: SafetyLevel
    dependencies: List[int] = None

@dataclass
class ExecutionResult:
    """Result of executing a task step"""
    success: bool
    output: str
    error: str = None
    generated_code: str = None
    execution_time: float = 0.0

class AutonomousAgent:
    """
    Main autonomous agent that coordinates between DeepSeek R1 and Blackbox AI
    """
    
    def __init__(self, ollama_host="localhost", ollama_port=11434):
        self.ollama_client = ollama.Client(host=f"http://{ollama_host}:{ollama_port}")
        self.model_name = "deepseek-r1:8b"
        self.conversation_history = []
        self.task_history = []
        self.blackbox_controller = BlackboxController()
        self.safety_monitor = SafetyMonitor()
        
        # System prompt for DeepSeek R1
        self.system_prompt = """You are an autonomous AI agent named Jarvis. Your role is to:

1. UNDERSTAND user requests and break them down into actionable steps
2. PLAN the execution by creating detailed task steps
3. GENERATE specific instructions for Blackbox AI to write code
4. COORDINATE the execution of generated code
5. SYNTHESIZE results and provide feedback to the user

For each user request, you should:
- Analyze what needs to be done
- Break it into logical steps
- Determine what code needs to be generated for each step
- Specify the expected output
- Assess safety levels
- Provide clear instructions for Blackbox AI

You can control:
- Computer (mouse, keyboard, screenshots, applications)
- Internet (browsing, downloads, API calls)
- Files (create, read, write, organize)
- System (monitoring, processes, automation)
- Code (generation, execution, debugging)

Always prioritize safety and ask for confirmation on dangerous operations.

Respond in JSON format with this structure:
{
    "understanding": "What the user wants",
    "plan": [
        {
            "step_id": 1,
            "description": "What this step does",
            "task_type": "computer_control|web_browsing|code_generation|etc",
            "code_to_generate": "Detailed instructions for Blackbox AI",
            "expected_output": "What should happen",
            "safety_level": "safe|caution|dangerous"
        }
    ],
    "overall_goal": "Summary of what will be accomplished"
}"""

    async def process_request(self, user_input: str) -> str:
        """
        Main entry point for processing user requests
        """
        logger.info(f"Processing user request: {user_input}")
        
        try:
            # Step 1: Use DeepSeek R1 to understand and plan
            plan = await self.create_execution_plan(user_input)
            
            if not plan:
                return "I couldn't understand your request. Could you please rephrase it?"
            
            # Step 2: Execute the plan
            results = await self.execute_plan(plan)
            
            # Step 3: Synthesize and report results
            final_result = await self.synthesize_results(user_input, plan, results)
            
            # Store in history
            self.conversation_history.append({
                "user_input": user_input,
                "plan": plan,
                "results": results,
                "final_result": final_result,
                "timestamp": time.time()
            })
            
            return final_result
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return f"I encountered an error: {str(e)}. Please try again."

    async def create_execution_plan(self, user_input: str) -> List[TaskStep]:
        """
        Use DeepSeek R1 to create a detailed execution plan
        """
        logger.info("Creating execution plan with DeepSeek R1")
        
        # Prepare context with conversation history
        context = self.build_context()
        
        # Create prompt for DeepSeek R1
        prompt = f"""
{self.system_prompt}

Previous conversation context:
{context}

User request: {user_input}

Please analyze this request and create a detailed execution plan.
"""

        try:
            # Get response from DeepSeek R1
            response = self.ollama_client.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse the JSON response
            response_text = response['message']['content']
            logger.info(f"DeepSeek R1 response: {response_text}")
            
            # Extract JSON from response
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
                    code_to_generate=step_data.get('code_to_generate', ''),
                    expected_output=step_data.get('expected_output', ''),
                    safety_level=SafetyLevel(step_data.get('safety_level', 'safe'))
                )
                task_steps.append(task_step)
            
            logger.info(f"Created execution plan with {len(task_steps)} steps")
            return task_steps
            
        except Exception as e:
            logger.error(f"Error creating execution plan: {e}")
            return None

    async def execute_plan(self, plan: List[TaskStep]) -> List[ExecutionResult]:
        """
        Execute the plan by generating code with Blackbox AI and running it
        """
        logger.info(f"Executing plan with {len(plan)} steps")
        results = []
        
        for step in plan:
            logger.info(f"Executing step {step.step_id}: {step.description}")
            
            # Safety check
            if not self.safety_monitor.validate_step(step):
                result = ExecutionResult(
                    success=False,
                    output="",
                    error="Step blocked by safety monitor"
                )
                results.append(result)
                continue
            
            # Ask for confirmation if needed
            if step.safety_level in [SafetyLevel.CAUTION, SafetyLevel.DANGEROUS]:
                if not await self.request_user_confirmation(step):
                    result = ExecutionResult(
                        success=False,
                        output="",
                        error="Step cancelled by user"
                    )
                    results.append(result)
                    continue
            
            # Generate code with Blackbox AI
            start_time = time.time()
            generated_code = await self.blackbox_controller.generate_code(step)
            
            if not generated_code:
                result = ExecutionResult(
                    success=False,
                    output="",
                    error="Failed to generate code",
                    execution_time=time.time() - start_time
                )
                results.append(result)
                continue
            
            # Execute the generated code
            execution_result = await self.execute_generated_code(generated_code, step)
            execution_result.generated_code = generated_code
            execution_result.execution_time = time.time() - start_time
            
            results.append(execution_result)
            
            # If step failed, decide whether to continue
            if not execution_result.success:
                logger.warning(f"Step {step.step_id} failed: {execution_result.error}")
                # For now, continue with other steps
        
        return results

    async def execute_generated_code(self, code: str, step: TaskStep) -> ExecutionResult:
        """
        Execute the code generated by Blackbox AI
        """
        logger.info(f"Executing generated code for step {step.step_id}")
        
        try:
            # Create a temporary file for the code
            temp_file = f"/tmp/agent_step_{step.step_id}_{int(time.time())}.py"
            
            with open(temp_file, 'w') as f:
                f.write(code)
            
            # Execute the code
            process = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )
            
            # Clean up
            os.remove(temp_file)
            
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
                error="Code execution timed out"
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=str(e)
            )

    async def synthesize_results(self, user_input: str, plan: List[TaskStep], results: List[ExecutionResult]) -> str:
        """
        Use DeepSeek R1 to synthesize the results and create a user-friendly response
        """
        logger.info("Synthesizing results with DeepSeek R1")
        
        # Prepare summary of execution
        execution_summary = []
        for i, (step, result) in enumerate(zip(plan, results)):
            execution_summary.append({
                "step": step.description,
                "success": result.success,
                "output": result.output[:500] if result.output else "",  # Truncate long outputs
                "error": result.error
            })
        
        synthesis_prompt = f"""
Based on the user request and execution results, provide a clear, helpful response.

User request: {user_input}

Execution results:
{json.dumps(execution_summary, indent=2)}

Please provide:
1. A summary of what was accomplished
2. Any important outputs or results
3. Any issues encountered
4. Next steps if applicable

Be conversational and helpful, like Jarvis from Iron Man.
"""

        try:
            response = self.ollama_client.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are Jarvis, a helpful AI assistant. Provide clear, conversational responses about task results."},
                    {"role": "user", "content": synthesis_prompt}
                ]
            )
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Error synthesizing results: {e}")
            # Fallback to simple summary
            successful_steps = sum(1 for r in results if r.success)
            total_steps = len(results)
            return f"Task completed. {successful_steps}/{total_steps} steps executed successfully."

    def build_context(self) -> str:
        """
        Build context from recent conversation history
        """
        if not self.conversation_history:
            return "No previous conversation."
        
        # Get last 3 interactions
        recent_history = self.conversation_history[-3:]
        context_parts = []
        
        for interaction in recent_history:
            context_parts.append(f"User: {interaction['user_input']}")
            context_parts.append(f"Result: {interaction['final_result'][:200]}...")
        
        return "\n".join(context_parts)

    def extract_json_from_response(self, response_text: str) -> Dict:
        """
        Extract JSON from DeepSeek R1 response
        """
        try:
            # Try to find JSON in the response
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

    async def request_user_confirmation(self, step: TaskStep) -> bool:
        """
        Request user confirmation for potentially dangerous operations
        """
        print(f"\n⚠️  CONFIRMATION REQUIRED ⚠️")
        print(f"Step: {step.description}")
        print(f"Safety Level: {step.safety_level.value}")
        print(f"Code to generate: {step.code_to_generate}")
        
        if step.safety_level == SafetyLevel.DANGEROUS:
            print("🚨 WARNING: This operation could be dangerous!")
        
        response = input("Do you want to proceed? (y/n): ").lower().strip()
        return response in ['y', 'yes']

class BlackboxController:
    """
    Controller for interacting with Blackbox AI to generate code
    """
    
    def __init__(self):
        self.vscode_path = self.find_vscode_path()
        
    def find_vscode_path(self) -> str:
        """
        Find VS Code installation path
        """
        possible_paths = [
            "/mnt/c/Users/*/AppData/Local/Programs/Microsoft VS Code/Code.exe",
            "/usr/bin/code",
            "/snap/bin/code"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return "code"  # Fallback to PATH

    async def generate_code(self, step: TaskStep) -> str:
        """
        Generate code using Blackbox AI for the given task step
        """
        logger.info(f"Generating code with Blackbox AI for: {step.description}")
        
        # Create a detailed prompt for Blackbox AI
        blackbox_prompt = self.create_blackbox_prompt(step)
        
        # Create a temporary file with the prompt
        temp_prompt_file = f"/tmp/blackbox_prompt_{step.step_id}_{int(time.time())}.py"
        
        with open(temp_prompt_file, 'w') as f:
            f.write(f'"""\n{blackbox_prompt}\n"""\n\n# Generated code will go here\n')
        
        try:
            # Open the file in VS Code (this will trigger Blackbox AI)
            subprocess.run([self.vscode_path, temp_prompt_file], check=False)
            
            # Wait for user to generate code with Blackbox AI
            print(f"\n🤖 BLACKBOX AI CODE GENERATION")
            print(f"Task: {step.description}")
            print(f"File opened in VS Code: {temp_prompt_file}")
            print("Please use Blackbox AI to generate the code, then press Enter to continue...")
            input()
            
            # Read the generated code
            with open(temp_prompt_file, 'r') as f:
                content = f.read()
            
            # Extract the generated code (everything after the prompt)
            lines = content.split('\n')
            code_start = -1
            for i, line in enumerate(lines):
                if '# Generated code will go here' in line:
                    code_start = i + 1
                    break
            
            if code_start != -1:
                generated_code = '\n'.join(lines[code_start:])
                # Clean up
                os.remove(temp_prompt_file)
                return generated_code.strip()
            else:
                logger.error("Could not find generated code in file")
                return None
                
        except Exception as e:
            logger.error(f"Error generating code with Blackbox AI: {e}")
            return None

    def create_blackbox_prompt(self, step: TaskStep) -> str:
        """
        Create a detailed prompt for Blackbox AI
        """
        prompt = f"""
AUTONOMOUS AGENT CODE GENERATION REQUEST

Task Description: {step.description}
Task Type: {step.task_type.value}
Expected Output: {step.expected_output}
Safety Level: {step.safety_level.value}

Specific Instructions:
{step.code_to_generate}

Requirements:
1. Write complete, executable Python code
2. Include all necessary imports
3. Add error handling and logging
4. Make the code robust and safe
5. Add comments explaining key parts
6. Ensure the code produces the expected output

Code Template:
```python
#!/usr/bin/env python3
import os
import sys
import logging
import subprocess
# Add other imports as needed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Your code here
        logger.info("Starting task: {step.description}")
        
        # Implementation goes here
        
        logger.info("Task completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error: {{e}}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

Please generate the complete code below this line:
"""
        return prompt

class SafetyMonitor:
    """
    Monitors and validates operations for safety
    """
    
    def __init__(self):
        self.dangerous_keywords = [
            'rm -rf', 'del /f', 'format', 'shutdown', 'reboot',
            'registry', 'system32', 'sudo rm', 'dd if=', 'mkfs'
        ]
        
        self.sensitive_paths = [
            '/system', '/etc', '/boot', '/usr/bin',
            'C:\\Windows', 'C:\\System32', 'C:\\Program Files'
        ]

    def validate_step(self, step: TaskStep) -> bool:
        """
        Validate if a step is safe to execute
        """
        # Check for dangerous keywords
        code_lower = step.code_to_generate.lower()
        desc_lower = step.description.lower()
        
        for keyword in self.dangerous_keywords:
            if keyword in code_lower or keyword in desc_lower:
                logger.warning(f"Dangerous keyword detected: {keyword}")
                if step.safety_level != SafetyLevel.DANGEROUS:
                    step.safety_level = SafetyLevel.DANGEROUS
        
        # Check for sensitive paths
        for path in self.sensitive_paths:
            if path.lower() in code_lower or path.lower() in desc_lower:
                logger.warning(f"Sensitive path detected: {path}")
                if step.safety_level == SafetyLevel.SAFE:
                    step.safety_level = SafetyLevel.CAUTION
        
        return True  # Always return True, but adjust safety level

# Example usage and testing
async def main():
    """
    Example usage of the Autonomous Agent
    """
    agent = AutonomousAgent()
    
    print("🤖 Autonomous DeepSeek R1 Agent with Blackbox AI")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\n🧠 Processing with DeepSeek R1...")
            result = await agent.process_request(user_input)
            print(f"\n🤖 Jarvis: {result}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

