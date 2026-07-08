import pytest

from app.services.groq_client import GroqConfigurationError, send_groq_test_prompt



def test_send_groq_test_prompt_raises_when_api_key_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.setenv("GROQ_MODEL", "gemma2-9b-it")
    from app.core.config import get_settings

    get_settings.cache_clear()

    with pytest.raises(GroqConfigurationError):
        send_groq_test_prompt("hello")

    get_settings.cache_clear()
