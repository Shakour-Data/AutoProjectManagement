import unittest
import datetime
import os
import tempfile
import json
from unittest.mock import Mock, patch, mock_open

# Import the actual classes from the correct path
from autoprojectmanagement.main_modules.task_management import Task, TaskManagement


class TestTaskManagement(unittest.TestCase):
    """Comprehensive test suite for Task and TaskManagement classes"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.task_manager = TaskManagement()

    def tearDown(self):
        """Clean up after each test method."""
        self.task_manager.clear_all_tasks()

    # ==================== Task Class Tests ====================

    def test_task_creation_basic(self):
        """Test basic task creation with required parameters."""
        task = Task(id=1, title="Test Task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.priority, 0)
        self.assertEqual(task.description, "")
        self.assertIsNone(task.deadline)
        self.assertEqual(task.dependencies, [])
        self.assertEqual(task.assigned_to, [])
        self.assertIsNone(task.parent_id)
        self.assertIsNone(task.github_issue_number)

    def test_task_creation_with_all_parameters(self):
        """Test task creation with all parameters."""
        deadline = datetime.date(2025, 12, 31)
        task = Task(
            id=1,
            title="Complete Project",
            description="Finish the main project",
            deadline=deadline,
            dependencies=[2, 3],
            assigned_to=["user1", "user2"],
            status="in_progress",
            priority=5,
            parent_id=0,
            urgency=75.5,
            importance=85.0,
            github_issue_number=42
        )
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Complete Project")
        self.assertEqual(task.description, "Finish the main project")
        self.assertEqual(task.deadline, deadline)
        self.assertEqual(task.dependencies, [2, 3])
        self.assertEqual(task.assigned_to, ["user1", "user2"])
        self.assertEqual(task.status, "in_progress")
        self.assertEqual(task.priority, 5)
        self.assertEqual(task.parent_id, 0)
        self.assertEqual(task.urgency, 75.5)
        self.assertEqual(task.importance, 85.0)
        self.assertEqual(task.github_issue_number, 42)

    def test_task_workflow_steps_initialization(self):
        """Test that workflow steps are properly initialized."""
        task = Task(id=1, title="Test Task")
        expected_steps = {
            "Coding": False,
            "Testing": False,
            "Documentation": False,
            "Code Review": False,
            "Merge and Deployment": False,
            "Verification": False,
        }
        self.assertEqual(task.workflow_steps, expected_steps)

    def test_mark_workflow_step_completed(self):
        """Test marking workflow steps as completed."""
        task = Task(id=1, title="Test Task")
        
        # Initially should be False
        self.assertFalse(task.workflow_steps["Coding"])
        
        # Mark as completed
        task.mark_workflow_step_completed("Coding")
        self.assertTrue(task.workflow_steps["Coding"])
        
        # Test invalid step
        task.mark_workflow_step_completed("Invalid Step")
        # Should not raise exception

    def test_is_workflow_completed(self):
        """Test checking if all workflow steps are completed."""
        task = Task(id=1, title="Test Task")
        
        # Initially should be False
        self.assertFalse(task.is_workflow_completed())
        
        # Complete all steps
        for step in task.workflow_steps:
            task.mark_workflow_step_completed(step)
        
        self.assertTrue(task.is_workflow_completed())

    def test_workflow_progress_percentage(self):
        """Test calculating workflow completion percentage."""
        task = Task(id=1, title="Test Task")
        
        # Initially 0%
        self.assertEqual(task.workflow_progress_percentage(), 0.0)
        
        # Complete 2 out of 6 steps
        task.mark_workflow_step_completed("Coding")
        task.mark_workflow_step_completed("Testing")
        expected_progress = (2/6) * 100
        self.assertEqual(task.workflow_progress_percentage(), expected_progress)
        
        # Complete all steps
        for step in task.workflow_steps:
            task.mark_workflow_step_completed(step)
        self.assertEqual(task.workflow_progress_percentage(), 100.0)

    # ==================== TaskManagement Class Tests ====================

    def test_task_management_initialization(self):
        """Test TaskManagement initialization."""
        manager = TaskManagement()
        self.assertEqual(len(manager.tasks), 0)
        self.assertEqual(manager.next_task_id, 1)

    def test_parse_creative_input(self):
        """Test parsing creative input into a task."""
        task = self.task_manager.parse_creative_input("Create a new feature")
        self.assertEqual(task.title, "Create a new feature")
        self.assertEqual(task.id, 1)
        self.assertEqual(len(self.task_manager.tasks), 1)
        self.assertEqual(self.task_manager.next_task_id, 2)

    def test_generate_wbs_from_idea(self):
        """Test generating WBS from an idea."""
        tasks = self.task_manager.generate_wbs_from_idea("Build a website")
        
        # Should create root task + subtasks
        self.assertGreater(len(tasks), 1)
        
        # Check that root task exists
        root_task = next(t for t in tasks if t.title == "Build a website")
        self.assertIsNotNone(root_task)
        
        # Check that subtasks were created
        subtasks = [t for t in tasks if t.parent_id == root_task.id]
        self.assertGreater(len(subtasks), 0)

    def test_update_workflow_steps_from_commit_message(self):
        """Test updating workflow steps from commit messages."""
        task = Task(id=1, title="Test Task")
        self.task_manager.tasks[1] = task
        
        # Test valid commit message
        commit_message = "Task 1: Code Review done"
        self.task_manager.update_workflow_steps_from_commit_message(commit_message)
        self.assertTrue(task.workflow_steps["Code Review"])
        
        # Test case insensitive
        commit_message = "task 1: testing done"
        self.task_manager.update_workflow_steps_from_commit_message(commit_message)
        self.assertTrue(task.workflow_steps["Testing"])
        
        # Test invalid task ID
        commit_message = "Task 999: Code Review done"
        self.task_manager.update_workflow_steps_from_commit_message(commit_message)
        # Should not affect existing task

    def test_calculate_urgency_importance(self):
        """Test calculating urgency and importance."""
        # Create a simple hierarchy
        root_task = Task(id=1, title="Root Task")
        child_task = Task(id=2, title="Child Task", parent_id=1)
        
        self.task_manager.tasks[1] = root_task
        self.task_manager.tasks[2] = child_task
        
        # This should complete without errors
        self.task_manager.calculate_urgency_importance()
        
        # Verify all tasks have urgency and importance values
        for task in self.task_manager.tasks.values():
            self.assertIsNotNone(task.urgency)
            self.assertIsNotNone(task.importance)
            self.assertGreaterEqual(task.urgency, 1)
            self.assertGreaterEqual(task.importance, 1)

    def test_classify_tasks_eisenhower(self):
        """Test classifying tasks using Eisenhower matrix."""
        # Create tasks with different urgency/importance values
        task1 = Task(id=1, title="High Priority", urgency=90, importance=90)
        task2 = Task(id=2, title="Low Priority", urgency=10, importance=10)
        task3 = Task(id=3, title="Medium", urgency=50, importance=80)
        task4 = Task(id=4, title="Delegate", urgency=80, importance=30)
        
        self.task_manager.tasks[1] = task1
        self.task_manager.tasks[2] = task2
        self.task_manager.tasks[3] = task3
        self.task_manager.tasks[4] = task4
        
        # Calculate urgency/importance first
        self.task_manager.calculate_urgency_importance()
        
        classification = self.task_manager.classify_tasks_eisenhower()
        
        self.assertEqual(len(classification["do_now"]), 1)
        self.assertEqual(len(classification["schedule"]), 1)
        self.assertEqual(len(classification["delegate"]), 1)
        self.assertEqual(len(classification["eliminate"]), 1)

    def test_prioritize_tasks(self):
        """Test task prioritization."""
        task1 = Task(id=1, title="Task 1", urgency=90, importance=90)
        task2 = Task(id=2, title="Task 2", urgency=50, importance=50)
        
        self.task_manager.tasks[1] = task1
        self.task_manager.tasks[2] = task2
        
        # Calculate urgency/importance first
        self.task_manager.calculate_urgency_importance()
        
        prioritized = self.task_manager.prioritize_tasks()
        
        self.assertEqual(len(prioritized), 2)
        # Higher priority task should be first
        self.assertGreaterEqual(prioritized[0].urgency + prioritized[0].importance,
                               prioritized[1].urgency + prioritized[1].importance)

    def test_schedule_tasks(self):
        """Test task scheduling."""
        task1 = Task(id=1, title="Task 1", urgency=90, importance=90)
        task2 = Task(id=2, title="Task 2", urgency=50, importance=50)
        
        self.task_manager.tasks[1] = task1
        self.task_manager.tasks[2] = task2
        
        scheduled = self.task_manager.schedule_tasks()
        
        self.assertEqual(len(scheduled), 2)

    def test_assign_task(self):
        """Test assigning tasks to users."""
        task = Task(id=1, title="Test Task")
        self.task_manager.tasks[1] = task
        
        result = self.task_manager.assign_task(1, ["user1", "user2"])
        self.assertTrue(result)
        self.assertEqual(task.assigned_to, ["user1", "user2"])
        
        # Test invalid task ID
        result = self.task_manager.assign_task(999, ["user1"])
        self.assertFalse(result)

    def test_mark_task_completed(self):
        """Test marking tasks as completed."""
        task = Task(id=1, title="Test Task")
        self.task_manager.tasks[1] = task
        
        result = self.task_manager.mark_task_completed(1)
        self.assertTrue(result)
        self.assertEqual(task.status, "completed")
        
        # Test invalid task ID
        result = self.task_manager.mark_task_completed(999)
        self.assertFalse(result)

    def test_detect_conflicts(self):
        """Test detecting conflicts in task dependencies."""
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2", dependencies=[1, 999])  # 999 doesn't exist
        
        self.task_manager.tasks[1] = task1
        self.task_manager.tasks[2] = task2
        
        conflicts = self.task_manager.detect_conflicts()
        self.assertIn("Task 2 depends on unknown task 999", conflicts)

    def test_detect_conflicts_no_conflicts(self):
        """Test when no conflicts exist."""
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2", dependencies=[1])
        
        self.task_manager.tasks[1] = task1
        self.task_manager.tasks[2] = task2
        
        conflicts = self.task_manager.detect_conflicts()
        self.assertEqual(len(conflicts), 0)

    def test_load_scores(self):
        """Test loading scores from JSON file."""
        # Create a temporary JSON file
        scores_data = {
            "1": {"importance": 85.5},
            "2": {"importance": 92.0}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(scores_data, f)
            temp_file = f.name
        
        try:
            # Create tasks
            task1 = Task(id=1, title="Task 1")
            task2 = Task(id=2, title="Task 2")
            self.task_manager.tasks[1] = task1
            self.task_manager.tasks[2] = task2
            
            # Load scores
            self.task_manager.load_scores(temp_file)
            
            self.assertEqual(task1.importance, 85.5)
            self.assertEqual(task2.importance, 92.0)
            
        finally:
            os.unlink(temp_file)

    def test_load_scores_nonexistent_file(self):
        """Test loading scores from non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.task_manager.load_scores("nonexistent.json")

    def test_calculate_urgency_with_deadline(self):
        """Test urgency calculation with deadline."""
        task = Task(id=1, title="Test Task", 
                   deadline=datetime.date.today() + datetime.timedelta(days=7))
        urgency = self.task_manager._calculate_urgency(task)
        self.assertGreater(urgency, 0)

    def test_calculate_urgency_without_deadline(self):
        """Test urgency calculation without deadline."""
        task = Task(id=1, title="Test Task")
        urgency = self.task_manager._calculate_urgency(task)
        self.assertEqual(urgency, 0.1)

    def test_calculate_importance_with_priority(self):
        """Test importance calculation with priority."""
        task = Task(id=1, title="Test Task", priority=5)
        importance = self.task_manager._calculate_importance(task)
        self.assertEqual(importance, 5)

    def test_calculate_importance_without_priority(self):
        """Test importance calculation without priority."""
        task = Task(id=1, title="Test Task")
        importance = self.task_manager._calculate_importance(task)
        self.assertEqual(importance, 1.0)

    def test_empty_tasks_scenarios(self):
        """Test various empty tasks scenarios."""
        # Empty classification
        classification = self.task_manager.classify_tasks_eisenhower()
        self.assertEqual(len(classification["do_now"]), 0)
        self.assertEqual(len(classification["schedule"]), 0)
        self.assertEqual(len(classification["delegate"]), 0)
        self.assertEqual(len(classification["eliminate"]), 0)
        
        # Empty prioritization
        prioritized = self.task_manager.prioritize_tasks()
        self.assertEqual(len(prioritized), 0)
        
        # Empty scheduling
        scheduled = self.task_manager.schedule_tasks()
        self.assertEqual(len(scheduled), 0)
        
        # Empty conflicts
        conflicts = self.task_manager.detect_conflicts()
        self.assertEqual(len(conflicts), 0)

    def test_unicode_and_special_characters(self):
        """Test handling of unicode and special characters."""
        # Unicode title
        task1 = Task(id=1, title="وظیفه تست")
        self.assertEqual(task1.title, "وظیفه تست")
        
        # Special characters
        task2 = Task(id=2, title="Test!@#$%^&*()")
        self.assertEqual(task2.title, "Test!@#$%^&*()")
        
        # Empty title
        task3 = Task(id=3, title="")
        self.assertEqual(task3.title, "")

    def test_complex_hierarchy_propagation(self):
        """Test complex hierarchy with urgency/importance propagation."""
        # Create a 3-level hierarchy
        root = Task(id=1, title="Root")
        child1 = Task(id=2, title="Child 1", parent_id=1)
        child2 = Task(id=3, title="Child 2", parent_id=1)
        grandchild1 = Task(id=4, title="Grandchild 1", parent_id=2)
        grandchild2 = Task(id=5, title="Grandchild 2", parent_id=2)
        
        self.task_manager.tasks = {1: root, 2: child1, 3: child2, 4: grandchild1, 5: grandchild2}
        
        # This should complete without errors
        self.task_manager.calculate_urgency_importance()
        
        # Verify all tasks have urgency and importance values
        for task in self.task_manager.tasks.values():
            self.assertIsNotNone(task.urgency)
            self.assertIsNotNone(task.importance)
            self.assertGreaterEqual(task.urgency, 1)
            self.assertGreaterEqual(task.importance, 1)


if __name__ == "__main__":
    unittest.main()
