import subprocess
import re
from collections import defaultdict
from typing import List, Dict, Any
import json
import os

# Global instance for module-level functions
_global_git_progress_updater = None

class GitProgressUpdater:
    def __init__(self, workflow_definition: List[Dict[str, Any]] = None):
        self.workflow_definition = workflow_definition or []
        self.task_progress = defaultdict(float)
        self.data_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../data/git_progress_data.json')
        self._load_progress_data()

    def _load_progress_data(self):
        try:
            if os.path.exists(self.data_file_path):
                with open(self.data_file_path, 'r') as f:
                    data = json.load(f)
                    for k, v in data.items():
                        self.task_progress[k] = float(v)
        except Exception as e:
            print(f"Failed to load progress data: {e}")

    def _save_progress_data(self):
        try:
            # Ensure directory exists before saving
            os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
            with open(self.data_file_path, 'w') as f:
                json.dump(self.task_progress, f)
        except Exception as e:
            print(f"Failed to save progress data: {e}")

    def run_git_log(self) -> str:
        try:
            result = subprocess.run(
                ["git", "log", "--name-only", "--pretty=format:%H%n%s%n%b%n==END=="],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Git log command failed: {e}")
            return ""

    def parse_git_log(self, log_text: str) -> List[Dict[str, Any]]:
        commits = []
        lines = log_text.splitlines()
        i = 0
        while i < len(lines):
            commit_hash = lines[i].strip()
            i += 1
            message_lines = []
            while i < len(lines) and lines[i].strip() != '' and lines[i].strip() != '==END==':
                message_lines.append(lines[i])
                i += 1
            message = "\n".join(message_lines).strip()
            files = []
            while i < len(lines) and lines[i].strip() != '==END==':
                if lines[i].strip() != '':
                    files.append(lines[i].strip())
                i += 1
            i += 1
            commits.append({
                "hash": commit_hash,
                "message": message,
                "files": files
            })
        return commits

    def map_commits_to_tasks(self, commits: List[Dict[str, Any]]) -> Dict[str, float]:
        task_progress_counts = defaultdict(int)
        for commit in commits:
            message = commit['message']
            # Improved regex to capture task IDs like 1, 1.1, 1.1.1 etc.
            task_ids = re.findall(r'\b\d+(?:\.\d+)*\b', message)
            for task_id in task_ids:
                task_progress_counts[task_id] += 1
        if task_progress_counts:
            max_count = max(task_progress_counts.values())
            for task_id in task_progress_counts:
                task_progress_counts[task_id] = (task_progress_counts[task_id] / max_count) * 100
        return task_progress_counts

    def calculate_workflow_progress(self) -> Dict[str, float]:
        # Placeholder for actual workflow step completion tracking
        return defaultdict(float)

    def combine_progress(self, commit_progress: Dict[str, float], workflow_progress: Dict[str, float]) -> Dict[str, float]:
        combined = defaultdict(float)
        all_task_ids = set(commit_progress.keys()) | set(workflow_progress.keys())
        for task_id in all_task_ids:
            combined[task_id] = (commit_progress.get(task_id, 0) + workflow_progress.get(task_id, 0)) / 2
        return combined

    def update_progress(self) -> Dict[str, float]:
        log_text = self.run_git_log()
        if not log_text:
            print("No git log data available.")
            return {}
        commits = self.parse_git_log(log_text)
        commit_progress = self.map_commits_to_tasks(commits)
        workflow_progress = self.calculate_workflow_progress()
        combined_progress = self.combine_progress(commit_progress, workflow_progress)
        return combined_progress

    # New instance methods for progress management
    def update_progress_for_commit(self, commit_data: dict) -> bool:
        if not isinstance(commit_data, dict):
            raise TypeError("commit_data must be a dictionary")
        commit_id = commit_data.get("commit_id")
        progress = commit_data.get("progress")

        print(f"update_progress_for_commit: commit_id={commit_id}, progress={progress}, current task_progress keys={list(self.task_progress.keys())}")

        if not isinstance(commit_id, str):
            raise TypeError("commit_id must be a string")
        if not commit_id:
            return False

        if progress is None:
            return False
        # Raise TypeError for any non int/float progress, including strings like "fifty"
        if isinstance(progress, bool) or not (isinstance(progress, int) or isinstance(progress, float)):
            raise TypeError("progress must be int or float")
        if progress < 0 or progress > 100:
            return False

        self.task_progress[commit_id] = float(progress)
        self._save_progress_data()
        print(f"update_progress_for_commit: updated task_progress keys={list(self.task_progress.keys())}")
        return True

    def get_progress(self, commit_id: str) -> dict:
        if not isinstance(commit_id, str):
            # Raise TypeError for list or dict to match test expectations
            if isinstance(commit_id, (list, dict, bool)):
                raise TypeError("commit_id must be a string")
            # For other types, raise TypeError to match test expectations
            raise TypeError("commit_id must be a string")
        if not commit_id:
            return None
        progress = self.task_progress.get(commit_id)
        if progress is None:
            return None
        return {"commit_id": commit_id, "progress": progress}

    def reset_progress(self, commit_id: str) -> bool:
        # Refactor to raise TypeError for any list input regardless of contents
        if isinstance(commit_id, (list, tuple, set)):
            raise TypeError("commit_id must be a string")
        if not isinstance(commit_id, str):
            if isinstance(commit_id, dict):
                raise TypeError("commit_id must be a string or a list/tuple/set of strings")
            raise TypeError("commit_id must be a string or a list/tuple/set of strings")
        if not commit_id:
            return False
        print(f"reset_progress: commit_id={commit_id}, current task_progress keys={list(self.task_progress.keys())}")
        if commit_id in self.task_progress:
            del self.task_progress[commit_id]
            self._save_progress_data()
            print(f"reset_progress: deleted commit_id={commit_id}, updated task_progress keys={list(self.task_progress.keys())}")
            return True
        print(f"reset_progress: commit_id={commit_id} not found in task_progress")
        return False

    def update_progress_for_commit(self, commit_data: dict) -> bool:
        if not isinstance(commit_data, dict):
            raise TypeError("commit_data must be a dictionary")
        commit_id = commit_data.get("commit_id")
        progress = commit_data.get("progress")

        if not isinstance(commit_id, str):
            raise TypeError("commit_id must be a string")
        if not commit_id:
            return False

        if progress is None:
            return False
        # Raise TypeError for any non int/float progress, including strings like "fifty"
        if isinstance(progress, bool) or not (isinstance(progress, int) or isinstance(progress, float)):
            raise TypeError("progress must be int or float")
        if progress < 0 or progress > 100:
            return False

        self.task_progress[commit_id] = float(progress)
        self._save_progress_data()
        return True

def _get_global_git_progress_updater():
    global _global_git_progress_updater
    if _global_git_progress_updater is None:
        _global_git_progress_updater = GitProgressUpdater()
    return _global_git_progress_updater

def update_progress(commit_data: dict) -> bool:
    updater = _get_global_git_progress_updater()
    return updater.update_progress_for_commit(commit_data)

def get_progress(commit_id: str) -> dict:
    updater = _get_global_git_progress_updater()
    return updater.get_progress(commit_id)

def reset_progress(commit_id: str) -> bool:
    updater = _get_global_git_progress_updater()
    return updater.reset_progress(commit_id)
