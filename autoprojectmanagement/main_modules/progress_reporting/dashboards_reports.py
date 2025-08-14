#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/progress_reporting/dashboards_reports.py
File: dashboards_reports.py
Purpose: Dashboard and report generation
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Dashboard and report generation within the AutoProjectManagement system
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
Dashboard and report generation within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from .progress_calculator import ProgressCalculator

# Constants
DEFAULT_INPUT_DIR = 'JSonDataBase/Inputs/UserInputs'
MAX_IMPORTANT_TASKS = 10
MAX_URGENT_TASKS = 10
PROGRESS_THRESHOLD = 0.5
IMPORTANCE_WEIGHT = 0.6
URGENCY_WEIGHT = 0.4
SCORE_PRECISION = 2
PERCENTAGE_PRECISION = 1

# Status constants
STATUS_COMPLETED = 'completed'
STATUS_IN_PROGRESS = 'in_progress'
STATUS_PENDING = 'pending'

# Matrix quadrants
QUADRANT_URGENT_IMPORTANT = 'Urgent & Important'
QUADRANT_URGENT_NOT_IMPORTANT = 'Urgent & Not Important'
QUADRANT_NOT_URGENT_IMPORTANT = 'Not Urgent & Important'
QUADRANT_NOT_URGENT_NOT_IMPORTANT = 'Not Urgent & Not Important'


