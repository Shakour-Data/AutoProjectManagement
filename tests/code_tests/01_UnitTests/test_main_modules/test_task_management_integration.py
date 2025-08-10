import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestTaskManagementIntegration(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        pass

    # Test 1: Test main function execution with normal flow
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_normal_flow(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with MagicMock
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "Task 1"
        mock_task1.github_issue_number = 101
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Task 2"
        mock_task2.github_issue_number = 102
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1, mock_task2]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1, mock_task2]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1, mock_task2]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1, mock_task2])
        
        # Verify that print was called for each task
        self.assertEqual(mock_print.call_count, 2)
        mock_print.assert_any_call("Task ID: 1, Title: Task 1, GitHub Issue #: 101")
        mock_print.assert_any_call("Task ID: 2, Title: Task 2, GitHub Issue #: 102")

    # Test 2: Test main function with empty task lists
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_empty_task_lists(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = []
        mock_tm_instance.prioritize_tasks.return_value = []
        mock_gh_instance.sync_tasks_to_github.return_value = []
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([])
        
        # Verify that print was not called
        mock_print.assert_not_called()

    # Test 3: Test main function with exception in generate_wbs_from_idea
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_exception_in_generate_wbs(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance to raise exception
        mock_tm_instance = mock_task_management.return_value
        mock_tm_instance.generate_wbs_from_idea.side_effect = Exception("Failed to generate WBS")
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            main()
        
        self.assertIn("Failed to generate WBS", str(context.exception))

    # Test 4: Test main function with exception in calculate_urgency_importance
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_exception_in_calculate_urgency_importance(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance to raise exception
        mock_tm_instance = mock_task_management.return_value
        mock_tm_instance.calculate_urgency_importance.side_effect = Exception("Failed to calculate urgency and importance")
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            main()
        
        self.assertIn("Failed to calculate urgency and importance", str(context.exception))

    # Test 5: Test main function with exception in prioritize_tasks
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_exception_in_prioritize_tasks(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance to raise exception
        mock_tm_instance = mock_task_management.return_value
        mock_tm_instance.prioritize_tasks.side_effect = Exception("Failed to prioritize tasks")
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            main()
        
        self.assertIn("Failed to prioritize tasks", str(context.exception))

    # Test 6: Test main function with exception in sync_tasks_to_github
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_exception_in_sync_tasks_to_github(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance to raise exception
        mock_gh_instance = mock_github_integration.return_value
        mock_gh_instance.sync_tasks_to_github.side_effect = Exception("Failed to sync tasks to GitHub")
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = []
        mock_tm_instance.prioritize_tasks.return_value = []
        
        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            main()
        
        self.assertIn("Failed to sync tasks to GitHub", str(context.exception))

    # Test 7: Test main function with unicode task titles
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_unicode_task_titles(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with unicode titles
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "مهمة 1"  # "Task 1" in Arabic
        mock_task1.github_issue_number = 101
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Задача 2"  # "Task 2" in Russian
        mock_task2.github_issue_number = 102
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1, mock_task2]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1, mock_task2]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1, mock_task2]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1, mock_task2])
        
        # Verify that print was called with unicode titles
        mock_print.assert_any_call("Task ID: 1, Title: مهمة 1, GitHub Issue #: 101")
        mock_print.assert_any_call("Task ID: 2, Title: Задача 2, GitHub Issue #: 102")

    # Test 8: Test main function with special characters in task titles
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_special_characters_in_task_titles(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with special characters
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "Task!@#$%^&*()"
        mock_task1.github_issue_number = 101
        
        mock_task2 = MagicMock()
        mock_task2.id = 2
        mock_task2.title = "Task\nwith\nnewlines"
        mock_task2.github_issue_number = 102
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1, mock_task2]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1, mock_task2]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1, mock_task2]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1, mock_task2])
        
        # Verify that print was called with special characters
        mock_print.assert_any_call("Task ID: 1, Title: Task!@#$%^&*(), GitHub Issue #: 101")
        mock_print.assert_any_call("Task ID: 2, Title: Task\nwith\nnewlines, GitHub Issue #: 102")

    # Test 9: Test main function with large number of tasks
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_large_number_of_tasks(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup 100 mock tasks
        tasks = []
        for i in range(100):
            mock_task = MagicMock()
            mock_task.id = i + 1
            mock_task.title = f"Task {i + 1}"
            mock_task.github_issue_number = 1000 + i + 1
            tasks.append(mock_task)
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = tasks
        mock_tm_instance.prioritize_tasks.return_value = tasks
        mock_gh_instance.sync_tasks_to_github.return_value = tasks
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with(tasks)
        
        # Verify that print was called for each task
        self.assertEqual(mock_print.call_count, 100)

    # Test 10: Test main function with None task attributes
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_none_task_attributes(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with None attributes
        mock_task1 = MagicMock()
        mock_task1.id = None
        mock_task1.title = None
        mock_task1.github_issue_number = None
        
        mock_task2 = MagicMock()
        mock_task2.id = None
        mock_task2.title = None
        mock_task2.github_issue_number = None
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1, mock_task2]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1, mock_task2]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1, mock_task2]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1, mock_task2])
        
        # Verify that print was called with None values
        mock_print.assert_any_call("Task ID: None, Title: None, GitHub Issue #: None")
        mock_print.assert_any_call("Task ID: None, Title: None, GitHub Issue #: None")

    # Test 11: Test main function with zero task IDs and issue numbers
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_zero_task_ids_and_issue_numbers(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with zero IDs and issue numbers
        mock_task1 = MagicMock()
        mock_task1.id = 0
        mock_task1.title = "Task 0"
        mock_task1.github_issue_number = 0
        
        mock_task2 = MagicMock()
        mock_task2.id = 0
        mock_task2.title = "Task 0"
        mock_task2.github_issue_number = 0
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1, mock_task2]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1, mock_task2]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1, mock_task2]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1, mock_task2])
        
        # Verify that print was called with zero values
        mock_print.assert_any_call("Task ID: 0, Title: Task 0, GitHub Issue #: 0")
        mock_print.assert_any_call("Task ID: 0, Title: Task 0, GitHub Issue #: 0")

    # Test 12: Test main function with negative task IDs and issue numbers
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_negative_task_ids_and_issue_numbers(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with negative IDs and issue numbers
        mock_task1 = MagicMock()
        mock_task1.id = -1
        mock_task1.title = "Task -1"
        mock_task1.github_issue_number = -101
        
        mock_task2 = MagicMock()
        mock_task2.id = -2
        mock_task2.title = "Task -2"
        mock_task2.github_issue_number = -102
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1, mock_task2]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1, mock_task2]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1, mock_task2]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1, mock_task2])
        
        # Verify that print was called with negative values
        mock_print.assert_any_call("Task ID: -1, Title: Task -1, GitHub Issue #: -101")
        mock_print.assert_any_call("Task ID: -2, Title: Task -2, GitHub Issue #: -102")

    # Test 13: Test main function with very high task IDs and issue numbers
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_very_high_task_ids_and_issue_numbers(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with very high IDs and issue numbers
        mock_task1 = MagicMock()
        mock_task1.id = 1000000
        mock_task1.title = "Task 1000000"
        mock_task1.github_issue_number = 9999999
        
        mock_task2 = MagicMock()
        mock_task2.id = 2000000
        mock_task2.title = "Task 2000000"
        mock_task2.github_issue_number = 8888888
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1, mock_task2]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1, mock_task2]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1, mock_task2]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1, mock_task2])
        
        # Verify that print was called with very high values
        mock_print.assert_any_call("Task ID: 1000000, Title: Task 1000000, GitHub Issue #: 9999999")
        mock_print.assert_any_call("Task ID: 2000000, Title: Task 2000000, GitHub Issue #: 8888888")

    # Test 14: Test main function with callable task attributes
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_callable_task_attributes(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with callable attributes
        def get_id():
            return 1
            
        def get_title():
            return "Task 1"
            
        def get_github_issue_number():
            return 101
        
        mock_task1 = MagicMock()
        mock_task1.id = get_id
        mock_task1.title = get_title
        mock_task1.github_issue_number = get_github_issue_number
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1])

    # Test 15: Test main function with task attributes as properties
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_task_attributes_as_properties(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with properties
        class MockTask:
            def __init__(self, id, title, github_issue_number):
                self._id = id
                self._title = title
                self._github_issue_number = github_issue_number
                
            @property
            def id(self):
                return self._id
                
            @property
            def title(self):
                return self._title
                
            @property
            def github_issue_number(self):
                return self._github_issue_number
        
        mock_task1 = MockTask(1, "Task 1", 101)
        mock_task2 = MockTask(2, "Task 2", 102)
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1, mock_task2]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1, mock_task2]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1, mock_task2]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1, mock_task2])
        
        # Verify that print was called with property values
        mock_print.assert_any_call("Task ID: 1, Title: Task 1, GitHub Issue #: 101")
        mock_print.assert_any_call("Task ID: 2, Title: Task 2, GitHub Issue #: 102")

    # Test 16: Test main function with task attributes as descriptors
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_task_attributes_as_descriptors(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with descriptors
        class Descriptor:
            def __init__(self, value):
                self.value = value
                
            def __get__(self, obj, objtype=None):
                return self.value
                
            def __set__(self, obj, value):
                self.value = value
        
        class MockTask:
            def __init__(self, id, title, github_issue_number):
                self.id = Descriptor(id)
                self.title = Descriptor(title)
                self.github_issue_number = Descriptor(github_issue_number)
        
        mock_task1 = MockTask(1, "Task 1", 101)
        mock_task2 = MockTask(2, "Task 2", 102)
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1, mock_task2]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1, mock_task2]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1, mock_task2]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1, mock_task2])

    # Test 17: Test main function with task attributes as magic methods
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_task_attributes_as_magic_methods(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with magic methods
        class MockTask:
            def __init__(self, id, title, github_issue_number):
                self._id = id
                self._title = title
                self._github_issue_number = github_issue_number
                
            def __str__(self):
                return f"Task {self._id}"
                
            def __repr__(self):
                return f"MockTask(id={self._id}, title={self._title})"
                
            def __getattr__(self, name):
                if name == "id":
                    return self._id
                elif name == "title":
                    return self._title
                elif name == "github_issue_number":
                    return self._github_issue_number
                else:
                    raise AttributeError(f"'MockTask' object has no attribute '{name}'")
        
        mock_task1 = MockTask(1, "Task 1", 101)
        mock_task2 = MockTask(2, "Task 2", 102)
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1, mock_task2]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1, mock_task2]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1, mock_task2]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1, mock_task2])

    # Test 18: Test main function with mixed task attribute types
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_mixed_task_attribute_types(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks with mixed attribute types
        mock_task1 = MagicMock()
        mock_task1.id = 1  # Integer
        mock_task1.title = "مهمة 1"  # Unicode string
        mock_task1.github_issue_number = 101  # Integer
        
        # Setup a task with properties
        class MockTask:
            def __init__(self, id, title, github_issue_number):
                self._id = id
                self._title = title
                self._github_issue_number = github_issue_number
                
            @property
            def id(self):
                return self._id
                
            @property
            def title(self):
                return self._title
                
            @property
            def github_issue_number(self):
                return self._github_issue_number
        
        mock_task2 = MockTask(2, "Task\nwith\nnewlines", 102)
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1, mock_task2]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1, mock_task2]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1, mock_task2]
        
        main()
        
        # Verify that methods were called
        mock_tm_instance.generate_wbs_from_idea.assert_called_once_with("Develop Project Management Tool")
        mock_tm_instance.calculate_urgency_importance.assert_called_once()
        mock_tm_instance.prioritize_tasks.assert_called_once()
        mock_gh_instance.sync_tasks_to_github.assert_called_once_with([mock_task1, mock_task2])

    # Test 19: Test main function with custom GitHub repository
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_custom_github_repository(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup mock tasks
        mock_task1 = MagicMock()
        mock_task1.id = 1
        mock_task1.title = "Task 1"
        mock_task1.github_issue_number = 101
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = [mock_task1]
        mock_tm_instance.prioritize_tasks.return_value = [mock_task1]
        mock_gh_instance.sync_tasks_to_github.return_value = [mock_task1]
        
        main()
        
        # Verify that GitHubIntegration was initialized with correct parameters
        mock_github_integration.assert_called_once_with(token=None, repo='user/repo')

    # Test 20: Test main function with multiple print calls verification
    @patch('project_management.modules.main_modules.task_management_integration.TaskManagement')
    @patch('project_management.modules.main_modules.task_management_integration.GitHubIntegration')
    @patch('builtins.print')
    def test_main_execution_multiple_print_calls_verification(self, mock_print, mock_github_integration, mock_task_management):
        from project_management.modules.main_modules.task_management_integration import main
        
        # Setup mock TaskManagement instance
        mock_tm_instance = mock_task_management.return_value
        
        # Setup mock GitHubIntegration instance
        mock_gh_instance = mock_github_integration.return_value
        
        # Setup 5 mock tasks
        tasks = []
        for i in range(5):
            mock_task = MagicMock()
            mock_task.id = i + 1
            mock_task.title = f"Task {i + 1}"
            mock_task.github_issue_number = 100 + i + 1
            tasks.append(mock_task)
        
        # Setup return values for methods
        mock_tm_instance.generate_wbs_from_idea.return_value = tasks
        mock_tm_instance.prioritize_tasks.return_value = tasks
        mock_gh_instance.sync_tasks_to_github.return_value = tasks
        
        main()
        
        # Verify that print was called exactly 5 times
        self.assertEqual(mock_print.call_count, 5)
        
        # Verify that each print call had the correct format
        for i in range(5):
            mock_print.assert_any_call(f"Task ID: {i + 1}, Title: Task {i + 1}, GitHub Issue #: {100 + i + 1}")

if __name__ == "__main__":
    unittest.main()
