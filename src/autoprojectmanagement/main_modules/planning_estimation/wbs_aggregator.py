import os
import json

class WBSAggregator:
    def __init__(self, parts_dir='SystemInputs/user_inputs/wbs_parts', output_file='SystemInputs/user_inputs/detailed_wbs.json'):
        self.parts_dir = parts_dir
        self.output_file = output_file

    def load_part(self, filename):
        path = os.path.join(self.parts_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def validate_wbs_levels(self, task, current_level=0):
        """
        Validate that WBS structure doesn't exceed 3 levels.
        """
        if current_level > 3:
            raise ValueError(f"WBS structure exceeds maximum allowed levels (3). Task '{task.get('name', 'unknown')}' is at level {current_level}")
        
        if 'subtasks' in task:
            for subtask in task['subtasks']:
                self.validate_wbs_levels(subtask, current_level + 1)

    def assign_hierarchical_numbers(self, task, prefix=''):
        """
        Recursively assign hierarchical numbering to tasks.
        """
        # Assign number to current task if it's not the root
        if prefix != '':
            task['wbs_number'] = prefix
        
        if 'subtasks' not in task or not task['subtasks']:
            return

        for index, subtask in enumerate(task['subtasks'], start=1):
            number = f"{prefix}{index}" if prefix == '' else f"{prefix}.{index}"
            self.assign_hierarchical_numbers(subtask, number)

    def find_wbs_parts(self, directory):
        """Recursively find all WBS part JSON files in the directory."""
        wbs_parts = []
        for root_dir, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    wbs_parts.append(os.path.join(root_dir, file))
        return wbs_parts

    def aggregate(self):
        # Recursively find all WBS part files
        parts_files = self.find_wbs_parts(self.parts_dir)
        if not parts_files:
            print("No WBS parts found in directory.")
            return

        # Create root with level 0
        root = {
            "id": "WBS-ROOT",
            "name": "Software Project",
            "level": 0,
            "subtasks": []
        }

        for file_path in parts_files:
            # Get relative path for loading
            rel_path = os.path.relpath(file_path, self.parts_dir)
            part = self.load_part(rel_path)
            # Add the entire part as a subtask to preserve hierarchy
            root["subtasks"].append(part)

        # Validate WBS levels before proceeding
        self.validate_wbs_levels(root)
        
        # Assign hierarchical numbers starting from root subtasks
        self.assign_hierarchical_numbers(root, '')

        # Write aggregated WBS to output file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(root, f, indent=2, ensure_ascii=False)
        print(f"Aggregated WBS written to {self.output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='WBS Aggregator with Hierarchical Numbering')
    parser.add_argument('--parts_dir', default='SystemInputs/user_inputs/wbs_parts', 
                       help='Directory containing WBS parts (default: SystemInputs/user_inputs/wbs_parts)')
    parser.add_argument('--output_file', default='SystemInputs/user_inputs/detailed_wbs.json',
                       help='Output file for aggregated WBS (default: SystemInputs/user_inputs/detailed_wbs.json)')
    
    args = parser.parse_args()
    
    aggregator = WBSAggregator(parts_dir=args.parts_dir, output_file=args.output_file)
    aggregator.aggregate()
