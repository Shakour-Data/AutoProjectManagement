"""
Unit tests for the reporting module.
This test suite covers the actual Reporting class functionality.
"""

import unittest
import json
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from project_management.modules.main_modules.reporting import Reporting, BaseManagement

class TestBaseManagement(unittest.TestCase):
    """Test cases for BaseManagement class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.temp_dir, 'input.json')
        self.output_file = os.path.join(self.temp_dir, 'output.json')
        
        # Create test input data
        self.test_data = {
            "test_key": "test_value",
            "nested": {"inner": "data"}
        }
        
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
        
    def test_init(self):
        """Test BaseManagement initialization."""
        input_paths = {"test": self.input_file}
        base_mgmt = BaseManagement(input_paths, self.output_file)
        
        self.assertEqual(base_mgmt.input_paths, input_paths)
        self.assertEqual(base_mgmt.output_path, self.output_file)
        self.assertEqual(base_mgmt.inputs, {})
        self.assertEqual(base_mgmt.output, {})
        
    def test_load_json_existing_file(self):
        """Test loading JSON from existing file."""
        with open(self.input_file, 'w') as f:
            json.dump(self.test_data, f)
            
        base_mgmt = BaseManagement({}, self.output_file)
        result = base_mgmt.load_json(self.input_file)
        
        self.assertEqual(result, self.test_data)
        
    def test_load_json_nonexistent_file(self):
        """Test loading JSON from non-existent file."""
        base_mgmt = BaseManagement({}, self.output_file)
        result = base_mgmt.load_json("nonexistent.json")
        
        self.assertIsNone(result)
        
    def test_save_json(self):
        """Test saving JSON data."""
        base_mgmt = BaseManagement({}, self.output_file)
        test_data = {"key": "value"}
        
        base_mgmt.save_json(test_data, self.output_file)
        
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, 'r') as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, test_data)
        
    def test_load_inputs(self):
        """Test loading multiple input files."""
        # Create test input files
        input1_path = os.path.join(self.temp_dir, 'input1.json')
        input2_path = os.path.join(self.temp_dir, 'input2.json')
        
        with open(input1_path, 'w') as f:
            json.dump({"data1": "value1"}, f)
        with open(input2_path, 'w') as f:
            json.dump({"data2": "value2"}, f)
            
        input_paths = {
            "input1": input1_path,
            "input2": input2_path
        }
        
        base_mgmt = BaseManagement(input_paths, self.output_file)
        base_mgmt.load_inputs()
        
        self.assertEqual(base_mgmt.inputs["input1"], {"data1": "value1"})
        self.assertEqual(base_mgmt.inputs["input2"], {"data2": "value2"})
        
    def test_analyze_not_implemented(self):
        """Test that analyze method raises NotImplementedError."""
        base_mgmt = BaseManagement({}, self.output_file)
        
        with self.assertRaises(NotImplementedError):
            base_mgmt.analyze()


class TestReporting(unittest.TestCase):
    """Test cases for Reporting class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test input files
        self.test_files = {
            'detailed_wbs.json': {
                "project_name": "Test Project",
                "tasks": [
                    {"id": 1, "name": "Task 1", "duration": 5},
                    {"id": 2, "name": "Task 2", "duration": 3}
                ]
            },
            'resource_allocation_summary.json': {
                "resources": [
                    {"name": "Developer", "allocated_hours": 40},
                    {"name": "Designer", "allocated_hours": 20}
                ]
            },
            'time_management.json': {
                "total_hours": 100,
                "completed_hours": 50
            },
            'risk_management.json': {
                "risks": [
                    {"id": 1, "probability": 0.3, "impact": "high"},
                    {"id": 2, "probability": 0.1, "impact": "medium"}
                ]
            },
            'quality_management.json': {
                "quality_score": 85,
                "issues": []
            }
        }
        
        # Create test files
        for filename, content in self.test_files.items():
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(content, f)
                
        self.output_file = os.path.join(self.temp_dir, 'project_reports.json')
        
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
        
    def test_init_default_paths(self):
        """Test Reporting initialization with default paths."""
        reporting = Reporting()
        
        expected_input_paths = {
            'detailed_wbs': 'project_inputs/PM_JSON/user_inputs/detailed_wbs.json',
            'resource_allocation_summary': 'project_inputs/PM_JSON/system_outputs/resource_allocation_summary.json',
            'time_management': 'project_inputs/PM_JSON/system_outputs/time_management.json',
            'risk_management': 'project_inputs/PM_JSON/system_outputs/risk_management.json',
            'quality_management': 'project_inputs/PM_JSON/system_outputs/quality_management.json'
        }
        
        self.assertEqual(reporting.input_paths, expected_input_paths)
        self.assertEqual(reporting.output_path, 'project_inputs/PM_JSON/system_outputs/project_reports.json')
        
    def test_init_custom_paths(self):
        """Test Reporting initialization with custom paths."""
        custom_paths = {
            'detailed_wbs': os.path.join(self.temp_dir, 'detailed_wbs.json'),
            'resource_allocation_summary': os.path.join(self.temp_dir, 'resource_allocation_summary.json'),
            'time_management': os.path.join(self.temp_dir, 'time_management.json'),
            'risk_management': os.path.join(self.temp_dir, 'risk_management.json'),
            'quality_management': os.path.join(self.temp_dir, 'quality_management.json'),
            'output': self.output_file
        }
        
        reporting = Reporting(
            detailed_wbs_path=custom_paths['detailed_wbs'],
            resource_allocation_summary_path=custom_paths['resource_allocation_summary'],
            time_management_path=custom_paths['time_management'],
            risk_management_path=custom_paths['risk_management'],
            quality_management_path=custom_paths['quality_management'],
            output_path=custom_paths['output']
        )
        
        self.assertEqual(reporting.input_paths['detailed_wbs'], custom_paths['detailed_wbs'])
        self.assertEqual(reporting.output_path, custom_paths['output'])
        
    def test_analyze_basic(self):
        """Test analyze method with basic data."""
        reporting = Reporting(
            detailed_wbs_path=os.path.join(self.temp_dir, 'detailed_wbs.json'),
            resource_allocation_summary_path=os.path.join(self.temp_dir, 'resource_allocation_summary.json'),
            time_management_path=os.path.join(self.temp_dir, 'time_management.json'),
            risk_management_path=os.path.join(self.temp_dir, 'risk_management.json'),
            quality_management_path=os.path.join(self.temp_dir, 'quality_management.json'),
            output_path=self.output_file
        )
        
        reporting.analyze()
        
        self.assertEqual(reporting.output['summary'], 'Project reports generation not yet implemented')
        self.assertIsInstance(reporting.output['details'], dict)
        
    def test_analyze_empty_inputs(self):
        """Test analyze method with empty input files."""
        # Create empty files
        empty_files = ['empty_wbs.json', 'empty_resources.json', 'empty_time.json', 'empty_risk.json', 'empty_quality.json']
        for filename in empty_files:
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'w') as f:
                json.dump({}, f)
                
        reporting = Reporting(
            detailed_wbs_path=os.path.join(self.temp_dir, 'empty_wbs.json'),
            resource_allocation_summary_path=os.path.join(self.temp_dir, 'empty_resources.json'),
            time_management_path=os.path.join(self.temp_dir, 'empty_time.json'),
            risk_management_path=os.path.join(self.temp_dir, 'empty_risk.json'),
            quality_management_path=os.path.join(self.temp_dir, 'empty_quality.json'),
            output_path=self.output_file
        )
        
        reporting.analyze()
        
        self.assertEqual(reporting.output['summary'], 'Project reports generation not yet implemented')
        
    def test_analyze_missing_files(self):
        """Test analyze method with missing input files."""
        reporting = Reporting(
            detailed_wbs_path=os.path.join(self.temp_dir, 'nonexistent.json'),
            resource_allocation_summary_path=os.path.join(self.temp_dir, 'nonexistent.json'),
            time_management_path=os.path.join(self.temp_dir, 'nonexistent.json'),
            risk_management_path=os.path.join(self.temp_dir, 'nonexistent.json'),
            quality_management_path=os.path.join(self.temp_dir, 'nonexistent.json'),
            output_path=self.output_file
        )
        
        reporting.load_inputs()
        
        # Should load empty dicts for missing files
        for key in reporting.inputs:
            self.assertEqual(reporting.inputs[key], {})
            
    def test_run_method(self):
        """Test the complete run method."""
        reporting = Reporting(
            detailed_wbs_path=os.path.join(self.temp_dir, 'detailed_wbs.json'),
            resource_allocation_summary_path=os.path.join(self.temp_dir, 'resource_allocation_summary.json'),
            time_management_path=os.path.join(self.temp_dir, 'time_management.json'),
            risk_management_path=os.path.join(self.temp_dir, 'risk_management.json'),
            quality_management_path=os.path.join(self.temp_dir, 'quality_management.json'),
            outputInformation Gathered:
- The current `test_reporting.py` tests a non-existent `generate_report` function, but the actual `reporting.py` module contains a `Reporting` class with methods like `load_inputs`, `analyze`, and `run`.
- The `Reporting` class inherits from `BaseManagement` and mainly loads JSON inputs, runs an analysis (currently a placeholder), and saves output.
- The unit testing documentation emphasizes mocking dependencies, isolating units, and covering normal, edge, and error cases.
- The test plan marks `test_reporting.py` as incomplete and requires implementation or correction.

Plan:
- Update `test_reporting.py` to test the `Reporting` class instead of a non-existent function.
- Write tests for:
  - Initialization of the `Reporting` class with default and custom paths.
  - The `load_inputs` method to ensure it loads JSON data correctly (mocking file I/O).
  - The `analyze` method to check it raises `NotImplementedError` in `BaseManagement` and runs correctly in `Reporting`.
  - The `run` method to verify the full workflow (load, analyze, save) with mocks.
  - Error handling for file loading and saving.
- Use `unittest.mock` to mock file system interactions and JSON operations.
- Remove or archive the old tests for `generate_report` function.

Dependent Files to be edited:
- `Tests/TestingCode/UnitTests/test_main_modules/test_reporting.py`

Followup steps:
- Implement the updated test suite in `test_reporting.py`.
- Run the tests to verify correctness.
- Update the detailed unit test plan checklist to mark `test_reporting.py` as complete.

<ask_followup_question>
<question>May I proceed with updating the `test_reporting.py` file to properly test the `Reporting` class as described in the plan?</question>
</ask_followup_question>
