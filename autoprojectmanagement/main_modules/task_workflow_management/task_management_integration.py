#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/task_workflow_management/task_management_integration.py
File: task_management_integration.py
Purpose: Task management integration
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Task management integration within the AutoProjectManagement system
"""

import logging
from typing import Dict, Any, Optional, List, Union
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CURRENT_VERSION = "2.0.0"
PYTHON_MIN_VERSION = "3.8+"
CREATED_DATE = "2025-08-14"
MODIFIED_DATE = "2025-08-14"

# Module-level docstring
__doc__ = """
Task management integration within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path

from .task_management import TaskManagement
from autoprojectmanagement.services.github_integration import GitHubIntegration

# Configure logging
logger = logging.getLogger(__name__)

# Constants
DEFAULT_REPO = "user/repo"
GITHUB_TOKEN_ENV = "GITHUB_TOKEN"
MAX_SYNC_RETRIES = 3
SYNC_RETRY_DELAY = 1.0

class SyncStatus(Enum):
    """Enumeration for synchronization status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class IntegrationConfig:
    """Configuration for task management integration."""
    github_token: Optional[str] = None
    repository: str = DEFAULT_REPO
    auto_sync: bool = True
    sync_interval: int = 300  # seconds
    dry_run: bool = False

class TaskManagementIntegration:
    """
    Integration layer for task management with GitHub and project management systems.
    
    This class provides seamless integration between task management functionality
    and GitHub issues, enabling automated synchronization and workflow management.
    
    Attributes:
        task_manager: Instance of TaskManagement for task operations
        github: Instance of GitHubIntegration for GitHub operations
        config: Integration configuration settings
    """
    
    def __init__(self, config: Optional[IntegrationConfig] = None) -> None:
        """
        Initialize the TaskManagementIntegration instance.
        
        Args:
            config: Configuration object for integration settings
            
        Raises:
            ValueError: If configuration is invalid
        """
        self.config = config or IntegrationConfig()
        self.task_manager = TaskManagement()
        self.github = GitHubIntegration(
            token=self.config.github_token or os.getenv(GITHUB_TOKEN_ENV),
            repo=self.config.repository
        )
        
        # Validate configuration
        self._validate_config()
        
        logger.info("TaskManagementIntegration initialized successfully")
    
    def _validate_config(self) -> None:
        """Validate the integration configuration."""
        if not self.config.repository or '/' not in self.config.repository:
            raise ValueError(
                f"Invalid repository format: {self.config.repository}. "
                "Expected format: 'owner/repo'"
            )
        
        if self.config.sync_interval < 60:
            logger.warning(
                f"Sync interval {self.config.sync_interval}s is very short. "
                "Consider increasing for better performance."
            )
    
    def generate_and_prioritize_tasks(self, project_idea: str) -> List[Dict[str, Any]]:
        """
        Generate WBS from project idea and prioritize tasks.
        
        Args:
            project_idea: Description of the project idea
            
        Returns:
            List of prioritized task dictionaries with urgency/importance scores
            
        Example:
            >>> integration = TaskManagementIntegration()
            >>> tasks = integration.generate_and_prioritize_tasks(
            ...     "Develop a web-based project management tool"
            ... )
            >>> print(tasks[0]['title'], tasks[0]['urgency_score'])
        """
        try:
            logger.info(f"Generating tasks for project: {project_idea}")
            
            # Generate WBS from project idea
            wbs_tasks = self.task_manager.generate_wbs_from_idea(project_idea)
            logger.debug(f"Generated {len(wbs_tasks)} WBS tasks")
            
            # Calculate urgency and importance
            self.task_manager.calculate_urgency_importance()
            
            # Prioritize tasks
            prioritized_tasks = self.task_manager.prioritize_tasks()
            logger.info(f"Prioritized {len(prioritized_tasks)} tasks")
            
            return prioritized_tasks
            
        except Exception as e:
            logger.error(f"Error generating and prioritizing tasks: {str(e)}")
            raise
    
    def sync_tasks_to_github(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Synchronize tasks to GitHub issues with retry logic.
        
        Args:
            tasks: List of task dictionaries to sync
            
        Returns:
            List of synced tasks with GitHub issue numbers
            
        Raises:
            ConnectionError: If GitHub API is unreachable
            ValueError: If task format is invalid
            
        Example:
            >>> integration = TaskManagementIntegration()
            >>> tasks = [{'id': 1, 'title': 'Setup project', 'description': '...'}]
            >>> synced = integration.sync_tasks_to_github(tasks)
            >>> print(f"Created issue #{synced[0]['github_issue_number']}")
        """
        if self.config.dry_run:
            logger.info("Dry run mode - skipping GitHub sync")
            return tasks
        
        if not tasks:
            logger.warning("No tasks provided for sync")
            return []
        
        try:
            logger.info(f"Syncing {len(tasks)} tasks to GitHub")
            
            # Validate task format
            self._validate_task_format(tasks)
            
            # Sync with retry logic
            synced_tasks = self._sync_with_retry(tasks)
            
            logger.info(f"Successfully synced {len(synced_tasks)} tasks")
            return synced_tasks
            
        except Exception as e:
            logger.error(f"Failed to sync tasks to GitHub: {str(e)}")
            raise
    
    def _validate_task_format(self, tasks: List[Dict[str, Any]]) -> None:
        """
        Validate the format of tasks before syncing.
        
        Args:
            tasks: List of task dictionaries
            
        Raises:
            ValueError: If task format is invalid
        """
        required_fields = {'id', 'title'}
        
        for task in tasks:
            if not isinstance(task, dict):
                raise ValueError(f"Task must be a dictionary, got {type(task)}")
            
            missing_fields = required_fields - set(task.keys())
            if missing_fields:
                raise ValueError(
                    f"Task missing required fields: {missing_fields}"
                )
    
    def _sync_with_retry(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sync tasks to GitHub with retry mechanism.
        
        Args:
            tasks: List of tasks to sync
            
        Returns:
            List of synced tasks
            
        Raises:
            ConnectionError: If sync fails after retries
        """
        last_error = None
        
        for attempt in range(MAX_SYNC_RETRIES):
            try:
                return self.github.sync_tasks_to_github(tasks)
                
            except Exception as e:
                last_error = e
                logger.warning(
                    f"Sync attempt {attempt + 1} failed: {str(e)}"
                )
                
                if attempt < MAX_SYNC_RETRIES - 1:
                    import time
                    time.sleep(SYNC_RETRY_DELAY)
        
        raise ConnectionError(
            f"Failed to sync tasks after {MAX_SYNC_RETRIES} attempts"
        )

    def get_sync_status(self) -> Dict[str, Any]:
        """
        Get the current synchronization status.
        
        Returns:
            Dictionary containing sync status information
        """
        return {
            "repository": self.config.repository,
            "auto_sync": self.config.auto_sync,
            "sync_interval": self.config.sync_interval,
            "dry_run": self.config.dry_run
        }

    def validate_configuration(self) -> bool:
        """
        Validate the current configuration settings.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            self._validate_config()
            return True
        except ValueError as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            return False


def main() -> None:
    """
    Main function to demonstrate task management integration.
    
    This function serves as an example of how to use the TaskManagementIntegration
    class to generate and prioritize tasks, then sync them to GitHub.
    
    Example:
        >>> main()
    """
    try:
        # Initialize integration with default configuration
        integration = TaskManagementIntegration()
        
        # Validate configuration
        if not integration.validate_configuration():
            logger.error("Invalid configuration. Please check settings.")
            return
        
        # Example: Generate and prioritize tasks
        project_idea = "Develop a web-based project management tool"
        prioritized_tasks = integration.generate_and_prioritize_tasks(project_idea)
        
        # Sync tasks to GitHub
        synced_tasks = integration.sync_tasks_to_github(prioritized_tasks)
        
        # Print results
        print(f"Successfully synced {len(synced_tasks)} tasks to GitHub")
        for task in synced_tasks:
            print(
                f"Task ID: {task.get('id')}, "
                f"Title: {task.get('title')}, "
                f"GitHub Issue #: {task.get('github_issue_number')}"
            )
            
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()
