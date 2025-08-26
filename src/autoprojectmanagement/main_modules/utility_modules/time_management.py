import json
import os
from datetime import datetime, timedelta

class TimeManagement:
    def __init__(self,
                 detailed_wbs_path='JSonDataBase/Inputs/UserInputs/detailed_wbs.json',
                 resource_allocation_path='JSonDataBase/OutPuts/resource_allocation_enriched.json',
                 output_path='JSonDataBase/OutPuts/time_management.json'):
        self.detailed_wbs_path = detailed_wbs_path
        self.resource_allocation_path = resource_allocation_path
        self.output_path = output_path

        self.detailed_wbs = {}
        self.resource_allocations = []

        self.task_schedules = {}

    def load_json(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_json(self, data, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_inputs(self):
        self.detailed_wbs = self.load_json(self.detailed_wbs_path) or {}
        self.resource_allocations = self.load_json(self.resource_allocation_path) or {}

    def calculate_task_duration(self, task):
        """
        Calculate task duration based on resource allocations and working hours.
        For simplicity, assume duration is difference between earliest start and latest end dates.
        """
        allocations = task.get('resource_allocations', [])
        if not allocations:
            return 0
        start_dates = []
        end_dates = []
        for alloc in allocations:
            try:
                start_dates.append(datetime.strptime(alloc['start_date'], '%Y-%m-%d'))
                end_dates.append(datetime.strptime(alloc['end_date'], '%Y-%m-%d'))
            except Exception:
                continue
        if not start_dates or not end_dates:
            return 0
        duration = (max(end_dates) - min(start_dates)).days + 1
        return duration

    def schedule_tasks(self, node=None):
        if node is None:
            node = self.detailed_wbs
        if not node:
            return
        task_id = node.get('id')
        duration = self.calculate_task_duration(node)
        self.task_schedules[task_id] = {
            'task_name': node.get('name'),
            'duration_days': duration,
            'start_date': None,
            'end_date': None
        }
        allocations = node.get('resource_allocations', [])
        if allocations:
            try:
                start_date = min(datetime.strptime(alloc['start_date'], '%Y-%m-%d') for alloc in allocations)
                end_date = max(datetime.strptime(alloc['end_date'], '%Y-%m-%d') for alloc in allocations)
                self.task_schedules[task_id]['start_date'] = start_date.strftime('%Y-%m-%d')
                self.task_schedules[task_id]['end_date'] = end_date.strftime('%Y-%m-%d')
            except Exception:
                pass
        for subtask in node.get('subtasks', []):
            self.schedule_tasks(subtask)

    def run(self):
        self.load_inputs()
        self.schedule_tasks()
        self.save_json(self.task_schedules, self.output_path)
        print(f"Time management schedule saved to {self.output_path}")

if __name__ == "__main__":
    manager = TimeManagement()
    manager.run()
