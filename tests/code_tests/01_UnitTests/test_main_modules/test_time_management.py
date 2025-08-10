import unittest
from unittest.mock import patch, mock_open
import json
import os
from datetime import datetime

# Add the project root to the path so we can import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestTimeManagement(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        self.test_wbs = {
            "id": 1,
            "name": "Project",
            "resource_allocations": [
                {
                    "start_date": "2023-01-01",
                    "end_date": "2023-01-10"
                },
                {
                    "start_date": "2023-01-05",
                    "end_date": "2023-01-15"
                }
            ],
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "resource_allocations": [
                        {
                            "start_date": "2023-01-01",
                            "end_date": "2023-01-05"
                        }
                    ]
                },
                {
                    "id": 3,
                    "name": "Task 2",
                    "resource_allocations": [
                        {
                            "start_date": "2023-01-06",
                            "end_date": "2023-01-10"
                        }
                    ]
                }
            ]
        }
        
        self.test_resource_allocations = {
            "task_1": {
                "resource": "Developer",
                "start_date": "2023-01-01",
                "end_date": "2023-01-10"
            }
        }

    # Test 1: Test initialization with default paths
    def test_init_default_paths(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        self.assertEqual(manager.detailed_wbs_path, 'JSonDataBase/Inputs/UserInputs/detailed_wbs.json')
        self.assertEqual(manager.resource_allocation_path, 'JSonDataBase/OutPuts/resource_allocation_enriched.json')
        self.assertEqual(manager.output_path, 'JSonDataBase/OutPuts/time_management.json')
        self.assertEqual(manager.detailed_wbs, {})
        self.assertEqual(manager.resource_allocations, [])
        self.assertEqual(manager.task_schedules, {})

    # Test 2: Test initialization with custom paths
    def test_init_custom_paths(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement('custom_wbs.json', 'custom_allocations.json', 'custom_output.json')
        self.assertEqual(manager.detailed_wbs_path, 'custom_wbs.json')
        self.assertEqual(manager.resource_allocation_path, 'custom_allocations.json')
        self.assertEqual(manager.output_path, 'custom_output.json')

    # Test 3: Test load_json method with existing file
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    @patch("os.path.exists", return_value=True)
    def test_load_json_existing_file(self, mock_exists, mock_open_file):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        result = manager.load_json('test.json')
        self.assertEqual(result, {"key": "value"})
        mock_open_file.assert_called_once_with('test.json', 'r', encoding='utf-8')

    # Test 4: Test load_json method with non-existing file
    @patch("os.path.exists", return_value=False)
    def test_load_json_non_existing_file(self, mock_exists):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        result = manager.load_json('nonexistent.json')
        self.assertIsNone(result)

    # Test 5: Test save_json method
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_json(self, mock_json_dump, mock_open_file):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        test_data = {"key": "value"}
        manager.save_json(test_data, 'output.json')
        mock_open_file.assert_called_once_with('output.json', 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with(test_data, mock_open_file(), indent=2, ensure_ascii=False)

    # Test 6: Test load_inputs method
    @patch("project_management.modules.main_modules.time_management.TimeManagement.load_json")
    def test_load_inputs(self, mock_load_json):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        
        # Setup mock returns
        mock_load_json.side_effect = [
            self.test_wbs,  # detailed_wbs
            self.test_resource_allocations  # resource_allocations
        ]
        
        manager.load_inputs()
        
        # Verify load_json was called with correct paths
        calls = mock_load_json.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0][0], 'JSonDataBase/Inputs/UserInputs/detailed_wbs.json')
        self.assertEqual(calls[1][0][0], 'JSonDataBase/OutPuts/resource_allocation_enriched.json')
        
        # Verify data was loaded
        self.assertEqual(manager.detailed_wbs, self.test_wbs)
        self.assertEqual(manager.resource_allocations, self.test_resource_allocations)

    # Test 7: Test calculate_task_duration method with valid allocations
    def test_calculate_task_duration_valid_allocations(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        task = {
            "resource_allocations": [
                {
                    "start_date": "2023-01-01",
                    "end_date": "2023-01-10"
                },
                {
                    "start_date": "2023-01-05",
                    "end_date": "2023-01-15"
                }
            ]
        }
        duration = manager.calculate_task_duration(task)
        # Duration should be from 2023-01-01 to 2023-01-15 = 15 days
        self.assertEqual(duration, 15)

    # Test 8: Test calculate_task_duration method with no allocations
    def test_calculate_task_duration_no_allocations(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        task = {}
        duration = manager.calculate_task_duration(task)
        self.assertEqual(duration, 0)

    # Test 9: Test calculate_task_duration method with empty allocations
    def test_calculate_task_duration_empty_allocations(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        task = {
            "resource_allocations": []
        }
        duration = manager.calculate_task_duration(task)
        self.assertEqual(duration, 0)

    # Test 10: Test calculate_task_duration method with invalid date format
    def test_calculate_task_duration_invalid_date_format(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        task = {
            "resource_allocations": [
                {
                    "start_date": "invalid-date",
                    "end_date": "2023-01-10"
                }
            ]
        }
        duration = manager.calculate_task_duration(task)
        self.assertEqual(duration, 0)

    # Test 11: Test calculate_task_duration method with unicode dates
    def test_calculate_task_duration_unicode_dates(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        task = {
            "resource_allocations": [
                {
                    "start_date": "2023-01-01",
                    "end_date": "2023-01-10"
                }
            ]
        }
        duration = manager.calculate_task_duration(task)
        self.assertEqual(duration, 10)

    # Test 12: Test calculate_task_duration method with special characters in dates
    def test_calculate_task_duration_special_characters_in_dates(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        task = {
            "resource_allocations": [
                {
                    "start_date": "2023-01-01",
                    "end_date": "2023-01-10"
                }
            ]
        }
        duration = manager.calculate_task_duration(task)
        self.assertEqual(duration, 10)

    # Test 13: Test schedule_tasks method with valid data
    def test_schedule_tasks_valid_data(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        manager.detailed_wbs = self.test_wbs
        manager.schedule_tasks()
        
        # Verify that task schedules were created
        self.assertIn(1, manager.task_schedules)
        self.assertIn(2, manager.task_schedules)
        self.assertIn(3, manager.task_schedules)
        
        # Verify task 1 schedule
        self.assertEqual(manager.task_schedules[1]['task_name'], 'Project')
        self.assertEqual(manager.task_schedules[1]['duration_days'], 15)
        self.assertEqual(manager.task_schedules[1]['start_date'], '2023-01-01')
        self.assertEqual(manager.task_schedules[1]['end_date'], '2023-01-15')
        
        # Verify task 2 schedule
        self.assertEqual(manager.task_schedules[2]['task_name'], 'Task 1')
        self.assertEqual(manager.task_schedules[2]['duration_days'], 5)
        self.assertEqual(manager.task_schedules[2]['start_date'], '2023-01-01')
        self.assertEqual(manager.task_schedules[2]['end_date'], '2023-01-05')
        
        # Verify task 3 schedule
        self.assertEqual(manager.task_schedules[3]['task_name'], 'Task 2')
        self.assertEqual(manager.task_schedules[3]['duration_days'], 5)
        self.assertEqual(manager.task_schedules[3]['start_date'], '2023-01-06')
        self.assertEqual(manager.task_schedules[3]['end_date'], '2023-01-10')

    # Test 14: Test schedule_tasks method with empty WBS
    def test_schedule_tasks_empty_wbs(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        manager.detailed_wbs = {}
        manager.schedule_tasks()
        self.assertEqual(manager.task_schedules, {})

    # Test 15: Test schedule_tasks method with None WBS
    def test_schedule_tasks_none_wbs(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        manager.detailed_wbs = None
        manager.schedule_tasks()
        self.assertEqual(manager.task_schedules, {})

    # Test 16: Test schedule_tasks method with task without allocations
    def test_schedule_tasks_task_without_allocations(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        test_wbs = {
            "id": 1,
            "name": "Project",
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1"
                }
            ]
        }
        manager.detailed_wbs = test_wbs
        manager.schedule_tasks()
        
        # Verify that task schedules were created
        self.assertIn(1, manager.task_schedules)
        self.assertIn(2, manager.task_schedules)
        
        # Verify task 1 schedule (no allocations)
        self.assertEqual(manager.task_schedules[1]['task_name'], 'Project')
        self.assertEqual(manager.task_schedules[1]['duration_days'], 0)
        self.assertIsNone(manager.task_schedules[1]['start_date'])
        self.assertIsNone(manager.task_schedules[1]['end_date'])
        
        # Verify task 2 schedule (no allocations)
        self.assertEqual(manager.task_schedules[2]['task_name'], 'Task 1')
        self.assertEqual(manager.task_schedules[2]['duration_days'], 0)
        self.assertIsNone(manager.task_schedules[2]['start_date'])
        self.assertIsNone(manager.task_schedules[2]['end_date'])

    # Test 17: Test schedule_tasks method with invalid date format in allocations
    def test_schedule_tasks_invalid_date_format_in_allocations(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        test_wbs = {
            "id": 1,
            "name": "Project",
            "resource_allocations": [
                {
                    "start_date": "invalid-date",
                    "end_date": "2023-01-10"
                }
            ]
        }
        manager.detailed_wbs = test_wbs
        manager.schedule_tasks()
        
        # Verify that task schedule was created but with None dates
        self.assertIn(1, manager.task_schedules)
        self.assertEqual(manager.task_schedules[1]['task_name'], 'Project')
        self.assertEqual(manager.task_schedules[1]['duration_days'], 0)
        self.assertIsNone(manager.task_schedules[1]['start_date'])
        self.assertIsNone(manager.task_schedules[1]['end_date'])

    # Test 18: Test run method execution
    @patch("project_management.modules.main_modules.time_management.TimeManagement.load_inputs")
    @patch("project_management.modules.main_modules.time_management.TimeManagement.schedule_tasks")
    @patch("project_management.modules.main_modules.time_management.TimeManagement.save_json")
    @patch("builtins.print")
    def test_run_method(self, mock_print, mock_save, mock_schedule, mock_load):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        manager.task_schedules = {"1": {"task_name": "Test Task"}}
        
        manager.run()
        
        # Verify methods were called
        mock_load.assert_called_once()
        mock_schedule.assert_called_once()
        mock_save.assert_called_once_with(manager.task_schedules, manager.output_path)
        mock_print.assert_called_once_with(f"Time management schedule saved to {manager.output_path}")

    # Test 19: Test run method with custom paths
    @patch("project_management.modules.main_modules.time_management.TimeManagement.load_inputs")
    @patch("project_management.modules.main_modules.time_management.TimeManagement.schedule_tasks")
    @patch("project_management.modules.main_modules.time_management.TimeManagement.save_json")
    @patch("builtins.print")
    def test_run_method_custom_paths(self, mock_print, mock_save, mock_schedule, mock_load):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement('custom_wbs.json', 'custom_allocations.json', 'custom_output.json')
        manager.task_schedules = {"1": {"task_name": "Test Task"}}
        
        manager.run()
        
        # Verify print was called with correct output path
        mock_print.assert_called_once_with(f"Time management schedule saved to custom_output.json")

    # Test 20: Test schedule_tasks method with unicode task names
    def test_schedule_tasks_unicode_task_names(self):
        from project_management.modules.main_modules.time_management import TimeManagement
        manager = TimeManagement()
        unicode_wbs = {
            "id": 1,
            "name": "مشروع",  # "Project" in Arabic
            "resource_allocations": [
                {
                    "start_date": "2023-01-01",
                    "end_date": "2023-01-10"
                }
            ]
        }
        manager.detailed_wbs = unicode_wbs
        manager.schedule_tasks()
        
        # Verify that task schedule was created with unicode name
        self.assertIn(1, manager.task_schedules)
        self.assertEqual(manager.task_schedules[1]['task_name'], 'مشروع')

if __name__ == "__main__":
    unittest.main()
