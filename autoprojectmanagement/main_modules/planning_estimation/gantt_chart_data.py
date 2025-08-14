#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/planning_estimation/gantt_chart_data.py
File: gantt_chart_data.py
Purpose: Gantt chart data generation
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Gantt chart data generation within the AutoProjectManagement system
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
Gantt chart data generation within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import json
import logging
from datetime import date, timedelta, datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple

# Configure logging
logger = logging.getLogger(__name__)

# Constants
DEFAULT_INPUT_DIR: str = 'project_inputs/PM_JSON/user_inputs'
DEFAULT_OUTPUT_PATH: str = 'SystemInputs/system_generated/gantt_chart_data.json'
DEFAULT_DURATION_DAYS: int = 1
MAX_PROGRESS: int = 100
MIN_PROGRESS: int = 0
DATE_FORMAT: str = '%Y-%m-%d'

# Type aliases
TaskDict = Dict[str, Any]
GanttTask = Dict[str, Any]
TaskList = List[TaskDict]


class GanttChartData:
    """
    A class to generate Gantt chart data from project tasks.
    
    This class loads project tasks from JSON files and transforms them into
    a format suitable for Gantt chart visualization, including task dependencies,
    durations, and progress tracking.
    
    Attributes:
        input_dir (str): Directory containing input JSON files
        tasks (TaskList): List of loaded project tasks
    """
    
    def __init__(self, input_dir: str = DEFAULT_INPUT_DIR) -> None:
        """
        Initialize the GanttChartData generator.
        
        Args:
            input_dir: Directory path containing input JSON files
        """
        self.input_dir: str = input_dir
        self.tasks: TaskList = []
        self.logger = logging.getLogger(__name__)

    def load_tasks(self) -> None:
        """
        Load project tasks from the detailed WBS JSON file.
        
        Raises:
            FileNotFoundError: If the WBS file doesn't exist
            json.JSONDecodeError: If the JSON file is malformed
        """
        wbs_path = Path(self.input_dir) / 'detailed_wbs.json'
        
        try:
            with open(wbs_path, 'r', encoding='utf-8') as file:
                self.tasks = json.load(file)
            self.logger.info(f"Successfully loaded {len(self.tasks)} tasks from {wbs_path}")
        except FileNotFoundError:
            self.logger.error(f"WBS file not found: {wbs_path}")
            self.tasks = []
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON format in {wbs_path}: {e}")
            self.tasks = []
            raise
        except Exception as e:
            self.logger.error(f"Error loading tasks: {e}")
            self.tasks = []
            raise

    def parse_date(self, date_str: Optional[str]) -> Optional[date]:
        """
        Parse a date string into a date object.
        
        Args:
            date_str: ISO format date string (YYYY-MM-DD)
            
        Returns:
            Parsed date object or None if date_str is empty/invalid
            
        Examples:
            >>> parse_date("2024-12-25")
            datetime.date(2024, 12, 25)
            >>> parse_date(None)
            None
            >>> parse_date("invalid")
            None
        """
        if not date_str:
            return None
            
        try:
            return datetime.strptime(date_str, DATE_FORMAT).date()
        except ValueError:
            self.logger.warning(f"Invalid date format: {date_str}")
            return None

    def calculate_end_date(self, start_date: date, duration_days: int) -> date:
        """
        Calculate the end date based on start date and duration.
        
        Args:
            start_date: The start date of the task
            duration_days: Number of days the task will take
            
        Returns:
            The calculated end date
            
        Raises:
            ValueError: If duration_days is negative
        """
        if duration_days < 0:
            raise ValueError("Duration cannot be negative")
            
        return start_date + timedelta(days=duration_days)

    def validate_task_data(self, task: TaskDict) -> Tuple[bool, str]:
        """
        Validate task data for Gantt chart generation.
        
        Args:
            task: Task dictionary to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ['id', 'name']
        
        for field in required_fields:
            if field not in task:
                return False, f"Missing required field: {field}"
                
        task_id = task.get('id')
        if not isinstance(task_id, (str, int)):
            return False, "Task ID must be a string or integer"
            
        name = task.get('name')
        if not isinstance(name, str) or not name.strip():
            return False, "Task name must be a non-empty string"
            
        progress = task.get('progress', 0)
        if not isinstance(progress, (int, float)):
            return False, "Progress must be a number"
        if not MIN_PROGRESS <= progress <= MAX_PROGRESS:
            return False, f"Progress must be between {MIN_PROGRESS} and {MAX_PROGRESS}"
            
        return True, ""

    def build_gantt_data(self) -> List[GanttTask]:
        """
        Build Gantt chart data from loaded tasks.
        
        This method processes all loaded tasks and their subtasks to create
        a standardized format for Gantt chart visualization.
        
        Returns:
            List of Gantt chart task dictionaries with the following structure:
            {
                'id': str|int,
                'name': str,
                'start_date': str (ISO format),
                'end_date': str (ISO format),
                'dependencies': List[str|int],
                'progress': int (0-100)
            }
            
        Raises:
            ValueError: If task data is invalid
        """
        gantt_data: List[GanttTask] = []
        
        def process_task(task: TaskDict, parent_start: Optional[date] = None) -> None:
            """Process a single task and its subtasks recursively."""
            is_valid, error_msg = self.validate_task_data(task)
            if not is_valid:
                self.logger.warning(f"Skipping invalid task {task.get('id', 'unknown')}: {error_msg}")
                return
                
            task_id = task['id']
            name = task.get('name', task.get('title', f"Task {task_id}"))
            start_date_str = task.get('start_date')
            duration_days = task.get('duration_days', task.get('duration', DEFAULT_DURATION_DAYS))
            dependencies = task.get('dependencies', [])
            
            # Parse start date
            start_date = self.parse_date(start_date_str) or parent_start or date.today()
            
            # Calculate end date
            try:
                end_date = self.calculate_end_date(start_date, duration_days)
            except ValueError as e:
                self.logger.error(f"Invalid duration for task {task_id}: {e}")
                return
                
            # Handle progress
            progress = task.get('progress', 0)
            if isinstance(progress, float):
                progress = int(progress * MAX_PROGRESS)
            progress = max(MIN_PROGRESS, min(MAX_PROGRESS, int(progress)))
            
            gantt_data.append({
                'id': task_id,
                'name': name,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'dependencies': dependencies,
                'progress': progress,
            })
            
            # Process subtasks
            for subtask in task.get('subtasks', []):
                process_task(subtask, start_date)

        for task in self.tasks:
            process_task(task)
            
        self.logger.info(f"Generated Gantt chart data for {len(gantt_data)} tasks")
        return gantt_data

    def save_gantt_data(self, output_path: str = DEFAULT_OUTPUT_PATH) -> None:
        """
        Save the generated Gantt chart data to a JSON file.
        
        Args:
            output_path: Path where the Gantt chart data should be saved
            
        Raises:
            IOError: If unable to write to the output file
        """
        gantt_data = self.build_gantt_data()
        output_file = Path(output_path)
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(gantt_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Gantt chart data saved to {output_file}")
        except IOError as e:
            self.logger.error(f"Failed to save Gantt chart data: {e}")
            raise

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the loaded tasks and generated data.
        
        Returns:
            Dictionary containing summary statistics
        """
        if not self.tasks:
            return {
                'total_tasks': 0,
                'total_subtasks': 0,
                'date_range': None,
                'completion_rate': 0
            }
            
        gantt_data = self.build_gantt_data()
        
        if not gantt_data:
            return {
                'total_tasks': len(self.tasks),
                'total_subtasks': 0,
                'date_range': None,
                'completion_rate': 0
            }
            
        start_dates = [datetime.fromisoformat(task['start_date']) for task in gantt_data]
        end_dates = [datetime.fromisoformat(task['end_date']) for task in gantt_data]
        
        min_date = min(start_dates).date()
        max_date = max(end_dates).date()
        
        total_progress = sum(task['progress'] for task in gantt_data)
        avg_progress = total_progress / len(gantt_data) if gantt_data else 0
        
        return {
            'total_tasks': len(gantt_data),
            'total_subtasks': len(gantt_data) - len(self.tasks),
            'date_range': {
                'start': min_date.isoformat(),
                'end': max_date.isoformat()
            },
            'completion_rate': round(avg_progress, 2)
        }