class DashboardReports:
    """
    Main dashboard reports generator for project management analytics.
    
    This class provides comprehensive reporting capabilities for project
    progress, resource allocation, cost management, and risk tracking.
    
    Attributes:
        input_dir (str): Directory path for input JSON files
        data (Dict[str, Any]): Loaded project data
        progress_calculator (ProgressCalculator): Calculator for progress metrics
        logger (logging.Logger): Logger instance for error tracking
    """
    
    def __init__(self, input_dir: str = DEFAULT_INPUT_DIR) -> None:
        """
        Initialize DashboardReports instance.
        
        Args:
            input_dir: Directory containing input JSON files
        """
        self.input_dir: str = input_dir
        self.data: Dict[str, Any] = {}
        self.progress_calculator: ProgressCalculator = ProgressCalculator(input_dir)
        self.logger: logging.Logger = logging.getLogger(__name__)
        
    def load_json_file(self, filename: str) -> Optional[Any]:
        """
        Load JSON file from specified path with error handling.
        
        Args:
            filename: Name of the JSON file to load
            
        Returns:
            Parsed JSON data or None if file cannot be loaded
            
        Raises:
            FileNotFoundError: If file does not exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        try:
            # Override to load wbs_scores.json from fixed path
            if filename == 'wbs_scores.json':
                path = Path('JSonDataBase/OutPuts/wbs_scores.json')
            else:
                path = Path(self.input_dir) / filename
                
            if not path.exists():
                self.logger.warning(f"File not found: {path}")
                return None
                
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in {filename}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error loading {filename}: {e}")
            return None
    
    def load_inputs(self) -> None:
        """
        Load all required input files and initialize data structures.
        
        This method loads all necessary JSON files including:
        - detailed_wbs.json: Work breakdown structure
        - human_resources.json: Resource information
        - resource_allocation.json: Resource assignments
        - task_resource_allocation.json: Task-resource mappings
        - wbs_scores.json: WBS scoring data
        - workflow_definition.json: Workflow definitions
        
        After loading files, it enriches tasks with progress data.
        """
        required_files = [
            'detailed_wbs.json',
            'human_resources.json',
            'resource_allocation.json',
            'task_resource_allocation.json',
            'wbs_scores.json',
            'workflow_definition.json'
        ]
        
        for filename in required_files:
            self.data[filename.replace('.json', '')] = self.load_json_file(filename)
        
        # Load and enrich task data with progress information
        self.progress_calculator.load_inputs()
        self.progress_calculator.enrich_tasks_with_progress()
        self.data['detailed_wbs'] = self.progress_calculator.get_enriched_tasks()
    
    def _format_task(self, task: Dict[str, Any]) -> str:
        """
        Format a single task for display in reports.
        
        Args:
            task: Dictionary containing task information
            
        Returns:
            Formatted string representation of the task
        """
        title = task.get('title', 'No Title')
        status = task.get('status', 'unknown')
        progress = task.get('progress', 0.0)
        progress_percent = progress * 100 if isinstance(progress, (int, float)) else 0.0
        
        importance = task.get('importance')
        urgency = task.get('urgency')
        
        if importance is not None and urgency is not None:
            score = (importance * IMPORTANCE_WEIGHT) + (urgency * URGENCY_WEIGHT)
            return (
                f"- **{title}** (Status: {status}, "
                f"Importance: {importance:.{SCORE_PRECISION}f}, "
                f"Urgency: {urgency:.{SCORE_PRECISION}f}, "
                f"Score: {score:.{SCORE_PRECISION}f}, "
                f"Progress: {progress_percent:.{PERCENTAGE_PRECISION}f}%)"
            )
        else:
            return (
                f"- **{title}** (Status: {status}, "
                f"Progress: {progress_percent:.{PERCENTAGE_PRECISION}f}%)"
            )
    
    def generate_progress_report(self) -> str:
        """
        Generate comprehensive progress report with task statistics.
        
        Returns:
            Markdown formatted string containing:
            - Total task count
            - Completed tasks count
            - In-progress tasks count
            - Pending tasks count
            - Overall progress percentage
            - Detailed task listings
        """
        tasks = self.data.get('detailed_wbs') or []
        total_tasks = len(tasks)
        
        if total_tasks == 0:
            return "# Progress Report Dashboard\n\nNo tasks found.\n"
        
        completed = sum(
            1 for t in tasks 
            if t.get('status') == STATUS_COMPLETED
        )
        in_progress = sum(
            1 for t in tasks 
            if t.get('status') == STATUS_IN_PROGRESS
        )
        pending = total_tasks - completed - in_progress
        
        progress_percent = (completed / total_tasks * 100) if total_tasks > 0 else 0.0
        
        report = f"# Progress Report Dashboard\n\n"
        report += f"- Total Tasks: {total_tasks}\n"
        report += f"- Completed: {completed}\n"
        report += f"- In Progress: {in_progress}\n"
        report += f"- Pending: {pending}\n"
        report += f"- Progress Percentage: {progress_percent:.2f}%\n\n"
        report += "## Task Details\n"
        
        for task in tasks:
            report += self._format_task(task) + "\n"
            
        return report
    
    def generate_priority_urgency_report(self) -> str:
        """
        Generate priority and urgency analysis report.
        
        Creates a comprehensive report including:
        - Top important tasks
        - Top urgent tasks
        - Eisenhower matrix categorization
        
        Returns:
            Markdown formatted string with priority analysis
        """
        tasks = self.data.get('detailed_wbs') or []
        
        if not tasks:
            return "# Task Priority and Urgency Report\n\nNo tasks found.\n"
        
        # Sort tasks by importance and urgency
        important_tasks = sorted(
            tasks, 
            key=lambda x: x.get('importance', 0.0), 
            reverse=True
        )[:MAX_IMPORTANT_TASKS]
        
        urgent_tasks = sorted(
            tasks, 
            key=lambda x: x.get('urgency', 0.0), 
            reverse=True
        )[:MAX_URGENT_TASKS]
        
        # Check for missing data
        importance_data_missing = any(
            task.get('importance') is None for task in tasks
        )
        urgency_data_missing = any(
            task.get('urgency') is None for task in tasks
        )
        
        # Create Eisenhower matrix
        matrix: Dict[str, List[Dict[str, Any]]] = {
            QUADRANT_URGENT_IMPORTANT: [],
            QUADRANT_URGENT_NOT_IMPORTANT: [],
            QUADRANT_NOT_URGENT_IMPORTANT: [],
            QUADRANT_NOT_URGENT_NOT_IMPORTANT: []
        }
        
        for task in tasks:
            urgent = task.get('urgency', 0.0) >= PROGRESS_THRESHOLD
            important = task.get('importance', 0.0) >= PROGRESS_THRESHOLD
            
            if urgent and important:
                matrix[QUADRANT_URGENT_IMPORTANT].append(task)
            elif urgent and not important:
                matrix[QUADRANT_URGENT_NOT_IMPORTANT].append(task)
            elif not urgent and important:
                matrix[QUADRANT_NOT_URGENT_IMPORTANT].append(task)
            else:
                matrix[QUADRANT_NOT_URGENT_NOT_IMPORTANT].append(task)
        
        report = "# Task Priority and Urgency Report\n\n"
        
        if importance_data_missing or urgency_data_missing:
            report += (
                "_Note: Importance and/or urgency data missing "
                "in input tasks. Report based on available data._\n\n"
            )
        
        report += "## Top 10 Important Tasks\n"
        for task in important_tasks:
            report += self._format_task(task) + "\n"
        
        report += "\n## Top 10 Urgent Tasks\n"
        for task in urgent_tasks:
            report += self._format_task(task) + "\n"
        
        report += "\n## Eisenhower Matrix\n"
        for quadrant, tasks_list in matrix.items():
            report += f"\n### {quadrant} ({len(tasks_list)} tasks)\n"
            for task in tasks_list:
                report += self._format_task(task) + "\n"
                
        return report
    
    def generate_resource_allocation_report(self) -> str:
        """
        Generate resource allocation and management report.
        
        Analyzes human resources and their allocation across tasks.
        
        Returns:
            Markdown formatted string with resource allocation details
        """
        human_resources = self.data.get('human_resources') or []
        resource_allocation = self.data.get('resource_allocation') or []
        task_resource_allocation = self.data.get('task_resource_allocation') or []
        
        allocation_summary: Dict[str, float] = {}
        
        # Calculate total allocation per resource
        for allocation in task_resource_allocation:
            resource_id = allocation.get('resource_id')
            if resource_id:
                allocation_summary[resource_id] = allocation_summary.get(
                    resource_id, 0.0
                ) + allocation.get('allocation_percent', 0.0)
        
        report = "# Resource Allocation Dashboard\n\n"
        
        if not human_resources:
            report += "## Human Resources\nNo human resources found.\n"
        else:
            report += "## Human Resources\n"
            for hr in human_resources:
                name = hr.get('name', 'Unknown')
                role = hr.get('role', 'Unknown Role')
                report += f"- {name} ({role})\n"
        
        if not allocation_summary:
            report += "\n## Resource Allocation Summary\nNo allocations found.\n"
        else:
            report += "\n## Resource Allocation Summary\n"
            for resource_id, allocation in allocation_summary.items():
                report += f"- Resource ID {resource_id}: {allocation}% allocated\n"
                
        return report
    
    def generate_cost_management_report(self) -> str:
        """
        Generate cost management and budget tracking report.
        
        Analyzes project costs based on WBS scores and resource allocation.
        
        Returns:
            Markdown formatted string with cost analysis
        """
        wbs_scores = self.data.get('wbs_scores') or []
        resource_allocation = self.data.get('resource_allocation') or []
        
        # Calculate total project cost
        total_cost = sum(
            item.get('cost', 0.0) 
            for item in wbs_scores 
            if isinstance(item, dict)
        )
        
        report = "# Cost Management Report\n\n"
        report += f"- Total Cost: {total_cost:.2f}\n\n"
        
        if not wbs_scores:
            report += "## WBS Scores\nNo WBS scores found.\n"
        else:
            report += "## WBS Scores\n"
            for item in wbs_scores:
                if isinstance(item, dict):
                    item_id = item.get('id', 'Unknown ID')
                    cost = item.get('cost', 0.0)
                    report += f"- {item_id}: Cost = {cost:.2f}\n"
                    
        return report
    
    def generate_risk_issue_tracking_report(self) -> str:
        """
        Generate risk and issue tracking report.
        
        Analyzes workflow definitions to identify risks and issues.
        
        Returns:
            Markdown formatted string with risk and issue tracking
        """
        workflow_definition = self.data.get('workflow_definition') or []
        
        if not workflow_definition:
            return "# Risk and Issue Tracking Dashboard\n\nNo workflow data found.\n"
        
        # Filter risks and issues from workflow
        risks = [
            item for item in workflow_definition 
            if item.get('type') == 'risk'
        ]
        issues = [
            item for item in workflow_definition 
            if item.get('type') == 'issue'
        ]
        
        report = "# Risk and Issue Tracking Dashboard\n\n"
        
        if not risks:
            report += "## Risks\nNo risks identified.\n"
        else:
            report += "## Risks\n"
            for risk in risks:
                description = risk.get('description', 'No description')
                report += f"- {description}\n"
        
        if not issues:
            report += "\n## Issues\nNo issues identified.\n"
        else:
            report += "\n## Issues\n"
            for issue in issues:
                description = issue.get('description', 'No description')
                report += f"- {description}\n"
                
        return report
