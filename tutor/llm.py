import os

import requests


class LLMError(Exception):
    pass


def call_llm(system_prompt, user_prompt):
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider == "claude":
        return call_claude(system_prompt, user_prompt)
    if provider == "gemini":
        return call_gemini(system_prompt, user_prompt)
    raise LLMError(f"Unknown LLM_PROVIDER: {provider}")


def call_claude(system_prompt, user_prompt):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise LLMError("ANTHROPIC_API_KEY is not set.")
    model = os.getenv("LLM_MODEL", "claude-haiku-4-5")
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": model,
                "max_tokens": 400,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_prompt}],
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"]
    except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
        raise LLMError(str(exc)) from exc


def call_gemini(system_prompt, user_prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise LLMError("GEMINI_API_KEY is not set.")
    model = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    try:
        response = requests.post(
            url,
            headers={"x-goog-api-key": api_key, "content-type": "application/json"},
            json={
                "system_instruction": {"parts": [{"text": system_prompt}]},
                "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
                "generationConfig": {"maxOutputTokens": 800, "temperature": 0.4},
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
        raise LLMError(str(exc)) from exc