def generate_gantt_chart(tasks: TaskList) -> Dict[str, List[GanttTask]]:
    """
    Generate Gantt chart data from a list of tasks.
    
    This is a convenience function that creates a GanttChartData instance
    and processes the tasks in one call.
    
    Args:
        tasks: List of task dictionaries
        
    Returns:
        Dictionary containing the processed Gantt chart tasks
        
    Raises:
        TypeError: If tasks is not a list
        ValueError: If task data is invalid
        
    Examples:
        >>> tasks = [
        ...     {
        ...         'id': 'task1',
        ...         'name': 'Design Phase',
        ...         'start_date': '2024-01-01',
        ...         'duration_days': 5,
        ...         'progress': 30
        ...     }
        ... ]
        >>> result = generate_gantt_chart(tasks)
        >>> print(result['tasks'][0]['name'])
        'Design Phase'
    """
    if tasks is None:
        raise TypeError("Tasks input cannot be None")
        
    if not isinstance(tasks, list):
        raise TypeError("Tasks input must be a list")
        
    generator = GanttChartData()
    generator.tasks = tasks
    
    try:
        processed_tasks = generator.build_gantt_data()
        return {"tasks": processed_tasks}
    except Exception as e:
        logger.error(f"Failed to generate Gantt chart: {e}")
        raise


def main() -> None:
    """Main entry point for the Gantt chart data generator."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    generator = GanttChartData()
    
    try:
        generator.load_tasks()
        generator.save_gantt_data()
        
        summary = generator.get_summary()
        print("\nGantt Chart Summary:")
        print(f"Total Tasks: {summary['total_tasks']}")
        print(f"Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}")
        print(f"Average Progress: {summary['completion_rate']}%")
        
    except Exception as e:
        logger.error(f"Failed to generate Gantt chart data: {e}")
        raise


if __name__ == "__main__":
    main()
