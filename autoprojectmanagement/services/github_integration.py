import requests
import os
import logging
import time

class GitHubIntegration:
    def __init__(self, repo_owner, repo_name, token=None, max_retries=3, retry_delay=2):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def _get(self, url, params=None):
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}. Retry {retries + 1} of {self.max_retries}")
                retries += 1
                time.sleep(self.retry_delay)
        self.logger.error(f"Failed to get data from {url} after {self.max_retries} retries.")
        return None

    def get_issues(self, state="open"):
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/issues"
        params = {"state": state}
        data = self._get(url, params)
        if data is None:
            self.logger.error("Failed to retrieve issues.")
            return []
        return data

    def get_commits(self, per_page=30):
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/commits"
        params = {"per_page": per_page}
        data = self._get(url, params)
        if data is None:
            self.logger.error("Failed to retrieve commits.")
            return []
        return data

    def get_pull_requests(self, state="open"):
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/pulls"
        params = {"state": state}
        data = self._get(url, params)
        if data is None:
            self.logger.error("Failed to retrieve pull requests.")
            return []
        return data

if __name__ == "__main__":
    # Example usage
    repo_owner = "your_org_or_username"
    repo_name = "ProjectManagement"
    github = GitHubIntegration(repo_owner, repo_name)
    issues = github.get_issues()
    print(f"Open issues: {len(issues)}")
    commits = github.get_commits()
    print(f"Recent commits: {len(commits)}")
    prs = github.get_pull_requests()
    print(f"Open pull requests: {len(prs)}")
