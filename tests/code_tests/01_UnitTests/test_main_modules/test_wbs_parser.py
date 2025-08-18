"""
Unit tests for WBS Parser module
"""

import unittest
import json
import os
import tempfile
from project_management.modules.main_modules.wbs_parser import WBSParser


class TestWBSParser(unittest.TestCase):
    """Test cases for WBSParser class"""
    
    def setUp(self):
        """Set up test environment"""
        self.parser = WBSParser()
    
    def test_init(self):
        """Test WBSParser initialization"""
        self.assertIsNotNone(self.parser)
    
    def test_parse_json_wbs_valid_structure(self):
        """Test parsing valid JSON WBS structure"""
        test_data = {
            "id": 1,
            "name": "Test Project",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "level": 1,
                    "subtasks": []
                }
            ]
        }
        
        parsed = self.parser.parse_json_wbs(test_data)
        self.assertEqual(parsed["id"], 1)
        self.assertEqual(parsed["name"], "Test Project")
        self.assertEqual(len(parsed["subtasks"]), 1)
    
    def test_parse_json_wbs_missing_required_fields(self):
        """Test parsing JSON WBS with missing required fields"""
        test_data = {"id": 1, "name": "Test"}  # Missing 'level'
        
        with self.assertRaises(ValueError):
            self.parser.parse_json_wbs(test_data)
    
    def test_parse_json_wbs_invalid_type(self):
        """Test parsing non-dictionary JSON data"""
        with self.assertRaises(ValueError):
            self.parser.parse_json_wbs("invalid")
    
    def test_parse_text_wbs_simple_structure(self):
        """Test parsing simple text WBS structure"""
        text = """Project
    Task 1
        Subtask 1.1
    Task 2"""
        
        parsed = self.parser.parse_text_wbs(text)
        self.assertEqual(parsed["name"], "Project")
        self.assertEqual(len(parsed["subtasks"]), 2)
        self.assertEqual(parsed["subtasks"][0]["name"], "Task 1")
        self.assertEqual(len(parsed["subtasks"][0]["subtasks"]), 1)
    
    def test_parse_text_wbs_empty_text(self):
        """Test parsing empty text"""
        parsed = self.parser.parse_text_wbs("")
        self.assertEqual(parsed["name"], "Project")
        self.assertEqual(parsed["subtasks"], [])
    
    def test_parse_text_wbs_single_line(self):
        """Test parsing single line text"""
        parsed = self.parser.parse_text_wbs("Single Task")
        self.assertEqual(parsed["name"], "Single Task")
        self.assertEqual(parsed["subtasks"], [])
    
    def test_extract_task_details_complete_task(self):
        """Test extracting details from complete task"""
        task = {
            "id": 1,
            "name": "Test Task",
            "description": "Test description",
            "deadline": "2025-12-31",
            "assigned_to": ["user1", "user2"],
            "dependencies": [2, 3],
            "status": "in_progress",
            "priority": 5,
            "subtasks": [{"id": 2, "name": "Subtask", "subtasks": []}]
        }
        
        details = self.parser.extract_task_details(task)
        self.assertEqual(details["id"], 1)
        self.assertEqual(details["name"], "Test Task")
        self.assertEqual(details["description"], "Test description")
        self.assertEqual(details["deadline"], "2025-12-31")
        self.assertEqual(details["assigned_to"], ["user1", "user2"])
        self.assertEqual(details["dependencies"], [2, 3])
        self.assertEqual(details["status"], "in_progress")
        self.assertEqual(details["priority"], 5)
        self.assertEqual(details["subtasks_count"], 1)
    
    def test_extract_task_details_minimal_task(self):
        """Test extracting details from minimal task"""
        task = {"id": 1, "name": "Minimal Task"}
        
        details = self.parser.extract_task_details(task)
        self.assertEqual(details["id"], 1)
        self.assertEqual(details["name"], "Minimal Task")
        self.assertEqual(details["description"], "")
        self.assertEqual(details["assigned_to"], [])
        self.assertEqual(details["dependencies"], [])
        self.assertEqual(details["status"], "pending")
        self.assertEqual(details["priority"], 1)
        self.assertEqual(details["subtasks_count"], 0)
    
    def test_validate_wbs_integrity_valid_structure(self):
        """Test validating valid WBS structure"""
        wbs = {
            "id": 1,
            "name": "Test Project",
            "level": 0,
            "subtasks": [
                {"id": 2, "name": "Task 1", "level": 1, "subtasks": []}
            ]
        }
        
        is_valid = self.parser.validate_wbs_integrity(wbs)
        self.assertTrue(is_valid)
    
    def test_validate_wbs_integrity_invalid_structure(self):
        """Test validating invalid WBS structure"""
        wbs = {"id": 1, "name": "Test"}  # Missing required fields
        
        is_valid = self.parser.validate_wbs_integrity(wbs)
        self.assertFalse(is_valid)
    
    def test_get_task_hierarchy_flat_list(self):
        """Test getting flat list of all tasks in hierarchy"""
        wbs = {
            "id": 1,
            "name": "Root",
            "level": 0,
            "subtasks": [
                {
                    "id": 2,
                    "name": "Task 1",
                    "level": 1,
                    "subtasks": [
                        {"id": 3, "name": "Subtask 1.1", "level": 2, "subtasks": []}
                    ]
                },
                {"id": 4, "name": "Task 2", "level": 1, "subtasks": []}
            ]
        }
        
        hierarchy = self.parser.get_task_hierarchy(wbs)
        self.assertEqual(len(hierarchy), 4)
        self.assertEqual(hierarchy[0]["name"], "Root")
        self.assertEqual(hierarchy[1]["name"], "Task 1")
        self.assertEqual(hierarchy[2]["name"], "Subtask 1.1")
        self.assertEqual(hierarchy[3]["name"], "Task 2")
    
    def test_get_task_hierarchy_empty_wbs(self):
        """Test getting hierarchy from empty WBS"""
        wbs = {"id": 1, "name": "Empty", "level": 0, "subtasks": []}
        
        hierarchy = self.parser.get_task_hierarchy(wbs)
        self.assertEqual(len(hierarchy), 1)
        self.assertEqual(hierarchy[0]["name"], "Empty")
    
    def test_parse_text_wbs_complex_structure(self):
        """Test parsing complex text WBS structure"""
        text = """Project
    Phase 1
        Task 1.1
            Subtask 1.1.1
        Task 1.2
    Phase 2
        Task 2.1
            Subtask 2.1.1
            Subtask 2.1.2"""
        
        parsed = self.parser.parse_text_wbs(text)
        self.assertEqual(parsed["name"], "Project")
        self.assertEqual(len(parsed["subtasks"]), 2)
        self.assertEqual(parsed["subtasks"][0]["name"], "Phase 1")
        self.assertEqual(len(parsed["subtasks"][0]["subtasks"]), 2)
        self.assertEqual(len(parsed["subtasks"][0]["subtasks"][0]["subtasks"]), 1)
    
    def test_parse_text_wbs_unicode_characters(self):
        """Test parsing text WBS with Unicode characters"""
        text = """پروژه
    وظیفه ۱
        زیروظیفه ۱.۱"""
        
        parsed = self.parser.parse_text_wbs(text)
        self.assertEqual(parsed["name"], "پروژه")
        self.assertEqual(len(parsed["subtasks"]), 1)
        self.assertEqual(parsed["subtasks"][0]["name"], "وظیفه ۱")
    
    def test_parse_text_wbs_special_characters(self):
        """Test parsing text WBS with special characters"""
        text = """Project!
    Task @#$%
        Sub-task &*()"""
        
        parsed = self.parser.parse_text_wbs(text)
        self.assertEqual(parsed["name"], "Project!")
        self.assertEqual(parsed["subtasks"][0]["name"], "Task @#$%")
        self.assertEqual(parsed["subtasks"][0]["subtasks"][0]["name"], "Sub-task &*()")


if __name__ == '__main__':
    unittest.main()
