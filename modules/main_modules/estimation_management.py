import json
import os

class BaseManagement:
    def __init__(self, input_paths: dict, output_path: str):
        """
        input_paths: dict of input name to file path
        output_path: output file path
        """
        self.input_paths = input_paths
        self.output_path = output_path
        self.inputs = {}
        self.output = {}

    def load_json(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_json(self, data, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_inputs(self):
        for key, path in self.input_paths.items():
            self.inputs[key] = self.load_json(path) or {}

    def analyze(self):
        """
        To be implemented by subclasses.
        """
        raise NotImplementedError

    def run(self):
        self.load_inputs()
        self.analyze()
        self.save_json(self.output, self.output_path)
        print(f"{self.__class__.__name__} output saved to {self.output_path}")


def estimate_task_duration(task):
    if task is None:
        raise TypeError("Task cannot be None")
    if not isinstance(task, dict):
        raise TypeError("Task must be a dictionary")
    complexity = task.get("complexity", "medium")
    # Simple mapping for complexity to duration
    mapping = {
        "low": 1,
        "medium": 3,
        "high": 5,
        "extreme": 8
    }
    duration = mapping.get(complexity, 3)
    return duration

def estimate_task_cost(task):
    if task is None:
        raise TypeError("Task cannot be None")
    if not isinstance(task, dict):
        raise TypeError("Task must be a dictionary")
    resources = task.get("resources", 1)
    if not isinstance(resources, (int, float)):
        raise TypeError("Resources must be a number")
    duration = estimate_task_duration(task)
    cost_per_resource_per_unit = 100  # arbitrary cost factor
    cost = duration * resources * cost_per_resource_per_unit
    return cost

def estimate_project_duration(project):
    if project is None:
        raise TypeError("Project cannot be None")
    if not isinstance(project, dict):
        raise TypeError("Project must be a dictionary")
    tasks = project.get("tasks", [])
    if not tasks:
        return 0
    total_duration = 0
    for task in tasks:
        total_duration += estimate_task_duration(task)
    return total_duration

def estimate_project_cost(project):
    if project is None:
        raise TypeError("Project cannot be None")
    if not isinstance(project, dict):
        raise TypeError("Project must be a dictionary")
    tasks = project.get("tasks", [])
    if not tasks:
        return 0
    total_cost = 0
    for task in tasks:
        total_cost += estimate_task_cost(task)
    return total_cost

class EstimationManagement(BaseManagement):
    def __init__(self,
                 detailed_wbs_path='project_inputs/PM_JSON/user_inputs/detailed_wbs.json',
                 output_path='project_inputs/PM_JSON/system_outputs/estimation_management.json'):
        input_paths = {
            'detailed_wbs': detailed_wbs_path
        }
        super().__init__(input_paths, output_path)

    def analyze(self):
        """
        Perform project estimation using parametric, COCOMO II, and Agile methods.
        This is a placeholder for actual estimation logic.
        """
        self.output = {
            'summary': 'Estimation methods not yet implemented',
            'details': {}
        }

if __name__ == "__main__":
    manager = EstimationManagement()
    manager.run()
