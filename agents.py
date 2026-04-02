from crewai import Agent, LLM
from tools import repo_structure_tool, repo_file_content_tool
from dotenv import load_dotenv
import os

load_dotenv()

# OpenRouter via CrewAI/LiteLLM
# Community guidance: use OPENAI_API_KEY and prefix model with openrouter/
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/microsoft/phi-3-mini-128k-instruct:free"
)

llm = LLM(
    model=OPENROUTER_MODEL,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.3
)
repo_researcher = Agent(
    role="Git Repository Analyzer",
    goal=(
        "Understand the repository efficiently by first inspecting the repo structure, "
        "then fetching only the most relevant files needed for analysis."
    ),
    verbose=False,
    memory=False,
    backstory=(
        "You are a software analyst who minimizes token usage by first reading the repo tree "
        "and then requesting only exact files needed for architecture and documentation."
    ),
    tools=[repo_structure_tool, repo_file_content_tool],
    allow_delegation=False,
    llm=llm
)

doc_writer = Agent(
    role="Technical Markdown Documentation Writer",
    goal=(
        "Create structured markdown documentation using the analyzed repository details."
    ),
    verbose=False,
    memory=False,
    backstory=(
        "You convert repository analysis into concise and useful developer documentation."
    ),
    allow_delegation=False,
    llm=llm
)