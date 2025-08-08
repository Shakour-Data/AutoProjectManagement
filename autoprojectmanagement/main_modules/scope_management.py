import json
import os
from datetime import datetime

class ScopeManagement:
    def __init__(self,
                 detailed_wbs_path='JSonDataBase/Inputs/UserInputs/detailed_wbs.json',
                 scope_changes_path='JSonDataBase/Inputs/UserInputs/scope_changes.json',
                 output_path='JSonDataBase/OutPuts/scope_management.json'):
        self.detailed_wbs_path = detailed_wbs_path
        self.scope_changes_path = scope_changes_path
        self.output_path = output_path

        self.detailed_wbs = {}
        self.scope_changes = []
        self.scope_status = {}

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
        self.scope_changes = self.load_json(self.scope_changes_path) or []

    def apply_scope_changes(self):
        """
        Apply scope changes to the detailed WBS.
        Scope changes are expected to be a list of dicts with:
        - task_id
        - change_type: 'add', 'remove', 'modify'
        - details: dict with change specifics
        """
        self.scope_status = {
            'added_tasks': [],
            'removed_tasks': [],
            'modified_tasks': []
        }
        for change in self.scope_changes:
            task_id = change.get('task_id')
            change_type = change.get('change_type')
            details = change.get('details', {})
            if change_type == 'add':
                # Add new task under parent specified in details
                parent_id = details.get('parent_id')
                new_task = details.get('task')
                if parent_id and new_task:
                    parent_task = self.find_task_by_id(parent_id)
                    if parent_task is not None:
                        if 'subtasks' not in parent_task:
                            parent_task['subtasks'] = []
                        parent_task['subtasks'].append(new_task)
                        self.scope_status['added_tasks'].append(new_task['id'])
            elif change_type == 'remove':
                # Remove task by id
                removed = self.remove_task_by_id(task_id)
                if removed:
                    self.scope_status['removed_tasks'].append(task_id)
            elif change_type == 'modify':
                # Modify task attributes
                task = self.find_task_by_id(task_id)
                if task:
                    for key, value in details.items():
                        task[key] = value
                    self.scope_status['modified_tasks'].append(task_id)

    def find_task_by_id(self, task_id, node=None):
        if node is None:
            node = self.detailed_wbs
        if not node:
            return None
        if node.get('id') == task_id:
            return node
        for subtask in node.get('subtasks', []):
            found = self.find_task_by_id(task_id, subtask)
            if found:
                return found
        return None

    def remove_task_by_id(self, task_id, node=None):
        if node is None:
            node = self.detailed_wbs
        if not node or 'subtasks' not in node:
            return False
        for i, subtask in enumerate(node['subtasks']):
            if subtask.get('id') == task_id:
                del node['subtasks'][i]
                return True
            else:
                removed = self.remove_task_by_id(task_id, subtask)
                if removed:
                    return True
        return False

    def run(self):
        self.load_inputs()
        self.apply_scope_changes()
        self.save_json(self.detailed_wbs, self.output_path)
        print(f"Scope management output saved to {self.output_path}")
        print(f"Scope changes applied: {self.scope_status}")

if __name__ == "__main__":
    manager = ScopeManagement()
    manager.run()
