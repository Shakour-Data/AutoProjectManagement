import unittest
import os
import json
from autoprojectmanagement.main_modules.project_management_system import ProjectManagementSystem

class TestProjectManagementSystem(unittest.TestCase):

    def setUp(self):
        """Set up the test case"""
        self.pms = ProjectManagementSystem()
        self.pms.initialize_system()

    def tearDown(self):
        """Clean up after the test case"""
        if os.path.exists("projects.json"):
            os.remove("projects.json")
        if os.path.exists("tasks.json"):
            os.remove("tasks.json")

    def test_add_project_and_task(self):
        """Test adding a project and a task"""
        project = {"id": 1, "name": "Test Project"}
        self.assertTrue(self.pms.add_project(project))

        task = {"id": 1, "title": "Test Task"}
        self.assertTrue(self.pms.add_task_to_project(1, task))

        # Verify that the project and task are saved
        self.pms.load_projects()
        self.pms.load_tasks()

        self.assertEqual(len(self.pms.projects), 1)
        # JSON keys are loaded as strings, so we need to convert them
        project_id_str = str(1)
        task_id_str = str(1)
        self.assertEqual(len(self.pms.tasks[project_id_str]), 1)

        self.assertEqual(self.pms.projects[project_id_str]['name'], "Test Project")
        self.assertEqual(self.pms.tasks[project_id_str][task_id_str]['title'], "Test Task")

if __name__ == "__main__":
    unittest.main()
