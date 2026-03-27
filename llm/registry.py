from llm.gemini import GeminiClient
from llm.claude import ClaudeClient

_REGISTRY: dict[str, type] = {
    "Gemini 3.1 Pro Preview": GeminiClient,
    "Claude Opus 4.6": ClaudeClient,
}

MODEL_OPTIONS = list(_REGISTRY.keys())


def get_client(model_name: str):
    """Instantiate and return the LLMClient for the given display name."""
    cls = _REGISTRY.get(model_name)
    if cls is None:
        raise ValueError(f"Unknown model: {model_name}. Choose from {MODEL_OPTIONS}")
    return cls()
