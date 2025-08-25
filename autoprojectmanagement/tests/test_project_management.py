import unittest
from autoprojectmanagement.main_modules.project_management.project_management_system import ProjectManagementSystem

class TestProjectManagementSystem(unittest.TestCase):
    def setUp(self):
        self.pms = ProjectManagementSystem()
        self.pms.initialize_system()

    def test_add_project(self):
