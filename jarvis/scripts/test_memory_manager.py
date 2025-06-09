import unittest
import memory_manager as mem_mgr

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = mem_mgr.MemoryManager()

    def test_load_and_unload_model(self):
        self.manager.loaded_models = {}
        self.manager.model_usage_stats = {}
        self.manager.load_model("test_model", 1000)
        self.assertIn("test_model", self.manager.loaded_models)
        self.manager.unload_least_used_model()
        self.assertNotIn("test_model", self.manager.loaded_models)

    def test_can_load_model(self):
        self.manager.ram_limit_mb = 2000
        self.manager.system_reserved_mb = 500
        self.manager.ai_available_mb = 1500
        # Override RAM usage for testing
        self.manager._test_used_mb = 0
        self.assertTrue(self.manager.can_load_model("model", 1000))
        self.assertFalse(self.manager.can_load_model("model", 2000))
        del self.manager._test_used_mb

if __name__ == '__main__':
    unittest.main()
