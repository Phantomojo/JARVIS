import unittest
from unittest.mock import patch, MagicMock
import jarvis.scripts.memory_manager as mem_mgr

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = mem_mgr.MemoryManager()

    @patch('psutil.virtual_memory')
    def test_get_ram_usage_mb(self, mock_virtual_memory):
        mock_virtual_memory.return_value.total = 16 * 1024**3
        mock_virtual_memory.return_value.available = 8 * 1024**3
        usage = self.manager.get_ram_usage_mb()
        self.assertAlmostEqual(usage, 8 * 1024, delta=100)

    @patch('builtins.print')
    def test_load_and_unload_model(self, mock_print):
        self.manager.loaded_models = {}
        self.manager.model_usage_stats = {}
        self.manager.load_model('test_model', 1000)
        mock_print.assert_any_call('Model test_model loaded.')
        self.manager.unload_least_used_model()
        mock_print.assert_any_call('Model test_model unloaded to free memory.')

if __name__ == '__main__':
    unittest.main()
