import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

# This file houses the business logic, making it independent of both the
# API framework (FastAPI) and the CLI framework (Click). This is a key
# part of the refactoring.

# Future imports from main_modules:
# from autoprojectmanagement.main_modules.progress_calculator_refactored import calculate_project_progress
# from autoprojectmanagement.main_modules.reporting import generate_status_report


class ProjectService:
    """
    A service class to handle project-related business logic.
    
    Acts as a bridge between API endpoints and core logic modules,
    providing a clean separation between presentation and business layers.
    """

    def __init__(self) -> None:
        """
        Initialize the service with data storage paths.
        
        Sets up paths relative to this file's location to ensure
        consistent behavior regardless of execution context.
        """
        self.db_path: Path = Path(__file__).resolve().parents[2] / 'JSonDataBase'
        self.inputs_path: Path = self.db_path / 'Inputs'
        self.outputs_path: Path = self.db_path / 'OutPuts'

    def get_status(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve and calculate the status of a given project.
        
        This method replaces CLICommands.get_project_status, returning
        structured data instead of formatted strings.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dict containing status information, or None if project
            is not found. Returns error dict if file operations fail.
            
        Raises:
            No exceptions are raised; errors are returned as dict values.
        """
        task_db_path: Path = (
            self.inputs_path / 'UserInputs' / 'commit_task_database.json'
        )

        if not task_db_path.exists():
            return None

        try:
            with open(task_db_path, 'r', encoding='utf-8') as file:
                tasks_data: Union[list, dict] = json.load(file)
        except IOError as e:
            return {
                "error": f"Could not read task database: {str(e)}"
            }
        except json.JSONDecodeError as e:
            return {
                "error": f"Invalid JSON in task database: {str(e)}"
            }

        if not isinstance(tasks_data, list):
            return {
                "error": (
                    "Task database format error: expected list "
                    f"but got {type(tasks_data).__name__}"
                )
            }

        total_tasks: int = len(tasks_data)
        completed_tasks: int = sum(
            1 for task in tasks_data 
            if isinstance(task, dict) and task.get('status') == 'Done'
        )
        
        progress: float = (
            (completed_tasks / total_tasks) * 100 
            if total_tasks > 0 
            else 0.0
        )

        # Determine project summary based on progress
        if progress == 0:
            summary: str = "Project not started."
        elif progress >= 100:
            summary = "Project completed."
        else:
            summary = "Project is in progress."

        status_info: Dict[str, Any] = {
            "project_id": project_id,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "progress_percentage": round(progress, 2),
            "summary": summary,
            "source_file": str(task_db_path)
        }

        return status_info

    def get_project_list(self) -> Dict[str, Any]:
        """
        Retrieve list of available projects.
        
        Returns:
            Dict containing list of projects and metadata
        """
        # Placeholder for future implementation
        return {
            "projects": [],
            "count": 0,
            "message": "Project listing not yet implemented"
        }


# Singleton instance for API endpoints
project_service: ProjectService = ProjectService()
