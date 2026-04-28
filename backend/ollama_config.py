import os


DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434/v1"
DEFAULT_OLLAMA_MODEL = "orion-lite"

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL)
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)


def get_ollama_api_url(path: str) -> str:
    base_url = OLLAMA_BASE_URL.rstrip("/")
    if base_url.endswith("/v1"):
        base_url = base_url[:-3]
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{base_url}{path}"


def create_ollama_client():
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "OpenAI client is not installed. Install the optional AI dependencies "
            "and set ORION_AI_ENABLED=true to use Ollama-backed features."
        ) from exc

    return OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key=os.environ.get("OLLAMA_API_KEY", "ollama"),
    )
