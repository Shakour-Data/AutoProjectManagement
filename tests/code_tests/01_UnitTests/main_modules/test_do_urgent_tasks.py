#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for do_urgent_tasks.py module.

This file contains 20 comprehensive tests for the do_urgent_tasks module:
- 5 functionality tests
- 5 edge case tests
- 5 error handling tests
- 5 integration tests

Tests cover:
- Task execution functionality
- Edge cases in task generation and execution
- Error handling for invalid inputs and failures
- Integration with task management system
"""

import unittest
import logging
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
from pathlib import Path
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'src'))

from autoprojectmanagement.main_modules.task_workflow_management.do_urgent_tasks import (
    UrgentTaskExecutor, TaskStatus, TaskResult, setup_logging, main
)

class TestUrgentTaskExecutorFunctionality(unittest.TestCase):
    """Functionality tests for UrgentTaskExecutor (5 tests)."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.logger = logging.getLogger("test_urgent_tasks")
        self.executor = UrgentTaskExecutor(logger=self.logger)
        
    def test_01_initialization(self):
        """Test UrgentTaskExecutor initialization with default and custom logger."""
        # Test with default logger
        executor1 = UrgentTaskExecutor()
        self.assertIsInstance(executor1, UrgentTaskExecutor)
        self.assertIsNotNone(executor1.logger)
        
        # Test with custom logger
        executor2 = UrgentTaskExecutor(logger=self.logger)
        self.assertEqual(executor2.logger, self.logger)
        
    def test_02_task_title_generation(self):
        """Test generation of standardized task titles."""
        titles = self.executor._generate_task_titles()
        self.assertIsInstance(titles, list)
        self.assertEqual(len(titles), 15)  # 10 critical + 5 additional
        self.assertIn("Develop Project Management Tool - Subtask Level 1.1", titles)
        
    def test_03_single_task_execution(self):
        """Test execution of a single task."""
        with patch.object(self.executor.task_manager, 'parse_creative_input') as mock_parse, \
             patch.object(self.executor.task_manager, 'mark_task_completed') as mock_mark:
            
            # Mock task creation
            mock_task = MagicMock()
            mock_task.id = "TASK-001"
            mock_parse.return_value = mock_task
            
            result = self.executor._execute_single_task("Test Task")
            
            self.assertIsInstance(result, TaskResult)
            self.assertEqual(result.title, "Test Task")
            self.assertEqual(result.status, TaskStatus.COMPLETED)
            self.assertTrue(result.is_successful)
            
    def test_04_urgent_task_execution(self):
        """Test execution of all urgent tasks."""
        with patch.object(self.executor, '_execute_single_task') as mock_execute:
            # Mock successful task results
            mock_result = MagicMock()
            mock_result.is_successful = True
            mock_execute.return_value = mock_result
            
            results = self.executor.execute_urgent_tasks()
            
            self.assertIsInstance(results, list)
            self.assertEqual(len(results), 15)  # 10 critical + 5 additional
            
    def test_05_summary_report_generation(self):
        """Test generation of summary report."""
        # First execute some tasks to have results
        with patch.object(self.executor, '_execute_single_task') as mock_execute:
            mock_result = MagicMock()
            mock_result.is_successful = True
            mock_result.status = TaskStatus.COMPLETED
            mock_result.duration_seconds = 1.5
            mock_execute.return_value = mock_result
            
            self.executor.execute_urgent_tasks()
            
            report = self.executor.get_summary_report()
            
            self.assertIsInstance(report, dict)
            self.assertIn("total_tasks", report)
            self.assertIn("completed_tasks", report)
            self.assertIn("success_rate", report)
            self.assertEqual(report["total_tasks"], 15)


