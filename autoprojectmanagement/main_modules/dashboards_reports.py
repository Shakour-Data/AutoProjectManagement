import json
from typing import Dict, Any, List, Optional
from .progress_calculator_refactored import ProgressCalculator

class DashboardReports:
    def __init__(self, input_dir: str = 'JSonDataBase/Inputs/UserInputs'):
        self.input_dir = input_dir
        self.data = {}
        self.progress_calculator = ProgressCalculator(input_dir)

    def load_json_file(self, filename: str) -> Optional[Any]:
        # Override to load wbs_scores.json from fixed path
        if filename == 'wbs_scores.json':
            path = 'JSonDataBase/OutPuts/wbs_scores.json'
        else:
            path = f"{self.input_dir}/{filename}"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None

    def load_inputs(self):
        self.data['detailed_wbs'] = self.load_json_file('detailed_wbs.json')
        self.data['human_resources'] = self.load_json_file('human_resources.json')
        self.data['resource_allocation'] = self.load_json_file('resource_allocation.json')
        self.data['task_resource_allocation'] = self.load_json_file('task_resource_allocation.json')
        self.data['wbs_scores'] = self.load_json_file('wbs_scores.json')
        self.data['workflow_definition'] = self.load_json_file('workflow_definition.json')

        self.progress_calculator.load_inputs()
        self.progress_calculator.enrich_tasks_with_progress()
        self.data['detailed_wbs'] = self.progress_calculator.get_enriched_tasks()

    def _format_task(self, task: Dict[str, Any]) -> str:
        title = task.get('title', 'No Title')
        status = task.get('status', 'unknown')
        progress = task.get('progress', 0.0)
        progress_percent = progress * 100 if isinstance(progress, (int, float)) else 0.0
        importance = task.get('importance')
        urgency = task.get('urgency')
        score = None
        if importance is not None and urgency is not None:
            score = (importance * 0.6) + (urgency * 0.4)
            return f"- **{title}** (Status: {status}, Importance: {importance:.2f}, Urgency: {urgency:.2f}, Score: {score:.2f}, Progress: {progress_percent:.1f}%)"
        else:
            return f"- **{title}** (Status: {status}, Progress: {progress_percent:.1f}%)"

    def generate_progress_report(self) -> str:
        tasks = self.data.get('detailed_wbs') or []
        total_tasks = len(tasks)
        completed = sum(1 for t in tasks if t.get('status') == 'completed')
        in_progress = sum(1 for t in tasks if t.get('status') == 'in_progress')
        pending = total_tasks - completed - in_progress
        progress_percent = (completed / total_tasks * 100) if total_tasks > 0 else 0.0

        md = f"# Progress Report Dashboard\n\n"
        md += f"- Total Tasks: {total_tasks}\n"
        md += f"- Completed: {completed}\n"
        md += f"- In Progress: {in_progress}\n"
        md += f"- Pending: {pending}\n"
        md += f"- Progress Percentage: {progress_percent:.2f}%\n\n"
        md += "## Task Details\n"
        for task in tasks:
            md += self._format_task(task) + "\n"
        return md

    def generate_priority_urgency_report(self) -> str:
        tasks = self.data.get('detailed_wbs') or []
        important_tasks = sorted(tasks, key=lambda x: x.get('importance', 0.0), reverse=True)[:10]
        urgent_tasks = sorted(tasks, key=lambda x: x.get('urgency', 0.0), reverse=True)[:10]

        # If importance or urgency data missing, add a note
        importance_data_missing = any(task.get('importance') is None for task in tasks)
        urgency_data_missing = any(task.get('urgency') is None for task in tasks)

        md = "# Task Priority and Urgency Report\n\n"
        if importance_data_missing or urgency_data_missing:
            md += "_Note: Importance and/or urgency data missing in input tasks. Report based on available data._\n\n"

        matrix = {
            'Urgent & Important': [],
            'Urgent & Not Important': [],
            'Not Urgent & Important': [],
            'Not Urgent & Not Important': []
        }
        for task in tasks:
            urgent = task.get('urgency', 0.0) >= 0.5
            important = task.get('importance', 0.0) >= 0.5
            if urgent and important:
                matrix['Urgent & Important'].append(task)
            elif urgent and not important:
                matrix['Urgent & Not Important'].append(task)
            elif not urgent and important:
                matrix['Not Urgent & Important'].append(task)
            else:
                matrix['Not Urgent & Not Important'].append(task)

        md += "## Top 10 Important Tasks\n"
        for task in important_tasks:
            md += self._format_task(task) + "\n"
        md += "\n## Top 10 Urgent Tasks\n"
        for task in urgent_tasks:
            md += self._format_task(task) + "\n"

        md += "\n## Eisenhower Matrix\n"
        for quadrant, tasks_list in matrix.items():
            md += f"\n### {quadrant} ({len(tasks_list)} tasks)\n"
            for task in tasks_list:
                md += self._format_task(task) + "\n"
        return md

    def generate_resource_allocation_report(self) -> str:
        human_resources = self.data.get('human_resources') or []
        resource_allocation = self.data.get('resource_allocation') or []
        task_resource_allocation = self.data.get('task_resource_allocation') or []

        allocation_summary = {}
        for alloc in task_resource_allocation:
            resource_id = alloc.get('resource_id')
            allocation_summary[resource_id] = allocation_summary.get(resource_id, 0.0) + alloc.get('allocation_percent', 0.0)

        md = "# Resource Allocation Dashboard\n\n"
        md += "## Human Resources\n"
        for hr in human_resources:
            md += f"- {hr.get('name', 'Unknown')} ({hr.get('role', 'Unknown Role')})\n"

        md += "\n## Resource Allocation Summary\n"
        for resource_id, allocation in allocation_summary.items():
            md += f"- Resource ID {resource_id}: {allocation}% allocated\n"

        return md

    def generate_cost_management_report(self) -> str:
        wbs_scores = self.data.get('wbs_scores') or []
        resource_allocation = self.data.get('resource_allocation') or []

        total_cost = sum(item.get('cost', 0.0) for item in wbs_scores if isinstance(item, dict))

        md = "# Cost Management Report\n\n"
        md += f"- Total Cost: {total_cost}\n\n"
        md += "## WBS Scores\n"
        for item in wbs_scores:
            if isinstance(item, dict):
                md += f"- {item.get('id', 'Unknown ID')}: Cost = {item.get('cost', 0.0)}\n"

        return md

    def generate_risk_issue_tracking_report(self) -> str:
        workflow_definition = self.data.get('workflow_definition') or []
        risks = [item for item in workflow_definition if item.get('type') == 'risk']
        issues = [item for item in workflow_definition if item.get('type') == 'issue']

        md = "# Risk and Issue Tracking Dashboard\n\n"
        md += "## Risks\n"
        for risk in risks:
            md += f"- {risk.get('description', 'No description')}\n"

        md += "\n## Issues\n"
        for issue in issues:
            md += f"- {issue.get('description', 'No description')}\n"

