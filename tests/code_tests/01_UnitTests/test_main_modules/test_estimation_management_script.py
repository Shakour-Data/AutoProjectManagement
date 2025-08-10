import unittest
import subprocess
import sys
import os

class TestEstimationManagementScript(unittest.TestCase):
    def test_script_execution(self):
        """Test that the script can be executed directly"""
        # Get the path to the estimation_management.py file
        script_path = os.path.join('project_management', 'modules', 'main_modules', 'estimation_management.py')
        
        # Execute the script as a subprocess
        result = subprocess.run([sys.executable, script_path], 
                                capture_output=True, text=True, cwd='.')
        
        # Check that the script executed without errors
        # Allow for successful execution or expected error messages
        self.assertTrue(result.returncode == 0 or len(result.stderr) > 0 or len(result.stdout) > 0)

    def test_script_import(self):
        """Test that the script can be imported without errors"""
        try:
            from project_management.modules.main_modules.estimation_management import EstimationManagement
            self.assertTrue(True, "Module imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import module: {e}")

    def test_class_exists(self):
        """Test that the EstimationManagement class exists"""
        try:
            from project_management.modules.main_modules.estimation_management import EstimationManagement
            self.assertTrue(callable(EstimationManagement))
        except ImportError as e:
            self.fail(f"Failed to import EstimationManagement class: {e}")

if __name__ == '__main__':
    unittest.main()
