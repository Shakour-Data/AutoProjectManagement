import unittest
from unittest.mock import patch, MagicMock
import json
import os

# Add the project root to the path so we can import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

# Import ProgressCalculator for the mock
from project_management.modules.main_modules.progress_calculator_refactored import ProgressCalculator
# Import DashboardReports for the tests
from project_management.modules.main_modules.dashboards_reports import DashboardReports

class TestDashboardReports(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        self.test_input_dir = 'test_input_dir'
        self.test_wbs_scores_path = 'JSonDataBase/OutPuts/wbs_scores.json'
        self.test_detailed_wbs = {
            "tasks": [
                {"id": 1, "title": "Task 1", "status": "completed", "importance": 0.8, "urgency": 0.9, "progress": 100},
                {"id": 2, "title": "Task 2", "status": "in_progress", "importance": 0.6, "urgency": 0.4, "progress": 50},
                {"id": 3, "title": "Task 3", "status": "pending", "importance": 0.3, "urgency": 0.2, "progress": 0}
            ]
        }
        self.test_human_resources = [
            {"name": "Alice", "role": "Developer"},
            {"name": "Bob", "role": "Project Manager"}
        ]
        self.test_resource_allocation = [
            {"resource_id": "R1", "task_id": 1, "allocation_percent": 50},
            {"resource_id": "R2", "task_id": 2, "allocation_percent": 75}
        ]
        self.test_task_resource_allocation = [
            {"resource_id": "R1", "task_id": 1, "allocation_percent": 50},
            {"resource_id": "R2", "task_id": 2, "allocation_percent": 75}
        ]
        self.test_wbs_scores = [
            {"id": 1, "cost": 1000},
            {"id": 2, "cost": 500}
        ]
        self.test_workflow_definition = [
            {"type": "risk", "description": "Risk 1"},
            {"type": "issue", "description": "Issue 1"},
            {"type": "task", "description": "Task 1"}
        ]

    # Test 1: Test initialization with default path
    def test_init_default_path(self):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        self.assertEqual(dashboard.input_dir, 'JSonDataBase/Inputs/UserInputs')
        self.assertIsInstance(dashboard.progress_calculator, ProgressCalculator)

    # Test 2: Test initialization with custom path
    def test_init_custom_path(self):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports('custom_input_dir')
        self.assertEqual(dashboard.input_dir, 'custom_input_dir')
        self.assertIsInstance(dashboard.progress_calculator, ProgressCalculator)

    # Test 3: Test load_json_file with existing file
    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.path.exists', return_value=True)
    def test_load_json_file_existing(self, mock_exists, mock_open):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({"key": "value"})
        result = dashboard.load_json_file('test_file.json')
        self.assertEqual(result, {"key": "value"})

    # Test 4: Test load_json_file with non-existing file
    @patch('os.path.exists', return_value=False)
    def test_load_json_file_non_existing(self, mock_exists):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        result = dashboard.load_json_file('nonexistent_file.json')
        self.assertIsNone(result)

    # Test 5: Test load_json_file with permission error
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    def test_load_json_file_permission_error(self, mock_open, mock_exists):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        result = dashboard.load_json_file('test_file.json')
        self.assertIsNone(result)

    # Test 6: Test load_json_file with invalid JSON
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=MagicMock)
    def test_load_json_file_invalid_json(self, mock_open, mock_exists):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        mock_open.return_value.__enter__.return_value.read.return_value = 'invalid json'
        result = dashboard.load_json_file('test_file.json')
        self.assertIsNone(result)

    # Test 7: Test load_inputs with all files
    @patch.object(DashboardReports, 'load_json_file')
    def test_load_inputs_all_files(self, mock_load_json):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup mock responses
        mock_load_json.side_effect = [
            self.test_detailed_wbs,
            self.test_human_resources,
            self.test_resource_allocation,
            self.test_task_resource_allocation,
            self.test_wbs_scores,
            self.test_workflow_definition
        ]
        
        dashboard.load_inputs()
        
        # Verify all files were loaded
        self.assertEqual(dashboard.data['detailed_wbs'], self.test_detailed_wbs)
        self.assertEqual(dashboard.data['human_resources'], self.test_human_resources)
        self.assertEqual(dashboard.data['resource_allocation'], self.test_resource_allocation)
        self.assertEqual(dashboard.data['task_resource_allocation'], self.test_task_resource_allocation)
        self.assertEqual(dashboard.data['wbs_scores'], self.test_wbs_scores)
        self.assertEqual(dashboard.data['workflow_definition'], self.test_workflow_definition)

    # Test 8: Test load_inputs with missing files
    @patch.object(DashboardReports, 'load_json_file')
    def test_load_inputs_missing_files(self, mock_load_json):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup mock responses with some None values
        mock_load_json.side_effect = [self.test_detailed_wbs, None, self.test_resource_allocation, None, self.test_wbs_scores, None]
        
        dashboard.load_inputs()
        
        # Verify missing files are handled
        self.assertEqual(dashboard.data['detailed_wbs'], self.test_detailed_wbs)
        self.assertIsNone(dashboard.data['human_resources'])
        self.assertEqual(dashboard.data['resource_allocation'], self.test_resource_allocation)
        self.assertIsNone(dashboard.data['task_resource_allocation'])
        self.assertEqual(dashboard.data['wbs_scores'], self.test_wbs_scores)
        self.assertIsNone(dashboard.data['workflow_definition'])

    # Test 9: Test _format_task with complete data
    def test_format_task_complete_data(self):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        task = {"title": "Test Task", "status": "completed", "importance": 0.8, "urgency": 0.9, "progress": 100}
        result = dashboard._format_task(task)
        self.assertIn("Test Task", result)
        self.assertIn("Status: completed", result)
        self.assertIn("Importance: 0.80", result)
        self.assertIn("Urgency: 0.90", result)
        self.assertIn("Score: 0.84", result)
        self.assertIn("Progress: 100%", result)

    # Test 10: Test _format_task with missing data
    def test_format_task_missing_data(self):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        task = {"title": "Test Task", "status": "in_progress", "progress": 50}
        result = dashboard._format_task(task)
        self.assertIn("Test Task", result)
        self.assertIn("Status: in_progress", result)
        self.assertIn("Progress: 50%", result)
        self.assertNotIn("Importance", result)
        self.assertNotIn("Urgency", result)
        self.assertNotIn("Score", result)

    # Test 11: Test generate_progress_report with complete data
    @patch.object(DashboardReports, 'load_inputs')
    def test_generate_progress_report_complete_data(self, mock_load_inputs):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup mock data
        dashboard.data = {
            'detailed_wbs': self.test_detailed_wbs['tasks']
        }
        
        result = dashboard.generate_progress_report()
        
        # Verify report structure
        self.assertIn("# Progress Report Dashboard", result)
        self.assertIn("Total Tasks: 3", result)
        self.assertIn("Completed: 1", result)
        self.assertIn("In Progress: 1", result)
        self.assertIn("Pending: 1", result)
        self.assertIn("Progress Percentage: 33.33%", result)
        self.assertIn("## Task Details", result)
        self.assertIn("Task 1", result)
        self.assertIn("Task 2", result)
        self.assertIn("Task 3", result)

    # Test 12: Test generate_progress_report with empty data
    @patch.object(DashboardReports, 'load_inputs')
    def test_generate_progress_report_empty_data(self, mock_load_inputs):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup empty data
        dashboard.data = {
            'detailed_wbs': []
        }
        
        result = dashboard.generate_progress_report()
        
        # Verify empty data handling
        self.assertIn("# Progress Report Dashboard", result)
        self.assertIn("Total Tasks: 0", result)
        self.assertIn("Progress Percentage: 0.00%", result)
        self.assertIn("## Task Details", result)
        self.assertIn("No tasks to display", result)

    # Test 13: Test generate_priority_urgency_report with complete data
    @patch.object(DashboardReports, 'load_inputs')
    def test_generate_priority_urgency_report_complete_data(self, mock_load_inputs):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup mock data
        dashboard.data = {
            'detailed_wbs': self.test_detailed_wbs['tasks']
        }
        
        result = dashboard.generate_priority_urgency_report()
        
        # Verify report structure
        self.assertIn("# Task Priority and Urgency Report", result)
        self.assertIn("Top 10 Important Tasks", result)
        self.assertIn("Top 10 Urgent Tasks", result)
        self.assertIn("Eisenhower Matrix", result)
        self.assertIn("Urgent & Important", result)
        self.assertIn("Urgent & Not Important", result)
        self.assertIn("Not Urgent & Important", result)
        self.assertIn("Not Urgent & Not Important", result)

    # Test 14: Test generate_resource_allocation_report with complete data
    @patch.object(DashboardReports, 'load_inputs')
    def test_generate_resource_allocation_report_complete_data(self, mock_load_inputs):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup mock data
        dashboard.data = {
            'human_resources': self.test_human_resources,
            'task_resource_allocation': self.test_task_resource_allocation
        }
        
        result = dashboard.generate_resource_allocation_report()
        
        # Verify report structure
        self.assertIn("# Resource Allocation Dashboard", result)
        self.assertIn("## Human Resources", result)
        self.assertIn("Alice (Developer)", result)
        self.assertIn("Bob (Project Manager)", result)
        self.assertIn("## Resource Allocation Summary", result)
        self.assertIn("Resource ID R1: 50% allocated", result)
        self.assertIn("Resource ID R2: 75% allocated", result)

    # Test 15: Test generate_cost_management_report with complete data
    @patch.object(DashboardReports, 'load_inputs')
    def test_generate_cost_management_report_complete_data(self, mock_load_inputs):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup mock data
        dashboard.data = {
            'wbs_scores': self.test_wbs_scores,
            'resource_allocation': self.test_resource_allocation
        }
        
        result = dashboard.generate_cost_management_report()
        
        # Verify report structure
        self.assertIn("# Cost Management Report", result)
        self.assertIn(f"Total Cost: {1500}", result)
        self.assertIn("## WBS Scores", result)
        self.assertIn("id 1: Cost = 1000", result)
        self.assertIn("id 2: Cost = 500", result)

    # Test 16: Test generate_risk_issue_tracking_report with complete data
    @patch.object(DashboardReports, 'load_inputs')
    def test_generate_risk_issue_tracking_report_complete_data(self, mock_load_inputs):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup mock data
        dashboard.data = {
            'workflow_definition': self.test_workflow_definition
        }
        
        result = dashboard.generate_risk_issue_tracking_report()
        
        # Verify report structure
        self.assertIn("# Risk and Issue Tracking Dashboard", result)
        self.assertIn("## Risks", result)
        self.assertIn("Risk 1", result)
        self.assertIn("## Issues", result)
        self.assertIn("Issue 1", result)

    # Test 17: Test generate_progress_report with unicode data
    @patch.object(DashboardReports, 'load_inputs')
    def test_generate_progress_report_unicode_data(self, mock_load_inputs):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup mock data with unicode
        dashboard.data = {
            'detailed_wbs': [
                {"title": "مهم", "status": "completed", "progress": 100},
                {"title": "وظيفة", "status": "in_progress", "progress": 50}
            ]
        }
        
        result = dashboard.generate_progress_report()
        
        # Verify unicode handling
        self.assertIn("مهم", result)
        self.assertIn("وظيفة", result)

    # Test 18: Test generate_priority_urgency_report with special characters
    @patch.object(DashboardReports, 'load_inputs')
    def test_generate_priority_urgency_report_special_characters(self, mock_load_inputs):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup mock data with special characters
        dashboard.data = {
            'detailed_wbs': [
                {"title": "Task!@#", "status": "completed", "importance": 0.8, "urgency": 0.9, "progress": 100},
                {"title": "Task$%^", "status": "in_progress", "importance": 0.6, "urgency": 0.4, "progress": 50}
            ]
        }
        
        result = dashboard.generate_priority_urgency_report()
        
        # Verify special characters handling
        self.assertIn("Task!@#", result)
        self.assertIn("Task$%^", result)

    # Test 19: Test generate_resource_allocation_report with zero allocation
    @patch.object(DashboardReports, 'load_inputs')
    def test_generate_resource_allocation_report_zero_allocation(self, mock_load_inputs):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup mock data with zero allocation
        dashboard.data = {
            'human_resources': self.test_human_resources,
            'task_resource_allocation': [
                {"resource_id": "R1", "task_id": 1, "allocation_percent": 0},
                {"resource_id": "R2", "task_id": 2, "allocation_percent": 0}
            ]
        }
        
        result = dashboard.generate_resource_allocation_report()
        
        # Verify zero allocation handling
        self.assertIn("Resource ID R1: 0% allocated", result)
        self.assertIn("Resource ID R2: 0% allocated", result)

    # Test 20: Test generate_cost_management_report with missing cost data
    @patch.object(DashboardReports, 'load_inputs')
    def test_generate_cost_management_report_missing_cost_data(self, mock_load_inputs):
        from project_management.modules.main_modules.dashboards_reports import DashboardReports
        dashboard = DashboardReports()
        
        # Setup mock data with missing cost
        dashboard.data = {
            'wbs_scores': [
                {"id": 1},
                {"id": 2, "cost": 500}
            ]
        }
        
        result = dashboard.generate_cost_management_report()
        
        # Verify missing cost handling
        self.assertIn("# Cost Management Report", result)
        self.assertIn("Total Cost: 500", result)
        self.assertIn("id 2: Cost = 500", result)

if __name__ == "__main__":
    unittest.main()
