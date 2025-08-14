#!/usr/bin/env python3
"""
Progress Report Generator Module for AutoProjectManagement.

This module provides functionality to generate comprehensive progress reports
based on project data stored in JSON files. It calculates task completion
rates, milestone achievements, and generates formatted markdown reports.

Author: AutoProjectManagement Team
Version: 2.0.0
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

# Constants
DEFAULT_DASHBOARD_PATH = Path('JSonDataBase') / 'OutPuts' / 'progress_report.md'
DEFAULT_PROGRESS_PATH = Path('JSonDataBase') / 'OutPuts' / 'commit_progress.json'
DEFAULT_TASK_DB_PATH = Path('JSonDataBase') / 'OutPuts' / 'commit_task_database.json'

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProgressReport:
    """
    A comprehensive progress report generator for project management.
    
    This class loads project data from JSON files, calculates various metrics
    about task completion, milestone achievements, and generates formatted
    markdown reports suitable for dashboards and documentation.
    
    Attributes:
        progress_path (Path): Path to the progress JSON file
        task_db_path (Path): Path to the task database JSON file
        output_path (Path): Path where the report will be saved
        
    Example:
        >>> report = ProgressReport()
        >>> report.generate()
        Progress report generated at JSonDataBase/OutPuts/progress_report.md
    """
    
    def __init__(self, 
                 progress_path: Optional[str] = None,
                 task_db_path: Optional[str] = None,
                 output_path: Optional[str] = None) -> None:
        """
        Initialize the ProgressReport generator.
        
        Args:
            progress_path: Custom path to progress JSON file
            task_db_path: Custom path to task database JSON file
            output_path: Custom path for output report file
            
        Raises:
            ValueError: If any provided path is invalid
        """
        self.progress_path = Path(progress_path) if progress_path else DEFAULT_PROGRESS_PATH
        self.task_db_path = Path(task_db_path) if task_db_path else DEFAULT_TASK_DB_PATH
        self.output_path = Path(output_path) if output_path else DEFAULT_DASHBOARD_PATH
        
        # Validate paths
        self._validate_paths()
        
    def _validate_paths(self) -> None:
        """Validate that all provided paths are valid."""
        for path_attr in ['progress_path', 'task_db_path', 'output_path']:
            path = getattr(self, path_attr)
            if not isinstance(path, Path):
                raise ValueError(f"Invalid path type for {path_attr}: {type(path)}")
    
    def load_json(self, path: Path) -> Dict[str, Any]:
        """
        Load and parse JSON data from a file.
        
        Args:
            path: Path to the JSON file to load
            
        Returns:
            Dictionary containing the parsed JSON data
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        if not path.exists():
            error_msg = f"JSON file not found: {path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
            
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"Successfully loaded JSON from {path}")
                return data
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in file {path}: {str(e)}"
            logger.error(error_msg)
            raise json.JSONDecodeError(error_msg, e.doc, e.pos)
    
    def generate_progress_summary(self) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of project progress.
        
        This method analyzes the progress data and task database to calculate
        various metrics including task completion rates, milestone achievements,
        and overall project status.
        
        Returns:
            Dictionary containing:
                - total_tasks: Total number of tasks
                - completed_tasks: Number of completed tasks
                - in_progress_tasks: Number of tasks in progress
                - pending_tasks: Number of pending tasks
                - completion_rate: Overall completion percentage
                - milestones_achieved: Number of achieved milestones
                - milestone_tasks: List of milestone tasks with status
        """
        try:
            progress_data = self.load_json(self.progress_path)
            task_db = self.load_json(self.task_db_path)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error loading data: {str(e)}")
            return self._get_empty_summary()
        
        # Calculate basic metrics
        total_tasks = len(task_db)
        completed_tasks = sum(1 for v in progress_data.values() 
                            if isinstance(v, (int, float)) and v >= 100)
        in_progress_tasks = sum(1 for v in progress_data.values() 
                              if isinstance(v, (int, float)) and 0 < v < 100)
        pending_tasks = max(0, total_tasks - completed_tasks - in_progress_tasks)
        
        # Calculate completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Process milestones
        milestones = [task for task in task_db.values() 
                     if isinstance(task, dict) and task.get('is_milestone', False)]
        milestones_achieved = 0
        milestone_tasks = []
        
        for milestone in milestones:
            file_path = milestone.get('file_path', 'Untitled')
            progress = progress_data.get(file_path, 0)
            status = 'Completed' if (isinstance(progress, (int, float)) and progress >= 100) else 'Pending'
            milestone_tasks.append((file_path, status))
            if status == 'Completed':
                milestones_achieved += 1
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'pending_tasks': pending_tasks,
            'completion_rate': round(completion_rate, 2),
            'milestones_achieved': milestones_achieved,
            'milestone_tasks': milestone_tasks
        }
    
    def _get_empty_summary(self) -> Dict[str, Any]:
        """Return an empty summary when data loading fails."""
        return {
            'total_tasks': 0,
            'completed_tasks': 0,
            'in_progress_tasks': 0,
            'pending_tasks': 0,
            'completion_rate': 0.0,
            'milestones_achieved': 0,
            'milestone_tasks': []
        }
    
    def generate_markdown_report(self, summary: Dict[str, Any]) -> str:
        """
        Generate a formatted markdown report from the progress summary.
        
        Args:
            summary: Dictionary containing progress metrics
            
        Returns:
            Formatted markdown string ready for display
        """
        lines = [
            "# Project Progress Report",
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            f"- **Total Tasks**: {summary['total_tasks']}",
            f"- **Completed Tasks**: {summary['completed_tasks']}",
            f"- **In Progress Tasks**: {summary['in_progress_tasks']}",
            f"- **Pending Tasks**: {summary['pending_tasks']}",
            f"- **Completion Rate**: {summary['completion_rate']}%",
            f"- **Milestones Achieved**: {summary['milestones_achieved']}",
            "",
            "## Task Distribution",
            "```",
            f"Completed:     {summary['completed_tasks']} tasks",
            f"In Progress:   {summary['in_progress_tasks']} tasks",
            f"Pending:       {summary['pending_tasks']} tasks",
            f"Total:         {summary['total_tasks']} tasks",
            "```",
            "",
            "## Completed Activities",
            f"- Successfully completed {summary['completed_tasks']} tasks",
            f"- Achieved {summary['milestones_achieved']} key milestones",
            "",
            "## In-Progress Activities",
            f"- Currently working on {summary['in_progress_tasks']} tasks",
            "",
            "## Pending Activities",
            f"- {summary['pending_tasks']} tasks remaining",
            "",
            "## Milestone Status"
        ]
        
        for milestone, status in summary['milestone_tasks']:
            lines.append(f"- **{milestone}**: {status}")
        
        lines.extend([
            "",
            "## Next Steps",
            "- Continue monitoring progress",
            "- Update task priorities as needed",
            "- Review and adjust project timeline"
        ])
        
        return "\n".join(lines)

    def save_report(self, content: str) -> None:
        """
        Save the generated report to a file.
        
        Args:
            content: The content to save in the report file
        """
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate(self) -> None:
        """
        Generate the progress report and save it to a file.
        """
        summary = self.generate_progress_summary()
        report_md = self.generate_markdown_report(summary)
        self.save_report(report_md)
        logger.info(f"Progress report generated at {self.output_path}")


def generate_report(task_management=None) -> None:
    """
    Generate a report using the ProgressReport class.
    
    Args:
        task_management: Optional task management parameter for future integration
    """
    report = ProgressReport()
    report.generate()


def generate_importance_urgency_report(task_management=None) -> None:
    """
    Placeholder for generating an importance-urgency report.
    
    Args:
        task_management: Optional task management parameter for future integration
    """
    logger.info("Importance-urgency report generation not yet implemented")


if __name__ == "__main__":
    report = ProgressReport()
    report.generate()
