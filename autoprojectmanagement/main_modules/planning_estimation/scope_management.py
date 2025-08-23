#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/planning_estimation/scope_management_improved.py
File: scope_management_improved.py
Purpose: Enhanced scope management
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Enhanced scope management within the AutoProjectManagement system
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
Enhanced scope management within the AutoProjectManagement system

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
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_DETAILED_WBS_PATH = 'JSonDataBase/Inputs/UserInputs/detailed_wbs.json'
DEFAULT_SCOPE_CHANGES_PATH = 'JSonDataBase/Inputs/UserInputs/scope_changes.json'
DEFAULT_OUTPUT_PATH = 'JSonDataBase/OutPuts/scope_management.json'
ENCODING = 'utf-8'
JSON_INDENT = 2

# Scope change types
CHANGE_TYPE_ADD = 'add'
CHANGE_TYPE_REMOVE = 'remove'
CHANGE_TYPE_MODIFY = 'modify'
VALID_CHANGE_TYPES = {CHANGE_TYPE_ADD, CHANGE_TYPE_REMOVE, CHANGE_TYPE_MODIFY}


class ScopeManagementError(Exception):
    """Base exception for scope management errors."""
    pass


class InvalidScopeChangeError(ScopeManagementError):
    """Raised when an invalid scope change is detected."""
    pass


class FileNotFoundError(ScopeManagementError):
    """Raised when required files are not found."""
    pass


