"""
Project Management System Module
Provides core functionality for managing projects and tasks
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class ProjectManagementSystem:
    """Main class for managing projects and tasks"""
    
    def __init__(self):
        self.projects: Dict[int, Dict[str, Any]] = {}
        self.tasks: Dict[int, Dict[int, Dict[str, Any]]] = {}  # project_id -> task_id -> task
        self.is_initialized = False
        
    def initialize_system(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Initialize the project management system"""
        if config is not None and not isinstance(config, dict):
            raise TypeError("Configuration must be a dictionary")
            
        self.projects = {}
        self.tasks = {}
        self.is_initialized = True
        return True
        
    def shutdown_system(self) -> bool:
        """Shutdown the project management system"""
        self.is_initialized = False
        return True
        
    def reset_system(self) -> bool:
        """Reset the system to initial state"""
        return self.initialize_system()
        
    def add_project(self, project: Dict[str, Any]) -> bool:
        """Add a new project to the system"""
        if not isinstance(project, dict):
            raise TypeError("Project must be a dictionary")
            
        if 'id' not in project or 'name' not in project:
            raise KeyError("Project must contain 'id' and 'name' fields")
            
        project_id = project['id']
        if project_id in self.projects:
            return False
            
        self.projects[project_id] = project
        self.tasks[project_id] = {}
        return True
        
    def remove_project(self, project_id: int) -> bool:
        """Remove a project from the system"""
        if project_id is None:
            return False
            
        if project_id not in self.projects:
            return False
            
        del self.projects[project_id]
        if project_id in self.tasks:
            del self.tasks[project_id]
        return True
        
    def update_project(self, project: Dict[str, Any]) -> bool:
        """Update an existing project"""
        if not isinstance(project, dict):
            raise TypeError("Project must be a dictionary")
            
        if 'id' not in project:
            raise KeyError("Project must contain 'id' field")
            
        project_id = project['id']
        if project_id not in self.projects:
            return False
            
        self.projects[project_id] = project
        return True
        
    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get a project by ID"""
        if project_id is None:
            return None
        return self.projects.get(project_id)
        
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects"""
        return list(self.projects.values())
        
    def add_task_to_project(self, project_id: int, task: Dict[str, Any]) -> bool:
        """Add a task to a project"""
        if project_id is None or not isinstance(project_id, int):
            return False
            
        if project_id not in self.projects:
            return False
            
        if not isinstance(task, dict):
            raise TypeError("Task must be a dictionary")
            
        if 'id' not in task:
            raise KeyError("Task must contain 'id' field")
            
        task_id = task['id']
        if project_id not in self.tasks:
            self.tasks[project_id] = {}
            
        self.tasks[project_id][task_id] = task
        return True
        
    def remove_task_from_project(self, project_id: int, task_id: int) -> bool:
        """Remove a task from a project"""
        if project_id is None or task_id is None:
            return False
            
        if project_id not in self.tasks:
            return False
            
        if task_id not in self.tasks[project_id]:
            return False
            
        del self.tasks[project_id][task_id]
        return True
        
    def update_task_in_project(self, project_id: int, task: Dict[str, Any]) -> bool:
        """Update a task in a project"""
        if not isinstance(project_id, int):
            raise TypeError("Project ID must be an integer")
            
        if not isinstance(task, dict):
            raise TypeError("Task must be a dictionary")
            
        if 'id' not in task:
            raise KeyError("Task must contain 'id' field")
            
        if project_id not in self.projects:
            return False
            
        task_id = task['id']
        if project_id not in self.tasks or task_id not in self.tasks[project_id]:
            return False
            
        self.tasks[project_id][task_id] = task
        return True
        
    def get_task_from_project(self, project_id: int, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a task from a project"""
        if project_id is None or task_id is None:
            return None
            
        if project_id not in self.tasks:
            return None
            
        return self.tasks[project_id].get(task_id)
        
    def list_tasks_in_project(self, project_id: int) -> List[Dict[str, Any]]:
        """List all tasks in a project"""
        if project_id is None:
            return []
            
        if project_id not in self.tasks:
            return []
            
        return list(self.tasks[project_id].values())

# Global instance
project_management_system = ProjectManagementSystem()
