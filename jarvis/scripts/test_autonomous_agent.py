
import unittest
import asyncio
from unittest.mock import MagicMock

class DummyTaskStep:
    def __init__(self):
        self.step_id = 1
        self.description = "Test step"
        self.task_type = "code_generation"
        self.blackbox_instructions = "Write test code"
        self.expected_output = "Success"
        self.safety_level = "green"
        self.hardware_requirements = {"vram_gb": 0.5}

class DummyJarvisAgent:
    def __init__(self):
        self.hardware_monitor = MagicMock()
        self.safety_monitor = MagicMock()
        self.blackbox_controller = MagicMock()

    async def process_request(self, user_input):
        if not self.hardware_monitor.is_safe_to_proceed():
            return "⚠️ System resources constrained"
        return "All done"

class TestJarvisAgent(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.agent = DummyJarvisAgent()

    async def test_process_request_safe(self):
        self.agent.hardware_monitor.is_safe_to_proceed = MagicMock(return_value=True)
        result = await self.agent.process_request("Test input")
        self.assertEqual(result, "All done")

    async def test_process_request_not_safe(self):
        self.agent.hardware_monitor.is_safe_to_proceed = MagicMock(return_value=False)
        result = await self.agent.process_request("Test input")
        self.assertIn("System resources constrained", result)

if __name__ == "__main__":
    unittest.main()
