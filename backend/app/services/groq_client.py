from groq import Groq

from app.core.config import get_settings


class GroqConfigurationError(RuntimeError):
    """Raised when the Groq client cannot be configured safely."""



def get_groq_client() -> Groq:
    settings = get_settings()

    if not settings.groq_api_key:
        raise GroqConfigurationError(
            "GROQ_API_KEY is not set. Add it to your backend environment before using Groq."
        )

    return Groq(api_key=settings.groq_api_key)



def send_groq_test_prompt(prompt: str) -> str:
    client = get_groq_client()
    settings = get_settings()

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=settings.groq_model,
        )
    except Exception as exc:
        raise RuntimeError("Groq test prompt failed.") from exc

    content = completion.choices[0].message.content
    if content is None:
        raise RuntimeError("Groq returned an empty response.")

    return content
