import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os

# Add the project root to the path so we can import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestDBDataCollector(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        self.test_data_dir = 'test_data_dir'
        self.test_tasks = [
            MagicMock(id=1, assigned_to=['Alice', 'Bob'], workflow_progress_percentage=MagicMock(return_value=50)),
            MagicMock(id=2, assigned_to=['Charlie'], workflow_progress_percentage=MagicMock(return_value=75))
        ]
        self.test_urgency_weights = {"deadline_proximity": 0.8, "next_activity_dependency": 0.6}
        self.test_importance_weights = {"dependency": 0.9, "critical_path": 0.7}

    # Test 1: Test initialization with default path
    def test_init_default_path(self):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        self.assertEqual(collector.data_dir, 'SystemInputs/user_inputs')
        self.assertEqual(collector.tasks_file, 'SystemInputs/user_inputs/tasks.json')
        self.assertEqual(collector.resource_allocation_file, 'SystemInputs/user_inputs/resource_allocation.json')
        self.assertEqual(collector.progress_metrics_file, 'SystemInputs/user_inputs/progress_metrics.json')
        self.assertEqual(collector.feature_weights_file, 'SystemInputs/user_inputs/feature_weights.json')

    # Test 2: Test initialization with custom path
    def test_init_custom_path(self):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector('custom_data_dir')
        self.assertEqual(collector.data_dir, 'custom_data_dir')
        self.assertEqual(collector.tasks_file, 'custom_data_dir/tasks.json')
        self.assertEqual(collector.resource_allocation_file, 'custom_data_dir/resource_allocation.json')
        self.assertEqual(collector.progress_metrics_file, 'custom_data_dir/progress_metrics.json')
        self.assertEqual(collector.feature_weights_file, 'custom_data_dir/feature_weights.json')

    # Test 3: Test collect_and_store_tasks with valid data
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_and_store_tasks_valid_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # Setup mock tasks
        mock_task1 = MagicMock()
        mock_task1.__dict__ = {"id": 1, "name": "Task 1"}
        mock_task2 = MagicMock()
        mock_task2.__dict__ = {"id": 2, "name": "Task 2"}
        tasks = [mock_task1, mock_task2]
        
        collector.collect_and_store_tasks(tasks)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.tasks_file, 'w', encoding='utf-8')
        
        # Verify json.dump was called with correct data
        handle = mock_open_file()
        handle.write.assert_called()

    # Test 4: Test collect_and_store_tasks with empty data
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_and_store_tasks_empty_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        collector.collect_and_store_tasks([])
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.tasks_file, 'w', encoding='utf-8')

    # Test 5: Test collect_and_store_tasks with permission error
    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    def test_collect_and_store_tasks_permission_error(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # Setup mock tasks
        mock_task = MagicMock()
        mock_task.__dict__ = {"id": 1, "name": "Task 1"}
        tasks = [mock_task]
        
        # This should raise a PermissionError
        with self.assertRaises(PermissionError):
            collector.collect_and_store_tasks(tasks)

    # Test 6: Test collect_resource_allocation with valid data
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_resource_allocation_valid_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # Setup mock tasks with assigned users
        mock_task1 = MagicMock()
        mock_task1.assigned_to = ['Alice', 'Bob']
        mock_task2 = MagicMock()
        mock_task2.assigned_to = ['Bob', 'Charlie']
        tasks = [mock_task1, mock_task2]
        
        collector.collect_resource_allocation(tasks)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.resource_allocation_file, 'w', encoding='utf-8')
        
        # Verify json.dump was called
        handle = mock_open_file()
        handle.write.assert_called()

    # Test 7: Test collect_resource_allocation with empty data
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_resource_allocation_empty_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        collector.collect_resource_allocation([])
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.resource_allocation_file, 'w', encoding='utf-8')

    # Test 8: Test collect_progress_metrics with valid data
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_progress_metrics_valid_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # Setup mock tasks with progress methods
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.workflow_progress_percentage.return_value = 50
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.workflow_progress_percentage.return_value = 75
        tasks = [mock_task1, mock_task2]
        
        collector.collect_progress_metrics(tasks)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.progress_metrics_file, 'w', encoding='utf-8')
        
        # Verify methods were called
        mock_task1.workflow_progress_percentage.assert_called_once()
        mock_task2.workflow_progress_percentage.assert_called_once()

    # Test 9: Test collect_progress_metrics with empty data
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_progress_metrics_empty_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        collector.collect_progress_metrics([])
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.progress_metrics_file, 'w', encoding='utf-8')

    # Test 10: Test insert_feature_weights with valid data
    @patch('builtins.open', new_callable=mock_open)
    def test_insert_feature_weights_valid_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        urgency_weights = {"deadline_proximity": 0.8, "next_activity_dependency": 0.6}
        importance_weights = {"dependency": 0.9, "critical_path": 0.7}
        
        collector.insert_feature_weights(urgency_weights, importance_weights)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.feature_weights_file, 'w', encoding='utf-8')

    # Test 11: Test insert_feature_weights with empty data
    @patch('builtins.open', new_callable=mock_open)
    def test_insert_feature_weights_empty_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        collector.insert_feature_weights({}, {})
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.feature_weights_file, 'w', encoding='utf-8')

    # Test 12: Test insert_feature_weights with unicode data
    @patch('builtins.open', new_callable=mock_open)
    def test_insert_feature_weights_unicode_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        urgency_weights = {"الموعد_النهائي": 0.8, "الأولوية": 0.6}
        importance_weights = {"الأهمية": 0.9, "المسار_الحرج": 0.7}
        
        collector.insert_feature_weights(urgency_weights, importance_weights)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.feature_weights_file, 'w', encoding='utf-8')

    # Test 13: Test collect_and_store_tasks with special characters
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_and_store_tasks_special_characters(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # Setup mock tasks with special characters
        mock_task = MagicMock()
        mock_task.__dict__ = {"id": 1, "name": "Task!@#", "description": "Description with $%^&*()"}
        tasks = [mock_task]
        
        collector.collect_and_store_tasks(tasks)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.tasks_file, 'w', encoding='utf-8')

    # Test 14: Test collect_resource_allocation with duplicate users
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_resource_allocation_duplicate_users(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # Setup mock tasks with duplicate users
        mock_task1 = MagicMock()
        mock_task1.assigned_to = ['Alice', 'Bob']
        mock_task2 = MagicMock()
        mock_task2.assigned_to = ['Alice', 'Charlie']
        tasks = [mock_task1, mock_task2]
        
        collector.collect_resource_allocation(tasks)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.resource_allocation_file, 'w', encoding='utf-8')

    # Test 15: Test collect_progress_metrics with zero progress
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_progress_metrics_zero_progress(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # Setup mock tasks with zero progress
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.workflow_progress_percentage.return_value = 0
        tasks = [mock_task]
        
        collector.collect_progress_metrics(tasks)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.progress_metrics_file, 'w', encoding='utf-8')

    # Test 16: Test collect_progress_metrics with 100% progress
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_progress_metrics_100_percent_progress(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # Setup mock tasks with 100% progress
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.workflow_progress_percentage.return_value = 100
        tasks = [mock_task]
        
        collector.collect_progress_metrics(tasks)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.progress_metrics_file, 'w', encoding='utf-8')

    # Test 17: Test collect_and_store_tasks with large data
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_and_store_tasks_large_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # Setup large number of mock tasks
        tasks = []
        for i in range(1000):
            mock_task = MagicMock()
            mock_task.__dict__ = {"id": i, "name": f"Task {i}"}
            tasks.append(mock_task)
        
        collector.collect_and_store_tasks(tasks)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.tasks_file, 'w', encoding='utf-8')

    # Test 18: Test collect_resource_allocation with large data
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_resource_allocation_large_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # Setup large number of mock tasks with many users
        tasks = []
        for i in range(100):
            mock_task = MagicMock()
            mock_task.assigned_to = [f"User{j}" for j in range(10)]
            tasks.append(mock_task)
        
        collector.collect_resource_allocation(tasks)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.resource_allocation_file, 'w', encoding='utf-8')

    # Test 19: Test collect_progress_metrics with large data
    @patch('builtins.open', new_callable=mock_open)
    def test_collect_progress_metrics_large_data(self, mock_open_file):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # Setup large number of mock tasks
        tasks = []
        for i in range(1000):
            mock_task = MagicMock()
            mock_task.id = i
            mock_task.workflow_progress_percentage.return_value = i % 100
            tasks.append(mock_task)
        
        collector.collect_progress_metrics(tasks)
        
        # Verify file was opened for writing
        mock_open_file.assert_called_once_with(collector.progress_metrics_file, 'w', encoding='utf-8')

    # Test 20: Test close method
    def test_close_method(self):
        from project_management.modules.main_modules.db_data_collector import DBDataCollector
        collector = DBDataCollector()
        
        # The close method should not raise any exceptions
        try:
            collector.close()
        except Exception as e:
            self.fail(f"close() method raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
