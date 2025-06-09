import unittest
from unittest.mock import patch, MagicMock
import cpu_optimizer as cpu_opt

class TestJARVISCPUOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = cpu_opt.JARVISCPUOptimizer()

    @patch('psutil.Process.cpu_affinity')
    @patch('psutil.Process.nice')
    def test_set_ai_process_affinity(self, mock_nice, mock_affinity):
        # Test setting affinity for inference task
        with patch('psutil.Process') as mock_process:
            mock_process.return_value.cpu_affinity = mock_affinity
            mock_process.return_value.nice = mock_nice
            self.optimizer.set_ai_process_affinity(1234, 'inference')
            mock_affinity.assert_called_once_with(self.optimizer.p_cores)
            mock_nice.assert_called_once_with(-10)

    @patch('subprocess.run')
    def test_check_thermal_throttling(self, mock_run):
        # Simulate no throttling
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Normal temperature"
        self.assertFalse(self.optimizer.check_thermal_throttling())

        # Simulate throttling detected
        mock_run.return_value.stdout = "Throttling detected"
        self.assertTrue(self.optimizer.check_thermal_throttling())

if __name__ == '__main__':
    unittest.main()
