import os
import json
from datetime import datetime

DASHBOARD_PATH = os.path.join('JSonDataBase', 'OutPuts', 'progress_report.md')

class ProgressReport:
    def __init__(self, progress_path=None, task_db_path=None, output_path=None):
        self.progress_path = progress_path or os.path.join('JSonDataBase', 'OutPuts', 'commit_progress.json')
        self.task_db_path = task_db_path or os.path.join('JSonDataBase', 'OutPuts', 'commit_task_database.json')
        self.output_path = output_path or DASHBOARD_PATH

    def load_json(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"JSON file not found: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate_progress_summary(self):
        progress_data = self.load_json(self.progress_path)
        task_db = self.load_json(self.task_db_path)

        total_tasks = len(task_db)
        completed_tasks = sum(1 for v in progress_data.values() if v >= 100)
        in_progress_tasks = sum(1 for v in progress_data.values() if 0 < v < 100)
        pending_tasks = total_tasks - completed_tasks - in_progress_tasks

        # Milestones can be identified from task_db if a field exists, else empty
        milestones = [task for task in task_db.values() if task.get('is_milestone', False)]
        milestones_achieved = sum(1 for m in milestones if progress_data.get(m.get('file_path'), 0) >= 100)
        milestone_tasks = [(m.get('file_path', 'Untitled'), 'Completed' if progress_data.get(m.get('file_path'), 0) >= 100 else 'Pending') for m in milestones]

        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'pending_tasks': pending_tasks,
            'milestones_achieved': milestones_achieved,
            'milestone_tasks': milestone_tasks
        }

    def generate_markdown_report(self, summary):
        lines = []
        lines.append(f"# Project Progress Report")
        lines.append(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append(f"## Summary")
        lines.append(f"- Total Tasks: {summary['total_tasks']}")
        lines.append(f"- Completed Tasks: {summary['completed_tasks']}")
        lines.append(f"- In Progress Tasks: {summary['in_progress_tasks']}")
        lines.append(f"- Pending Tasks: {summary['pending_tasks']}")
        lines.append(f"- Milestones Achieved: {summary['milestones_achieved']}")
        lines.append("")
        lines.append(f"## Completed Activities")
        lines.append(f"- Completed Tasks: {summary['completed_tasks']}")
        lines.append(f"- Milestones Achieved: {summary['milestones_achieved']}")
        lines.append("")
        lines.append(f"## In-Progress Activities")
        lines.append(f"- In Progress Tasks: {summary['in_progress_tasks']}")
        lines.append("")
        lines.append(f"## Pending Activities")
        lines.append(f"- Pending Tasks: {summary['pending_tasks']}")
        lines.append("")
        lines.append(f"## Milestone Status")
        for milestone, status in summary['milestone_tasks']:
            lines.append(f"- **{milestone}**: {status}")
        lines.append("")
        lines.append(f"## Urgency and Importance Summary")
        lines.append(f"- Urgency and Importance data will be included here.")
        lines.append("")
        return "\n".join(lines)

    def save_report(self, content):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate(self):
        summary = self.generate_progress_summary()
        report_md = self.generate_markdown_report(summary)
        self.save_report(report_md)
        print(f"Progress report generated at {self.output_path}")

def generate_report(task_management=None):
    report = ProgressReport()
    report.generate()


def generate_importance_urgency_report(task_management=None):
    # Removed import and usage of deleted importance_urgency_report module
    pass

if __name__ == "__main__":
    report = ProgressReport()
    report.generate()
