import subprocess
import json
import os
import re
import logging
from collections import defaultdict
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ProgressDataGenerator:
    def __init__(
        self,
        db_progress_json_path: str = os.path.join('docs', 'project_management', 'task_progress.json'),
        workflow_definition_path: str = os.path.join('docs', 'db_json', 'workflow_definition.json'),
        commit_task_id_pattern: str = r'\\b\\d+\\.\\d+\\b',
        commit_weight: float = 0.6,
        workflow_weight: float = 0.4,
        commit_json_path: str = None,
    ):
        self.db_progress_json_path = db_progress_json_path
        self.workflow_definition_path = workflow_definition_path
        self.commit_task_id_pattern = commit_task_id_pattern
        self.commit_weight = commit_weight
        self.workflow_weight = workflow_weight
        self.commit_json_path = commit_json_path

    def run_git_log(self) -> Optional[str]:
        """Run git log to get commit history with messages and files changed."""
        try:
            result = subprocess.run(
                ["git", "log", "--name-only", "--pretty=format:%H%n%s%n%b%n==END=="],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Git log command failed: {e}")
            return None

    def parse_git_log(self, log_text: str) -> List[Dict]:
        """
        Parse git log output into a list of commits.
        Each commit is a dict with keys: hash, message, files (list).
        """
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
            # Skip the ==END== line
            i += 1
            commits.append({
                "hash": commit_hash,
                "message": message,
                "files": files
            })
        return commits

    def load_workflow_definition(self) -> List[Dict]:
        try:
            with open(self.workflow_definition_path, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
            return workflow
        except Exception as e:
            logger.error(f"Failed to load workflow definition: {e}")
            return []

    def map_commits_to_tasks(self, commits: List[Dict]) -> Dict[str, float]:
        """
        Map commits to tasks based on commit messages or file paths.
        This looks for task ids in commit messages using regex pattern.
        """
        task_progress = defaultdict(int)  # task_id -> progress count

        pattern = re.compile(self.commit_task_id_pattern)

        for commit in commits:
            message = commit['message']
            task_ids = pattern.findall(message)
            for task_id in task_ids:
                task_progress[task_id] += 1

        # Normalize progress counts to a 0-100 scale
        if task_progress:
            max_count = max(task_progress.values())
            for task_id in task_progress:
                task_progress[task_id] = (task_progress[task_id] / max_count) * 100
        return task_progress

    def calculate_workflow_progress(self) -> Dict[str, float]:
        """
        Calculate progress based on workflow steps completion.
        Implement actual task-step mapping and weighting.
        """
        workflow = self.load_workflow_definition()
        if not workflow:
            return {}

        step_weight = 100 / len(workflow)
        workflow_progress = defaultdict(float)  # task_id -> progress percentage

        # TODO: Implement actual tracking of completed steps per task
        # For now, return empty progress

        return workflow_progress

    def combine_progress(self, commit_progress: Dict[str, float], workflow_progress: Dict[str, float]) -> Dict[str, float]:
        """
        Combine commit-based and workflow-based progress using configured weights.
        """
        combined_progress = defaultdict(float)
        all_task_ids = set(commit_progress.keys()) | set(workflow_progress.keys())

        for task_id in all_task_ids:
            commit_val = commit_progress.get(task_id, 0)
            workflow_val = workflow_progress.get(task_id, 0)
            combined_progress[task_id] = (commit_val * self.commit_weight) + (workflow_val * self.workflow_weight)

        return combined_progress

    def save_progress_to_json(self, progress_data: Dict[str, float]) -> None:
        try:
            # Ensure directory exists
            dir_path = os.path.dirname(self.db_progress_json_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(self.db_progress_json_path, 'w', encoding='utf-8') as f:
                json.dump(progress_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Task progress data saved to {self.db_progress_json_path}")
        except Exception as e:
            logger.error(f"Failed to save progress data: {e}")

    def generate_progress(self) -> None:
        log_text = self.run_git_log()
        if not log_text:
            logger.warning("No git log data available.")
            return
        commits = self.parse_git_log(log_text)
        commit_progress = self.map_commits_to_tasks(commits)
        workflow_progress = self.calculate_workflow_progress()
        combined_progress = self.combine_progress(commit_progress, workflow_progress)
        self.save_progress_to_json(combined_progress)

def generate_progress_data(input_data):
    if not isinstance(input_data, dict):
        raise TypeError("Input data must be a dictionary.")
    tasks = input_data.get("tasks", [])
    if not isinstance(tasks, list):
        raise TypeError("Tasks must be a list.")

    # Instantiate ProgressDataGenerator and generate progress data from git logs and workflow
    generator = ProgressDataGenerator()
    generator.generate_progress()
    # Load the generated progress data from the JSON file
    try:
        with open(generator.db_progress_json_path, 'r', encoding='utf-8') as f:
            generated_progress = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load generated progress data: {e}")

    # Validate and process input tasks, override or merge with generated progress
    for task in tasks:
        if task is None:
            raise TypeError("Task cannot be None.")
        if not isinstance(task, dict):
            raise TypeError("Each task must be a dictionary.")
        task_id = task.get("id")
        status = task.get("status", "")
        if not isinstance(status, (str, type(None))):
            raise TypeError("Status must be a string or None.")
        # Normalize status to string
        if status is None:
            status_str = ""
        else:
            status_str = str(status)
        # Override or add to generated progress
        generated_progress[str(task_id)] = status_str

    return generated_progress

if __name__ == "__main__":
    generator = ProgressDataGenerator()
    generator.generate()
