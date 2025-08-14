#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/task_workflow_management/task_management.py
File: task_management.py
Purpose: Task management system
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Task management system within the AutoProjectManagement system
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
Task management system within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import datetime
import json
import logging
import re
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Configure logging for the module
logger = logging.getLogger(__name__)

# Constants for better maintainability
MAX_LINE_LENGTH = 79
DEFAULT_PRIORITY = 0
DEFAULT_STATUS = "pending"
WORKFLOW_STEPS = {
    "Coding": False,
    "Testing": False,
    "Documentation": False,
    "Code Review": False,
    "Merge and Deployment": False,
    "Verification": False,
}

class TaskStatus(Enum):
    """Enumeration for task status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class WorkflowStep(Enum):
    """Enumeration for workflow step names."""
    CODING = "Coding"
    TESTING = "Testing"
    DOCUMENTATION = "Documentation"
    CODE_REVIEW = "Code Review"
    MERGE_AND_DEPLOYMENT = "Merge and Deployment"
    VERIFICATION = "Verification"

@dataclass
class Task:
    """
    Represents a project task with comprehensive attributes for tracking and management.
    
    Attributes:
        id: Unique identifier for the task
        title: Brief description of the task
        description: Detailed task description
        deadline: Target completion date
        dependencies: List of task IDs this task depends on
        assigned_to: List of assignees for this task
        status: Current task status
        priority: Task priority level (0-100)
        parent_id: Parent task ID for hierarchical organization
        urgency: Calculated urgency score (1-100)
        importance: Calculated importance score (1-100)
        github_issue_number: Associated GitHub issue number
        workflow_steps: Dictionary tracking completion of workflow steps
    """
    id: int
    title: str
    description: str = ""
    deadline: Optional[datetime.date] = None
    dependencies: List[int] = field(default_factory=list)
    assigned_to: List[str] = field(default_factory=list)
    status: str = TaskStatus.PENDING.value
    priority: int = DEFAULT_PRIORITY
    parent_id: Optional[int] = None
    urgency: Optional[float] = None
    importance: Optional[float] = None
    github_issue_number: Optional[int] = None
    workflow_steps: Dict[str, bool] = field(default_factory=lambda: WORKFLOW_STEPS.copy())

    def mark_workflow_step_completed(self, step_name: str) -> bool:
        """
        Mark a specific workflow step as completed.
        
        Args:
            step_name: Name of the workflow step to mark as completed
            
        Returns:
            True if step was successfully marked, False otherwise
        """
        if step_name in self.workflow_steps:
            self.workflow_steps[step_name] = True
            logger.info(f"Marked workflow step '{step_name}' as completed for Task {self.id}")
            return True
        logger.warning(f"Invalid workflow step '{step_name}' for Task {self.id}")
        return False

    def is_workflow_completed(self) -> bool:
        """Check if all workflow steps are completed."""
        return all(self.workflow_steps.values())

    def workflow_progress_percentage(self) -> float:
        """Calculate the percentage of completed workflow steps."""
        total_steps = len(self.workflow_steps)
        if total_steps == 0:
            return 0.0
        completed_steps = sum(1 for completed in self.workflow_steps.values() if completed)
        return (completed_steps / total_steps) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary representation."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'dependencies': self.dependencies,
            'assigned_to': self.assigned_to,
            'status': self.status,
            'priority': self.priority,
            'parent_id': self.parent_id,
            'urgency': self.urgency,
            'importance': self.importance,
            'github_issue_number': self.github_issue_number,
            'workflow_steps': self.workflow_steps,
            'workflow_progress': self.workflow_progress_percentage(),
            'is_workflow_completed': self.is_workflow_completed()
        }

class TaskManagement:
    """
    Central task management system for handling project tasks and workflows.
    
    This class provides comprehensive task management capabilities including:
    - Task creation and lifecycle management
    - Workflow step tracking
    - GitHub integration via commit message parsing
    - Hierarchical task organization (WBS)
    - Eisenhower matrix classification
    - Task prioritization and scheduling
    
    Example:
        >>> tm = TaskManagement()
        >>> task = tm.create_task("Implement new feature", priority=90)
        >>> tm.mark_workflow_step_completed(task.id, "Coding")
        >>> tasks = tm.classify_tasks_eisenhower()
    """
    
    def __init__(self) -> None:
        """Initialize the task management system."""
        self.tasks: Dict[int, Task] = {}
        self.next_task_id = 1
        logger.info("TaskManagement system initialized")

    def create_task(self, title: str, description: str = "", 
                   deadline: Optional[datetime.date] = None,
                   dependencies: Optional[List[int]] = None,
                   assigned_to: Optional[List[str]] = None,
                   priority: int = DEFAULT_PRIORITY,
                   parent_id: Optional[int] = None) -> Task:
        """
        Create a new task with the specified parameters.
        
        Args:
            title: Task title
            description: Detailed task description
            deadline: Target completion date
            dependencies: List of dependent task IDs
            assigned_to: List of assignees
            priority: Task priority (0-100)
            parent_id: Parent task ID for hierarchical organization
            
        Returns:
            The newly created Task object
        """
        task = Task(
            id=self.next_task_id,
            title=title,
            description=description,
            deadline=deadline,
            dependencies=dependencies or [],
            assigned_to=assigned_to or [],
            priority=priority,
            parent_id=parent_id
        )
        self.tasks[self.next_task_id] = task
        self.next_task_id += 1
        logger.info(f"Created task {task.id}: {task.title}")
        return task

    def update_workflow_steps_from_commit_message(self, commit_message: str) -> None:
        """
        Parse commit message to update workflow steps of tasks.
        
        Expected format: "Task <id>: <step> done" or similar variations.
        
        Args:
            commit_message: Git commit message to parse
            
        Example:
            >>> tm.update_workflow_steps_from_commit_message(
            ...     "Task 123: Code Review done - fixed all review comments")
        """
        pattern = r"Task (\d+): (\w+(?: \w+)*) done"
        matches = re.findall(pattern, commit_message, re.IGNORECASE)
        
        for task_id_str, step_name in matches:
            try:
                task_id = int(task_id_str)
                step_name = step_name.strip().title()
                if task_id in self.tasks:
                    self.tasks[task_id].mark_workflow_step_completed(step_name)
                    logger.info(
                        f"Updated workflow step '{step_name}' for Task {task_id} "
                        f"from commit message"
                    )
                else:
                    logger.warning(f"Task {task_id} not found for commit message update")
            except ValueError:
                logger.error(f"Invalid task ID format: {task_id_str}")
                continue

    def parse_creative_input(self, input_text: str) -> Task:
        """
        Parse creative user input text into a formal Task object.
        
        This method serves as a placeholder for NLP or rule-based parsing logic
        that can convert natural language task descriptions into structured tasks.
        
        Args:
            input_text: Natural language task description
            
        Returns:
            Task object created from the parsed input
            
        Example:
            >>> task = tm.parse_creative_input(
            ...     "Create a user authentication system by next Friday")
        """
        task = self.create_task(title=input_text.strip())
        logger.info(f"Parsed creative input into task {task.id}")
        return task

    def generate_wbs_from_idea(self, input_text: str, max_depth: int = 5) -> List[Task]:
        """
        Generate a hierarchical Work Breakdown Structure (WBS) from a creative idea.
        
        Creates a multi-level task hierarchy with parent-child relationships.
        
        Args:
            input_text: The main idea or project description
            max_depth: Maximum depth for task hierarchy (default: 5)
            
        Returns:
            List of all created tasks including the hierarchy
            
        Example:
            >>> tasks = tm.generate_wbs_from_idea("Build a web application")
            >>> print(f"Generated {len(tasks)} tasks across multiple levels")
        """
        root_task = self.create_task(
            title=input_text,
            description=f"Root task for: {input_text}"
        )
        
        # Generate hierarchical structure
        self._generate_task_hierarchy(root_task, 1, max_depth)
        
        all_tasks = list(self.tasks.values())
        logger.info(
            f"Generated WBS with {len(all_tasks)} tasks from idea: '{input_text}'"
        )
        return all_tasks

    def _generate_task_hierarchy(self, parent_task: Task, current_level: int, 
                               max_depth: int) -> None:
        """Recursively generate task hierarchy."""
        if current_level >= max_depth:
            return
            
        # Create subtasks for this level
        num_subtasks = max(1, 4 - current_level)  # Fewer tasks at deeper levels
        for i in range(1, num_subtasks + 1):
            subtask = self.create_task(
                title=f"{parent_task.title} - Level {current_level}.{i}",
                description=f"Subtask {i} at level {current_level}",
                parent_id=parent_task.id
            )
            
            # Recursively generate deeper levels
            self._generate_task_hierarchy(subtask, current_level + 1, max_depth)

    def load_scores(self, scores_path: str) -> None:
        """
        Load importance and urgency scores from JSON file.
        
        Args:
            scores_path: Path to JSON file containing task scores
            
        Raises:
            FileNotFoundError: If scores file doesn't exist
            json.JSONDecodeError: If scores file is invalid JSON
        """
        try:
            with open(scores_path, 'r', encoding='utf-8') as f:
                scores = json.load(f)
            
            # Map scores to tasks by ID
            updated_count = 0
            for task in self.tasks.values():
                score = scores.get(str(task.id))
                if score:
                    task.importance = score.get('importance', 0)
                    task.urgency = score.get('urgency', 0)
                    updated_count += 1
            
            logger.info(
                f"Loaded scores for {updated_count} tasks from {scores_path}"
            )
            
        except FileNotFoundError:
            logger.error(f"Scores file not found: {scores_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in scores file: {e}")
            raise

    def calculate_urgency_importance(self) -> None:
        """
        Calculate urgency and importance for each task using comprehensive factors.
        
        This method implements sophisticated scoring algorithms that consider:
        - Deadline proximity for urgency
        - Task significance, dependencies, and impact for importance
        - Propagates scores up the task hierarchy
        
        The calculation is performed for leaf tasks first, then propagated
        upward through the task hierarchy.
        """
        import random
        
        def calculate_importance_factors(task: Task) -> float:
            """Calculate importance based on multiple weighted factors."""
            factors = {
                "dependency": 8.5 if task.dependencies else 3.0,
                "critical_path": 9.0 if self._is_on_critical_path(task) else 2.0,
                "schedule_impact": random.uniform(5, 10),
                "cost_impact": random.uniform(4, 9),
                "key_objectives": random.uniform(6, 10),
                "risk_complexity": random.uniform(3, 8),
                "resource_rarity": random.uniform(2, 7),
                "stakeholder_priority": random.uniform(5, 10),
                "milestone_role": random.uniform(4, 9),
                "quality_impact": random.uniform(3, 8),
                "bottleneck_potential": random.uniform(4, 9),
                "reuse_frequency": random.uniform(2, 6),
            }
            importance_score = sum(factors.values())
            return max(1.0, min(100.0, importance_score))

        def calculate_urgency_factors(task: Task) -> float:
            """Calculate urgency based on deadline and time-sensitive factors."""
            factors = {
                "deadline_proximity": self._calculate_deadline_urgency(task),
                "next_activity_dependency": random.uniform(1, 10),
                "high_delay_risk": random.uniform(2, 8),
                "immediate_decision": random.uniform(1, 7),
                "stakeholder_pressure": random.uniform(2, 9),
                "limited_resource_time": random.uniform(1, 8),
                "competitive_advantage": random.uniform(1, 6),
                "critical_issue_fix": random.uniform(3, 10),
                "external_schedule_coordination": random.uniform(2, 7),
                "high_compensatory_cost": random.uniform(2, 8),
            }
            urgency_score = sum(factors.values())
            return max(1.0, min(100.0, urgency_score))

        # Calculate for leaf tasks first
        leaf_tasks = [
            t for t in self.tasks.values() 
            if not any(child.parent_id == t.id for child in self.tasks.values())
        ]
        
        for task in leaf_tasks:
            task.importance = calculate_importance_factors(task)
            task.urgency = calculate_urgency_factors(task)

        # Propagate scores up the hierarchy
        def propagate_scores(task_id: int) -> Tuple[float, float]:
            """Recursively propagate urgency and importance scores."""
            children = [
                t for t in self.tasks.values() 
                if t.parent_id == task_id
            ]
            
            if not children:
                task = self.tasks[task_id]
                return task.urgency or 0, task.importance or 0
            
            urgency_sum = 0.0
            importance_sum = 0.0
            
            for child in children:
                u, i = propagate_scores(child.id)
                urgency_sum += u
                importance_sum += i
            
            # Use average for parent tasks
            count = len(children)
            self.tasks[task_id].urgency = urgency_sum / count
            self.tasks[task_id].importance = importance_sum / count
            
            return urgency_sum / count, importance_sum / count

        # Process root tasks
        root_tasks = [
            t for t in self.tasks.values() 
            if t.parent_id is None
        ]
        
        for root in root_tasks:
            propagate_scores(root.id)

    def _calculate_deadline_urgency(self, task: Task) -> float:
        """Calculate urgency based on deadline proximity."""
        if not task.deadline:
            return 1.0
        
        days_left = (task.deadline - datetime.date.today()).days
        if days_left <= 0:
            return 100.0  # Maximum urgency for overdue tasks
        elif days_left <= 7:
            return 90.0 - (days_left * 10)  # 90-20 for 1-7 days
        elif days_left <= 30:
            return 50.0 - (days_left * 1)  # 50-20 for 8-30 days
        else:
            return max(1.0, 20.0 - (days_left * 0.1))  # 20-1 for 31+ days

    def _is_on_critical_path(self, task: Task) -> bool:
        """Determine if task is on the critical path."""
        # Placeholder implementation - would need actual project data
        return len(task.dependencies) > 2

    def classify_tasks_eisenhower(self) -> Dict[str, List[Task]]:
        """
        Classify tasks into Eisenhower matrix quadrants.
        
        Returns a dictionary with four categories:
        - do_now: High importance, high urgency (Do First)
        - schedule: High importance, low urgency (Schedule)
        - delegate: Low importance, high urgency (Delegate)
        - eliminate: Low importance, low urgency (Eliminate)
        
        Returns:
            Dictionary mapping quadrant names to lists of tasks
        """
        self.calculate_urgency_importance()
        
        do_now = []
        schedule = []
        delegate = []
        eliminate = []
        
        threshold = 70.0  # Threshold for high importance/urgency
        
        for task in self.tasks.values():
            if task.importance is None or task.urgency is None:
                continue
                
            if task.importance >= threshold and task.urgency >= threshold:
                do_now.append(task)
            elif task.importance >= threshold and task.urgency < threshold:
                schedule.append(task)
            elif task.importance < threshold and task.urgency >= threshold:
                delegate.append(task)
            else:
                eliminate.append(task)
        
        return {
            "do_now": sorted(do_now, key=lambda t: (t.urgency, t.importance), reverse=True),
            "schedule": sorted(schedule, key=lambda t: t.importance, reverse=True),
            "delegate": sorted(delegate, key=lambda t: t.urgency, reverse=True),
            "eliminate": sorted(eliminate, key=lambda t: (t.urgency, t.importance))
        }

    def prioritize_tasks(self) -> List[Task]:
        """
        Prioritize tasks based on calculated urgency and importance scores.
        
        Returns:
            List of tasks sorted by priority (highest first)
        """
        self.calculate_urgency_importance()
        
        def task_priority(task: Task) -> Tuple[float, datetime.date]:
            """Calculate composite priority score for sorting."""
            if task.importance is None or task.urgency is None:
                return (0.0, datetime.date.max)
            
            # Weighted combination of importance and urgency
            priority_score = (task.importance * 0.7 + task.urgency * 0.3)
            deadline = task.deadline or datetime.date.max
            
            return (-priority_score, deadline)  # Negative for descending sort
        
        sorted_tasks = sorted(self.tasks.values(), key=task_priority)
        logger.info(f"Prioritized {len(sorted_tasks)} tasks")
        return sorted_tasks

    def schedule_tasks(self) -> List[Task]:
        """
        Generate task scheduling recommendations based on priorities.
        
        Returns:
            List of tasks in recommended execution order
        """
        prioritized = self.prioritize_tasks()
        
        # Consider dependencies in scheduling
        scheduled = []
        completed = set()
        
        for task in prioritized:
            if all(dep in completed for dep in task.dependencies):
                scheduled.append(task)
                completed.add(task.id)
            else:
                # Move to later if dependencies not met
                logger.warning(
                    f"Task {task.id} has unmet dependencies: {task.dependencies}"
                )
        
        logger.info(f"Scheduled {len(scheduled)} tasks")
        return scheduled

    def detect_conflicts(self) -> List[str]:
        """
        Detect and report conflicts in task dependencies or assignments.
        
        Returns:
            List of conflict messages
        """
        conflicts = []
        
        # Check for missing dependencies
        for task in self.tasks.values():
            for dep_id in task.dependencies:
                if dep_id not in self.tasks:
                    conflicts.append(
                        f"Task {task.id} depends on unknown task {dep_id}"
                    )
        
        # Check for circular dependencies
        visited = set()
        path = set()
        
        def has_cycle(task_id: int) -> bool:
            """Check for circular dependencies using DFS."""
            if task_id in path:
                return True
            if task_id in visited:
                return False
                
            path.add(task_id)
            visited.add(task_id)
            
            task = self.tasks.get(task_id)
            if task:
                for dep_id in task.dependencies:
                    if has_cycle(dep_id):
                        return True
            
            path.remove(task_id)
            return False
        
        for task_id in self.tasks:
            if has_cycle(task_id):
                conflicts.append(f"Circular dependency detected involving task {task_id}")
        
        if conflicts:
            logger.warning(f"Detected {len(conflicts)} task conflicts")
        else:
            logger.info("No task conflicts detected")
        
        return conflicts

    def assign_task(self, task_id: int, users: List[str]) -> bool:
        """
        Assign a task to one or more users.
        
        Args:
            task_id: ID of the task to assign
            users: List of user names/identifiers
            
        Returns:
            True if assignment successful, False otherwise
        """
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found for assignment")
            return False
        
        self.tasks[task_id].assigned_to = users
        logger.info(f"Assigned task {task_id} to users: {users}")
        return True

    def mark_task_completed(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of the task to mark as completed
            
        Returns:
            True if task was successfully marked, False otherwise
        """
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found for completion")
            return False
        
        self.tasks[task_id].status = TaskStatus.COMPLETED.value
        logger.info(f"Marked task {task_id} as completed")
        return True

    def export_tasks(self, export_path: str) -> None:
        """
        Export all tasks to JSON file.
        
        Args:
            export_path: Path where tasks should be exported
            
        Raises:
            IOError: If file cannot be written
        """
        try:
            tasks_data = {
                str(task.id): task.to_dict() 
                for task in self.tasks.values()
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported {len(tasks_data)} tasks to {export_path}")
            
        except IOError as e:
            logger.error(f"Failed to export tasks: {e}")
            raise

    def import_tasks(self, import_path: str) -> None:
        """
        Import tasks from JSON file.
        
        Args:
            import_path: Path to JSON file containing tasks
            
        Raises:
            FileNotFoundError: If import file doesn't exist
            json.JSONDecodeError: If import file is invalid JSON
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            imported_count = 0
            for task_id_str, task_data in tasks_data.items():
                try:
                    task_id = int(task_id_str)
                    task = Task(
                        id=task_id,
                        title=task_data['title'],
                        description=task_data.get('description', ''),
                        deadline=datetime.date.fromisoformat(task_data['deadline']) 
                                if task_data.get('deadline') else None,
                        dependencies=task_data.get('dependencies', []),
                        assigned_to=task_data.get('assigned_to', []),
                        status=task_data.get('status', TaskStatus.PENDING.value),
                        priority=task_data.get('priority', DEFAULT_PRIORITY),
                        parent_id=task_data.get('parent_id'),
                        urgency=task_data.get('urgency'),
                        importance=task_data.get('importance'),
                        github_issue_number=task_data.get('github_issue_number')
                    )
                    
                    # Restore workflow steps
                    if 'workflow_steps' in task_data:
                        task.workflow_steps.update(task_data['workflow_steps'])
                    
                    self.tasks[task_id] = task
                    imported_count += 1
                    
                    # Update next_task_id if needed
                    if task_id >= self.next_task_id:
                        self.next_task_id = task_id + 1
                        
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping invalid task data: {e}")
                    continue
            
            logger.info(f"Successfully imported {imported_count} tasks from {import_path}")
            
        except FileNotFoundError as e:
            logger.error(f"Import file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in import file: {e}")
            raise

    def get_task_statistics(self) -> Dict[str, Any]:
        """
        Generate comprehensive task statistics.
        
        Returns:
            Dictionary containing task statistics
        """
        if not self.tasks:
            return {
                'total_tasks': 0,
                'completed_tasks': 0,
                'pending_tasks': 0,
                'in_progress_tasks': 0,
                'average_completion': 0.0,
                'tasks_with_deadlines': 0,
                'overdue_tasks': 0
            }
        
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks.values() 
                            if t.status == TaskStatus.COMPLETED.value)
        pending_tasks = sum(1 for t in self.tasks.values() 
                          if t.status == TaskStatus.PENDING.value)
        in_progress_tasks = sum(1 for t in self.tasks.values() 
                              if t.status == TaskStatus.IN_PROGRESS.value)
        
        # Calculate average workflow completion
        total_completion = sum(t.workflow_progress_percentage() 
                             for t in self.tasks.values())
        average_completion = total_completion / total_tasks
        
        # Deadline statistics
        today = datetime.date.today()
        tasks_with_deadlines = sum(1 for t in self.tasks.values() 
                                 if t.deadline is not None)
        overdue_tasks = sum(1 for t in self.tasks.values() 
                          if t.deadline and t.deadline < today 
                          and t.status != TaskStatus.COMPLETED.value)
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'average_completion': round(average_completion, 2),
            'tasks_with_deadlines': tasks_with_deadlines,
            'overdue_tasks': overdue_tasks,
            'completion_rate': round((completed_tasks / total_tasks) * 100, 2)
        }
