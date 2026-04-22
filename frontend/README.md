# 🖥️ Frontend — Personal AI Stack

> Interface de chat moderna e responsiva construída com **Streamlit**, conectada ao backend FastAPI via Groq.  
> Identidade visual exclusiva em vermelho vinho e tema dark.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Interface](#interface)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Execução](#execução)
- [Personalização](#personalização)

---

## Visão Geral

O frontend oferece uma experiência de chat completa consumindo a API local, com suporte a streaming de respostas, controle de parâmetros e persistência de histórico por sessão.

| Recurso | Detalhe |
|---|---|
| Framework | Streamlit 1.41+ |
| HTTP Client | httpx |
| Tema | Dark Customizado (`#8B1A1A` · `#0D0D0D`) |
| Backend | FastAPI em `http://localhost:8000` |

---

## Interface

**Sidebar de Configuração**

| Componente | Função |
|---|---|
| Status badge | Indica em tempo real se a conexão com o Groq está ativa |
| Seletor de modelo | Lista os modelos disponíveis na API (Llama 3, Mixtral, Gemma) |
| Parâmetros (Temperature/Tokens) | Ajuste fino do comportamento do modelo |
| System Prompt | Define a personalidade/contexto do assistente |
| Métricas | Contador de mensagens enviadas e tokens utilizados |
| Botão Limpar | Reseta o histórico da sessão local e no servidor |

**Área de Chat**

- Balões de conversa com estilos diferenciados para Usuário e IA.
- Indicador visual de processamento.
- Tratamento de erro quando o backend está inacessível.

---

## Pré-requisitos

- Python **3.10+**
- Backend rodando em `http://localhost:8000` (veja `../backend/README.md`)

---

## Instalação

```bash
cd frontend
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Execução

```bash
bash start.sh
# Ou manualmente:
streamlit run app.py --server.port 8501
```

---

## Personalização

### Alterar a URL da API

Em `app.py`, você pode alterar a variável para apontar para um servidor externo se necessário:
```python
BACKEND_URL = "http://localhost:8000"
```

### Paleta de Cores e Estilo

As cores principais são definidas em `.streamlit/config.toml` e via CSS injetado em `app.py`. Para alterar o vermelho vinho:
- Substitua `#8B1A1A` pela sua cor de preferência.

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
