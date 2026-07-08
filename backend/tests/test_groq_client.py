from types import SimpleNamespace

import pytest

from app.services.groq_client import GroqConfigurationError, send_groq_test_prompt


def test_send_groq_test_prompt_raises_when_api_key_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.services.groq_client.get_settings",
        lambda: SimpleNamespace(groq_api_key=None, groq_model="llama-3.3-70b-versatile"),
    )

    with pytest.raises(GroqConfigurationError):
        send_groq_test_prompt("hello")
