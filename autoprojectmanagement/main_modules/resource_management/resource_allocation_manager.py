"""
path: autoprojectmanagement/main_modules/resource_management/resource_allocation_manager.py
File: resource_allocation_manager.py
Purpose: Manages resource allocation and cost calculation for project tasks
Author: BLACKBOXAI
Version: 2.0.0
License: MIT
Description: Enhanced resource allocation manager with comprehensive cost tracking,
resource optimization, and detailed reporting capabilities for project management.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResourceType(Enum):
    """Enumeration of supported resource types."""
    HUMAN = "human"
    EQUIPMENT = "equipment"
    MATERIAL = "material"
    SOFTWARE = "software"
    FACILITY = "facility"


class AllocationStatus(Enum):
    """Enumeration of resource allocation statuses."""
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


@dataclass
class ResourceCost:
    """Data class for resource cost information."""
    resource_id: str
    resource_name: str
    resource_type: ResourceType
    hourly_cost: float
    daily_cost: float
    currency: str = "USD"
    effective_date: Optional[str] = None
    expiry_date: Optional[str] = None


@dataclass
class ResourceAllocation:
    """Data class for resource allocation details."""
    task_id: str
    resource_id: str
    allocation_percent: float
    start_date: str
    end_date: str
    status: AllocationStatus
    notes: Optional[str] = None
    calculated_cost: Optional[float] = None


class ResourceAllocationError(Exception):
    """Custom exception for resource allocation errors."""
    pass


class ResourceAllocationManager:
    """
    Enhanced resource allocation manager with comprehensive cost tracking,
    resource optimization, and detailed reporting capabilities.
    
    This class provides functionality for:
    - Loading and validating resource allocation data
    - Calculating detailed costs for resource allocations
    - Optimizing resource utilization
    - Generating comprehensive reports
    - Managing resource conflicts and constraints
    """
    
    # Constants
    WORKING_HOURS_PER_DAY = 8
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"
    
    def __init__(self,
                 resource_allocation_path: str = 'JSonDataBase/Inputs/UserInputs/task_resource_allocation.json',
                 detailed_wbs_path: str = 'JSonDataBase/Inputs/UserInputs/detailed_wbs.json',
                 resource_costs_path: str = 'JSonDataBase/Inputs/UserInputs/resource_costs.json',
                 resource_constraints_path: Optional[str] = None,
                 output_path: str = 'JSonDataBase/OutPuts/resource_allocation_enriched.json',
                 summary_output_path: str = 'JSonDataBase/OutPuts/resource_allocation_summary.json',
                 report_output_path: str = 'JSonDataBase/OutPuts/resource_allocation_report.json') -> None:
        """
        Initialize the Resource Allocation Manager.
        
        Args:
            resource_allocation_path: Path to resource allocation JSON file
            detailed_wbs_path: Path to detailed WBS JSON file
            resource_costs_path: Path to resource costs JSON file
            resource_constraints_path: Optional path to resource constraints JSON file
            output_path: Path for enriched WBS output
            summary_output_path: Path for cost summary output
            report_output_path: Path for comprehensive report output
        """
        self.resource_allocation_path = Path(resource_allocation_path)
        self.detailed_wbs_path = Path(detailed_wbs_path)
        self.resource_costs_path = Path(resource_costs_path)
        self.resource_constraints_path = Path(resource_constraints_path) if resource_constraints_path else None
        self.output_path = Path(output_path)
        self.summary_output_path = Path(summary_output_path)
        self.report_output_path = Path(report_output_path)
        
        # Ensure output directories exist
        for path in [self.output_path, self.summary_output_path, self.report_output_path]:
            path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize data containers
        self.resource_allocations: List[Dict[str, Any]] = []
        self.detailed_wbs: Dict[str, Any] = {}
        self.resource_costs: Dict[str, Any] = {}
        self.resource_constraints: Dict[str, Any] = {}
        self.task_cost_summary: Dict[str, Dict[str, Any]] = {}
        self.allocation_conflicts: List[Dict[str, Any]] = []
        
        # Performance metrics
        self.total_cost: float = 0.0
        self.resource_utilization: Dict[str, float] = {}
        self.budget_variance: float = 0.0
        
    def load_json(self, path: Path) -> Optional[Dict[str, Any]]:
        """
        Load JSON data from file with error handling.
        
        Args:
            path: Path to JSON file
            
        Returns:
            Dictionary containing JSON data or None if file not found
            
        Raises:
            ResourceAllocationError: If JSON is malformed
        """
        try:
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"File not found: {path}")
                return None
        except json.JSONDecodeError as e:
            raise ResourceAllocationError(f"Invalid JSON in {path}: {e}")
        except Exception as e:
            raise ResourceAllocationError(f"Error loading {path}: {e}")
    
    def save_json(self, data: Any, path: Path) -> None:
        """
        Save data to JSON file with proper formatting.
        
        Args:
            data: Data to save
            path: Output file path
            
        Raises:
            ResourceAllocationError: If unable to save file
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"Saved data to {path}")
        except Exception as e:
            raise ResourceAllocationError(f"Error saving to {path}: {e}")
    
    def load_inputs(self) -> None:
        """Load and validate all input data."""
        logger.info("Loading input data...")
        
        # Load resource allocations
        allocations_data = self.load_json(self.resource_allocation_path)
        self.resource_allocations = allocations_data or []
        
        # Load detailed WBS
        wbs_data = self.load_json(self.detailed_wbs_path)
        self.detailed_wbs = wbs_data or {}
        
        # Load resource costs
        costs_data = self.load_json(self.resource_costs_path)
        self.resource_costs = costs_data or {}
        
        # Load resource constraints if provided
        if self.resource_constraints_path:
            constraints_data = self.load_json(self.resource_constraints_path)
            self.resource_constraints = constraints_data or {}
        
        logger.info(f"Loaded {len(self.resource_allocations)} resource allocations")
        logger.info(f"Loaded {len(self.resource_costs)} resource costs")
    
    def find_task_by_id(self, task_id: str, node: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Find a task in the WBS by its ID using recursive search.
        
        Args:
            task_id: The ID of the task to find
            node: The current node to search (defaults to root WBS)
            
        Returns:
            The task dictionary if found, None otherwise
        """
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
    
    def calculate_task_cost(self, allocation: Dict[str, Any]) -> float:
        """
        Calculate the cost of a task based on its resource allocation.
        
        Args:
            allocation: Resource allocation dictionary
            
        Returns:
            Calculated cost as float
        """
        resource_id = allocation.get('resource_id')
        allocation_percent = allocation.get('allocation_percent', 0) / 100.0
        start_date_str = allocation.get('start_date')
        end_date_str = allocation.get('end_date')
        
        # Validate resource exists
        if resource_id not in self.resource_costs:
            logger.warning(f"Resource {resource_id} not found in costs")
            return 0.0
        
        # Get hourly cost
        hourly_cost = self.resource_costs[resource_id].get('hourly_cost', 0.0)
        if hourly_cost <= 0:
            logger.warning(f"Invalid hourly cost for resource {resource_id}")
            return 0.0
        
        # Calculate duration in days
        try:
            start_date = datetime.strptime(start_date_str, self.DEFAULT_DATE_FORMAT)
            end_date = datetime.strptime(end_date_str, self.DEFAULT_DATE_FORMAT)
            if end_date < start_date:
                logger.warning(f"End date before start date for allocation {allocation}")
                return 0.0
            days = (end_date - start_date).days + 1
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing dates: {e}")
            return 0.0
        
        # Calculate total hours and cost
        total_hours = days * self.WORKING_HOURS_PER_DAY * allocation_percent
        cost = total_hours * hourly_cost
        
        return round(cost, 2)
    
    def enrich_wbs_with_resources(self) -> None:
        """Enrich WBS tasks with resource allocation and cost information."""
        logger.info("Enriching WBS with resource allocations...")
        
        allocation_count = 0
        for allocation in self.resource_allocations:
            task_id = allocation.get('task_id')
            if not task_id:
                logger.warning("Allocation missing task_id, skipping")
                continue
                
            task_node = self.find_task_by_id(task_id)
            if not task_node:
                logger.warning(f"Task {task_id} not found in WBS")
                continue
                
            # Initialize resource allocations list if needed
            if 'resource_allocations' not in task_node:
                task_node['resource_allocations'] = []
                
            # Calculate cost and create enriched allocation
            cost = self.calculate_task_cost(allocation)
            allocation_enriched = dict(allocation)
            allocation_enriched['calculated_cost'] = cost
            
            task_node['resource_allocations'].append(allocation_enriched)
            allocation_count += 1
            
        logger.info(f"Enriched {allocation_count} resource allocations")
    
    def summarize_costs(self, node: Optional[Dict[str, Any]] = None) -> float:
        """
        Recursively summarize costs for a task and all subtasks.
        
        Args:
            node: The task node to summarize (defaults to root WBS)
            
        Returns:
            Total cost for the task and all subtasks
        """
        if node is None:
            node = self.detailed_wbs
            
        if not node:
            return 0.0
            
        total_cost = 0.0
        
        # Sum costs from resource allocations
        for alloc in node.get('resource_allocations', []):
            total_cost += alloc.get('calculated_cost', 0.0)
            
        # Recursively sum subtask costs
        for subtask in node.get('subtasks', []):
            total_cost += self.summarize_costs(subtask)
            
        # Store summary for this task
        task_id = node.get('id')
        if task_id:
            self.task_cost_summary[task_id] = {
                'task_name': node.get('name', 'Unknown'),
                'total_cost': round(total_cost, 2)
            }
            
        return total_cost
    
    def generate_resource_utilization_report(self) -> Dict[str, Any]:
        """Generate resource utilization analysis."""
        utilization = {}
        
        # Count allocations per resource
        resource_allocations = {}
        for allocation in self.resource_allocations:
            resource_id = allocation.get('resource_id')
            if resource_id:
                if resource_id not in resource_allocations:
                    resource_allocations[resource_id] = 0
                resource_allocations[resource_id] += 1
        
        # Calculate utilization rates
        for resource_id, count in resource_allocations.items():
            if resource_id in self.resource_costs:
                utilization[resource_id] = {
                    'resource_name': self.resource_costs[resource_id].get('name', resource_id),
                    'allocation_count': count,
                    'utilization_rate': min(count * 0.1, 1.0)  # Simplified calculation
                }
        
        return utilization
    
    def validate_allocations(self) -> List[Dict[str, Any]]:
        """Validate resource allocations for conflicts and issues."""
        conflicts = []
        
        # Check for overlapping allocations
        resource_time_map = {}
        
        for allocation in self.resource_allocations:
            resource_id = allocation.get('resource_id')
            if not resource_id:
                continue
                
            if resource_id not in resource_time_map:
                resource_time_map[resource_id] = []
                
            try:
                start_date = datetime.strptime(allocation.get('start_date', ''), self.DEFAULT_DATE_FORMAT)
                end_date = datetime.strptime(allocation.get('end_date', ''), self.DEFAULT_DATE_FORMAT)
                
                # Check for overlaps with existing allocations
                for existing in resource_time_map[resource_id]:
                    if not (end_date < existing['start_date'] or start_date > existing['end_date']):
                        conflicts.append({
                            'type': 'overlap',
                            'resource_id': resource_id,
                            'allocation1': allocation,
                            'allocation2': existing,
                            'message': f"Resource {resource_id} has overlapping allocations"
                        })
                
                resource_time_map[resource_id].append({
                    'start_date': start_date,
                    'end_date': end_date,
                    'allocation': allocation
                })
                
            except ValueError:
                conflicts.append({
                    'type': 'invalid_date',
                    'allocation': allocation,
                    'message': "Invalid date format in allocation"
                })
        
        return conflicts
    
    def run(self) -> None:
        """Execute the complete resource allocation process."""
        logger.info("Starting resource allocation process...")
        
        try:
            # Load all input data
            self.load_inputs()
            
            # Validate allocations
            self.allocation_conflicts = self.validate_allocations()
            if self.allocation_conflicts:
                logger.warning(f"Found {len(self.allocation_conflicts)} allocation conflicts")
            
            # Enrich WBS with resource information
            self.enrich_wbs_with_resources()
            
            # Calculate total costs
            self.total_cost = self.summarize_costs()
            
            # Generate utilization report
            self.resource_utilization = self.generate_resource_utilization_report()
            
            # Save outputs
            self.save_json(self.detailed_wbs, self.output_path)
            self.save_json(self.task_cost_summary, self.summary_output_path)
            
            # Generate comprehensive report
            report = {
                'process_date': datetime.now().isoformat(),
                'total_cost': self.total_cost,
                'resource_utilization': self.resource_utilization,
                'allocation_conflicts': self.allocation_conflicts,
                'task_count': len(self.task_cost_summary),
                'resource_count': len(self.resource_costs)
            }
            self.save_json(report, self.report_output_path)
            
            logger.info(f"Resource allocation process completed successfully")
            logger.info(f"Total cost calculated: ${self.total_cost}")
            logger.info(f"Enriched WBS saved to: {self.output_path}")
            logger.info(f"Cost summary saved to: {self.summary_output_path}")
            logger.info(f"Report saved to: {self.report_output_path}")
            
        except Exception as e:
            logger.error(f"Error in resource allocation process: {e}")
            raise ResourceAllocationError(f"Process failed: {e}")


# Example usage and testing
if __name__ == "__main__":
    """Example usage of the ResourceAllocationManager."""
    try:
        manager = ResourceAllocationManager()
        manager.run()
        
        # Print summary
        print("\n=== Resource Allocation Summary ===")
        print(f"Total Project Cost: ${manager.total_cost}")
        print(f"Number of Tasks: {len(manager.task_cost_summary)}")
        print(f"Number of Resources: {len(manager.resource_costs)}")
        
        if manager.allocation_conflicts:
            print(f"\nAllocation Conflicts: {len(manager.allocation_conflicts)}")
            for conflict in manager.allocation_conflicts:
                print(f"  - {conflict['message']}")
                
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
