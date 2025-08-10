"""
Unit tests for WBS Merger module
"""

import unittest
import json
import os
import tempfile
from project_management.modules.main_modules.wbs_merger import WBSMerger


class TestWBSMerger(unittest.TestCase):
    """Test cases for WBSMerger class"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.parts_dir = os.path.join(self.temp_dir, 'wbs_parts')
        self.output_file = os.path.join(self.temp_dir, 'merged_wbs.json')
        os.makedirs(self.parts_dir, exist_ok=True)
        
        self.merger = WBSMerger(
            parts_dir=self.parts_dir,
            output_file=self.output_file
        )
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test WBSMerger initialization"""
        self.assertEqual(self.merger.parts_dir, self.parts_dir)
        self.assertEqual(self.merger.output_file, self.output_file)
    
    def test_load_part_valid_json(self):
        """Test loading valid JSON WBS part"""
        test_data = {
            "id": 1,
            "name": "Test Part",
            "level": 0,
            "subtasks": []
        }
        
        test_file = os.path.join(self.parts_dir, 'test_part.json')
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        loaded = self.merger.load_part('test_part.json')
        self.assertEqual(loaded, test_data)
    
    def test_load_part_file_not_found(self):
        """Test loading non-existent file"""
        with self.assertRaises(FileNotFoundError):
            self.merger.load_part('nonexistent.json')
    
    def test_load_part_invalid_json(self):
        """Test loading invalid JSON file"""
        test_file = os.path.join(self.parts_dir, 'invalid.json')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('invalid json content')
        
        with self.assertRaises(ValueError):
            self.merger.load_part('invalid.json')
    
    def test_merge_subtasks_empty_lists(self):
        """Test merging empty subtask lists"""
        merged = self.merger.merge_subtasks([], [])
        self.assertEqual(merged, [])
    
    def test_merge_subtasks_no_overlap(self):
        """Test merging subtasks with no overlapping IDs"""
        base = [{"id": 1, "name": "Task 1", "subtasks": []}]
        additional = [{"id": 2, "name": "Task 2", "subtasks": []}]
        
        merged = self.merger.merge_subtasks(base, additional)
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0]["id"], 1)
        self.assertEqual(merged[1]["id"], 2)
    
    def test_merge_subtasks_with_overlap(self):
        """Test merging subtasks with overlapping IDs"""
        base = [{"id": 1, "name": "Base Task", "subtasks": []}]
        additional = [{"id": 1, "name": "Updated Task", "subtasks": []}]
        
        merged = self.merger.merge_subtasks(base, additional)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["name"], "Updated Task")
    
    def test_merge_subtasks_nested(self):
        """Test merging nested subtasks"""
        base = [{
            "id": 1,
            "name": "Base Task",
            "subtasks": [{"id": 2, "name": "Base Subtask", "subtasks": []}]
        }]
        additional = [{
            "id": 1,
            "name": "Base Task",
            "subtasks": [{"id": 3, "name": "Additional Subtask", "subtasks": []}]
        }]
        
        merged = self.merger.merge_subtasks(base, additional)
        self.assertEqual(len(merged[0]["subtasks"]), 2)
    
    def test_merge_all_parts_empty_directory(self):
        """Test merging with empty directory"""
        merged = self.merger.merge_all_parts()
        self.assertEqual(merged["name"], "Project")
        self.assertEqual(merged["subtasks"], [])
    
    def test_merge_all_parts_single_part(self):
        """Test merging single WBS part"""
        part_data = {
            "id": 1,
            "name": "Single Part",
            "level": 0,
            "subtasks": [
                {"id": 2, "name": "Subtask 1", "subtasks": []},
                {"id": 3, "name": "Subtask 2", "subtasks": []}
            ]
        }
        
        test_file = os.path.join(self.parts_dir, 'single_part.json')
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(part_data, f)
        
        merged = self.merger.merge_all_parts()
        self.assertEqual(len(merged["subtasks"]), 2)
        self.assertEqual(merged["subtasks"][0]["name"], "Subtask 1")
    
    def test_merge_all_parts_multiple_parts(self):
        """Test merging multiple WBS parts"""
        part1 = {
            "id": 1,
            "name": "Part 1",
            "subtasks": [{"id": 2, "name": "Task from Part 1", "subtasks": []}]
        }
        
        part2 = {
            "id": 1,
            "name": "Part 2",
            "subtasks": [{"id": 3, "name": "Task from Part 2", "subtasks": []}]
        }
        
        with open(os.path.join(self.parts_dir, 'part1.json'), 'w', encoding='utf-8') as f:
            json.dump(part1, f)
        
        with open(os.path.join(self.parts_dir, 'part2.json'), 'w', encoding='utf-8') as f:
            json.dump(part2, f)
        
        merged = self.merger.merge_all_parts()
        self.assertEqual(len(merged["subtasks"]), 2)
    
    def test_merge_all_parts_output_file_created(self):
        """Test that output file is created after merging"""
        part_data = {
            "id": 1,
            "name": "Test Part",
            "subtasks": []
        }
        
        test_file = os.path.join(self.parts_dir, 'test.json')
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(part_data, f)
        
        self.merger.merge_all_parts()
        self.assertTrue(os.path.exists(self.output_file))
        
        # Verify content
        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            self.assertEqual(content["name"], "Project")
    
    def test_merge_all_parts_directory_not_found(self):
        """Test merging with non-existent directory"""
        merger = WBSMerger(parts_dir="/nonexistent/path")
        with self.assertRaises(FileNotFoundError):
            merger.merge_all_parts()
    
    def test_merge_all_parts_invalid_json(self):
        """Test handling invalid JSON files"""
        test_file = os.path.join(self.parts_dir, 'invalid.json')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('invalid json content')
        
        # Should handle gracefully and continue
        merged = self.merger.merge_all_parts()
        self.assertEqual(merged["name"], "Project")
        self.assertEqual(merged["subtasks"], [])


if __name__ == '__main__':
    unittest.main()
