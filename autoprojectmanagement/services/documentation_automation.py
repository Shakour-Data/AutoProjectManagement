from ..services.github_integration import GitHubIntegration
import datetime
import logging

class DocumentationAutomation:
    def __init__(self, github_integration, max_retries=3, retry_delay=2):
        self.github = github_integration
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def generate_changelog(self, since_date=None):
        retries = 0
        while retries < self.max_retries:
            try:
                commits = self.github.get_commits(per_page=100)
                changelog_entries = []
                for commit in commits:
                    commit_date = commit['commit']['author']['date']
                    if since_date and commit_date < since_date:
                        continue
                    message = commit['commit']['message']
                    sha = commit['sha'][:7]
                    changelog_entries.append(f"- {commit_date[:10]}: {message} ({sha})")
                return "\n".join(changelog_entries)
            except Exception as e:
                self.logger.error(f"Error generating changelog: {e}. Retry {retries + 1} of {self.max_retries}")
                retries += 1
        self.logger.error("Failed to generate changelog after retries.")
        return ""

    def generate_release_notes(self, tag_name):
        try:
            # Placeholder for release notes generation based on tag
            # Could be extended to fetch PRs merged since last tag
            return f"Release notes for {tag_name} - generated on {datetime.datetime.now().strftime('%Y-%m-%d')}"
        except Exception as e:
            self.logger.error(f"Error generating release notes: {e}")
            return ""

if __name__ == "__main__":
    repo_owner = "your_org_or_username"
    repo_name = "ProjectManagement"
    github = GitHubIntegration(repo_owner, repo_name)
    doc_auto = DocumentationAutomation(github)
    changelog = doc_auto.generate_changelog()
    print("Changelog:\n", changelog)
    release_notes = doc_auto.generate_release_notes("v1.0.0")
    print("\nRelease Notes:\n", release_notes)
