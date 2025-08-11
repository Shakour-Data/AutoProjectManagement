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

    def aggregate(self):
        # Load level 0 from any part (all have same root)
        parts_files = [f for f in os.listdir(self.parts_dir) if f.endswith('.json')]
        if not parts_files:
            print("No WBS parts found in directory.")
            return

        root = None
        subtasks = []

        for file in parts_files:
            part = self.load_part(file)
            if root is None:
                root = {
                    "id": part["id"],
                    "name": part["name"],
                    "level": part["level"],
                    "subtasks": []
                }
            # Append the main branch (level 1) from this part to root subtasks
            if "subtasks" in part and part["subtasks"]:
                root["subtasks"].extend(part["subtasks"])

        # Write aggregated WBS to output file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(root, f, indent=2, ensure_ascii=False)
        print(f"Aggregated WBS written to {self.output_file}")

if __name__ == "__main__":
    aggregator = WBSAggregator()
    aggregator.aggregate()
