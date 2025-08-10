"""
Test suite for DBDataCollector service
"""
import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock, mock_open

from autoprojectmanagement.main_modules.db_data_collector import DBDataCollector


class TestDBDataCollector:
    """Test cases for DBDataCollector class"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        import shutil
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def data_collector(self, temp_dir):
        """Create DBDataCollector instance with temp directory"""
        return DBDataCollector(data_dir=temp_dir)
    
    @pytest.fixture
    def mock_task(self):
        """Mock task object for testing"""
        class MockTask:
            def __init__(self, task_id, title, assigned_to=None):
                self.id = task_id
                self.title = title
                self.assigned_to = assigned_to or []
                self.workflow_progress_percentage = lambda: 75.0
        
        return MockTask
    
    def test_initialization(self, data_collector):
        """Test service initialization"""
        assert data_collector is not None
        assert hasattr(data_collector, 'collect_and_store_tasks')
        assert hasattr(data_collector, 'collect_resource_allocation')
        assert hasattr(data_collector, 'collect_progress_metrics')
    
    def test_collect_and_store_tasks(self, data_collector, mock_task, temp_dir):
        """Test collecting and storing task data"""
        tasks = [
            mock_task(1, "Task 1", ["user1", "user2"]),
            mock_task(2, "Task 2", ["user1"])
        ]
        
        data_collector.collect_and_store_tasks(tasks)
        
        tasks_file = os.path.join(temp_dir, 'tasks.json')
        assert os.path.exists(tasks_file)
        
        with open(tasks_file, 'r') as f:
            stored_data = json.load(f)
            assert len(stored_data) == 2
            assert stored_data[0]['id'] == 1
            assert stored_data[0]['title'] == "Task 1"
    
    def test_collect_resource_allocation(self, data_collector, mock_task, temp_dir):
        """Test collecting resource allocation data"""
        tasks = [
            mock_task(1, "Task 1", ["user1", "user2"]),
            mock_task(2, "Task 2", ["user1", "user3"]),
            mock_task(3, "Task 3", ["user2"])
        ]
        
        data_collector.collect_resource_allocation(tasks)
        
        resource_file = os.path.join(temp_dir, 'resource_allocation.json')
        assert os.path.exists(resource_file)
        
        with open(resource_file, 'r') as f:
            allocation_data = json.load(f)
            assert allocation_data['user1'] == 2
            assert allocation_data['user2'] == 2
            assert allocation_data['user3'] == 1
    
    def test_collect_progress_metrics(self, data_collector, mock_task, temp_dir):
        """Test collecting progress metrics"""
        tasks = [
            mock_task(1, "Task 1"),
            mock_task(2, "Task 2")
        ]
        
        data_collector.collect_progress_metrics(tasks)
        
        progress_file = os.path.join(temp_dir, 'progress_metrics.json')
        assert os.path.exists(progress_file)
        
        with open(progress_file, 'r') as f:
            progress_data = json.load(f)
            assert progress_data['1'] == 75.0
            assert progress_data['2'] == 75.0
    
    def test_insert_feature_weights(self, data_collector, temp_dir):
        """Test inserting feature weights"""
        urgency_weights = {"deadline": 0.8, "impact": 0.6}
        importance_weights = {"business_value": 0.9, "effort": 0.7}
        
        data_collector.insert_feature_weights(urgency_weights, importance_weights)
        
        weights_file = os.path.join(temp_dir, 'feature_weights.json')
        assert os.path.exists(weights_file)
        
        with open(weights_file, 'r') as f:
            weights_data = json.load(f)
            assert weights_data['urgency_weights'] == urgency_weights
            assert weights_data['importance_weights'] == importance_weights
    
    def test_empty_tasks_collection(self, data_collector, temp_dir):
        """Test handling empty task list"""
        data_collector.collect_and_store_tasks([])
        
        tasks_file = os.path.join(temp_dir, 'tasks.json')
        assert os.path.exists(tasks_file)
        
        with open(tasks_file, 'r') as f:
            stored_data = json.load(f)
            assert stored_data == []
    
    def test_close_method(self, data_collector):
        """Test close method exists and can be called"""
        data_collector.close()  # Should not raise any exception
