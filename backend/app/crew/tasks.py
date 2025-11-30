# backend/app/crew/tasks.py

from crewai import Task
from .agents import (
    idea_clarifier_agent,
    research_agent,
    roadmap_agent,
    industry_agent,
)

# Task 1: Clarify the user's idea
clarify_idea_task = Task(
    description=(
        "The user has the following vague idea about an industrial or product project:\n\n"
        "{idea}\n\n"
        "Your job is to clarify what exactly they want to build or understand. "
        "Output a concise JSON-like structure with fields:\n"
        "- refined_goal: a clear description of what they should aim to learn or build\n"
        "- keywords: a list of 5–10 important technical keywords for searching\n"
        "- domain: a simple label like 'hardware', 'software', 'electronics', etc.\n"
    ),
    agent=idea_clarifier_agent,
    expected_output=(
        "A short JSON-like structure describing refined_goal, keywords, and domain."
    ),
)

# Task 2: Research based on the clarified idea
research_task = Task(
    description=(
        "Using the clarified idea, refined goal, and keywords produced in the previous task, "
        "search the web and identify the most important concepts, components, and practical "
        "subtopics needed to understand and start working on this project.\n\n"
        "You have access to web search tools. Use them to find 5–10 high-value resources "
        "(articles, tutorials, overviews, etc.).\n\n"
        "Summarize your findings in a JSON-like structure with keys:\n"
        "- key_concepts: list of the most important theoretical ideas\n"
        "- subtopics: list of practical subtopics or components to learn about\n"
        "- helpful_links: array of objects with fields {title, url, note}\n"
    ),
    agent=research_agent,
    expected_output=(
        "JSON with key_concepts, subtopics, and helpful_links (title, url, note)."
    ),
)

# Task 3: Turn research into a roadmap
roadmap_task = Task(
    description=(
        "From the research summary (key_concepts, subtopics, helpful_links) produced in the "
        "earlier task, design a concrete learning roadmap for a college student.\n\n"
        "Your output must:\n"
        "1) Propose a concise project_topic the student can realistically attempt.\n"
        "2) Provide a 5–7 step learning_roadmap, where each step has:\n"
        "   - title: short title of the step\n"
        "   - description: 2–3 sentence explanation of what to do/learn in this step\n\n"
        "Return a JSON-like structure with keys: project_topic, learning_roadmap."
    ),
    agent=roadmap_agent,
    expected_output="JSON with project_topic and learning_roadmap.",
)

# Task 4: Connect to industry & real-world exposure, AND summarize everything
industry_task = Task(
    description=(
        "You are the final agent in a pipeline that has already:\n"
        "1) Clarified the user's vague idea into a refined goal and keywords.\n"
        "2) Researched key concepts, subtopics, and helpful links.\n"
        "3) Designed a concrete project topic and learning roadmap.\n\n"
        "Using the FULL conversation history so far, do the following:\n"
        "- Recover and restate the final clarified goal.\n"
        "- Recover and restate the most important keywords.\n"
        "- Recover and restate the chosen project topic.\n"
        "- Recover and restate the learning roadmap steps.\n"
        "- Additionally, identify up to 5 relevant companies, 3–5 online communities,\n"
        "  and 2–3 good courses or structured resources.\n\n"
        "You may use web search tools to find real and useful links for companies,\n"
        "communities, and courses.\n\n"
        "Return ONE JSON object with exactly these keys:\n"
        "- refined_goal: string\n"
        "- keywords: array of strings\n"
        "- project_topic: string\n"
        "- learning_roadmap: array of objects {title, description}\n"
        "- companies: array of {name, url, short_note}\n"
        "- communities: array of {name, url, why_relevant}\n"
        "- courses: array of {title, url, level}\n"
        "Ensure the output is valid JSON (no trailing commas, double quotes around keys and strings)."
    ),
    agent=industry_agent,
    expected_output=(
        "A single valid JSON object with keys: refined_goal, keywords, project_topic, "
        "learning_roadmap, companies, communities, courses."
    ),
)

