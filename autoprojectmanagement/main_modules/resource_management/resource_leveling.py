"""
Resource leveling module for AutoProjectManagement.

This module provides functionality for leveling resources across tasks
to ensure optimal resource allocation without conflicts.
"""

import json
import logging
from collections import defaultdict
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResourceLeveler:
    """
    A class to handle resource leveling for project tasks.
    
    This class loads task and allocation data, flattens nested task structures,
    and performs resource leveling to prevent resource conflicts.
    """

    def __init__(self, tasks_filepath: str, allocations_filepath: str, 
                 output_filepath: str, duration_type: str = 'normal') -> None:
        """
        Initialize the ResourceLeveler with file paths and configuration.
        
        Args:
            tasks_filepath: Path to the tasks JSON file
            allocations_filepath: Path to the allocations JSON file
            output_filepath: Path where the leveled schedule will be saved
            duration_type: Type of duration to use ('optimistic', 'normal', 'pessimistic')
        """
        if duration_type not in ['optimistic', 'normal', 'pessimistic']:
            raise ValueError("duration_type must be 'optimistic', 'normal', or 'pessimistic'")
            
        self.tasks_filepath = tasks_filepath
        self.allocations_filepath = allocations_filepath
        self.output_filepath = output_filepath
        self.duration_type = duration_type
        self.tasks: List[Dict[str, Any]] = []
        self.allocations: List[Dict[str, Any]] = []
        self.flat_tasks: List[Dict[str, Any]] = []
        self.task_map: Dict[str, Dict[str, Any]] = {}
        self.task_schedules: Dict[str, Dict[str, Any]] = {}

    def load_json_file(self, filepath: str) -> Dict[str, Any]:
        """Load and return JSON data from the specified file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Successfully loaded JSON from {filepath}")
                return data
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {filepath}: {e}")
            raise

    def save_json_file(self, data: Dict[str, Any], filepath: str) -> None:
        """Save JSON data to the specified file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                logger.info(f"Successfully saved JSON to {filepath}")
        except IOError as e:
            logger.error(f"Unable to write to file {filepath}: {e}")
            raise

    def flatten_tasks(self, tasks: List[Dict[str, Any]], 
                    parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Flatten nested tasks into a list with parent-child relationships.
        
        Args:
            tasks: List of task dictionaries
            parent_id: ID of the parent task (None for root tasks)
            
        Returns:
            List of flattened task dictionaries
        """
        flat_list = []
        for task in tasks:
            task_copy = task.copy()
            task_copy['parent_id'] = parent_id
            subtasks = task_copy.pop('subtasks', [])
            flat_list.append(task_copy)
            flat_list.extend(self.flatten_tasks(subtasks, task_copy['id']))
        return flat_list

    def resource_leveling(self) -> Dict[str, Dict[str, Any]]:
        """
        Perform resource leveling to prevent resource conflicts.
        
        This algorithm ensures that tasks assigned to the same resource
        do not overlap in time by adjusting their start times.
        
        Returns:
            Dictionary mapping task IDs to their scheduled times
        """
        # Map task_id to task details for quick lookup
        self.task_map = {task['id']: task for task in self.flat_tasks}

        # Map resource_id to list of assigned tasks
        resource_tasks = defaultdict(list)
        for alloc in self.allocations:
            resource_id = alloc.get('role', 'unknown')
            resource_tasks[resource_id].append(alloc['task_id'])

        # Process each resource's tasks sequentially
        for resource_id, task_ids in resource_tasks.items():
            current_time = 0
            for tid in task_ids:
                task = self.task_map.get(tid)
                if not task:
                    logger.warning(f"Task {tid} not found in task map, skipping")
                    continue
                
                duration = task.get(f'{self.duration_type}_hours', 1)
                if duration <= 0:
                    logger.warning(f"Invalid duration {duration} for task {tid}, using 1 hour")
                    duration = 1
                
                start = current_time
                end = start + duration
                
                # Store the schedule for this task
                self.task_schedules[tid] = {
                    'resource_id': resource_id,
                    'start': start,
                    'end': end
                }
                
                current_time = end

        return self.task_schedules

    def run(self) -> None:
        """Execute the complete resource leveling process."""
        try:
            logger.info("Starting resource leveling process")
            
            # Load input data
            self.tasks = self.load_json_file(self.tasks_filepath)
            self.allocations = self.load_json_file(self.allocations_filepath)
            
            # Process data
            self.flat_tasks = self.flatten_tasks(self.tasks)
            logger.info(f"Flattened {len(self.flat_tasks)} tasks from hierarchy")
            
            leveled_schedule = self.resource_leveling()
            logger.info(f"Generated schedule for {len(leveled_schedule)} tasks")
            
            # Save results
            self.save_json_file(leveled_schedule, self.output_filepath)
            logger.info(f"Resource leveling completed. Output saved to {self.output_filepath}")
            
        except Exception as e:
            logger.error(f"Error during resource leveling: {e}")
            raise

    @staticmethod
    def main() -> None:
        """Entry point for running the resource leveler."""
        tasks_filepath = 'projects/current_project/docs/detailed_wbs.json'
        allocations_filepath = 'projects/current_project/docs/task_resource_allocation.json'
        output_filepath = 'projects/current_project/docs/leveled_resource_schedule.json'

        leveler = ResourceLeveler(tasks_filepath, allocations_filepath, output_filepath)
        leveler.run()

if __name__ == '__main__':
    ResourceLeveler.main()
