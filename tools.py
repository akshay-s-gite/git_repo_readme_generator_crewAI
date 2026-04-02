from __future__ import annotations

import os
import base64
import requests
from typing import Type, Optional
from urllib.parse import urlparse

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("Missing GITHUB_PERSONAL_ACCESS_TOKEN in .env")


def parse_github_repo_url(repo_url: str) -> tuple[str, str]:
    parsed = urlparse(repo_url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        raise ValueError(f"Invalid GitHub repo URL: {repo_url}")
    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo


def github_headers() -> dict:
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


class RepoStructureInput(BaseModel):
    repo_url: str = Field(..., description="GitHub repository URL")
    branch: str = Field(default="main", description="Branch name to inspect")


class RepoFileInput(BaseModel):
    repo_url: str = Field(..., description="GitHub repository URL")
    file_path: str = Field(..., description="Exact path of the file in repo")
    branch: str = Field(default="main", description="Branch name to inspect")


class RepoStructureTool(BaseTool):
    name: str = "repo_structure_tool"
    description: str = (
        "Fetch the repository directory structure from GitHub. "
        "Use this first to understand folders and identify important files."
    )
    args_schema: Type[BaseModel] = RepoStructureInput

    def _run(self, repo_url: str, branch: str = "main") -> str:
        owner, repo = parse_github_repo_url(repo_url)

        branch_resp = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}",
            headers=github_headers(),
            timeout=30,
        )
        if branch_resp.status_code != 200:
            return (
                f"Could not access branch '{branch}'. "
                f"GitHub API status: {branch_resp.status_code}, response: {branch_resp.text}"
            )

        tree_sha = branch_resp.json()["commit"]["commit"]["tree"]["sha"]

        tree_resp = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/trees/{tree_sha}?recursive=1",
            headers=github_headers(),
            timeout=60,
        )
        if tree_resp.status_code != 200:
            return (
                f"Could not fetch repository tree. "
                f"GitHub API status: {tree_resp.status_code}, response: {tree_resp.text}"
            )

        items = tree_resp.json().get("tree", [])

        lines = []
        for item in items:
            item_type = item.get("type", "")
            path = item.get("path", "")
            if item_type == "tree":
                lines.append(f"[DIR]  {path}")
            elif item_type == "blob":
                lines.append(f"[FILE] {path}")

        return "\n".join(lines[:4000])  # keep it bounded


class RepoFileContentTool(BaseTool):
    name: str = "repo_file_content_tool"
    description: str = (
        "Fetch the content of a single file from a GitHub repository. "
        "Use only after identifying the exact file path from repo structure."
    )
    args_schema: Type[BaseModel] = RepoFileInput

    def _run(self, repo_url: str, file_path: str, branch: str = "main") -> str:
        owner, repo = parse_github_repo_url(repo_url)

        resp = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}",
            headers=github_headers(),
            timeout=30,
        )

        if resp.status_code != 200:
            return (
                f"Could not fetch file '{file_path}'. "
                f"GitHub API status: {resp.status_code}, response: {resp.text}"
            )

        data = resp.json()

        if isinstance(data, list):
            return f"'{file_path}' is a directory, not a file."

        if data.get("type") != "file":
            return f"'{file_path}' is not a regular file."

        encoding = data.get("encoding")
        content = data.get("content", "")

        if encoding == "base64":
            decoded = base64.b64decode(content).decode("utf-8", errors="replace")
        else:
            decoded = content

        max_chars = 20000
        if len(decoded) > max_chars:
            decoded = decoded[:max_chars] + "\n\n[TRUNCATED]"

        return f"FILE: {file_path}\n\n{decoded}"


repo_structure_tool = RepoStructureTool()
repo_file_content_tool = RepoFileContentTool()