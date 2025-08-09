import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestCheckProgressDashboardUpdate(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        pass

    # Test 1: Test read_file with existing file
    @patch("builtins.open", new_callable=mock_open, read_data="test content")
    @patch("os.path.exists", return_value=True)
    def test_read_file_existing(self, mock_exists, mock_open_file):
        from project_management.modules.main_modules.check_progress_dashboard_update import read_file
        result = read_file("test_path.md")
        self.assertEqual(result, "test content")
        mock_open_file.assert_called_once_with("test_path.md", 'r', encoding='utf-8')

    # Test 2: Test read_file with non-existing file
    @patch("os.path.exists", return_value=False)
    def test_read_file_non_existing(self, mock_exists):
        from project_management.modules.main_modules.check_progress_dashboard_update import read_file
        result = read_file("nonexistent_path.md")
        self.assertEqual(result, "")

    # Test 3: Test read_file with permission error
    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    @patch("os.path.exists", return_value=True)
    def test_read_file_permission_error(self, mock_exists, mock_open_file):
        from project_management.modules.main_modules.check_progress_dashboard_update import read_file
        result = read_file("test_path.md")
        self.assertEqual(result, "")

    # Test 4: Test main function execution
    @patch("project_management.modules.main_modules.check_progress_dashboard_update.read_file")
    @patch("project_management.modules.main_modules.progress_report.generate_report")
    @patch("project_management.modules.main_modules.task_management.TaskManagement")
    @patch("builtins.print")
    def test_main_execution_no_changes(self, mock_print, mock_task_management, mock_generate_report, mock_read_file):
        # Mock read_file to return the same content before and after
        mock_read_file.return_value = "same content"
        
        # Import and run main
        from project_management.modules.main_modules.check_progress_dashboard_update import main
        main()
        
        # Verify that the correct messages were printed
        mock_print.assert_any_call("Content length after update:", 12)
        mock_print.assert_any_call("No changes detected in progress_dashboard.md after update.")

    # Test 5: Test main function execution with changes
    @patch("project_management.modules.main_modules.check_progress_dashboard_update.read_file")
    @patch("project_management.modules.main_modules.progress_report.generate_report")
    @patch("project_management.modules.main_modules.task_management.TaskManagement")
    @patch("builtins.print")
    def test_main_execution_with_changes(self, mock_print, mock_task_management, mock_generate_report, mock_read_file):
        # Mock read_file to return different content before and after
        mock_read_file.side_effect = ["before content", "after content"]
        
        # Import and run main
        from project_management.modules.main_modules.check_progress_dashboard_update import main
        main()
        
        # Verify that the correct messages were printed
        mock_print.assert_any_call("progress_dashboard.md updated successfully.")

    # Test 6: Test main function with file not found
    @patch("project_management.modules.main_modules.check_progress_dashboard_update.read_file", side_effect=Exception("File not found"))
    @patch("project_management.modules.main_modules.progress_report.generate_report")
    @patch("project_management.modules.main_modules.task_management.TaskManagement")
    @patch("builtins.print")
    def test_main_execution_file_error(self, mock_print, mock_task_management, mock_generate_report, mock_read_file):
        # Import and run main
        from project_management.modules.main_modules.check_progress_dashboard_update import main
        main()
        
        # Verify that error handling occurred
        # Note: The actual behavior depends on how exceptions are handled in the main function

    # Test 7: Test main function with empty files
    @patch("project_management.modules.main_modules.check_progress_dashboard_update.read_file")
    @patch("project_management.modules.main_modules.progress_report.generate_report")
    @patch("project_management.modules.main_modules.task_management.TaskManagement")
    @patch("builtins.print")
    def test_main_execution_empty_files(self, mock_print, mock_task_management, mock_generate_report, mock_read_file):
        # Mock read_file to return empty content
        mock_read_file.return_value = ""
        
        # Import and run main
        from project_management.modules.main_modules.check_progress_dashboard_update import main
        main()
        
        # Verify that the correct messages were printed
        mock_print.assert_any_call("Content length before update:", 0)
        mock_print.assert_any_call("Content length after update:", 0)
        mock_print.assert_any_call("No changes detected in progress_dashboard.md after update.")

    # Test 8: Test main function with TaskManagement initialization
    @patch("project_management.modules.main_modules.check_progress_dashboard_update.read_file")
    @patch("project_management.modules.main_modules.progress_report.generate_report")
    @patch("project_management.modules.main_modules.task_management.TaskManagement")
    @patch("builtins.print")
    def test_main_execution_task_management(self, mock_print, mock_task_management, mock_generate_report, mock_read_file):
        # Mock read_file to return different content
        mock_read_file.side_effect = ["before", "after"]
        
        # Configure the mock TaskManagement
        mock_task_instance = mock_task_management.return_value
        mock_task_instance.generate_wbs_from_idea.return_value = []
        
        # Import and run main
        from project_management.modules.main_modules.check_progress_dashboard_update import main
        main()
        
        # Verify that TaskManagement methods were called
        mock_task_management.assert_called_once()
        mock_task_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")

    # Test 9: Test main function with generate_report
    @patch("project_management.modules.main_modules.check_progress_dashboard_update.read_file")
    @patch("project_management.modules.main_modules.progress_report.generate_report")
    @patch("project_management.modules.main_modules.task_management.TaskManagement")
    @patch("builtins.print")
    def test_main_execution_generate_report_called(self, mock_print, mock_task_management, mock_generate_report, mock_read_file):
        # Mock read_file to return different content
        mock_read_file.side_effect = ["before", "after"]
        
        # Import and run main
        from project_management.modules.main_modules.check_progress_dashboard_update import main
        main()
        
        # Verify that generate_report was called
        mock_generate_report.assert_called_once()

    # Test 10: Test main function with unicode content
    @patch("project_management.modules.main_modules.check_progress_dashboard_update.read_file")
    @patch("project_management.modules.main_modules.progress_report.generate_report")
    @patch("project_management.modules.main_modules.task_management.TaskManagement")
    @patch("builtins.print")
    def test_main_execution_unicode_content(self, mock_print, mock_task_management, mock_generate_report, mock_read_file):
        # Mock read_file to return unicode content
        mock_read_file.side_effect = ["محتوى بالعربية", "محتوى بالعربية محدث"]
        
        # Import and run main
        from project_management.modules.main_modules.check_progress_dashboard_update import main
        main()
        
        # Verify that the function handles unicode content
        mock_print.assert_any_call("progress_dashboard.md updated successfully.")

if __name__ == "__main__":
    unittest.main()
