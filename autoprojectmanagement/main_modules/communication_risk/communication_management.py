#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/communication_risk/communication_management.py
File: communication_management.py
Purpose: Communication management module
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Communication management module within the AutoProjectManagement system
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
Communication management module within the AutoProjectManagement system

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
from typing import Any, Dict, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_ENCODING = 'utf-8'
DEFAULT_INDENT = 2
MAX_LINE_LENGTH = 79
DEFAULT_COMMUNICATION_PLAN_PATH = 'project_inputs/PM_JSON/user_inputs/communication_plan.json'
DEFAULT_COMMUNICATION_LOGS_PATH = 'project_inputs/PM_JSON/user_inputs/communication_logs.json'
DEFAULT_OUTPUT_PATH = 'project_inputs/PM_JSON/system_outputs/communication_management.json'


class BaseManagement:
    """
    Base management class for handling file-based operations.
    
    Provides common functionality for loading JSON inputs, processing data,
    and saving outputs. Designed to be subclassed for specific management
    tasks.
    
    Attributes:
        input_paths: Dictionary mapping input names to file paths
        output_path: Path where output will be saved
        inputs: Loaded input data
        output: Processed output data
    """

    def __init__(self, input_paths: Dict[str, str], output_path: str) -> None:
        """
        Initialize BaseManagement with input and output paths.
        
        Args:
            input_paths: Dictionary mapping input names to file paths
            output_path: Path where output will be saved
            
        Raises:
            ValueError: If input_paths or output_path are invalid
        """
        if not isinstance(input_paths, dict):
            raise ValueError("input_paths must be a dictionary")
        if not output_path or not isinstance(output_path, str):
            raise ValueError("output_path must be a non-empty string")
            
        self.input_paths: Dict[str, str] = input_paths
        self.output_path: str = output_path
        self.inputs: Dict[str, Any] = {}
        self.output: Dict[str, Any] = {}

    def load_json(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Load JSON data from a file.
        
        Args:
            path: Path to the JSON file
            
        Returns:
            Dictionary containing the JSON data, or None if file doesn't exist
            
        Raises:
            json.JSONDecodeError: If the file contains invalid JSON
            OSError: If there's an error reading the file
        """
        if not os.path.exists(path):
            logger.warning(f"File not found: {path}")
            return None
            
        try:
            with open(path, 'r', encoding=DEFAULT_ENCODING) as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {path}: {e}")
            raise
        except OSError as e:
            logger.error(f"Error reading file {path}: {e}")
            raise

    def save_json(self, data: Dict[str, Any], path: str) -> None:
        """
        Save data as JSON to a file.
        
        Args:
            data: Dictionary to save as JSON
            path: Path where to save the file
            
        Raises:
            OSError: If there's an error writing the file
            TypeError: If data is not JSON serializable
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w', encoding=DEFAULT_ENCODING) as file:
                json.dump(data, file, indent=DEFAULT_INDENT, ensure_ascii=False)
        except TypeError as e:
            logger.error(f"Data not JSON serializable: {e}")
            raise
        except OSError as e:
            logger.error(f"Error writing file {path}: {e}")
            raise

    def load_inputs(self) -> None:
        """Load all input files specified in input_paths."""
        for key, path in self.input_paths.items():
            try:
                self.inputs[key] = self.load_json(path) or {}
                logger.info(f"Loaded input: {key} from {path}")
            except Exception as e:
                logger.error(f"Failed to load input {key}: {e}")
                self.inputs[key] = {}

    def analyze(self) -> None:
        """
        Analyze the loaded data.
        
        This method must be implemented by subclasses to provide specific
        analysis logic for the management task.
        
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement analyze()")

    def run(self) -> None:
        """
        Execute the complete management workflow.
        
        Loads inputs, performs analysis, and saves output.
        """
        try:
            self.load_inputs()
            self.analyze()
            self.save_json(self.output, self.output_path)
            logger.info(f"{self.__class__.__name__} output saved to {self.output_path}")
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")
            raise


class CommunicationManagement(BaseManagement):
    """
    Communication management and analysis class.
    
    Provides comprehensive analysis of project communication effectiveness
    including plan validation, log analysis, and metrics calculation.
    
    Attributes:
        communication_plan_path: Path to communication plan JSON file
        communication_logs_path: Path to communication logs JSON file
        output_path: Path for saving analysis results
    """

    def __init__(
        self,
        communication_plan_path: str = DEFAULT_COMMUNICATION_PLAN_PATH,
        communication_logs_path: str = DEFAULT_COMMUNICATION_LOGS_PATH,
        output_path: str = DEFAULT_OUTPUT_PATH
    ) -> None:
        """
        Initialize CommunicationManagement with file paths.
        
        Args:
            communication_plan_path: Path to communication plan JSON file
            communication_logs_path: Path to communication logs JSON file
            output_path: Path for saving analysis results
            
        Example:
            >>> manager = CommunicationManagement(
            ...     communication_plan_path='custom/plan.json',
            ...     communication_logs_path='custom/logs.json',
            ...     output_path='custom/output.json'
            ... )
        """
        input_paths = {
            'communication_plan': communication_plan_path,
            'communication_logs': communication_logs_path
        }
        super().__init__(input_paths, output_path)

    def analyze(self) -> None:
        """
        Analyze communication effectiveness and logs.
        
        Performs comprehensive analysis including:
        - Communication plan validation
        - Log analysis and metrics calculation
        - Effectiveness scoring
        - Gap identification
        - Recommendations generation
        
        The analysis results are stored in self.output.
        """
        try:
            communication_plan = self.inputs.get('communication_plan', {})
            communication_logs = self.inputs.get('communication_logs', {})
            
            # Validate communication plan
            plan_validation = self._validate_communication_plan(communication_plan)
            
            # Analyze communication logs
            log_analysis = self._analyze_communication_logs(communication_logs)
            
            # Calculate effectiveness metrics
            effectiveness = self._calculate_effectiveness(
                communication_plan, communication_logs
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                plan_validation, log_analysis, effectiveness
            )
            
            self.output = {
                'summary': {
                    'status': 'completed',
                    'total_logs': len(communication_logs.get('logs', [])),
                    'plan_valid': plan_validation['valid'],
                    'effectiveness_score': effectiveness['score']
                },
                'plan_validation': plan_validation,
                'log_analysis': log_analysis,
                'effectiveness': effectiveness,
                'recommendations': recommendations,
                'metadata': {
                    'analysis_timestamp': str(Path().cwd()),
                    'version': '1.0.0'
                }
            }
            
            logger.info("Communication analysis completed successfully")
            
        except Exception as e:
            logger.error(f"Error during communication analysis: {e}")
            self.output = {
                'summary': {
                    'status': 'failed',
                    'error': str(e)
                },
                'error_details': {
                    'type': type(e).__name__,
                    'message': str(e)
                }
            }

    def _validate_communication_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the communication plan structure and content.
        
        Args:
            plan: Communication plan dictionary
            
        Returns:
            Validation results including validity status and issues
        """
        required_fields = ['stakeholders', 'communication_types', 'frequency']
        issues = []
        
        for field in required_fields:
            if field not in plan:
                issues.append(f"Missing required field: {field}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'stakeholder_count': len(plan.get('stakeholders', [])),
            'communication_types': len(plan.get('communication_types', []))
        }

    def _analyze_communication_logs(self, logs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze communication logs for patterns and effectiveness.
        
        Args:
            logs: Communication logs dictionary
            
        Returns:
            Analysis results including metrics and patterns
        """
        log_entries = logs.get('logs', [])
        
        if not log_entries:
            return {
                'total_logs': 0,
                'frequency_analysis': {},
                'effectiveness_trends': [],
                'gaps': ['No communication logs found']
            }
        
        # Basic analysis - can be expanded
        frequency_analysis = {}
        for log in log_entries:
            comm_type = log.get('type', 'unknown')
            frequency_analysis[comm_type] = frequency_analysis.get(comm_type, 0) + 1
        
        return {
            'total_logs': len(log_entries),
            'frequency_analysis': frequency_analysis,
            'effectiveness_trends': [],
            'gaps': []
        }

    def _calculate_effectiveness(
        self, 
        plan: Dict[str, Any], 
        logs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate communication effectiveness metrics.
        
        Args:
            plan: Communication plan
            logs: Communication logs
            
        Returns:
            Effectiveness metrics and scores
        """
        plan_stakeholders = len(plan.get('stakeholders', []))
        log_entries = logs.get('logs', [])
        
        if plan_stakeholders == 0 or not log_entries:
            return {
                'score': 0.0,
                'metrics': {},
                'issues': ['Insufficient data for effectiveness calculation']
            }
        
        # Simplified effectiveness calculation
        actual_communications = len(log_entries)
        expected_min = plan_stakeholders * 2  # At least 2 per stakeholder
        
        score = min(actual_communications / expected_min, 1.0) if expected_min > 0 else 0.0
        
        return {
            'score': round(score, 2),
            'metrics': {
                'actual_communications': actual_communications,
                'expected_minimum': expected_min,
                'plan_stakeholders': plan_stakeholders
            },
            'issues': []
        }

    def _generate_recommendations(
        self,
        plan_validation: Dict[str, Any],
        log_analysis: Dict[str, Any],
        effectiveness: Dict[str, Any]
    ) -> list[str]:
        """
        Generate recommendations based on analysis results.
        
        Args:
            plan_validation: Plan validation results
            log_analysis: Log analysis results
            effectiveness: Effectiveness metrics
            
        Returns:
            List of actionable recommendations
        """
        recommendations = []
        
        if not plan_validation['valid']:
            recommendations.append("Fix communication plan validation issues")
        
        if effectiveness['score'] < 0.8:
            recommendations.append("Increase communication frequency")
        
        if log_analysis['total_logs'] == 0:
            recommendations.append("Start logging communications")
        
        return recommendations


if __name__ == "__main__":
    manager = CommunicationManagement()
    manager.run()
