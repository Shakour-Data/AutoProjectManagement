#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/task_workflow_management/importance_urgency_calculator.py
File: importance_urgency_calculator.py
Purpose: Importance and urgency calculation
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Importance and urgency calculation within the AutoProjectManagement system
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
Importance and urgency calculation within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import json
import os
import logging
from typing import List, Dict, Tuple, Any, Optional
from datetime import datetime, timedelta
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Phase 1: Structure & Standards - Constants and Enums
class PriorityLevel(Enum):
    """Enumeration for task priority levels."""
    LOW = 1
    MEDIUM = 5
    HIGH = 10

class TaskCategory(Enum):
    """Enumeration for task categories in Eisenhower Matrix."""
    DO_FIRST = "do_first"      # Important & Urgent
    SCHEDULE = "schedule"      # Important & Not Urgent
    DELEGATE = "delegate"      # Not Important & Urgent
    ELIMINATE = "eliminate"    # Not Important & Not Urgent

# Phase 2: Documentation - Constants for configuration
MAX_DEPENDENCIES = 10
MAX_COST_IMPACT = 100000
MAX_RISK_SCORE = 10
MAX_PRIORITY = 10
DAYS_WINDOW = 3

class ImportanceUrgencyCalculator:
    """
    Calculate task importance and urgency scores using Eisenhower Matrix methodology.
    
    This class provides comprehensive task prioritization based on multiple factors
    including dependencies, critical path, cost impact, deadlines, and risk assessment.
    
    Attributes:
        wbs_data: List of task dictionaries with hierarchical structure
        task_scores: Dictionary mapping task IDs to their calculated scores
    """
    
    def __init__(self, wbs_data: List[Dict[str, Any]]) -> None:
        """
        Initialize the calculator with WBS data.
        
        Args:
            wbs_data: List of task dictionaries with hierarchical structure
                      Each task dict should have:
                      - id: unique identifier
                      - title: task title
                      - level: hierarchical level (int)
                      - subtasks: list of subtasks (same structure)
                      - other metadata as needed
                      
        Raises:
            ValueError: If wbs_data is empty or invalid
        """
        if not wbs_data:
            raise ValueError("WBS data cannot be empty")
            
        self.wbs_data = wbs_data
        self.task_scores = {}

    def score_task(self, task: Dict[str, Any]) -> Tuple[float, float]:
        """
        Recursively score a task based on its subtasks or base criteria.
        
        For leaf tasks, scores are calculated based on defined criteria.
        For parent tasks, scores are aggregated from subtasks.
        
        Args:
            task: Task dictionary to score
            
        Returns:
            Tuple of (importance_score, urgency_score) both between 0-100
            
        Raises:
            TypeError: If task is None or has invalid structure
            ValueError: If task data is malformed
        """
        if task is None:
            raise TypeError("Task cannot be None")
            
        task_id = task.get('id')
        if not task_id:
            raise ValueError("Task must have an 'id' field")
            
        # Check if already scored
        if task_id in self.task_scores:
            existing = self.task_scores[task_id]
            return existing.importance, existing.urgency
            
        try:
            if not task.get('subtasks'):
                # Leaf task - calculate based on criteria
                importance = self._calculate_importance(task)
                urgency = self._calculate_urgency(task)
            else:
                # Parent task - aggregate from subtasks
                importance_values = []
                urgency_values = []
                
                for subtask in task['subtasks']:
                    sub_imp, sub_urg = self.score_task(subtask)
                    importance_values.append(sub_imp)
                    urgency_values.append(sub_urg)
                
                importance = sum(importance_values) / len(importance_values) if importance_values else 0.0
                urgency = sum(urgency_values) / len(urgency_values) if urgency_values else 0.0
            
            # Store the score
            self.task_scores[task_id] = {
                'importance': round(importance, 2),
                'urgency': round(urgency, 2)
            }
            
            return importance, urgency
            
        except Exception as e:
            logger.error(f"Error scoring task {task_id}: {str(e)}")
            raise

    def _calculate_importance(self, task: Dict[str, Any]) -> float:
        """
        Calculate importance based on multiple factors.
        
        Args:
            task: Task dictionary containing task details
            
        Returns:
            Importance score between 0-100
            
        Raises:
            TypeError: If task is None or has invalid structure
        """
        if task is None:
            raise TypeError("Task cannot be None")
            
        try:
            # Calculate dependency factor
            dependencies = task.get('dependencies', [])
            if not isinstance(dependencies, list):
                raise TypeError("dependencies must be a list")
            dependency_factor = min(1.0, len(dependencies) / MAX_DEPENDENCIES)

            # Calculate critical path factor
            critical_path = task.get('critical_path', False)
            critical_path_factor = 1.0 if critical_path else 0.0

            # Calculate cost impact factor
            cost_impact = task.get('cost_impact', 0)
            if isinstance(cost_impact, bool):
                raise TypeError("cost_impact must not be a boolean")
            cost_factor = min(1.0, cost_impact / MAX_COST_IMPACT)

            # Calculate priority factor
            priority = task.get('priority', 0)
            priority_factor = self._normalize_priority(priority)

            # Weighted calculation
            weights = [0.3, 0.3, 0.2, 0.2]  # dependency, critical_path, cost, priority
            factors = [dependency_factor, critical_path_factor, cost_factor, priority_factor]
            
            importance = sum(w * f for w, f in zip(weights, factors))
            return round(importance * 100, 2)
            
        except Exception as e:
            task_id = task.get('id', 'unknown')
            logger.error(f"Error calculating importance for task {task_id}: {str(e)}")
            raise

    def _calculate_urgency(self, task: Dict[str, Any]) -> float:
        """
        Calculate urgency based on multiple factors.
        
        Args:
            task: Task dictionary containing task details
            
        Returns:
            Urgency score between 0-100
            
        Raises:
            TypeError: If task is None or has invalid structure
        """
        if task is None:
            raise TypeError("Task cannot be None")
            
        try:
            # Calculate time factor based on deadline
            now = datetime.now()
            deadline_str = task.get('deadline')
            time_factor = 0.0
            
            if deadline_str:
                try:
                    deadline = datetime.fromisoformat(str(deadline_str))
                    total_seconds = (deadline - now).total_seconds()
                    normalized_time = max(0.0, min(1.0, total_seconds / (DAYS_WINDOW * 24 * 3600)))
                    time_factor = 1.0 - normalized_time
                except ValueError:
                    time_factor = 0.0

            # Calculate risk factor
            risk_of_delay = task.get('risk_of_delay', 0)
            risk_factor = min(1.0, risk_of_delay / MAX_RISK_SCORE)

            # Calculate pressure factor
            stakeholder_pressure = task.get('stakeholder_pressure', 0)
            pressure_factor = min(1.0, stakeholder_pressure / MAX_RISK_SCORE)

            # Weighted calculation
            weights = [0.5, 0.3, 0.2]  # time, risk, pressure
            factors = [time_factor, risk_factor, pressure_factor]
            
            urgency = sum(w * f for w, f in zip(weights, factors))
            return round(urgency * 100, 2)
            
        except Exception as e:
            task_id = task.get('id', 'unknown')
            logger.error(f"Error calculating urgency for task {task_id}: {str(e)}")
            raise

    def _normalize_priority(self, priority: Any) -> float:
        """
        Normalize priority value to 0-1 range.
        
        Args:
            priority: Priority value (string, int, or float)
            
        Returns:
            Normalized priority factor between 0-1
        """
        if priority is None:
            return 0.0
            
        if isinstance(priority, str):
            priority_map = {
                "low": 0.1,
                "medium": 0.5,
                "high": 1.0,
                "بالا": 1.0,
                "اهم": 1.0,
            }
            return priority_map.get(priority.lower(), 0.0)
        elif isinstance(priority, (int, float)) and not isinstance(priority, bool):
            return min(1.0, max(0.0, priority / MAX_PRIORITY))
        else:
            return 0.0

    def _determine_category(self, importance: float, urgency: float) -> TaskCategory:
        """
        Determine Eisenhower Matrix category based on importance and urgency.
        
        Args:
            importance: Importance score (0-100)
            urgency: Urgency score (0-100)
            
        Returns:
            Task category enum value
        """
        importance_threshold = 50
        urgency_threshold = 50
        
        if importance >= importance_threshold and urgency >= urgency_threshold:
            return TaskCategory.DO_FIRST
        elif importance >= importance_threshold and urgency < urgency_threshold:
            return TaskCategory.SCHEDULE
        elif importance < importance_threshold and urgency >= urgency_threshold:
            return TaskCategory.DELEGATE
        else:
            return TaskCategory.ELIMINATE

    def calculate_all(self) -> Dict[str, Dict[str, float]]:
        """
        Calculate scores for all tasks in the WBS data.
        
        Returns:
            Dictionary mapping task IDs to their importance and urgency scores
        """
        for task in self.wbs_data:
            self.score_task(task)
        return self.task_scores

    def get_eisenhower_matrix(self) -> Dict[str, List[str]]:
        """
        Organize tasks into Eisenhower Matrix categories.
        
        Returns:
            Dictionary with categories as keys and lists of task IDs as values
        """
        matrix = {
            "do_first": [],
            "schedule": [],
            "delegate": [],
            "eliminate": []
        }
        
        for task_id, scores in self.task_scores.items():
            importance = scores['importance']
            urgency = scores['urgency']
            category = self._determine_category(importance, urgency)
            matrix[category.value].append(task_id)
            
        return matrix

