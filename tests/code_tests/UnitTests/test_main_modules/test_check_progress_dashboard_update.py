"""
Professional test suite for check_progress_dashboard_update module.

This module tests the functionality of checking and updating progress dashboard,
including file operations and integration with task management and progress reporting.
"""

import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from autoprojectmanagement.main_modules.check_progress_dashboard_update import (
    read_file,
    main
)


class TestReadFile:
    """Test cases for the read_file utility function."""
    
    def test_read_existing_file_success(self):
        """Test reading an existing file with UTF-8 encoding."""
        test_content = "Test content with unicode: مرحبا"
        mock_file = mock_open(read_data=test_content)
        
        with patch('builtins.open', mock_file):
            with patch('pathlib.Path.exists', return_value=True):
                result = read_file("test_path.md")
        
        assert result == test_content
        mock_file.assert_called_once_with("test_path.md", 'r', encoding='utf-8')
    
    def test_read_nonexistent_file_returns_empty_string(self):
        """Test reading a non-existent file returns empty string."""
        with patch('pathlib.Path.exists', return_value=False):
            result = read_file("nonexistent.md")
        
        assert result == ""
    
    def test_read_file_permission_error_returns_empty_string(self):
        """Test handling permission errors gracefully."""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', side_effect=PermissionError("Access denied")):
                result = read_file("protected.md")
        
        assert result == ""
    
    def test_read_file_unicode_decode_error(self):
        """Test handling unicode decode errors."""
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid")):
                result = read_file("corrupted.md")
        
        assert result == ""


class TestMainFunction:
    """Test cases for the main function integration."""
    
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.read_file')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.TaskManagement')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.generate_report')
    @patch('builtins.print')
    def test_main_no_changes_detected(self, mock_print, mock_generate_report, 
                                    mock_task_management, mock_read_file):
        """Test main function when no changes are detected."""
        mock_read_file.return_value = "same content"
        mock_task_instance = MagicMock()
        mock_task_management.return_value = mock_task_instance
        
        main()
        
        mock_read_file.assert_called_with("docs/project_management/progress_dashboard.md")
        mock_task_management.assert_called_once()
        mock_task_instance.generate_wbs_from_idea.assert_called_once_with(
            "Develop Project Management Tool"
        )
        mock_generate_report.assert_called_once_with(mock_task_instance)
        
        # Verify output messages
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "Content length before update: 12" in print_calls
        assert "Content length after update: 12" in print_calls
        assert "No changes detected in progress_dashboard.md after update." in print_calls
    
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.read_file')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.TaskManagement')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.generate_report')
    @patch('builtins.print')
    def test_main_with_changes_detected(self, mock_print, mock_generate_report,
                                      mock_task_management, mock_read_file):
        """Test main function when changes are detected."""
        mock_read_file.side_effect = ["before content", "after content"]
        mock_task_instance = MagicMock()
        mock_task_management.return_value = mock_task_instance
        
        main()
        
        assert mock_read_file.call_count == 2
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "progress_dashboard.md updated successfully." in print_calls
    
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.read_file')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.TaskManagement')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.generate_report')
    @patch('builtins.print')
    def test_main_with_empty_files(self, mock_print, mock_generate_report,
                                 mock_task_management, mock_read_file):
        """Test main function with empty files."""
        mock_read_file.return_value = ""
        mock_task_instance = MagicMock()
        mock_task_management.return_value = mock_task_instance
        
        main()
        
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "Content length before update: 0" in print_calls
        assert "Content length after update: 0" in print_calls
    
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.read_file')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.TaskManagement')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.generate_report')
    @patch('builtins.print')
    def test_main_with_unicode_content(self, mock_print, mock_generate_report,
                                     mock_task_management, mock_read_file):
        """Test main function handles unicode content correctly."""
        unicode_content = "محتوى بالعربية"
        mock_read_file.side_effect = [unicode_content, unicode_content + " محدث"]
        mock_task_instance = MagicMock()
        mock_task_management.return_value = mock_task_instance
        
        main()
        
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "progress_dashboard.md updated successfully." in print_calls
    
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.read_file')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.TaskManagement')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.generate_report')
    @patch('builtins.print')
    def test_main_exception_handling(self, mock_print, mock_generate_report,
                                   mock_task_management, mock_read_file):
        """Test main function handles exceptions gracefully."""
        mock_read_file.side_effect = Exception("Unexpected error")
        
        # Should not raise exception
        main()
        
        # Verify error was handled gracefully
        mock_task_management.assert_not_called()
        mock_generate_report.assert_not_called()


class TestIntegrationScenarios:
    """Test complex integration scenarios."""
    
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.read_file')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.TaskManagement')
    @patch('autoprojectmanagement.main_modules.check_progress_dashboard_update.generate_report')
    @patch('builtins.print')
    def test_full_workflow_simulation(self, mock_print, mock_generate_report,
                                    mock_task_management, mock_read_file):
        """Test complete workflow simulation."""
        # Simulate file changes during processing
        mock_read_file.side_effect = [
            "initial content",
            "updated content with new progress"
        ]
        
        mock_task_instance = MagicMock()
        mock_task_instance.generate_wbs_from_idea.return_value = [
            MagicMock(id=1, title="Task 1"),
            MagicMock(id=2, title="Task 2")
        ]
        mock_task_management.return_value = mock_task_instance
        
        main()
        
        # Verify complete workflow
        assert mock_read_file.call_count == 2
        mock_task_instance.generate_wbs_from_idea.assert_called_once()
        mock_generate_report.assert_called_once_with(mock_task_instance)
        
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert any("updated successfully" in str(call) for call in print_calls)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
