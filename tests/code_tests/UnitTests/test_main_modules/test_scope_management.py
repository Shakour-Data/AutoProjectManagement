import unittest
from unittest.mock import patch, mock_open
import json
import os

# Add the project root to the path so we can import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestScopeManagement(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        self.test_wbs = {
            "id": 1,
            "name": "Project",
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "subtasks": [
                        {
                            "id": 3,
                            "name": "Subtask 1.1"
                        }
                    ]
                },
                {
                    "id": 4,
                    "name": "Task 2"
                }
            ]
        }
        
        self.test_scope_changes = [
            {
                "task_id": 2,
                "change_type": "add",
                "details": {
                    "parent_id": 2,
                    "task": {
                        "id": 5,
                        "name": "New Subtask 1.2"
                    }
                }
            },
            {
                "task_id": 3,
                "change_type": "remove"
            },
            {
                "task_id": 4,
                "change_type": "modify",
                "details": {
                    "name": "Modified Task 2",
                    "status": "in_progress"
                }
            }
        ]

    # Test 1: Test initialization with default paths
    def test_init_default_paths(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        self.assertEqual(manager.detailed_wbs_path, 'JSonDataBase/Inputs/UserInputs/detailed_wbs.json')
        self.assertEqual(manager.scope_changes_path, 'JSonDataBase/Inputs/UserInputs/scope_changes.json')
        self.assertEqual(manager.output_path, 'JSonDataBase/OutPuts/scope_management.json')
        self.assertEqual(manager.detailed_wbs, {})
        self.assertEqual(manager.scope_changes, [])
        self.assertEqual(manager.scope_status, {})

    # Test 2: Test initialization with custom paths
    def test_init_custom_paths(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement('custom_wbs.json', 'custom_changes.json', 'custom_output.json')
        self.assertEqual(manager.detailed_wbs_path, 'custom_wbs.json')
        self.assertEqual(manager.scope_changes_path, 'custom_changes.json')
        self.assertEqual(manager.output_path, 'custom_output.json')

    # Test 3: Test load_json method with existing file
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    @patch("os.path.exists", return_value=True)
    def test_load_json_existing_file(self, mock_exists, mock_open_file):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        result = manager.load_json('test.json')
        self.assertEqual(result, {"key": "value"})
        mock_open_file.assert_called_once_with('test.json', 'r', encoding='utf-8')

    # Test 4: Test load_json method with non-existing file
    @patch("os.path.exists", return_value=False)
    def test_load_json_non_existing_file(self, mock_exists):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        result = manager.load_json('nonexistent.json')
        self.assertIsNone(result)

    # Test 5: Test save_json method
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_json(self, mock_json_dump, mock_open_file):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        test_data = {"key": "value"}
        manager.save_json(test_data, 'output.json')
        mock_open_file.assert_called_once_with('output.json', 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with(test_data, mock_open_file(), indent=2, ensure_ascii=False)

    # Test 6: Test load_inputs method
    @patch("project_management.modules.main_modules.scope_management.ScopeManagement.load_json")
    def test_load_inputs(self, mock_load_json):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        
        # Setup mock returns
        mock_load_json.side_effect = [
            self.test_wbs,  # detailed_wbs
            self.test_scope_changes  # scope_changes
        ]
        
        manager.load_inputs()
        
        # Verify load_json was called with correct paths
        calls = mock_load_json.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0][0], 'JSonDataBase/Inputs/UserInputs/detailed_wbs.json')
        self.assertEqual(calls[1][0][0], 'JSonDataBase/Inputs/UserInputs/scope_changes.json')
        
        # Verify data was loaded
        self.assertEqual(manager.detailed_wbs, self.test_wbs)
        self.assertEqual(manager.scope_changes, self.test_scope_changes)

    # Test 7: Test find_task_by_id method
    def test_find_task_by_id(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        manager.detailed_wbs = self.test_wbs
        
        # Test finding existing task
        task = manager.find_task_by_id(3)
        self.assertIsNotNone(task)
        self.assertEqual(task['id'], 3)
        self.assertEqual(task['name'], 'Subtask 1.1')
        
        # Test finding non-existing task
        task = manager.find_task_by_id(999)
        self.assertIsNone(task)

    # Test 8: Test remove_task_by_id method
    def test_remove_task_by_id(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        manager.detailed_wbs = self.test_wbs
        
        # Test removing existing task
        result = manager.remove_task_by_id(3)
        self.assertTrue(result)
        
        # Verify task was removed
        task = manager.find_task_by_id(3)
        self.assertIsNone(task)
        
        # Test removing non-existing task
        result = manager.remove_task_by_id(999)
        self.assertFalse(result)

    # Test 9: Test apply_scope_changes method with add change
    def test_apply_scope_changes_add_change(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        manager.detailed_wbs = self.test_wbs
        manager.scope_changes = [
            {
                "task_id": 5,
                "change_type": "add",
                "details": {
                    "parent_id": 2,
                    "task": {
                        "id": 5,
                        "name": "New Subtask 1.2"
                    }
                }
            }
        ]
        
        manager.apply_scope_changes()
        
        # Verify task was added
        self.assertIn(5, manager.scope_status['added_tasks'])
        # Verify task exists in WBS
        task = manager.find_task_by_id(5)
        self.assertIsNotNone(task)
        self.assertEqual(task['name'], 'New Subtask 1.2')

    # Test 10: Test apply_scope_changes method with remove change
    def test_apply_scope_changes_remove_change(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        manager.detailed_wbs = self.test_wbs
        manager.scope_changes = [
            {
                "task_id": 3,
                "change_type": "remove"
            }
        ]
        
        manager.apply_scope_changes()
        
        # Verify task was removed
        self.assertIn(3, manager.scope_status['removed_tasks'])
        # Verify task no longer exists in WBS
        task = manager.find_task_by_id(3)
        self.assertIsNone(task)

    # Test 11: Test apply_scope_changes method with modify change
    def test_apply_scope_changes_modify_change(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        manager.detailed_wbs = self.test_wbs
        manager.scope_changes = [
            {
                "task_id": 4,
                "change_type": "modify",
                "details": {
                    "name": "Modified Task 2",
                    "status": "in_progress"
                }
            }
        ]
        
        manager.apply_scope_changes()
        
        # Verify task was modified
        self.assertIn(4, manager.scope_status['modified_tasks'])
        # Verify task attributes were changed
        task = manager.find_task_by_id(4)
        self.assertEqual(task['name'], 'Modified Task 2')
        self.assertEqual(task['status'], 'in_progress')

    # Test 12: Test apply_scope_changes method with multiple changes
    def test_apply_scope_changes_multiple_changes(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        manager.detailed_wbs = self.test_wbs
        manager.scope_changes = self.test_scope_changes
        
        manager.apply_scope_changes()
        
        # Verify all changes were applied
        self.assertIn(5, manager.scope_status['added_tasks'])
        self.assertIn(3, manager.scope_status['removed_tasks'])
        self.assertIn(4, manager.scope_status['modified_tasks'])

    # Test 13: Test apply_scope_changes method with empty changes
    def test_apply_scope_changes_empty_changes(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        manager.detailed_wbs = self.test_wbs
        manager.scope_changes = []
        
        manager.apply_scope_changes()
        
        # Verify no changes were applied
        self.assertEqual(manager.scope_status['added_tasks'], [])
        self.assertEqual(manager.scope_status['removed_tasks'], [])
        self.assertEqual(manager.scope_status['modified_tasks'], [])

    # Test 14: Test apply_scope_changes method with invalid change type
    def test_apply_scope_changes_invalid_change_type(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        manager.detailed_wbs = self.test_wbs
        manager.scope_changes = [
            {
                "task_id": 1,
                "change_type": "invalid_type",
                "details": {}
            }
        ]
        
        manager.apply_scope_changes()
        
        # Verify no changes were applied
        self.assertEqual(manager.scope_status['added_tasks'], [])
        self.assertEqual(manager.scope_status['removed_tasks'], [])
        self.assertEqual(manager.scope_status['modified_tasks'], [])

    # Test 15: Test apply_scope_changes method with missing parent_id in add change
    def test_apply_scope_changes_missing_parent_id_in_add_change(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        manager.detailed_wbs = self.test_wbs
        manager.scope_changes = [
            {
                "task_id": 5,
                "change_type": "add",
                "details": {
                    "task": {
                        "id": 5,
                        "name": "New Subtask 1.2"
                    }
                }
            }
        ]
        
        manager.apply_scope_changes()
        
        # Verify no changes were applied
        self.assertEqual(manager.scope_status['added_tasks'], [])

    # Test 16: Test apply_scope_changes method with missing task in add change
    def test_apply_scope_changes_missing_task_in_add_change(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        manager.detailed_wbs = self.test_wbs
        manager.scope_changes = [
            {
                "task_id": 5,
                "change_type": "add",
                "details": {
                    "parent_id": 2
                }
            }
        ]
        
        manager.apply_scope_changes()
        
        # Verify no changes were applied
        self.assertEqual(manager.scope_status['added_tasks'], [])

    # Test 17: Test run method execution
    @patch("project_management.modules.main_modules.scope_management.ScopeManagement.load_inputs")
    @patch("project_management.modules.main_modules.scope_management.ScopeManagement.apply_scope_changes")
    @patch("project_management.modules.main_modules.scope_management.ScopeManagement.save_json")
    @patch("builtins.print")
    def test_run_method(self, mock_print, mock_save, mock_apply, mock_load):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        manager.detailed_wbs = self.test_wbs
        manager.scope_status = {
            'added_tasks': [5],
            'removed_tasks': [3],
            'modified_tasks': [4]
        }
        
        manager.run()
        
        # Verify methods were called
        mock_load.assert_called_once()
        mock_apply.assert_called_once()
        mock_save.assert_called_once_with(manager.detailed_wbs, manager.output_path)
        self.assertEqual(mock_print.call_count, 2)

    # Test 18: Test run method with custom paths
    @patch("project_management.modules.main_modules.scope_management.ScopeManagement.load_inputs")
    @patch("project_management.modules.main_modules.scope_management.ScopeManagement.apply_scope_changes")
    @patch("project_management.modules.main_modules.scope_management.ScopeManagement.save_json")
    @patch("builtins.print")
    def test_run_method_custom_paths(self, mock_print, mock_save, mock_apply, mock_load):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement('custom_wbs.json', 'custom_changes.json', 'custom_output.json')
        manager.detailed_wbs = self.test_wbs
        manager.scope_status = {
            'added_tasks': [5],
            'removed_tasks': [3],
            'modified_tasks': [4]
        }
        
        manager.run()
        
        # Verify print was called with correct output path
        mock_print.assert_any_call(f"Scope management output saved to custom_output.json")

    # Test 19: Test apply_scope_changes method with unicode data
    def test_apply_scope_changes_unicode_data(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        unicode_wbs = {
            "id": 1,
            "name": "مشروع",  # "Project" in Arabic
            "subtasks": [
                {
                    "id": 2,
                    "name": "مهمة 1",  # "Task 1" in Arabic
                }
            ]
        }
        manager.detailed_wbs = unicode_wbs
        manager.scope_changes = [
            {
                "task_id": 2,
                "change_type": "modify",
                "details": {
                    "name": "مهمة معدلة",  # "Modified Task" in Arabic
                    "status": "قيد التنفيذ"  # "In Progress" in Arabic
                }
            }
        ]
        
        manager.apply_scope_changes()
        
        # Verify task was modified with unicode data
        self.assertIn(2, manager.scope_status['modified_tasks'])
        task = manager.find_task_by_id(2)
        self.assertEqual(task['name'], 'مهمة معدلة')
        self.assertEqual(task['status'], 'قيد التنفيذ')

    # Test 20: Test apply_scope_changes method with special characters in task names
    def test_apply_scope_changes_special_characters_in_task_names(self):
        from project_management.modules.main_modules.scope_management import ScopeManagement
        manager = ScopeManagement()
        special_char_wbs = {
            "id": 1,
            "name": "Task!@#$%^&*()",
            "subtasks": [
                {
                    "id": 2,
                    "name": "Subtask with\nnewlines and\ttabs",
                }
            ]
        }
        manager.detailed_wbs = special_char_wbs
        manager.scope_changes = [
            {
                "task_id": 2,
                "change_type": "modify",
                "details": {
                    "name": "Modified Task with $pecial characters!",
                }
            }
        ]
        
        manager.apply_scope_changes()
        
        # Verify task was modified with special characters
        self.assertIn(2, manager.scope_status['modified_tasks'])
        task = manager.find_task_by_id(2)
        self.assertEqual(task['name'], 'Modified Task with $pecial characters!')

if __name__ == "__main__":
    unittest.main()
