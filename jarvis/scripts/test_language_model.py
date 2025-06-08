import unittest
from unittest.mock import patch, MagicMock
from jarvis.scripts.language_model import LanguageModel

class TestLanguageModel(unittest.TestCase):
    @patch('jarvis.scripts.language_model.LlamaForCausalLM.from_pretrained')
    @patch('jarvis.scripts.language_model.LlamaTokenizer.from_pretrained')
    def setUp(self, mock_tokenizer, mock_model):
        self.mock_tokenizer = mock_tokenizer.return_value
        self.mock_model = mock_model.return_value
        self.mock_model.generate.return_value = [101, 102, 103]
        self.mock_tokenizer.decode.return_value = "Test response"
        self.lm = LanguageModel()

    def test_load_model(self):
        self.assertIsNotNone(self.lm.model)
        self.assertIsNotNone(self.lm.tokenizer)

    def test_generate(self):
        prompt = "Hello"
        response = self.lm.generate(prompt)
        self.mock_tokenizer.assert_called()
        self.mock_model.generate.assert_called()
        self.mock_tokenizer.decode.assert_called()
        self.assertEqual(response, "Test response")

    def test_generate_empty_prompt(self):
        prompt = ""
        response = self.lm.generate(prompt)
        self.assertEqual(response, "Test response")

    def test_generate_long_prompt(self):
        prompt = "A" * 1000
        response = self.lm.generate(prompt)
        self.assertEqual(response, "Test response")

if __name__ == '__main__':
    unittest.main()
