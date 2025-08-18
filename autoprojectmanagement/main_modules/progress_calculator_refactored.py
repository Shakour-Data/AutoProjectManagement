import os
import json
import datetime
import logging
from typing import List, Dict, Any
from collections import defaultdict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ProgressCalculator:
    def __init__(self, input_dir: str = 'project_inputs/PM_JSON/user_inputs'):
        self.input_dir = input_dir
        self.tasks = []
        self.workflow_steps = []
        self.commit_progress = {}
        self.importance_cache = {}
        self.urgency_cache = {}

    def load_json_file(self, filename: str) -> Any:
        path = os.path.join(self.input_dir, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            return None

    def load_inputs(self):
        self.tasks = self.load_json_file('detailed_wbs.json') or []
        self.workflow_steps = self.load_json_file('workflow_definition.json') or []
        self.commit_progress = self.load_json_file('commit_progress.json') or {}

    def calculate_commit_progress(self, task_id: str) -> float:
        """Return commit-based progress percentage for a task."""
        return self.commit_progress.get(task_id, 0.0)

    def calculate_workflow_progress(self, task_id: str) -> float:
        """Calculate workflow progress as ratio of completed steps to total steps for the task."""
        steps = [step for step in self.workflow_steps if step.get('task_id') == task_id]
        if not steps:
            return 0.0
        completed_steps = sum(1 for step in steps if step.get('completed', False))
        return completed_steps / len(steps)

    def calculate_combined_progress(self, task_id: str, weight_commit: float = 0.5, weight_workflow: float = 0.5) -> float:
        """
        Calculate combined progress as weighted sum of commit and workflow progress.
        Adjust combined progress based on task status.
        """
        commit_prog = self.calculate_commit_progress(task_id)
        workflow_prog = self.calculate_workflow_progress(task_id)
        combined = (commit_prog * weight_commit) + (workflow_prog * weight_workflow)
        task = next((t for t in self.tasks if t.get('id') == task_id), None)
        if task:
            status = task.get('status', '').lower()
            if status == 'completed' and combined < 1.0:
                combined = 1.0
            elif status != 'completed' and combined > 0.0:
                combined = min(combined, 0.5)
        return combined

    def calculate_dynamic_importance(self, task: dict) -> float:
        """
        Calculate dynamic importance score based on:
        - Time factor: proximity to deadline (normalized over 7 days)
        - Dependency factor: number of dependencies normalized
        - Priority factor: normalized priority value
        Weights: 0.5, 0.3, 0.2 respectively
        """
        w1, w2, w3 = 0.5, 0.3, 0.2
        now = datetime.datetime.now()
        deadline_str = task.get('deadline')
        if deadline_str:
            try:
                deadline = datetime.datetime.fromisoformat(deadline_str)
                total_time = (deadline - now).total_seconds()
                normalized_time = max(0, min(1, total_time / (7*24*3600)))
                time_factor = 1 - normalized_time
            except Exception:
                time_factor = 0
        else:
            time_factor = 0
        dependencies = task.get('dependencies', [])
        dependency_factor = min(1, len(dependencies) / 10)
        priority = task.get('priority', 0)
        priority_factor = min(1, priority / 10)
        importance = w1 * time_factor + w2 * dependency_factor + w3 * priority_factor
        return importance

    def calculate_dynamic_urgency(self, task: dict) -> float:
        """
        Calculate dynamic urgency score based on:
        - Time factor: proximity to deadline (normalized over 3 days)
        - Status factor: task status (pending, in progress, etc.)
        - Resource availability factor: whether task is assigned
        Weights: 0.6, 0.3, 0.1 respectively
        """
        w1, w2, w3 = 0.6, 0.3, 0.1
        now = datetime.datetime.now()
        deadline_str = task.get('deadline')
        if deadline_str:
            try:
                deadline = datetime.datetime.fromisoformat(deadline_str)
                total_time = (deadline - now).total_seconds()
                normalized_time = max(0, min(1, total_time / (3*24*3600)))
                time_factor = 1 - normalized_time
            except Exception:
                time_factor = 0
        else:
            time_factor = 0
        status = task.get('status', '').lower()
        status_factor = 1 if status in ['pending', 'not started', 'in progress'] else 0
        assigned_to = task.get('assigned_to', [])
        resource_availability_factor = 1 if not assigned_to else 0
        urgency = w1 * time_factor + w2 * status_factor + w3 * resource_availability_factor
        return urgency

    def enrich_tasks_with_progress(self):
        """Calculate and enrich tasks with importance, urgency, score, and progress."""
        self.importance_cache = {}
        self.urgency_cache = {}
        for task in self.tasks:
            task_id = task.get('id')
            if not task_id:
                continue
            if task_id in self.importance_cache:
                importance = self.importance_cache[task_id]
            else:
                importance = self.calculate_dynamic_importance(task)
                self.importance_cache[task_id] = importance
            if task_id in self.urgency_cache:
                urgency = self.urgency_cache[task_id]
            else:
                urgency = self.calculate_dynamic_urgency(task)
                self.urgency_cache[task_id] = urgency
            score = self.calculate_score(importance, urgency)
            progress = self.calculate_combined_progress(task_id)
            task['importance'] = importance
            task['urgency'] = urgency
            task['score'] = score
            task['progress'] = progress
            # Set default status based on progress if missing
            if 'status' not in task or not task['status']:
                if progress >= 1.0:
                    task['status'] = 'completed'
                elif progress > 0.0:
                    task['status'] = 'in_progress'
                else:
                    task['status'] = 'pending'

    def calculate_score(self, importance: float, urgency: float, weight_importance: float = 0.6, weight_urgency: float = 0.4) -> float:
        """Calculate combined score as weighted sum of importance and urgency."""
        return (importance * weight_importance) + (urgency * weight_urgency)

    def get_enriched_tasks(self) -> List[Dict[str, Any]]:
        """Return the list of enriched tasks."""
        return self.tasks

def calculate_progress(data: dict) -> float:
    """
    Calculate progress percentage based on tasks_completed and total_tasks.
    Raises:
        KeyError: if required keys are missing.
        TypeError: if input types are invalid.
        ValueError: if values are negative or tasks_completed > total_tasks.
        ZeroDivisionError: if total_tasks is zero.
    """
    if not isinstance(data, dict):
        raise TypeError("Input data must be a dictionary.")
    if 'tasks_completed' not in data or 'total_tasks' not in data:
        raise KeyError("Missing required keys: 'tasks_completed' and/or 'total_tasks'.")
    tasks_completed = data['tasks_completed']
    total_tasks = data['total_tasks']
    if not (isinstance(tasks_completed, (int, float)) and isinstance(total_tasks, (int, float))):
        raise TypeError("Values for 'tasks_completed' and 'total_tasks' must be int or float.")
    if isinstance(tasks_completed, bool) or isinstance(total_tasks, bool):
        raise TypeError("Boolean values are not allowed for 'tasks_completed' or 'total_tasks'.")
    if tasks_completed < 0 or total_tasks < 0:
        raise ValueError("Values for 'tasks_completed' and 'total_tasks' must be non-negative.")
    if total_tasks == 0:
        raise ZeroDivisionError("Total tasks cannot be zero.")
    if tasks_completed > total_tasks:
        raise ValueError("'tasks_completed' cannot be greater than 'total_tasks'.")
    progress = (tasks_completed / total_tasks) * 100
    return progress
