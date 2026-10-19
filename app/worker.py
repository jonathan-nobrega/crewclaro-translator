import asyncio
import json
import os
import redis.asyncio as redis
from .schemas import TranslationJob, TranslationResult
from .translate import translate

JOBS_KEY = "translation:jobs"
DONE_CHANNEL = "translation:done"


async def handle(r: redis.Redis, raw: str) -> None:
    job = TranslationJob.model_validate_json(raw)
    try:
        pairs = await asyncio.gather(*(translate(job.text, job.sourceLang, t) for t in job.targetLangs))
        result = TranslationResult(messageId=job.messageId, translations=dict(zip(job.targetLangs, pairs)), status="done")
    except Exception as e:  # noqa: BLE001
        result = TranslationResult(messageId=job.messageId, translations={}, status="failed", error=str(e))
    await r.publish(DONE_CHANNEL, result.model_dump_json())


async def main() -> None:
    r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses=True)
    print("translator worker listening on", JOBS_KEY)
    while True:
        _, raw = await r.brpop(JOBS_KEY)
        asyncio.create_task(handle(r, raw))


if __name__ == "__main__":
    asyncio.run(main())
