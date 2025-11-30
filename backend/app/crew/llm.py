# backend/app/crew/llm.py
from crewai import LLM
from app.config import settings

# Shared LLM instance for all agents
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash", 
    api_key=settings.google_api_key or settings.gemini_api_key,
    temperature=0.6,
)
