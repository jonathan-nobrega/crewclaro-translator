# crewclaro-translator

> **Hackathon demo repo.** Mock code for testing a multi-repo agent. Not affiliated with or endorsed by CrewClaro.

Async translation worker. Consumes jobs from Redis, translates messages into every crew member's language using a construction-aware glossary, and publishes results back to `crewclaro-api`.

## Stack
- Python 3.12
- Redis (`translation:jobs` list in, `translation:done` channel out)
- Pluggable provider: LLM (default) or DeepL
- FastAPI for `/healthz` and `/glossary` admin endpoints
- pytest

## Contract
Must stay in sync with `crewclaro-api/src/queue/translation.types.ts`.

Job (in):
```json
{ "messageId": "msg_8f2k", "text": "Necesitamos más tablaroca", "sourceLang": "es", "targetLangs": ["en", "pt"] }
```
Result (out):
```json
{ "messageId": "msg_8f2k", "translations": { "en": "We need more drywall" }, "status": "done" }
```

## Glossary
`app/glossary.yaml` pins trade terms so "tablaroca" always becomes "drywall", not "plasterboard" or "wallboard".

## Run
```bash
pip install -e ".[dev]"
python -m app.worker          # queue consumer
uvicorn app.main:app --port 8081   # health/admin
pytest
```
