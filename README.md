# 🤖 Personal AI Stack (Groq Edition)

> Stack completa para chat com **LLMs de alta performance** via Groq API — respostas instantâneas, sem necessidade de GPU local.  
> Backend em **FastAPI** · Frontend em **Streamlit** · Modelo padrão: **Llama 3.3 70B**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Cloud-orange?style=flat)
![License](https://img.shields.io/badge/License-MIT-8B1A1A?style=flat)

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Execução](#execução)
  - [▶ Execução rápida (recomendado)](#-execução-rápida-recomendado)
  - [▶ Execução manual](#-execução-manual)
- [Endpoints da API](#endpoints-da-api)
- [Modelos Disponíveis](#modelos-disponíveis)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Referências](#referências)

---

## Visão Geral

O **Personal AI Stack** é uma aplicação de chat que combina a velocidade extrema da infraestrutura da **Groq** com uma interface personalizada e controle total do backend. Ideal para quem busca respostas em milissegundos sem depender de hardware caro localmente.

| Camada | Tecnologia | Função |
|---|---|---|
| **LLM Engine** | Groq Cloud | Inferência ultra-rápida via API |
| **Backend** | FastAPI + httpx | Gerencia sessões, histórico (memória) e roteamento |
| **Frontend** | Streamlit | Interface de chat com identidade visual customizada |
| **Modelo padrão** | llama-3.3-70b-versatile | O estado da arte em modelos abertos rodando em tempo real |

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                     Navegador                           │
│              http://localhost:8501                      │
│                                                         │
│              ┌─────────────────┐                        │
│              │  Streamlit UI   │                        │
│              │   (frontend)    │                        │
│              └────────┬────────┘                        │
└───────────────────────┼─────────────────────────────────┘
                        │ HTTP REST
                        ▼
┌─────────────────────────────────────────────────────────┐
│              http://localhost:8000                      │
│                                                         │
│              ┌─────────────────┐                        │
│              │   FastAPI API   │         ┌──────────┐   │
│              │   (backend)     │────────▶│ Groq API │   │
│              │                 │         └──────────┘   │
│              │  • /chat        │                        │
│              │  • /chat/stream │                        │
│              │  • /models      │                        │
│              │  • /health      │                        │
│              └─────────────────┘                        │
└─────────────────────────────────────────────────────────┘
```

**Fluxo:** `Usuário digita` → `Streamlit` → `FastAPI (gerencia sessão/histórico)` → `Groq API (inferência)` → `Resposta retornada`

---

## Pré-requisitos

- Python **3.10+**
- Uma chave de API da Groq (gratuita em [console.groq.com](https://console.groq.com))

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/faanogueira/personal-ai-stack.git
cd personal-ai-stack
```

### 2. Configurar variáveis de ambiente

Crie o arquivo `.env` na pasta `backend/`:

```bash
cp backend/.env.example backend/.env
```

Edite o arquivo `backend/.env` e insira sua chave:
```env
GROQ_API_KEY=gsk_sua_chave_aqui
```

### 3. Instalar dependências do backend

**Linux:**
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

### 4. Instalar dependências do frontend

**Linux:**
```bash
cd ../frontend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
cd ..\frontend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

---

## Execução

### ▶ Execução rápida (recomendado)

Um único arquivo inicializa toda a stack automaticamente — backend e frontend.

**Linux:**
```bash
chmod +x start_all.sh
bash start_all.sh
```

**Windows:**
```
start_all.bat
```

---

### ▶ Execução manual

Abra **dois terminais** e execute:

**Terminal 1 — Backend:**
```bash
cd backend
# Linux
.venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000
# Windows
.venv\Scripts\uvicorn api:app --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
# Linux
.venv/bin/streamlit run app.py --server.port 8501
# Windows
.venv\Scripts\streamlit run app.py --server.port 8501
```

---

| Serviço | URL |
|---|---|
| Interface de chat | http://localhost:8501 |
| API REST | http://localhost:8000 |
| Documentação da API (Swagger) | http://localhost:8000/docs |

---

## Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/health` | Status da API e conexão com Groq |
| `GET` | `/models` | Modelos configurados no backend |
| `POST` | `/chat` | Chat síncrono |
| `POST` | `/chat/stream` | Chat com streaming (SSE) |
| `GET` | `/session/{id}` | Recupera histórico da sessão |
| `DELETE` | `/session/{id}` | Limpa histórico de uma sessão |

---

## Modelos Disponíveis

A stack vem configurada com os seguintes modelos da Groq:

- `llama-3.3-70b-versatile` (Padrão)
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

---

## Estrutura do Projeto

```
personal-ai/
├── start_all.sh            # Inicialização rápida — Linux
├── start_all.bat           # Inicialização rápida — Windows
├── backend/
│   ├── api.py              # API FastAPI — lógica de chat e sessões
│   ├── .env.example        # Exemplo de configuração
│   ├── requirements.txt
│   ├── start.sh
│   └── test_api.sh         # Script para testar a API via curl
├── frontend/
│   ├── app.py              # Interface Streamlit
│   ├── requirements.txt
│   ├── start.sh
│   └── .streamlit/
│       └── config.toml     # Tema (Cores: Vermelho Vinho e Dark)
└── README.md
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
