import json
import os
from datetime import datetime

class CommitProgressManager:
    def __init__(self, commit_task_db_path='JSonDataBase/OutPuts/commit_task_database.json',
                 commit_progress_path='JSonDataBase/OutPuts/commit_progress.json'):
        self.commit_task_db_path = commit_task_db_path
        self.commit_progress_path = commit_progress_path
        self.commit_task_db = {}
        self.commit_progress = {}


    def load_commit_task_db(self):
        if os.path.exists(self.commit_task_db_path):
            with open(self.commit_task_db_path, 'r', encoding='utf-8') as f:
                self.commit_task_db = json.load(f)
        else:
            self.commit_task_db = {}

    def generate_commit_progress(self):
        """
        Generate commit progress per task based on commit_task_database.
        For each task, calculate number of commits, last commit date, and progress percentage.
        """
        task_commits = {}
        for commit_hash, task_info in self.commit_task_db.items():
            task_id = task_info.get('task_id')
            commit_date_str = task_info.get('commit_date')
            if not task_id or not commit_date_str:
                continue
            commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%S')
            if task_id not in task_commits:
                task_commits[task_id] = {
                    'commit_count': 0,
                    'last_commit_date': commit_date,
                }
            task_commits[task_id]['commit_count'] += 1
            if commit_date > task_commits[task_id]['last_commit_date']:
                task_commits[task_id]['last_commit_date'] = commit_date

        # Calculate progress percentage (simple heuristic: commit_count capped at 10)
        for task_id, data in task_commits.items():
            commit_count = data['commit_count']
            progress_percent = min(commit_count * 10, 100)
            self.commit_progress[task_id] = {
                'commit_count': commit_count,
                'last_commit_date': data['last_commit_date'].isoformat(),
                'progress_percent': progress_percent
            }

    def save_commit_progress(self):
        with open(self.commit_progress_path, 'w', encoding='utf-8') as f:
            json.dump(self.commit_progress, f, indent=2, ensure_ascii=False)

    def run(self):
        self.load_commit_task_db()
        self.generate_commit_progress()
        self.save_commit_progress()
        print(f"Commit progress saved to {self.commit_progress_path}")

if __name__ == "__main__":
    manager = CommitProgressManager()
    manager.run()
