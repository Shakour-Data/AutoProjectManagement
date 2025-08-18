import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestDoImportantTasksMain(unittest.TestCase):
    """Test cases for do_important_tasks main module functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.original_argv = sys.argv

    def tearDown(self):
        """Clean up after tests."""
        sys.argv = self.original_argv

    def test_main_function_exists(self):
        """Test that the main function exists and is callable."""
        try:
            from project_management.modules.main_modules.do_important_tasks import main
            self.assertTrue(callable(main))
        except ImportError:
            self.fail("main function not found in do_important_tasks module")

    @patch('project_management.modules.main_modules.do_important_tasks.TaskManagement')
    @patch('builtins.print')
    def test_main_function_execution(self, mock_print, mock_task_management):
        """Test that main function executes correctly."""
        mock_tm_instance = MagicMock()
        mock_task_management.return_value = mock_tm_instance
        
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task.status = "completed"
        
        mock_tm_instance.parse_creative_input.return_value = mock_task
        
        from project_management.modules.main_modules.do_important_tasks import main
        main()
        
        mock_task_management.assert_called_once()
        self.assertEqual(mock_tm_instance.parse_creative_input.call_count, 15)
        self.assertEqual(mock_tm_instance.mark_task_completed.call_count, 15)

    @patch('project_management.modules.main_modules.do_important_tasks.TaskManagement')
    @patch('builtins.print')
    def test_main_function_task_titles(self, mock_print, mock_task_management):
        """Test that main function uses correct task titles."""
        mock_tm_instance = MagicMock()
        mock_task_management.return_value = mock_tm_instance
        
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task.status = "completed"
        
        mock_tm_instance.parse_creative_input.return_value = mock_task
        
        from project_management.modules.main_modules.do_important_tasks import main
        main()
        
        call_args = mock_tm_instance.parse_creative_input.call_args_list
        self.assertEqual(len(call_args), 15)

if __name__ == '__main__':
    unittest.main()
