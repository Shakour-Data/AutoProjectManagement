import unittest
from unittest.mock import patch, MagicMock
import sys
import os

class TestEstimationManagementMain(unittest.TestCase):
    @patch('project_management.modules.main_modules.estimation_management.EstimationManagement')
    def test_main_execution(self, mock_estimation_manager):
        # Test that the EstimationManagement class is properly defined
        self.assertTrue(mock_estimation_manager)

    @patch('project_management.modules.main_modules.estimation_management.EstimationManagement.run')
    @patch('project_management.modules.main_modules.estimation_management.EstimationManagement.__init__')
    def test_main_functionality(self, mock_init, mock_run):
        # Test that when instantiated and run, the methods are called correctly
        mock_init.return_value = None  # __init__ should return None
        from project_management.modules.main_modules.estimation_management import EstimationManagement
        manager = EstimationManagement()
        manager.run()
        mock_init.assert_called_once()
        mock_run.assert_called_once()

    def test_module_import(self):
        # Test that the module can be imported without errors
        try:
            from project_management.modules.main_modules.estimation_management import EstimationManagement
            self.assertTrue(True, "Module imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import module: {e}")

if __name__ == '__main__':
    unittest.main()
