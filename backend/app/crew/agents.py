# backend/app/crew/agents.py
from crewai import Agent
from .llm import gemini_llm
from .tools import web_search_tool, scrape_tool

idea_clarifier_agent = Agent(
    role="Idea Clarifier",
    goal=(
        "Convert vague industrial or product ideas into a clear learning goal, "
        "with specific technical keywords and reasonable scope for a student."
    ),
    backstory=(
        "You are an expert educator and engineer who helps beginners define "
        "what exactly they want to build or understand."
    ),
    llm=gemini_llm,
    verbose=True,
)

research_agent = Agent(
    role="Research Scout",
    goal=(
        "Search the web and identify the most important concepts, components, "
        "and subtopics needed to understand and build the product idea."
    ),
    backstory=(
        "You are a meticulous research assistant who can search the web, scan "
        "multiple pages, and extract only the most useful, beginner-friendly information."
    ),
    tools=[web_search_tool, scrape_tool],
    llm=gemini_llm,
    verbose=True,
)

roadmap_agent = Agent(
    role="Roadmap Designer",
    goal=(
        "Turn messy research into a concise project topic and a step-by-step "
        "learning roadmap tailored to a college student."
    ),
    backstory=(
        "You specialize in curriculum design and project scoping. "
        "You avoid jargon and keep things actionable."
    ),
    llm=gemini_llm,
    verbose=True,
)

industry_agent = Agent(
    role="Industry Bridge",
    goal=(
        "Given the topic and roadmap, identify companies, communities, and "
        "courses that connect the user to real-world exposure."
    ),
    backstory=(
        "You are well-connected with industry and know where people can learn, "
        "find communities, and follow relevant companies online."
    ),
    tools=[web_search_tool],
    llm=gemini_llm,
    verbose=True,
)
