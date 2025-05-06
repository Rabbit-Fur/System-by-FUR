# upload_and_push_github_service.py

from github_service import create_branch, commit_file, create_pull_request
from dotenv import load_dotenv
load_dotenv()


# Datei laden
with open("github_service.py", "r", encoding="utf-8") as f:
    content = f.read()

branch = create_branch("main", "auto/update-uqm")
commit_file("app/services/github_service.py", content,
            branch, "Add GitHub service for automation")
create_pull_request(
    title="Add github_service.py for automated PR/commit handling",
    body="Diese Datei integriert GitHub API Unterstützung für Branches, Commits und PRs."
)
