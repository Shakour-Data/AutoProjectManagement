"""
Unit tests for the ResourceAllocationManager module.
This test suite covers the actual ResourceAllocationManager class functionality.
"""

import unittest
import json
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime
from project_management.modules.main_modules.resource_allocation_manager import ResourceAllocationManager

class TestResourceAllocationManager(unittest.TestCase):
    """Test cases for ResourceAllocationManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test input files
        self.resource_allocation_path = os.path.join(self.temp_dir, 'task_resource_allocation.json')
        self.detailed_wbs_path = os.path.join(self.temp_dir, 'detailed_wbs.json')
        self.resource_costs_path = os.path.join(self.temp_dir, 'resource_costs.json')
        self.output_path = os.path.join(self.temp_dir, 'resource_allocation_enriched.json')
        self.summary_output_path = os.path.join(self.temp_dir, 'resource_allocation_summary.json')
        
        # Create test data
        self.resource_allocations = [
            {
                "task_id": "task1",
                "resource_id": "dev1",
                "allocation_percent": 50,
                "start_date": "2024-01-01",
                "end_date": "2024-01-05"
            },
            {
                "task_id": "task2",
                "resource_id": "designer1",
                "allocation_percent": 100,
                "start_date": "2024-01-03",
                "end_date": "2024-01-07"
            }
        ]
        
        self.detailed_wbs = {
            "id": "project1",
            "name": "Test Project",
            "subtasks": [
                {
                    "id": "task1",
                    "name": "Development Task",
                    "subtasks": []
                },
                {
                    "id": "task2",
                    "name": "Design Task",
                    "subtasks": []
                }
            ]
        }
        
        self.resource_costs = {
            "dev1": {"hourly_cost": 50.0, "name": "Senior Developer"},
            "designer1": {"hourly_cost": 40.0, "name": "UI Designer"}
        }
        
        # Write test files
        with open(self.resource_allocation_path, 'w') as f:
            json.dump(self.resource_allocations, f)
        with open(self.detailed_wbs_path, 'w') as f:
            json.dump(self.detailed_wbs, f)
        with open(self.resource_costs_path, 'w') as f:
            json.dump(self.resource_costs, f)
            
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
        
    def test_init_default_paths(self):
        """Test initialization with default paths."""
        manager = ResourceAllocationManager()
        
        self.assertEqual(manager.resource_allocation_path, 'JSonDataBase/Inputs/UserInputs/task_resource_allocation.json')
        self.assertEqual(manager.detailed_wbs_path, 'JSonDataBase/Inputs/UserInputs/detailed_wbs.json')
        self.assertEqual(manager.resource_costs_path, 'JSonDataBase/Inputs/UserInputs/resource_costs.json')
        self.assertEqual(manager.output_path, 'JSonDataBase/OutPuts/resource_allocation_enriched.json')
        self.assertEqual(manager.summary_output_path, 'JSonDataBase/OutPuts/resource_allocation_summary.json')
        
    def test_init_custom_paths(self):
        """Test initialization with custom paths."""
        manager = ResourceAllocationManager(
            resource_allocation_path=self.resource_allocation_path,
            detailed_wbs_path=self.detailed_wbs_path,
            resource_costs_path=self.resource_costs_path,
            output_path=self.output_path,
            summary_output_path=self.summary_output_path
        )
        
        self.assertEqual(manager.resource_allocation_path, self.resource_allocation_path)
        self.assertEqual(manager.detailed_wbs_path, self.detailed_wbs_path)
        self.assertEqual(manager.resource_costs_path, self.resource_costs_path)
        self.assertEqual(manager.output_path, self.output_path)
        self.assertEqual(manager.summary_output_path, self.summary_output_path)
        
    def test_load_json_existing_file(self):
        """Test loading JSON from existing file."""
        manager = ResourceAllocationManager()
        test_data = {"test": "data"}
        test_file = os.path.join(self.temp_dir, 'test.json')
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
            
        result = manager.load_json(test_file)
        self.assertEqual(result, test_data)
        
    def test_load_json_nonexistent_file(self):
        """Test loading JSON from non-existent file."""
        manager = ResourceAllocationManager()
        result = manager.load_json('nonexistent.json')
        self.assertIsNone(result)
        
    def test_save_json(self):
        """Test saving JSON data."""
        manager = ResourceAllocationManager()
        test_data = {"test": "data"}
        test_file = os.path.join(self.temp_dir, 'test_output.json')
        
        manager.save_json(test_data, test_file)
        
        self.assertTrue(os.path.exists(test_file))
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, test_data)
        
    def test_load_inputs(self):
        """Test loading input files."""
        manager = ResourceAllocationManager(
            resource_allocation_path=self.resource_allocation_path,
            detailed_wbs_path=self.detailed_wbs_path,
            resource_costs_path=self.resource_costs_path,
            output_path=self.output_path,
            summary_output_path=self.summary_output_path
        )
        
        manager.load_inputs()
        
        self.assertEqual(manager.resource_allocations, self.resource_allocations)
        self.assertEqual(manager.detailed_wbs, self.detailed_wbs)
        self.assertEqual(manager.resource_costs, self.resource_costs)
        
    def test_load_inputs_missing_files(self):
        """Test loading inputs with missing files."""
        manager = ResourceAllocationManager(
            resource_allocation_path='nonexistent.json',
            detailed_wbs_path='nonexistent.json',
            resource_costs_path='nonexistent.json',
            output_path=self.output_path,
            summary_output_path=self.summary_output_path
        )
        
        manager.load_inputs()
        
        self.assertEqual(manager.resource_allocations, [])
        self.assertEqual(manager.detailed_wbs, {})
        self.assertEqual(manager.resource_costs, {})
        
    def test_find_task_by_id_root_level(self):
        """Test finding task by ID at root level."""
        manager = ResourceAllocationManager()
        manager.detailed_wbs = self.detailed_wbs
        
        task = manager.find_task_by_id('task1')
        self.assertIsNotNone(task)
        self.assertEqual(task['id'], 'task1')
        self.assertEqual(task['name'], 'Development Task')
        
    def test_find_task_by_id_nested(self):
        """Test finding task by ID in nested structure."""
        manager = ResourceAllocationManager()
        nested_wbs = {
            "id": "project1",
            "name": "Test Project",
            "subtasks": [
                {
                    "id": "phase1",
                    "name": "Phase 1",
                    "subtasks": [
                        {
                            "id": "task1",
                            "name": "Nested Task",
                            "subtasks": []
                        }
                    ]
                }
            ]
        }
        manager.detailed_wbs = nested_wbs
        
        task = manager.find_task_by_id('task1')
        self.assertIsNotNone(task)
        self.assertEqual(task['id'], 'task1')
        self.assertEqual(task['name'], 'Nested Task')
        
    def test_find_task_by_id_not_found(self):
        """Test finding non-existent task."""
        manager = ResourceAllocationManager()
        manager.detailed_wbs = self.detailed_wbs
        
        task = manager.find_task_by_id('nonexistent')
        self.assertIsNone(task)
        
    def test_calculate_task_cost_basic(self):
        """Test basic task cost calculation."""
        manager = ResourceAllocationManager()
        manager.resource_costs = self.resource_costs
        
        allocation = {
            "task_id": "task1",
            "resource_id": "dev1",
            "allocation_percent": 100,
            "start_date": "2024-01-01",
            "end_date": "2024-01-05"
        }
        
        cost = manager.calculate_task_cost(allocation)
        expected_days = 5  # 5 days
        expected_hours = 5 * 8 * 1.0  # 5 days * 8 hours * 100%
        expected_cost = expected_hours * 50.0  # 40 hours * $50/hour
        self.assertEqual(cost, expected_cost)
        
    def test_calculate_task_cost_partial_allocation(self):
        """Test task cost calculation with partial allocation."""
        manager = ResourceAllocationManager()
        manager.resource_costs = self.resource_costs
        
        allocation = {
            "task_id": "task1",
            "resource_id": "dev1",
            "allocation_percent": 50,
            "start_date": "2024-01-01",
            "end_date": "2024-01-05"
        }
        
        cost = manager.calculate_task_cost(allocation)
        expected_days = 5
        expected_hours = 5 * 8 * 0.5  # 5 days * 8 hours * 50%
        expected_cost = expected_hours * 50.0
        self.assertEqual(cost, expected_cost)
        
    def test_calculate_task_cost_missing_resource(self):
        """Test task cost calculation with missing resource."""
        manager = ResourceAllocationManager()
        manager.resource_costs = self.resource_costs
        
        allocation = {
            "task_id": "task1",
            "resource_id": "nonexistent",
            "allocation_percent": 100,
            "start_date": "2024-01-01",
            "end_date": "2024-01-05"
        }
        
        cost = manager.calculate_task_cost(allocation)
        self.assertEqual(cost, 0.0)
        
    def test_calculate_task_cost_invalid_date(self):
        """Test task cost calculation with invalid date format."""
        manager = ResourceAllocationManager()
        manager.resource_costs = self.resource_costs
        
        allocation = {
            "task_id": "task1",
            "resource_id": "dev1",
            "allocation_percent": 100,
            "start_date": "invalid-date",
            "end_date": "2024-01-05"
        }
        
        cost = manager.calculate_task_cost(allocation)
        self.assertEqual(cost, 0.0)
        
    def test_enrich_wbs_with_resources(self):
        """Test enriching WBS with resource allocations."""
        manager = ResourceAllocationManager(
            resource_allocation_path=self.resource_allocation_path,
            detailed_wbs_path=self.detailed_wbs_path,
            resource_costs_path=self.resource_costs_path,
            output_path=self.output_path,
            summary_output_path=self.summary_output_path
        )
        
        manager.load_inputs()
        manager.enrich_wbs_with_resources()
        
        # Check that task1 has resource allocations
        task1 = manager.find_task_by_id('task1')
        self.assertIn('resource_allocations', task1)
        self.assertEqual(len(task1['resource_allocations']), 1)
        self.assertIn('calculated_cost', task1['resource_allocations'][0])
        
    def test_enrich_wbs_with_nonexistent_task(self):
        """Test enriching WBS with allocations for non-existent tasks."""
        manager = ResourceAllocationManager(
            resource_allocation_path=self.resource_allocation_path,
            detailed_wbs_path=self.detailed_wbs_path,
            resource_costs_path=self.resource_costs_path,
            output_path=self.output_path,
            summary_output_path=self.summary_output_path
        )
        
        # Add allocation for non-existent task
        manager.resource_allocations = [
            {
                "task_id": "nonexistent",
                "resource_id": "dev1",
                "allocation_percent": 100,
                "start_date": "2024-01-01",
                "end_date": "2024-01-05"
            }
        ]
        manager.detailed_wbs = self.detailed_wbs
        
        manager.enrich_wbs_with_resources()
        
        # Should not crash, just skip non-existent tasks
        task1 = manager.find_task_by_id('task1')
        self.assertNotIn('resource_allocations', task1)
        
    def test_summarize_costs(self):
        """Test cost summarization."""
        manager = ResourceAllocationManager(
            resource_allocation_path=self.resource_allocation_path,
            detailed_wbs_path=self.detailed_wbs_path,
            resource_costs_path=self.resource_costs_path,
            output_path=self.output_path,
            summary_output_path=self.summary_output_path
        )
        
        manager.load_inputs()
        manager.enrich_wbs_with_resources()
        total_cost = manager.summarize_costs()
        
        # Calculate expected cost
        expected_cost = 0.0
        for allocation in self.resource_allocations:
            expected_cost += manager.calculate_task_cost(allocation)
        
        self.assertEqual(total_cost, expected_cost)
        self.assertIn('task1', manager.task_cost_summary)
        self.assertIn('task2', manager.task_cost_summary)
        
    def test_summarize_costs_empty_wbs(self):
        """Test cost summarization with empty WBS."""
        manager = ResourceAllocationManager()
        manager.detailed_wbs = {}
        
        total_cost = manager.summarize_costs()
        self.assertEqual(total_cost, 0.0)
        self.assertEqual(manager.task_cost_summary, {})
        
    def test_run_complete_workflow(self):
        """Test complete workflow execution."""
        manager = ResourceAllocationManager(
            resource_allocation_path=self.resource_allocation_path,
            detailed_wbs_path=self.detailed_wbs_path,
            resource_costs_path=self.resource_costs_path,
            output_path=self.output_path,
            summary_output_path=self.summary_output_path
        )
        
        manager.run()
        
        # Check that output files were created
        self.assertTrue(os.path.exists(self.output_path))
        self.assertTrue(os.path.exists(self.summary_output_path))
        
        # Check output content
        with open(self.output_path, 'r') as f:
            enriched_wbs = json.load(f)
        self.assertIn('subtasks', enriched_wbs)
        
        with open(self.summary_output_path, 'r') as f:
            summary = json.load(f)
        self.assertIn('task1', summary)
        self.assertIn('task2', summary)
        
    def test_run_with_missing_files(self):
        """Test complete workflow with missing input files."""
        manager = ResourceAllocationManager(
            resource_allocation_path='nonexistent.json',
            detailed_wbs_path='nonexistent.json',
            resource_costs_path='nonexistent.json',
            output_path=self.output_path,
            summary_output_path=self.summary_output_path
        )
        
        manager.run()
        
        # Should still create output files
        self.assertTrue(os.path.exists(self.output_path))
        self.assertTrue(os.path.exists(self.summary_output_path))
        
        # Check that files contain empty/default data
        with open(self.output_path, 'r') as f:
            enriched_wbs = json.load(f)
        self.assertEqual(enriched_wbs, {})
        
        with open(self.summary_output_path, 'r') as f:
            summary = json.load(f)
        self.assertEqual(summary, {})


if __name__ == "__main__":
    unittest.main()
