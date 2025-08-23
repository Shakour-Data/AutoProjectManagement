import json
import os

class WorkflowDataCollector:
    def __init__(self, data_dir='SystemInputs/user_inputs'):
        self.data_dir = data_dir
        self.scrum_sprints_file = os.path.join(self.data_dir, 'scrum_sprints.json')
        self.scrum_tasks_file = os.path.join(self.data_dir, 'scrum_tasks.json')
        self.scrum_burndown_file = os.path.join(self.data_dir, 'scrum_burndown.json')

    def create_scrum_workflow_tables(self):
        # No database tables needed, ensure JSON files exist
        for file in [self.scrum_sprints_file, self.scrum_tasks_file, self.scrum_burndown_file]:
            if not os.path.exists(file):
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump([], f)

    def update_scrum_task(self, task_id, sprint_id, title, status, priority, progress):
        with open(self.scrum_tasks_file, 'r+', encoding='utf-8') as f:
            tasks = json.load(f)
            # Remove existing task with same task_id
            tasks = [t for t in tasks if t.get('task_id') != task_id]
            # Add updated task
            tasks.append({
                'task_id': task_id,
                'sprint_id': sprint_id,
                'title': title,
                'status': status,
                'priority': priority,
                'progress': progress
            })
            f.seek(0)
            json.dump(tasks, f, indent=4)
            f.truncate()

    def update_scrum_burndown(self, sprint_id, day, remaining_work):
        with open(self.scrum_burndown_file, 'r+', encoding='utf-8') as f:
            burndown = json.load(f)
            # Remove existing entry for sprint_id and day
            burndown = [b for b in burndown if not (b.get('sprint_id') == sprint_id and b.get('day') == day)]
            # Add updated entry
            burndown.append({
                'sprint_id': sprint_id,
                'day': day,
                'remaining_work': remaining_work
            })
            f.seek(0)
            json.dump(burndown, f, indent=4)
            f.truncate()

    def generate_scrum_report(self, sprint_id):
        with open(self.scrum_burndown_file, 'r', encoding='utf-8') as f:
            burndown = json.load(f)
            report = sorted(
                [(entry['day'], entry['remaining_work']) for entry in burndown if entry['sprint_id'] == sprint_id],
                key=lambda x: x[0]
            )
            return report

    def close(self):
        pass

# Note: Integration with GitHub should be handled in src/github_integration.py or related modules,
# ensuring synchronization of Scrum workflow stages with GitHub Issues, Pull Requests, and Projects.
