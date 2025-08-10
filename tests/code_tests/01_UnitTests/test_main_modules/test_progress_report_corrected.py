import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, mock_open
from project_management.modules.main_modules.progress_report import ProgressReport, generate_report

class TestProgressReport(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures with temporary directories."""
        self.test_dir = tempfile.mkdtemp()
        self.progress_path = os.path.join(self.test_dir, 'commit_progress.json')
        self.task_db_path = os.path.join(self.test_dir, 'commit_task_database.json')
        self.output_path = os.path.join(self.test_dir, 'progress_report.md')
        
        # Sample data
        self.sample_progress = {
            "task1.py": 100,
            "task2.py": 75,
            "task3.py": 0,
            "task4.py": 100
        }
        
        self.sample_task_db = {
            "task1.py": {"title": "Task 1", "is_milestone": True},
            "task2.py": {"title": "Task 2", "is_milestone": False},
            "task3.py": {"title": "Task 3", "is_milestone": False},
            "task4.py": {"title": "Task 4", "is_milestone": True}
        }
        
        # Write sample data to files
        with open(self.progress_path, 'w') as f:
            json.dump(self.sample_progress, f)
        with open(self.task_db_path, 'w') as f:
            json.dump(self.sample_task_db, f)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_init_with_default_paths(self):
        """Test initialization with default paths."""
        report = ProgressReport()
        self.assertIsNotNone(report.progress_path)
        self.assertIsNotNone(report.task_db_path)
        self.assertIsNotNone(report.output_path)

    def test_init_with_custom_paths(self):
        """Test initialization with custom paths."""
        report = ProgressReport(
            progress_path=self.progress_path,
            task_db_path=self.task_db_path,
            output_path=self.output_path
        )
        self.assertEqual(report.progress_path, self.progress_path)
        self.assertEqual(report.task_db_path, self.task_db_path)
        self.assertEqual(report.output_path, self.output_path)

    def test_load_json_success(self):
        """Test successful JSON loading."""
        report = ProgressReport(
            progress_path=self.progress_path,
            task_db_path=self.task_db_path
        )
        data = report.load_json(self.progress_path)
        self.assertEqual(data, self.sample_progress)

    def test_load_json_file_not_found(self):
        """Test JSON loading with non-existent file."""
        report = ProgressReport()
        with self.assertRaises(FileNotFoundError):
            report.load_json('non_existent.json')

    def test_generate_progress_summary(self):
        """Test progress summary generation."""
        report = ProgressReport(
            progress_path=self.progress_path,
            task_db_path=self.task_db_path
        )
        summary = report.generate_progress_summary()
        
        self.assertEqual(summary['total_tasks'], 4)
        self.assertEqual(summary['completed_tasks'], 2)
        self.assertEqual(summary['in_progress_tasks'], 1)
        self.assertEqual(summary['pending_tasks'], 1)
        self.assertEqual(summary['milestones_achieved'], 2)

    def test_generate_progress_summary_empty_data(self):
        """Test progress summary with empty data."""
        empty_progress_path = os.path.join(self.test_dir, 'empty_progress.json')
        empty_task_db_path = os.path.join(self.test_dir, 'empty_task_db.json')
        
        with open(empty_progress_path, 'w') as f:
            json.dump({}, f)
        with open(empty_task_db_path, 'w') as f:
            json.dump({}, f)
        
        report = ProgressReport(
            progress_path=empty_progress_path,
            task_db_path=empty_task_db_path
        )
        summary = report.generate_progress_summary()
        
        self.assertEqual(summary['total_tasks'], 0)
        self.assertEqual(summary['completed_tasks'], 0)
        self.assertEqual(summary['in_progress_tasks'], 0)
        self.assertEqual(summary['pending_tasks'], 0)
        self.assertEqual(summary['milestones_achieved'], 0)

    def test_generate_markdown_report(self):
        """Test markdown report generation."""
        report = ProgressReport(
            progress_path=self.progress_path,
            task_db_path=self.task_db_path
        )
        summary = report.generate_progress_summary()
        markdown = report.generate_markdown_report(summary)
        
        self.assertIn("# Project Progress Report", markdown)
        self.assertIn("Total Tasks: 4", markdown)
        self.assertIn("Completed Tasks: 2", markdown)

    def test_save_report(self):
        """Test report saving functionality."""
        report = ProgressReport(output_path=self.output_path)
        test_content = "# Test Report\nThis is a test."
        
        report.save_report(test_content)
        
        self.assertTrue(os.path.exists(self.output_path))
        with open(self.output_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, test_content)

    def test_generate_method(self):
        """Test the complete generate method."""
        report = ProgressReport(
            progress_path=self.progress_path,
            task_db_path=self.task_db_path,
            output_path=self.output_path
        )
        
        report.generate()
        
        self.assertTrue(os.path.exists(self.output_path))

    def test_generate_report_function(self):
        """Test the standalone generate_report function."""
        with patch('project_management.modules.main_modules.progress_report.ProgressReport') as mock_class:
            mock_instance = mock_class.return_value
            generate_report()
            mock_instance.generate.assert_called_once()

if __name__ == "__main__":
    unittest.main()
