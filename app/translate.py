import os
import httpx
from .glossary import terms_for

PROVIDER = os.getenv("TRANSLATION_PROVIDER", "llm")


def build_prompt(text: str, source: str, target: str) -> str:
    glossary = terms_for(source, target)
    pinned = "\n".join(f"- {s} => {t}" for s, t in glossary.items())
    return (
        f"Translate this construction job-site message from {source} to {target}. "
        f"Keep it short and informal, as a foreman would write it. "
        f"Always use these term translations:\n{pinned}\n\nMessage: {text}"
    )


async def translate(text: str, source: str, target: str) -> str:
    if PROVIDER == "deepl":
        async with httpx.AsyncClient() as client:
            r = await client.post(
                "https://api-free.deepl.com/v2/translate",
                headers={"Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}"},
                data={"text": text, "source_lang": source.upper(), "target_lang": target.upper()},
            )
            r.raise_for_status()
            return r.json()["translations"][0]["text"]
    # Hackathon stub: replace with a real LLM call
    return f"[{target}] {text}"
