import unittest
from unittest.mock import patch, mock_open
import json
import os
from datetime import datetime

# Add the project root to the path so we can import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestCommitProgressManager(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        pass

    # Test 1: Test initialization with default paths
    def test_init_default_paths(self):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        self.assertEqual(manager.commit_task_db_path, 'JSonDataBase/OutPuts/commit_task_database.json')
        self.assertEqual(manager.commit_progress_path, 'JSonDataBase/OutPuts/commit_progress.json')
        self.assertEqual(manager.commit_task_db, {})
        self.assertEqual(manager.commit_progress, {})

    # Test 2: Test initialization with custom paths
    def test_init_custom_paths(self):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager('custom_db.json', 'custom_progress.json')
        self.assertEqual(manager.commit_task_db_path, 'custom_db.json')
        self.assertEqual(manager.commit_progress_path, 'custom_progress.json')

    # Test 3: Test load_commit_task_db with existing file
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"commit1": {"task_id": "task1", "commit_date": "2023-01-01T12:00:00"}}')
    def test_load_commit_task_db_existing(self, mock_open_file, mock_exists):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.load_commit_task_db()
        self.assertIn("commit1", manager.commit_task_db)
        self.assertEqual(manager.commit_task_db["commit1"]["task_id"], "task1")

    # Test 4: Test load_commit_task_db with non-existing file
    @patch("os.path.exists", return_value=False)
    def test_load_commit_task_db_non_existing(self, mock_exists):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.load_commit_task_db()
        self.assertEqual(manager.commit_task_db, {})

    # Test 5: Test load_commit_task_db with invalid JSON
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    @patch("json.load", side_effect=json.JSONDecodeError("Invalid JSON", "", 0))
    def test_load_commit_task_db_invalid_json(self, mock_json_load, mock_open_file, mock_exists):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.load_commit_task_db()
        self.assertEqual(manager.commit_task_db, {})

    # Test 6: Test generate_commit_progress with valid data
    def test_generate_commit_progress_valid_data(self):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1", "commit_date": "2023-01-01T12:00:00"},
            "commit2": {"task_id": "task1", "commit_date": "2023-01-02T12:00:00"},
            "commit3": {"task_id": "task2", "commit_date": "2023-01-01T12:00:00"}
        }
        manager.generate_commit_progress()
        self.assertIn("task1", manager.commit_progress)
        self.assertIn("task2", manager.commit_progress)
        self.assertEqual(manager.commit_progress["task1"]["commit_count"], 2)
        self.assertEqual(manager.commit_progress["task2"]["commit_count"], 1)

    # Test 7: Test generate_commit_progress with empty data
    def test_generate_commit_progress_empty_data(self):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_task_db = {}
        manager.generate_commit_progress()
        self.assertEqual(manager.commit_progress, {})

    # Test 8: Test generate_commit_progress with missing task_id
    def test_generate_commit_progress_missing_task_id(self):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"commit_date": "2023-01-01T12:00:00"}  # Missing task_id
        }
        manager.generate_commit_progress()
        self.assertEqual(manager.commit_progress, {})

    # Test 9: Test generate_commit_progress with missing commit_date
    def test_generate_commit_progress_missing_commit_date(self):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1"}  # Missing commit_date
        }
        manager.generate_commit_progress()
        self.assertEqual(manager.commit_progress, {})

    # Test 10: Test generate_commit_progress with invalid date format
    @patch("datetime.datetime.strptime", side_effect=ValueError("Invalid date format"))
    def test_generate_commit_progress_invalid_date(self, mock_strptime):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1", "commit_date": "invalid-date"}
        }
        manager.generate_commit_progress()
        self.assertEqual(manager.commit_progress, {})

    # Test 11: Test generate_commit_progress progress percentage calculation
    def test_generate_commit_progress_percentage_calculation(self):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        # Create 15 commits for a single task to test the 100% cap
        manager.commit_task_db = {
            f"commit{i}": {"task_id": "task1", "commit_date": f"2023-01-01T12:00:00"}
            for i in range(15)
        }
        manager.generate_commit_progress()
        # Progress should be capped at 100% (15 commits * 10 = 150, but capped at 100)
        self.assertEqual(manager.commit_progress["task1"]["progress_percent"], 100)

    # Test 12: Test save_commit_progress with valid data
    @patch("builtins.open", new_callable=mock_open)
    def test_save_commit_progress_valid_data(self, mock_open_file):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_progress = {
            "task1": {
                "commit_count": 5,
                "last_commit_date": "2023-01-02T12:00:00",
                "progress_percent": 50
            }
        }
        manager.save_commit_progress()
        mock_open_file.assert_called_once_with('JSonDataBase/OutPuts/commit_progress.json', 'w', encoding='utf-8')

    # Test 13: Test save_commit_progress with permission error
    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_save_commit_progress_permission_error(self, mock_open_file):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_progress = {"task1": {"commit_count": 1, "last_commit_date": "2023-01-01T12:00:00", "progress_percent": 10}}
        with self.assertRaises(PermissionError):
            manager.save_commit_progress()

    # Test 14: Test save_commit_progress with unicode data
    @patch("builtins.open", new_callable=mock_open)
    def test_save_commit_progress_unicode_data(self, mock_open_file):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_progress = {
            "وظيفة1": {  # Arabic task ID
                "commit_count": 5,
                "last_commit_date": "2023-01-02T12:00:00",
                "progress_percent": 50
            }
        }
        manager.save_commit_progress()
        mock_open_file.assert_called_once_with('JSonDataBase/OutPuts/commit_progress.json', 'w', encoding='utf-8')

    # Test 15: Test run method execution
    @patch("project_management.modules.main_modules.commit_progress_manager.CommitProgressManager.load_commit_task_db")
    @patch("project_management.modules.main_modules.commit_progress_manager.CommitProgressManager.generate_commit_progress")
    @patch("project_management.modules.main_modules.commit_progress_manager.CommitProgressManager.save_commit_progress")
    @patch("builtins.print")
    def test_run_method(self, mock_print, mock_save, mock_generate, mock_load):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.run()
        mock_load.assert_called_once()
        mock_generate.assert_called_once()
        mock_save.assert_called_once()
        mock_print.assert_called_once_with(f"Commit progress saved to JSonDataBase/OutPuts/commit_progress.json")

    # Test 16: Test run method with custom paths
    @patch("project_management.modules.main_modules.commit_progress_manager.CommitProgressManager.load_commit_task_db")
    @patch("project_management.modules.main_modules.commit_progress_manager.CommitProgressManager.generate_commit_progress")
    @patch("project_management.modules.main_modules.commit_progress_manager.CommitProgressManager.save_commit_progress")
    @patch("builtins.print")
    def test_run_method_custom_paths(self, mock_print, mock_save, mock_generate, mock_load):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager('custom_db.json', 'custom_progress.json')
        manager.run()
        mock_print.assert_called_once_with(f"Commit progress saved to custom_progress.json")

    # Test 17: Test last commit date selection
    def test_last_commit_date_selection(self):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1", "commit_date": "2023-01-01T12:00:00"},
            "commit2": {"task_id": "task1", "commit_date": "2023-01-03T12:00:00"},  # Latest date
            "commit3": {"task_id": "task1", "commit_date": "2023-01-02T12:00:00"}
        }
        manager.generate_commit_progress()
        # The last commit date should be the latest one
        expected_last_date = datetime.strptime("2023-01-03T12:00:00", '%Y-%m-%dT%H:%M:%S').isoformat()
        self.assertEqual(manager.commit_progress["task1"]["last_commit_date"], expected_last_date)

    # Test 18: Test multiple tasks with different commit counts
    def test_multiple_tasks_different_commit_counts(self):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1", "commit_date": "2023-01-01T12:00:00"},
            "commit2": {"task_id": "task2", "commit_date": "2023-01-01T12:00:00"},
            "commit3": {"task_id": "task2", "commit_date": "2023-01-02T12:00:00"},
            "commit4": {"task_id": "task2", "commit_date": "2023-01-03T12:00:00"}
        }
        manager.generate_commit_progress()
        self.assertEqual(manager.commit_progress["task1"]["commit_count"], 1)
        self.assertEqual(manager.commit_progress["task2"]["commit_count"], 3)
        # Progress percentages should be different
        self.assertEqual(manager.commit_progress["task1"]["progress_percent"], 10)
        self.assertEqual(manager.commit_progress["task2"]["progress_percent"], 30)

    # Test 19: Test edge case with zero commits
    def test_zero_commits_edge_case(self):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_task_db = {}
        manager.generate_commit_progress()
        self.assertEqual(len(manager.commit_progress), 0)

    # Test 20: Test with malformed commit data
    def test_malformed_commit_data(self):
        from project_management.modules.main_modules.commit_progress_manager import CommitProgressManager
        manager = CommitProgressManager()
        manager.commit_task_db = {
            "commit1": {"task_id": "task1"},  # Missing commit_date
            "commit2": {"commit_date": "2023-01-01T12:00:00"},  # Missing task_id
            "commit3": {}  # Missing both
        }
        manager.generate_commit_progress()
        self.assertEqual(manager.commit_progress, {})

if __name__ == "__main__":
    unittest.main()
