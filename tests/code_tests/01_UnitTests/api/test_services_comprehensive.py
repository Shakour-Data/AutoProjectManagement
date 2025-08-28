"""
Comprehensive unit tests for autoprojectmanagement/api/services.py
Generated according to AutoProjectManagement testing standards
"""

import pytest
import json
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile
import os

from autoprojectmanagement.api.services import ProjectService

class TestProjectService:
    """Test class for ProjectService"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.service = ProjectService()
        
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = Path(self.temp_dir) / 'JSonDataBase'
        self.test_inputs_path = self.test_db_path / 'Inputs'
        self.test_inputs_path.mkdir(parents=True, exist_ok=True)
        
        # Patch the paths to use our test directory
        self.service.db_path = self.test_db_path
        self.service.inputs_path = self.test_inputs_path
        self.service.outputs_path = self.test_db_path / 'OutPuts'
    
    def teardown_method(self):
        """Cleanup after each test method"""
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir)

    # Functionality Tests (5 tests)
    def test_get_status_with_valid_project_and_tasks(self):
        """Test get_status with valid project ID and tasks"""
        # Create test task database
        task_data = [
            {"id": "1", "name": "Task 1", "status": "Done"},
            {"id": "2", "name": "Task 2", "status": "In Progress"},
            {"id": "3", "name": "Task 3", "status": "Done"}
        ]
        
        task_db_path = self.test_inputs_path / 'UserInputs'
        task_db_path.mkdir(parents=True, exist_ok=True)
        task_file = task_db_path / 'commit_task_database.json'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f)
        
        result = self.service.get_status("test-project")
        
        assert result is not None
        assert result["project_id"] == "test-project"
        assert result["total_tasks"] == 3
        assert result["completed_tasks"] == 2
        assert result["progress_percentage"] == 66.67
        assert "Project is in progress" in result["summary"]

    def test_get_status_with_all_completed_tasks(self):
        """Test get_status with all tasks completed"""
        task_data = [
            {"id": "1", "name": "Task 1", "status": "Done"},
            {"id": "2", "name": "Task 2", "status": "Done"}
        ]
        
        task_db_path = self.test_inputs_path / 'UserInputs'
        task_db_path.mkdir(parents=True, exist_ok=True)
        task_file = task_db_path / 'commit_task_database.json'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f)
        
        result = self.service.get_status("test-project")
        
        assert result["progress_percentage"] == 100.0
        assert "Project completed" in result["summary"]

    def test_get_status_with_no_tasks(self):
        """Test get_status with no tasks"""
        task_data = []
        
        task_db_path = self.test_inputs_path / 'UserInputs'
        task_db_path.mkdir(parents=True, exist_ok=True)
        task_file = task_db_path / 'commit_task_database.json'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f)
        
        result = self.service.get_status("test-project")
        
        assert result["total_tasks"] == 0
        assert result["completed_tasks"] == 0
        assert result["progress_percentage"] == 0.0
        assert "Project not started" in result["summary"]

    def test_get_status_with_dictionary_format(self):
        """Test get_status with dictionary format task database"""
        task_data = {
            "task1": {"id": "1", "name": "Task 1", "status": "Done"},
            "task2": {"id": "2", "name": "Task 2", "status": "In Progress"}
        }
        
        task_db_path = self.test_inputs_path / 'UserInputs'
        task_db_path.mkdir(parents=True, exist_ok=True)
        task_file = task_db_path / 'commit_task_database.json'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f)
        
        result = self.service.get_status("test-project")
        
        assert result["total_tasks"] == 2
        assert result["completed_tasks"] == 1
        assert result["progress_percentage"] == 50.0

    def test_get_project_list(self):
        """Test get_project_list method"""
        result = self.service.get_project_list()
        
        assert isinstance(result, dict)
        assert "projects" in result
        assert "count" in result
        assert "message" in result
        assert result["message"] == "Project listing not yet implemented"

    # Edge Case Tests (5 tests)
    def test_get_status_with_missing_task_database(self):
        """Test get_status when task database file doesn't exist"""
        result = self.service.get_status("test-project")
        
        assert result is None

    def test_get_status_with_invalid_json(self):
        """Test get_status with invalid JSON in task database"""
        task_db_path = self.test_inputs_path / 'UserInputs'
        task_db_path.mkdir(parents=True, exist_ok=True)
        task_file = task_db_path / 'commit_task_database.json'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            f.write("invalid json content")
        
        result = self.service.get_status("test-project")
        
        assert "error" in result
        assert "Invalid JSON" in result["error"]

    def test_get_status_with_unreadable_file(self):
        """Test get_status with unreadable task database file"""
        task_db_path = self.test_inputs_path / 'UserInputs'
        task_db_path.mkdir(parents=True, exist_ok=True)
        task_file = task_db_path / 'commit_task_database.json'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump([{"test": "data"}], f)
        
        # Make file unreadable
        os.chmod(task_file, 0o000)
        
        result = self.service.get_status("test-project")
        
        # Restore permissions for cleanup
        os.chmod(task_file, 0o644)
        
        assert "error" in result
        assert "Could not read" in result["error"]

    def test_get_status_with_invalid_data_format(self):
        """Test get_status with invalid data format (neither list nor dict)"""
        task_db_path = self.test_inputs_path / 'UserInputs'
        task_db_path.mkdir(parents=True, exist_ok=True)
        task_file = task_db_path / 'commit_task_database.json'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump("invalid format", f)
        
        result = self.service.get_status("test-project")
        
        assert "error" in result
        assert "Task database format error" in result["error"]

    def test_get_status_with_mixed_task_statuses(self):
        """Test get_status with various task status formats"""
        task_data = [
            {"id": "1", "name": "Task 1", "status": "Done"},
            {"id": "2", "name": "Task 2", "status": "done"},  # lowercase
            {"id": "3", "name": "Task 3", "status": "DONE"},  # uppercase
            {"id": "4", "name": "Task 4", "status": "In Progress"},
            {"id": "5", "name": "Task 5"}  # no status field
        ]
        
        task_db_path = self.test_inputs_path / 'UserInputs'
        task_db_path.mkdir(parents=True, exist_ok=True)
        task_file = task_db_path / 'commit_task_database.json'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f)
        
        result = self.service.get_status("test-project")
        
        assert result["total_tasks"] == 5
        assert result["completed_tasks"] == 3  # Only "Done", "done", "DONE" should count

    # Error Handling Tests (5 tests)
    def test_get_status_with_empty_project_id(self):
        """Test get_status with empty project ID"""
        result = self.service.get_status("")
        
        assert result is None

    def test_get_status_with_none_project_id(self):
        """Test get_status with None project ID"""
        result = self.service.get_status(None)
        
        assert result is None

    def test_get_status_with_special_characters_project_id(self):
        """Test get_status with special characters in project ID"""
        result = self.service.get_status("project@test#123")
        
        assert result is None  # Should return None since file doesn't exist

    def test_get_status_with_long_project_id(self):
        """Test get_status with very long project ID"""
        long_id = "a" * 1000
        result = self.service.get_status(long_id)
        
        assert result is None  # Should return None since file doesn't exist

    def test_get_status_with_numeric_project_id(self):
        """Test get_status with numeric project ID"""
        result = self.service.get_status("12345")
        
        assert result is None  # Should return None since file doesn't exist

    # Integration Tests (5 tests)
    def test_service_initialization_paths(self):
        """Test that service initializes with correct paths"""
        service = ProjectService()
        
        assert service.db_path is not None
        assert service.inputs_path is not None
        assert service.outputs_path is not None
        assert "JSonDataBase" in str(service.db_path)
        assert "Inputs" in str(service.inputs_path)
        assert "OutPuts" in str(service.outputs_path)

    def test_get_status_integration_with_real_file(self):
        """Test get_status integration with real file operations"""
        task_data = [
            {"id": "1", "name": "Integration Task 1", "status": "Done"},
            {"id": "2", "name": "Integration Task 2", "status": "In Progress"}
        ]
        
        task_db_path = self.test_inputs_path / 'UserInputs'
        task_db_path.mkdir(parents=True, exist_ok=True)
        task_file = task_db_path / 'commit_task_database.json'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f)
        
        result = self.service.get_status("integration-test")
        
        assert result is not None
        assert result["source_file"] == str(task_file)
        assert os.path.exists(result["source_file"])

    def test_error_response_format(self):
        """Test that error responses follow consistent format"""
        task_db_path = self.test_inputs_path / 'UserInputs'
        task_db_path.mkdir(parents=True, exist_ok=True)
        task_file = task_db_path / 'commit_task_database.json'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            f.write("invalid json")
        
        result = self.service.get_status("test-project")
        
        assert "error" in result
        assert isinstance(result["error"], str)
        assert "Invalid JSON" in result["error"]

    def test_progress_calculation_accuracy(self):
        """Test that progress calculation is mathematically accurate"""
        task_data = [
            {"id": "1", "name": "Task 1", "status": "Done"},
            {"id": "2", "name": "Task 2", "status": "Done"},
            {"id": "3", "name": "Task 3", "status": "In Progress"},
            {"id": "4", "name": "Task 4", "status": "Not Started"}
        ]
        
        task_db_path = self.test_inputs_path / 'UserInputs'
        task_db_path.mkdir(parents=True, exist_ok=True)
        task_file = task_db_path / 'commit_task_database.json'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f)
        
        result = self.service.get_status("test-project")
        
        expected_progress = (2 / 4) * 100  # 2 completed out of 4 total
        assert abs(result["progress_percentage"] - expected_progress) < 0.01

    def test_service_singleton_pattern(self):
        """Test that service follows singleton pattern in API usage"""
        from autoprojectmanagement.api.services import project_service
        
        # Both should be the same instance
        assert project_service is self.service
        assert isinstance(project_service, ProjectService)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
