#!/usr/bin/env python3
"""
Workflow Data Collector Module for AutoProjectManagement System.

This module provides comprehensive data collection and management capabilities
for Scrum workflow tracking, including sprint management, task tracking,
and burndown chart generation.

Author: AutoProjectManagement Team
Version: 2.0.0
"""

import json
import os
import logging
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Enumeration for task status values."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    """Enumeration for task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class ScrumTask:
    """Data class representing a Scrum task."""
    task_id: str
    sprint_id: str
    title: str
    status: TaskStatus
    priority: TaskPriority
    progress: int
    description: Optional[str] = None
    assignee: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()


@dataclass
class Sprint:
    """Data class representing a Scrum sprint."""
    sprint_id: str
    name: str
    start_date: str
    end_date: str
    goal: Optional[str] = None
    status: str = "active"


@dataclass
class BurndownEntry:
    """Data class representing a burndown chart entry."""
    sprint_id: str
    day: int
    remaining_work: float
    date: str
    ideal_remaining: Optional[float] = None


class WorkflowDataCollector:
    """
    Comprehensive workflow data collector for Scrum project management.
    
    This class provides methods to collect, manage, and analyze Scrum workflow data
    including sprints, tasks, and burndown charts. It handles JSON file persistence
    and provides APIs for data manipulation and reporting.
    """
    
    # Constants
    DEFAULT_DATA_DIR = 'SystemInputs/user_inputs'
    DEFAULT_ENCODING = 'utf-8'
    DEFAULT_INDENT = 4
    
    def __init__(self, data_dir: Optional[str] = None) -> None:
        """Initialize the WorkflowDataCollector."""
        self.data_dir = Path(data_dir or self.DEFAULT_DATA_DIR)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Define file paths
        self.scrum_sprints_file = self.data_dir / 'scrum_sprints.json'
        self.scrum_tasks_file = self.data_dir / 'scrum_tasks.json'
        self.scrum_burndown_file = self.data_dir / 'scrum_burndown.json'
        
        # Initialize files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self) -> None:
        """Initialize JSON files with empty arrays if they don't exist."""
        files_to_init = [
            self.scrum_sprints_file,
            self.scrum_tasks_file,
            self.scrum_burndown_file
        ]
        
        for file_path in files_to_init:
            if not file_path.exists():
                with open(file_path, 'w', encoding=self.DEFAULT_ENCODING) as f:
                    json.dump([], f, indent=self.DEFAULT_INDENT)
    
    def create_scrum_workflow_tables(self) -> None:
        """Create and initialize Scrum workflow tables (JSON files)."""
        self._initialize_files()
        logger.info("Scrum workflow tables created successfully")
    
    def update_scrum_task(self, task: ScrumTask) -> bool:
        """Update or create a Scrum task in the workflow."""
        try:
            tasks_data = json.load(open(self.scrum_tasks_file, 'r', encoding=self.DEFAULT_ENCODING))
            
            # Remove existing task with same task_id
            tasks_data = [t for t in tasks_data if t.get('task_id') != task.task_id]
            
            # Add updated task
            task_dict = asdict(task)
            task_dict['status'] = task.status.value
            task_dict['priority'] = task.priority.value
            tasks_data.append(task_dict)
            
            with open(self.scrum_tasks_file, 'w', encoding=self.DEFAULT_ENCODING) as f:
                json.dump(tasks_data, f, indent=self.DEFAULT_INDENT)
            return True
            
        except Exception as e:
            logger.error(f"Failed to update task: {e}")
            return False
    
    def update_scrum_burndown(self, entry: BurndownEntry) -> bool:
        """Update or create a burndown chart entry."""
        try:
            burndown_data = json.load(open(self.scrum_burndown_file, 'r', encoding=self.DEFAULT_ENCODING))
            
            # Remove existing entry
            burndown_data = [
                b for b in burndown_data 
                if not (b.get('sprint_id') == entry.sprint_id and b.get('day') == entry.day)
            ]
            
            # Add updated entry
            entry_dict = asdict(entry)
            burndown_data.append(entry_dict)
            
            with open(self.scrum_burndown_file, 'w', encoding=self.DEFAULT_ENCODING) as f:
                json.dump(burndown_data, f, indent=self.DEFAULT_INDENT)
            return True
            
        except Exception as e:
            logger.error(f"Failed to update burndown: {e}")
            return False
    
    def generate_scrum_report(self, sprint_id: str) -> List[Tuple[int, float]]:
        """Generate a sorted Scrum burndown report for a given sprint."""
        try:
            burndown_data = json.load(open(self.scrum_burndown_file, 'r', encoding=self.DEFAULT_ENCODING))
            
            report = [
                (entry['day'], entry['remaining_work'])
                for entry in burndown_data
                if entry.get('sprint_id') == sprint_id
            ]
            
            return sorted(report, key=lambda x: x[0])
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return []
    
    def get_sprint_tasks(self, sprint_id: str) -> List[Dict[str, Any]]:
        """Get all tasks for a specific sprint."""
        try:
            tasks_data = json.load(open(self.scrum_tasks_file, 'r', encoding=self.DEFAULT_ENCODING))
            return [t for t in tasks_data if t.get('sprint_id') == sprint_id]
        except Exception as e:
            logger.error(f"Failed to get sprint tasks: {e}")
            return []
    
    def close(self) -> None:
        """Cleanup method for any resources that need explicit cleanup."""
        logger.info("WorkflowDataCollector closed")
