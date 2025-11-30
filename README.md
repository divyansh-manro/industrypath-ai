# IndustryPath AI

An agentic AI prototype built with CrewAI and Google Gemini that:
- takes a vague industrial idea (e.g., "I want to build a refrigerator"),
- clarifies it,
- researches key concepts,
- generates a learning roadmap,
- and suggests industry exposure links.

## Stack

- Python, FastAPI
- CrewAI + Gemini (Google API key)
- SerperDevTool for web search (optional)
- Simple HTML/JS frontend

## Running locally

```bash
cd backend
cp .env.example .env  # put your keys
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
