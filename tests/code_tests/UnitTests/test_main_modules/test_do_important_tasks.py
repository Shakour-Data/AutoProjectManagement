import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestDoImportantTasks(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        pass

    # Test 1: Test main function execution
    @patch('project_management.modules.main_modules.do_important_tasks.TaskManagement')
    @patch('builtins.print')
    def test_main_execution(self, mock_print, mock_task_management):
        from project_management.modules.main_modules.do_important_tasks import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        mock_tm_instance.parse_creative_input.side_effect = lambda title: MagicMock(id=1, title=title, status='pending')
        mock_tm_instance.mark_task_completed = MagicMock()
        
        main()
        
        # Verify that parse_creative_input was called multiple times
        self.assertTrue(mock_tm_instance.parse_creative_input.call_count >= 15)
        
        # Verify that mark_task_completed was called for each task
        self.assertTrue(mock_tm_instance.mark_task_completed.call_count >= 15)
        
        # Verify that print was called for each task
        self.assertTrue(mock_print.call_count >= 16)  # 1 for summary + 15 for tasks

if __name__ == "__main__":
    unittest.main()
