@echo off
title Local AI Stack

echo.
echo ============================================
echo        Local AI Stack — Inicializando
echo ============================================
echo.

set ROOT_DIR=%CD%

echo [1/3] Verificando configuracao...
if not exist "%ROOT_DIR%\backend\.env" (
    echo   Arquivo backend\.env nao encontrado.
    copy "%ROOT_DIR%\backend\.env.example" "%ROOT_DIR%\backend\.env" >nul
    echo   Arquivo .env criado. Edite backend\.env e adicione sua GROQ_API_KEY.
    echo   Chave gratuita em: https://console.groq.com
    echo.
    pause
)
echo   Configuracao OK.

echo [2/3] Iniciando Backend (FastAPI)...
cd "%ROOT_DIR%\backend"

if not exist ".venv" (
    python -m venv .venv
)

.venv\Scripts\pip install -q -r requirements.txt
taskkill /f /im uvicorn.exe >nul 2>&1
start "Backend FastAPI" /min cmd /c ".venv\Scripts\uvicorn api:app --host 0.0.0.0 --port 8000"

cd "%ROOT_DIR%"

echo   Aguardando backend inicializar...
set TRIES=0
:WAIT_BACKEND
curl -s http://localhost:8000/health >nul 2>&1
if %ERRORLEVEL% EQU 0 goto BACKEND_OK
set /a TRIES+=1
if %TRIES% GEQ 10 (
    echo   Backend nao respondeu.
    goto BACKEND_DONE
)
timeout /t 1 /nobreak >nul
goto WAIT_BACKEND
:BACKEND_OK
echo   Backend rodando em http://localhost:8000
:BACKEND_DONE

echo [3/3] Iniciando Frontend (Streamlit)...
cd "%ROOT_DIR%\frontend"

if not exist ".venv" (
    python -m venv .venv
)

.venv\Scripts\pip install -q -r requirements.txt

echo.
echo ============================================
echo   Stack inicializada com sucesso!
echo ============================================
echo.
echo   Interface: http://localhost:8501
echo   API:       http://localhost:8000
echo   Docs API:  http://localhost:8000/docs
echo.

timeout /t 4 /nobreak >nul
start "" http://localhost:8501
.venv\Scripts\streamlit run app.py --server.port 8501
