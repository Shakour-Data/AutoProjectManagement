import json
import os

class JSONDataLinker:
    def __init__(self, input_dir="project_inputs/PM_JSON/user_inputs", intermediate_dir="project_management/PM_SystemOutputs/intermediate", output_dir="project_management/PM_SystemOutputs/system_outputs"):
        self.input_dir = input_dir
        self.intermediate_dir = intermediate_dir
        self.output_dir = output_dir
        os.makedirs(self.intermediate_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def load_json(self, filename):
        path = os.path.join(self.input_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json(self, data, filename, intermediate=True):
        dir_path = self.intermediate_dir if intermediate else self.output_dir
        path = os.path.join(dir_path, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def link_wbs_and_resources(self):
        """
        Link detailed WBS tasks with resource allocations to create an intermediate JSON file
        that includes task dependencies, durations, resource assignments, and planned dates.
        """
        wbs = self.load_json("detailed_wbs.json")
        allocations = self.load_json("task_resource_allocation.json")

        # Create a mapping from task_id to resource allocations
        allocation_map = {}
        for alloc in allocations:
            task_id = alloc["task_id"]
            if task_id not in allocation_map:
                allocation_map[task_id] = []
            allocation_map[task_id].append({
                "resource_id": alloc["resource_id"],
                "allocation_percent": alloc["allocation_percent"],
                "role_in_task": alloc["role_in_task"],
                "start_date": alloc["start_date"],
                "end_date": alloc["end_date"],
                "notes": alloc.get("notes", "")
            })

        def enrich_task(task):
            task_id = task.get("id")
            task["allocations"] = allocation_map.get(task_id, [])
            # Recursively enrich subtasks
            if "subtasks" in task and task["subtasks"]:
                task["subtasks"] = [enrich_task(sub) for sub in task["subtasks"]]
            return task

        enriched_wbs = [enrich_task(task) for task in wbs]

        self.save_json(enriched_wbs, "linked_wbs_resources.json", intermediate=True)
        return enriched_wbs

    def generate_all_links(self):
        """
        Generate all intermediate JSON files linking inputs for use in calculations and outputs.
        """
        self.link_wbs_and_resources()
        # Additional linking functions can be added here for other JSON files

if __name__ == "__main__":
    linker = JSONDataLinker()
    linker.generate_all_links()
    print("Intermediate JSON linking completed.")
