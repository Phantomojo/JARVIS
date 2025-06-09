import torch

# Alternative lightweight language model using GPT-2 from transformers
try:
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
except ImportError:
    GPT2LMHeadModel = None
    GPT2Tokenizer = None

class LanguageModel:
    def __init__(self, model_name="gpt2", device="cpu"):
        if GPT2LMHeadModel is None or GPT2Tokenizer is None:
            raise ImportError("transformers package with GPT2 is required for LanguageModel")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()
        self.device = device
        self.model.to(self.device)

    def generate_text(self, prompt: str, max_length: int = 100) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(input_ids=inputs['input_ids'], max_length=max_length)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
