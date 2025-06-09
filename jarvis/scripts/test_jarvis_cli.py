import unittest
from unittest.mock import patch, MagicMock
import jarvis.scripts.jarvis_cli as jarvis_cli

class TestJarvisCLI(unittest.TestCase):
    @patch('builtins.input', side_effect=['exit'])
    @patch('builtins.print')
    def test_main_exit(self, mock_print, mock_input):
        jarvis_cli.main()
        mock_print.assert_any_call("JARVIS: Goodbye! Powering down...")

    @patch('builtins.input', side_effect=['test command', 'exit'])
    @patch('builtins.print')
    @patch('asyncio.run')
    def test_main_process_request(self, mock_asyncio_run, mock_print, mock_input):
        mock_asyncio_run.return_value = "Test response"
        jarvis_cli.main()
        mock_asyncio_run.assert_called()
        mock_print.assert_any_call("\n🤖 JARVIS: Test response")

if __name__ == '__main__':
    unittest.main()
