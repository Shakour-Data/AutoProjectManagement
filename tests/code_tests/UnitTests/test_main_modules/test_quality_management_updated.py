import unittest
import json
import os
import tempfile
import shutil
from unittest.mock import patch, mock_open
from project_management.modules.main_modules.quality_management import QualityManagement, BaseManagement

class TestQualityManagement(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.detailed_wbs_path = os.path.join(self.test_dir, 'detailed_wbs.json')
        self.quality_standards_path = os.path.join(self.test_dir, 'quality_standards.json')
        self.output_path = os.path.join(self.test_dir, 'quality_management.json')
        
        # Create test data
        self.detailed_wbs_data = {
            "tasks": [
                {"id": 1, "name": "Task 1", "status": "completed", "quality_score": 95},
                {"id": 2, "name": "Task 2", "status": "in_progress", "quality_score": 80},
                {"id": 3, "name": "Task 3", "status": "pending", "quality_score": None}
            ]
        }
        
        self.quality_standards_data = {
            "thresholds": {
                "min_quality_score": 85,
                "max_defects": 5,
                "min_coverage": 80
            }
        }
        
        # Write test data to files
        with open(self.detailed_wbs_path, 'w') as f:
            json.dump(self.detailed_wbs_data, f)
        with open(self.quality_standards_path, 'w') as f:
            json.dump(self.quality_standards_data, f)

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        shutil.rmtree(self.test_dir)

    def test_quality_management_initialization(self):
        """Test QualityManagement class initialization."""
        manager = QualityManagement(
            detailed_wbs_path=self.detailed_wbs_path,
            quality_standards_path=self.quality_standards_path,
            output_path=self.output_path
        )
        
        self.assertEqual(manager.input_paths['detailed_wbs'], self.detailed_wbs_path)
        self.assertEqual(manager.input_paths['quality_standards'], self.quality_standards_path)
        self.assertEqual(manager.output_path, self.output_path)

    def test_base_management_initialization(self):
        """Test BaseManagement class initialization."""
        input_paths = {
            'test_input': '/path/to/test.json'
        }
        output_path = '/path/to/output.json'
        
        base = BaseManagement(input_paths, output_path)
        self.assertEqual(base.input_paths, input_paths)
        self.assertEqual(base.output_path, output_path)
        self.assertEqual(base.inputs, {})
        self.assertEqual(base.output, {})

    def test_load_json_existing_file(self):
        """Test loading JSON from existing file."""
        manager = QualityManagement(
            detailed_wbs_path=self.detailed_wbs_path,
            quality_standards_path=self.quality_standards_path,
            output_path=self.output_path
        )
        
        result = manager.load_json(self.detailed_wbs_path)
        self.assertEqual(result, self.detailed_wbs_data)

    def test_load_json_nonexistent_file(self):
        """Test loading JSON from non-existent file."""
        manager = QualityManagement(
            detailed_wbs_path=self.detailed_wbs_path,
            quality_standards_path=self.quality_standards_path,
            output_path=self.output_path
        )
        
        result = manager.load_json('/nonexistent/path.json')
        self.assertIsNone(result)

    def test_save_json(self):
        """Test saving JSON data to file."""
        manager = QualityManagement(
            detailed_wbs_path=self.detailed_wbs_path,
            quality_standards_path=self.quality_standards_path,
            output_path=self.output_path
        )
        
        test_data = {"test": "data"}
        manager.save_json(test_data, self.output_path)
        
        self.assertTrue(os.path.exists(self.output_path))
        with open(self.output_path, 'r') as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, test_data)

    def test_load_inputs(self):
        """Test loading all input files."""
        manager = QualityManagement(
            detailed_wbs_path=self.detailed_wbs_path,
            quality_standards_path=self.quality_standards_path,
            output_path=self.output_path
        )
        
        manager.load_inputs()
        
        self.assertIn('detailed_wbs', manager.inputs)
        self.assertIn('quality_standards', manager.inputs)
        self.assertEqual(manager.inputs['detailed_wbs'], self.detailed_wbs_data)
        self.assertEqual(manager.inputs['quality_standards'], self.quality_standards_data)

    def test_analyze_placeholder_implementation(self):
        """Test the placeholder analyze method in QualityManagement."""
        manager = QualityManagement(
            detailed_wbs_path=self.detailed_wbs_path,
            quality_standards_path=self.quality_standards_path,
            output_path=self.output_path
        )
        
        manager.analyze()
        
        expected_output = {
            'summary': 'Quality evaluation not yet implemented',
            'details': {}
        }
        self.assertEqual(manager.output, expected_output)

    def test_base_management_analyze_not_implemented(self):
        """Test that BaseManagement analyze raises NotImplementedError."""
        base = BaseManagement({}, '')
        with self.assertRaises(NotImplementedError):
            base.analyze()

    @patch('builtins.print')
    def test_run_method(self, mock_print):
        """Test the complete run method."""
        manager = QualityManagement(
            detailed_wbs_path=self.detailed_wbs_path,
            quality_standards_path=self.quality_standards_path,
            output_path=self.output_path
        )
        
        manager.run()
        
        # Check that output file was created
        self.assertTrue(os.path.exists(self.output_path))
        
        # Check that print was called
        mock_print.assert_called_once()
        self.assertIn('QualityManagement output saved to', mock_print.call_args[0][0])

    def test_run_with_missing_files(self):
        """Test run method with missing input files."""
        manager = QualityManagement(
            detailed_wbs_path='/nonexistent/detailed_wbs.json',
            quality_standards_path='/nonexistent/quality_standards.json',
            output_path=self.output_path
        )
        
        # Should not raise exception, just use empty dicts for missing files
        manager.run()
        
        self.assertTrue(os.path.exists(self.output_path))
        with open(self.output_path, 'r') as f:
            output = json.load(f)
        self.assertEqual(output, {
            'summary': 'Quality evaluation not yet implemented',
            'details': {}
        })

    def test_empty_detailed_wbs(self):
        """Test with empty detailed WBS data."""
        empty_wbs_path = os.path.join(self.test_dir, 'empty_wbs.json')
        with open(empty_wbs_path, 'w') as f:
            json.dump({}, f)
        
        manager = QualityManagement(
            detailed_wbs_path=empty_wbs_path,
            quality_standards_path=self.quality_standards_path,
            output_path=self.output_path
        )
        
        manager.run()
        
        self.assertTrue(os.path.exists(self.output_path))

    def test_empty_quality_standards(self):
        """Test with empty quality standards data."""
        empty_standards_path = os.path.join(self.test_dir, 'empty_standards.json')
        with open(empty_standards_path, 'w') as f:
            json.dump({}, f)
        
        manager = QualityManagement(
            detailed_wbs_path=self.detailed_wbs_path,
            quality_standards_path=empty_standards_path,
            output_path=self.output_path
        )
        
        manager.run()
        
        self.assertTrue(os.path.exists(self.output_path))

    def test_malformed_json_handling(self):
        """Test handling of malformed JSON files."""
        malformed_path = os.path.join(self.test_dir, 'malformed.json')
        with open(malformed_path, 'w') as f:
            f.write('{"invalid": json content}')
        
        manager = QualityManagement(
            detailed_wbs_path=malformed_path,
            quality_standards_path=self.quality_standards_path,
            output_path=self.output_path
        )
        
        # Should handle malformed JSON gracefully
        manager.load_inputs()
        self.assertEqual(manager.inputs['detailed_wbs'], {})

    def test_unicode_content_handling(self):
        """Test handling of Unicode content in JSON files."""
        unicode_data = {
            "tasks": [
                {"id": 1, "name": "تست یونیکد", "status": "completed", "quality_score": 95}
            ]
        }
        
        unicode_path = os.path.join(self.test_dir, 'unicode.json')
        with open(unicode_path, 'w', encoding='utf-8') as f:
            json.dump(unicode_data, f, ensure_ascii=False)
        
        manager = QualityManagement(
            detailed_wbs_path=unicode_path,
            quality_standards_path=self.quality_standards_path,
            output_path=self.output_path
        )
        
        manager.load_inputs()
        self.assertEqual(manager.inputs['detailed_wbs'], unicode_data)

    def test_large_dataset_handling(self):
        """Test handling of large datasets."""
        large_data = {
            "tasks": [{"id": i, "name": f"Task {i}", "status": "completed", "quality_score": 95} 
                     for i in range(1000)]
        }
        
        large_path = os.path.join(self.test_dir, 'large.json')
        with open(large_path, 'w') as f:
            json.dump(large_data, f)
        
        manager = QualityManagement(
            detailed_wbs_path=large_path,
            quality_standards_path=self.quality_standards_path,
            output_path=self.output_path
        )
        
        manager.run()
        
        self.assertTrue(os.path.exists(self.output_path))

if __name__ == '__main__':
    unittest.main()
