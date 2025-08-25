import unittest
from autoprojectmanagement.main_modules.project_management.project_management_system import ProjectManagementSystem

class TestProjectManagementSystem(unittest.TestCase):
    def setUp(self):
        self.pms = ProjectManagementSystem()
        self.pms.initialize_system()

    def test_add_project(self):
        project_data = {"id": 1, "name": "Test Project"}
        result = self.pms.add_project(project_data)
        self.assertTrue(result)
        self.assertIn("1", self.pms.projects)

    def test_get_project(self):
        project_data = {"id": "2", "name": "Another Project"}
        self.pms.add_project(project_data)
        project = self.pms.get_project("2")
        self.assertIsNotNone(project)
        self.assertEqual(project["name"], "Another Project")

    def test_remove_project(self):
        project_data = {"id": "3", "name": "Project to Remove"}
        self.pms.add_project(project_data)
        result = self.pms.remove_project("3")
        self.assertTrue(result)
        self.assertNotIn("3", self.pms.projects)

    def test_update_project(self):
        project_data = {"id": "4", "name": "Project to Update"}
        self.pms.add_project(project_data)
        updated_data = {"id": "4", "name": "Updated Project"}
        result = self.pms.update_project(updated_data)
        self.assertTrue(result)
        project = self.pms.get_project("4")
        self.assertEqual(project["name"], "Updated Project")

    def test_add_task_to_project(self):
        project_data = {"id": "5", "name": "Project with Tasks"}
        self.pms.add_project(project_data)
        task_data = {"id": 101, "title": "New Task"}
        result = self.pms.add_task_to_project("5", task_data)
        self.assertTrue(result)

    def test_remove_task_from_project(self):
        project_data = {"id": "6", "name": "Project with Task Removal"}
        self.pms.add_project(project_data)
        task_data = {"id": 102, "title": "Task to Remove"}
        self.pms.add_task_to_project("6", task_data)
        result = self.pms.remove_task_from_project("6", 102)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
