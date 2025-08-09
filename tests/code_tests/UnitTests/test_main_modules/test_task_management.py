"""
Professional test suite for task_management module.

This module provides comprehensive testing for Task and TaskManagement classes,
including task creation, workflow management, prioritization, and scheduling.
"""

import pytest
from datetime import date, timedelta
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from autoprojectmanagement.main_modules.task_management import Task, TaskManagement


class TestTask:
    """Test cases for the Task class."""
    
    def test_task_creation_minimal(self):
        """Test task creation with minimal required parameters."""
        task = Task(id=1, title="Test Task")
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.status == "pending"
        assert task.priority == 0
        assert task.description == ""
        assert task.deadline is None
        assert task.dependencies == []
        assert task.assigned_to == []
        assert task.parent_id is None
        assert task.github_issue_number is None
    
    def test_task_creation_full_parameters(self):
        """Test task creation with all parameters."""
        deadline = date(2025, 12, 31)
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
        
        assert task.id == 1
        assert task.title == "Complete Project"
        assert task.description == "Finish the main project"
        assert task.deadline == deadline
        assert task.dependencies == [2, 3]
        assert task.assigned_to == ["user1", "user2"]
        assert task.status == "in_progress"
        assert task.priority == 5
        assert task.parent_id == 0
        assert task.urgency == 75.5
        assert task.importance == 85.0
        assert task.github_issue_number == 42
    
    def test_workflow_steps_initialization(self):
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
        assert task.workflow_steps == expected_steps
    
    def test_mark_workflow_step_completed(self):
        """Test marking workflow steps as completed."""
        task = Task(id=1, title="Test Task")
        
        # Initially should be False
        assert not task.workflow_steps["Coding"]
        
        # Mark as completed
        task.mark_workflow_step_completed("Coding")
        assert task.workflow_steps["Coding"]
        
        # Test invalid step - should not raise exception
        task.mark_workflow_step_completed("Invalid Step")
    
    def test_is_workflow_completed(self):
        """Test checking if all workflow steps are completed."""
        task = Task(id=1, title="Test Task")
        
        # Initially should be False
        assert not task.is_workflow_completed()
        
        # Complete all steps
        for step in task.workflow_steps:
            task.mark_workflow_step_completed(step)
        
        assert task.is_workflow_completed()
    
    def test_workflow_progress_percentage(self):
        """Test calculating workflow completion percentage."""
        task = Task(id=1, title="Test Task")
        
        # Initially 0%
        assert task.workflow_progress_percentage() == 0.0
        
        # Complete 2 out of 6 steps
        task.mark_workflow_step_completed("Coding")
        task.mark_workflow_step_completed("Testing")
        expected_progress = (2/6) * 100
        assert task.workflow_progress_percentage() == expected_progress
        
        # Complete all steps
        for step in task.workflow_steps:
            task.mark_workflow_step_completed(step)
        assert task.workflow_progress_percentage() == 100.0
    
    def test_unicode_handling(self):
        """Test handling of unicode characters in task properties."""
        task = Task(
            id=1,
            title="وظيفة تست",
            description="وصف بالعربية مع رموز خاصة: !@#$%^&*()",
            assigned_to=["مستخدم1", "مستخدم2"]
        )
        
        assert task.title == "وظيفة تست"
        assert "وصف بالعربية" in task.description
        assert "مستخدم1" in task.assigned_to
    
    def test_empty_strings_handling(self):
        """Test handling of empty strings and edge cases."""
        task = Task(id=1, title="", description="", assigned_to=[])
        
        assert task.title == ""
        assert task.description == ""
        assert task.assigned_to == []


