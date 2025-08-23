#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: project_management_system
File: project_management_system.py
Path: autoprojectmanagement/main_modules/project_management_system.py

Description:
    Project Management System module

Author: AutoProjectManagement Team
Contact: team@autoprojectmanagement.com
Repository: https://github.com/autoprojectmanagement/autoprojectmanagement

Version Information:
    Current Version: 1.0.0
    Last Updated: 2025-08-14
    Python Version: 3.8+
    
Development Status:
    Status: Production/Stable
    Created: 2024-01-01
    Last Modified: 2025-08-14
    Modified By: AutoProjectManagement Team

Dependencies:
    - Python 3.8+
    - See requirements.txt for full dependency list

License: MIT License
Copyright: (c) 2024 AutoProjectManagement Team

Usage:
    This module is part of the AutoProjectManagement package.
    Import and use as needed within the package ecosystem.

Example:
    >>> from autoprojectmanagement.main_modules.project_management_system import {main_class}
    >>> instance = {main_class}()
    >>> instance.run()

Notes:
    - This file follows the AutoProjectManagement coding standards
    - All changes should be documented in the changelog below
    - Ensure compatibility with Python 3.8+

Changelog:
    1.0.0 (2024-01-01): Initial release
    1.0.1 (2025-08-14): {change_description}

TODO:
    - [ ] Add comprehensive error handling
    - [ ] Implement logging throughout
    - [ ] Add unit tests
    - [ ] Update documentation

================================================================================
"""


import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from pathlib import Path

# Constants
DEFAULT_PROJECT_FIELDS = {"id", "name"}
REQUIRED_TASK_FIELDS = {"id", "title"}
MAX_PROJECT_NAME_LENGTH = 100
MAX_TASK_TITLE_LENGTH = 200
DEFAULT_DATA_DIR = Path(".auto_project_data")
PROJECTS_FILE = DEFAULT_DATA_DIR / "projects.json"
TASKS_FILE = DEFAULT_DATA_DIR / "tasks.json"

# Configure logging
logger = logging.getLogger(__name__)

class ProjectManagementSystem:
    """
    Main class for managing projects and tasks with comprehensive functionality.
    
    This class provides a centralized system for managing projects, their tasks,
    and maintaining data integrity across operations. It supports CRUD operations
    for both projects and tasks with proper error handling and validation.
    
    Attributes:
        projects: Dictionary mapping project IDs to project data
        tasks: Nested dictionary mapping project IDs to task dictionaries
        is_initialized: Flag indicating system initialization status
        
    Example:
        >>> pms = ProjectManagementSystem()
        >>> pms.initialize_system()
        True
        >>> project = {"id": 1, "name": "Test Project"}
        >>> pms.add_project(project)
        True
    """
    
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