# Phase 4: Integration - Utility functions
def load_wbs_from_file(filepath: str) -> List[Dict[str, Any]]:
    """
    Load WBS data from JSON file.
    
    Args:
        filepath: Path to JSON file containing WBS data
        
    Returns:
        List of task dictionaries
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        logger.error(f"WBS file not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {filepath}: {str(e)}")
        raise

def save_scores_to_json(scores: Dict[str, Dict[str, float]], filepath: str) -> None:
    """
    Save calculated scores to JSON file.
    
    Args:
        scores: Dictionary of task scores
        filepath: Path to save the scores file
        
    Raises:
        IOError: If file cannot be written
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scores, f, indent=2, ensure_ascii=False)
    except IOError as e:
        logger.error(f"Error saving scores to {filepath}: {str(e)}")
        raise

# Phase 4: Integration - Main execution
if __name__ == "__main__":
    """Main execution block for standalone usage."""
    import os
    
    # Define file paths
    wbs_file = os.path.join(os.path.dirname(__file__), '../../SystemInputs/user_inputs/detailed_wbs.json')
    scores_file = os.path.join(os.path.dirname(__file__), '../../SystemInputs/system_generated/wbs_scores.json')
    
    try:
        # Load WBS data
        wbs_data = load_wbs_from_file(wbs_file)
        
        # Calculate scores
        calculator = ImportanceUrgencyCalculator(wbs_data)
        scores = calculator.calculate_all()
        
        # Save results
        save_scores_to_json(scores, scores_file)
        
        # Generate Eisenhower Matrix
        matrix = calculator.get_eisenhower_matrix()
        
        logger.info(f"Successfully calculated scores for {len(scores)} tasks")
        logger.info(f"Eisenhower Matrix: {matrix}")
        print(f"Importance and urgency scores saved to {scores_file}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise
