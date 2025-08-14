"""
path: autoprojectmanagement/services/automation_services/auto_commit.py
File: auto_commit.py
Purpose: Automated git commit service with project management integration
Author: Shakour-Data2
Version: 2.0.0
License: MIT
Description: This module provides automated commit functionality that integrates with
project management workflows, including progress tracking, task mapping, and
intelligent commit message generation based on conventional commit standards.
"""

import os
import subprocess
import datetime
from collections import defaultdict
import sys
import re
import json
from typing import Dict, List, Tuple, Optional, Any, Union
from pathlib import Path
import logging

# Constants
MAX_COMMIT_MESSAGE_LENGTH = 255
DEFAULT_ENCODING = 'utf-8'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
STAGE_WEIGHTS = {
    "Requirements Gathering": 0.15,
    "Design": 0.15,
    "Implementation": 0.30,
    "Code Review": 0.10,
    "Testing": 0.15,
    "Deployment": 0.10,
    "Maintenance": 0.05
}

# Type aliases
GitStatus = str
FilePath = str
CommitHash = str
TaskId = str

# Configure logging
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to Python path to handle imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def format_commit_message(message: Optional[str]) -> str:
    """
    Format a commit message by cleaning and normalizing it.
    
    Args:
        message: The raw commit message
        
    Returns:
        The formatted commit message
        
    Raises:
        TypeError: If message is None or not a string
    """
    if message is None:
        raise TypeError("Commit message cannot be None")
    
    if not isinstance(message, str):
        raise TypeError("Commit message must be a string")
    
    # Remove leading and trailing whitespace
    message = message.strip()
    
    # Replace multiple consecutive whitespace characters with single spaces
    message = re.sub(r'\s+', ' ', message)
    
    # Remove control characters except for spaces and tabs
    message = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', message)
    
    # Remove literal escape sequences like \n, \t, \r
    message = re.sub(r'\\n(?=\s|$)', ' ', message)
    message = re.sub(r'\\t(?=\s|$)', ' ', message)
    message = re.sub(r'\\r(?=\s|$)', ' ', message)
    
    # Remove extra spaces that may have been created
    message = re.sub(r'\s+', ' ', message).strip()
    
    # Limit message length
    if len(message) > MAX_COMMIT_MESSAGE_LENGTH:
        message = message[:MAX_COMMIT_MESSAGE_LENGTH]
    
    return message