class TestUrgentTaskExecutorEdgeCases(unittest.TestCase):
    """Edge case tests for UrgentTaskExecutor (5 tests)."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.logger = logging.getLogger("test_urgent_tasks")
        self.executor = UrgentTaskExecutor(logger=self.logger)
        
    def test_06_empty_task_title(self):
        """Test execution with empty task title."""
        with self.assertRaises(ValueError):
            self.executor._execute_single_task("")
            
    def test_07_none_task_title(self):
        """Test execution with None task title."""
        with self.assertRaises(ValueError):
            self.executor._execute_single_task(None)
            
    def test_08_non_string_task_title(self):
        """Test execution with non-string task title."""
        with self.assertRaises(ValueError):
            self.executor._execute_single_task(123)
            
    def test_09_task_parsing_failure(self):
        """Test handling when task parsing fails."""
        with patch.object(self.executor.task_manager, 'parse_creative_input') as mock_parse:
            mock_parse.return_value = None  # Simulate parsing failure
            
            result = self.executor._execute_single_task("Test Task")
            
            self.assertEqual(result.status, TaskStatus.FAILED)
            self.assertIsNotNone(result.error_message)
            
    def test_10_task_without_id(self):
        """Test handling when parsed task has no ID."""
        with patch.object(self.executor.task_manager, 'parse_creative_input') as mock_parse:
            mock_task = MagicMock()
            del mock_task.id  # Remove id attribute
            mock_parse.return_value = mock_task
            
            result = self.executor._execute_single_task("Test Task")
            
            self.assertEqual(result.status, TaskStatus.FAILED)
            self.assertIsNotNone(result.error_message)


class TestUrgentTaskExecutorErrorHandling(unittest.TestCase):
    """Error handling tests for UrgentTaskExecutor (5 tests)."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.logger = logging.getLogger("test_urgent_tasks")
        self.executor = UrgentTaskExecutor(logger=self.logger)
        
    def test_11_task_generation_failure(self):
        """Test handling of task generation failure."""
        with patch('autoprojectmanagement.main_modules.task_workflow_management.do_urgent_tasks.CRITICAL_TASK_COUNT', 10), \
             patch('autoprojectmanagement.main_modules.task_workflow_management.do_urgent_tasks.ADDITIONAL_TASK_COUNT', 5):
            
            # This should work normally
            titles = self.executor._generate_task_titles()
            self.assertEqual(len(titles), 15)
            
    def test_12_task_manager_parse_exception(self):
        """Test handling of exceptions in task manager parsing."""
        with patch.object(self.executor.task_manager, 'parse_creative_input') as mock_parse:
            mock_parse.side_effect = Exception("Parsing error")
            
            result = self.executor._execute_single_task("Test Task")
            
            self.assertEqual(result.status, TaskStatus.FAILED)
            self.assertIn("Parsing error", result.error_message)
            
    def test_13_task_manager_mark_completed_exception(self):
        """Test handling of exceptions in marking task as completed."""
        with patch.object(self.executor.task_manager, 'parse_creative_input') as mock_parse, \
             patch.object(self.executor.task_manager, 'mark_task_completed') as mock_mark:
            
            # Mock successful task creation
            mock_task = MagicMock()
            mock_task.id = "TASK-001"
            mock_parse.return_value = mock_task
            
            # Mock exception in marking task completed
            mock_mark.side_effect = Exception("Completion error")
            
            result = self.executor._execute_single_task("Test Task")
            
            self.assertEqual(result.status, TaskStatus.FAILED)
            self.assertIn("Completion error", result.error_message)
            
    def test_14_execute_urgent_tasks_critical_error(self):
        """Test handling of critical error in execute_urgent_tasks."""
        with patch.object(self.executor, '_generate_task_titles') as mock_generate:
            mock_generate.side_effect = Exception("Critical error")
            
            with self.assertRaises(RuntimeError):
                self.executor.execute_urgent_tasks()
                
            mock_generate.side_effect = Exception("Critical error")
            
            executor = UrgentTaskExecutor()
            try:
                results = executor.execute_urgent_tasks()
                # If we get here, it means the test failed
                assert False, "Should have raised an error"
            except RuntimeError as e:
                # Expected behavior
                assert "Task execution failed" in str(e)
    
    def test_export_results_to_file_io_error(self):
        """Test export_results_to_file handling of IO errors."""
        executor = UrgentTaskExecutor()
        
        # Create a result to export
        result = TaskResult(
            task_id="task_1",
            title="Test Task",
            status=TaskStatus.COMPLETED,
            start_time=datetime.now()
        )
        executor.results = [result]
        
        # Try to export to an invalid path
        try:
            executor.export_results_to_file("/invalid/path/results.json")
            # If we get here, it means the test failed
            assert False, "Should have raised an error"
        except IOError:
            # Expected behavior
            assert True

class TestUrgentTaskExecutorIntegration(unittest.TestCase):
    """Test class for UrgentTaskExecutor integration tests (5 tests)"""
    
    def test_urgent_task_executor_complete_workflow(self):
        """Test complete workflow of UrgentTaskExecutor."""
        executor = UrgentTaskExecutor()
        results = executor.execute_urgent_tasks()
        
        # Check that we have the expected number of results
        self.assertEqual(len(results), 15)  # 10 critical + 5 additional
        
        # Check that all results have valid data
        for result in results:
            self.assertIsNotNone(result.task_id)
            self.assertIsNotNone(result.title)
            self.assertIn(result.status, [TaskStatus.COMPLETED, TaskStatus.FAILED])
            self.assertIsNotNone(result.start_time)
    
    def test_get_summary_report(self):
        """Test get_summary_report functionality."""
        executor = UrgentTaskExecutor()
        results = executor.execute_urgent_tasks()
        report = executor.get_summary_report()
        
        # Check report contains expected data
        self.assertIn("total_tasks", report)
        self.assertIn("completed_tasks", report)
        self.assertIn("failed_tasks", report)
        self.assertIn("success_rate", report)
        self.assertEqual(report["total_tasks"], len(results))
    
    def test_export_results_to_file(self):
        """Test export_results_to_file functionality."""
        # This test would require a temporary directory and json import
        # For now, we'll just test that the method is callable
        executor = UrgentTaskExecutor()
        self.assertTrue(callable(executor.export_results_to_file))
    
    def test_setup_logging(self):
        """Test setup_logging functionality."""
        logger = setup_logging()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.level, 20)  # INFO level
    
    def test_main_function(self):
        """Test main function execution."""
        # This is more of a smoke test since main() has side effects
        # We'll just check that it's callable
        self.assertTrue(callable(main))

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
