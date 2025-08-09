"""
Comprehensive unit tests for task_management module
"""
import pytest
from unittest.mock import Mock, patch, mock_open
import json
from datetime import datetime, timedelta

from autoprojectmanagement.main_modules.task_management import TaskManager


class TestTaskManager:
    """Test cases for TaskManager class"""
    
    @pytest.fixture
    def task_manager(self):
        """Create a fresh TaskManager instance"""
        return TaskManager()
    
    @pytest.fixture
    def sample_task_data(self):
        """Provide sample task data"""
        return {
            "task_id": "TASK-001",
            "title": "Implement user authentication",
            "description": "Create login and registration system",
            "priority": "high",
            "status": "pending",
            "estimated_hours": 16,
            "assigned_to": "developer1",
            "due_date": "2024-02-15",
            "dependencies": [],
            "tags": ["backend", "security"]
        }
    
    def test_create_task_success(self, task_manager, sample_task_data):
        """Test successful task creation"""
        task = task_manager.create_task(sample_task_data)
        
        assert task.task_id == "TASK-001"
        assert task.title == "Implement user authentication"
        assert task.status == "pending"
        assert task.created_at is not None
    
    def test_create_task_missing_required_fields(self, task_manager):
        """Test task creation with missing required fields"""
        invalid_data = {"description": "Missing title"}
        
        with pytest.raises(ValueError, match="Title is required"):
            task_manager.create_task(invalid_data)
    
    def test_create_task_invalid_priority(self, task_manager):
        """Test task creation with invalid priority"""
        invalid_data = {
            "title": "Test Task",
            "priority": "invalid_priority"
        }
        
        with pytest.raises(ValueError, match="Invalid priority level"):
            task_manager.create_task(invalid_data)
    
    def test_update_task_status(self, task_manager, sample_task_data):
        """Test updating task status"""
        task = task_manager.create_task(sample_task_data)
        
        updated_task = task_manager.update_task(
            task.task_id, 
            {"status": "in_progress"}
        )
        
        assert updated_task.status == "in_progress"
        assert updated_task.updated_at is not None
    
    def test_update_nonexistent_task(self, task_manager):
        """Test updating a non-existent task"""
        with pytest.raises(ValueError, match="Task not found"):
            task_manager.update_task("NONEXISTENT", {"status": "completed"})
    
    def test_delete_task(self, task_manager, sample_task_data):
        """Test task deletion"""
        task = task_manager.create_task(sample_task_data)
        
        result = task_manager.delete_task(task.task_id)
        assert result is True
        
        with pytest.raises(ValueError, match="Task not found"):
            task_manager.get_task(task.task_id)
    
    def test_get_task_by_id(self, task_manager, sample_task_data):
        """Test retrieving task by ID"""
        created_task = task_manager.create_task(sample_task_data)
        retrieved_task = task_manager.get_task(created_task.task_id)
        
        assert retrieved_task.task_id == created_task.task_id
        assert retrieved_task.title == created_task.title
    
    def test_list_tasks_by_status(self, task_manager, sample_task_data):
        """Test listing tasks filtered by status"""
        task1 = task_manager.create_task(sample_task_data)
        
        task2_data = sample_task_data.copy()
        task2_data["task_id"] = "TASK-002"
        task2_data["status"] = "completed"
        task2 = task_manager.create_task(task2_data)
        
        pending_tasks = task_manager.list_tasks(status="pending")
        completed_tasks = task_manager.list_tasks(status="completed")
        
        assert len(pending_tasks) == 1
        assert pending_tasks[0].task_id == "TASK-001"
        assert len(completed_tasks) == 1
        assert completed_tasks[0].task_id == "TASK-002"
    
    def test_list_tasks_by_assignee(self, task_manager, sample_task_data):
        """Test listing tasks filtered by assignee"""
        task1 = task_manager.create_task(sample_task_data)
        
        task2_data = sample_task_data.copy()
        task2_data["task_id"] = "TASK-002"
        task2_data["assigned_to"] = "developer2"
        task2 = task_manager.create_task(task2_data)
        
        dev1_tasks = task_manager.list_tasks(assigned_to="developer1")
        dev2_tasks = task_manager.list_tasks(assigned_to="developer2")
        
        assert len(dev1_tasks) == 1
        assert dev1_tasks[0].task_id == "TASK-001"
        assert len(dev2_tasks) == 1
        assert dev2_tasks[0].task_id == "TASK-002"
    
    def test_calculate_task_progress(self, task_manager, sample_task_data):
        """Test task progress calculation"""
        task = task_manager.create_task(sample_task_data)
        
        # Simulate progress updates
        task_manager.update_task(task.task_id, {
            "actual_hours": 8,
            "status": "in_progress"
        })
        
        progress = task_manager.calculate_progress(task.task_id)
        assert progress == 0.5  # 8/16 hours
    
    def test_validate_task_dependencies(self, task_manager, sample_task_data):
        """Test task dependency validation"""
        # Create prerequisite task
        prereq_data = sample_task_data.copy()
        prereq_data["task_id"] = "TASK-PREQ"
        prereq_task = task_manager.create_task(prereq_data)
        
        # Create dependent task
        dependent_data = sample_task_data.copy()
        dependent_data["task_id"] = "TASK-DEP"
        dependent_data["dependencies"] = ["TASK-PREQ"]
        dependent_task = task_manager.create_task(dependent_data)
        
        # Validate dependencies
        is_valid = task_manager.validate_dependencies(dependent_task.task_id)
        assert is_valid is True
        
        # Test circular dependency detection
        with pytest.raises(ValueError, match="Circular dependency detected"):
            task_manager.update_task(prereq_task.task_id, {
                "dependencies": ["TASK-DEP"]
            })
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_tasks_to_file(self, mock_json_dump, mock_file, task_manager, sample_task_data):
        """Test saving tasks to JSON file"""
        task = task_manager.create_task(sample_task_data)
        
        task_manager.save_to_file("tasks.json")
        
        mock_file.assert_called_once_with("tasks.json", 'w')
        mock_json_dump.assert_called_once()
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"tasks": []}')
    @patch('json.load')
    def test_load_tasks_from_file(self, mock_json_load, mock_file, task_manager):
        """Test loading tasks from JSON file"""
        mock_json_load.return_value = {
            "tasks": [{
                "task_id": "TASK-001",
                "title": "Loaded Task",
                "status": "pending"
            }]
        }
        
        task_manager.load_from_file("tasks.json")
        
        mock_file.assert_called_once_with("tasks.json", 'r')
        assert len(task_manager.list_tasks()) == 1
    
    def test_search_tasks(self, task_manager, sample_task_data):
        """Test task search functionality"""
        task1 = task_manager.create_task(sample_task_data)
        
        task2_data = sample_task_data.copy()
        task2_data["task_id"] = "TASK-002"
        task2_data["title"] = "Fix authentication bug"
        task2 = task_manager.create_task(task2_data)
        
        # Search by title
        results = task_manager.search_tasks("authentication")
        assert len(results) == 2
        
        # Search by description
        results = task_manager.search_tasks("login system")
        assert len(results) == 1
        assert results[0].task_id == "TASK-001"
    
    def test_get_overdue_tasks(self, task_manager, sample_task_data):
        """Test retrieving overdue tasks"""
        overdue_data = sample_task_data.copy()
        overdue_data["task_id"] = "TASK-OVERDUE"
        overdue_data["due_date"] = "2024-01-01"  # Past date
        overdue_task = task_manager.create_task(overdue_data)
        
        overdue_tasks = task_manager.get_overdue_tasks()
        assert len(overdue_tasks) == 1
        assert overdue_tasks[0].task_id == "TASK-OVERDUE"
    
    def test_get_tasks_due_soon(self, task_manager, sample_task_data):
        """Test retrieving tasks due soon"""
        soon_data = sample_task_data.copy()
        soon_data["task_id"] = "TASK-SOON"
        soon_data["due_date"] = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        soon_task = task_manager.create_task(soon_data)
        
        due_soon_tasks = task_manager.get_tasks_due_soon(days=3)
        assert len(due_soon_tasks) == 1
        assert due_soon_tasks[0].task_id == "TASK-SOON"