class AutoCommit:
    """Automated git commit service with project management integration."""
    
    def __init__(self) -> None:
        """Initialize the AutoCommit service."""
        self.logger = logging.getLogger(__name__)
        self.bm = self._load_backup_manager()
        
    def _load_backup_manager(self) -> Any:
        """
        Load the backup manager module dynamically with proper configuration.
        
        Returns:
            BackupManager instance
        """
        try:
            import importlib.util
            current_dir = os.path.dirname(os.path.abspath(__file__))
            backup_manager_path = os.path.join(current_dir, 'backup_manager.py')
            
            spec = importlib.util.spec_from_file_location("backup_manager", backup_manager_path)
            if spec is None or spec.loader is None:
                raise ImportError("Could not load backup_manager module")
                
            backup_manager = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(backup_manager)
            
            # Create proper BackupConfig instance
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            config = backup_manager.BackupConfig(
                source_paths=[project_root],
                backup_location=os.path.join(project_root, 'backups'),
                retention_days=30,
                compression_type=backup_manager.CompressionType.ZIP,
                exclude_patterns=['.git', '__pycache__', '*.pyc', '.DS_Store', 'node_modules', 'venv', '.venv']
            )
            
            return backup_manager.BackupManager(config)
        except Exception as e:
            self.logger.error(f"Failed to load backup manager: {e}")
            raise

    def run_git_command(self, args: List[str], cwd: Optional[str] = None) -> Tuple[bool, str]:
        """
        Run a git command and return the result.
        
        Args:
            args: Git command arguments
            cwd: Working directory for the command
            
        Returns:
            Tuple of (success, output)
        """
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd,
                encoding=DEFAULT_ENCODING,
                errors='ignore'
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git command failed: git {' '.join(args)}")
            self.logger.error(f"Error: {e.stderr.strip()}")
            return False, e.stderr.strip()

    def get_git_changes(self) -> List[str]:
        """
        Fetch Git status and return list of changes.
        
        Returns:
            List of git status lines
        """
        success, output = self.run_git_command(["status", "--short"])
        if not success:
            return []
        return [line for line in output.splitlines() if line.strip()]

    def group_related_files(self, changes: List[str]) -> Dict[str, List[Tuple[str, str]]]:
        """
        Group files based on top-level directory (code relationship).
        
        Args:
            changes: List of git status changes
            
        Returns:
            Dictionary mapping group names to file tuples
        """
        groups: Dict[str, List[Tuple[str, str]]] = defaultdict(list)

        for change in changes:
            if not change:
                continue
                
            status, file_path = self._parse_git_status(change)
            if not file_path:
                continue
                
            group_name = self._determine_group_name(file_path)
            groups[group_name].append((status, file_path))

        return groups

    def _parse_git_status(self, change: str) -> Tuple[str, str]:
        """
        Parse a git status line into status and file path.
        
        Args:
            change: Git status line
            
        Returns:
            Tuple of (status, file_path)
        """
        if change.startswith("??"):
            status = "??"
            file_path = change[2:].lstrip()
        else:
            parts = change.split(None, 1)
            if len(parts) == 2:
                status, file_path = parts[0], parts[1].lstrip()
            else:
                status = parts[0]
                file_path = ""

        if status == "R":
            parts = file_path.split("->")
            if len(parts) == 2:
                file_path = parts[1].strip()
            else:
                file_path = file_path.strip()

        return status, file_path

    def _determine_group_name(self, file_path: str) -> str:
        """
        Determine the group name for a file based on its path.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Group name
        """
        parts = file_path.split(os.sep)
        return parts[0] if len(parts) > 1 else "root"

    def categorize_files(self, files: List[Tuple[str, str]]) -> Dict[str, List[str]]:
        """
        Categorize files into different change types.
        
        Args:
            files: List of (status, file_path) tuples
            
        Returns:
            Dictionary mapping categories to file lists
        """
        categories: Dict[str, List[str]] = defaultdict(list)
        
        status_mapping = {
            "A": "Added",
            "M": "Modified",
            "D": "Deleted",
            "R": "Renamed",
            "??": "Untracked"
        }

        for status, file_path in files:
            category = status_mapping.get(status, "Other")
            categories[category].append(file_path)

        return categories

    def get_file_diff_summary(self, file_path: str) -> str:
        """
        Get a short summary of changes for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Summary of changes
        """
        try:
            result = subprocess.run(
                ["git", "diff", "--staged", "--", file_path],
                capture_output=True,
                text=True,
                check=True,
                encoding=DEFAULT_ENCODING
            )
            diff_lines = result.stdout.strip().splitlines()
            if not diff_lines:
                return "No diff available."
            
            # Limit to first 5 lines and escape properly
            summary_lines = diff_lines[:5]
            return "\n    ".join(summary_lines)
        except subprocess.CalledProcessError as e:
            logger.warning(f"Could not retrieve diff for {file_path}: {e}")
            return "Could not retrieve diff."

    def generate_commit_message(self, group_name, category_name, files):
        """Generate a professional conventional commit style message."""
        type_map = {
            "Added": "feat",
            "Modified": "fix",
            "Deleted": "remove",
            "Renamed": "refactor",
            "Copied": "chore",
            "Updated but unmerged": "conflict",
            "Untracked": "docs",
            "Ignored": "chore",
            "Added and Modified": "feat",
            "Deleted and Modified": "fix",
            "Renamed and Modified": "refactor",
            "Copied and Modified": "chore",
            "Unmerged": "conflict",
            "Type Changed": "refactor",
            "Unknown": "chore",
            "Other": "chore",
            "Conflicted": "conflict",
            "Staged": "chore",
            "Unstaged": "chore",
            "Both Modified": "fix",
        }
        emoji_map = {
            "feat": "✨",
            "fix": "🐛",
            "remove": "🗑️",
            "refactor": "♻️",
            "chore": "🔧",
            "conflict": "⚠️",
            "docs": "📝",
        }
        commit_type = type_map.get(category_name, "chore")
        emoji = emoji_map.get(commit_type, "")
        scope = group_name if group_name != "root" else ""
        subject = f"{emoji} {commit_type}"
        if scope:
            subject += f"({scope})"
        subject += f": {category_name} files updated"

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        body = f"Changes included (as of {timestamp}):\\n"
        for f in files:
            desc = {
                "Added": "This file was newly added to the project and is now tracked.",
                "Modified": "This file was modified with updates or fixes.",
                "Deleted": "This file was removed from the project.",
                "Renamed": "This file was renamed or moved to a different location.",
                "Copied": "This file was copied from another file.",
                "Updated but unmerged": "This file has merge conflicts that need to be resolved.",
                "Untracked": "This file is new and not yet tracked by git.",
                "Ignored": "This file is ignored by git.",
                "Added and Modified": "This file was added and then modified before committing.",
                "Deleted and Modified": "This file was deleted and modified before committing.",
                "Renamed and Modified": "This file was renamed and modified before committing.",
                "Copied and Modified": "This file was copied and modified before committing.",
                "Unmerged": "This file has unmerged changes.",
                "Type Changed": "The file type has changed.",
                "Unknown": "This file has an unknown change status.",
                "Other": "This file has other types of changes.",
                "Conflicted": "This file has conflicts that need to be resolved.",
                "Staged": "This file is staged for commit.",
                "Unstaged": "This file has unstaged changes.",
                "Both Modified": "This file was modified in both the index and working tree.",
            }.get(category_name, "")
            diff_summary = self.get_file_diff_summary(f)
            body += f"- {f}: {desc}\\n  Summary:\\n    {diff_summary}\\n"

        footer = "\\nPlease describe the reason or issue addressed by these changes."

        message = f"{subject}\\n\\n{body}\\n{footer}"
        return message

    def load_linked_wbs_resources(self, filepath: str = "JSonDataBase/Inputs/UserInputs/linked_wbs_resources.json") -> List[Dict[str, Any]]:
        """
        Load linked WBS (Work Breakdown Structure) resources from JSON file.
        
        This method loads the project task structure that links files to specific
        project tasks, enabling intelligent commit messages and progress tracking.
        
        Args:
            filepath: Path to the linked WBS resources JSON file
            
        Returns:
            List of task dictionaries with hierarchical structure
            
        Example:
            >>> tasks = auto_commit.load_linked_wbs_resources()
            >>> print(tasks[0]['id'])
            'task-001'
        """
        if not os.path.exists(filepath):
            logger.warning(f"Linked WBS resources file not found: {filepath}")
            return []
        
        try:
            with open(filepath, 'r', encoding=DEFAULT_ENCODING) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse WBS resources file: {e}")
            return []

    def find_task_by_file_path(self, linked_wbs: List[Dict[str, Any]], file_path: str) -> Optional[Dict[str, Any]]:
        """
        Find the task in linked WBS resources that corresponds to the given file path.
        
        This method searches through the hierarchical task structure to find
        which project task a specific file belongs to, enabling task-based
        commit categorization and progress tracking.
        
        Args:
            linked_wbs: List of task dictionaries from WBS resources
            file_path: Path to the file being committed
            
        Returns:
            Task dictionary if found, None otherwise
            
        Example:
            >>> task = auto_commit.find_task_by_file_path(wbs_tasks, 'src/main.py')
            >>> if task:
            ...     print(task['name'])
            'Main Application Development'
        """
        for task in linked_wbs:
            found = self.search_task_recursive(task, file_path)
            if found:
                return found
        return None

    def search_task_recursive(self, task: Dict[str, Any], file_path: str) -> Optional[Dict[str, Any]]:
        """
        Recursively search for a task that matches the given file path.
        
        This helper method traverses the task hierarchy (including subtasks)
        to find a task whose ID appears in the file path, establishing the
        relationship between files and project tasks.
        
        Args:
            task: Current task dictionary to examine
            file_path: File path to match against task IDs
            
        Returns:
            Task dictionary if match found, None otherwise
            
        Note:
            This is a basic implementation that matches task IDs in file paths.
            For more sophisticated matching, consider using path patterns or
            file extension mappings.
        """
        if task.get("id") and task.get("id") in file_path:
            return task
        
        for subtask in task.get("subtasks", []):
            found = self.search_task_recursive(subtask, file_path)
            if found:
                return found
        return None

    def backup(self) -> str:
        """
        Create a backup of user input JSON files before committing changes.
        
        This method ensures data integrity by creating backups of critical
        project configuration files before any git operations are performed.
        
        Returns:
            Path to the backup directory
            
        Raises:
            SystemExit: If backup creation fails
            
        Example:
            >>> backup_path = auto_commit.backup()
            >>> print(f"Backup created at: {backup_path}")
            '/tmp/autoproject_backup_20241220_143022'
        """
        logger.info("Running backup of user input JSON files before commit...")
        backup_dir = self.bm.create_backup()
        
        if backup_dir is None:
            logger.error("Backup failed. Aborting commit.")
            raise SystemExit("Backup creation failed")
        
        logger.info(f"Backup successful: {backup_dir}")
        return backup_dir

    def map_group_to_workflow_stage(self, group_name):
        mapping = {
            "requirements": "Requirements Gathering",
            "design": "Design",
            "implementation": "Implementation",
            "code_review": "Code Review",
            "testing": "Testing",
            "deployment": "Deployment",
            "maintenance": "Maintenance"
        }
        key = group_name.lower()
        return mapping.get(key, "Implementation")

    def calculate_progress_change(self, workflow_stage, total_commits_in_stage):
        stage_weights = {
            "Requirements Gathering": 0.15,
            "Design": 0.15,
            "Implementation": 0.30,
            "Code Review": 0.10,
            "Testing": 0.15,
            "Deployment": 0.10,
            "Maintenance": 0.05
        }
        weight = stage_weights.get(workflow_stage, 0.0)
        if total_commits_in_stage <= 0:
            return 0.0
        progress_per_commit = weight / total_commits_in_stage
        return min(progress_per_commit, 0.05)

    def calculate_importance(self, task_id, workflow_stage, dependencies, progress, delays):
        stage_weights = {
            "Requirements Gathering": 0.15,
            "Design": 0.15,
            "Implementation": 0.30,
            "Code Review": 0.10,
            "Testing": 0.15,
            "Deployment": 0.10,
            "Maintenance": 0.05
        }
        base_importance = stage_weights.get(workflow_stage, 0.1)
        dependency_factor = min(len(dependencies) * 0.05, 0.3)
        progress_factor = max(0, 1 - progress)
        delay_factor = min(delays * 0.1, 0.3)
        importance = base_importance + dependency_factor + progress_factor + delay_factor
        importance = min(max(importance, 0), 1)
        return round(importance, 3)

    def calculate_urgency(self, deadline, current_time, delays, progress):
        if not deadline:
            return 0.0
        remaining_time = (deadline - current_time).total_seconds() / (3600 * 24)
        if remaining_time < 0:
            return 1.0
        max_days = 30
        time_factor = max(0, min(1, (max_days - remaining_time) / max_days))
        delay_factor = min(delays * 0.1, 0.5)
        progress_factor = max(0, 1 - progress)
        urgency = time_factor + delay_factor + progress_factor
        urgency = min(max(urgency, 0), 1)
        return round(urgency, 3)

    def update_commit_task_database(self, commit_hash, task_id, file_path, commit_message, workflow_stage=None, progress_change=0.0, importance_change=0, priority_change=0, db_path="JSonDataBase/OutPuts/commit_task_database.json"):
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                db = json.load(f)
        except FileNotFoundError:
            db = {}

        dir_path = os.path.dirname(db_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        success_author, author = self.run_git_command(["log", "-1", "--pretty=format:%an", commit_hash])
        success_email, email = self.run_git_command(["log", "-1", "--pretty=format:%ae", commit_hash])
        success_date, date = self.run_git_command(["log", "-1", "--pretty=format:%ad", commit_hash])
        success_branch, branch = self.run_git_command(["branch", "--contains", commit_hash])
        success_parents, parents = self.run_git_command(["log", "-1", "--pretty=format:%P", commit_hash])

        import time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        db[commit_hash] = {
            "task_id": task_id,
            "file_path": file_path,
            "commit_message": commit_message,
            "workflow_stage": workflow_stage if workflow_stage else "",
            "progress_change": round(progress_change, 3),
            "importance_change": importance_change,
            "priority_change": priority_change,
            "timestamp": timestamp,
            "author": author if success_author else "",
            "email": email if success_email else "",
            "date": date if success_date else "",
            "branch": branch.strip() if success_branch else "",
            "parent_commits": parents.split() if success_parents else []
        }

        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4, ensure_ascii=False)

    def collect_commit_progress(self):
        changes = self.get_git_changes()
        if not changes or (len(changes) == 1 and changes[0] == ''):
            print("No changes detected.")
            return {}

        grouped_files = self.group_related_files(changes)
        progress_data = {}

        for group_name, files in grouped_files.items():
            categories = self.categorize_files(files)
            progress_data[group_name] = {}

            for category_name, category_files in categories.items():
                if not category_files:
                    continue

                commit_messages = []
                for f in category_files:
                    commit_message = self.generate_commit_message(group_name, category_name, [f])
                    commit_messages.append({
                        "file": f,
                        "commit_message": commit_message
                    })

                progress_data[group_name][category_name] = {
                    "files": category_files,
                    "commit_messages": commit_messages
                }

        return progress_data

    def write_commit_progress_to_json(self, file_path="JSonDataBase/OutPuts/commit_progress.json"):
        progress_data = self.collect_commit_progress()
        if not progress_data:
            print("No commit progress data to write.")
            return

        simplified_progress = {}
        for group_name, categories in progress_data.items():
            total_files = 0
            committed_files = 0
            for category_name, data in categories.items():
                files = data.get("files", [])
                total_files += len(files)
                if category_name in ["Added", "Modified", "Renamed"]:
                    committed_files += len(files)
            if total_files > 0:
                progress_ratio = committed_files / total_files
            else:
                progress_ratio = 0.0
            simplified_progress[group_name] = round(progress_ratio, 2)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(simplified_progress, f, indent=4, ensure_ascii=False)
            print(f"Commit progress data written to {file_path}")
        except Exception as e:
            print(f"Failed to write commit progress data to {file_path}: {e}")


    def commit_and_push(self):
        linked_wbs = self.load_linked_wbs_resources()
        changes = self.get_git_changes()
        if not changes or (len(changes) == 1 and changes[0] == ''):
            print("No changes detected.")
            return

        grouped_files = self.group_related_files(changes)

        for group_name, files in grouped_files.items():
            categories = self.categorize_files(files)

            total_commits_in_group = sum(len(files) for files in categories.values())

            workflow_stage = self.map_group_to_workflow_stage(group_name)

            for category_name, category_files in categories.items():
                if not category_files:
                    continue

                for f in category_files:
                    success, _ = self.run_git_command(["add", f])
                    if not success:
                        print(f"Failed to stage file {f} for {group_name} - {category_name}. Skipping commit.")
                        continue

                    commit_message = self.generate_commit_message(group_name, category_name, [f])

                    success, _ = self.run_git_command(["commit", "-m", commit_message])
                    if not success:
                        print(f"Failed to commit file {f} for {group_name} - {category_name}. Skipping push.")
                        continue

                    success_hash, commit_hash = self.run_git_command(["rev-parse", "HEAD"])
                    if not success_hash:
                        print(f"Failed to get commit hash for file {f} in {group_name} - {category_name}.")
                        continue

                    progress_change = self.calculate_progress_change(workflow_stage, total_commits_in_group)

                    task = self.find_task_by_file_path(linked_wbs, f)
                    if task:
                        dependencies = task.get("predecessors", [])
                        progress = 0.0
                        delays = 0
                        deadline_str = None
                        allocations = task.get("allocations", [])
                        if allocations:
                            start_dates = [alloc.get("start_date") for alloc in allocations if alloc.get("start_date")]
                            end_dates = [alloc.get("end_date") for alloc in allocations if alloc.get("end_date")]
                            if end_dates:
                                deadline_str = max(end_dates)
                        if deadline_str:
                            try:
                                deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d")
                            except ValueError:
                                deadline = None
                        else:
                            deadline = None
                    else:
                        dependencies = []
                        progress = 0.0
                        delays = 0
                        deadline = None

                    current_time = datetime.datetime.now()

                    importance_change = self.calculate_importance(group_name, workflow_stage, dependencies, progress, delays)
                    priority_change = self.calculate_urgency(deadline, current_time, delays, progress)

                    self.update_commit_task_database(commit_hash, group_name, f, commit_message, workflow_stage, progress_change, importance_change, priority_change)

                    success, output = self.run_git_command(["push", "--set-upstream", "origin", "main"])
                    if not success:
                        print(f"Failed to push commit for file {f} in {group_name} - {category_name}. Error: {output}")
                        continue

                    print(f"Committed and pushed changes for file: {f} in group: {group_name} - {category_name}")

        self.write_commit_progress_to_json()

if __name__ == "__main__":
    auto_commit = AutoCommit()
    auto_commit.backup()
    auto_commit.commit_and_push()
