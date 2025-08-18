import unittest
from unittest.mock import patch, mock_open
import os
import json

# Add the project root to the path so we can import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestWBSAggregator(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        self.test_wbs_part1 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "level": 1,
                    "subtasks": [
                        {
                            "id": 3,
                            "name": "Subtask 1.1",
                            "level": 2
                        }
                    ]
                }
            ]
        }
        
        self.test_wbs_part2 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 4,
                    "name": "Task 2",
                    "level": 1,
                    "subtasks": [
                        {
                            "id": 5,
                            "name": "Subtask 2.1",
                            "level": 2
                        }
                    ]
                }
            ]
        }

    # Test 1: Test initialization with default paths
    def test_init_default_paths(self):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        self.assertEqual(aggregator.parts_dir, 'SystemInputs/user_inputs/wbs_parts')
        self.assertEqual(aggregator.output_file, 'SystemInputs/user_inputs/detailed_wbs.json')

    # Test 2: Test initialization with custom paths
    def test_init_custom_paths(self):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator('custom_parts_dir', 'custom_output.json')
        self.assertEqual(aggregator.parts_dir, 'custom_parts_dir')
        self.assertEqual(aggregator.output_file, 'custom_output.json')

    # Test 3: Test load_part method
    @patch("builtins.open", new_callable=mock_open, read_data='{"id": 1, "name": "Test"}')
    def test_load_part(self, mock_open_file):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        result = aggregator.load_part('test.json')
        self.assertEqual(result, {"id": 1, "name": "Test"})
        mock_open_file.assert_called_once_with(os.path.join(aggregator.parts_dir, 'test.json'), 'r', encoding='utf-8')

    # Test 4: Test aggregate method with valid data
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_valid_data(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json', 'part2.json']
        mock_load_part.side_effect = [self.test_wbs_part1, self.test_wbs_part2]
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        self.assertEqual(mock_load_part.call_count, 2)
        mock_open_file.assert_called_once_with(aggregator.output_file, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once()
        mock_print.assert_called_once_with(f"Aggregated WBS written to {aggregator.output_file}")

    # Test 5: Test aggregate method with no WBS parts
    @patch("os.listdir")
    @patch("builtins.print")
    def test_aggregate_no_wbs_parts(self, mock_print, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup mock returns
        mock_listdir.return_value = []
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        mock_print.assert_called_once_with("No WBS parts found in directory.")

    # Test 6: Test aggregate method with empty WBS parts directory
    @patch("os.listdir")
    @patch("builtins.print")
    def test_aggregate_empty_wbs_parts_directory(self, mock_print, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup mock returns
        mock_listdir.return_value = []
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        mock_print.assert_called_once_with("No WBS parts found in directory.")

    # Test 7: Test aggregate method with exception in load_part
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part", side_effect=Exception("Failed to load part"))
    @patch("builtins.print")
    def test_aggregate_exception_in_load_part(self, mock_print, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json']
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            aggregator.aggregate()
        
        self.assertIn("Failed to load part", str(context.exception))

    # Test 8: Test aggregate method with exception in json.dump
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump", side_effect=Exception("Failed to dump JSON"))
    @patch("builtins.print")
    def test_aggregate_exception_in_json_dump(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json']
        mock_load_part.return_value = self.test_wbs_part1
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            aggregator.aggregate()
        
        self.assertIn("Failed to dump JSON", str(context.exception))

    # Test 9: Test aggregate method with unicode file names
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_unicode_file_names(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup mock returns with unicode file names
        mock_listdir.return_value = ['جزء1.json', 'جزء2.json']  # "part1.json" and "part2.json" in Arabic
        mock_load_part.side_effect = [self.test_wbs_part1, self.test_wbs_part2]
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)

    # Test 10: Test aggregate method with special characters in file names
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_special_characters_in_file_names(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup mock returns with special characters in file names
        mock_listdir.return_value = ['part!@#.json', 'part$%^&.json']
        mock_load_part.side_effect = [self.test_wbs_part1, self.test_wbs_part2]
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)

    # Test 11: Test aggregate method with large number of WBS parts
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_large_number_of_wbs_parts(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup mock returns with 100 WBS parts
        file_names = [f'part{i}.json' for i in range(100)]
        mock_listdir.return_value = file_names
        
        # Create 100 test WBS parts
        test_parts = []
        for i in range(100):
            part = {
                "id": 1,
                "name": "Project",
                "level": 0,
                "subtasks": [
                    {
                        "id": i + 2,
                        "name": f"Task {i + 1}",
                        "level": 1
                    }
                ]
            }
            test_parts.append(part)
        
        mock_load_part.side_effect = test_parts
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        self.assertEqual(mock_load_part.call_count, 100)

    # Test 12: Test aggregate method with nested subtasks
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_nested_subtasks(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup WBS part with deeply nested subtasks
        nested_wbs_part = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "level": 1,
                    "subtasks": [
                        {
                            "id": 3,
                            "name": "Subtask 1.1",
                            "level": 2,
                            "subtasks": [
                                {
                                    "id": 4,
                                    "name": "Subtask 1.1.1",
                                    "level": 3,
                                    "subtasks": [
                                        {
                                            "id": 5,
                                            "name": "Subtask 1.1.1.1",
                                            "level": 4
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json']
        mock_load_part.return_value = nested_wbs_part
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        mock_load_part.assert_called_once_with('part1.json')
        mock_open_file.assert_called_once_with(aggregator.output_file, 'w', encoding='utf-8')

    # Test 13: Test aggregate method with empty subtasks
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_empty_subtasks(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup WBS part with empty subtasks
        empty_subtasks_part = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": []
        }
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json']
        mock_load_part.return_value = empty_subtasks_part
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        mock_load_part.assert_called_once_with('part1.json')
        mock_open_file.assert_called_once_with(aggregator.output_file, 'w', encoding='utf-8')

    # Test 14: Test aggregate method with None subtasks
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_none_subtasks(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup WBS part with None subtasks
        none_subtasks_part = {
            "id": 1,
            "name": "Project",
            "level": 0
            # No subtasks key
        }
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json']
        mock_load_part.return_value = none_subtasks_part
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        mock_load_part.assert_called_once_with('part1.json')
        mock_open_file.assert_called_once_with(aggregator.output_file, 'w', encoding='utf-8')

    # Test 15: Test aggregate method with unicode task names
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_unicode_task_names(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup WBS part with unicode task names
        unicode_wbs_part = {
            "id": 1,
            "name": "مشروع",  # "Project" in Arabic
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "مهمة 1",  # "Task 1" in Arabic
                    "level": 1
                }
            ]
        }
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json']
        mock_load_part.return_value = unicode_wbs_part
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        mock_load_part.assert_called_once_with('part1.json')
        mock_open_file.assert_called_once_with(aggregator.output_file, 'w', encoding='utf-8')

    # Test 16: Test aggregate method with special characters in task names
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_special_characters_in_task_names(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup WBS part with special characters in task names
        special_chars_wbs_part = {
            "id": 1,
            "name": "Task!@#$%^&*()",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Subtask\nwith\nnewlines",
                    "level": 1
                }
            ]
        }
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json']
        mock_load_part.return_value = special_chars_wbs_part
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        mock_load_part.assert_called_once_with('part1.json')
        mock_open_file.assert_called_once_with(aggregator.output_file, 'w', encoding='utf-8')

    # Test 17: Test aggregate method with mixed WBS parts
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_mixed_wbs_parts(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup different WBS parts
        wbs_part1 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "level": 1
                }
            ]
        }
        
        wbs_part2 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 3,
                    "name": "Task 2",
                    "level": 1
                }
            ]
        }
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json', 'part2.json']
        mock_load_part.side_effect = [wbs_part1, wbs_part2]
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        self.assertEqual(mock_load_part.call_count, 2)
        mock_open_file.assert_called_once_with(aggregator.output_file, 'w', encoding='utf-8')

    # Test 18: Test aggregate method with duplicate task IDs
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_duplicate_task_ids(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup WBS parts with duplicate task IDs
        wbs_part1 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "level": 1
                }
            ]
        }
        
        wbs_part2 = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,  # Same ID as part1
                    "name": "Task 1 Duplicate",
                    "level": 1
                }
            ]
        }
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json', 'part2.json']
        mock_load_part.side_effect = [wbs_part1, wbs_part2]
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        self.assertEqual(mock_load_part.call_count, 2)
        mock_open_file.assert_called_once_with(aggregator.output_file, 'w', encoding='utf-8')

    # Test 19: Test aggregate method with zero task IDs
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_zero_task_ids(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup WBS part with zero task IDs
        zero_ids_wbs_part = {
            "id": 0,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 0,
                    "name": "Task 0",
                    "level": 1
                }
            ]
        }
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json']
        mock_load_part.return_value = zero_ids_wbs_part
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        mock_load_part.assert_called_once_with('part1.json')
        mock_open_file.assert_called_once_with(aggregator.output_file, 'w', encoding='utf-8')

    # Test 20: Test aggregate method with negative task IDs
    @patch("os.listdir")
    @patch("project_management.modules.main_modules.wbs_aggregator.WBSAggregator.load_part")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_aggregate_negative_task_ids(self, mock_print, mock_json_dump, mock_open_file, mock_load_part, mock_listdir):
        from project_management.modules.main_modules.wbs_aggregator import WBSAggregator
        aggregator = WBSAggregator()
        
        # Setup WBS part with negative task IDs
        negative_ids_wbs_part = {
            "id": -1,
            "name": "Project",
            "level": 0,
            "subtasks": [
                {
                    "id": -2,
                    "name": "Task -2",
                    "level": 1
                }
            ]
        }
        
        # Setup mock returns
        mock_listdir.return_value = ['part1.json']
        mock_load_part.return_value = negative_ids_wbs_part
        
        aggregator.aggregate()
        
        # Verify methods were called
        mock_listdir.assert_called_once_with(aggregator.parts_dir)
        mock_load_part.assert_called_once_with('part1.json')
        mock_open_file.assert_called_once_with(aggregator.output_file, 'w', encoding='utf-8')

if __name__ == "__main__":
    unittest.main()
