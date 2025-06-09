import unittest
from unittest.mock import MagicMock, patch
from jarvis.scripts.performance_dashboard import PerformanceDashboard

class TestPerformanceDashboard(unittest.TestCase):
    def setUp(self):
        self.dashboard = PerformanceDashboard()

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_get_system_metrics(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 50.0
        mock_virtual_memory.return_value.percent = 60.0
        metrics = self.dashboard.get_system_metrics()
        self.assertEqual(metrics['cpu_percent'], 50.0)
        self.assertEqual(metrics['ram_percent'], 60.0)

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_monitor_performance(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 30.0
        mock_virtual_memory.return_value.percent = 40.0
        # Test that monitor_performance runs without error for one iteration
        with patch('time.sleep', return_value=None):
            self.dashboard.monitor_performance_once()

if __name__ == '__main__':
    unittest.main()
