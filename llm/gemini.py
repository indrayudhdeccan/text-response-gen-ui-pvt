import os
from openai import OpenAI
from llm.base import LLMClient

MODEL_ID = "google/gemini-3.1-pro-preview"
BASE_URL = "https://openrouter.ai/api/v1"


class GeminiClient(LLMClient):
    def __init__(self):
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENROUTER_API_KEY is not set")
        self.client = OpenAI(api_key=api_key, base_url=BASE_URL)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
