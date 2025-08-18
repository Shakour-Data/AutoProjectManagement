#!/usr/bin/env python3
"""
Project Estimation Management Module

This module provides comprehensive project estimation capabilities including:
- Task duration estimation based on complexity
- Task cost estimation based on resources and duration
- Project-level duration and cost aggregation
- Multiple estimation methodologies (parametric, COCOMO II, Agile)
- JSON-based input/output handling

Usage:
    Basic usage:
    ```python
    from estimation_management import EstimationManagement
    
    # Create estimation manager
    manager = EstimationManagement()
    manager.run()
    ```
    
    Custom paths:
    ```python
    manager = EstimationManagement(
        detailed_wbs_path='custom/path/wbs.json',
        output_path='custom/path/output.json'
    )
    ```

Author: AutoProjectManagement Team
Date: 2024
Version: 2.0.0
"""

import json
import logging
import os
from typing import Dict, Any, Optional, Union
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_COST_PER_RESOURCE = 100.0  # Base cost per resource unit
DEFAULT_COMPLEXITY_MAPPING = {
    "low": 1.0,
    "medium": 3.0,
    "high": 5.0,
    "extreme": 8.0
}
MAX_LINE_LENGTH = 79
DEFAULT_ENCODING = 'utf-8'
JSON_INDENT = 2

# Estimation method constants
ESTIMATION_METHODS = {
    'PARAMETRIC': 'parametric',
    'COCOMO_II': 'cocomo_ii',
    'AGILE': 'agile'
}

# Error messages
ERROR_INVALID_TASK = "Task must be a non-empty dictionary"
ERROR_INVALID_PROJECT = "Project must be a non-empty dictionary"
ERROR_INVALID_RESOURCES = "Resources must be a positive number"


class BaseManagement:
    """
    Base class for management operations with JSON I/O capabilities.
    
    Provides common functionality for loading inputs from JSON files,
    processing data, and saving outputs to JSON files.
    """
    
    def __init__(self, input_paths: Dict[str, str], output_path: str) -> None:
        """
        Initialize BaseManagement with input and output paths.
        
        Args:
            input_paths: Dictionary mapping input names to file paths
            output_path: Path where output JSON will be saved
        """
        if not input_paths:
            raise ValueError("input_paths cannot be empty")
        if not output_path:
            raise ValueError("output_path cannot be empty")
            
        self.input_paths = input_paths
        self.output_path = output_path
        self.inputs = {}
        self.output = {}
        
    def load_json(self, path: str) -> Optional[Dict[str, Any]]:
        """Load JSON data from file with error handling."""
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            return None
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format in file: {path}")
            raise
        except Exception as e:
            logger.error(f"Error loading file {path}: {str(e)}")
            return None
            
    def save_json(self, data: Dict[str, Any], path: str) -> None:
        """Save data to JSON file with proper formatting."""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(
                    data, 
                    file, 
                    indent=2, 
                    ensure_ascii=False,
                    sort_keys=True
                )
        except IOError as e:
            logger.error(f"Error saving file {path}: {str(e)}")
            raise
            
    def load_inputs(self) -> None:
        """Load all input JSON files into memory."""
        for key, path in self.input_paths.items():
            self.inputs[key] = self.load_json(path) or {}
            logger.info(f"Loaded input: {key} from {path}")
            
    def analyze(self) -> None:
        """Abstract method for data analysis."""
        raise NotImplementedError("Subclasses must implement analyze() method")
        
    def validate_inputs(self) -> bool:
        """Validate loaded inputs before analysis."""
        return all(self.inputs.values())
        
    def run(self) -> None:
        """Execute the complete management workflow."""
        logger.info(f"Starting {self.__class__.__name__}")
        
        self.load_inputs()
        
        if not self.validate_inputs():
            raise ValueError("Invalid inputs provided")
            
        self.analyze()
        
        self.save_json(self.output, self.output_path)
        logger.info(
            f"{self.__class__.__name__} output saved to {self.output_path}"
        )


def estimate_task_duration(task: Dict[str, Any]) -> float:
    """Estimate task duration based on complexity level."""
    if task is None:
        raise TypeError("Task cannot be None")
    if not isinstance(task, dict):
        raise TypeError("Task must be a dictionary")
        
    complexity = task.get("complexity", "medium")
    return DEFAULT_COMPLEXITY_MAPPING.get(complexity, 3.0)


def estimate_task_cost(task: Dict[str, Any]) -> float:
    """Estimate task cost based on resources and duration."""
    if task is None:
        raise TypeError("Task cannot be None")
    if not isinstance(task, dict):
        raise TypeError("Task must be a dictionary")
        
    resources = task.get("resources", 1)
    duration = estimate_task_duration(task)
    return duration * resources * DEFAULT_COST_PER_RESOURCE


def estimate_project_duration(project: Dict[str, Any]) -> float:
    """Estimate project duration by summing task durations."""
    if project is None:
        raise TypeError("Project cannot be None")
    if not isinstance(project, dict):
        raise TypeError("Project must be a dictionary")
        
    tasks = project.get("tasks", [])
    return sum(estimate_task_duration(task) for task in tasks)


def estimate_project_cost(project: Dict[str, Any]) -> float:
    """Estimate project cost by summing task costs."""
    if project is None:
        raise TypeError("Project cannot be None")
    if not isinstance(project, dict):
        raise TypeError("Project must be a dictionary")
        
    tasks = project.get("tasks", [])
    return sum(estimate_task_cost(task) for task in tasks)


class EstimationManagement(BaseManagement):
    """
    Project estimation management class with advanced estimation capabilities.
    """
    
    def __init__(self,
                 detailed_wbs_path: str = 'project_inputs/PM_JSON/user_inputs/detailed_wbs.json',
                 output_path: str = 'project_inputs/PM_JSON/system_outputs/estimation_management.json') -> None:
        input_paths = {
            'detailed_wbs': detailed_wbs_path
        }
        super().__init__(input_paths, output_path)

    def analyze(self) -> None:
        """Perform comprehensive project estimation analysis."""
        detailed_wbs = self.inputs.get('detailed_wbs', {})
        
        if not detailed_wbs:
            self.output = {
                'summary': 'No WBS data provided',
                'details': {}
            }
            return
            
        tasks = detailed_wbs.get('tasks', [])
        task_estimates = []
        
        for task in tasks:
            task_estimate = {
                'id': task.get('id'),
                'name': task.get('name'),
                'duration': estimate_task_duration(task),
                'cost': estimate_task_cost(task),
                'complexity': task.get('complexity', 'medium')
            }
            task_estimates.append(task_estimate)
        
        total_duration = sum(te['duration'] for te in task_estimates)
        total_cost = sum(te['cost'] for te in task_estimates)
        
        self.output = {
            'summary': {
                'total_tasks': len(task_estimates),
                'total_duration': total_duration,
                'total_cost': total_cost
            },
            'details': {
                'task_estimates': task_estimates
            }
        }


if __name__ == "__main__":
    manager = EstimationManagement()
    manager.run()
