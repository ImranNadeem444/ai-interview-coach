from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from app.core.config import settings


# ============================================================
# Gemini LLM
# ============================================================

gemini_llm = None

if settings.gemini_api_key:
    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.gemini_api_key,
        temperature=0.7,
    )


# ============================================================
# OpenAI LLM
# ============================================================

openai_llm = None

if settings.openai_api_key:
    openai_llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.7,
    )


# ============================================================
# Get selected LLM
# ============================================================

def get_llm():
    """
    Return the LLM selected in .env.
    """

    provider = settings.llm_provider.lower()

    if provider == "openai":

        if openai_llm is None:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        return openai_llm

    if provider == "gemini":

        if gemini_llm is None:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        return gemini_llm

    raise ValueError(
        f"Unsupported LLM provider: {provider}"
    )


# ============================================================
# Generate text
# ============================================================

def generate_text(prompt: str) -> str:

    llm = get_llm()

    response = llm.invoke(prompt)

    if not response.content:
        raise ValueError(
            "LLM returned an empty response."
        )

    return response.content.strip()