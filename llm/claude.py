import os
import anthropic
from llm.base import LLMClient

MODEL_ID = "claude-opus-4-6"


class ClaudeClient(LLMClient):
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY is not set")
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt: str) -> str:
        message = self.client.messages.create(
            model=MODEL_ID,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
