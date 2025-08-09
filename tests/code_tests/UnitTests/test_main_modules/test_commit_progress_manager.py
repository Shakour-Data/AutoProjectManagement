"""
Professional test suite for commit_progress_manager module.

This module provides comprehensive testing for CommitProgressManager class,
including commit tracking, progress management, and JSON file handling.
"""

import pytest
from datetime import datetime
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

from autoprojectmanagement.main_modules.commit_progress_manager import CommitProgressManager


class TestCommitProgressManagerInitialization:
    """Test cases for CommitProgressManager initialization."""
    
    def test_init_default_paths(self):
        """Test initialization with default paths."""
        manager = CommitProgressManager()
        assert manager.commit_task_db_path == 'JSonDataBase/OutPuts/commit_task_database.json'
        assert manager.commit_progress_path == 'JSonDataBase/OutPuts/commit_progress.json'
        assert manager.commit_task_db == {}
        assert manager.commit_progress == {}
    
    def test_init_custom_paths(self):
        """Test initialization with custom paths."""
        manager = CommitProgressManager('custom_db.json', 'custom_progress.json')
        assert manager.commit_task_db_path == 'custom_db.json'
        assert manager.commit_progress_path == 'custom_progress.json'


class TestLoadCommitTaskDb:
    """Test cases for loading commit task database."""
    
    def test_load_existing_file(self):
        """Test loading from existing file."""
        test_data = {
            "commit1": {"task_id": "task1", "commit_date": "2023-01-01T12:00:00"},
            "commit2": {"task_id": "task1", "commit_date": "2023-01-02T12:00:00"}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name
        
        try:
            manager = CommitProgressManager(temp_file, 'dummy.json')
            manager.load_commit_task_db()
            assert "commit1" in manager.commit_task_db
            assert manager.commit_task_db["commit1"]["task_id"] == "task1"
            assert manager.commit_task_db["commit1"]["commit_date"] == "2023-01-01T12:00:00"
        finally:
            Path(temp_file).unlink()
    
    def test_load_nonexistent_file(self):
        """Test loading from non-existent file."""
        manager = CommitProgressManager('nonexistent.json', 'dummy.json')
        manager.load_commit_task_db()
        assert manager.commit_task_db == {}
    
    def test_load_invalid_json(self):
        """Test handling invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('invalid json content')
            temp_file = f.name
        
        try:
            manager = CommitProgressManager(temp_file, 'dummy.json')
            manager.load_commit_task_db()
            assert manager.commit_task_db == {}
        finally:
            Path(temp_file).unlink()
    
    def test_load_empty_file(self):
        """Test loading from empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('')
            temp_file = f.name
        
        try:
            manager = CommitProgressManager(temp_file, 'dummy.json')
            manager.load_commit_task_db()
            assert manager.commit_task_db == {}
        finally:
            Path(temp_file).unlink()


class TestGenerateCommitProgress:
    """Test cases for generating commit progress."""
    
    def test_generate_with_valid_data(self):
        """Test generating progress with valid commit data."""
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1", "commit_date": "2023-01-01T12:00:00"},
            "commit2": {"task_id": "task1", "commit_date": "2023-01-02T12:00:00"},
            "commit3": {"task_id": "task2", "commit_date": "2023-01-01T12:00:00"}
        }
        
        manager.generate_commit_progress()
        
        assert "task1" in manager.commit_progress
        assert "task2" in manager.commit_progress
        assert manager.commit_progress["task1"]["commit_count"] == 2
        assert manager.commit_progress["task2"]["commit_count"] == 1
        assert manager.commit_progress["task1"]["progress_percent"] == 20
        assert manager.commit_progress["task2"]["progress_percent"] == 10
    
    def test_generate_with_empty_data(self):
        """Test generating progress with empty commit data."""
        manager = CommitProgressManager()
        manager.commit_task_db = {}
        
        manager.generate_commit_progress()
        
        assert manager.commit_progress == {}
    
    def test_generate_with_missing_fields(self):
        """Test handling missing required fields."""
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1"},  # Missing commit_date
            "commit2": {"commit_date": "2023-01-01T12:00:00"},  # Missing task_id
            "commit3": {}  # Missing both
        }
        
        manager.generate_commit_progress()
        
        assert manager.commit_progress == {}
    
    def test_progress_percentage_capping(self):
        """Test that progress percentage is capped at 100%."""
        manager = CommitProgressManager()
        # Create 15 commits for a single task (15 * 10 = 150%, should cap at 100%)
        manager.commit_task_db = {
            f"commit{i}": {"task_id": "task1", "commit_date": "2023-01-01T12:00:00"}
            for i in range(15)
        }
        
        manager.generate_commit_progress()
        
        assert manager.commit_progress["task1"]["progress_percent"] == 100
    
    def test_last_commit_date_selection(self):
        """Test that the latest commit date is selected."""
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1", "commit_date": "2023-01-01T12:00:00"},
            "commit2": {"task_id": "task1", "commit_date": "2023-01-03T12:00:00"},  # Latest
            "commit3": {"task_id": "task1", "commit_date": "2023-01-02T12:00:00"}
        }
        
        manager.generate_commit_progress()
        
        expected_date = "2023-01-03T12:00:00"
        assert manager.commit_progress["task1"]["last_commit_date"] == expected_date
    
    def test_invalid_date_format(self):
        """Test handling invalid date formats."""
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1", "commit_date": "invalid-date"}
        }
        
        manager.generate_commit_progress()
        
        assert manager.commit_progress == {}
    
    def test_multiple_tasks_different_commit_counts(self):
        """Test multiple tasks with different commit counts."""
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1", "commit_date": "2023-01-01T12:00:00"},
            "commit2": {"task_id": "task2", "commit_date": "2023-01-01T12:00:00"},
            "commit3": {"task_id": "task2", "commit_date": "2023-01-02T12:00:00"},
            "commit4": {"task_id": "task2", "commit_date": "2023-01-03T12:00:00"}
        }
        
        manager.generate_commit_progress()
        
        assert manager.commit_progress["task1"]["commit_count"] == 1
        assert manager.commit_progress["task2"]["commit_count"] == 3
        assert manager.commit_progress["task1"]["progress_percent"] == 10
        assert manager.commit_progress["task2"]["progress_percent"] == 30


