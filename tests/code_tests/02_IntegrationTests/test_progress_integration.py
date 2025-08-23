#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: test_progress_integration
File: test_progress_integration.py
Path: tests/code_tests/02_IntegrationTests/test_progress_integration.py

Description:
    Test Progress Integration module

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
    >>> from tests.code_tests.02_IntegrationTests.test_progress_integration import {main_class}
    >>> instance = {main_class}()
    >>> instance.run()

Notes:
    - This file follows the AutoProjectManagement coding standards
    - All changes should be documented in the changelog below
    - Ensure compatibility with Python 3.8+

Changelog:
    1.0.0 (2024-01-01): Initial release
    1.0.1 (2025-08-14): Fixed syntax error and duplicate test methods

TODO:
    - [ ] Add comprehensive error handling
    - [ ] Implement logging throughout
    - [ ] Add unit tests
    - [ ] Update documentation

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


class TestProgressIntegration(unittest.TestCase):
    """Integration tests for progress_data_generator module."""
    
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
    
    def test_init_custom_values(self):
        """Test initialization with custom values."""
        gen = ProgressDataGenerator(
            db_progress_json_path='custom_progress.json',
            workflow_definition_path='custom_workflow.json',
            commit_weight=0.7,
            workflow_weight=0.3
        )
        self.assertEqual(gen.db_progress_json_path, 'custom_progress.json')
        self.assertEqual(gen.workflow_definition_path, 'custom_workflow.json')
        self.assertEqual(gen.commit_weight, 0.7)
        self.assertEqual(gen.workflow_weight, 0.3)
    
    def test_load_progress_data_empty_file(self):
        """Test loading progress data from empty file."""
        # Create empty progress file
        with open(self.progress_file, 'w') as f:
            json.dump({}, f)
        
        progress_data = self.generator.load_progress_data()
        self.assertEqual(progress_data, {})
    
    def test_load_progress_data_valid_file(self):
        """Test loading progress data from valid file."""
        test_data = {
            "total_commits": 10,
            "completed_tasks": 5,
            "progress_percentage": 50.0
        }
        
        with open(self.progress_file, 'w') as f:
            json.dump(test_data, f)
        
        progress_data = self.generator.load_progress_data()
        self.assertEqual(progress_data, test_data)
    
    def test_load_workflow_data_empty_file(self):
        """Test loading workflow data from empty file."""
        # Create empty workflow file
        with open(self.workflow_file, 'w') as f:
            json.dump({}, f)
        
        workflow_data = self.generator.load_workflow_data()
        self.assertEqual(workflow_data, {})
    
    def test_load_workflow_data_valid_file(self):
        """Test loading workflow data from valid file."""
        test_data = {
            "total_steps": 20,
            "completed_steps": 10,
            "progress_percentage": 50.0
        }
        
        with open(self.workflow_file, 'w') as f:
            json.dump(test_data, f)
        
        workflow_data = self.generator.load_workflow_data()
        self.assertEqual(workflow_data, test_data)
    
    def test_calculate_overall_progress(self):
        """Test calculating overall progress."""
        # Mock the data loading methods
        with patch.object(self.generator, 'load_progress_data') as mock_progress, \
             patch.object(self.generator, 'load_workflow_data') as mock_workflow:
            
            mock_progress.return_value = {
                "total_commits": 10,
                "completed_tasks": 5,
                "progress_percentage": 50.0
            }
            
            mock_workflow.return_value = {
                "total_steps": 20,
                "completed_steps": 10,
                "progress_percentage": 50.0
            }
            
            overall_progress = self.generator.calculate_overall_progress()
            
            # Should be weighted average: (0.6 * 50) + (0.4 * 50) = 50
            self.assertEqual(overall_progress, 50.0)
    
    def test_generate_progress_data_function(self):
        """Test the standalone generate_progress_data function."""
        with patch('autoprojectmanagement.main_modules.data_collection_processing.progress_data_generator.ProgressDataGenerator') as mock_class:
            mock_instance = MagicMock()
            mock_instance.calculate_overall_progress.return_value = 75.0
            mock_class.return_value = mock_instance
            
            result = generate_progress_data()
            
            self.assertEqual(result, 75.0)
            mock_class.assert_called_once()
            mock_instance.calculate_overall_progress.assert_called_once()


if __name__ == '__main__':
    unittest.main()
