#!/usr/bin/env python3
"""
Unit tests for WorkflowDataCollector module.

This module contains comprehensive unit tests for the WorkflowDataCollector class,
covering all public methods and edge cases.

Author: AutoProjectManagement Team
Version: 1.0.0
"""

import pytest
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
from autoprojectmanagement.main_modules.data_collection_processing.workflow_data_collector import (
    WorkflowDataCollector,
    ScrumTask,
    TaskStatus,
    TaskPriority,
    BurndownEntry
)


class TestWorkflowDataCollector:
    """Test suite for WorkflowDataCollector class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def collector(self, temp_dir):
        """Create a WorkflowDataCollector instance with temp directory."""
        return WorkflowDataCollector(data_dir=temp_dir)
    
    @pytest.fixture
    def sample_task(self):
        """Create a sample ScrumTask for testing."""
        return ScrumTask(
            task_id="TASK-001",
            sprint_id="SPRINT-001",
            title="Test Task",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            progress=75
        )
    
    @pytest.fixture
    def sample_burndown(self):
        """Create a sample BurndownEntry for testing."""
        return BurndownEntry(
            sprint_id="SPRINT-001",
            day=1,
            remaining_work=100.0,
            date="2024-01-01"
        )
    
    def test_initialization(self, temp_dir):
        """Test WorkflowDataCollector initialization."""
        collector = WorkflowDataCollector(data_dir=temp_dir)
        assert collector.data_dir == Path(temp_dir)
        assert collector.scrum_sprints_file.exists()
        assert collector.scrum_tasks_file.exists()
        assert collector.scrum_burndown_file.exists()
    
    def test_create_scrum_workflow_tables(self, collector):
        """Test creation of workflow tables."""
        collector.create_scrum_workflow_tables()
        assert collector.scrum_sprints_file.exists()
        assert collector.scrum_tasks_file.exists()
        assert collector.scrum_burndown_file.exists()
    
    def test_update_scrum_task(self, collector, sample_task):
        """Test updating a Scrum task."""
        result = collector.update_scrum_task(sample_task)
        assert result is True
        
        # Verify task was saved
        with open(collector.scrum_tasks_file, 'r') as f:
            tasks = json.load(f)
            assert len(tasks) == 1
            assert tasks[0]['task_id'] == "TASK-001"
            assert tasks[0]['title'] == "Test Task"
    
    def test_update_existing_scrum_task(self, collector, sample_task):
        """Test updating an existing Scrum task."""
        collector.update_scrum_task(sample_task)
        
        # Update the same task
        sample_task.progress = 90
        collector.update_scrum_task(sample_task)
        
        with open(collector.scrum_tasks_file, 'r') as f:
            tasks = json.load(f)
            assert len(tasks) == 1
            assert tasks[0]['progress'] == 90
    
    def test_update_scrum_burndown(self, collector, sample_burndown):
        """Test updating a burndown entry."""
        result = collector.update_scrum_burndown(sample_burndown)
        assert result is True
        
        with open(collector.scrum_burndown_file, 'r') as f:
            burndown = json.load(f)
            assert len(burndown) == 1
            assert burndown[0]['sprint_id'] == "SPRINT-001"
            assert burndown[0]['remaining_work'] == 100.0
    
    def test_update_existing_burndown(self, collector, sample_burndown):
        """Test updating an existing burndown entry."""
        collector.update_scrum_burndown(sample_burndown)
        
        # Update the same entry
        sample_burndown.remaining_work = 85.0
        collector.update_scrum_burndown(sample_burndown)
        
        with open(collector.scrum_burndown_file, 'r') as f:
            burndown = json.load(f)
            assert len(burndown) == 1
            assert burndown[0]['remaining_work'] == 85.0
    
    def test_generate_scrum_report_empty(self, collector):
        """Test generating report for non-existent sprint."""
        report = collector.generate_scrum_report("NON_EXISTENT")
        assert report == []
    
    def test_generate_scrum_report(self, collector):
        """Test generating a Scrum report."""
        # Add multiple burndown entries
        entries = [
            BurndownEntry("SPRINT-001", 1, 100.0, "2024-01-01"),
            BurndownEntry("SPRINT-001", 3, 70.0, "2024-01-03"),
            BurndownEntry("SPRINT-001", 2, 85.0, "2024-01-02")
        ]
        
        for entry in entries:
            collector.update_scrum_burndown(entry)
        
        report = collector.generate_scrum_report("SPRINT-001")
        assert len(report) == 3
        assert report == [(1, 100.0), (2, 85.0), (3, 70.0)]
    
    def test_get_sprint_tasks(self, collector, sample_task):
        """Test getting tasks for a specific sprint."""
        collector.update_scrum_task(sample_task)
        
        # Add another task for different sprint
        task2 = ScrumTask(
            task_id="TASK-002",
            sprint_id="SPRINT-002",
            title="Another Task",
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            progress=0
        )
        collector.update_scrum_task(task2)
        
        sprint_tasks = collector.get_sprint_tasks("SPRINT-001")
        assert len(sprint_tasks) == 1
        assert sprint_tasks[0]['task_id'] == "TASK-001"
    
    def test_get_sprint_tasks_empty(self, collector):
        """Test getting tasks for non-existent sprint."""
        tasks = collector.get_sprint_tasks("NON_EXISTENT")
        assert tasks == []
    
    def test_error_handling_file_not_found(self, temp_dir):
        """Test error handling when files don't exist."""
        collector = WorkflowDataCollector(data_dir=temp_dir)
        
        # Remove files to simulate missing files
        os.remove(collector.scrum_tasks_file)
        
        task = ScrumTask(
            task_id="TASK-001",
            sprint_id="SPRINT-001",
            title="Test",
            status=TaskStatus.TODO,
            priority=TaskPriority.LOW,
            progress=0
        )
        
        # Should handle missing file gracefully
        result = collector.update_scrum_task(task)
        assert result is True  # File will be recreated
    
    def test_error_handling_invalid_json(self, collector):
        """Test error handling with invalid JSON."""
        # Write invalid JSON to file
        with open(collector.scrum_tasks_file, 'w') as f:
            f.write('invalid json')
        
        task = ScrumTask(
            task_id="TASK-001",
            sprint_id="SPRINT-001",
            title="Test",
            status=TaskStatus.TODO,
            priority=TaskPriority.LOW,
            progress=0
        )
        
        # Should handle invalid JSON gracefully
        result = collector.update_scrum_task(task)
        assert result is True
    
    def test_close_method(self, collector):
        """Test the close method."""
        collector.close()  # Should not raise any exceptions
    
    def test_task_status_enum(self):
        """Test TaskStatus enum values."""
        assert TaskStatus.TODO.value == "todo"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.DONE.value == "done"
    
    def test_task_priority_enum(self):
        """Test TaskPriority enum values."""
        assert TaskPriority.LOW.value == 1
        assert TaskPriority.HIGH.value == 3