class TestSaveCommitProgress:
    """Test cases for saving commit progress."""
    
    def test_save_valid_data(self):
        """Test saving valid progress data."""
        manager = CommitProgressManager()
        manager.commit_progress = {
            "task1": {
                "commit_count": 5,
                "last_commit_date": "2023-01-02T12:00:00",
                "progress_percent": 50
            }
        }
        
        with patch('builtins.open', mock_open()) as mock_file:
            manager.save_commit_progress()
            mock_file.assert_called_once_with(
                'JSonDataBase/OutPuts/commit_progress.json', 'w', encoding='utf-8'
            )
    
    def test_save_unicode_data(self):
        """Test saving data with unicode characters."""
        manager = CommitProgressManager()
        manager.commit_progress = {
            "وظيفة1": {
                "commit_count": 5,
                "last_commit_date": "2023-01-02T12:00:00",
                "progress_percent": 50
            }
        }
        
        with patch('builtins.open', mock_open()) as mock_file:
            manager.save_commit_progress()
            mock_file.assert_called_once()
    
    def test_save_permission_error(self):
        """Test handling permission errors during save."""
        manager = CommitProgressManager()
        manager.commit_progress = {"task1": {"commit_count": 1, "last_commit_date": "2023-01-01T12:00:00", "progress_percent": 10}}
        
        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            with pytest.raises(PermissionError):
                manager.save_commit_progress()


class TestRunMethod:
    """Test cases for the run method."""
    
    @patch.object(CommitProgressManager, 'load_commit_task_db')
    @patch.object(CommitProgressManager, 'generate_commit_progress')
    @patch.object(CommitProgressManager, 'save_commit_progress')
    @patch('builtins.print')
    def test_run_method_execution(self, mock_print, mock_save, mock_generate, mock_load):
        """Test complete run method execution."""
        manager = CommitProgressManager()
        manager.run()
        
        mock_load.assert_called_once()
        mock_generate.assert_called_once()
        mock_save.assert_called_once()
        mock_print.assert_called_once_with(
            "Commit progress saved to JSonDataBase/OutPuts/commit_progress.json"
        )
    
    @patch.object(CommitProgressManager, 'load_commit_task_db')
    @patch.object(CommitProgressManager, 'generate_commit_progress')
    @patch.object(CommitProgressManager, 'save_commit_progress')
    @patch('builtins.print')
    def test_run_method_custom_paths(self, mock_print, mock_save, mock_generate, mock_load):
        """Test run method with custom paths."""
        manager = CommitProgressManager('custom_db.json', 'custom_progress.json')
        manager.run()
        
        mock_print.assert_called_once_with(
            "Commit progress saved to custom_progress.json"
        )


class TestEdgeCases:
    """Test edge cases and error scenarios."""
    
    def test_zero_commits(self):
        """Test with zero commits."""
        manager = CommitProgressManager()
        manager.commit_task_db = {}
        manager.generate_commit_progress()
        assert len(manager.commit_progress) == 0
    
    def test_malformed_commit_data(self):
        """Test with malformed commit data."""
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1"},  # Missing commit_date
            "commit2": {"commit_date": "2023-01-01T12:00:00"},  # Missing task_id
            "commit3": {}  # Missing both
        }
        manager.generate_commit_progress()
        assert manager.commit_progress == {}
    
    def test_unicode_task_ids(self):
        """Test with unicode task IDs."""
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "وظيفة1", "commit_date": "2023-01-01T12:00:00"},
            "commit2": {"task_id": "وظيفة1", "commit_date": "2023-01-02T12:00:00"}
        }
        manager.generate_commit_progress()
        
        assert "وظيفة1" in manager.commit_progress
        assert manager.commit_progress["وظيفة1"]["commit_count"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
