"""
Database Data Collector Module

This module provides functionality for collecting and storing project management data
from various sources into JSON files for further processing and analysis.

Author: AutoProjectManagement Team
Version: 2.0.0
"""

import json
import datetime
import logging
import os
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

from ..utility_modules.feature_weights import URGENCY_FEATURE_WEIGHTS, IMPORTANCE_FEATURE_WEIGHTS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_DATA_DIR = 'SystemInputs/user_inputs'
ENCODING = 'utf-8'
JSON_INDENT = 4


class DBDataCollector:
    """
    A comprehensive data collector for project management data.
    
    This class provides methods to collect, validate, and store various types
    of project management data including tasks, resource allocation, progress
    metrics, and feature weights.
    
    Attributes:
        data_dir (str): Directory path for storing JSON files
        tasks_file (str): Path to tasks JSON file
        resource_allocation_file (str): Path to resource allocation JSON file
        progress_metrics_file (str): Path to progress metrics JSON file
        feature_weights_file (str): Path to feature weights JSON file
    """
    
    def __init__(self, data_dir: str = DEFAULT_DATA_DIR) -> None:
        """
        Initialize the Database Data Collector.
        
        Args:
            data_dir: Directory path for storing JSON files.
                     Defaults to 'SystemInputs/user_inputs'
        
        Raises:
            ValueError: If data_dir is empty or None
            OSError: If directory creation fails
        """
        if not data_dir:
            raise ValueError("data_dir cannot be empty or None")
            
        self.data_dir = data_dir
        self._ensure_directory_exists()
        
        # Initialize file paths
        self.tasks_file = os.path.join(self.data_dir, 'tasks.json')
        self.resource_allocation_file = os.path.join(self.data_dir, 'resource_allocation.json')
        self.progress_metrics_file = os.path.join(self.data_dir, 'progress_metrics.json')
        self.feature_weights_file = os.path.join(self.data_dir, 'feature_weights.json')
        
        logger.info(f"DBDataCollector initialized with data_dir: {self.data_dir}")
    
    def _ensure_directory_exists(self) -> None:
        """Ensure the data directory exists, create if it doesn't."""
        try:
            Path(self.data_dir).mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directory ensured: {self.data_dir}")
        except OSError as e:
            logger.error(f"Failed to create directory {self.data_dir}: {e}")
            raise
    
    def _validate_tasks(self, tasks: List[Any]) -> bool:
        """
        Validate the tasks list for data integrity.
        
        Args:
            tasks: List of task objects to validate
            
        Returns:
            bool: True if all tasks are valid, False otherwise
        """
        if not isinstance(tasks, list):
            logger.error("Tasks must be a list")
            return False
            
        if not tasks:
            logger.warning("Empty tasks list provided")
            return True
            
        for i, task in enumerate(tasks):
            if not hasattr(task, '__dict__'):
                logger.error(f"Task at index {i} does not have __dict__ attribute")
                return False
                
        return True
    
    def _write_json_file(self, file_path: str, data: Any) -> bool:
        """
        Write data to a JSON file with error handling.
        
        Args:
            file_path: Path to the JSON file
            data: Data to write
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file_path, 'w', encoding=ENCODING) as f:
                json.dump(data, f, indent=JSON_INDENT, ensure_ascii=False)
            logger.info(f"Successfully wrote data to {file_path}")
            return True
        except (IOError, OSError, json.JSONEncodeError) as e:
            logger.error(f"Failed to write to {file_path}: {e}")
            return False
    
    def collect_and_store_tasks(self, tasks: List[Any]) -> bool:
        """
        Collect task data including progress, resource allocation, and store in JSON file.
        
        This method serializes task objects to JSON format and stores them in the
        designated tasks file. It includes validation and error handling.
        
        Args:
            tasks: List of task objects to collect and store
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            >>> collector = DBDataCollector()
            >>> tasks = [task1, task2, task3]
            >>> success = collector.collect_and_store_tasks(tasks)
            >>> if success:
            ...     print("Tasks successfully stored")
        """
        if not self._validate_tasks(tasks):
            return False
            
        try:
            tasks_data = [task.__dict__ for task in tasks]
            return self._write_json_file(self.tasks_file, tasks_data)
        except Exception as e:
            logger.error(f"Error collecting tasks: {e}")
            return False
    
    def collect_resource_allocation(self, tasks: List[Any]) -> bool:
        """
        Analyze resource allocation and store summary in JSON file.
        
        This method analyzes how resources (team members) are allocated across
        tasks and creates a summary of resource usage.
        
        Args:
            tasks: List of task objects to analyze
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            >>> collector = DBDataCollector()
            >>> tasks = [task1, task2]  # tasks with assigned_to attribute
            >>> success = collector.collect_resource_allocation(tasks)
        """
        if not self._validate_tasks(tasks):
            return False
            
        try:
            resource_usage: Dict[str, int] = {}
            
            for task in tasks:
                if hasattr(task, 'assigned_to') and task.assigned_to:
                    for user in task.assigned_to:
                        if isinstance(user, str):
                            resource_usage[user] = resource_usage.get(user, 0) + 1
                        else:
                            logger.warning(f"Invalid user type: {type(user)}")
            
            return self._write_json_file(self.resource_allocation_file, resource_usage)
            
        except Exception as e:
            logger.error(f"Error collecting resource allocation: {e}")
            return False
    
    def collect_progress_metrics(self, tasks: List[Any]) -> bool:
        """
        Collect progress percentages and store/update in JSON file.
        
        This method extracts progress metrics from tasks and stores them in a
        structured format for analysis and reporting.
        
        Args:
            tasks: List of task objects to collect progress from
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            >>> collector = DBDataCollector()
            >>> tasks = [task1, task2]  # tasks with workflow_progress_percentage method
            >>> success = collector.collect_progress_metrics(tasks)
        """
        if not self._validate_tasks(tasks):
            return False
            
        try:
            progress_data: Dict[str, Union[float, int]] = {}
            
            for task in tasks:
                if hasattr(task, 'id') and hasattr(task, 'workflow_progress_percentage'):
                    try:
                        progress = task.workflow_progress_percentage()
                        if isinstance(progress, (int, float)) and 0 <= progress <= 100:
                            progress_data[task.id] = progress
                        else:
                            logger.warning(f"Invalid progress value for task {task.id}: {progress}")
                    except Exception as e:
                        logger.error(f"Error getting progress for task {task.id}: {e}")
                else:
                    logger.warning(f"Task missing required attributes: {type(task)}")
            
            return self._write_json_file(self.progress_metrics_file, progress_data)
            
        except Exception as e:
            logger.error(f"Error collecting progress metrics: {e}")
            return False
    
    def insert_feature_weights(self, urgency_weights: Dict[str, float], 
                              importance_weights: Dict[str, float]) -> bool:
        """
        Insert predefined weights for urgency and importance features into JSON file.
        
        This method stores feature weights used for calculating task priorities
        and urgency/importance scores.
        
        Args:
            urgency_weights: Dictionary of urgency feature weights
            importance_weights: Dictionary of importance feature weights
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            >>> collector = DBDataCollector()
            >>> urgency = {'deadline': 0.4, 'priority': 0.6}
            >>> importance = {'impact': 0.5, 'effort': 0.5}
            >>> success = collector.insert_feature_weights(urgency, importance)
        """
        try:
            if not isinstance(urgency_weights, dict) or not isinstance(importance_weights, dict):
                logger.error("Weights must be dictionaries")
                return False
                
            # Validate weight values
            for weights_dict, name in [(urgency_weights, "urgency"), (importance_weights, "importance")]:
                for key, value in weights_dict.items():
                    if not isinstance(value, (int, float)) or not 0 <= value <= 1:
                        logger.error(f"Invalid {name} weight for {key}: {value}")
                        return False
            
            weights = {
                'urgency_weights': urgency_weights,
                'importance_weights': importance_weights,
                'metadata': {
                    'created_at': str(datetime.now()),
                    'version': '1.0.0'
                }
            }
            
            return self._write_json_file(self.feature_weights_file, weights)
            
        except Exception as e:
            logger.error(f"Error inserting feature weights: {e}")
            return False
    
    def get_collected_data(self, data_type: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve previously collected data from JSON files.
        
        Args:
            data_type: Type of data to retrieve ('tasks', 'resource_allocation', 
                      'progress_metrics', 'feature_weights')
        
        Returns:
            Optional[Dict[str, Any]]: The collected data or None if file doesn't exist
            
        Example:
            >>> collector = DBDataCollector()
            >>> tasks = collector.get_collected_data('tasks')
            >>> if tasks:
            ...     print(f"Found {len(tasks)} tasks")
        """
        file_mapping = {
            'tasks': self.tasks_file,
            'resource_allocation': self.resource_allocation_file,
            'progress_metrics': self.progress_metrics_file,
            'feature_weights': self.feature_weights_file
        }
        
        if data_type not in file_mapping:
            logger.error(f"Invalid data type: {data_type}")
            return None
            
        file_path = file_mapping[data_type]
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding=ENCODING) as f:
                    return json.load(f)
            else:
                logger.warning(f"File not found: {file_path}")
                return None
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error reading {file_path}: {e}")
            return None
    
    def close(self) -> None:
        """
        Clean up resources and close any open connections.
        
        This method ensures proper cleanup of resources when the collector
        is no longer needed.
        """
        logger.info("DBDataCollector closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.close()
        if exc_type:
            logger.error(f"Exception occurred: {exc_val}")
        return False
