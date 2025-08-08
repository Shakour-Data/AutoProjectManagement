from .task_management import TaskManagement
from project_management.modules.services.github_integration import GitHubIntegration

def main():
    # Initialize Task Management and GitHub Integration
    tm = TaskManagement()
    gh = GitHubIntegration(token=None, repo='user/repo')  # Replace with actual repo

    # Example: Generate WBS from a project idea
    wbs_tasks = tm.generate_wbs_from_idea("Develop Project Management Tool")

    # Calculate urgency and importance, prioritize tasks
    tm.calculate_urgency_importance()
    prioritized_tasks = tm.prioritize_tasks()

    # Sync tasks to GitHub issues
    synced_tasks = gh.sync_tasks_to_github(prioritized_tasks)

    # Print synced tasks with GitHub issue numbers
    for task in synced_tasks:
        print(f"Task ID: {task.id}, Title: {task.title}, GitHub Issue #: {task.github_issue_number}")

if __name__ == "__main__":
    main()
