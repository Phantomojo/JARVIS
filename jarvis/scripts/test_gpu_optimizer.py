import unittest
from unittest.mock import patch, MagicMock
from pynvml import nvmlInit, nvmlDeviceGetMemoryInfo, nvmlDeviceGetUtilizationRates, nvmlDeviceGetTemperature, NVML_TEMPERATURE_GPU
import gpu_optimizer as gpu_opt

class TestJARVISGPUOptimizer(unittest.TestCase):
    def setUp(self):
        nvmlInit()
        self.optimizer = gpu_opt.JARVISGPUOptimizer()

    @patch('torch.cuda.set_per_process_memory_fraction')
    @patch('torch.cuda.empty_cache')
    def test_optimize_gpu_settings(self, mock_empty_cache, mock_set_mem_frac):
        status = self.optimizer.optimize_gpu_settings()
        mock_set_mem_frac.assert_called_once()
        mock_empty_cache.assert_called_once()
        self.assertIn('memory_used_gb', status)
        self.assertIn('gpu_utilization', status)

    @patch('gpu_optimizer.nvmlDeviceGetMemoryInfo')
    @patch('gpu_optimizer.nvmlDeviceGetUtilizationRates')
    @patch('gpu_optimizer.nvmlDeviceGetTemperature')
    def test_get_gpu_status(self, mock_temp, mock_util, mock_mem):
        mock_mem.return_value.used = 2 * 1024**3
        mock_mem.return_value.free = 2 * 1024**3
        mock_mem.return_value.total = 4 * 1024**3
        mock_util.return_value.gpu = 50
        mock_util.return_value.memory = 30
        mock_temp.return_value = 70
        status = self.optimizer.get_gpu_status()
        self.assertEqual(status['memory_used_gb'], 2)
        self.assertEqual(status['gpu_utilization'], 50)
        self.assertEqual(status['temperature_c'], 70)

    @patch('gpu_optimizer.nvmlDeviceGetTemperature')
    def test_monitor_thermal_throttling(self, mock_temp):
        mock_temp.return_value = 85
        self.assertTrue(self.optimizer.monitor_thermal_throttling())
        mock_temp.return_value = 75
        self.assertFalse(self.optimizer.monitor_thermal_throttling())

    @patch('gpu_optimizer.JARVISGPUOptimizer.get_gpu_status')
    def test_intelligent_model_swapping(self, mock_get_status):
        # Test swap required when VRAM low
        mock_get_status.return_value = {'memory_free_gb': 0.5}
        result = self.optimizer.intelligent_model_swapping([], 'conversation')
        self.assertEqual(result, "swap_required")
        # Test sufficient memory
        mock_get_status.return_value = {'memory_free_gb': 2.0}
        result = self.optimizer.intelligent_model_swapping([], 'conversation')
        self.assertEqual(result, "sufficient_memory")

if __name__ == '__main__':
    unittest.main()
