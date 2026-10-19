from fastapi import FastAPI
from .glossary import load_glossary

app = FastAPI(title="crewclaro-translator")


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/glossary")
def glossary():
    return load_glossary()
