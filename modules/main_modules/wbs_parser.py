"""
WBS Parser Module - Parses different WBS formats into structured data
"""

import json
import re
from typing import Dict, List, Any, Optional


class WBSParser:
    """
    Parses different WBS (Work Breakdown Structure) formats into structured data
    """
    
    def __init__(self):
        """Initialize WBS Parser"""
        pass
    
    def parse_json_wbs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse JSON format WBS
        
        Args:
            data: JSON data containing WBS structure
            
        Returns:
            Parsed WBS structure
        """
        return self._validate_wbs_structure(data)
    
    def parse_text_wbs(self, text: str) -> Dict[str, Any]:
        """
        Parse text format WBS
        
        Args:
            text: Text containing WBS structure
            
        Returns:
            Parsed WBS structure
        """
        lines = text.strip().split('\n')
        return self._parse_text_lines(lines)
    
    def _validate_wbs_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize WBS structure
        
        Args:
            data: WBS data to validate
            
        Returns:
            Validated WBS structure
        """
        if not isinstance(data, dict):
            raise ValueError("WBS data must be a dictionary")
        
        required_fields = ['id', 'name', 'level']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Ensure subtasks is a list
        if 'subtasks' not in data:
            data['subtasks'] = []
        
        # Recursively validate subtasks
        for subtask in data['subtasks']:
            self._validate_wbs_structure(subtask)
        
        return data
    
    def _parse_text_lines(self, lines: List[str]) -> Dict[str, Any]:
        """
        Parse text lines into WBS structure
        
        Args:
            lines: List of text lines
            
        Returns:
            Parsed WBS structure
        """
        if not lines:
            return {"id": 1, "name": "Project", "level": 0, "subtasks": []}
        
        root = {"id": 1, "name": "Project", "level": 0, "subtasks": []}
        stack = [root]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Determine level based on indentation
            level = len(line) - len(line.lstrip())
            name = line.strip()
            
            # Create task
            task = {
                "id": len(stack) + 1,
                "name": name,
                "level": level // 2,  # Assuming 2 spaces per level
                "subtasks": []
            }
            
            # Find parent
            while stack and stack[-1]["level"] >= task["level"]:
                stack.pop()
            
            if stack:
                stack[-1]["subtasks"].append(task)
            else:
                root["subtasks"].append(task)
            
            stack.append(task)
        
        return root
    
    def extract_task_details(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract detailed information from a task
        
        Args:
            task: Task dictionary
            
        Returns:
            Detailed task information
        """
        return {
            "id": task.get("id"),
            "name": task.get("name", ""),
            "level": task.get("level", 0),
            "description": task.get("description", ""),
            "deadline": task.get("deadline"),
            "assigned_to": task.get("assigned_to", []),
            "dependencies": task.get("dependencies", []),
            "status": task.get("status", "pending"),
            "priority": task.get("priority", 1),
            "subtasks_count": len(task.get("subtasks", []))
        }
    
    def validate_wbs_integrity(self, wbs: Dict[str, Any]) -> bool:
        """
        Validate WBS structure integrity
        
        Args:
            wbs: WBS structure to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self._validate_wbs_structure(wbs)
            return True
        except ValueError:
            return False
    
    def get_task_hierarchy(self, wbs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get flat list of all tasks in hierarchy
        
        Args:
            wbs: WBS structure
            
        Returns:
            Flat list of all tasks
        """
        tasks = []
        
        def collect_tasks(task: Dict[str, Any], level: int = 0):
            task_info = self.extract_task_details(task)
            task_info['level'] = level
            tasks.append(task_info)
            
            for subtask in task.get('subtasks', []):
                collect_tasks(subtask, level + 1)
        
        collect_tasks(wbs)
        return tasks
