from crewai import Task
from agents import repo_researcher, doc_writer

research_task = Task(
    description=(
        "Analyze the repository at {repo_url}. "
        "First use the repo structure tool to inspect the folder and file layout. "
        "Then fetch only the most relevant files one by one using the single-file tool. "
        "Focus on README, dependency files, entry points, config files, and core source files. "
        "Do not retrieve unnecessary files."
    ),
    expected_output=(
        "A structured repository analysis containing repository purpose, tech stack, "
        "important folders, important files, execution flow, setup, and noteworthy design choices."
    ),
    agent=repo_researcher,
)

write_task = Task(
    description=(
        "Using the repository analysis, create a polished markdown document for the repository."
    ),
    expected_output=(
        "A well-formatted markdown document covering overview, tech stack, setup, architecture, "
        "important files, and how the project works."
    ),
    agent=doc_writer,
    async_execution=False,
    output_file="generated_docs/{file_name}"
)