# Mirrors crewclaro-api/src/queue/translation.types.ts
from typing import Literal
from pydantic import BaseModel

Lang = Literal["en", "es", "pt", "pl"]


class TranslationJob(BaseModel):
    messageId: str
    text: str
    sourceLang: Lang
    targetLangs: list[Lang]


class TranslationResult(BaseModel):
    messageId: str
    translations: dict[str, str]
    status: Literal["done", "failed"]
    error: str | None = None
