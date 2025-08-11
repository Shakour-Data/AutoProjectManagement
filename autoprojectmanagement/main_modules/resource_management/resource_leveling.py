import json
from collections import defaultdict

class ResourceLeveler:
    def __init__(self, tasks_filepath, allocations_filepath, output_filepath, duration_type='normal'):
        self.tasks_filepath = tasks_filepath
        self.allocations_filepath = allocations_filepath
        self.output_filepath = output_filepath
        self.duration_type = duration_type  # 'optimistic', 'normal', or 'pessimistic'
        self.tasks = []
        self.allocations = []
        self.flat_tasks = []
        self.task_map = {}
        self.task_schedules = {}

    def load_json_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json_file(self, data, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def flatten_tasks(self, tasks, parent_id=None):
        """
        Flatten nested tasks into a list with parent-child relationships.
        """
        flat_list = []
        for task in tasks:
            task_copy = task.copy()
            task_copy['parent_id'] = parent_id
            subtasks = task_copy.pop('subtasks', [])
            flat_list.append(task_copy)
            flat_list.extend(self.flatten_tasks(subtasks, task_copy['id']))
        return flat_list

    def resource_leveling(self):
        """
        Basic resource leveling algorithm:
        - For each resource, ensure tasks assigned do not overlap in time.
        - Adjust task start times to avoid resource conflicts.
        Note: This is a simplified example assuming tasks have duration fields and no explicit start/end dates.
        """
        # Map task_id to task details
        self.task_map = {task['id']: task for task in self.flat_tasks}

        # Map resource_id to list of assigned tasks
        resource_tasks = defaultdict(list)
        for alloc in self.allocations:
            # Use 'task_id' and 'role' from allocation to assign resource_id as role for demo
            resource_id = alloc.get('role', 'unknown')
            resource_tasks[resource_id].append(alloc['task_id'])

        # Assign start and end times per resource
        resource_schedules = {}

        for resource_id, task_ids in resource_tasks.items():
            current_time = 0
            schedule = []
            for tid in task_ids:
                task = self.task_map.get(tid)
                if not task:
                    continue
                duration = task.get(f'{self.duration_type}_hours', 1)  # default 1 hour if missing
                start = current_time
                end = start + duration
                schedule.append({'task_id': tid, 'start': start, 'end': end})
                self.task_schedules[tid] = {'resource_id': resource_id, 'start': start, 'end': end}
                current_time = end  # next task starts after current ends
            resource_schedules[resource_id] = schedule

        return self.task_schedules

    def run(self):
        self.tasks = self.load_json_file(self.tasks_filepath)
        self.allocations = self.load_json_file(self.allocations_filepath)
        self.flat_tasks = self.flatten_tasks(self.tasks)
        leveled_schedule = self.resource_leveling()
        self.save_json_file(leveled_schedule, self.output_filepath)
        print(f"Resource leveling completed. Output saved to {self.output_filepath}")

    def main():
        tasks_filepath = 'projects/current_project/docs/detailed_wbs.json'
        allocations_filepath = 'projects/current_project/docs/task_resource_allocation.json'
        output_filepath = 'projects/current_project/docs/leveled_resource_schedule.json'

        leveler = ResourceLeveler(tasks_filepath, allocations_filepath, output_filepath)
        leveler.run()

    if __name__ == '__main__':
        main()
