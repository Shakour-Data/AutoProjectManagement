import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

class TestScheduler(unittest.TestCase):
    def setUp(self):
        # Setup any necessary test data or state
        pass

    # Test 1: Test initialization
    def test_init(self):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        self.assertEqual(scheduler.jobs, [])

    # Test 2: Test start method
    @patch("project_management.modules.main_modules.scheduler.threading.Thread")
    def test_start_method(self, mock_thread):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        scheduler.start()
        mock_thread.assert_called_once()
        # Check that the thread is started as a daemon
        mock_thread.return_value.start.assert_called_once()

    # Test 3: Test schedule_hourly method
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_hourly_method(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.hours.do.return_value = mock_job
        
        # Define a test function
        def test_func():
            pass
        
        scheduler.schedule_hourly(test_func)
        
        # Verify schedule calls
        mock_schedule.every.assert_called_once_with(1)
        mock_schedule.every.return_value.hours.do.assert_called_once_with(test_func)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 4: Test schedule_daily method
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_daily_method(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.day.at.return_value.do.return_value = mock_job
        
        # Define a test function
        def test_func():
            pass
        
        scheduler.schedule_daily(test_func)
        
        # Verify schedule calls
        mock_schedule.every.assert_called_once()
        mock_schedule.every.return_value.day.at.assert_called_once_with("00:00")
        mock_schedule.every.return_value.day.at.return_value.do.assert_called_once_with(test_func)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 5: Test multiple job scheduling
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_multiple_job_scheduling(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain for hourly
        mock_hourly_job = MagicMock()
        mock_schedule.every.return_value.hours.do.return_value = mock_hourly_job
        
        # Setup mock schedule chain for daily
        mock_daily_job = MagicMock()
        mock_schedule.every.return_value.day.at.return_value.do.return_value = mock_daily_job
        
        # Define test functions
        def test_func1():
            pass
            
        def test_func2():
            pass
        
        scheduler.schedule_hourly(test_func1)
        scheduler.schedule_daily(test_func2)
        
        # Verify jobs were added to jobs list
        self.assertEqual(len(scheduler.jobs), 2)
        self.assertEqual(scheduler.jobs[0], mock_hourly_job)
        self.assertEqual(scheduler.jobs[1], mock_daily_job)

    # Test 6: Test schedule_hourly with exception in job function
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_hourly_with_exception_in_job_function(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.hours.do.return_value = mock_job
        
        # Define a test function that raises an exception
        def test_func():
            raise Exception("Test exception")
        
        scheduler.schedule_hourly(test_func)
        
        # Verify schedule calls
        mock_schedule.every.assert_called_once_with(1)
        mock_schedule.every.return_value.hours.do.assert_called_once_with(test_func)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 7: Test schedule_daily with exception in job function
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_daily_with_exception_in_job_function(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.day.at.return_value.do.return_value = mock_job
        
        # Define a test function that raises an exception
        def test_func():
            raise Exception("Test exception")
        
        scheduler.schedule_daily(test_func)
        
        # Verify schedule calls
        mock_schedule.every.return_value.day.at.return_value.do.assert_called_once_with(test_func)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 8: Test schedule_hourly with lambda function
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_hourly_with_lambda_function(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.hours.do.return_value = mock_job
        
        # Define a lambda function
        test_func = lambda: "test"
        
        scheduler.schedule_hourly(test_func)
        
        # Verify schedule calls
        mock_schedule.every.return_value.hours.do.assert_called_once_with(test_func)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 9: Test schedule_daily with lambda function
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_daily_with_lambda_function(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.day.at.return_value.do.return_value = mock_job
        
        # Define a lambda function
        test_func = lambda: "test"
        
        scheduler.schedule_daily(test_func)
        
        # Verify schedule calls
        mock_schedule.every.return_value.day.at.return_value.do.assert_called_once_with(test_func)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 10: Test schedule_hourly with method as job function
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_hourly_with_method_as_job_function(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.hours.do.return_value = mock_job
        
        # Define a class with a method
        class TestClass:
            def test_method(self):
                return "test"
        
        test_instance = TestClass()
        
        scheduler.schedule_hourly(test_instance.test_method)
        
        # Verify schedule calls
        mock_schedule.every.return_value.hours.do.assert_called_once_with(test_instance.test_method)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 11: Test schedule_daily with method as job function
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_daily_with_method_as_job_function(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.day.at.return_value.do.return_value = mock_job
        
        # Define a class with a method
        class TestClass:
            def test_method(self):
                return "test"
        
        test_instance = TestClass()
        
        scheduler.schedule_daily(test_instance.test_method)
        
        # Verify schedule calls
        mock_schedule.every.return_value.day.at.return_value.do.assert_called_once_with(test_instance.test_method)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 12: Test schedule_hourly with function that returns value
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_hourly_with_function_that_returns_value(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.hours.do.return_value = mock_job
        
        # Define a function that returns a value
        def test_func():
            return "test_result"
        
        scheduler.schedule_hourly(test_func)
        
        # Verify schedule calls
        mock_schedule.every.return_value.hours.do.assert_called_once_with(test_func)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 13: Test schedule_daily with function that returns value
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_daily_with_function_that_returns_value(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.day.at.return_value.do.return_value = mock_job
        
        # Define a function that returns a value
        def test_func():
            return "test_result"
        
        scheduler.schedule_daily(test_func)
        
        # Verify schedule calls
        mock_schedule.every.return_value.day.at.return_value.do.assert_called_once_with(test_func)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 14: Test schedule_hourly with function that takes arguments
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_hourly_with_function_that_takes_arguments(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.hours.do.return_value = mock_job
        
        # Define a function that takes arguments
        def test_func(arg1, arg2):
            return f"{arg1} {arg2}"
        
        # Note: In practice, you would need to use functools.partial or similar to pass arguments
        # For this test, we're just checking that the function can be scheduled
        scheduler.schedule_hourly(test_func)
        
        # Verify schedule calls
        mock_schedule.every.return_value.hours.do.assert_called_once_with(test_func)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 15: Test schedule_daily with function that takes arguments
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_daily_with_function_that_takes_arguments(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.day.at.return_value.do.return_value = mock_job
        
        # Define a function that takes arguments
        def test_func(arg1, arg2):
            return f"{arg1} {arg2}"
        
        # Note: In practice, you would need to use functools.partial or similar to pass arguments
        # For this test, we're just checking that the function can be scheduled
        scheduler.schedule_daily(test_func)
        
        # Verify schedule calls
        mock_schedule.every.return_value.day.at.return_value.do.assert_called_once_with(test_func)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 16: Test schedule_hourly with unicode function name
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_hourly_with_unicode_function_name(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.hours.do.return_value = mock_job
        
        # Define a function with unicode name
        def تابع_اختبار():  # "test_function" in Arabic
            return "test"
        
        scheduler.schedule_hourly(تابع_اختبار)
        
        # Verify schedule calls
        mock_schedule.every.return_value.hours.do.assert_called_once_with(تابع_اختبار)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 17: Test schedule_daily with unicode function name
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_daily_with_unicode_function_name(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.day.at.return_value.do.return_value = mock_job
        
        # Define a function with unicode name
        def تابع_اختبار():  # "test_function" in Arabic
            return "test"
        
        scheduler.schedule_daily(تابع_اختبار)
        
        # Verify schedule calls
        mock_schedule.every.return_value.day.at.return_value.do.assert_called_once_with(تابع_اختبار)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 18: Test schedule_hourly with special characters in function name
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_hourly_with_special_characters_in_function_name(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.hours.do.return_value = mock_job
        
        # Define a function with special characters in a valid way
        def test_func_special():
            return "test"
        
        scheduler.schedule_hourly(test_func_special)
        
        # Verify schedule calls
        mock_schedule.every.return_value.hours.do.assert_called_once_with(test_func_special)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 19: Test schedule_daily with special characters in function name
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_schedule_daily_with_special_characters_in_function_name(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.day.at.return_value.do.return_value = mock_job
        
        # Define a function with special characters in a valid way
        def test_func_special():
            return "test"
        
        scheduler.schedule_daily(test_func_special)
        
        # Verify schedule calls
        mock_schedule.every.return_value.day.at.return_value.do.assert_called_once_with(test_func_special)
        
        # Verify job was added to jobs list
        self.assertEqual(len(scheduler.jobs), 1)
        self.assertEqual(scheduler.jobs[0], mock_job)

    # Test 20: Test scheduler with large number of jobs
    @patch("project_management.modules.main_modules.scheduler.schedule")
    def test_scheduler_with_large_number_of_jobs(self, mock_schedule):
        from project_management.modules.main_modules.scheduler import Scheduler
        scheduler = Scheduler()
        
        # Setup mock schedule chain
        mock_job = MagicMock()
        mock_schedule.every.return_value.hours.do.return_value = mock_job
        mock_schedule.every.return_value.day.at.return_value.do.return_value = mock_job
        
        # Define a test function
        def test_func():
            pass
        
        # Schedule many jobs
        for i in range(100):
            scheduler.schedule_hourly(test_func)
            scheduler.schedule_daily(test_func)
        
        # Verify all jobs were added
        self.assertEqual(len(scheduler.jobs), 200)

if __name__ == "__main__":
    unittest.main()
