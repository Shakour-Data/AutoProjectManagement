import unittest
import json
import os
from project_management.modules.main_modules.estimation_management import (
    BaseManagement, EstimationManagement, estimate_task_duration, 
    estimate_task_cost, estimate_project_duration, estimate_project_cost
)
from unittest.mock import patch, mock_open

class TestBaseManagement(unittest.TestCase):
    def setUp(self):
        self.input_paths = {'test_input': 'test_input.json'}
        self.output_path = 'test_output.json'
        self.base_manager = BaseManagement(self.input_paths, self.output_path)

    def test_init(self):
        self.assertEqual(self.base_manager.input_paths, self.input_paths)
        self.assertEqual(self.base_manager.output_path, self.output_path)
        self.assertEqual(self.base_manager.inputs, {})
        self.assertEqual(self.base_manager.output, {})

    def test_load_json_file_exists(self):
        test_data = {"key": "value"}
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
                result = self.base_manager.load_json("test_file.json")
                self.assertEqual(result, test_data)

    def test_load_json_file_not_exists(self):
        with patch("os.path.exists", return_value=False):
            result = self.base_manager.load_json("nonexistent_file.json")
            self.assertIsNone(result)

    def test_save_json(self):
        test_data = {"key": "value"}
        with patch("builtins.open", mock_open()) as mock_file:
            self.base_manager.save_json(test_data, "test_file.json")
            mock_file.assert_called_once_with("test_file.json", 'w', encoding='utf-8')

    def test_load_inputs(self):
        with patch.object(self.base_manager, 'load_json', return_value={"data": "test"}) as mock_load:
            self.base_manager.load_inputs()
            mock_load.assert_called_once_with(self.input_paths['test_input'])
            self.assertEqual(self.base_manager.inputs['test_input'], {"data": "test"})

    def test_analyze_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.base_manager.analyze()

    def test_run(self):
        with patch.object(self.base_manager, 'load_inputs') as mock_load_inputs:
            with patch.object(self.base_manager, 'analyze') as mock_analyze:
                with patch.object(self.base_manager, 'save_json') as mock_save:
                    self.base_manager.run()
                    mock_load_inputs.assert_called_once()
                    mock_analyze.assert_called_once()
                    mock_save.assert_called_once_with(self.base_manager.output, self.output_path)

class TestEstimationManagement(unittest.TestCase):
    def setUp(self):
        self.estimation_manager = EstimationManagement()

    def test_init(self):
        self.assertEqual(self.estimation_manager.input_paths, {'detailed_wbs': 'project_inputs/PM_JSON/user_inputs/detailed_wbs.json'})
        self.assertEqual(self.estimation_manager.output_path, 'project_inputs/PM_JSON/system_outputs/estimation_management.json')

    def test_analyze(self):
        self.estimation_manager.analyze()
        self.assertEqual(self.estimation_manager.output['summary'], 'Estimation methods not yet implemented')
        self.assertEqual(self.estimation_manager.output['details'], {})

if __name__ == '__main__':
    unittest.main()
