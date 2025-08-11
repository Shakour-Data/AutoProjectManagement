import json
import os
from datetime import datetime

class ResourceAllocationManager:
    def __init__(self,
                 resource_allocation_path='JSonDataBase/Inputs/UserInputs/task_resource_allocation.json',
                 detailed_wbs_path='JSonDataBase/Inputs/UserInputs/detailed_wbs.json',
                 resource_costs_path='JSonDataBase/Inputs/UserInputs/resource_costs.json',
                 output_path='JSonDataBase/OutPuts/resource_allocation_enriched.json',
                 summary_output_path='JSonDataBase/OutPuts/resource_allocation_summary.json'):
        self.resource_allocation_path = resource_allocation_path
        self.detailed_wbs_path = detailed_wbs_path
        self.resource_costs_path = resource_costs_path
        self.output_path = output_path
        self.summary_output_path = summary_output_path

        self.resource_allocations = []
        self.detailed_wbs = {}
        self.resource_costs = {}

        self.task_cost_summary = {}

    def load_json(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_json(self, data, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_inputs(self):
        self.resource_allocations = self.load_json(self.resource_allocation_path) or []
        self.detailed_wbs = self.load_json(self.detailed_wbs_path) or {}
        self.resource_costs = self.load_json(self.resource_costs_path) or {}

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

    def calculate_task_cost(self, allocation):
        resource_id = allocation.get('resource_id')
        allocation_percent = allocation.get('allocation_percent', 0) / 100.0
        start_date_str = allocation.get('start_date')
        end_date_str = allocation.get('end_date')

        if resource_id not in self.resource_costs:
            return 0.0

        hourly_cost = self.resource_costs[resource_id].get('hourly_cost', 0.0)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            days = (end_date - start_date).days + 1
        except Exception:
            days = 0

        # Assuming 8 working hours per day
        total_hours = days * 8 * allocation_percent
        cost = total_hours * hourly_cost
        return cost

    def enrich_wbs_with_resources(self):
        # Add resource allocation and cost info to tasks in detailed WBS
        for allocation in self.resource_allocations:
            task_id = allocation.get('task_id')
            task_node = self.find_task_by_id(task_id)
            if not task_node:
                continue
            if 'resource_allocations' not in task_node:
                task_node['resource_allocations'] = []
            cost = self.calculate_task_cost(allocation)
            allocation_enriched = allocation.copy()
            allocation_enriched['calculated_cost'] = cost
            task_node['resource_allocations'].append(allocation_enriched)

    def summarize_costs(self, node=None):
        if node is None:
            node = self.detailed_wbs
        if not node:
            return 0.0
        total_cost = 0.0
        for alloc in node.get('resource_allocations', []):
            total_cost += alloc.get('calculated_cost', 0.0)
        for subtask in node.get('subtasks', []):
            total_cost += self.summarize_costs(subtask)
        self.task_cost_summary[node.get('id')] = {
            'task_name': node.get('name'),
            'total_cost': total_cost
        }
        return total_cost

    def run(self):
        self.load_inputs()
        self.enrich_wbs_with_resources()
        self.summarize_costs()
        self.save_json(self.detailed_wbs, self.output_path)
        self.save_json(self.task_cost_summary, self.summary_output_path)
        print(f"Resource allocation enriched WBS saved to {self.output_path}")
        print(f"Resource allocation cost summary saved to {self.summary_output_path}")

if __name__ == "__main__":
    manager = ResourceAllocationManager()
    manager.run()
