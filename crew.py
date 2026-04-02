from crewai import Crew, Process
from agents import repo_researcher, doc_writer
from tasks import research_task, write_task

def run_repo_doc_crew(repo_url: str, file_name: str):
    crew = Crew(
        agents=[repo_researcher, doc_writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        memory=True,
        cache=True,
        verbose=False
    )

    result = crew.kickoff(inputs={
        "repo_url": repo_url,
        "file_name": file_name
    })

    return result