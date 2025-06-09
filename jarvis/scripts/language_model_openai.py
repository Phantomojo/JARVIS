import os
import openai

class OpenAILanguageModel:
    def __init__(self, model_name="gpt-4", api_key=None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")
        openai.api_key = self.api_key

    def generate_text(self, prompt: str, max_tokens: int = 100) -> str:
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        content = response.choices[0].message.content
        return (content or "").strip()