class ScopeManagement:
    """
    Comprehensive scope management system for project deliverables.
    
    This class handles the complete lifecycle of scope management including:
    - Loading and validating WBS data
    - Processing scope changes with impact analysis
    - Generating detailed scope management reports
    - Maintaining audit trails for all scope modifications
    
    Attributes:
        detailed_wbs_path: Path to detailed WBS JSON file
        scope_changes_path: Path to scope changes JSON file
        output_path: Path for scope management output
        detailed_wbs: Loaded WBS data structure
        scope_changes: List of scope change requests
        scope_status: Current status of scope changes
        
    Example:
        >>> manager = ScopeManagement()
        >>> manager.run()
        >>> print(manager.get_scope_summary())
    """
    
    def __init__(self,
                 detailed_wbs_path: str = DEFAULT_DETAILED_WBS_PATH,
                 scope_changes_path: str = DEFAULT_SCOPE_CHANGES_PATH,
                 output_path: str = DEFAULT_OUTPUT_PATH) -> None:
        """
        Initialize the ScopeManagement instance.
        
        Args:
            detailed_wbs_path: Path to detailed WBS JSON file
            scope_changes_path: Path to scope changes JSON file
            output_path: Path for scope management output
            
        Raises:
            ValueError: If any path is empty or invalid
        """
        if not all([detailed_wbs_path, scope_changes_path, output_path]):
            raise ValueError("All file paths must be provided")
            
        self.detailed_wbs_path = Path(detailed_wbs_path)
        self.scope_changes_path = Path(scope_changes_path)
        self.output_path = Path(output_path)
        
        self.detailed_wbs: Dict[str, Any] = {}
        self.scope_changes: List[Dict[str, Any]] = []
        self.scope_status: Dict[str, List[str]] = {
            'added_tasks': [],
            'removed_tasks': [],
            'modified_tasks': [],
            'errors': []
        }
    
    def load_json(self, path: Path) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """
        Load JSON data from file with error handling.
        
        Args:
            path: Path to JSON file
            
        Returns:
            Parsed JSON data or None if file doesn't exist
            
        Raises:
            FileNotFoundError: If file exists but cannot be read
            json.JSONDecodeError: If file contains invalid JSON
        """
        try:
            if path.exists():
                with open(path, 'r', encoding=ENCODING) as f:
                    return json.load(f)
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {path}: {e}")
            raise ScopeManagementError(f"Invalid JSON format in {path}")
        except Exception as e:
            logger.error(f"Error reading {path}: {e}")
            raise FileNotFoundError(f"Cannot read file: {path}")
    
    def save_json(self, data: Union[Dict[str, Any], List[Any]], path: Path) -> None:
        """
        Save data to JSON file with proper formatting.
        
        Args:
            data: Data to save (dict or list)
            path: Output file path
            
        Raises:
            ScopeManagementError: If file cannot be written
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding=ENCODING) as f:
                json.dump(data, f, indent=JSON_INDENT, ensure_ascii=False)
            logger.info(f"Saved JSON data to {path}")
        except Exception as e:
            logger.error(f"Error saving JSON to {path}: {e}")
            raise ScopeManagementError(f"Cannot write file: {path}")
    
    def load_inputs(self) -> None:
        """Load and validate input files."""
        logger.info("Loading scope management inputs...")
        
        self.detailed_wbs = self.load_json(self.detailed_wbs_path) or {}
        self.scope_changes = self.load_json(self.scope_changes_path) or []
        
        if not isinstance(self.scope_changes, list):
            raise InvalidScopeChangeError("Scope changes must be a list")
    
    def validate_scope_change(self, change: Dict[str, Any]) -> bool:
        """
        Validate a scope change request.
        
        Args:
            change: Scope change dictionary
            
        Returns:
            True if valid
            
        Raises:
            InvalidScopeChangeError: If change is invalid
        """
        required_keys = {'task_id', 'change_type', 'details'}
        if not all(key in change for key in required_keys):
            raise InvalidScopeChangeError(
                f"Missing required keys: {required_keys - set(change.keys())}"
            )
        
        change_type = change.get('change_type')
        if change_type not in VALID_CHANGE_TYPES:
            raise InvalidScopeChangeError(
                f"Invalid change type: {change_type}. Must be one of {VALID_CHANGE_TYPES}"
            )
        
        return True
    
    def apply_scope_changes(self) -> None:
        """
        Apply validated scope changes to the detailed WBS.
        
        This method processes all scope changes and applies them to the WBS
        structure while maintaining data integrity and generating audit trails.
        """
        logger.info("Applying scope changes...")
        
        self.scope_status = {
            'added_tasks': [],
            'removed_tasks': [],
            'modified_tasks': [],
            'errors': []
        }
        
        for change in self.scope_changes:
            try:
                self.validate_scope_change(change)
                self._process_single_change(change)
            except Exception as e:
                error_msg = f"Error processing change {change}: {e}"
                logger.error(error_msg)
                self.scope_status['errors'].append(error_msg)
    
    def _process_single_change(self, change: Dict[str, Any]) -> None:
        """Process a single validated scope change."""
        task_id = change['task_id']
        change_type = change['change_type']
        details = change['details']
        
        if change_type == CHANGE_TYPE_ADD:
            self._process_add_change(task_id, details)
        elif change_type == CHANGE_TYPE_REMOVE:
            self._process_remove_change(task_id)
        elif change_type == CHANGE_TYPE_MODIFY:
            self._process_modify_change(task_id, details)
    
    def _process_add_change(self, task_id: str, details: Dict[str, Any]) -> None:
        """Process an 'add' type scope change."""
        parent_id = details.get('parent_id')
        new_task = details.get('task')
        
        if parent_id and new_task:
            parent_task = self.find_task_by_id(parent_id)
            if parent_task is not None:
                if 'subtasks' not in parent_task:
                    parent_task['subtasks'] = []
                parent_task['subtasks'].append(new_task)
                self.scope_status['added_tasks'].append(new_task.get('id', ''))
                logger.info(f"Added task {new_task.get('id')} under parent {parent_id}")
    
    def _process_remove_change(self, task_id: str) -> None:
        """Process a 'remove' type scope change."""
        removed = self.remove_task_by_id(task_id)
        if removed:
            self.scope_status['removed_tasks'].append(task_id)
            logger.info(f"Removed task {task_id}")
    
    def _process_modify_change(self, task_id: str, details: Dict[str, Any]) -> None:
        """Process a 'modify' type scope change."""
        task = self.find_task_by_id(task_id)
        if task:
            task.update(details)
            self.scope_status['modified_tasks'].append(task_id)
            logger.info(f"Modified task {task_id}")
    
    def find_task_by_id(self, task_id: Union[str, int], node: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Recursively find a task by its ID."""
        if node is None:
            node = self.detailed_wbs
        if not node:
            return None
        if node.get('id') == task_id:
            return node
        for subtask in node.get('subtasks', []):
            found = self.find_task_by_id(task_id, subtask)
            if found:
                return found
        return None
    
    def remove_task_by_id(self, task_id: Union[str, int], node: Optional[Dict[str, Any]] = None) -> bool:
        """Recursively remove a task by its ID."""
        if node is None:
            node = self.detailed_wbs
        if not node or 'subtasks' not in node:
            return False
        for i, subtask in enumerate(node['subtasks']):
            if subtask.get('id') == task_id:
                del node['subtasks'][i]
                return True
            if self.remove_task_by_id(task_id, subtask):
                return True
        return False
    
    def get_scope_summary(self) -> Dict[str, Any]:
        """Get a summary of the current scope management status."""
        return {
            'total_tasks_added': len(self.scope_status['added_tasks']),
            'total_tasks_removed': len(self.scope_status['removed_tasks']),
            'total_tasks_modified': len(self.scope_status['modified_tasks']),
            'total_errors': len(self.scope_status['errors']),
            'added_tasks': self.scope_status['added_tasks'],
            'removed_tasks': self.scope_status['removed_tasks'],
            'modified_tasks': self.scope_status['modified_tasks'],
            'errors': self.scope_status['errors']
        }
    
    def run(self) -> None:
        """Run the complete scope management process."""
        logger.info("Starting scope management process...")
        self.load_inputs()
        self.apply_scope_changes()
        self.save_json(self.detailed_wbs, self.output_path)
        
        summary = self.get_scope_summary()
        logger.info(f"Scope management completed: {summary}")
        print(f"Scope management output saved to {self.output_path}")
        print(f"Summary: {summary}")

if __name__ == "__main__":
    manager = ScopeManagement()
    manager.run()
