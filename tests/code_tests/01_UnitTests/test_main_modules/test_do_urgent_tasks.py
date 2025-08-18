import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestDoUrgentTasks(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        pass

    # Test 1: Test main function execution
    @patch('project_management.modules.main_modules.do_urgent_tasks.TaskManagement')
    @patch('builtins.print')
    def test_main_execution(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.do_urgent_tasks import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        mock_tm_instance.parse_creative_input.side_effect = lambda title: MagicMock(id=1, title=title, status='pending')
        mock_tm_instance.mark_task_completed = MagicMock()
        
        main()
        
        # Verify that parse_creative_input was called exactly 15 times
        self.assertEqual(mock_tm_instance.parse_creative_input.call_count, 15)
        
        # Verify that mark_task_completed was called exactly 15 times
        self.assertEqual(mock_tm_instance.mark_task_completed.call_count, 15)
        
        # Verify that print was called for each task + 1 for summary
        self.assertEqual(mock_print.call_count, 16)

    # Test 2: Test task creation with specific titles
    @patch('project_management.modules.main_modules.do_urgent_tasks.TaskManagement')
    @patch('builtins.print')
    def test_task_creation_with_titles(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.do_urgent_tasks import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        mock_tm_instance.parse_creative_input.side_effect = lambda title: MagicMock(id=1, title=title, status='pending')
        mock_tm_instance.mark_task_completed = MagicMock()
        
        main()
        
        # Verify that parse_creative_input was called with expected titles
        calls = mock_tm_instance.parse_creative_input.call_args_list
        titles = [call[0][0] for call in calls]
        
        # Check that all expected titles are present
        expected_titles = [
            "Develop Project Management Tool",
            "Develop Project Management Tool - Subtask Level 1.1",
            "Develop Project Management Tool - Subtask Level 1.3",
            "Develop Project Management Tool - Subtask Level 1.2",
            "Develop Project Management Tool - Subtask Level 2.1.1",
            "Develop Project Management Tool - Subtask Level 2.1.2",
            "Develop Project Management Tool - Subtask Level 2.3.2",
            "Develop Project Management Tool - Subtask Level 2.2.1",
            "Develop Project Management Tool - Subtask Level 2.2.2",
            "Develop Project Management Tool - Subtask Level 2.3.1",
            "Develop Project Management Tool - Subtask Level 3.1.1",
            "Develop Project Management Tool - Subtask Level 3.1.2",
            "Develop Project Management Tool - Subtask Level 3.2.1",
            "Develop Project Management Tool - Subtask Level 3.2.2",
            "Develop Project Management Tool - Subtask Level 3.3.1",
        ]
        
        for title in expected_titles:
            self.assertIn(title, titles)

    # Test 3: Test task completion marking
    @patch('project_management.modules.main_modules.do_urgent_tasks.TaskManagement')
    @patch('builtins.print')
    def test_task_completion_marking(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.do_urgent_tasks import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        mock_task = MagicMock(id=1, title="Test Task", status='pending')
        mock_tm_instance.parse_creative_input.return_value = mock_task
        mock_tm_instance.mark_task_completed = MagicMock()
        
        main()
        
        # Verify that mark_task_completed was called with task IDs
        calls = mock_tm_instance.mark_task_completed.call_args_list
        # Since all tasks have the same ID in our mock, we just check that it was called 15 times
        self.assertEqual(len(calls), 15)

    # Test 4: Test print output for completed tasks
    @patch('project_management.modules.main_modules.do_urgent_tasks.TaskManagement')
    @patch('builtins.print')
    def test_print_output_for_completed_tasks(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.do_urgent_tasks import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        mock_task = MagicMock(id=1, title="Test Task", status='pending')
        mock_tm_instance.parse_creative_input.return_value = mock_task
        mock_tm_instance.mark_task_completed = MagicMock()
        
        main()
        
        # Verify that print was called with expected messages
        calls = mock_print.call_args_list
        # First call should be the summary
        self.assertEqual(calls[0][0][0], "Completed 15 urgent tasks:")
        
        # Subsequent calls should contain task information
        for i in range(1, 16):
            self.assertIn("Task ID:", calls[i][0][0])
            self.assertIn("Title:", calls[i][0][0])
            self.assertIn("Status:", calls[i][0][0])

    # Test 5: Test exception handling when TaskManagement fails
    @patch('project_management.modules.main_modules.do_urgent_tasks.TaskManagement')
    @patch('builtins.print')
    def test_exception_handling_task_management_failure(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.do_urgent_tasks import main
        
        # Setup mock TaskManagement to raise an exception
        mock_task_management.side_effect = Exception("TaskManagement initialization failed")
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            main()
        
        self.assertIn("TaskManagement initialization failed", str(context.exception))

    # Test 6: Test exception handling when parse_creative_input fails
    @patch('project_management.modules.main_modules.do_urgent_tasks.TaskManagement')
    @patch('builtins.print')
    def test_exception_handling_parse_creative_input_failure(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.do_urgent_tasks import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        mock_tm_instance.parse_creative_input.side_effect = Exception("Failed to parse creative input")
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            main()
        
        self.assertIn("Failed to parse creative input", str(context.exception))

    # Test 7: Test exception handling when mark_task_completed fails
    @patch('project_management.modules.main_modules.do_urgent_tasks.TaskManagement')
    @patch('builtins.print')
    def test_exception_handling_mark_task_completed_failure(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.do_urgent_tasks import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        mock_tm_instance.parse_creative_input.side_effect = lambda title: MagicMock(id=1, title=title, status='pending')
        mock_tm_instance.mark_task_completed.side_effect = Exception("Failed to mark task as completed")
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            main()
        
        self.assertIn("Failed to mark task as completed", str(context.exception))

if __name__ == "__main__":
    unittest.main()
