import requests

class GitHubIntegration:
    def __init__(self, owner: str, repo: str, token: str = None):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.api_url = f"https://api.github.com/repos/{owner}/{repo}"

    def _get_headers(self):
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def get_issues(self, state="open", labels=None):
        url = f"{self.api_url}/issues"
        params = {
            "state": state,
            "labels": labels if labels else ""
        }
        response = requests.get(url, headers=self._get_headers(), params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
