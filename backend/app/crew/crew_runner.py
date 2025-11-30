# backend/app/crew/crew_runner.py

from crewai import Crew, Process
from .tasks import (
    clarify_idea_task,
    research_task,
    roadmap_task,
    industry_task,
)
import json
import re

# Assemble the crew
industrypath_crew = Crew(
    agents=[
        clarify_idea_task.agent,
        research_task.agent,
        roadmap_task.agent,
        industry_task.agent,
    ],
    tasks=[
        clarify_idea_task,
        research_task,
        roadmap_task,
        industry_task,
    ],
    process=Process.sequential,
    verbose=True,
)


def _extract_json(raw_text: str):
    """Try to pull a JSON object out of the model's text."""
    text = raw_text.strip()

    # Strip markdown fences like ```json ... ```
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\s*", "", text)
        text = re.sub(r"```$", "", text).strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except Exception:
        pass

    # Fallback: grab from first '{' to last '}' and try that
    try:
        start = text.index("{")
        end = text.rindex("}")
        json_str = text[start : end + 1]
        return json.loads(json_str)
    except Exception:
        return None


def run_industrypath_pipeline(user_idea: str) -> dict:
    """
    Runs the entire agentic workflow and returns structured data
    for the frontend.

    - raw_text: whatever CrewAI returned as the final result
    - parsed: JSON object if we could parse it, otherwise None
    """
    result = industrypath_crew.kickoff(
        inputs={
            "idea": user_idea,
        }
    )

    raw_text = str(result)
    parsed = _extract_json(raw_text)

    return {
        "raw_text": raw_text,
        "parsed": parsed,
    }
