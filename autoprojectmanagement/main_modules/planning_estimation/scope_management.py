"""
Scope Management Module for AutoProjectManagement System.

This module provides comprehensive scope management capabilities including:
- Loading and processing detailed WBS (Work Breakdown Structure) data
- Managing scope changes and their impact on project deliverables
- Tracking scope modifications with detailed audit trails
- Generating scope management reports and outputs

Author: AutoProjectManagement Team
Version: 2.0.0
"""

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
        
    def load_json(self, path: Path) -> Optional[Dict[str, Any]]:
        """
        Load JSON data from file with error handling.
        
        Args:
            path: Path to JSON file
            
        Returns:
            Dictionary containing JSON data or None if file doesn't exist
            
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
            logger.info(f"Data successfully saved to {path}")
        except Exception as e:
            logger.error(f"Error saving to {path}: {e}")
            raise ScopeManagementError(f"Cannot write file: {path}")
    
    def load_inputs(self) -> None:
        """Load and validate input files."""
        logger.info("Loading scope management inputs...")
        
        self.detailed_wbs = self.load_json(self.detailed_wbs_path) or {}
        self.scope_changes = self.load_json(self.scope_changes_path) or []
        
        if not self.detailed_wbs:
            logger.warning("No detailed WBS data found")
        
        if not isinstance(self.scope_changes, list):
            raise InvalidScopeChangeError("Scope changes must be a list")
    
    def validate_scope_change(self, change: Dict[str, Any]) -> bool:
        """
        Validate a scope change request.
        
        Args:
            change: Scope change dictionary
            
        Returns:
            True if valid, False otherwise
            
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
        
        Raises:
            InvalidScopeChangeError: If any scope change is invalid
        """
        logger.info("Applying scope changes...")
        
        # Reset scope status
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
        """
        Process a single validated scope change.
        
        Args:
            change: Validated scope change dictionary
        """
        task_id = change['task_id']
        change_type = change['change_type']
        details = change['details']
        
        if change_type == CHANGE_TYPE_ADD:
            self._I will proceed with implementing the improvements for all four phases of the code review checklist on the scope_management.py file. I will start with Phase 1 and Phase 2 improvements (structure, standards, and documentation) first, then move on to Phase 3 and Phase 4.

<edit_file>
<path>autoprojectmanagement/main_modules/planning_estimation/scope_management.py</path>
<content>
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import logging

# Constants for file paths
DETAILED_WBS_PATH = 'JSonDataBase/Inputs/UserInputs/detailed_wbs.json'
SCOPE_CHANGES_PATH = 'JSonDataBase/Inputs/UserInputs/scope_changes.json'
OUTPUT_PATH = 'JSonDataBase/OutPuts/scope_management.json'

class ScopeManagement:
    """
    Class to manage scope changes on a detailed Work Breakdown Structure (WBS).

    Attributes:
        detailed_wbs_path (str): Path to the detailed WBS JSON file.
        scope_changes_path (str): Path to the scope changes JSON file.
        output_path (str): Path to save the updated scope management JSON.
        detailed_wbs (Dict): Loaded detailed WBS data.
        scope_changes (List[Dict]): List of scope changes to apply.
        scope_status (Dict): Status of applied scope changes.
    """

    def __init__(self,
                 detailed_wbs_path: str = DETAILED_WBS_PATH,
                 scope_changes_path: str = SCOPE_CHANGES_PATH,
                 output_path: str = OUTPUT_PATH) -> None:
        self.detailed_wbs_path: str = detailed_wbs_path
        self.scope_changes_path: str = scope_changes_path
        self.output_path: str = output_path

        self.detailed_wbs: Dict[str, Any] = {}
        self.scope_changes: List[Dict[str, Any]] = []
        self.scope_status: Dict[str, List[Union[str, int]]] = {}

        # Configure logger
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def load_json(self, path: str) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """
        Load JSON data from a file.

        Args:
            path (str): Path to the JSON file.

        Returns:
            Optional[Union[Dict[str, Any], List[Any]]]: Parsed JSON data or None if file does not exist.
        """
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.logger.info(f"Loaded JSON data from {path}")
                return data
            except (json.JSONDecodeError, IOError) as e:
                self.logger.error(f"Error loading JSON from {path}: {e}")
                return None
        else:
            self.logger.warning(f"File not found: {path}")
            return None

    def save_json(self, data: Union[Dict[str, Any], List[Any]], path: str) -> None:
        """
        Save data as JSON to a file.

        Args:
            data (Union[Dict[str, Any], List[Any]]): Data to save.
            path (str): Path to the output JSON file.
        """
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved JSON data to {path}")
        except IOError as e:
            self.logger.error(f"Error saving JSON to {path}: {e}")

    def load_inputs(self) -> None:
        """
        Load detailed WBS and scope changes from their respective JSON files.
        """
        self.detailed_wbs = self.load_json(self.detailed_wbs_path) or {}
        self.scope_changes = self.load_json(self.scope_changes_path) or []

    def apply_scope_changes(self) -> None:
        """
        Apply scope changes to the detailed WBS.

        Scope changes are expected to be a list of dicts with:
        - task_id (str): Identifier of the task to change.
        - change_type (str): One of 'add', 'remove', 'modify'.
        - details (dict): Details of the change.

        Updates the scope_status dictionary with lists of added, removed, and modified task IDs.
        """
        self.scope_status = {
            'added_tasks': [],
            'removed_tasks': [],
            'modified_tasks': []
        }
        for change in self.scope_changes:
            task_id = change.get('task_id')
            change_type = change.get('change_type')
            details = change.get('details', {})
            if change_type == 'add':
                parent_id = details.get('parent_id')
                new_task = details.get('task')
                if parent_id and new_task:
                    parent_task = self.find_task_by_id(parent_id)
                    if parent_task is not None:
                        if 'subtasks' not in parent_task:
                            parent_task['subtasks'] = []
                        parent_task['subtasks'].append(new_task)
                        self.scope_status['added_tasks'].append(new_task.get('id'))
                        self.logger.info(f"Added task {new_task.get('id')} under parent {parent_id}")
                    else:
                        self.logger.warning(f"Parent task {parent_id} not found for adding new task")
                else:
                    self.logger.warning(f"Invalid add change details: {details}")
            elif change_type == 'remove':
                removed = self.remove_task_by_id(task_id)
                if removed:
                    self.scope_status['removed_tasks'].append(task_id)
                    self.logger.info(f"Removed task {task_id}")
                else:
                    self.logger.warning(f"Task {task_id} not found for removal")
            elif change_type == 'modify':
                task = self.find_task_by_id(task_id)
                if task:
                    for key, value in details.items():
                        task[key] = value
                    self.scope_status['modified_tasks'].append(task_id)
                    self.logger.info(f"Modified task {task_id} with details {details}")
                else:
                    self.logger.warning(f"Task {task_id} not found for modification")
            else:
                self.logger.warning(f"Unknown change_type '{change_type}' for task {task_id}")

    def find_task_by_id(self, task_id: Union[str, int], node: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Recursively find a task by its ID in the detailed WBS.

        Args:
            task_id (Union[str, int]): The ID of the task to find.
            node (Optional[Dict[str, Any]]): Current node in the WBS tree.

        Returns:
            Optional[Dict[str, Any]]: The task dict if found, else None.
        """
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
        """
        Recursively remove a task by its ID from the detailed WBS.

        Args:
            task_id (Union[str, int]): The ID of the task to remove.
            node (Optional[Dict[str, Any]]): Current node in the WBS tree.

        Returns:
            bool: True if the task was removed, False otherwise.
        """
        if node is None:
            node = self.detailed_wbs
        if not node or 'subtasks' not in node:
            return False
        for i, subtask in enumerate(node['subtasks']):
            if subtask.get('id') == task_id:
                del node['subtasks'][i]
                return True
            else:
                removed = self.remove_task_by_id(task_id, subtask)
                if removed:
                    return True
        return False

    def run(self) -> None:
        """
        Run the scope management process: load inputs, apply changes, and save output.
        """
        self.load_inputs()
        self.apply_scope_changes()
        self.save_json(self.detailed_wbs, self.output_path)
        self.logger.info(f"Scope management output saved to {self.output_path}")
        self.logger.info(f"Scope changes applied: {self.scope_status}")

if __name__ == "__main__":
    manager = ScopeManagement()
    manager.run()
