import json
from pathlib import Path
from typing import Any, Dict, Optional

# This file will house the business logic, making it independent of both the
# API framework (FastAPI) and the CLI framework (Click). This is a key
# part of the refactoring.

# We will eventually import directly from `main_modules` to perform tasks.
# For example:
# from autoprojectmanagement.main_modules.progress_calculator_refactored import calculate_project_progress
# from autoprojectmanagement.main_modules.reporting import generate_status_report

class ProjectService:
    """
    A service class to handle project-related business logic.
    It acts as a bridge between the API endpoints and the core logic modules.
    """

    def __init__(self):
        """
        Initializes the service, setting up paths to the data storage.
        """
        # The base path is calculated relative to this file's location to ensure it works
        # regardless of where the application is run from.
        self.db_path = Path(__file__).resolve().parents[2] / 'JSonDataBase'
        self.inputs_path = self.db_path / 'Inputs'
        self.outputs_path = self.db_path / 'OutPuts'

    def get_status(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves and calculates the status of a given project.

        This method is the new home for the logic that was in `CLICommands.get_project_status`.
        Instead of returning a formatted string, it returns structured data (a dictionary).

        Args:
            project_id: The ID or name of the project. For now, we assume it maps
                        to a file or a key in the JSON database.

        Returns:
            A dictionary containing status information, or None if the project is not found.
        """
        # This is a placeholder implementation. The real implementation will
        # involve reading the relevant JSON files and calling logic from `main_modules`.
        
        # Example: Check for a project's task database
        # Note: The project_id needs to be mapped to actual files. This is a simplification.
        task_db_path = self.inputs_path / 'UserInputs' / 'commit_task_database.json'

        if not task_db_path.exists():
            return None

        try:
            with open(task_db_path, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
        except (IOError, json.JSONDecodeError):
            # Handle cases where the file is unreadable or not valid JSON
            return {"error": "Could not read or parse the task database."}

        # This is a simplified calculation. The real calculation would be more complex
        # and likely handled by a dedicated module in `main_modules`.
        # We assume `tasks_data` is a list of task dictionaries for this example.
        if not isinstance(tasks_data, list):
             return {"error": "Task database is not in the expected format (a list of tasks)."}

        total_tasks = len(tasks_data)
        completed_tasks = sum(1 for task in tasks_data if task.get('status') == 'Done')
        progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        # This is the structured data that our API will return.
        status_info = {
            "project_id": project_id,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "progress_percentage": round(progress, 2),
            "summary": "Project is in progress." if progress < 100 and progress > 0 else "Project not started." if progress == 0 else "Project completed.",
            "source_file": str(task_db_path)
        }

        return status_info

# A single instance of the service that can be imported and used by API endpoints.
# This follows the singleton pattern for this context.
project_service = ProjectService()