#!/usr/bin/env python3
"""
Resource Management Module for AutoProjectManagement System.

This module provides comprehensive resource management capabilities including:
- Resource allocation and tracking
- Resource leveling and optimization
- Resource utilization analysis
- Conflict resolution for resource constraints

Classes:
    BaseManagement: Base class for management operations
    ResourceManagement: Main resource management implementation

Usage:
    >>> from autoprojectmanagement.main_modules.resource_management.resource_management import ResourceManagement
    >>> manager = ResourceManagement()
    >>> manager.run()
    ResourceManagement output saved to JSonDataBase/OutPuts/resource_management.json

Author: AutoProjectManagement Team
Version: 2.0.0
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

# Constants
DEFAULT_ENCODING = 'utf-8'
RESOURCE_ALLOCATION_PATH = 'JSonDataBase/OutPuts/resource_allocation_enriched.json'
OUTPUT_PATH = 'JSonDataBase/OutPuts/resource_management.json'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Configure logging
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class BaseManagement:
    """
    Base class for management operations in AutoProjectManagement.

    This class provides common functionality for loading inputs, processing data,
    and saving outputs. It serves as a foundation for specialized management
    classes.

    Attributes:
        input_paths (Dict[str, str]): Mapping of input names to file paths
        output_path (str): Path where output will be saved
        inputs (Dict[str, Any]): Loaded input data
        output (Dict[str, Any]): Processed output data
    """

    def __init__(self, input_paths: Dict[str, str], output_path: str) -> None:
        """
        Initialize BaseManagement with configurable paths.

        Args:
            input_paths: Dictionary mapping input names to file paths
            output_path: Path where output JSON will be saved

        Raises:
            ValueError: If input_paths is empty or output_path is invalid
        """
        if not input_paths:
            raise ValueError("input_paths cannot be empty")
        if not output_path:
            raise ValueError("output_path cannot be empty")

        self.input_paths: Dict[str, str] = input_paths
        self.output_path: str = output_path
        self.inputs: Dict[str, Any] = {}
        self.output: Dict[str, Any] = {}

    def load_json(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Load JSON data from specified file path.

        Args:
            path: Path to the JSON file to load

        Returns:
            Dictionary containing the loaded JSON data, or None if file doesn't exist
        """
        try:
            file_path = Path(path)
            if file_path.exists():
                with open(file_path, 'r', encoding=DEFAULT_ENCODING) as file:
                    return json.load(file)
            else:
                logger.warning(f"File not found: {path}")
                return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {path}: {e}")
            raise
        except PermissionError as e:
            logger.error(f"Permission denied reading file {path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading file {path}: {e}")
            raise

    def save_json(self, data: Dict[str, Any], path: str) -> None:
        """
        Save data to JSON file with proper formatting.

        Args:
            data: Dictionary to save as JSON
            path: Path where JSON file will be saved
        """
        try:
            file_path = Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding=DEFAULT_ENCODING) as file:
                json.dump(
                    data, 
                    file, 
                    indent=2, 
                    ensure_ascii=False,
                    sort_keys=True
                )
            logger.info(f"Data successfully saved to {path}")
        except PermissionError as e:
            logger.error(f"Permission denied writing file {path}: {e}")
            raise
        except OSError as e:
            logger.error(f"OS error saving file {path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error saving file {path}: {e}")
            raise

    def load_inputs(self) -> None:
        """Load all input files specified in input_paths."""
        for key, path in self.input_paths.items():
            try:
                self.inputs[key] = self.load_json(path) or {}
                logger.info(f"Successfully loaded input: {key}")
            except Exception as e:
                logger.error(f"Error loading input {key} from {path}: {e}")
                self.inputs[key] = {}

    def analyze(self) -> None:
        """Abstract method for data analysis to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the analyze method")

    def run(self) -> None:
        """Execute the complete management process."""
        try:
            logger.info(f"Starting {self.__class__.__name__}")
            self.load_inputs()
            self.analyze()
            self.save_json(self.output, self.output_path)
            logger.info(
                f"{self.__class__.__name__} output saved to {self.output_path}"
            )
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")
            raise


class ResourceManagement(BaseManagement):
    """
    Main resource management implementation for AutoProjectManagement.

    This class provides comprehensive resource management including:
    - Resource allocation analysis
    - Resource leveling optimization
    - Utilization tracking
    - Conflict detection and resolution
    """

    def __init__(
        self,
        resource_allocation_path: str = RESOURCE_ALLOCATION_PATH,
        output_path: str = OUTPUT_PATH
    ) -> None:
        """
        Initialize ResourceManagement with configurable paths.

        Args:
            resource_allocation_path: Path to resource allocation JSON file
            output_path: Path where management results will be saved
        """
        input_paths = {
            'resource_allocations': resource_allocation_path
        }
        super().__init__(input_paths, output_path)

    def analyze(self) -> None:
        """
        Perform comprehensive resource management analysis.

        This method analyzes resource allocations, identifies conflicts,
        calculates utilization rates, and generates optimization
        recommendations.
        """
        try:
            resource_data = self.inputs.get('resource_allocations', {})
            
            if not resource_data:
                logger.warning("No resource allocation data found")
                self.output = {
                    'summary': 'No resource data available',
                    'details': {},
                    'timestamp': datetime.now().isoformat(),
                    'status': 'error'
                }
                return

            # Perform detailed analysis
            utilization_analysis = self.analyze_resource_utilization(resource_data)
            conflicts = self.resolve_conflicts(resource_data)
            recommendations = self.generate_recommendations(
                resource_data, 
                utilization_analysis, 
                conflicts
            )

            self.output = {
                'summary': 'Resource management analysis completed',
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'utilization_analysis': utilization_analysis,
                'conflicts': conflicts,
                'recommendations': recommendations,
                'resource_count': len(resource_data.get('resources', [])),
                'allocation_count': len(resource_data.get('allocations', []))
            }

            logger.info("Resource management analysis completed successfully")

        except Exception as e:
            logger.error(f"Error during resource analysis: {e}")
            self.output = {
                'summary': f'Resource analysis failed: {str(e)}',
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'details': {}
            }
            raise

    def analyze_resource_utilization(
        self, 
        resource_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze resource utilization patterns and efficiency."""
        resources = resource_data.get('resources', [])
        allocations = resource_data.get('allocations', [])

        if not resources or not allocations:
            return {
                'overall_utilization': 0.0,
                'resource_utilization': {},
                'efficiency_score': 0.0,
                'analysis': 'No data available for analysis'
            }

        # Calculate utilization metrics
        resource_utilization = {}
        total_capacity = 0
        total_allocated = 0

        for resource in resources:
            resource_id = resource.get('id')
            capacity = resource.get('capacity', 0)
            allocated = sum(
                alloc.get('hours', 0) 
                for alloc in allocations 
                if alloc.get('resource_id') == resource_id
            )

            utilization_rate = (allocated / capacity * 100) if capacity > 0 else 0
            resource_utilization[resource_id] = {
                'capacity': capacity,
                'allocated': allocated,
                'utilization_rate': utilization_rate,
                'status': 'overallocated' if utilization_rate > 100 else
                         'optimal' if 80 <= utilization_rate <= 100 else
                         'underutilized'
            }

            total_capacity += capacity
            total_allocated += allocated

        overall_utilization = (
            total_allocated / total_capacity * 100 if total_capacity > 0 else 0
        )

        # Calculate efficiency score
        efficiency_score = self.calculate_efficiency_score(resource_utilization)

        return {
            'overall_utilization': overall_utilization,
            'resource_utilization': resource_utilization,
            'efficiency_score': efficiency_score,
            'analysis': self.generate_utilization_analysis(resource_utilization)
        }

    def resolve_conflicts(
        self, 
        resource_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Detect and resolve resource allocation conflicts."""
        allocations = resource_data.get('allocations', [])
        conflicts = {
            'total_conflicts': 0,
            'conflict_details': [],
            'resolutions': []
        }

        # Group allocations by resource and time period
        resource_allocations = {}
        for allocation in allocations:
            resource_id = allocation.get('resource_id')
            start_date = allocation.get('start_date')
            end_date = allocation.get('end_date')
            hours = allocation.get('hours', 0)

            if resource_id not in resource_allocations:
                resource_allocations[resource_id] = []

            resource_allocations[resource_id].append({
                'start_date': start_date,
                'end_date': end_date,
                'hours': hours,
                'allocation_id': allocation.get('id')
            })

        # Detect overlapping allocations
        for resource_id, allocations_list in resource_allocations.items():
            for i, alloc1 in enumerate(allocations_list):
                for alloc2 in allocations_list[i+1:]:
                    if self.is_overlapping(alloc1, alloc2):
                        conflicts['total_conflicts'] += 1
                        conflicts['conflict_details'].append({
                            'resource_id': resource_id,
                            'allocation1': alloc1,
                            'allocation2': alloc2,
                            'conflict_type': 'time_overlap'
                        })

        # Generate resolutions
        conflicts['resolutions'] = self.generate_conflict_resolutions(
            conflicts['conflict_details']
        )

        return conflicts

    def generate_recommendations(
        self,
        resource_data: Dict[str, Any],
        utilization_analysis: Dict[str, Any],
        conflicts: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []

        # Resource utilization recommendations
        for resource_id, utilization in utilization_analysis.get(
            'resource_utilization', {}
        ).items():
            if utilization['status'] == 'overallocated':
                recommendations.append({
                    'priority': 'high',
                    'type': 'resource_reallocation',
                    'resource_id': resource_id,
                    'action': f'Reduce allocation for resource {resource_id}',
                    'current_utilization': utilization['utilization_rate'],
                    'target_utilization': 85
                })
            elif utilization['status'] == 'underutilized':
                recommendations.append({
                    'priority': 'medium',
                    'type': 'resource_optimization',
                    'resource_id': resource_id,
                    'action': f'Consider additional tasks for resource {resource_id}',
                    'current_utilization': utilization['utilization_rate'],
                    'target_utilization': 85
                })

        # Conflict resolution recommendations
        for conflict in conflicts.get('conflict_details', []):
            recommendations.append({
                'priority': 'high',
                'type': 'conflict_resolution',
                'resource_id': conflict['resource_id'],
                'action': 'Reschedule conflicting allocations',
                'details': conflict
            })

        return sorted(recommendations, key=lambda x: x['priority'])

    def calculate_efficiency_score(
        self, 
        resource_utilization: Dict[str, Any]
    ) -> float:
        """Calculate overall resource efficiency score."""
        if not resource_utilization:
            return 0.0

        scores = []
        for utilization in resource_utilization.values():
            rate = utilization.get('utilization_rate', 0)
            # Optimal range is 80-100%
            if 80 <= rate <= 100:
                scores.append(100)
            elif rate > 100:
                scores.append(max(0, 100 - (rate - 100) * 2))
            else:
                scores.append(rate)

        return sum(scores) / len(scores) if scores else 0.0

    def generate_utilization_analysis(
        self, 
        resource_utilization: Dict[str, Any]
    ) -> str:
        """Generate human-readable analysis of resource utilization."""
        if not resource_utilization:
            return "No resource utilization data available"

        overall_rates = [
            util['utilization_rate'] 
            for util in resource_utilization.values()
        ]
        avg_utilization = sum(overall_rates) / len(overall_rates)

        overallocated = sum(
            1 for util in resource_utilization.values() 
            if util['status'] == 'overallocated'
        )
        underutilized = sum(
            1 for util in resource_utilization.values() 
            if util['status'] == 'underutilized'
        )

        return (
            f"Average utilization: {avg_utilization:.1f}%. "
            f"Overallocated: {overallocated}, "
            f"Underutilized: {underutilized}"
        )

    def is_overlapping(
        self, 
        allocation1: Dict[str, Any], 
        allocation2: Dict[str, Any]
    ) -> bool:
        """Check if two allocations overlap in time."""
        return (
            allocation1.get('resource_id') == allocation2.get('resource_id') and
            allocation1.get('start_date') == allocation2.get('start_date')
        )

    def generate_conflict_resolutions(
        self, 
        conflicts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate specific resolutions for detected conflicts."""
        resolutions = []
        for conflict in conflicts:
            resolutions.append({
                'conflict_id': f"{conflict['resource_id']}_conflict",
                'resolution_type': 'reschedule',
                'suggested_action': 'Adjust allocation dates to remove overlap',
                'priority': 'high'
            })
        return resolutions


if __name__ == "__main__":
    manager = ResourceManagement()
    manager.run()
