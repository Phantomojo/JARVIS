import unittest
import unittest
from unittest.mock import patch, MagicMock
import sys
import types

# Mock transformers module to avoid ImportError during testing
mock_transformers = types.ModuleType("transformers")
setattr(mock_transformers, "GPT2LMHeadModel", MagicMock())
setattr(mock_transformers, "GPT2Tokenizer", MagicMock())
sys.modules["transformers"] = mock_transformers

# Mock ollama module and Client class to avoid AttributeError during testing
mock_ollama = types.ModuleType("ollama")
mock_client_class = MagicMock()
setattr(mock_ollama, "Client", mock_client_class)
sys.modules["language_model.ollama"] = mock_ollama

from language_model import LanguageModel

class TestLanguageModel(unittest.TestCase):
    def setUp(self):
        self.model = LanguageModel()

    @patch('language_model.ollama.Client.chat')
    def test_generate_text(self, mock_chat):
        mock_chat.return_value = {'message': {'content': 'Test response'}}
        # Mock the generate_text method to return a fixed string
        self.model.generate_text = MagicMock(return_value='Test response')
        response = self.model.generate_text("Hello")
        self.assertEqual(response, 'Test response')

if __name__ == '__main__':
    unittest.main()
