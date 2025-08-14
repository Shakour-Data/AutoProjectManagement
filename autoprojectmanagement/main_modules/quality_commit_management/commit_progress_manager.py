#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/quality_commit_management/commit_progress_manager.py
File: commit_progress_manager.py
Purpose: Commit progress tracking
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Commit progress tracking within the AutoProjectManagement system
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
Commit progress tracking within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_COMMIT_TASK_DB_PATH = 'JSonDataBase/OutPuts/commit_task_database.json'
DEFAULT_COMMIT_PROGRESS_PATH = 'JSonDataBase/OutPuts/commit_progress.json'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
MAX_PROGRESS_PERCENTAGE = 100
COMMIT_PROGRESS_MULTIPLIER = 10


class CommitProgressManager:
    """
    Manages commit progress tracking for project tasks.
    
    This class loads commit task data, calculates progress metrics,
    and saves progress information for tracking purposes.
    
    The manager processes commit-task relationships and calculates
    progress percentages based on commit frequency for each task.
    
    Attributes:
        commit_task_db_path: Path to the commit task database JSON file
        commit_progress_path: Path where progress data will be saved
        commit_task_db: Dictionary containing commit-task mappings
        commit_progress: Dictionary containing calculated progress metrics
    
    Example:
        >>> manager = CommitProgressManager()
        >>> manager.load_commit_task_db()
        >>> manager.generate_commit_progress()
        >>> summary = manager.get_progress_summary()
        >>> print(f"Processed {summary['total_tasks']} tasks")
    """
    
    def __init__(
        self,
        commit_task_db_path: str = DEFAULT_COMMIT_TASK_DB_PATH,
        commit_progress_path: str = DEFAULT_COMMIT_PROGRESS_PATH
    ) -> None:
        """
        Initialize the CommitProgressManager.
        
        Args:
            commit_task_db_path: Path to the commit task database file
            commit_progress_path: Path to save commit progress data
        """
        self.commit_task_db_path: str = commit_task_db_path
        self.commit_progress_path: str = commit_progress_path
        self.commit_task_db: Dict[str, Dict[str, Any]] = {}
        self.commit_progress: Dict[str, Dict[str, Any]] = {}

    def load_commit_task_db(self) -> None:
        """Load commit task database from JSON file."""
        try:
            if os.path.exists(self.commit_task_db_path):
                with open(self.commit_task_db_path, 'r', encoding='utf-8') as f:
                    self.commit_task_db = json.load(f)
            else:
                self.commit_task_db = {}
                print(f"Warning: Commit task database not found at {self.commit_task_db_path}")
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error loading commit task database: {e}")
            self.commit_task_db = {}

    def generate_commit_progress(self) -> None:
        """
        Generate commit progress per task based on commit_task_database.
        
        For each task, calculate:
        - Number of commits
        - Last commit date
        - Progress percentage (based on commit count)
        """
        task_commits: Dict[str, Dict[str, Any]] = {}
        
        for commit_hash, task_info in self.commit_task_db.items():
            task_id = task_info.get('task_id')
            commit_date_str = task_info.get('commit_date')
            
            if not task_id or not commit_date_str:
                continue
                
            try:
                commit_date = datetime.strptime(commit_date_str, DATETIME_FORMAT)
            except ValueError:
                print(f"Warning: Invalid date format for commit {commit_hash}")
                continue
            
            if task_id not in task_commits:
                task_commits[task_id] = {
                    'commit_count': 0,
                    'last_commit_date': commit_date,
                }
            
            task_commits[task_id]['commit_count'] += 1
            if commit_date > task_commits[task_id]['last_commit_date']:
                task_commits[task_id]['last_commit_date'] = commit_date

        # Calculate progress percentage
        for task_id, data in task_commits.items():
            commit_count = data['commit_count']
            progress_percent = min(
                commit_count * COMMIT_PROGRESS_MULTIPLIER,
                MAX_PROGRESS_PERCENTAGE
            )
            self.commit_progress[task_id] = {
                'commit_count': commit_count,
                'last_commit_date': data['last_commit_date'].isoformat(),
                'progress_percent': progress_percent
            }

    def save_commit_progress(self) -> bool:
        """
        Save commit progress data to JSON file.
        
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(self.commit_progress_path), exist_ok=True)
            with open(self.commit_progress_path, 'w', encoding='utf-8') as f:
                json.dump(self.commit_progress, f, indent=2, ensure_ascii=False)
            return True
        except (OSError, json.JSONEncodeError) as e:
            print(f"Error saving commit progress: {e}")
            return False

    def get_progress_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all commit progress data.
        
        Returns:
            Dict containing summary statistics:
            - total_tasks: Total number of tasks with commits
            - total_commits: Total number of commits across all tasks
            - average_progress: Average progress percentage
            - tasks_with_progress: List of task progress details
        """
        if not self.commit_progress:
            return {
                'total_tasks': 0,
                'total_commits': 0,
                'average_progress': 0.0,
                'tasks_with_progress': []
            }
        
        total_tasks = len(self.commit_progress)
        total_commits = sum(data['commit_count'] for data in self.commit_progress.values())
        average_progress = sum(
            data['progress_percent'] for data in self.commit_progress.values()
        ) / total_tasks
        
        return {
            'total_tasks': total_tasks,
            'total_commits': total_commits,
            'average_progress': round(average_progress, 2),
            'tasks_with_progress': list(self.commit_progress.items())
        }

    def run(self) -> bool:
        """
        Execute the complete commit progress management workflow.
        
        Returns:
            bool: True if all operations completed successfully
        """
        try:
            self.load_commit_task_db()
            self.generate_commit_progress()
            success = self.save_commit_progress()
            if success:
                print(f"Commit progress saved to {self.commit_progress_path}")
            return success
        except Exception as e:
            print(f"Error running commit progress manager: {e}")
            return False

if __name__ == "__main__":
    manager = CommitProgressManager()
    manager.run()
