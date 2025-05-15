# upload_and_push_github_service.py

import os
from dotenv import load_dotenv
from github_service import commit_file, create_branch, create_pull_request

# 🌱 .env laden (für GITHUB_TOKEN etc.)
load_dotenv()

# 🔁 Konfiguration
SOURCE_FILE = "github_service.py"
DESTINATION_PATH = "app/services/github_service.py"
BRANCH_NAME = "auto/update-uqm"
BASE_BRANCH = "main"
COMMIT_MESSAGE = "Add GitHub service for automation"
PR_TITLE = "Add github_service.py for automated PR/commit handling"
PR_BODY = "Diese Datei integriert GitHub API Unterstützung für Branches, Commits und PRs."

# 📄 Dateiinhalt laden
if not os.path.exists(SOURCE_FILE):
    raise FileNotFoundError(f"❌ Datei nicht gefunden: {SOURCE_FILE}")

with open(SOURCE_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 🧪 Branch erstellen (falls noch nicht vorhanden)
branch = create_branch(BASE_BRANCH, BRANCH_NAME)

# 📦 Datei in GitHub-Repo committen
commit_file(
    path=DESTINATION_PATH,
    content=content,
    branch=branch,
    message=COMMIT_MESSAGE
)

# 🔀 Pull Request erstellen
create_pull_request(
    title=PR_TITLE,
    body=PR_BODY,
    head=branch,
    base=BASE_BRANCH
)
