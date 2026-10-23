from functools import lru_cache
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.rag import BIAssistant

app = FastAPI(title="BI Knowledge Assistant", version="1.0")


@lru_cache(maxsize=1)
def get_assistant():
    return BIAssistant()  # loads the FAISS index once, on first use


class Query(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(q: Query):
    if not q.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    return get_assistant().ask(q.question)