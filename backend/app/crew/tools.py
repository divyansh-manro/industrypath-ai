# backend/app/crew/tools.py
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from app.config import settings

# Web search tool (Google-like results via Serper)
web_search_tool = SerperDevTool(
    api_key=settings.serper_api_key, 
)

# Optional: scrape content from URLs returned by search
scrape_tool = ScrapeWebsiteTool()
