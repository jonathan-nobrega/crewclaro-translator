# crewclaro-translator onboarding

A Python background worker that translates job-site chat messages. It pulls jobs from Redis, translates each message into every target language using a construction-specific glossary, and publishes the results back for `crewclaro-api` to store. It has no user-facing API, only health and admin endpoints.

## Where it fits
- **Receives work from:** `crewclaro-api`, via the Redis list `translation:jobs`.
- **Sends results to:** `crewclaro-api`, via the Redis channel `translation:done`.
- **Deployed by:** `crewclaro-infra` (ECS Fargate, image `ghcr.io/jonathan-nobrega/crewclaro-translator`).

## Stack
Python 3.12, Redis (`redis.asyncio`), Pydantic schemas, FastAPI (`/healthz`, `/glossary`), pytest. Translation provider is pluggable: `llm` (default) or `deepl`, set with `TRANSLATION_PROVIDER`.

## Run locally
```bash
pip install -e ".[dev]"
set -a; source .env.example; set +a  # nothing loads .env automatically; vars must be in the environment
python -m app.worker                 # queue consumer
uvicorn app.main:app --port 8081     # health/admin endpoints
pytest
```
Needs the same Redis as `crewclaro-api` (`docker compose up -d redis` in that repo).

## Code map
| Path | What's there |
|---|---|
| `app/worker.py` | Main loop: `BRPOP` from `translation:jobs`, translate, publish to `translation:done` |
| `app/translate.py` | Provider logic and the LLM prompt |
| `app/glossary.yaml`, `app/glossary.py` | Pinned trade terms, e.g. "tablaroca" always becomes "drywall" |
| `app/schemas.py` | `TranslationJob` / `TranslationResult` |
| `app/main.py` | FastAPI health and glossary endpoints |

## Contract
```json
// in  (translation:jobs)
{ "messageId": "msg_8f2k", "text": "Necesitamos más tablaroca", "sourceLang": "es", "targetLangs": ["en", "pt"] }
// out (translation:done)
{ "messageId": "msg_8f2k", "translations": { "en": "We need more drywall" }, "status": "done" }
```
On error the worker publishes `status: "failed"` with an `error` message.

## Gotchas
- `app/schemas.py` must match `crewclaro-api/src/queue/translation.types.ts`. Change both together.
- The `llm` provider is still a stub: it returns `"[<lang>] <original text>"`. Only `deepl` makes a real call (`DEEPL_API_KEY` required).
- `WORKER_CONCURRENCY` is in `.env.example` but `worker.py` doesn't read it yet. Every job is started as its own task with no limit.
