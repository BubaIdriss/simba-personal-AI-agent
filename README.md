# Buba Agent

## Overview

Buba Agent is a personal AI assistant API built with FastAPI and LangChain. It integrates with Google services (Gmail, Calendar, Contacts), WhatsApp, and a web search provider to perform actions like sending emails, scheduling events, reading emails, and searching the web. The project exposes a small HTTP API to interact with the agent programmatically.

## Tech stack

- **Python** (>=3.12)
- **FastAPI**: HTTP API server
- **LangChain** / **langgraph**: agent / LLM orchestration
- **OpenRouter / Deepseek**: configured LLM model provider
- **Google API Client**: Gmail, Calendar, Contacts integrations
- **Tavily**: web search integration
- **Uvicorn**: ASGI server
- **python-dotenv**: environment variable loading

## Getting started

### Prerequisites

- Python 3.12 or newer
- pip (or a compatible installer)
- A Google OAuth `token.json` (for Google integrations)
- Environment variables configured (see below)

### Installation

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -U pip
pip install -r requirements.txt || pip install .
```

Note: this project uses `pyproject.toml`. You can install the package in editable mode with `pip install -e .` or build/install with `pip install .`.

### Environment variables

Create a `.env` file at the project root or export environment variables directly. Common variables used by the project:

- `DEEPSEEK-V4` — OpenRouter / Deepseek API key used by the LLM.
- `GOOGLE_APPLICATION_CREDENTIALS` — path to Google credentials (if using service account flow).

For Google user-level OAuth, ensure `token.json` (the authorized user token) is available at the project root.

### Run the API server

Start the FastAPI server with Uvicorn:

```bash
uvicorn src.buba_agent.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` and the OpenAPI docs at `http://localhost:8000/docs`.

## Project layout

- `src/buba_agent/` — main package with agent, integrations and tools
  - `api/main.py` — FastAPI app and endpoints
  - `agent.py` — agent setup and entrypoints (`chat_agent`, `resume_agent`)
  - `integrations/` — Google, WhatsApp, web search connectors
  - `tools.py` — LangChain tools exposed to the agent
  - `prompt.py`, `schemas.py` — prompt templates and request schemas

## Available scripts & entrypoints

- Package script: `buba-agent` (defined in `pyproject.toml`) calls `buba_agent:main`.
- Run the API directly with Uvicorn (see Run the API server).

## Notes

- The Google integrations expect an OAuth token file (`token.json`) with the required scopes (Gmail, Calendar, Contacts). See `src/buba_agent/integrations/google.py` for details about scopes and usage.
- Some agent actions require human approval. The API supports approval endpoints to resume interrupted operations.
