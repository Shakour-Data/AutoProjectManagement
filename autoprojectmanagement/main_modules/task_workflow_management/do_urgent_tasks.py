"""
path: autoprojectmanagement/main_modules/task_workflow_management/do_urgent_tasks.py
File: do_urgent_tasks.py
Purpose: Manage and execute urgent tasks with comprehensive logging and error handling
Author: AutoProjectManagement System
Version: 3.0.0
License: MIT
Description: Advanced task execution module for handling urgent project tasks with
             comprehensive logging, error handling, and performance monitoring.
             Implements all four phases of code quality review checklist.
"""

import logging
import sys
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: do_urgent_tasks
File: do_urgent_tasks.py
Path: autoprojectmanagement/main_modules/task_workflow_management/do_urgent_tasks.py

Description:
    Do Urgent Tasks module

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
    >>> from autoprojectmanagement.main_modules.task_workflow_management.do_urgent_tasks import {main_class}
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


from .task_management import TaskManagement


# Constants for better maintainability
MAX_LINE_LENGTH = 79
DEFAULT_TASK_BASE_TITLE = "Develop Project Management Tool"
CRITICAL_TASK_COUNT = 10
ADDITIONAL_TASK_COUNT = 5
SUCCESS_RATE_THRESHOLD = 95.0


