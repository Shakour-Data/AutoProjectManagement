import unittest
from ..main_modules.task_management import TaskManagement

import unittest

class TestImportantTasks(unittest.TestCase):
    def setUp(self):
        self.tm = TaskManagement()
        self.task_titles = [
            "Develop Project Management Tool",
            "Develop Project Management Tool - Subtask Level 1.1",
            "Develop Project Management Tool - Subtask Level 1.3",
            "Develop Project Management Tool - Subtask Level 1.2",
            "Develop Project Management Tool - Subtask Level 2.1.2",
            "Develop Project Management Tool - Subtask Level 2.3.2",
            "Develop Project Management Tool - Subtask Level 2.1.1",
            "Develop Project Management Tool - Subtask Level 2.3.1",
            "Develop Project Management Tool - Subtask Level 2.2.1",
            "Develop Project Management Tool - Subtask Level 2.2.2",
            "Develop Project Management Tool - Subtask Level 3.1.1",
            "Develop Project Management Tool - Subtask Level 3.1.2",
            "Develop Project Management Tool - Subtask Level 3.2.1",
            "Develop Project Management Tool - Subtask Level 3.2.2",
            "Develop Project Management Tool - Subtask Level 3.3.1",
        ]
        self.tasks = []
        for title in self.task_titles:
            task = self.tm.parse_creative_input(title)
            self.tasks.append(task)
        for task in self.tasks:
            self.tm.mark_task_completed(task.id)

    def test_all_tasks_created(self):
        self.assertEqual(len(self.tm.tasks), 15)

    def test_all_tasks_completed(self):
        for task in self.tasks:
            self.assertEqual(task.status, 'completed')

    def test_mark_nonexistent_task_completed(self):
        result = self.tm.mark_task_completed(9999)  # Non-existent task id
        self.assertFalse(result)

    def test_task_titles_match(self):
        for i, task in enumerate(self.tasks):
            self.assertEqual(task.title, self.task_titles[i])

if __name__ == '__main__':
    unittest.main()
