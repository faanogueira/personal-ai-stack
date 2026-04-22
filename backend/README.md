# Backend — Personal AI Stack

API REST construída com **FastAPI** que atua como ponte entre o frontend e a infraestrutura da **Groq**.

---

## Stack

| Componente | Tecnologia |
|---|---|
| Framework | FastAPI 0.115 |
| Servidor | Uvicorn (ASGI) |
| HTTP Client | httpx (assíncrono) |
| LLM Engine | Groq Cloud |
| Streaming | Server-Sent Events (SSE) |

---

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/health` | Status da API e conectividade com Groq |
| `GET` | `/models` | Lista de modelos Groq configurados |
| `POST` | `/chat` | Chat síncrono (aguarda resposta completa) |
| `POST` | `/chat/stream` | Chat assíncrono com streaming de tokens |
| `GET` | `/session/{id}` | Recupera histórico de uma sessão específica |
| `DELETE` | `/session/{id}` | Limpa o histórico de uma sessão |
| `DELETE` | `/sessions` | Remove todas as sessões ativas na memória |

Documentação interativa (Swagger): `http://localhost:8000/docs`

---

## Instalação e Execução

### 1. Configurar Variáveis de Ambiente

Crie o arquivo `.env` baseado no `.env.example` e insira sua `GROQ_API_KEY`:

```bash
cp .env.example .env
```

### 2. Instalar Dependências

```bash
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Iniciar o Servidor

```bash
bash start.sh
# Ou manualmente:
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

---

## Testando a API

Você pode usar o script `test_api.sh` para validar os endpoints via `curl`:

```bash
bash test_api.sh
```

---

## Lógica de Sessão

O backend mantém o histórico das conversas em memória (variável `sessions`). 
- **MAX_HISTORY**: Por padrão, enviamos as últimas 20 mensagens para o modelo para manter o contexto sem exceder limites de tokens.
- **session_id**: Se não enviado no `/chat`, a API gera um novo UUID e o retorna na resposta.

---

## Exemplo de Requisição (Chat)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Olá, quem é você?",
    "model": "llama-3.3-70b-versatile",
    "temperature": 0.7
  }'
```
---

## 👤 Autor

<div>
  <p>Developed by <b>Fábio Nogueira</b></p>
</div>
<p>
<a href="https://www.linkedin.com/in/faanogueira/" target="_blank"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=13930&format=png&color=000000" width="80"></a>
<a href="https://github.com/faanogueira" target="_blank"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=AZOZNnY73haj&format=png&color=000000" width="80"></a>
<a href="https://api.whatsapp.com/send?phone=5571983937557" target="_blank"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=16713&format=png&color=000000" width="80"></a>
<a href="mailto:faanogueira@gmail.com"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=P7UIlhbpWzZm&format=png&color=000000" width="80"></a>
</p>
