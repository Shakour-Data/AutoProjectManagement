import unittest
from unittest.mock import patch, mock_open
import os
import json

# Add the project root to the path so we can import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestWorkflowDataCollector(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        self.test_tasks = [
            {
                "task_id": 1,
                "sprint_id": 1,
                "title": "Task 1",
                "status": "todo",
                "priority": "high",
                "progress": 0
            },
            {
                "task_id": 2,
                "sprint_id": 1,
                "title": "Task 2",
                "status": "in_progress",
                "priority": "medium",
                "progress": 50
            }
        ]
        
        self.test_burndown = [
            {
                "sprint_id": 1,
                "day": 1,
                "remaining_work": 100
            },
            {
                "sprint_id": 1,
                "day": 2,
                "remaining_work": 80
            }
        ]

    # Test 1: Test initialization with default data directory
    def test_init_default_data_directory(self):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        self.assertEqual(collector.data_dir, 'SystemInputs/user_inputs')
        self.assertEqual(collector.scrum_sprints_file, os.path.join('SystemInputs/user_inputs', 'scrum_sprints.json'))
        self.assertEqual(collector.scrum_tasks_file, os.path.join('SystemInputs/user_inputs', 'scrum_tasks.json'))
        self.assertEqual(collector.scrum_burndown_file, os.path.join('SystemInputs/user_inputs', 'scrum_burndown.json'))

    # Test 2: Test initialization with custom data directory
    def test_init_custom_data_directory(self):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector('custom_data_dir')
        self.assertEqual(collector.data_dir, 'custom_data_dir')
        self.assertEqual(collector.scrum_sprints_file, os.path.join('custom_data_dir', 'scrum_sprints.json'))
        self.assertEqual(collector.scrum_tasks_file, os.path.join('custom_data_dir', 'scrum_tasks.json'))
        self.assertEqual(collector.scrum_burndown_file, os.path.join('custom_data_dir', 'scrum_burndown.json'))

    # Test 3: Test create_scrum_workflow_tables with existing files
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_create_scrum_workflow_tables_existing_files(self, mock_open_file, mock_exists):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        collector.create_scrum_workflow_tables()
        
        # Verify that open was not called since files exist
        mock_open_file.assert_not_called()

    # Test 4: Test create_scrum_workflow_tables with non-existing files
    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_create_scrum_workflow_tables_non_existing_files(self, mock_json_dump, mock_open_file, mock_exists):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        collector.create_scrum_workflow_tables()
        
        # Verify that open was called for each file
        self.assertEqual(mock_open_file.call_count, 3)
        # Verify that json.dump was called with empty lists
        self.assertEqual(mock_json_dump.call_count, 3)
        mock_json_dump.assert_any_call([], mock_open_file())

    # Test 5: Test update_scrum_task with new task
    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_update_scrum_task_new_task(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Mock the file operations
        mock_file_handle = mock_open_file.return_value
        mock_file_handle.read.return_value = '[]'
        
        collector.update_scrum_task(1, 1, "New Task", "todo", "high", 0)
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_with(collector.scrum_tasks_file, 'r+', encoding='utf-8')
        
        # Verify that json.dump was called with the new task
        mock_file_handle.seek.assert_called_once_with(0)
        mock_file_handle.truncate.assert_called_once()

    # Test 6: Test update_scrum_task with existing task
    @patch("builtins.open", new_callable=mock_open)
    def test_update_scrum_task_existing_task(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Mock the file operations with existing tasks
        mock_file_handle = mock_open_file.return_value
        mock_file_handle.read.return_value = json.dumps(self.test_tasks)
        
        collector.update_scrum_task(1, 1, "Updated Task", "in_progress", "high", 25)
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_with(collector.scrum_tasks_file, 'r+', encoding='utf-8')

    # Test 7: Test update_scrum_burndown with new entry
    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_update_scrum_burndown_new_entry(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Mock the file operations
        mock_file_handle = mock_open_file.return_value
        mock_file_handle.read.return_value = '[]'
        
        collector.update_scrum_burndown(1, 1, 100)
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_with(collector.scrum_burndown_file, 'r+', encoding='utf-8')
        
        # Verify that file operations were called
        mock_file_handle.seek.assert_called_once_with(0)
        mock_file_handle.truncate.assert_called_once()

    # Test 8: Test update_scrum_burndown with existing entry
    @patch("builtins.open", new_callable=mock_open)
    def test_update_scrum_burndown_existing_entry(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Mock the file operations with existing burndown data
        mock_file_handle = mock_open_file.return_value
        mock_file_handle.read.return_value = json.dumps(self.test_burndown)
        
        collector.update_scrum_burndown(1, 1, 90)
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_with(collector.scrum_burndown_file, 'r+', encoding='utf-8')

    # Test 9: Test generate_scrum_report with valid data
    @patch("builtins.open", new_callable=mock_open)
    def test_generate_scrum_report_valid_data(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Mock the file operations with burndown data
        mock_open_file.return_value.read.return_value = json.dumps(self.test_burndown)
        
        report = collector.generate_scrum_report(1)
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_with(collector.scrum_burndown_file, 'r', encoding='utf-8')
        
        # Verify that the report is correctly generated
        self.assertEqual(len(report), 2)
        self.assertEqual(report[0], (1, 100))
        self.assertEqual(report[1], (2, 80))

    # Test 10: Test generate_scrum_report with no data for sprint
    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_generate_scrum_report_no_data_for_sprint(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        report = collector.generate_scrum_report(1)
        
        # Verify that an empty report is returned
        self.assertEqual(report, [])

    # Test 11: Test close method
    def test_close_method(self):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # The close method should not raise any exceptions
        try:
            collector.close()
        except Exception as e:
            self.fail(f"close() method raised an exception: {e}")

    # Test 12: Test create_scrum_workflow_tables with permission error
    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_create_scrum_workflow_tables_permission_error(self, mock_open_file, mock_exists):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Verify that the exception is raised
        with self.assertRaises(PermissionError) as context:
            collector.create_scrum_workflow_tables()
        
        self.assertIn("Permission denied", str(context.exception))

    # Test 13: Test update_scrum_task with unicode data
    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_update_scrum_task_unicode_data(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Mock the file operations
        mock_file_handle = mock_open_file.return_value
        mock_file_handle.read.return_value = '[]'
        
        collector.update_scrum_task(1, 1, "مهمة جديدة", "لتنفيذ", "عالية", 0)  # "New Task", "To Do", "High" in Arabic
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_with(collector.scrum_tasks_file, 'r+', encoding='utf-8')

    # Test 14: Test update_scrum_task with special characters
    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_update_scrum_task_special_characters(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Mock the file operations
        mock_file_handle = mock_open_file.return_value
        mock_file_handle.read.return_value = '[]'
        
        collector.update_scrum_task(1, 1, "Task!@#$%^&*()", "status\nwith\nnewlines", "priority\twith\tabs", 0)
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_with(collector.scrum_tasks_file, 'r+', encoding='utf-8')

    # Test 15: Test update_scrum_burndown with unicode data
    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_update_scrum_burndown_unicode_data(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Mock the file operations
        mock_file_handle = mock_open_file.return_value
        mock_file_handle.read.return_value = '[]'
        
        collector.update_scrum_burndown(1, 1, 100)
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_with(collector.scrum_burndown_file, 'r+', encoding='utf-8')

    # Test 16: Test update_scrum_burndown with special characters
    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_update_scrum_burndown_special_characters(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Mock the file operations
        mock_file_handle = mock_open_file.return_value
        mock_file_handle.read.return_value = '[]'
        
        collector.update_scrum_burndown(1, 1, 100)
        
        # Verify that open was called with correct parameters
        mock_open_file.assert_called_with(collector.scrum_burndown_file, 'r+', encoding='utf-8')

    # Test 17: Test generate_scrum_report with unicode data
    @patch("builtins.open", new_callable=mock_open)
    def test_generate_scrum_report_unicode_data(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Mock the file operations with unicode burndown data
        unicode_burndown = [
            {
                "sprint_id": 1,
                "day": 1,
                "remaining_work": 100
            }
        ]
        mock_open_file.return_value.read.return_value = json.dumps(unicode_burndown)
        
        report = collector.generate_scrum_report(1)
        
        # Verify that the report is correctly generated
        self.assertEqual(len(report), 1)
        self.assertEqual(report[0], (1, 100))

    # Test 18: Test generate_scrum_report with large data
    @patch("builtins.open", new_callable=mock_open)
    def test_generate_scrum_report_large_data(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Create large burndown data with 1000 entries
        large_burndown = []
        for i in range(1000):
            large_burndown.append({
                "sprint_id": 1,
                "day": i + 1,
                "remaining_work": 1000 - i
            })
        
        mock_open_file.return_value.read.return_value = json.dumps(large_burndown)
        
        report = collector.generate_scrum_report(1)
        
        # Verify that the report is correctly generated
        self.assertEqual(len(report), 1000)
        self.assertEqual(report[0], (1, 1000))
        self.assertEqual(report[999], (1000, 0))

    # Test 19: Test update_scrum_task with file not found
    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_update_scrum_task_file_not_found(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Verify that the exception is raised
        with self.assertRaises(FileNotFoundError) as context:
            collector.update_scrum_task(1, 1, "Task", "todo", "high", 0)
        
        self.assertIn("File not found", str(context.exception))

    # Test 20: Test update_scrum_burndown with file not found
    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_update_scrum_burndown_file_not_found(self, mock_open_file):
        from project_management.modules.main_modules.workflow_data_collector import WorkflowDataCollector
        collector = WorkflowDataCollector()
        
        # Verify that the exception is raised
        with self.assertRaises(FileNotFoundError) as context:
            collector.update_scrum_burndown(1, 1, 100)
        
        self.assertIn("File not found", str(context.exception))

if __name__ == "__main__":
    unittest.main()
