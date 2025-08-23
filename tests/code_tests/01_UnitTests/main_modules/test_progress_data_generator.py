#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: test_progress_data_generator
File: test_progress_data_generator.py
Path: tests/code_tests/01_UnitTests/main_modules/test_progress_data_generator.py

Description:
    Test Progress Data Generator module

Author: AutoProjectManagement Team
Contact: team@autoprojectmanagement.com
Repository: https://github.com/autoprojectmanagement/autoprojectmanagement

Version Information:
    Current Version: 1.0.0
    Last Updated: 2025-08-14
    Python Version: 3.8+
    
Development Status:
    Status: Production/Stable
    Created: 2024-01-01
    Last Modified: 2025-08-14
    Modified By: AutoProjectManagement Team

Dependencies:
    - Python 3.8+
    - See requirements.txt for full dependency list

License: MIT License
Copyright: (c) 2024 AutoProjectManagement Team

Usage:
    This module is part of the AutoProjectManagement package.
    Import and use as needed within the package ecosystem.

Example:
    >>> from tests.code_tests.01_UnitTests.main_modules.test_progress_data_generator import {main_class}
    >>> instance = {main_class}()
    >>> instance.run()

Notes:
    - This file follows the AutoProjectManagement coding standards
    - All changes should be documented in the changelog below
    - Ensure compatibility with Python 3.8+

Changelog:
    1.0.0 (2024-01-01): Initial release

================================================================================
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from autoprojectmanagement.main_modules.data_collection_processing.progress_data_generator import (
    ProgressDataGenerator,
    generate_progress_data
)

class TestProgressDataGenerator(unittest.TestCase):
    """Unit tests for ProgressDataGenerator module."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.progress_file = os.path.join(self.temp_dir, 'progress.json')
        self.workflow_file = os.path.join(self.temp_dir, 'workflow.json')
        
        self.generator = ProgressDataGenerator(
            db_progress_json_path=self.progress_file,
            workflow_definition_path=self.workflow_file
        )
        
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init_default_values(self):
        """Test initialization with default values."""
        gen = ProgressDataGenerator()
        self.assertIsNotNone(gen.db_progress_json_path)
        self.assertIsNotNone(gen.workflow_definition_path)
        self.assertEqual(gen.commit_weight, 0.6)
        self.assertEqual(gen.workflow_weight, 0.4)
    
    def test_run_git_log(self):
        """Test running git log."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "commit_hash\ncommit_message\n==END=="
            log_output = self.generator.run_git_log()
            self.assertEqual(log_output, "commit_hash\ncommit_message\n==END==")
    
    def test_parse_git_log(self):
        """Test parsing git log output."""
        log_text = "commit_hash\ncommit_message\n==END==\nfile1.py\nfile2.py\n==END=="
        commits = self.generator.parse_git_log(log_text)
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0]['hash'], "commit_hash")
        self.assertEqual(commits[0]['message'], "commit_message")
        self.assertEqual(commits[0]['files'], ["file1.py", "file2.py"])
    
    def test_load_workflow_definition(self):
        """Test loading workflow definition."""
        with open(self.workflow_file, 'w') as f:
            json.dump({"steps": ["step1", "step2"]}, f)
        
        workflow = self.generator.load_workflow_definition()
        self.assertEqual(workflow, {"steps": ["step1", "step2"]})
    
    def test_map_commits_to_tasks(self):
        """Test mapping commits to tasks."""
        commits = [{"message": "Task 1 completed"}, {"message": "Task 2 completed"}]
        task_progress = self.generator.map_commits_to_tasks(commits)
        self.assertIn("Task 1", task_progress)
        self.assertIn("Task 2", task_progress)
    
    def test_calculate_workflow_progress(self):
        """Test calculating workflow progress."""
        with patch('autoprojectmanagement.main_modules.data_collection_processing.progress_data_generator.ProgressDataGenerator.load_workflow_definition') as mock_load:
            mock_load.return_value = [{"step": "step1"}, {"step": "step2"}]
            progress = self.generator.calculate_workflow_progress()
            self.assertEqual(progress, {})  # Placeholder until implementation is complete
    
    def test_combine_progress(self):
        """Test combining commit and workflow progress."""
        commit_progress = {"Task 1": 50, "Task 2": 75}
        workflow_progress = {"Task 1": 100}
        combined_progress = self.generator.combine_progress(commit_progress, workflow_progress)
        self.assertEqual(combined_progress["Task 1"], 80.0)  # Weighted average
        self.assertEqual(combined_progress["Task 2"], 75.0)  # Only from commits

if __name__ == '__main__':
    unittest.main()