class TestScrumTask:
    """Test suite for ScrumTask dataclass."""
    
    def test_scrum_task_creation(self):
        """Test creating a ScrumTask instance."""
        task = ScrumTask(
            task_id="TASK-001",
            sprint_id="SPRINT-001",
            title="Test Task",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            progress=75
        )
        
        assert task.task_id == "TASK-001"
        assert task.sprint_id == "SPRINT-001"
        assert task.title == "Test Task"
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.priority == TaskPriority.HIGH
        assert task.progress == 75
    
    def test_scrum_task_optional_fields(self):
        """Test ScrumTask with optional fields."""
        task = ScrumTask(
            task_id="TASK-001",
            sprint_id="SPRINT-001",
            title="Test Task",
            status=TaskStatus.TODO,
            priority=TaskPriority.LOW,
            progress=0,
            description="Test description",
            assignee="user@example.com",
            estimated_hours=8.0
        )
        
        assert task.description == "Test description"
        assert task.assignee == "user@example.com"
        assert task.estimated_hours == 8.0


class TestBurndownEntry:
    """Test suite for BurndownEntry dataclass."""
    
    def test_burndown_entry_creation(self):
        """Test creating a BurndownEntry instance."""
        entry = BurndownEntry(
            sprint_id="SPRINT-001",
            day=1,
            remaining_work=100.0,
            date="2024-01-01"
        )
        
        assert entry.sprint_id == "SPRINT-001"
        assert entry.day == 1
        assert entry.remaining_work == 100.0
        assert entry.date == "2024-01-01"


if __name__ == "__main__":
    pytest.main([__file__])
