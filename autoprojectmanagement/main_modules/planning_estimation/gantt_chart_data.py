import os
import json
import datetime
from typing import List, Dict, Any, Optional

class GanttChartData:
    def __init__(self, input_dir: str = 'project_inputs/PM_JSON/user_inputs'):
        self.input_dir = input_dir
        self.tasks = []

    def load_tasks(self):
        path = os.path.join(self.input_dir, 'detailed_wbs.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
        except Exception as e:
            print(f"Error loading tasks for Gantt chart: {e}")
            self.tasks = []

    def parse_date(self, date_str: Optional[str]) -> Optional[datetime.date]:
        if not date_str:
            return None
        try:
            return datetime.date.fromisoformat(date_str)
        except Exception:
            return None

    def build_gantt_data(self) -> List[Dict[str, Any]]:
        """
        Build Gantt chart data from tasks.
        Each task dict should include:
            - id
            - name
            - start_date
            - end_date (calculated from start_date + duration)
            - dependencies (list of task ids)
            - progress (0-100)
        """
        gantt_data = []

        def process_task(task, parent_start: Optional[datetime.date] = None):
            task_id = task.get('id')
            name = task.get('name') or task.get('title') or f"Task {task_id}"
            start_date_str = task.get('start_date')
            duration_days = task.get('duration_days') or task.get('duration') or 1
            dependencies = task.get('dependencies', [])

            start_date = self.parse_date(start_date_str) or parent_start or datetime.date.today()
            end_date = start_date + datetime.timedelta(days=duration_days)

            progress = task.get('progress', 0) * 100 if isinstance(task.get('progress'), float) else task.get('progress', 0)

            gantt_data.append({
                'id': task_id,
                'name': name,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'dependencies': dependencies,
                'progress': progress,
            })

            for subtask in task.get('subtasks', []):
                process_task(subtask, start_date)

        for task in self.tasks:
            process_task(task)

        return gantt_data

def generate_gantt_chart(tasks):
    """Generate Gantt chart data from a list of tasks."""
    if tasks is None:
        raise TypeError("Tasks input cannot be None")
    if not isinstance(tasks, list):
        raise TypeError("Tasks input must be a list")
    for task in tasks:
        if task is None:
            raise TypeError("Task cannot be None")
        if not isinstance(task, dict):
            raise TypeError("Each task must be a dict")
        if 'id' not in task:
            raise KeyError("Task missing 'id'")
        if 'start' not in task:
            raise KeyError("Task missing 'start'")
        if 'end' not in task:
            raise KeyError("Task missing 'end'")
        # Validate date format
        start = task['start']
        end = task['end']
        if not isinstance(start, str) or not isinstance(end, str):
            raise TypeError("Start and end dates must be strings")
        try:
            from datetime import datetime
            start_date = datetime.fromisoformat(start)
            end_date = datetime.fromisoformat(end)
        except Exception:
            raise ValueError("Invalid date format, expected ISO format YYYY-MM-DD")
        if start_date > end_date:
            raise ValueError("Start date cannot be after end date")
        # Validate name type if present
        name = task.get('name', '')
        if name is not None and not isinstance(name, (str, type(None))):
            raise TypeError("Task name must be a string or None")
    generator = GanttChartData()
    generator.tasks = tasks
    processed_tasks = generator.build_gantt_data()
    return {"tasks": processed_tasks}

if __name__ == "__main__":
    generator = GanttChartData()
    generator.load_tasks()
    data = generator.build_gantt_data()
    output_path = 'SystemInputs/system_generated/gantt_chart_data.json'
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Gantt chart data saved to {output_path}")
    except Exception as e:
        print(f"Failed to save Gantt chart data: {e}")