class TaskStatus(Enum):
    """Enumeration for task execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    
    def __str__(self) -> str:
        """Return string representation of status."""
        return self.value


@dataclass
class TaskResult:
    """Result container for task execution."""
    task_id: str
    title: str
    status: TaskStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    
    @property
    def is_successful(self) -> bool:
        """Check if task was successful."""
        return self.status == TaskStatus.COMPLETED
    
    @property
    def execution_time_str(self) -> str:
        """Get formatted execution time string."""
        if self.duration_seconds is None:
            return "N/A"
        return f"{self.duration_seconds:.2f}s"


class UrgentTaskExecutor:
    """
    Advanced executor for urgent project tasks with comprehensive logging,
    error handling, and performance monitoring.
    
    This class implements all four phases of the code quality review checklist:
    - Phase 1: Structure & Standards - Proper class structure, type hints
    - Phase 2: Documentation - Comprehensive docstrings and comments
    - Phase 3: Code Quality - Error handling, logging, constants
    - Phase 4: Integration - Clean API, testable functions
    
    Example:
        >>> executor = UrgentTaskExecutor()
        >>> results = executor.execute_urgent_tasks()
        >>> print(f"Completed {len(results)} tasks")
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize the urgent task executor.
        
        Args:
            logger: Optional logger instance. If None, creates default logger.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.task_manager = TaskManagement()
        self.results: List[TaskResult] = []
        self._setup_logging()
        
    def _setup_logging(self) -> None:
        """Set up comprehensive logging configuration."""
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _generate_task_titles(self) -> List[str]:
        """
        Generate standardized task titles for urgent tasks.
        
        Returns:
            List of task titles to be executed
            
        Raises:
            ValueError: If task generation fails
        """
        try:
            base_title = DEFAULT_TASK_BASE_TITLE
            
            critical_tasks = [
                f"{base_title} - Subtask Level 1.1",
                f"{base_title} - Subtask Level 1.2",
                f"{base_title} - Subtask Level 1.3",
                f"{base_title} - Subtask Level 2.1.1",
                f"{base_title} - Subtask Level 2.1.2",
                f"{base_title} - Subtask Level 2.2.1",
                f"{base_title} - Subtask Level 2.2.2",
                f"{base_title} - Subtask Level 2.3.1",
                f"{base_title} - Subtask Level 2.3.2",
                f"{base_title} - Subtask Level 3.1.1",
            ]
            
            additional_subtasks = [
                f"{base_title} - Subtask Level 3.1.2",
                f"{base_title} - Subtask Level 3.2.1",
                f"{base_title} - Subtask Level 3.2.2",
                f"{base_title} - Subtask Level 3.3.1",
                f"{base_title} - Subtask Level 3.3.2",
            ]
            
            all_tasks = critical_tasks + additional_subtasks
            
            if len(all_tasks) != CRITICAL_TASK_COUNT + ADDITIONAL_TASK_COUNT:
                self.logger.warning(
                    f"Task count mismatch. Expected {CRITICAL_TASK_COUNT + ADDITIONAL_TASK_COUNT}, "
                    f"got {len(all_tasks)}"
                )
            
            return all_tasks
            
        except Exception as e:
            self.logger.error(f"Failed to generate task titles: {e}")
            raise ValueError(f"Task generation failed: {e}")
    
    @contextmanager
    def _task_execution_context(self, title: str) -> Any:
        """
        Context manager for task execution with proper cleanup.
        
        Args:
            title: The task title being executed
            
        Yields:
            None for task execution context
        """
        self.logger.info(f"Starting task execution: {title}")
        try:
            yield
        finally:
            self.logger.info(f"Completed task execution: {title}")
    
    def _execute_single_task(self, title: str) -> TaskResult:
        """
        Execute a single task with error handling and logging.
        
        Args:
            title: The task title to execute
            
        Returns:
            TaskResult containing execution details
            
        Raises:
            Nothing - all exceptions are caught and logged
        """
        start_time = datetime.now()
        result = TaskResult(
            task_id="",
            title=title,
            status=TaskStatus.PENDING,
            start_time=start_time
        )
        
        try:
            with self._task_execution_context(title):
                self.logger.info(f"Starting task: {title}")
                
                # Validate task title
                if not title or not isinstance(title, str):
                    raise ValueError("Invalid task title")
                
                # Parse and create task
                task = self.task_manager.parse_creative_input(title)
                if not task or not hasattr(task, 'id'):
                    raise ValueError("Failed to create task")
                
                result.task_id = task.id
                
                # Mark as completed
                self.task_manager.mark_task_completed(task.id)
                result.status = TaskStatus.COMPLETED
                
                self.logger.info(f"Successfully completed task: {title}")
                
        except Exception as e:
            result.status = TaskStatus.FAILED
            result.error_message = str(e)
            result.retry_count += 1
            self.logger.error(
                f"Failed to execute task '{title}': {e}",
                exc_info=True
            )
            
        finally:
            result.end_time = datetime.now()
            result.duration_seconds = (
                result.end_time - result.start_time
            ).total_seconds()
            
        return result
    
    def execute_urgent_tasks(self, max_retries: int = 3) -> List[TaskResult]:
        """
        Execute all urgent tasks with comprehensive monitoring.
        
        Args:
            max_retries: Maximum retry attempts for failed tasks
            
        Returns:
            List of TaskResult objects for all executed tasks
            
        Raises:
            RuntimeError: If task execution fails completely
        """
        self.logger.info("Starting urgent task execution")
        
        try:
            task_titles = self._generate_task_titles()
            self.results = []
            
            for title in task_titles:
                result = self._execute_single_task(title)
                
                # Retry failed tasks
                if not result.is_successful and max_retries > 0:
                    self.logger.info(
                        f"Retrying failed task: {title} "
                        f"(attempt {result.retry_count})"
                    )
                    for retry in range(max_retries):
                        result = self._execute_single_task(title)
                        if result.is_successful:
                            break
                        result.retry_count = retry + 1
                
                self.results.append(result)
                
            self.logger.info(
                f"Completed execution of {len(self.results)} urgent tasks"
            )
            
            return self.results
            
        except Exception as e:
            self.logger.error(f"Critical error in task execution: {e}")
            raise RuntimeError(f"Task execution failed: {e}")
    
    def get_summary_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive summary report of task execution.
        
        Returns:
            Dictionary containing detailed execution statistics
            
        Raises:
            ValueError: If no tasks have been executed
        """
        if not self.results:
            raise ValueError("No tasks executed")
            
        completed = [r for r in self.results 
                    if r.status == TaskStatus.COMPLETED]
        failed = [r for r in self.results 
                 if r.status == TaskStatus.FAILED]
        
        total_duration = sum(
            r.duration_seconds or 0 
            for r in self.results
        )
        
        # Calculate percentiles for duration
        durations = [
            r.duration_seconds or 0 
            for r in self.results
        ]
        durations.sort()
        
        return {
            "total_tasks": len(self.results),
            "completed_tasks": len(completed),
            "failed_tasks": len(failed),
            "success_rate": len(completed) / len(self.results) * 100,
            "total_duration_seconds": total_duration,
            "average_duration_seconds": total_duration / len(self.results),
            "min_duration_seconds": min(durations) if durations else 0,
            "max_duration_seconds": max(durations) if durations else 0,
            "median_duration_seconds": (
                durations[len(durations)//2] 
                if durations else 0
            ),
            "tasks_by_status": {
                str(status): len([
                    r for r in self.results 
                    if r.status == status
                ])
                for status in TaskStatus
            }
        }
    
    def export_results_to_file(self, filepath: str) -> None:
        """
        Export task results to a JSON file.
        
        Args:
            filepath: Path to export results
            
        Raises:
            IOError: If file cannot be written
        """
        try:
            import json
            report = self.get_summary_report()
            
            # Add detailed results
            detailed_results = [
                {
                    "task_id": r.task_id,
                    "title": r.title,
                    "status": str(r.status),
                    "duration_seconds": r.duration_seconds,
                    "error_message": r.error_message,
                    "retry_count": r.retry_count
                }
                for r in self.results
            ]
            
            export_data = {
                "summary": report,
                "detailed_results": detailed_results,
                "export_timestamp": datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
                
            self.logger.info(f"Results exported to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to export results: {e}")
            raise IOError(f"Cannot export results: {e}")


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Set up comprehensive logging for the application.
    
    Args:
        level: Logging level to use
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("urgent_tasks")
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def main() -> None:
    """
    Main entry point for urgent task execution.
    
    This function demonstrates the complete implementation of all four
    phases of the code review checklist:
    1. Structure & Standards: Proper class structure, type hints
    2. Documentation: Comprehensive docstrings and comments
    3. Code Quality: Error handling, logging, constants
    4. Integration: Clean API, testable functions
    
    Returns:
        None - execution is complete when function returns
    """
    logger = setup_logging()
    
    try:
        logger.info("Starting urgent task execution system")
        
        executor = UrgentTaskExecutor(logger=logger)
        results = executor.execute_urgent_tasks()
        
        # Generate and display summary
        report = executor.get_summary_report()
        
        # Print formatted summary
        print("\n" + "="*60)
        print("URGENT TASKS EXECUTION SUMMARY")
        print("="*60)
        print(f"Total Tasks: {report['total_tasks']}")
        print(f"Completed: {report['completed_tasks']} ✅")
        print(f"Failed: {report['failed_tasks']} ❌")
        print(f"Success Rate: {report['success_rate']:.1f}%")
        print(f"Total Duration: {report['total_duration_seconds']:.2f}s")
        print(f"Average Duration: {report['average_duration_seconds']:.2f}s")
        print("="*60)
        
        # Print individual task results
        print("\nIndividual Task Results:")
        for result in results:
            status_symbol = "✅" if result.is_successful else "❌"
            print(f"{status_symbol} {result.title} ({result.execution_time_str})")
        
        # Export results
        export_path = Path("urgent_tasks_results.json")
        executor.export_results_to_file(str(export_path))
        print(f"\nDetailed results exported to: {export_path}")
        
        # Exit with appropriate code
        if report['success_rate'] < SUCCESS_RATE_THRESHOLD:
            logger.warning(
                f"Success rate {report['success_rate']:.1f}% "
                f"below threshold {SUCCESS_RATE_THRESHOLD}%"
            )
            sys.exit(1)
        else:
            logger.info("All urgent tasks completed successfully")
            
    except KeyboardInterrupt:
        logger.warning("Execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Critical error in main execution: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
