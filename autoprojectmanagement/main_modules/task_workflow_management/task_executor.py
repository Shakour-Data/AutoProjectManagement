"""
Task Executor Module

This module provides functionality for managing and executing tasks in the project management system.
It includes task creation, execution, status tracking, and management capabilities.
"""

from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime


class TaskStatus(Enum):
    """Enumeration for task status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:
    """Represents a single task with execution capabilities."""
    
    def __init__(self, task_id: str, name: str, description: str = "", 
                 priority: int = 1, estimated_hours: float = 0.0):
        """
        Initialize a new task.
        
        Args:
            task_id: Unique identifier for the task
            name: Human-readable task name
            description: Detailed task description
            priority: Task priority (1-5, where 1 is highest)
            estimated_hours: Estimated time to complete in hours
        """
        self.task_id = task_id
        self.name = name
        self.description = description
        self.priority = priority
        self.estimated_hours = estimated_hours
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.error_message = None
    
    def start(self):
        """Mark the task as in progress."""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()
    
    def complete(self):
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def fail(self, error_message: str):
        """Mark the task as failed with an error message."""
        self.status = TaskStatus.FAILED
        self.error_message = error_message
        self.completed_at = datetime.now()
    
    def execute(self) -> bool:
        """
        Execute the task. This method should be overridden by subclasses.
        
        Returns:
            bool: True if execution succeeded, False otherwise
        """
        # Default implementation - subclasses should override
        try:
            # Simulate task execution
            self.start()
            # Add actual task logic here in subclasses
            self.complete()
            return True
        except Exception as e:
            self.fail(str(e))
            return False
    
    def __repr__(self):
        return f"Task(id={self.task_id}, name={self.name}, status={self.status.value})"


class TaskExecutor:
    """Manages and executes tasks in the project management system."""
    
    def __init__(self):
        """Initialize a new task executor."""
        self.tasks: Dict[str, Task] = {}
    
    def add_task(self, task: Task):
        """
        Add a task to the executor.
        
        Args:
            task: Task instance to add
            
        Raises:
            ValueError: If task with same ID already exists
        """
        if task.task_id in self.tasks:
            raise ValueError(f"Task with ID {task.task_id} already exists")
        self.tasks[task.task_id] = task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by ID.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            Task instance or None if not found
        """
        return self.tasks.get(task_id)
    
    def remove_task(self, task_id: str) -> bool:
        """
        Remove a task from the executor.
        
        Args:
            task_id: ID of the task to remove
            
        Returns:
            bool: True if task was removed, False if not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def execute_task(self, task_id: str) -> bool:
        """
        Execute a specific task.
        
        Args:
            task_id: ID of the task to execute
            
        Returns:
            bool: True if execution succeeded, False otherwise
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        try:
            result = task.execute()
            return result
        except Exception as e:
            task.fail(str(e))
            return False
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """
        Get all tasks with a specific status.
        
        Args:
            status: TaskStatus to filter by
            
        Returns:
            List of tasks with the specified status
        """
        return [task for task in self.tasks.values() if task.status == status]
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks managed by the executor.
        
        Returns:
            List of all tasks
        """
        return list(self.tasks.values())
    
    def clear_completed_tasks(self):
        """Remove all completed tasks from the executor."""
        completed_tasks = self.get_tasks_by_status(TaskStatus.COMPLETED)
        for task in completed_tasks:
            self.remove_task(task.task_id)
    
    def get_task_statistics(self) -> Dict[str, int]:
        """
        Get statistics about task statuses.
        
        Returns:
            Dictionary with counts for each task status
        """
        stats = {status.value: 0 for status in TaskStatus}
        for task in self.tasks.values():
            stats[task.status.value] += 1
        return stats


# Example usage and testing
if __name__ == "__main__":
    # Create a task executor
    executor = TaskExecutor()
    
    # Create some tasks
    task1 = Task("task-001", "Setup project", "Initialize the project structure", 1, 2.0)
    task2 = Task("task-002", "Write tests", "Create unit tests for modules", 2, 4.0)
    
    # Add tasks to executor
    executor.add_task(task1)
    executor.add_task(task2)
    
    # Execute tasks
    executor.execute_task("task-001")
    executor.execute_task("task-002")
    
    # Print statistics
    stats = executor.get_task_statistics()
    print("Task Statistics:", stats)
    
    # List all tasks
    print("\nAll Tasks:")
    for task in executor.get_all_tasks():
        print(f"  {task}")
