#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/planning_estimation/scope_management.py
File: scope_management.py
Purpose: Enhanced scope management
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Enhanced scope management within the AutoProjectManagement system
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
CURRENT_VERSION = "2.0.0"
PYTHON_MIN_VERSION = "3.8+"
CREATED_DATE = "2025-08-14"
MODIFIED_DATE = "2025-08-14"

# Module-level docstring
__doc__ = """
Enhanced scope management within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"

# Constants
DEFAULT_DETAILED_WBS_PATH = 'JSonDataBase/Inputs/UserInputs/detailed_wbs.json'
DEFAULT_SCOPE_CHANGES_PATH = 'JSonDataBase/Inputs/UserInputs/scope_changes.json'
DEFAULT_OUTPUT_PATH = 'JSonDataBase/OutPuts/scope_management.json'
ENCODING = 'utf-8'
JSON_INDENT = 2

# Scope change types
CHANGE_TYPE_ADD = 'add'
CHANGE_TYPE_REMOVE = 'remove'
CHANGE_TYPE_MODIFY = 'modify'
VALID_CHANGE_TYPES = {CHANGE_TYPE_ADD, CHANGE_TYPE_REMOVE, CHANGE_TYPE_MODIFY}


class ScopeManagementError(Exception):
    """Base exception for scope management errors."""
    pass


class InvalidScopeChangeError(ScopeManagementError):
    """Raised when an invalid scope change is detected."""
    pass


class FileNotFoundError(ScopeManagementError):
    """Raised when required files are not found."""
    pass


class ScopeManagement:
    """
    Comprehensive scope management system for project deliverables.
    
    This class handles the complete lifecycle of scope management including:
    - Loading and validating WBS data
    - Processing scope changes with impact analysis
    - Generating detailed scope management reports
    - Maintaining audit trails for all scope modifications
    
    Attributes:
        detailed_wbs_path: Path to detailed WBS JSON file
        scope_changes_path: Path to scope changes JSON file
        output_path: Path for scope management output
        detailed_wbs: Loaded WBS data structure
        scope_changes: List of scope change requests
        scope_status: Current status of scope changes
        
    Example:
        >>> manager = ScopeManagement()
        >>> manager.run()
        >>> print(manager.get_scope_summary())
    """
    
    def __init__(self,
                 detailed_wbs_path: str = DEFAULT_DETAILED_WBS_PATH,
                 scope_changes_path: str = DEFAULT_SCOPE_CHANGES_PATH,
                 output_path: str = DEFAULT_OUTPUT_PATH) -> None:
        """
        Initialize the ScopeManagement instance.
        
        Args:
            detailed_wbs_path: Path to detailed WBS JSON file
            scope_changes_path: Path to scope changes JSON file
            output_path: Path for scope management output
            
        Raises:
            ValueError: If any path is empty or invalid
        """
        if not all([detailed_wbs_path, scope_changes_path, output_path]):
            raise ValueError("All file paths must be provided")
            
        self.detailed_wbs_path = Path(detailed_wbs_path)
        self.scope_changes_path = Path(scope_changes_path)
        self.output_path = Path(output_path)
        
        self.detailed_wbs: Dict[str, Any] = {}
        self.scope_changes: List[Dict[str, Any]] = []
        self.scope_status: Dict[str, List[str]] = {
            'added_tasks': [],
            'removed_tasks': [],
            'modified_tasks': [],
            'errors': []
        }
    
    def load_json(self, path: Path) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """
        Load JSON data from file with error handling.
        
        Args:
            path: Path to JSON file
            
        Returns:
            Parsed JSON data or None if file doesn't exist
            
        Raises:
            FileNotFoundError: If file exists but cannot be read
            json.JSONDecodeError: If file contains invalid JSON
        """
        try:
            if path.exists():
                with open(path, 'r', encoding=ENCODING) as f:
                    return json.load(f)
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {path}: {e}")
            raise ScopeManagementError(f"Invalid JSON format in {path}")
        except Exception as e:
            logger.error(f"Error reading {path}: {e}")
            raise FileNotFoundError(f"Cannot read file: {path}")
    
    def save_json(self, data: Union[Dict[str, Any], List[Any]], path: Path) -> None:
        """
        Save data to JSON file with proper formatting.
        
        Args:
            data: Data to save (dict or list)
            path: Output file path
            
        Raises:
            ScopeManagementError: If file cannot be written
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding=ENCODING) as f:
                json.dump(data, f, indent=JSON_INDENT, ensure_ascii=False)
            logger.info(f"Saved JSON data to {path}")
        except Exception as e:
            logger.error(f"Error saving JSON to {path}: {e}")
            raise ScopeManagementError(f"Cannot write file: {path}")
    
    def load_inputs(self) -> None:
        """Load and validate input files."""
        logger.info("Loading scope management inputs...")
        
        self.detailed_wbs = self.load_json(self.detailed_wbs_path) or {}
        self.scope_changes = self.load_json(self.scope_changes_path) or []
        
        if not isinstance(self.scope_changes, list):
            raise InvalidScopeChangeError("Scope changes must be a list")
    
    def validate_scope_change(self, change: Dict[str, Any]) -> bool:
        """
        Validate a scope change request.
        
        Args:
            change: Scope change dictionary
            
        Returns:
            True if valid
            
        Raises:
            InvalidScopeChangeError: If change is invalid
        """
        required_keys = {'task_id', 'change_type', 'details'}
        if not all(key in change for key in required_keys):
            raise InvalidScopeChangeError(
                f"Missing required keys: {required_keys - set(change.keys())}"
            )
        
        change_type = change.get('change_type')
        if change_type not in VALID_CHANGE_TYPES:
            raise InvalidScopeChangeError(
                f"Invalid change type: {change_type}. Must be one of {VALID_CHANGE_TYPES}"
            )
        
        return True
    
    def apply_scope_changes(self) -> None:
        """
        Apply validated scope changes to the detailed WBS.
        
        This method processes all scope changes and applies them to the WBS
        structure while maintaining data integrity and generating audit trails.
        """
        logger.info("Applying scope changes...")
        
        self.scope_status = {
            'added_tasks': [],
            'removed_tasks': [],
            'modified_tasks': [],
            'errors': []
        }
        
        for change in self.scope_changes:
            try:
                self.validate_scope_change(change)
                self._process_single_change(change)
            except Exception as e:
                error_msg = f"Error processing change {change}: {e}"
                logger.error(error_msg)
                self.scope_status['errors'].append(error_msg)
    
    def _process_single_change(self, change: Dict[str, Any]) -> None:
        """Process a single validated scope change."""
        task_id = change['task_id']
        change_type = change['change_type']
        details = change['details']
        
        if change_type == CHANGE_TYPE_ADD:
            self._process_add_change(task_id, details)
        elif change_type == CHANGE_TYPE_REMOVE:
            self._process_remove_change(task_id)
        elif change_type == CHANGE_TYPE_MODIFY:
            self._process_modify_change(task_id, details)
    
    def _process_add_change(self, task_id: str, details: Dict[str, Any]) -> None:
        """Process an 'add' type scope change."""
        parent_id = details.get('parent_id')
        new_task = details.get('task')
        
        if parent_id and new_task:
            parent_task = self.find_task_by_id(parent_id)
            if parent_task is not None:
                if 'subtasks' not in parent_task:
                    parent_task['subtasks'] = []
                parent_task['subtasks'].append(new_task)
                self.scope_status['added_tasks'].append(new_task.get('id', ''))
                logger.info(f"Added task {new_task.get('id')} under parent {parent_id}")
    
    def _process_remove_change(self, task_id: str) -> None:
        """Process a 'remove' type scope change."""
        removed = self.remove_task_by_id(task_id)
        if removed:
            self.scope_status['removed_tasks'].append(task_id)
            logger.info(f"Removed task {task_id}")
    
    def _process_modify_change(self, task_id: str, details: Dict[str, Any]) -> None:
        """Process a 'modify' type scope change."""
        task = self.find_task_by_id(task_id)
        if task:
            task.update(details)
            self.scope_status['modified_tasks'].append(task_id)
            logger.info(f"Modified task {task_id}")
    
    def find_task_by_id(self, task_id: Union[str, int], node: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Recursively find a task by its ID."""
        if node is None:
            node = self.detailed_wbs
        if not node:
            return None
        if node.get('id') == task_id:
            return node
        for subtask in node.get('subtasks', []):
            found = self.find_task_by_id(task_id, subtask)
            if found:
                return found
        return None
    
    def remove_task_by_id(self, task_id: Union[str, int], node: Optional[Dict[str, Any]] = None) -> bool:
        """Recursively remove a task by its ID."""
        if node is None:
            node = self.detailed_wbs
        if not node or 'subtasks' not in node:
            return False
        for i, subtask in enumerate(node['subtasks']):
            if subtask.get('id') == task_id:
                del node['subtasks'][i]
                return True
            if self.remove_task_by_id(task_id, subtask):
                return True
        return False
    
    def get_scope_summary(self) -> Dict[str, Any]:
        """Get a summary of the current scope management status."""
        return {
            'total_tasks_added': len(self.scope_status['added_tasks']),
            'total_tasks_removed': len(self.scope_status['removed_tasks']),
            'total_tasks_modified': len(self.scope_status['modified_tasks']),
            'total_errors': len(self.scope_status['errors']),
            'added_tasks': self.scope_status['added_tasks'],
            'removed_tasks': self.scope_status['removed_tasks'],
            'modified_tasks': self.scope_status['modified_tasks'],
            'errors': self.scope_status['errors']
        }
    
    def analyze_scope_change_impact(self, change: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the impact of a scope change on related tasks and dependencies.
        
        Args:
            change: Scope change dictionary
            
        Returns:
            Dictionary containing impact analysis results
        """
        impact_analysis = {
            'change_id': change.get('task_id', 'unknown'),
            'change_type': change.get('change_type', 'unknown'),
            'affected_tasks': [],
            'dependency_changes': [],
            'schedule_impact': 0,
            'cost_impact': 0,
            'resource_impact': 0,
            'risk_level': 'low',
            'recommendations': []
        }
        
        task_id = change.get('task_id')
        change_type = change.get('change_type')
        details = change.get('details', {})
        
        # Find affected tasks based on dependencies
        affected_tasks = self._find_affected_tasks(task_id)
        impact_analysis['affected_tasks'] = affected_tasks
        
        # Calculate schedule impact
        schedule_impact = self._calculate_schedule_impact(task_id, change_type, details)
        impact_analysis['schedule_impact'] = schedule_impact
        
        # Calculate cost impact
        cost_impact = self._calculate_cost_impact(task_id, change_type, details)
        impact_analysis['cost_impact'] = cost_impact
        
        # Calculate resource impact
        resource_impact = self._calculate_resource_impact(task_id, change_type, details)
        impact_analysis['resource_impact'] = resource_impact
        
        # Determine risk level
        risk_level = self._determine_risk_level(schedule_impact, cost_impact, resource_impact)
        impact_analysis['risk_level'] = risk_level
        
        # Generate recommendations
        recommendations = self._generate_impact_recommendations(change_type, impact_analysis)
        impact_analysis['recommendations'] = recommendations
        
        return impact_analysis
    
    def _find_affected_tasks(self, task_id: str) -> List[str]:
        """Find tasks that depend on or are affected by the given task."""
        affected_tasks = []
        
        # Build dependency mapping from WBS structure
        dependencies = self._build_dependency_mapping()
        
        # Find tasks that depend on this task
        if task_id in dependencies:
            affected_tasks.extend(dependencies[task_id])
        
        # Find tasks that this task depends on (reverse dependencies)
        reverse_deps = self._build_reverse_dependency_mapping()
        if task_id in reverse_deps:
            affected_tasks.extend(reverse_deps[task_id])
        
        # Remove duplicates and return
        return list(set(affected_tasks))
    
    def _build_dependency_mapping(self) -> Dict[str, List[str]]:
        """Build a mapping of task dependencies from the WBS structure."""
        dependencies = {}
        
        def process_node(node: Dict[str, Any], parent_id: Optional[str] = None):
            if 'id' in node:
                task_id = node['id']
                
                # Add dependency on parent if exists
                if parent_id:
                    if task_id not in dependencies:
                        dependencies[task_id] = []
                    dependencies[task_id].append(parent_id)
                
                # Process dependencies from task metadata
                if 'dependencies' in node and isinstance(node['dependencies'], list):
                    if task_id not in dependencies:
                        dependencies[task_id] = []
                    dependencies[task_id].extend(node['dependencies'])
            
            # Process subtasks recursively
            if 'subtasks' in node and isinstance(node['subtasks'], list):
                for subtask in node['subtasks']:
                    process_node(subtask, node.get('id'))
        
        process_node(self.detailed_wbs)
        return dependencies
    
    def _build_reverse_dependency_mapping(self) -> Dict[str, List[str]]:
        """Build reverse dependency mapping (which tasks depend on each task)."""
        dependencies = self._build_dependency_mapping()
        reverse_deps = {}
        
        for task_id, deps in dependencies.items():
            for dep in deps:
                if dep not in reverse_deps:
                    reverse_deps[dep] = []
                reverse_deps[dep].append(task_id)
        
        return reverse_deps
    
    def _calculate_schedule_impact(self, task_id: str, change_type: str, details: Dict[str, Any]) -> int:
        """Calculate the schedule impact of a scope change."""
        # Placeholder implementation
        # In a real system, this would analyze task dependencies and critical path
        if change_type == CHANGE_TYPE_ADD:
            return 2  # days added
        elif change_type == CHANGE_TYPE_REMOVE:
            return -1  # days saved
        elif change_type == CHANGE_TYPE_MODIFY:
            return 1   # days added for modifications
        return 0
    
    def _calculate_cost_impact(self, task_id: str, change_type: str, details: Dict[str, Any]) -> float:
        """Calculate the cost impact of a scope change."""
        # Placeholder implementation
        if change_type == CHANGE_TYPE_ADD:
            return 1000.0  # additional cost
        elif change_type == CHANGE_TYPE_REMOVE:
            return -500.0  # cost savings
        elif change_type == CHANGE_TYPE_MODIFY:
            return 200.0   # modification cost
        return 0.0
    
    def _calculate_resource_impact(self, task_id: str, change_type: str, details: Dict[str, Any]) -> int:
        """Calculate the resource impact of a scope change."""
        # Placeholder implementation
        if change_type == CHANGE_TYPE_ADD:
            return 2  # additional resources needed
        elif change_type == CHANGE_TYPE_REMOVE:
            return -1  # resources freed
        elif change_type == CHANGE_TYPE_MODIFY:
            return 1   # resource adjustment
        return 0
    
    def _determine_risk_level(self, schedule_impact: int, cost_impact: float, resource_impact: int) -> str:
        """Determine the risk level based on impact analysis."""
        total_impact = abs(schedule_impact) + abs(cost_impact) + abs(resource_impact)
        
        if total_impact > 10:
            return 'high'
        elif total_impact > 5:
            return 'medium'
        else:
            return 'low'
    
    def _generate_impact_recommendations(self, change_type: str, impact_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on impact analysis."""
        recommendations = []
        
        if impact_analysis['risk_level'] == 'high':
            recommendations.append("High impact change - requires management approval")
            recommendations.append("Consider phased implementation to mitigate risks")
        
        if impact_analysis['schedule_impact'] > 3:
            recommendations.append("Significant schedule impact - review project timeline")
        
        if impact_analysis['cost_impact'] > 1000:
            recommendations.append("Major cost impact - budget review required")
        
        if impact_analysis['resource_impact'] > 2:
            recommendations.append("Resource allocation needs adjustment")
        
        return recommendations
    
    def process_scope_change_approval(self, change: Dict[str, Any], 
                                    impact_analysis: Dict[str, Any],
                                    approver: str = "system") -> Dict[str, Any]:
        """
        Process scope change approval workflow.
        
        Args:
            change: Scope change dictionary
            impact_analysis: Impact analysis results
            approver: Name of the approver (default: "system")
            
        Returns:
            Dictionary containing approval status and details
        """
        approval_result = {
            'change_id': change.get('task_id'),
            'approver': approver,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending',
            'comments': [],
            'conditions': []
        }
        
        # Automatic approval for low-risk changes
        if impact_analysis['risk_level'] == 'low':
            approval_result['status'] = 'approved'
            approval_result['comments'].append("Automatically approved - low risk impact")
        
        # Require management approval for medium/high risk changes
        elif impact_analysis['risk_level'] in ['medium', 'high']:
            approval_result['status'] = 'requires_approval'
            approval_result['comments'].append(f"Requires management approval - {impact_analysis['risk_level']} risk")
            
            # Add approval conditions based on impact
            if impact_analysis['schedule_impact'] > 3:
                approval_result['conditions'].append("Schedule impact review required")
            if impact_analysis['cost_impact'] > 1000:
                approval_result['conditions'].append("Budget approval required")
            if impact_analysis['resource_impact'] > 2:
                approval_result['conditions'].append("Resource allocation approval required")
        
        return approval_result
    
    def approve_scope_change(self, change_id: str, approver: str, 
                           comments: str = "") -> bool:
        """
        Approve a scope change.
        
        Args:
            change_id: ID of the change to approve
            approver: Name of the approver
            comments: Optional approval comments
            
        Returns:
            True if approved successfully, False otherwise
        """
        # Find the change in scope changes
        for change in self.scope_changes:
            if change.get('task_id') == change_id:
                if 'approval_status' not in change:
                    change['approval_status'] = {}
                change['approval_status']['status'] = 'approved'
                change['approval_status']['approver'] = approver
                change['approval_status']['timestamp'] = datetime.now().isoformat()
                if comments:
                    change['approval_status']['comments'] = comments
                logger.info(f"Change {change_id} approved by {approver}")
                return True
        
        logger.warning(f"Change {change_id} not found for approval")
        return False
    
    def reject_scope_change(self, change_id: str, approver: str, 
                          reason: str) -> bool:
        """
        Reject a scope change.
        
        Args:
            change_id: ID of the change to reject
            approver: Name of the approver
            reason: Reason for rejection
            
        Returns:
            True if rejected successfully, False otherwise
        """
        # Find the change in scope changes
        for change in self.scope_changes:
            if change.get('task_id') == change_id:
                if 'approval_status' not in change:
                    change['approval_status'] = {}
                change['approval_status']['status'] = 'rejected'
                change['approval_status']['approver'] = approver
                change['approval_status']['timestamp'] = datetime.now().isoformat()
                change['approval_status']['reason'] = reason
                logger.info(f"Change {change_id} rejected by {approver}: {reason}")
                return True
        
        logger.warning(f"Change {change_id} not found for rejection")
        return False
    
    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        """
        Get list of scope changes pending approval.
        
        Returns:
            List of changes requiring approval
        """
        pending_changes = []
        
        for change in self.scope_changes:
            approval_status = change.get('approval_status', {})
            if approval_status.get('status') == 'requires_approval':
                pending_changes.append(change)
        
        return pending_changes
    
    def run(self) -> None:
        """Run the complete scope management process."""
        logger.info("Starting scope management process...")
        self.load_inputs()
        
        # Perform impact analysis for each scope change
        impact_analyses = []
        approval_results = []
        
        for change in self.scope_changes:
            try:
                impact_analysis = self.analyze_scope_change_impact(change)
                impact_analyses.append(impact_analysis)
                
                # Process approval workflow
                approval_result = self.process_scope_change_approval(change, impact_analysis)
                approval_results.append(approval_result)
                
                logger.info(f"Change {change.get('task_id')}: {impact_analysis['risk_level']} risk - {approval_result['status']}")
                
            except Exception as e:
                logger.error(f"Error processing change {change.get('task_id')}: {e}")
        
        # Apply only approved changes
        approved_changes = [change for change in self.scope_changes 
                          if change.get('approval_status', {}).get('status') == 'approved']
        
        if approved_changes:
            self.scope_changes = approved_changes
            self.apply_scope_changes()
            logger.info(f"Applied {len(approved_changes)} approved scope changes")
        else:
            logger.info("No approved scope changes to apply")
        
        # Save comprehensive output including approvals
        output_data = {
            'detailed_wbs': self.detailed_wbs,
            'scope_changes': self.scope_changes,
            'impact_analyses': impact_analyses,
            'approval_results': approval_results,
            'summary': self.get_scope_summary(),
            'pending_approvals': self.get_pending_approvals(),
            'timestamp': datetime.now().isoformat()
        }
        
        self.save_json(output_data, self.output_path)
        
        summary = self.get_scope_summary()
        pending_count = len(output_data['pending_approvals'])
        
        logger.info(f"Scope management completed: {summary}")
        print(f"Scope management output saved to {self.output_path}")
        print(f"Summary: {summary}")
        print(f"Impact analyses completed for {len(impact_analyses)} changes")
        print(f"Pending approvals: {pending_count} changes require management approval")
        
        if pending_count > 0:
            print("\nChanges requiring approval:")
            for change in output_data['pending_approvals']:
                print(f"  - {change.get('task_id')}: {change.get('approval_status', {}).get('conditions', [])}")

if __name__ == "__main__":
    manager = ScopeManagement()
    manager.run()
