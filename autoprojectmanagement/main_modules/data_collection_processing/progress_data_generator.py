#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: progress_data_generator
File: progress_data_generator.py
Path: autoprojectmanagement/main_modules/data_collection_processing/progress_data_generator.py

Description:
    Progress Data Generator module

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
    >>> from autoprojectmanagement.main_modules.data_collection_processing.progress_data_generator import {main_class}
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


import json
import logging
import os
import re
import subprocess
from collections import defaultdict
from typing import Dict, List, Optional, Any, Union

logger = logging.getLogger(__name__)

# Constants
DEFAULT_DB_PROGRESS_PATH = os.path.join('docs', 'project_management', 'task_progress.json')
DEFAULT_WORKFLOW_PATH = os.path.join('docs', 'db_json', 'workflow_definition.json')
DEFAULT_COMMIT_PATTERN = r'\b\d+\.\d+\b'
DEFAULT_COMMIT_WEIGHT = 0.6
DEFAULT_WORKFLOW_WEIGHT = 0.4
MAX_LINE_LENGTH = 79


class ProgressDataGenerator:
    """
    Generates progress data for project management by analyzing git commits and workflow.
    
    This class provides functionality to:
    - Parse git commit history
    - Map commits to tasks based on patterns
    - Calculate workflow-based progress
    - Combine multiple progress sources
    - Save progress data to JSON
    """
    
    def __init__(
        self,
        db_progress_json_path: str = DEFAULT_DB_PROGRESS_PATH,
        workflow_definition_path: str = DEFAULT_WORKFLOW_PATH,
        commit_task_id_pattern: str = DEFAULT_COMMIT_PATTERN,
        commit_weight: float = DEFAULT_COMMIT_WEIGHT,
        workflow_weight: float = DEFAULT_WORKFLOW_WEIGHT,
        commit_json_path: Optional[str] = None,
    ) -> None:
        """
        Initialize the ProgressDataGenerator.
        
        Args:
            db_progress_json_path: Path to save progress JSON file
            workflow_definition_path: Path to workflow definition JSON
            commit_task_id_pattern: Regex pattern to extract task IDs from commits
            commit_weight: Weight for commit-based progress (0-1)
            workflow_weight: Weight for workflow-based progress (0-1)
            commit_json_path: Optional path to commit JSON file
        """
        self.db_progress_json_path: str = db_progress_json_path
        self.workflow_definition_path: str = workflow_definition_path
        self.commit_task_id_pattern: str = commit_task_id_pattern
        self.commit_weight: float = commit_weight
        self.workflow_weight: float = workflow_weight
        self.commit_json_path: Optional[str] = commit_json_path

    def run_git_log(self) -> Optional[str]:
        """
        Run git log to get commit history with messages and files changed.
        
        Returns:
            String containing git log output or None if command fails
            
        Example:
            >>> generator = ProgressDataGenerator()
            >>> log_output = generator.run_git_log()
            >>> if log_output:
            ...     commits = generator.parse_git_log(log_output)
        """
        try:
            result = subprocess.run(
                ["git", "log", "--name-only", 
                 "--pretty=format:%H%n%s%n%b%n==END=="],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Git log command failed: {e}")
            return None

    def parse_git_log(self, log_text: str) -> List[Dict[str, Any]]:
        """
        Parse git log output into structured commit data.
        
        Args:
            log_text: Raw git log output string
            
        Returns:
            List of dictionaries, each containing:
            - hash: Commit hash
            - message: Commit message
            - files: List of changed files
            
        Example:
            >>> log_text = "abc123\\nFix bug\\nfile1.py\\n==END=="
            >>> commits = generator.parse_git_log(log_text)
            >>> print(commits[0]['hash'])  # abc123
        """
        commits: List[Dict[str, Any]] = []
        lines = log_text.splitlines()
        i = 0
        
        while i < len(lines):
            # Extract commit hash
            commit_hash = lines[i].strip()
            i += 1
            
            # Extract commit message
            message_lines = []
            while (i < len(lines) and 
                   lines[i].strip() != '' and 
                   lines[i].strip() != '==END=='):
                message_lines.append(lines[i])
                i += 1
            message = "\n".join(message_lines).strip()
            
            # Extract changed files
            files = []
            while i < len(lines) and lines[i].strip() != '==END==':
                if lines[i].strip():
                    files.append(lines[i].strip())
                i += 1
            
            # Skip the ==END== line
            i += 1
            
            commits.append({
                "hash": commit_hash,
                "message": message,
                "files": files
            })
        
        return commits

    def load_workflow_definition(self) -> List[Dict[str, Any]]:
        """
        Load workflow definition from JSON file.
        
        Returns:
            List of workflow steps as dictionaries
            
        Raises:
            FileNotFoundError: If workflow file doesn't exist
            json.JSONDecodeError: If workflow file is invalid JSON
        """
        try:
            with open(self.workflow_definition_path, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
            return workflow
        except FileNotFoundError:
            logger.error(f"Workflow file not found: {self.workflow_definition_path}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in workflow file: {e}")
            return []
        except Exception as e:
            logger.error(f"Failed to load workflow definition: {e}")
            return []

    def map_commits_to_tasks(self, commits: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Map commits to tasks based on commit messages or file paths.
        
        This method looks for task IDs in commit messages using the configured
        regex pattern and calculates progress based on commit frequency.
        
        Args:
            commits: List of commit dictionaries from parse_git_log
            
        Returns:
            Dictionary mapping task IDs to progress percentages (0-100)
            
        Example:
            >>> commits = [{"message": "Fix issue 1.2", "files": []}]
            >>> progress = generator.map_commits_to_tasks(commits)
            >>> print(progress)  # {"1.2": 100.0}
        """
        task_progress: Dict[str, int] = defaultdict(int)
        
        try:
            pattern = re.compile(self.commit_task_id_pattern)
        except re.error as e:
            logger.error(f"Invalid regex pattern: {e}")
            return {}

        for commit in commits:
            message = commit.get('message', '')
            task_ids = pattern.findall(message)
            for task_id in task_ids:
                task_progress[task_id] += 1

        # Normalize progress counts to a 0-100 scale
        if task_progress:
            max_count = max(task_progress.values())
            if max_count > 0:
                return {
                    task_id: (count / max_count) * 100
                    for task_id, count in task_progress.items()
                }
        
        return {}

    def calculate_workflow_progress(self) -> Dict[str, float]:
        """
        Calculate progress based on workflow steps completion.
        
        This method analyzes workflow definitions to determine task progress
        based on completed workflow steps.
        
        Returns:
            Dictionary mapping task IDs to workflow-based progress percentages
            
        Note:
            This is a placeholder implementation. In production, this should
            track actual completion of workflow steps per task.
        """
        workflow = self.load_workflow_definition()
        if not workflow:
            return {}

        # Placeholder implementation - returns empty progress
        # TODO: Implement actual workflow step tracking
        workflow_progress: Dict[str, float] = defaultdict(float)
        
        return dict(workflow_progress)

    def combine_progress(
        self, 
        commit_progress: Dict[str, float], 
        workflow_progress: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Combine commit-based and workflow-based progress using configured weights.
        
        Args:
            commit_progress: Progress from commit analysis
            workflow_progress: Progress from workflow analysis
            
        Returns:
            Combined progress dictionary with weighted values
            
        Example:
            >>> commit = {"1.2": 80.0}
            >>> workflow = {"1.2": 60.0}
            >>> combined = generator.combine_progress(commit, workflow)
            >>> print(combined)  # {"1.2": 72.0} (80*0.6 + 60*0.4)
        """
        combined_progress: Dict[str, float] = defaultdict(float)
        all_task_ids = set(commit_progress.keys()) | set(workflow_progress.keys())

        for task_id in all_task_ids:
            commit_val = commit_progress.get(task_id, 0.0)
            workflow_val = workflow_progress.get(task_id, 0.0)
            combined_progress[task_id] = (
                commit_val * self.commit_weight + 
                workflow_val * self.workflow_weight
            )

        return dict(combined_progress)

    def save_progress_to_json(self, progress_data: Dict[str, float]) -> None:
        """
        Save progress data to JSON file.
        
        Args:
            progress_data: Dictionary containing task progress data
            
        Raises:
            OSError: If directory creation or file writing fails
        """
        try:
            # Ensure directory exists
            dir_path = os.path.dirname(self.db_progress_json_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                
            with open(self.db_progress_json_path, 'w', encoding='utf-8') as f:
                json.dump(
                    progress_data, 
                    f, 
                    indent=2, 
                    ensure_ascii=False,
                    sort_keys=True
                )
            logger.info(
                f"Task progress data saved to {self.db_progress_json_path}"
            )
        except OSError as e:
            logger.error(f"Failed to create directory or save file: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to save progress data: {e}")
            raise

    def generate_progress(self) -> None:
        """
        Generate complete progress data by combining git and workflow analysis.
        
        This method orchestrates the entire progress generation process:
        1. Fetch git commit history
        2. Parse and analyze commits
        3. Calculate workflow-based progress
        4. Combine both progress sources
        5. Save results to JSON file
        """
        log_text = self.run_git_log()
        if not log_text:
            logger.warning("No git log data available.")
            return
            
        try:
            commits = self.parse_git_log(log_text)
            commit_progress = self.map_commits_to_tasks(commits)
            workflow_progress = self.calculate_workflow_progress()
            combined_progress = self.combine_progress(
                commit_progress, 
                workflow_progress
            )
            self.save_progress_to_json(combined_progress)
        except Exception as e:
            logger.error(f"Error during progress generation: {e}")
            raise


def generate_progress_data(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate progress data from input tasks and git history.
    
    This function serves as the main entry point for progress data generation.
    It validates input, generates progress from git history, and merges with
    provided task data.
    
    Args:
        input_data: Dictionary containing task information
        
    Returns:
        Dictionary mapping task IDs to progress status
        
    Raises:
        TypeError: If input data format is invalid
        RuntimeError: If progress data generation fails
        
    Example:
        >>> input_data = {"tasks": [{"id": "1.2", "status": "completed"}]}
        >>> progress = generate_progress_data(input_data)
        >>> print(progress)  # {"1.2": "completed"}
    """
    if not isinstance(input_data, dict):
        raise TypeError("Input data must be a dictionary.")
        
    tasks = input_data.get("tasks", [])
    if not isinstance(tasks, list):
        raise TypeError("Tasks must be a list.")

    # Instantiate ProgressDataGenerator and generate progress
    generator = ProgressDataGenerator()
    generator.generate_progress()
    
    # Load the generated progress data from JSON file
    try:
        with open(generator.db_progress_json_path, 'r', encoding='utf-8') as f:
            generated_progress = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load generated progress data: {e}")

    # Validate and process input tasks
    for task in tasks:
        if task is None:
            raise TypeError("Task cannot be None.")
        if not isinstance(task, dict):
            raise TypeError("Each task must be a dictionary.")
            
        task_id = task.get("id")
        if task_id is None:
            raise TypeError("Task must have an 'id' field.")
            
        status = task.get("status", "")
        if not isinstance(status, (str, type(None))):
            raise TypeError("Status must be a string or None.")
            
        # Normalize status to string
        status_str = str(status) if status is not None else ""
        
        # Override or add to generated progress
        generated_progress[str(task_id)] = status_str

    return generated_progress


if __name__ == "__main__":
    """Main entry point for direct script execution."""
    generator = ProgressDataGenerator()
    generator.generate_progress()
