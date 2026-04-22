#!/usr/bin/env bash
# =============================================================================
# start_all.sh — inicializa o backend e o frontend (Groq — sem Ollama)
# =============================================================================

set +e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ROOT_DIR=$(pwd)

echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}        Local AI Stack — Inicializando      ${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# PASSO 1 — Verificar .env
echo -e "${YELLOW}[1/3] Verificando configuração...${NC}"
if [ ! -f "$ROOT_DIR/backend/.env" ]; then
    echo -e "${RED}  Arquivo backend/.env não encontrado.${NC}"
    echo -e "${YELLOW}  Criando a partir do exemplo...${NC}"
    cp "$ROOT_DIR/backend/.env.example" "$ROOT_DIR/backend/.env"
    echo -e "${RED}  ⚠️  Edite backend/.env e adicione sua GROQ_API_KEY antes de continuar.${NC}"
    echo -e "${YELLOW}  Chave gratuita em: https://console.groq.com${NC}"
    echo ""
    read -p "  Pressione ENTER após configurar o .env..."
fi
echo -e "${GREEN}  Configuração OK.${NC}"

# PASSO 2 — Backend
echo -e "${YELLOW}[2/3] Iniciando Backend (FastAPI)...${NC}"
cd "$ROOT_DIR/backend"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

.venv/bin/pip install -q -r requirements.txt
pkill -f "uvicorn api:app" 2>/dev/null || true
sleep 1

nohup .venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
disown $!

cd "$ROOT_DIR"

echo -e "${YELLOW}      Aguardando backend inicializar...${NC}"
TRIES=0
until curl -s http://localhost:8000/health > /dev/null 2>&1; do
    TRIES=$((TRIES + 1))
    if [ $TRIES -ge 10 ]; then
        echo -e "${RED}  Backend não respondeu. Verifique /tmp/backend.log${NC}"
        break
    fi
    sleep 1
done
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}  Backend rodando em http://localhost:8000${NC}"
fi

# PASSO 3 — Frontend
echo -e "${YELLOW}[3/3] Iniciando Frontend (Streamlit)...${NC}"
cd "$ROOT_DIR/frontend"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements.txt

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  Stack inicializada com sucesso!           ${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "  Interface: ${CYAN}http://localhost:8501${NC}"
echo -e "  API:       ${CYAN}http://localhost:8000${NC}"
echo -e "  Docs API:  ${CYAN}http://localhost:8000/docs${NC}"
echo ""
echo -e "  Pressione ${RED}Ctrl+C${NC} para encerrar o frontend."
echo ""

sleep 3 && xdg-open http://localhost:8501 &
streamlit run app.py --server.port 8501 --server.headless true
