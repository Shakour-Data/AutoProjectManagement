from project_management.modules.services.github_integration import GitHubIntegration
from project_management.modules.main_modules.risk_management import RiskManagement
from project_management.modules.services.documentation_automation import DocumentationAutomation

class CommunicationRiskDocIntegration:
    def __init__(self, repo_owner, repo_name, token=None):
        self.github = GitHubIntegration(repo_owner, repo_name, token)
        self.risk_manager = RiskManagement(self.github)
        self.doc_automation = DocumentationAutomation(self.github)

    def run_all(self):
        # Identify risks and get summary
        risks = self.risk_manager.identify_risks()
        risk_summary = self.risk_manager.get_risk_summary()

        # Generate changelog and release notes
        changelog = self.doc_automation.generate_changelog()
        release_notes = self.doc_automation.generate_release_notes("latest")

        return {
            "risks": risks,
            "risk_summary": risk_summary,
            "changelog": changelog,
            "release_notes": release_notes
        }

if __name__ == "__main__":
    repo_owner = "your_org_or_username"
    repo_name = "ProjectManagement"
    token = None  # Or set your GitHub token here

    integration = CommunicationRiskDocIntegration(repo_owner, repo_name, token)
    results = integration.run_all()

    print("Risk Summary:")
    print(results["risk_summary"])

    print("\nChangelog:")
    print(results["changelog"])

    print("\nRelease Notes:")
    print(results["release_notes"])
