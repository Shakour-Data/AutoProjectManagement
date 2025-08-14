#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/planning_estimation/wbs_merger.py
File: wbs_merger.py
Purpose: WBS merging functionality
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: WBS merging functionality within the AutoProjectManagement system
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
WBS merging functionality within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_PARTS_DIR = 'SystemInputs/user_inputs/wbs_parts'
DEFAULT_OUTPUT_FILE = 'SystemInputs/system_generated/detailed_wbs.json'
MAX_FILE_SIZE_MB = 10
SUPPORTED_FILE_EXTENSIONS = {'.json'}
ENCODING = 'utf-8'


class WBSMergerError(Exception):
    """Base exception for WBS Merger errors."""
    pass


class FileNotFoundError(WBSMergerError):
    """Raised when a required file is not found."""
    pass


class InvalidWBSError(WBSMergerError):
    """Raised when WBS data is invalid or malformed."""
    pass


class WBSMerger:
    """
    Merges multiple WBS (Work Breakdown Structure) parts into a single detailed WBS.
    
    This class provides functionality to load, validate, and merge multiple WBS parts
    into a comprehensive structure. It handles hierarchical relationships between tasks
    and subtasks while preserving all metadata and attributes.
    
    Attributes:
        parts_dir: Directory containing WBS part files
        output_file: Path for the merged WBS output
        max_file_size_mb: Maximum allowed file size in MB
        
    Example:
        >>> merger = WBSMerger(
        ...     parts_dir='custom_parts',
        ...     output_file='merged_wbs.json'
        ... )
        >>> result = merger.merge_all_parts()
        >>> print(f"Successfully merged {len(result.get('subtasks', []))} tasks")
    """
    
    def __init__(
        self,
        parts_dir: str = DEFAULT_PARTS_DIR,
        output_file: str = DEFAULT_OUTPUT_FILE,
        max_file_size_mb: int = MAX_FILE_SIZE_MB
    ) -> None:
        """
        Initialize WBS Merger with configuration parameters.
        
        Args:
            parts_dir: Directory containing WBS part files (default: 'SystemInputs/user_inputs/wbs_parts')
            output_file: Output file path for merged WBS (default: 'SystemInputs/system_generated/detailed_wbs.json')
            max_file_size_mb: Maximum file size in MB (default: 10)
            
        Raises:
            ValueError: If parts_dir or output_file is empty
            FileNotFoundError: If parts_dir doesn't exist
        """
        if not parts_dir:
            raise ValueError("parts_dir cannot be empty")
        if not output_file:
            raise ValueError("output_file cannot be empty")
            
        self.parts_dir = Path(parts_dir)
        self.output_file = Path(output_file)
        self.max_file_size_mb = max_file_size_mb
        
        # Validate parts directory exists
        if not self.parts_dir.exists():
            raise FileNotFoundError(f"WBS parts directory not found: {self.parts_dir}")
            
        # Ensure output directory exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(
            f"Initialized WBSMerger with parts_dir={self.parts_dir}, "
            f"output_file={self.output_file}"
        )
    
    def load_part(self, filename: str) -> Dict[str, Any]:
        """
        Load a single WBS part from JSON file with validation.
        
        Args:
            filename: Name of the WBS part file to load
            
        Returns:
            Dictionary containing validated WBS part data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            InvalidWBSError: If file is invalid JSON or exceeds size limit
        """
        filepath = self.parts_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"WBS part file not found: {filepath}")
            
        # Check file size
        file_size_mb = filepath.stat().st_size / (1024 * 1024)
        if file_size_mb > self.max_file_size_mb:
            raise InvalidWBSError(
                f"File {filename} exceeds maximum size of {self.max_file_size_mb}MB"
            )
            
        try:
            with open(filepath, 'r', encoding=ENCODING) as file:
                data = json.load(file)
                
            # Basic validation
            if not isinstance(data, dict):
                raise InvalidWBSError(f"Invalid WBS format in {filename}: expected dictionary")
                
            logger.debug(f"Successfully loaded WBS part: {filename}")
            return data
            
        except json.JSONDecodeError as e:
            raise InvalidWBSError(f"Invalid JSON in file {filename}: {e}")
        except Exception as e:
            raise WBSMergerError(f"Error loading file {filename}: {e}")
    
    def merge_subtasks(
        self,
        base_subtasks: List[Dict[str, Any]],
        additional_subtasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Recursively merge subtasks from additional subtasks into base subtasks.
        
        This method handles merging of hierarchical task structures, preserving
        relationships and updating existing tasks with new information.
        
        Args:
            base_subtasks: Base subtasks to merge into
            additional_subtasks: Additional subtasks to merge
            
        Returns:
            Merged list of subtasks with updated hierarchy
            
        Example:
            >>> merger = WBSMerger()
            >>> merged = merger.merge_subtasks(
            ...     [{'id': 1, 'name': 'Task1', 'subtasks': []}],
            ...     [{'id': 2, 'name': 'Task2', 'subtasks': []}]
            ... )
            >>> len(merged)
            2
        """
        if not isinstance(base_subtasks, list) or not isinstance(additional_subtasks, list):
            raise InvalidWBSError("Subtasks must be provided as lists")
            
        merged = base_subtasks.copy()
        task_lookup = {task['id']: task for task in merged}
        
        for additional_task in additional_subtasks:
            if not isinstance(additional_task, dict):
                logger.warning(f"Skipping invalid task: {additional_task}")
                continue
                
            task_id = additional_task.get('id')
            if not task_id:
                logger.warning(f"Skipping task without ID: {additional_task}")
                continue
                
            if task_id in task_lookup:
                # Update existing task
                existing_task = task_lookup[task_id]
                
                # Preserve existing subtasks
                existing_subtasks = existing_task.get('subtasks', [])
                
                # Update task attributes
                existing_task.update(additional_task)
                
                # Recursively merge subtasks
                additional_subtasks_list = additional_task.get('subtasks', [])
                if additional_subtasks_list:
                    existing_task['subtasks'] = self.merge_subtasks(
                        existing_subtasks,
                        additional_subtasks_list
                    )
            else:
                # Add new task
                merged.append(additional_task)
        
        return merged
    
    def validate_wbs_structure(self, wbs_data: Dict[str, Any]) -> bool:
        """
        Validate the structure and content of WBS data.
        
        Args:
            wbs_data: WBS data to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            InvalidWBSError: If validation fails
        """
        if not isinstance(wbs_data, dict):
            raise InvalidWBSError("WBS data must be a dictionary")
            
        required_keys = {'id', 'name', 'level', 'subtasks'}
        missing_keys = required_keys - set(wbs_data.keys())
        if missing_keys:
            raise InvalidWBSError(f"Missing required keys: {missing_keys}")
            
        if not isinstance(wbs_data.get('subtasks'), list):
            raise InvalidWBSError("subtasks must be a list")
            
        return True
    
    def merge_all_parts(self) -> Dict[str, Any]:
        """
        Merge all WBS parts into a single comprehensive WBS structure.
        
        This method orchestrates the complete merging process by:
        1. Discovering all WBS part files
        2. Loading and validating each part
        3. Merging all parts hierarchically
        4. Saving the merged result
        
        Returns:
            Dictionary containing the complete merged WBS
            
        Raises:
            WBSMergerError: If any part of the process fails
            
        Example:
            >>> merger = WBSMerger()
            >>> merged = merger.merge_all_parts()
            >>> print(f"Merged {len(merged.get('subtasks', []))} top-level tasks")
        """
        logger.info("Starting WBS merging process")
        
        # Initialize merged structure
        merged_wbs = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [],
            "metadata": {
                "merged_at": None,
                "parts_count": 0,
                "total_tasks": 0
            }
        }
        
        # Get all WBS part files
        wbs_files = [
            f for f in self.parts_dir.iterdir()
            if f.suffix.lower() in SUPPORTED_FILE_EXTENSIONS
        ]
        
        if not wbs_files:
            logger.warning("No WBS parts found in directory")
            return merged_wbs
        
        logger.info(f"Found {len(wbs_files)} WBS parts to merge")
        
        # Load and merge all parts
        for filepath in wbs_files:
            try:
                part = self.load_part(filepath.name)
                self.validate_wbs_structure(part)
                
                if 'subtasks' in part:
                    merged_wbs['subtasks'] = self.merge_subtasks(
                        merged_wbs['subtasks'],
                        part['subtasks']
                    )
                
                merged_wbs['metadata']['parts_count'] += 1
                logger.debug(f"Successfully merged part: {filepath.name}")
                
            except (FileNotFoundError, InvalidWBSError) as e:
                logger.error(f"Skipping invalid part {filepath.name}: {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error processing {filepath.name}: {e}")
                continue
        
        # Update metadata
        from datetime import datetime
        merged_wbs['metadata']['merged_at'] = datetime.now().isoformat()
        
        # Count total tasks recursively
        def count_tasks(tasks: List[Dict[str, Any]]) -> int:
            count = len(tasks)
            for task in tasks:
                count += count_tasks(task.get('subtasks', []))
            return count
        
        merged_wbs['metadata']['total_tasks'] = count_tasks(merged_wbs['subtasks'])
        
        # Save merged WBS
        try:
            with open(self.output_file, 'w', encoding=ENCODING) as f:
                json.dump(merged_wbs, f, indent=2, ensure_ascii=False)
            logger.info(f"Merged detailed WBS saved to {self.output_file}")
        except Exception as e:
            raise WBSMergerError(f"Failed to save merged WBS: {e}")
        
        return merged_wbs
    
    def get_merge_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the last merge operation.
        
        Returns:
            Dictionary with merge statistics
            
        Example:
            >>> merger = WBSMerger()
            >>> merger.merge_all_parts()
            >>> summary = merger.get_merge_summary()
            >>> print(f"Merged {summary['total_tasks']} tasks from {summary['parts_count']} parts")
        """
        if not self.output_file.exists():
            return {
                'status': 'no_merge',
                'message': 'No merge operation performed yet'
            }
            
        try:
            with open(self.output_file, 'r', encoding=ENCODING) as f:
                merged_wbs = json.load(f)
                
            return {
                'status': 'success',
                'parts_count': merged_wbs.get('metadata', {}).get('parts_count', 0),
                'total_tasks': merged_wbs.get('metadata', {}).get('total_tasks', 0),
                'output_file': str(self.output_file),
                'merged_at': merged_wbs.get('metadata', {}).get('merged_at')
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }


# Convenience functions for direct usage
def merge_wbs_parts(
    parts_dir: str = DEFAULT_PARTS_DIR,
    output_file: str = DEFAULT_OUTPUT_FILE
) -> Dict[str, Any]:
    """
    Convenience function to merge WBS parts without instantiating the class.
    
    Args:
        parts_dir: Directory containing WBS parts
        output_file: Output file path
        
    Returns:
        Merged WBS dictionary
        
    Example:
        >>> merged = merge_wbs_parts('my_parts', 'merged.json')
        >>> print(f"Created WBS with {len(merged.get('subtasks', []))} tasks")
    """
    merger = WBSMerger(parts_dir=parts_dir, output_file=output_file)
    return merger.merge_all_parts()


if __name__ == "__main__":
    # Example usage when run directly
    try:
        merger = WBSMerger()
        result = merger.merge_all_parts()
        summary = merger.get_merge_summary()
        print(json.dumps(summary, indent=2))
    except Exception as e:
        logger.error(f"Failed to merge WBS parts: {e}")
        exit(1)
