import unittest
from unittest.mock import patch, MagicMock
from jarvis.scripts.core_inference import CoreInferenceManager

class TestCoreInferenceManager(unittest.TestCase):
    def setUp(self):
        self.manager = CoreInferenceManager()

    @patch('jarvis.scripts.memory_manager.MemoryManager.load_model')
    @patch('jarvis.scripts.gpu_optimizer.JARVISGPUOptimizer.get_gpu_status')
    @patch('jarvis.scripts.cpu_optimizer.JARVISCPUOptimizer.set_ai_process_affinity')
    def test_load_models(self, mock_set_affinity, mock_gpu_status, mock_load_model):
        mock_gpu_status.return_value = {
            'memory_used_gb': 1.0,
            'memory_free_gb': 3.0,
            'memory_total_gb': 4.0,
            'gpu_utilization': 50,
            'memory_utilization': 30,
            'temperature_c': 65
        }
        self.manager.load_models()
        self.assertTrue(mock_load_model.called)
        mock_set_affinity.assert_called_once()

    @patch('time.sleep', return_value=None)
    @patch('jarvis.scripts.gpu_optimizer.JARVISGPUOptimizer.intelligent_model_swapping')
    def test_run_inference(self, mock_model_swapping, mock_sleep):
        mock_model_swapping.return_value = "sufficient_memory"
        result = self.manager.run_inference("test input", "language_model")
        self.assertIn("Inference result", result['result'])

        mock_model_swapping.return_value = "swap_required"
        result = self.manager.run_inference("test input", "language_model")
        self.assertIn("Inference result", result['result'])

    @patch('jarvis.scripts.gpu_optimizer.JARVISGPUOptimizer.get_gpu_status')
    @patch('jarvis.scripts.cpu_optimizer.JARVISCPUOptimizer.monitor_cpu_performance')
    @patch('jarvis.scripts.memory_manager.MemoryManager.get_ram_usage_mb')
    def test_monitor_performance(self, mock_ram_usage, mock_cpu_perf, mock_gpu_status):
        mock_gpu_status.return_value = {'memory_used_gb': 1.0}
        mock_cpu_perf.return_value = {'total_cpu_usage': 50}
        mock_ram_usage.return_value = 8000
        perf = self.manager.monitor_performance()
        self.assertIn('gpu', perf)
        self.assertIn('cpu', perf)
        self.assertIn('ram_usage_mb', perf)

if __name__ == '__main__':
    unittest.main()
