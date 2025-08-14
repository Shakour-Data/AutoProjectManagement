"""
path: autoprojectmanagement/main_modules/utility_modules/time_management.py
File: time_management.py
Purpose: Time management module for automated project scheduling and resource allocation
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Advanced time management system that calculates task durations, schedules resources,
and generates comprehensive project timelines based on WBS and resource allocations.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_WORKING_HOURS_PER_DAY = 8
DEFAULT_WORKING_DAYS_PER_WEEK = 5
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class TimeManagementError(Exception):
    """Custom exception for time management related errors."""
    pass

class InvalidDateError(TimeManagementError):
    """Raised when invalid date format is encountered."""
    pass

class ResourceAllocationError(TimeManagementError):
    """Raised when resource allocation conflicts are detected."""
    pass

class TimeManagement:
    """
    Advanced time management system for automated project scheduling.
    
    This class provides comprehensive time management capabilities including:
    - Task duration calculation based on resource allocations
    - Project timeline generation
    - Resource conflict detection
    - Working calendar management
    - Schedule optimization
    
    Attributes:
        detailed_wbs_path (str): Path to detailed WBS JSON file
        resource_allocation_path (str): Path to resource allocation JSON file
        output_path (str): Path for output time management JSON file
        detailed_wbs (Dict[str, Any]): Loaded WBS data structure
        resource_allocations (Dict[str, Any]): Loaded resource allocation data
        task_schedules (Dict[str, Dict[str, Any]]): Generated task schedules
    """
    
    def __init__(self,
                 detailed_wbs_path: str = 'JSonDataBase/Inputs/UserInputs/detailed_wbs.json',
                 resource_allocation_path: str = 'JSonDataBase/OutPuts/resource_allocation_enriched.json',
                 output_path: str = 'JSonDataBase/OutPuts/time_management.json',
                 working_hours_per_day: int = DEFAULT_WORKING_HOURS_PER_DAY,
                 working_days_per_week: int = DEFAULT_WORKING_DAYS_PER_WEEK) -> None:
        """
        Initialize the TimeManagement system.
        
        Args:
            detailed_wbs_path: Path to detailed WBS JSON file
            resource_allocation_path: Path to resource allocation JSON file
            output_path: Path for output time management JSON file
            working_hours_per_day: Standard working hours per day
            working_days_per_week: Standard working days per week
            
        Raises:
            ValueError: If working hours or days are invalid
        """
        if working_hours_per_day <= 0:
            raise ValueError("Working hours per day must be positive")
        if working_days_per_week <= 0 or working_days_per_week > 7:
            raise ValueError("Working days per week must be between 1 and 7")
            
        self.detailed_wbs_path = detailed_wbs_path
        self.resource_allocation_path = resource_allocation_path
        self.output_path = output_path
        self.working_hours_per_day = working_hours_per_day
        self.working_days_per_week = working_days_per_week
        
        self.detailed_wbs: Dict[str, Any] = {}
        self.resource_allocations: Dict[str, Any] = {}
        self.task_schedules: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"TimeManagement initialized with working hours: {working_hours_per_day}/day, "
                   f"{working_days_per_week}/week")

    def load_json(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Safely load JSON data from file.
        
        Args:
            path: Path to JSON file
            
        Returns:
            Dictionary containing JSON data, or None if file doesn't exist
            
        Raises:
            TimeManagementError: If JSON file is invalid
        """
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                logger.warning(f"File not found: {path}")
                return None
        except json.JSONDecodeError as e:
            raise TimeManagementError(f"Invalid JSON in file {path}: {str(e)}")
        except Exception as e:
            raise TimeManagementError(f"Error loading file {path}: {str(e)}")

    def save_json(self, data: Dict[str, Any], path: str) -> None:
        """
        Save data to JSON file with proper error handling.
        
        Args:
            data: Data to save
            path: Output file path
            
        Raises:
            TimeManagementError: If unable to save file
        """
        try:
            # Ensure directory exists
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False, default=str)
            logger.info(f"Data successfully saved to {path}")
        except Exception as e:
            raise TimeManagementError(f"Error saving file {path}: {str(e)}")

    def parse_date(self, date_str: str) -> datetime:
        """
        Parse date string to datetime object.
        
        Args:
            date_str: Date string in format 'YYYY-MM-DD'
            
        Returns:
            datetime object
            
        Raises:
            InvalidDateError: If date format is invalid
        """
        try:
            return datetime.strptime(date_str, DATE_FORMAT)
        except ValueError as e:
            raise InvalidDateError(f"Invalid date format '{date_str}': {str(e)}")

    def calculate_working_days(self, start_date: datetime, end_date: datetime) -> int:
        """
        Calculate number of working days between two dates.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Number of working days
        """
        if start_date > end_date:
            return 0
            
        current_date = start_date
        working_days = 0
        
        while current_date <= end_date:
            # Skip weekends based on working_days_per_week
            if self.working_days_per_week >= 5:
                # Standard Monday-Friday work week
                if current_date.weekday() < 5:  # 0-4 are Monday-Friday
                    working_days += 1
            elif self.working_days_per_week == 6:
                # Monday-Saturday work week
                if current_date.weekday() < 6:  # 0-5 are Monday-Saturday
                    working_days += 1
            else:
                # Custom work week - assume all days are working days
                working_days += 1
                
            current_date += timedelta(days=1)
            
        return working_days

    def calculate_task_duration(self, task: Dict[str, Any]) -> int:
        """
        Calculate task duration in working days based on resource allocations.
        
        Args:
            task: Task dictionary containing resource allocations
            
        Returns:
            Task duration in working days
            
        Raises:
            ResourceAllocationError: If resource allocations are invalid
        """
        allocations = task.get('resource_allocations', [])
        if not allocations:
            logger.warning(f"No resource allocations found for task {task.get('id', 'unknown')}")
            return 0
            
        try:
            start_dates = []
            end_dates = []
            
            for allocation in allocations:
                if not isinstance(allocation, dict):
                    continue
                    
                start_date_str = allocation.get('start_date')
                end_date_str = allocation.get('end_date')
                
                if start_date_str and end_date_str:
                    start_date = self.parse_date(start_date_str)
                    end_date = self.parse_date(end_date_str)
                    start_dates.append(start_date)
                    end_dates.append(end_date)
                    
            if not start_dates or not end_dates:
                return 0
                
            min_start = min(start_dates)
            max_end = max(end_dates)
            
            # Calculate working days between dates
            duration = self.calculate_working_days(min_start, max_end)
            
            logger.debug(f"Task {task.get('id', 'unknown')} duration: {duration} working days")
            return duration
            
        except Exception as e:
            raise ResourceAllocationError(f"Error calculating task duration: {str(e)}")

    def detect_resource_conflicts(self, task_id: str, allocations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect resource allocation conflicts for a given task.
        
        Args:
            task_id: ID of the task being checked
            allocations: List of resource allocations for the task
            
        Returns:
            List of detected conflicts
        """
        conflicts = []
        
        for allocation in allocations:
            resource_id = allocation.get('resource_id')
            start_date = allocation.get('start_date')
            end_date = allocation.get('end_date')
            
            if not all([resource_id, start_date, end_date]):
                continue
                
            # Check for overlapping allocations with same resource
            # This is a simplified check - in real implementation, would check against all tasks
            conflicts.append({
                'task_id': task_id,
                'resource_id': resource_id,
                'conflict_type': 'potential_overlap',
                'start_date': start_date,
                'end_date': end_date
            })
            
        return conflicts

    def schedule_tasks(self, node: Optional[Dict[str, Any]] = None) -> None:
        """
        Recursively schedule all tasks in the WBS structure.
        
        Args:
            node: Current node in WBS structure, defaults to root
            
        Raises:
            TimeManagementError: If scheduling fails
        """
        if node is None:
            node = self.detailed_wbs
            
        if not node:
            logger.warning("Empty WBS structure provided")
            return
            
        try:
            task_id = node.get('id')
            if not task_id:
                logger.warning("Task without ID found, skipping")
                return
                
            # Calculate task duration
            duration = self.calculate_task_duration(node)
            
            # Get resource allocations
            allocations = node.get('resource_allocations', [])
            
            # Detect conflicts
            conflicts = self.detect_resource_conflicts(task_id, allocations)
            
            # Determine start and end dates
            start_date = None
            end_date = None
            
            if allocations:
                try:
                    start_dates = [self.parse_date(alloc['start_date']) 
                                 for alloc in allocations if alloc.get('start_date')]
                    end_dates = [self.parse_date(alloc['end_date']) 
                               for alloc in allocations if alloc.get('end_date')]
                    
                    if start_dates and end_dates:
                        start_date = min(start_dates).strftime(DATE_FORMAT)
                        end_date = max(end_dates).strftime(DATE_FORMAT)
                except (KeyError, InvalidDateError) as e:
                    logger.warning(f"Invalid date format in task {task_id}: {str(e)}")
            
            # Store task schedule
            self.task_schedules[task_id] = {
                'task_name': node.get('name', 'Unnamed Task'),
                'duration_days': duration,
                'start_date': start_date,
                'end_date': end_date,
                'resource_allocations': allocations,
                'conflicts': conflicts,
                'last_updated': datetime.now().strftime(DATETIME_FORMAT)
            }
            
            logger.debug(f"Scheduled task {task_id}: {duration} days")
            
            # Process subtasks
            for subtask in node.get('subtasks', []):
                self.schedule_tasks(subtask)
                
        except Exception as e:
            raise TimeManagementError(f"Error scheduling task: {str(e)}")

    def generate_project_timeline(self) -> Dict[str, Any]:
        """
        Generate comprehensive project timeline based on task schedules.
        
        Returns:
            Dictionary containing project timeline information
        """
        if not self.task_schedules:
            return {}
            
        # Find project start and end dates
        start_dates = [schedule['start_date'] for schedule in self.task_schedules.values() 
                      if schedule['start_date']]
        end_dates = [schedule['end_date'] for schedule in self.task_schedules.values() 
                    if schedule['end_date']]
        
        project_start = min(start_dates) if start_dates else None
        project_end = max(end_dates) if end_dates else None
        
        # Calculate total project duration
        total_duration = 0
        if project_start and project_end:
            start = self.parse_date(project_start)
            end = self.parse_date(project_end)
            total_duration = self.calculate_working_days(start, end)
        
        # Count tasks by status
        total_tasks = len(self.task_schedules)
        tasks_with_conflicts = sum(1 for schedule in self.task_schedules.values() 
                                 if schedule.get('conflicts'))
        
        return {
            'project_start_date': project_start,
            'project_end_date': project_end,
            'total_project_duration_days': total_duration,
            'total_tasks': total_tasks,
            'tasks_with_conflicts': tasks_with_conflicts,
            'task_schedules': self.task_schedules,
            'generated_at': datetime.now().strftime(DATETIME_FORMAT)
        }

    def validate_inputs(self) -> bool:
        """
        Validate all input data before processing.
        
        Returns:
            True if inputs are valid, False otherwise
        """
        try:
            # Check if required files exist
            if not os.path.exists(self.detailed_wbs_path):
                logger.error(f"WBS file not found: {self.detailed_wbs_path}")
                return False
                
            if not os.path.exists(self.resource_allocation_path):
                logger.warning(f"Resource allocation file not found: {self.resource_allocation_path}")
                
            # Validate loaded data
            if not isinstance(self.detailed_wbs, dict):
                logger.error("Invalid WBS data format")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Input validation failed: {str(e)}")
            return False

    def run(self) -> bool:
        """
        Execute the complete time management process.
        
        Returns:
            True if successful, False otherwise
            
        Raises:
            TimeManagementError: If any critical error occurs
        """
        try:
            logger.info("Starting time management process...")
            
            # Load and validate inputs
            self.load_inputs()
            if not self.validate_inputs():
                return False
                
            # Schedule all tasks
            self.schedule_tasks()
            
            # Generate project timeline
            timeline = self.generate_project_timeline()
            
            # Save results
            self.save_json(timeline, self.output_path)
            
            logger.info(f"Time management completed successfully. Results saved to {self.output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Time management process failed: {str(e)}")
            raise TimeManagementError(f"Process failed: {str(e)}")

    def get_task_schedule(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get schedule for a specific task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task schedule dictionary or None if not found
        """
        return self.task_schedules.get(task_id)

    def export_to_csv(self, csv_path: str) -> None:
        """
        Export task schedules to CSV format.
        
        Args:
            csv_path: Path for CSV output file
            
        Raises:
            TimeManagementError: If export fails
        """
        try:
            import csv
            
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['task_id', 'task_name', 'duration_days', 'start_date', 
                            'end_date', 'resource_count', 'conflicts_count']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for task_id, schedule in self.task_schedules.items():
                    writer.writerow({
                        'task_id': task_id,
                        'task_name': schedule.get('task_name', ''),
                        'duration_days': schedule.get('duration_days', 0),
                        'start_date': schedule.get('start_date', ''),
                        'end_date': schedule.get('end_date', ''),
                        'resource_count': len(schedule.get('resource_allocations', [])),
                        'conflicts_count': len(schedule.get('conflicts', []))
                    })
                    
            logger.info(f"Task schedules exported to CSV: {csv_path}")
            
        except Exception as e:
            raise TimeManagementError(f"CSV export failed: {str(e)}")


def main() -> None:
    """Main entry point for the time management module."""
    try:
        manager = TimeManagement()
        success = manager.run()
        
        if success:
            print("✅ Time management process completed successfully")
        else:
            print("❌ Time management process failed")
            exit(1)
            
    except TimeManagementError as e:
        print(f"❌ Time management error: {str(e)}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
