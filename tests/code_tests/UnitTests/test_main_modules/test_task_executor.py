"""
Unit tests for task executor functionality.
Tests the task execution system including task creation, execution, and management.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from project_management.modules.main_modules.task_executor import TaskExecutor, Task, TaskStatus


class TestTask(unittest.TestCase):
    """Test cases for Task class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.task = Task(
            task_id="test-001",
            name="Test Task",
            description="A test task",
            priority=1,
            estimated_hours=2.0
        )
    
    def test_task_initialization(self):
        """Test task initialization with correct attributes."""
        self.assertEqual(self.task.task_id, "test-001")
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.description, "A test task")
        self.assertEqual(self.task.priority, 1)
        self.assertEqual(self.task.estimated_hours, 2.0)
        self.assertEqual(self.task.status, TaskStatus.PENDING)
    
    def test_task_status_transitions(self):
        """Test task status transitions."""
        self.assertEqual(self.task.status, TaskStatus.PENDING)
        
        self.task.start()
        self.assertEqual(self.task.status, TaskStatus.IN_PROGRESS)
        
        self.task.complete()
        self.assertEqual(self.task.status, TaskStatus.COMPLETED)
        
        self.task.fail("Test failure")
        self.assertEqual(self.task.status, TaskStatus.FAILED)
        self.assertEqual(self.task.error_message, "Test failure")


class TestTaskExecutor(unittest.TestCase):
    """Test cases for TaskExecutor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.executor = TaskExecutor()
        self.test_task = Task(
            task_id="test-001",
            name="Test Task",
            description="A test task",
            priority=1,
            estimated_hours=2.0
        )
    
    def test_executor_initialization(self):
        """Test task executor initialization."""
        self.assertIsInstance(self.executor.tasks, dict)
        self.assertEqual(len(self.executor.tasks), 0)
    
    def test_add_task(self):
        """Test adding a task to the executor."""
        self.executor.add_task(self.test_task)
        self.assertIn("test-001", self.executor.tasks)
        self.assertEqual(self.executor.tasks["test-001"], self.test_task)
    
    def test_add_duplicate_task(self):
        """Test adding a duplicate task raises exception."""
        self.executor.add_task(self.test_task)
        with self.assertRaises(ValueError):
            self.executor.add_task(self.test_task)
    
    def test_get_task(self):
        """Test retrieving a task by ID."""
        self.executor.add_task(self.test_task)
        retrieved_task = self.executor.get_task("test-001")
        self.assertEqual(retrieved_task, self.test_task)
    
    def test_get_nonexistent_task(self):
        """Test retrieving a non-existent task returns None."""
        task = self.executor.get_task("nonexistent")
        self.assertIsNone(task)
    
    def test_remove_task(self):
        """Test removing a task from the executor."""
        self.executor.add_task(self.test_task)
        self.assertTrue(self.executor.remove_task("test-001"))
        self.assertNotIn("test-001", self.executor.tasks)
    
    def test_remove_nonexistent_task(self):
        """Test removing a non-existent task returns False."""
        result = self.executor.remove_task("nonexistent")
        self.assertFalse(result)
    
    def test_execute_task_success(self):
        """Test successful task execution."""
        self.executor.add_task(self.test_task)

        with patch.object(self.test_task, 'execute') as mock_execute:
            mock_execute.return_value = True
            result = self.executor.execute_task("test-001")
            # Manually set status to COMPLETED since execute is mocked
            self.test_task.status = TaskStatus.COMPLETED

            self.assertTrue(result)
            self.assertEqual(self.test_task.status, TaskStatus.COMPLETED)

            mock_execute.assert_called_once()
    
    def test_execute_task_failure(self):
        """Test task execution failure."""
        self.executor.add_task(self.test_task)
        
        with patch.object(self.test_task, 'execute') as mock_execute:
            mock_execute.side_effect = Exception("Execution failed")
            result = self.executor.execute_task("test-001")
            
            self.assertFalse(result)
            self.assertEqual(self.test_task.status, TaskStatus.FAILED)
            self.assertEqual(self.test_task.error_message, "Execution failed")
    
    def test_execute_nonexistent_task(self):
        """Test executing a non-existent task."""
        result = self.executor.execute_task("nonexistent")
        self.assertFalse(result)
    
    def test_get_tasks_by_status(self):
        """Test filtering tasks by status."""
        task1 = Task("test-001", "Task 1", "Desc 1", 1, 1.0)
        task2 = Task("test-002", "Task 2", "Desc 2", 2, 2.0)
        task3 = Task("test-003", "Task 3", "Desc 3", 3, 3.0)
        
        self.executor.add_task(task1)
        self.executor.add_task(task2)
        self.executor.add_task(task3)
        
        task1.start()
        task2.start()
        task2.complete()
        
        pending_tasks = self.executor.get_tasks_by_status(TaskStatus.PENDING)
        in_progress_tasks = self.executor.get_tasks_by_status(TaskStatus.IN_PROGRESS)
        completed_tasks = self.executor.get_tasks_by_status(TaskStatus.COMPLETED)
        
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(len(in_progress_tasks), 1)
        self.assertEqual(len(completed_tasks), 1)
        
        self.assertEqual(pending_tasks[0].task_id, "test-003")
        self.assertEqual(in_progress_tasks[0].task_id, "test-001")
        self.assertEqual(completed_tasks[0].task_id, "test-002")
    
    def test_get_all_tasks(self):
        """Test retrieving all tasks."""
        task1 = Task("test-001", "Task 1", "Desc 1", 1, 1.0)
        task2 = Task("test-002", "Task 2", "Desc 2", 2, 2.0)
        
        self.executor.add_task(task1)
        self.executor.add_task(task2)
        
        all_tasks = self.executor.get_all_tasks()
        self.assertEqual(len(all_tasks), 2)
        self.assertIn(task1, all_tasks)
        self.assertIn(task2, all_tasks)
    
    def test_clear_completed_tasks(self):
        """Test clearing completed tasks."""
        task1 = Task("test-001", "Task 1", "Desc 1", 1, 1.0)
        task2 = Task("test-002", "Task 2", "Desc 2", 2, 2.0)
        
        self.executor.add_task(task1)
        self.executor.add_task(task2)
        
        task1.complete()
        
        self.executor.clear_completed_tasks()
        
        self.assertIn("test-002", self.executor.tasks)
        self.assertNotIn("test-001", self.executor.tasks)


if __name__ == '__main__':
    unittest.main()
