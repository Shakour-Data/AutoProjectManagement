import json
import os
from .feature_weights import URGENCY_FEATURE_WEIGHTS, IMPORTANCE_FEATURE_WEIGHTS

class DBDataCollector:
    def __init__(self, data_dir='SystemInputs/user_inputs'):
        self.data_dir = data_dir
        self.tasks_file = os.path.join(self.data_dir, 'tasks.json')
        self.resource_allocation_file = os.path.join(self.data_dir, 'resource_allocation.json')
        self.progress_metrics_file = os.path.join(self.data_dir, 'progress_metrics.json')
        self.feature_weights_file = os.path.join(self.data_dir, 'feature_weights.json')

    def collect_and_store_tasks(self, tasks):
        """
        Collect task data including progress, resource allocation, and store in JSON file.
        """
        tasks_data = [task.__dict__ for task in tasks]
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, indent=4)

    def collect_resource_allocation(self, tasks):
        """
        Analyze resource allocation and store summary in JSON file.
        """
        resource_usage = {}
        for task in tasks:
            for user in task.assigned_to:
                resource_usage[user] = resource_usage.get(user, 0) + 1
        with open(self.resource_allocation_file, 'w', encoding='utf-8') as f:
            json.dump(resource_usage, f, indent=4)

    def collect_progress_metrics(self, tasks):
        """
        Collect progress percentages and store/update in JSON file.
        """
        progress_data = {}
        for task in tasks:
            progress_data[task.id] = task.workflow_progress_percentage()
        with open(self.progress_metrics_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=4)

    def insert_feature_weights(self, urgency_weights, importance_weights):
        """
        Insert predefined weights for urgency and importance features into JSON file.
        """
        weights = {
            'urgency_weights': urgency_weights,
            'importance_weights': importance_weights
        }
        with open(self.feature_weights_file, 'w', encoding='utf-8') as f:
            json.dump(weights, f, indent=4)

    def close(self):
        pass
