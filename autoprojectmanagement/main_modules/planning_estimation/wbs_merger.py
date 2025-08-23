"""
WBS Merger Module - Merges multiple WBS parts into a single detailed WBS
"""

import os
import json
from typing import List, Dict, Any


class WBSMerger:
    """
    Merges multiple WBS (Work Breakdown Structure) parts into a single detailed WBS.
    Handles merging of tasks, subtasks, and their relationships.
    """
    
    def __init__(self, parts_dir: str = 'SystemInputs/user_inputs/wbs_parts', 
                 output_file: str = 'SystemInputs/system_generated/detailed_wbs.json'):
        """
        Initialize WBS Merger with directory paths
        
        Args:
            parts_dir: Directory containing WBS parts
            output_file: Output file for merged WBS
        """
        self.parts_dir = parts_dir
        self.output_file = output_file
        
    def load_part(self, filename: str) -> Dict[str, Any]:
        """
        Load a single WBS part from JSON file
        
        Args:
            filename: Path to the WBS part file
            
        Returns:
            Dictionary containing the WBS part data
        """
        filepath = os.path.join(self.parts_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"WBS part file not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {filepath}: {e}")
    
    def merge_subtasks(self, base_subtasks: List[Dict], additional_subtasks: List[Dict]) -> List[Dict]:
        """
        Merge subtasks from additional subtasks into base subtasks
        
        Args:
            base_subtasks: Base subtasks to merge into
            additional_subtasks: Additional subtasks to merge
            
        Returns:
            Merged list of subtasks
        """
        merged = base_subtasks.copy()
        
        # Create a lookup dictionary for existing tasks
        task_lookup = {task['id']: task for task in merged}
        
        for additional_task in additional_subtasks:
            task_id = additional_task['id']
            
            if task_id in task_lookup:
                # Update existing task
                existing_task = task_lookup[task_id]
                existing_task.update(additional_task)
                
                # Merge subtasks recursively
                if 'subtasks' in additional_task:
                    existing_subtasks = existing_task.get('subtasks', [])
                    additional_subtasks_list = additional_task.get('subtasks', [])
                    existing_task['subtasks'] = self.merge_subtasks(existing_subtasks, additional_subtasks_list)
            else:
                # Add new task
                merged.append(additional_task)
        
        return merged
    
    def merge_all_parts(self) -> Dict[str, Any]:
        """
        Merge all WBS parts into a single detailed WBS
        
        Returns:
            Dictionary containing the merged WBS
        """
        merged_wbs = {
            "id": 1,
            "name": "Project",
            "level": 0,
            "subtasks": []
        }
        
        # Get all WBS part files
        if not os.path.exists(self.parts_dir):
            raise FileNotFoundError(f"WBS parts directory not found: {self.parts_dir}")
        
        wbs_files = [f for f in os.listdir(self.parts_dir) if f.endswith('.json')]
        
        if not wbs_files:
            print("No WBS parts found in directory.")
            return merged_wbs
        
        # Load and merge all parts
        for filename in wbs_files:
            try:
                part = self.load_part(filename)
                if 'subtasks' in part:
                    merged_wbs['subtasks'] = self.merge_subtasks(
                        merged_wbs['subtasks'], 
                        part.get('subtasks', [])
                    )
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
        
        # Save merged WBS
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_wbs, f, indent=2, ensure_ascii=False)
        
        print(f"Merged detailed WBS saved to {self.output_file}")
        return merged_wbs
