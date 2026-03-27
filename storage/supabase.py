import os
from supabase import create_client, Client

TABLE = "responses"

_client: Client | None = None
_current_url: str | None = None


def _get_client() -> Client:
    global _client, _current_url
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError("SUPABASE_URL and SUPABASE_KEY must be set")
    if _client is None or _current_url != url:
        _client = create_client(url, key)
        _current_url = url
    return _client


def save_response(uid: str, prompt: str, response: str, model: str) -> dict:
    """Insert a row into the responses table. Returns the inserted row."""
    row = {
        "id": uid,
        "prompt": prompt,
        "response": response,
        "model": model,
    }
    result = _get_client().table(TABLE).insert(row).execute()
    return result.data[0] if result.data else row
