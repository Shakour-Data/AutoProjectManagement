import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os

# Add the project root to the path so we can import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestResourceLeveling(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        self.test_tasks = [
            {
                "id": 1,
                "name": "Task 1",
                "optimistic_hours": 2,
                "normal_hours": 4,
                "pessimistic_hours": 6,
                "subtasks": [
                    {
                        "id": 2,
                        "name": "Subtask 1.1",
                        "optimistic_hours": 1,
                        "normal_hours": 2,
                        "pessimistic_hours": 3
                    }
                ]
            },
            {
                "id": 3,
                "name": "Task 2",
                "optimistic_hours": 3,
                "normal_hours": 5,
                "pessimistic_hours": 7
            }
        ]
        
        self.test_allocations = [
            {
                "task_id": 1,
                "role": "Developer"
            },
            {
                "task_id": 2,
                "role": "Developer"
            },
            {
                "task_id": 3,
                "role": "Tester"
            }
        ]
        
        self.test_flat_tasks = [
            {
                "id": 1,
                "name": "Task 1",
                "optimistic_hours": 2,
                "normal_hours": 4,
                "pessimistic_hours": 6,
                "parent_id": None
            },
            {
                "id": 2,
                "name": "Subtask 1.1",
                "optimistic_hours": 1,
                "normal_hours": 2,
                "pessimistic_hours": 3,
                "parent_id": 1
            },
            {
                "id": 3,
                "name": "Task 2",
                "optimistic_hours": 3,
                "normal_hours": 5,
                "pessimistic_hours": 7,
                "parent_id": None
            }
        ]

    # Test 1: Test initialization with default parameters
    def test_init_default_parameters(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        self.assertEqual(leveler.tasks_filepath, 'tasks.json')
        self.assertEqual(leveler.allocations_filepath, 'allocations.json')
        self.assertEqual(leveler.output_filepath, 'output.json')
        self.assertEqual(leveler.duration_type, 'normal')
        self.assertEqual(leveler.tasks, [])
        self.assertEqual(leveler.allocations, [])
        self.assertEqual(leveler.flat_tasks, [])
        self.assertEqual(leveler.task_map, {})
        self.assertEqual(leveler.task_schedules, {})

    # Test 2: Test initialization with custom duration type
    def test_init_custom_duration_type(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json', 'optimistic')
        self.assertEqual(leveler.duration_type, 'optimistic')

    # Test 3: Test load_json_file method
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_json_file(self, mock_open_file):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        result = leveler.load_json_file('test.json')
        self.assertEqual(result, {"key": "value"})
        mock_open_file.assert_called_once_with('test.json', 'r', encoding='utf-8')

    # Test 4: Test save_json_file method
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_json_file(self, mock_json_dump, mock_open_file):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        test_data = {"key": "value"}
        leveler.save_json_file(test_data, 'output.json')
        mock_open_file.assert_called_once_with('output.json', 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with(test_data, mock_open_file(), indent=2)

    # Test 5: Test flatten_tasks method
    def test_flatten_tasks(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        result = leveler.flatten_tasks(self.test_tasks)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['parent_id'], None)
        self.assertEqual(result[1]['id'], 2)
        self.assertEqual(result[1]['parent_id'], 1)
        self.assertEqual(result[2]['id'], 3)
        self.assertEqual(result[2]['parent_id'], None)

    # Test 6: Test flatten_tasks with empty list
    def test_flatten_tasks_empty_list(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        result = leveler.flatten_tasks([])
        self.assertEqual(result, [])

    # Test 7: Test resource_leveling method with normal duration
    def test_resource_leveling_normal_duration(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        leveler.flat_tasks = self.test_flat_tasks
        leveler.allocations = self.test_allocations
        result = leveler.resource_leveling()
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertIn(3, result)
        self.assertEqual(result[1]['resource_id'], 'Developer')
        self.assertEqual(result[2]['resource_id'], 'Developer')
        self.assertEqual(result[3]['resource_id'], 'Tester')

    # Test 8: Test resource_leveling method with optimistic duration
    def test_resource_leveling_optimistic_duration(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json', 'optimistic')
        leveler.flat_tasks = self.test_flat_tasks
        leveler.allocations = self.test_allocations
        result = leveler.resource_leveling()
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertIn(3, result)
        # Check that optimistic hours were used
        self.assertEqual(result[2]['end'] - result[2]['start'], 1)  # 1 hour for subtask 2

    # Test 9: Test resource_leveling method with pessimistic duration
    def test_resource_leveling_pessimistic_duration(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json', 'pessimistic')
        leveler.flat_tasks = self.test_flat_tasks
        leveler.allocations = self.test_allocations
        result = leveler.resource_leveling()
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertIn(3, result)
        # Check that pessimistic hours were used
        self.assertEqual(result[2]['end'] - result[2]['start'], 3)  # 3 hours for subtask 2

    # Test 10: Test resource_leveling with missing duration fields
    def test_resource_leveling_missing_duration_fields(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        # Tasks without duration fields
        flat_tasks_no_duration = [
            {
                "id": 1,
                "name": "Task 1",
                "parent_id": None
            }
        ]
        leveler.flat_tasks = flat_tasks_no_duration
        leveler.allocations = [{"task_id": 1, "role": "Developer"}]
        result = leveler.resource_leveling()
        # Should use default duration of 1 hour
        self.assertEqual(result[1]['end'] - result[1]['start'], 1)

    # Test 11: Test resource_leveling with missing task in allocations
    def test_resource_leveling_missing_task_in_allocations(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        leveler.flat_tasks = self.test_flat_tasks
        # Allocation for task that doesn't exist
        leveler.allocations = [{"task_id": 999, "role": "Developer"}]
        result = leveler.resource_leveling()
        # Should not crash and return empty schedules
        self.assertEqual(result, {})

    # Test 12: Test run method execution
    @patch("project_management.modules.main_modules.resource_leveling.ResourceLeveler.load_json_file")
    @patch("project_management.modules.main_modules.resource_leveling.ResourceLeveler.flatten_tasks")
    @patch("project_management.modules.main_modules.resource_leveling.ResourceLeveler.resource_leveling")
    @patch("project_management.modules.main_modules.resource_leveling.ResourceLeveler.save_json_file")
    @patch("builtins.print")
    def test_run_method(self, mock_print, mock_save, mock_leveling, mock_flatten, mock_load):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        
        # Setup mock returns
        mock_load.side_effect = lambda filepath: self.test_tasks if filepath == 'tasks.json' else self.test_allocations
        mock_flatten.return_value = self.test_flat_tasks
        mock_leveling.return_value = {"1": {"resource_id": "Developer", "start": 0, "end": 4}}
        
        leveler.run()
        
        # Verify methods were called
        self.assertEqual(mock_load.call_count, 2)
        mock_flatten.assert_called_once()
        mock_leveling.assert_called_once()
        mock_save.assert_called_once()
        mock_print.assert_called_once_with("Resource leveling completed. Output saved to output.json")

    # Test 13: Test run method with file not found error
    @patch("project_management.modules.main_modules.resource_leveling.ResourceLeveler.load_json_file", side_effect=FileNotFoundError("File not found"))
    @patch("builtins.print")
    def test_run_method_file_not_found(self, mock_print, mock_load):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        
        # Verify that the exception is raised
        with self.assertRaises(FileNotFoundError) as context:
            leveler.run()
        
        self.assertIn("File not found", str(context.exception))

    # Test 14: Test run method with permission error on save
    @patch("project_management.modules.main_modules.resource_leveling.ResourceLeveler.load_json_file")
    @patch("project_management.modules.main_modules.resource_leveling.ResourceLeveler.flatten_tasks")
    @patch("project_management.modules.main_modules.resource_leveling.ResourceLeveler.resource_leveling")
    @patch("project_management.modules.main_modules.resource_leveling.ResourceLeveler.save_json_file", side_effect=PermissionError("Permission denied"))
    @patch("builtins.print")
    def test_run_method_permission_error(self, mock_print, mock_save, mock_leveling, mock_flatten, mock_load):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        
        # Setup mock returns
        mock_load.side_effect = lambda filepath: self.test_tasks if filepath == 'tasks.json' else self.test_allocations
        mock_flatten.return_value = self.test_flat_tasks
        mock_leveling.return_value = {"1": {"resource_id": "Developer", "start": 0, "end": 4}}
        
        # Verify that the exception is raised
        with self.assertRaises(PermissionError) as context:
            leveler.run()
        
        self.assertIn("Permission denied", str(context.exception))

    # Test 15: Test resource_leveling with unicode data
    def test_resource_leveling_unicode_data(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        unicode_tasks = [
            {
                "id": 1,
                "name": "وظيفة 1",  # "Task 1" in Arabic
                "normal_hours": 4,
                "parent_id": None
            }
        ]
        unicode_allocations = [
            {
                "task_id": 1,
                "role": "مطور"  # "Developer" in Arabic
            }
        ]
        leveler.flat_tasks = unicode_tasks
        leveler.allocations = unicode_allocations
        result = leveler.resource_leveling()
        self.assertIn(1, result)
        self.assertEqual(result[1]['resource_id'], 'مطور')

    # Test 16: Test resource_leveling with special characters in task names
    def test_resource_leveling_special_characters(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        special_char_tasks = [
            {
                "id": 1,
                "name": "Task!@#$%^&*()",
                "normal_hours": 4,
                "parent_id": None
            }
        ]
        special_char_allocations = [
            {
                "task_id": 1,
                "role": "Special!@#Role"
            }
        ]
        leveler.flat_tasks = special_char_tasks
        leveler.allocations = special_char_allocations
        result = leveler.resource_leveling()
        self.assertIn(1, result)
        self.assertEqual(result[1]['resource_id'], 'Special!@#Role')

    # Test 17: Test resource_leveling with nested subtasks
    def test_resource_leveling_nested_subtasks(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        nested_tasks = [
            {
                "id": 1,
                "name": "Task 1",
                "normal_hours": 4,
                "subtasks": [
                    {
                        "id": 2,
                        "name": "Subtask 1.1",
                        "normal_hours": 2,
                        "subtasks": [
                            {
                                "id": 3,
                                "name": "Subtask 1.1.1",
                                "normal_hours": 1
                            }
                        ]
                    }
                ]
            }
        ]
        flat_nested_tasks = leveler.flatten_tasks(nested_tasks)
        nested_allocations = [
            {"task_id": 1, "role": "Developer"},
            {"task_id": 2, "role": "Developer"},
            {"task_id": 3, "role": "Developer"}
        ]
        leveler.flat_tasks = flat_nested_tasks
        leveler.allocations = nested_allocations
        result = leveler.resource_leveling()
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertIn(3, result)

    # Test 18: Test resource_leveling with zero duration tasks
    def test_resource_leveling_zero_duration_tasks(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        zero_duration_tasks = [
            {
                "id": 1,
                "name": "Task 1",
                "normal_hours": 0,
                "parent_id": None
            }
        ]
        zero_duration_allocations = [
            {
                "task_id": 1,
                "role": "Developer"
            }
        ]
        leveler.flat_tasks = zero_duration_tasks
        leveler.allocations = zero_duration_allocations
        result = leveler.resource_leveling()
        self.assertIn(1, result)
        # Should have start and end times that are the same (zero duration)
        self.assertEqual(result[1]['start'], result[1]['end'])

    # Test 19: Test resource_leveling with large number of tasks
    def test_resource_leveling_large_number_of_tasks(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        # Create large number of tasks
        large_tasks = []
        large_allocations = []
        for i in range(100):
            large_tasks.append({
                "id": i,
                "name": f"Task {i}",
                "normal_hours": 1,
                "parent_id": None
            })
            large_allocations.append({
                "task_id": i,
                "role": "Developer" if i % 2 == 0 else "Tester"
            })
        leveler.flat_tasks = large_tasks
        leveler.allocations = large_allocations
        result = leveler.resource_leveling()
        # Should process all tasks
        self.assertEqual(len(result), 100)

    # Test 20: Test resource_leveling with empty allocations
    def test_resource_leveling_empty_allocations(self):
        from project_management.modules.main_modules.resource_leveling import ResourceLeveler
        leveler = ResourceLeveler('tasks.json', 'allocations.json', 'output.json')
        leveler.flat_tasks = self.test_flat_tasks
        leveler.allocations = []
        result = leveler.resource_leveling()
        # Should return empty schedules
        self.assertEqual(result, {})

if __name__ == "__main__":
    unittest.main()
