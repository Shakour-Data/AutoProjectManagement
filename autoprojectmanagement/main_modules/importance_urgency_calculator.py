import json
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ImportanceUrgencyCalculator:
    def __init__(self, wbs_data):
        """
        wbs_data: list of dicts representing tasks with hierarchical structure
        Each task dict should have:
            - id: unique identifier
            - title: task title
            - level: hierarchical level (int)
            - subtasks: list of subtasks (same structure)
            - other metadata as needed
        """
        self.wbs_data = wbs_data
        self.task_scores = {}

    def score_task(self, task):
        """
        Recursively score a task based on its subtasks or base criteria.
        Importance and urgency are scored 0-100.
        For leaf tasks, score based on defined criteria.
        For parent tasks, average scores of subtasks.
        """
        if not task.get('subtasks'):
            importance = self.calculate_importance(task)
            urgency = self.calculate_urgency(task)
        else:
            importance_values = []
            urgency_values = []
            for subtask in task['subtasks']:
                sub_imp, sub_urg = self.score_task(subtask)
                importance_values.append(sub_imp)
                urgency_values.append(sub_urg)
            importance = sum(importance_values) / len(importance_values) if importance_values else 0
            urgency = sum(urgency_values) / len(urgency_values) if urgency_values else 0

        self.task_scores[task['id']] = {'importance': importance, 'urgency': urgency}
        return importance, urgency

    def calculate_importance(self, task):
        """
        Calculate importance based on:
        - Dependency count (normalized)
        - Critical path involvement (boolean)
        - Cost impact (normalized)
        - Stakeholder priority (normalized)
        Weights can be adjusted as needed.
        """
        if task is None:
            raise TypeError("Task cannot be None")
        try:
            dependencies = task.get('dependencies', [])
            if not isinstance(dependencies, list):
                raise TypeError("dependencies must be a list")
            dependency_factor = min(1, len(dependencies) / 10)

            critical_path = task.get('critical_path', False)
            critical_path_factor = 1 if critical_path else 0

            cost_impact = task.get('cost_impact', 0)
            if isinstance(cost_impact, bool):
                raise TypeError("cost_impact must not be a boolean")
            if not (isinstance(cost_impact, int) or isinstance(cost_impact, float)):
                raise TypeError("cost_impact must be a number")
            cost_factor = min(1, cost_impact / 100000)  # assuming cost in currency units

            priority = task.get('priority', 0)
            if priority is None:
                raise TypeError("priority must not be None")
            if isinstance(priority, bool):
                raise TypeError("priority must not be a boolean")
            if isinstance(priority, str):
                priority_map = {
                    "low": 1,
                    "medium": 5,
                    "high": 10,
                    "بالا": 10,
                    "اهم": 10,
                }
                priority_factor = priority_map.get(priority.lower(), 0) / 10
            elif isinstance(priority, (int, float)) and not isinstance(priority, bool):
                if priority < 0 or priority > 10:
                    raise TypeError("priority numeric value out of range")
                priority_factor = min(1, priority / 10)
            else:
                raise TypeError("priority must be a number or recognized string")

            w_dep, w_cp, w_cost, w_prio = 0.3, 0.3, 0.2, 0.2

            importance = (w_dep * dependency_factor +
                          w_cp * critical_path_factor +
                          w_cost * cost_factor +
                          w_prio * priority_factor)
            importance_score = round(importance * 100, 2)
            return importance_score
        except Exception as e:
            task_id = task.get('id') if task and isinstance(task, dict) else 'unknown'
            logger.error(f"Error calculating importance for task {task_id}: {e}")
            raise

    def calculate_urgency(self, task):
        """
        Calculate urgency based on:
        - Deadline proximity (normalized)
        - Risk of delay (normalized)
        - Stakeholder pressure (normalized)
        Weights can be adjusted as needed.
        """
        if task is None:
            raise TypeError("Task cannot be None")
        try:
            import datetime
            now = datetime.datetime.now()
            deadline_str = task.get('deadline', None)
            if deadline_str is None:
                # Treat missing or None deadline as no deadline, urgency time factor 0
                time_factor = 0
            elif deadline_str:
                if not isinstance(deadline_str, str):
                    if isinstance(deadline_str, bool):
                        raise TypeError("deadline must be a string in ISO format")
                    if isinstance(deadline_str, float) or isinstance(deadline_str, int):
                        raise TypeError("deadline must be a string in ISO format")
                    try:
                        deadline_str = str(deadline_str)
                    except Exception:
                        raise TypeError("deadline must be a string in ISO format")
                try:
                    deadline = datetime.datetime.fromisoformat(deadline_str)
                    total_time = (deadline - now).total_seconds()
                    normalized_time = max(0, min(1, total_time / (3*24*3600)))  # 3 days window
                    time_factor = 1 - normalized_time
                except Exception:
                    time_factor = 0

            risk_of_delay = task.get('risk_of_delay', 0)
            if isinstance(risk_of_delay, bool):
                raise TypeError("risk_of_delay must not be a boolean")
            if not (isinstance(risk_of_delay, int) or isinstance(risk_of_delay, float)):
                raise TypeError("risk_of_delay must be a number")
            risk_factor = min(1, risk_of_delay / 10)

            stakeholder_pressure = task.get('stakeholder_pressure', 0)
            if isinstance(stakeholder_pressure, bool):
                raise TypeError("stakeholder_pressure must not be a boolean")
            if not (isinstance(stakeholder_pressure, int) or isinstance(stakeholder_pressure, float)):
                raise TypeError("stakeholder_pressure must be a number")
            pressure_factor = min(1, stakeholder_pressure / 10)

            w_time, w_risk, w_pressure = 0.5, 0.3, 0.2

            urgency = (w_time * time_factor +
                       w_risk * risk_factor +
                       w_pressure * pressure_factor)
            urgency_score = round(urgency * 100, 2)
            return urgency_score
        except Exception as e:
            task_id = task.get('id') if task and isinstance(task, dict) else 'unknown'
            logger.error(f"Error calculating urgency for task {task_id}: {e}")
            raise

    def calculate_all(self):
        for task in self.wbs_data:
            self.score_task(task)
        return self.task_scores

def load_wbs_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_scores_to_json(scores, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    import os
    wbs_file = os.path.join(os.path.dirname(__file__), '../../SystemInputs/user_inputs/detailed_wbs.json')
    scores_file = os.path.join(os.path.dirname(__file__), '../../SystemInputs/system_generated/wbs_scores.json')
    try:
        wbs_data = load_wbs_from_file(wbs_file)
    except FileNotFoundError:
        print(f"Error: WBS data file not found at {wbs_file}")
        exit(1)
    calculator = ImportanceUrgencyCalculator(wbs_data)
    scores = calculator.calculate_all()
    save_scores_to_json(scores, scores_file)
    print(f"Importance and urgency scores saved to {scores_file}")
