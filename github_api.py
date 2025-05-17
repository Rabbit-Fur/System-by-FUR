import requests
from env_helpers import get_env_str

def fetch_repo_info(owner: str, repo: str) -> dict:
    token = get_env_str("FUR_PAT")

    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GitHub API Fehler {response.status_code}: {response.text}")
