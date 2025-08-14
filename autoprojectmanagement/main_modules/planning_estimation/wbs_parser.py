#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: wbs_parser
File: wbs_parser.py
Path: autoprojectmanagement/main_modules/planning_estimation/wbs_parser.py

Description:
    Wbs Parser module

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
    >>> from autoprojectmanagement.main_modules.planning_estimation.wbs_parser import {main_class}
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
import re
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import os
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

# Constants
DEFAULT_INDENT_SIZE = 2
MAX_LINE_LENGTH = 79
DEFAULT_ROOT_NAME = "Project"
DEFAULT_ROOT_ID = 1
DEFAULT_ROOT_LEVEL = 0

# Task status constants
class TaskStatus(Enum):
    """Enumeration for task status values"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

# Priority levels
class TaskPriority(Enum):
    """Enumeration for task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# Required fields for WBS validation
REQUIRED_WBS_FIELDS = ['id', 'name', 'level']
REQUIRED_TASK_FIELDS = ['id', 'name', 'level']

@dataclass
class Task:
    """Represents a single task in the WBS structure"""
    id: int
    name: str
    level: int
    description: str = ""
    deadline: Optional[str] = None
    assigned_to: List[str] = None
    dependencies: List[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    subtasks: List['Task'] = None
    
    def __post_init__(self):
        """Initialize default values for optional fields"""
        if self.assigned_to is None:
            self.assigned_to = []
        if self.dependencies is None:
            self.dependencies = []
        if self.subtasks is None:
            self.subtasks = []

@dataclass
class WBSProject:
    """Represents the complete WBS project structure"""
    id: int
    name: str
    level: int = 0
    description: str = ""
    tasks: List[Task] = None
    
    def __post_init__(self):
        """Initialize default values for optional fields"""
        if self.tasks is None:
            self.tasks = []

class WBSValidationError(Exception):
    """Custom exception for WBS validation errors"""
    pass

class WBSFormatError(Exception):
    """Custom exception for WBS format errors"""
    pass

class WBSParser:
    """
    Comprehensive WBS (Work Breakdown Structure) parser supporting multiple formats
    
    This parser handles various WBS formats including JSON, text, and other
    structured formats. It provides validation, normalization, and detailed
    information extraction capabilities.
    
    Features:
        - JSON format parsing
        - Text format parsing with indentation detection
        - Comprehensive validation
        - Detailed task information extraction
        - Hierarchy flattening
        - Format conversion utilities
    
    Example:
        >>> parser = WBSParser()
        >>> wbs_json = {"id": 1, "name": "Project", "level": 0, "subtasks": []}
        >>> parsed = parser.parse_json_wbs(wbs_json)
        >>> print(f"Project: {parsed['name']}")
    """
    
    def __init__(self, indent_size: int = DEFAULT_INDENT_SIZE):
        """
        Initialize WBS Parser
        
        Args:
            indent_size: Number of spaces per indentation level (default: 2)
        """
        self.indent_size = indent_size
        logger.info(f"Initialized WBSParser with indent_size={indent_size}")
    
    def parse_json_wbs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse JSON format WBS data
        
        Args:
            data: JSON data containing WBS structure
            
        Returns:
            Parsed and validated WBS structure
            
        Raises:
            WBSValidationError: If the WBS structure is invalid
            
        Example:
            >>> parser = WBSParser()
            >>> data = {"id": 1, "name": "Project", "level": 0, "subtasks": []}
            >>> result = parser.parse_json_wbs(data)
            >>> assert result["name"] == "Project"
        """
        if not isinstance(data, dict):
            raise WBSValidationError("WBS data must be a dictionary")
        
        logger.debug("Parsing JSON WBS data")
        return self._validate_wbs_structure(data)
    
    def parse_text_wbs(self, text: str) -> Dict[str, Any]:
        """
        Parse text format WBS with indentation-based hierarchy
        
        Args:
            text: Text containing WBS structure with indentation
            
        Returns:
            Parsed WBS structure
            
        Example:
            >>> parser = WBSParser()
            >>> text = '''
            ... Project
            ...   Phase 1
            ...     Task 1.1
            ...   Phase 2
            ...     Task 2.1
            ... '''
            >>> result = parser.parse_text_wbs(text)
            >>> assert result["name"] == "Project"
        """
        if not isinstance(text, str):
            raise WBSFormatError("Text WBS must be a string")
        
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        logger.debug(f"Parsing text WBS with {len(lines)} lines")
        return self._parse_text_lines(lines)
    
    def parse_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Parse WBS from file
        
        Args:
            file_path: Path to the WBS file
            
        Returns:
            Parsed WBS structure
            
        Raises:
            WBSFormatError: If the file format is not supported
            
        Example:
            >>> parser = WBSParser()
            >>> wbs_data = parser.parse_file("project_wbs.json")
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise WBSFormatError(f"File not found: {file_path}")
        
        try:
            if file_path.suffix.lower() == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return self.parse_json_wbs(data)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                return self.parse_text_wbs(text)
        except json.JSONDecodeError as e:
            raise WBSFormatError(f"Invalid JSON format: {e}")
        except Exception as e:
            raise WBSFormatError(f"Error reading file: {e}")
    
    def _validate_wbs_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize WBS structure
        
        Args:
            data: WBS data to validate
            
        Returns:
            Validated and normalized WBS structure
            
        Raises:
            WBSValidationError: If validation fails
        """
        if not isinstance(data, dict):
            raise WBSValidationError("WBS data must be a dictionary")
        
        # Check required fields
        for field in REQUIRED_WBS_FIELDS:
            if field not in data:
                raise WBSValidationError(f"Missing required field: {field}")
        
        # Ensure subtasks is a list
        if 'subtasks' not in data:
            data['subtasks'] = []
        elif not isinstance(data['subtasks'], list):
            raise WBSValidationError("subtasks must be a list")
        
        # Validate ID is positive integer
        if not isinstance(data['id'], int) or data['id'] <= 0:
            raise WBSValidationError("Task ID must be a positive integer")
        
        # Validate name is non-empty string
        if not isinstance(data['name'], str) or not data['name'].strip():
            raise WBSValidationError("Task name must be a non-empty string")
        
        # Validate level is non-negative integer
        if not isinstance(data['level'], int) or data['level'] < 0:
            raise WBSValidationError("Task level must be a non-negative integer")
        
        # Recursively validate subtasks
        for subtask in data['subtasks']:
            self._validate_wbs_structure(subtask)
        
        logger.debug(f"Validated WBS structure with {len(data['subtasks'])} subtasks")
        return data
    
    def _parse_text_lines(self, lines: List[str]) -> Dict[str, Any]:
        """
        Parse text lines into WBS structure using indentation
        
        Args:
            lines: List of text lines with indentation
            
        Returns:
            Parsed WBS structure
            
        Note:
            Indentation is detected automatically based on the minimum
            indentation found in the lines
        """
        if not lines:
            return {
                "id": DEFAULT_ROOT_ID,
                "name": DEFAULT_ROOT_NAME,
                "level": DEFAULT_ROOT_LEVEL,
                "subtasks": []
            }
        
        # Calculate indentation levels
        indent_levels = []
        for line in lines:
            if line.strip():  # Skip empty lines
                indent = len(line) - len(line.lstrip())
                indent_levels.append(indent)
        
        if not indent_levels:
            return {
                "id": DEFAULT_ROOT_ID,
                "name": lines[0] if lines else DEFAULT_ROOT_NAME,
                "level": DEFAULT_ROOT_LEVEL,
                "subtasks": []
            }
        
        # Determine minimum indentation
        min_indent = min(indent_levels)
        adjusted_indent = max(self.indent_size, min_indent)
        
        root = {
            "id": DEFAULT_ROOT_ID,
            "name": lines[0].strip(),
            "level": DEFAULT_ROOT_LEVEL,
            "subtasks": []
        }
        
        stack = [(root, 0)]  # (task, level)
        
        for line in lines[1:]:
            line = line.rstrip()
            if not line.strip():
                continue
            
            # Calculate level based on indentation
            indent = len(line) - len(line.lstrip())
            level = max(0, (indent - min_indent) // adjusted_indent)
            
            name = line.strip()
            if not name:
                continue
            
            # Create task
            task = {
                "id": len([t for t, _ in stack]) + 1,
                "name": name,
                "level": level,
                "subtasks": []
            }
            
            # Find parent
            while stack and stack[-1][1] >= level:
                stack.pop()
            
            if stack:
                parent = stack[-1][0]
                parent["subtasks"].append(task)
            else:
                root["subtasks"].append(task)
            
            stack.append((task, level))
        
        return root
    
    def extract_task_details(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract detailed information from a task
        
        Args:
            task: Task dictionary
            
        Returns:
            Detailed task information with normalized fields
            
        Example:
            >>> parser = WBSParser()
            >>> task = {"id": 1, "name": "Task 1", "level": 0}
            >>> details = parser.extract_task_details(task)
            >>> assert details["name"] == "Task 1"
        """
        if not isinstance(task, dict):
            raise WBSValidationError("Task must be a dictionary")
        
        return {
            "id": task.get("id"),
            "name": task.get("name", ""),
            "level": task.get("level", 0),
            "description": task.get("description", ""),
            "deadline": task.get("deadline"),
            "assigned_to": task.get("assigned_to", []),
            "dependencies": task.get("dependencies", []),
            "status": task.get("status", TaskStatus.PENDING.value),
            "priority": task.get("priority", TaskPriority.MEDIUM.value),
            "subtasks_count": len(task.get("subtasks", [])),
            "estimated_hours": task.get("estimated_hours", 0),
            "actual_hours": task.get("actual_hours", 0),
            "completion_percentage": task.get("completion_percentage", 0)
        }
    
    def validate_wbs_integrity(self, wbs: Dict[str, Any]) -> bool:
        """
        Validate WBS structure integrity
        
        Args:
            wbs: WBS structure to validate
            
        Returns:
            True if valid, False otherwise
            
        Example:
            >>> parser = WBSParser()
            >>> wbs = {"id": 1, "name": "Project", "level": 0, "subtasks": []}
            >>> assert parser.validate_wbs_integrity(wbs) is True
        """
        try:
            self._validate_wbs_structure(wbs)
            logger.debug("WBS integrity validation passed")
            return True
        except WBSValidationError as e:
            logger.warning(f"WBS integrity validation failed: {e}")
            return False
    
    def get_task_hierarchy(self, wbs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get flat list of all tasks in hierarchy
        
        Args:
            wbs: WBS structure
            
        Returns:
            Flat list of all tasks with hierarchy information
            
        Example:
            >>> parser = WBSParser()
            >>> wbs = {"id": 1, "name": "Project", "subtasks": [
            ...     {"id": 2, "name": "Phase 1", "subtasks": []}
            ... ]}
            >>> tasks = parser.get_task_hierarchy(wbs)
            >>> assert len(tasks) == 2
        """
        if not isinstance(wbs, dict):
            raise WBSValidationError("WBS must be a dictionary")
        
        tasks = []
        
        def collect_tasks(task: Dict[str, Any], level: int = 0, 
                         parent_path: str = "") -> None:
            """Recursively collect all tasks in hierarchy"""
            task_info = self.extract_task_details(task)
            task_info['level'] = level
            
            # Build hierarchical path
            current_path = f"{parent_path}/{task['name']}" if parent_path else task['name']
            task_info['path'] = current_path
            
            tasks.append(task_info)
            
            # Process subtasks
            for subtask in task.get('subtasks', []):
                collect_tasks(subtask, level + 1, current_path)
        
        collect_tasks(wbs)
        logger.debug(f"Extracted {len(tasks)} tasks from hierarchy")
        return tasks
    
    def convert_to_json(self, wbs: Dict[str, Any], indent: int = 2) -> str:
        """
        Convert WBS structure to JSON string
        
        Args:
            wbs: WBS structure to convert
            indent: JSON indentation level
            
        Returns:
            JSON string representation of WBS
            
        Example:
            >>> parser = WBSParser()
            >>> wbs = {"id": 1, "name": "Project", "subtasks": []}
            >>> json_str = parser.convert_to_json(wbs)
            >>> assert "Project" in json_str
        """
        if not isinstance(wbs, dict):
            raise WBSValidationError("WBS must be a dictionary")
        
        return json.dumps(wbs, indent=indent, ensure_ascii=False)
    
    def get_statistics(self, wbs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the WBS
        
        Args:
            wbs: WBS structure
            
        Returns:
            Dictionary with WBS statistics
            
        Example:
            >>> parser = WBSParser()
            >>> wbs = {"id": 1, "name": "Project", "subtasks": [
            ...     {"id": 2, "name": "Task 1", "subtasks": []}
            ... ]}
            >>> stats = parser.get_statistics(wbs)
            >>> assert stats["total_tasks"] == 2
        """
        if not isinstance(wbs, dict):
            raise WBSValidationError("WBS must be a dictionary")
        
        tasks = self.get_task_hierarchy(wbs)
        
        stats = {
            "total_tasks": len(tasks),
            "max_depth": max([t['level'] for t in tasks]) if tasks else 0,
            "tasks_by_level": {},
            "tasks_without_subtasks": 0,
            "tasks_with_subtasks": 0
        }
        
        # Count tasks by level
        for task in tasks:
            level = task['level']
            stats['tasks_by_level'][level] = stats['tasks_by_level'].get(level, 0) + 1
            
            if task['subtasks_count'] == 0:
                stats['tasks_without_subtasks'] += 1
            else:
                stats['tasks_with_subtasks'] += 1
        
        return stats
    
    def merge_wbs_structures(self, *wbs_list: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge multiple WBS structures into one
        
        Args:
            *wbs_list: Variable number of WBS structures to merge
            
        Returns:
            Merged WBS structure
            
        Example:
            >>> parser = WBSParser()
            >>> wbs1 = {"id": 1, "name": "Project A", "subtasks": []}
            >>> wbs2 = {"id": 2, "name": "Project B", "subtasks": []}
            >>> merged = parser.merge_wbs_structures(wbs1, wbs2)
            >>> assert "merged" in merged["name"]
        """
        if not wbs_list:
            raise WBSValidationError("At least one WBS structure is required")
        
        merged = {
            "id": DEFAULT_ROOT_ID,
            "name": "Merged Project",
            "level": DEFAULT_ROOT_LEVEL,
            "subtasks": []
        }
        
        for i, wbs in enumerate(wbs_list):
            if not isinstance(wbs, dict):
                raise WBSValidationError(f"WBS {i+1} must be a dictionary")
            
            # Create a copy to avoid modifying original
            wbs_copy = dict(wbs)
            wbs_copy["id"] = i + 1
            merged["subtasks"].append(wbs_copy)
        
        logger.info(f"Merged {len(wbs_list)} WBS structures")
        return merged

# Utility functions for backward compatibility
def create_parser(indent_size: int = DEFAULT_INDENT_SIZE) -> WBSParser:
    """
    Create a new WBS parser instance
    
    Args:
        indent_size: Number of spaces per indentation level
        
    Returns:
        Configured WBSParser instance
    """
    return WBSParser(indent_size=indent_size)

def quick_parse(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Quick parse function for simple use cases
    
    Args:
        data: WBS data to parse
        
    Returns:
        Parsed WBS structure
    """
    parser = WBSParser()
    return parser.parse_json_wbs(data)

# Export public API
__all__ = [
    'WBSParser',
    'WBSValidationError',
    'WBSFormatError',
    'TaskStatus',
    'TaskPriority',
    'create_parser',
    'quick_parse'
]
