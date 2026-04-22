# =============================================================================
# Backend — API REST para chat com LLM via Groq
# Stack: FastAPI + httpx + SSE (Server-Sent Events para streaming)
#
# Configuração:
#   Crie um arquivo .env na pasta backend/ com:
#   GROQ_API_KEY=sua_chave_aqui
#
#   Chave gratuita em: https://console.groq.com
# =============================================================================

import uuid
import json
import httpx
import logging
import os
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL  = "https://api.groq.com/openai/v1"
GROQ_API_KEY  = os.getenv("GROQ_API_KEY", "")
DEFAULT_MODEL = "llama-3.3-70b-versatile"
MAX_HISTORY   = 20

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

sessions: dict[str, list[dict]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not GROQ_API_KEY:
        logger.warning("GROQ_API_KEY não encontrada. Configure o arquivo .env")
    else:
        logger.info("API iniciada — Groq configurado.")
    yield
    logger.info("API encerrada.")


app = FastAPI(
    title="Local AI Stack API",
    description="API para chat com LLMs via Groq",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str                  = Field(..., min_length=1)
    session_id: Optional[str]    = Field(default=None)
    model: str                    = Field(default=DEFAULT_MODEL)
    system_prompt: Optional[str] = Field(default=None)
    temperature: float            = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int               = Field(default=1024, ge=64, le=8192)

class ChatResponse(BaseModel):
    session_id: str
    response: str
    model: str
    tokens_used: Optional[int]
    timestamp: str


def get_headers() -> dict:
    if not GROQ_API_KEY:
        raise HTTPException(status_code=503, detail="GROQ_API_KEY não configurada. Adicione ao arquivo .env")
    return {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}


def get_or_create_session(session_id: Optional[str]) -> str:
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = []
        logger.info(f"Nova sessão criada: {session_id}")
    return session_id


def build_messages(session_id: str, user_message: str, system_prompt: Optional[str]) -> list[dict]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.extend(sessions[session_id][-MAX_HISTORY:])
    messages.append({"role": "user", "content": user_message})
    return messages


def update_history(session_id: str, user_message: str, assistant_reply: str):
    sessions[session_id].append({"role": "user",      "content": user_message})
    sessions[session_id].append({"role": "assistant", "content": assistant_reply})


@app.get("/health")
async def health_check():
    groq_ok = False
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{GROQ_API_URL}/models", headers=get_headers())
            groq_ok = resp.status_code == 200
    except Exception as e:
        logger.warning(f"Health check — Groq indisponível: {e}")
    return {
        "api":             "online",
        "groq":            "online" if groq_ok else "offline",
        "models":          GROQ_MODELS,
        "sessions_active": len(sessions),
        "timestamp":       datetime.now().isoformat(),
    }


@app.get("/models")
async def list_models():
    return {"models": [{"name": m, "size_gb": 0, "modified": ""} for m in GROQ_MODELS]}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = get_or_create_session(req.session_id)
    messages   = build_messages(session_id, req.message, req.system_prompt)
    payload = {
        "model": req.model, "messages": messages,
        "temperature": req.temperature, "max_tokens": req.max_tokens, "stream": False,
    }
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(f"{GROQ_API_URL}/chat/completions", headers=get_headers(), json=payload)
            resp.raise_for_status()
            data = resp.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout na resposta do Groq.")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Erro do Groq: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    assistant_reply = data["choices"][0]["message"]["content"]
    tokens_used     = data.get("usage", {}).get("total_tokens")
    update_history(session_id, req.message, assistant_reply)
    logger.info(f"[{session_id[:8]}] {req.model} — {tokens_used} tokens")
    return ChatResponse(session_id=session_id, response=assistant_reply, model=req.model, tokens_used=tokens_used, timestamp=datetime.now().isoformat())


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    session_id = get_or_create_session(req.session_id)
    messages   = build_messages(session_id, req.message, req.system_prompt)
    payload = {
        "model": req.model, "messages": messages,
        "temperature": req.temperature, "max_tokens": req.max_tokens, "stream": True,
    }

    async def event_generator():
        full_reply = ""
        yield f"data: {json.dumps({'session_id': session_id, 'type': 'start'})}\n\n"
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                async with client.stream("POST", f"{GROQ_API_URL}/chat/completions", headers=get_headers(), json=payload) as response:
                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue
                        raw = line[5:].strip()
                        if raw == "[DONE]":
                            update_history(session_id, req.message, full_reply)
                            yield f"data: {json.dumps({'type': 'done', 'session_id': session_id})}\n\n"
                            break
                        try:
                            chunk = json.loads(raw)
                            token = chunk["choices"][0]["delta"].get("content", "")
                            full_reply += token
                            yield f"data: {json.dumps({'token': token, 'type': 'token'})}\n\n"
                        except (json.JSONDecodeError, KeyError):
                            continue
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'detail': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.get("/session/{session_id}")
async def get_session_history(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")
    return {"session_id": session_id, "messages": sessions[session_id], "total": len(sessions[session_id])}


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")
    sessions[session_id] = []
    return {"message": "Histórico limpo com sucesso.", "session_id": session_id}


@app.delete("/sessions")
async def clear_all_sessions():
    total = len(sessions)
    sessions.clear()
    return {"message": f"{total} sessão(ões) removida(s)."}