class TestTaskManagement:
    """Test cases for the TaskManagement class."""
    
    @pytest.fixture
    def task_manager(self):
        """Fixture providing a clean TaskManagement instance."""
        manager = TaskManagement()
        yield manager
        manager.clear_all_tasks()
    
    def test_initialization(self, task_manager):
        """Test TaskManagement initialization."""
        assert len(task_manager.tasks) == 0
        assert task_manager.next_task_id == 1
    
    def test_parse_creative_input(self, task_manager):
        """Test parsing creative input into a task."""
        task = task_manager.parse_creative_input("Create a new feature")
        
        assert task.title == "Create a new feature"
        assert task.id == 1
        assert len(task_manager.tasks) == 1
        assert task_manager.next_task_id == 2
    
    def test_generate_wbs_from_idea(self, task_manager):
        """Test generating WBS from an idea."""
        tasks = task_manager.generate_wbs_from_idea("Build a website")
        
        # Should create root task + subtasks
        assert len(tasks) > 1
        
        # Check that root task exists
        root_task = next(t for t in tasks if t.title == "Build a website")
        assert root_task is not None
        
        # Check that subtasks were created
        subtasks = [t for t in tasks if t.parent_id == root_task.id]
        assert len(subtasks) > 0
    
    def test_update_workflow_steps_from_commit_message(self, task_manager):
        """Test updating workflow steps from commit messages."""
        task = Task(id=1, title="Test Task")
        task_manager.tasks[1] = task
        
        # Test valid commit message
        commit_message = "Task 1: Code Review done"
        task_manager.update_workflow_steps_from_commit_message(commit_message)
        assert task.workflow_steps["Code Review"]
        
        # Test case insensitive
        commit_message = "task 1: testing done"
        task_manager.update_workflow_steps_from_commit_message(commit_message)
        assert task.workflow_steps["Testing"]
        
        # Test invalid task ID - should not affect existing task
        commit_message = "Task 999: Code Review done"
        task_manager.update_workflow_steps_from_commit_message(commit_message)
    
    def test_calculate_urgency_importance(self, task_manager):
        """Test calculating urgency and importance."""
        # Create a simple hierarchy
        root_task = Task(id=1, title="Root Task")
        child_task = Task(id=2, title="Child Task", parent_id=1)
        
        task_manager.tasks[1] = root_task
        task_manager.tasks[2] = child_task
        
        # This should complete without errors
        task_manager.calculate_urgency_importance()
        
        # Verify all tasks have urgency and importance values
        for task in task_manager.tasks.values():
            assert task.urgency is not None
            assert task.importance is not None
            assert task.urgency >= 1
            assert task.importance >= 1
    
    def test_classify_tasks_eisenhower(self, task_manager):
        """Test classifying tasks using Eisenhower matrix."""
        # Create tasks with different urgency/importance values
        task1 = Task(id=1, title="High Priority", urgency=90, importance=90)
        task2 = Task(id=2, title="Low Priority", urgency=10, importance=10)
        task3 = Task(id=3, title="Medium", urgency=50, importance=80)
        task4 = Task(id=4, title="Delegate", urgency=80, importance=30)
        
        task_manager.tasks[1] = task1
        task_manager.tasks[2] = task2
        task_manager.tasks[3] = task3
        task_manager.tasks[4] = task4
        
        # Calculate urgency/importance first
        task_manager.calculate_urgency_importance()
        
        classification = task_manager.classify_tasks_eisenhower()
        
        assert len(classification["do_now"]) == 1
        assert len(classification["schedule"]) == 1
        assert len(classification["delegate"]) == 1
        assert len(classification["eliminate"]) == 1
    
    def test_prioritize_tasks(self, task_manager):
        """Test task prioritization."""
        task1 = Task(id=1, title="Task 1", urgency=90, importance=90)
        task2 = Task(id=2, title="Task 2", urgency=50, importance=50)
        
        task_manager.tasks[1] = task1
        task_manager.tasks[2] = task2
        
        # Calculate urgency/importance first
        task_manager.calculate_urgency_importance()
        
        prioritized = task_manager.prioritize_tasks()
        
        assert len(prioritized) == 2
        # Higher priority task should be first
        assert (prioritized[0].urgency + prioritized[0].importance >=
                prioritized[1].urgency + prioritized[1].importance)
    
    def test_schedule_tasks(self, task_manager):
        """Test task scheduling."""
        task1 = Task(id=1, title="Task 1", urgency=90, importance=90)
        task2 = Task(id=2, title="Task 2", urgency=50, importance=50)
        
        task_manager.tasks[1] = task1
        task_manager.tasks[2] = task2
        
        scheduled = task_manager.schedule_tasks()
        
        assert len(scheduled) == 2
    
    def test_assign_task(self, task_manager):
        """Test assigning tasks to users."""
        task = Task(id=1, title="Test Task")
        task_manager.tasks[1] = task
        
        result = task_manager.assign_task(1, ["user1", "user2"])
        assert result is True
        assert task.assigned_to == ["user1", "user2"]
        
        # Test invalid task ID
        result = task_manager.assign_task(999, ["user1"])
        assert result is False
    
    def test_mark_task_completed(self, task_manager):
        """Test marking tasks as completed."""
        task = Task(id=1, title="Test Task")
        task_manager.tasks[1] = task
        
        result = task_manager.mark_task_completed(1)
        assert result is True
        assert task.status == "completed"
        
        # Test invalid task ID
        result = task_manager.mark_task_completed(999)
        assert result is False
    
    def test_detect_conflicts(self, task_manager):
        """Test detecting conflicts in task dependencies."""
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2", dependencies=[1, 999])  # 999 doesn't exist
        
        task_manager.tasks[1] = task1
        task_manager.tasks[2] = task2
        
        conflicts = task_manager.detect_conflicts()
        assert "Task 2 depends on unknown task 999" in conflicts
    
    def test_detect_conflicts_no_conflicts(self, task_manager):
        """Test when no conflicts exist."""
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=2, title="Task 2", dependencies=[1])
        
        task_manager.tasks[1] = task1
        task_manager.tasks[2] = task2
        
        conflicts = task_manager.detect_conflicts()
        assert len(conflicts) == 0
    
    def test_load_scores(self, task_manager):
        """Test loading scores from JSON file."""
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
            task_manager.tasks[1] = task1
            task_manager.tasks[2] = task2
            
            # Load scores
            task_manager.load_scores(temp_file)
            
            assert task1.importance == 85.5
            assert task2.importance == 92.0
            
        finally:
            Path(temp_file).unlink()
    
    def test_load_scores_nonexistent_file(self, task_manager):
        """Test loading scores from non-existent file."""
        with pytest.raises(FileNotFoundError):
            task_manager.load_scores("nonexistent.json")
    
    def test_calculate_urgency_with_deadline(self, task_manager):
        """Test urgency calculation with deadline."""
        task = Task(id=1, title="Test Task", 
                   deadline=date.today() + timedelta(days=7))
        urgency = task_manager._calculate_urgency(task)
        assert urgency > 0
    
    def test_calculate_urgency_without_deadline(self, task_manager):
        """Test urgency calculation without deadline."""
        task = Task(id=1, title="Test Task")
        urgency = task_manager._calculate_urgency(task)
        assert urgency == 0.1
    
    def test_calculate_importance_with_priority(self, task_manager):
        """Test importance calculation with priority."""
        task = Task(id=1, title="Test Task", priority=5)
        importance = task_manager._calculate_importance(task)
        assert importance == 5
    
    def test_calculate_importance_without_priority(self, task_manager):
        """Test importance calculation without priority."""
        task = Task(id=1, title="Test Task")
        importance = task_manager._calculate_importance(task)
        assert importance == 1.0
    
    def test_empty_tasks_scenarios(self, task_manager):
        """Test various empty tasks scenarios."""
        # Empty classification
        classification = task_manager.classify_tasks_eisenhower()
        assert len(classification["do_now"]) == 0
        assert len(classification["schedule"]) == 0
        assert len(classification["delegate"]) == 0
        assert len(classification["eliminate"]) == 0
        
        # Empty prioritization
        prioritized = task_manager.prioritize_tasks()
        assert len(prioritized) == 0
        
        # Empty scheduling
        scheduled = task_manager.schedule_tasks()
        assert len(scheduled) == 0
        
        # Empty conflicts
        conflicts = task_manager.detect_conflicts()
        assert len(conflicts) == 0
    
    def test_complex_hierarchy_propagation(self, task_manager):
        """Test complex hierarchy with urgency/importance propagation."""
        # Create a 3-level hierarchy
        root = Task(id=1, title="Root")
        child1 = Task(id=2, title="Child 1", parent_id=1)
        child2 = Task(id=3, title="Child 2", parent_id=1)
        grandchild1 = Task(id=4, title="Grandchild 1", parent_id=2)
        grandchild2 = Task(id=5, title="Grandchild 2", parent_id=2)
        
        task_manager.tasks = {1: root, 2: child1, 3: child2, 4: grandchild1, 5: grandchild2}
        
        # This should complete without errors
        task_manager.calculate_urgency_importance()
        
        # Verify all tasks have urgency and importance values
        for task in task_manager.tasks.values():
            assert task.urgency is not None
            assert task.importance is not None
            assert task.urgency >= 1
            assert task.importance >= 1


class TestTaskManagementIntegration:
    """Integration tests for TaskManagement."""
    
    @pytest.fixture
    def task_manager(self):
        """Fixture providing a clean TaskManagement instance."""
        manager = TaskManagement()
        yield manager
        manager.clear_all_tasks()
    
    def test_full_workflow_simulation(self, task_manager):
        """Test complete workflow from task creation to completion."""
        # Create tasks
        task1 = task_manager.parse_creative_input("Implement feature A")
        task2 = task_manager.parse_creative_input("Write tests for feature A")
        task2.parent_id = task1.id
        
        # Assign tasks
        task_manager.assign_task(task1.id, ["developer1"])
        task_manager.assign_task(task2.id, ["qa_engineer"])
        
        # Update workflow steps via commit messages
        task_manager.update_workflow_steps_from_commit_message("Task 1: Coding done")
        task_manager.update_workflow_steps_from_commit_message("Task 1: Testing done")
        task_manager
