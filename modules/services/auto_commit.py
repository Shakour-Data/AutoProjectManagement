import os
import subprocess
import datetime
from collections import defaultdict
import sys
import os
import re
# from project_management.modules.services.backup_manager import BackupManager
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

def format_commit_message(message):
    """
    Format a commit message by cleaning and normalizing it.
    
    Args:
        message (str): The raw commit message
        
    Returns:
        str: The formatted commit message
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
    
    # Remove literal escape sequences like \n, \t, \r (but not other backslashes)
    # Use word boundaries to avoid partial matches
    message = re.sub(r'\\n(?=\s|$)', ' ', message)  # newline followed by space or end of string
    message = re.sub(r'\\t(?=\s|$)', ' ', message)  # tab followed by space or end of string
    message = re.sub(r'\\r(?=\s|$)', ' ', message)  # carriage return followed by space or end of string
    # Remove extra spaces that may have been created
    message = re.sub(r'\s+', ' ', message).strip()
    
    # Limit message length to 255 characters
    if len(message) > 255:
        message = message[:255]
    
    return message

class AutoCommit:
    def __init__(self):
        from project_management.modules.services.backup_manager import BackupManager
        self.bm = BackupManager()

    def run_git_command(self, args, cwd=None):
        """Run a git command and return (success, output)."""
        try:
            # Use UTF-8 encoding to avoid UnicodeDecodeError
            result = subprocess.run(["git"] + args, capture_output=True, text=True, check=True, cwd=cwd, encoding='utf-8', errors='ignore')
            if result.stdout is None:
                return True, ""
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: git {' '.join(args)}")
            print(f"Error: {e.stderr.strip()}")
            return False, e.stderr.strip()

    def get_git_changes(self):
        """Fetch Git status and return list of changes."""
        success, output = self.run_git_command(["status", "--short"])
        if not success:
            return []
        return output.splitlines()

    def group_related_files(self, changes):
        """Group files based on top-level directory (code relationship)."""
        groups = defaultdict(list)

        for change in changes:
            if not change:
                continue
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
                    old_path = parts[0].strip()
                    new_path = parts[1].strip()
                    file_path = new_path
                else:
                    file_path = file_path.strip()

            parts = file_path.split(os.sep)
            if len(parts) > 1:
                top_level_dir = parts[0]
            else:
                top_level_dir = "root"

            groups[top_level_dir].append((status, file_path))

        return groups

    def categorize_files(self, files):
        """Categorize files into different change types."""
        categories = defaultdict(list)

        for status, file in files:
            if status == "A":
                categories["Added"].append(file)
            elif status == "M":
                categories["Modified"].append(file)
            elif status == "D":
                categories["Deleted"].append(file)
            elif status == "R":
                categories["Renamed"].append(file)
            elif status == "??":
                categories["Untracked"].append(file)
            else:
                categories["Other"].append(file)

        return categories

    def get_file_diff_summary(self, file_path):
        """Get a short summary of changes for a file."""  
        try:
            result = subprocess.run(
                ["git", "diff", "--staged", "--", file_path],
                capture_output=True,
                text=True,
                check=True,
            )
            if result.stdout is None:
                return "No diff available."
            diff_lines = result.stdout.strip().splitlines()
            summary = "\\n    ".join(diff_lines[:5]) if diff_lines else "No diff available."
            return summary
        except subprocess.CalledProcessError:
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

    def load_linked_wbs_resources(self, filepath="JSonDataBase/Inputs/UserInputs/linked_wbs_resources.json"):
        if not os.path.exists(filepath):
            print(f"Linked WBS resources file not found: {filepath}")
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def find_task_by_file_path(self, linked_wbs, file_path):
        """
        Find the task in linked Wbs resources that corresponds to the given file path.
        This is a placeholder function and should be customized based on actual file-task mapping.
        """
        for task in linked_wbs:
            found = self.search_task_recursive(task, file_path)
            if found:
                return found
        return None

    def search_task_recursive(self, task, file_path):
        if task.get("id") and task.get("id") in file_path:
            return task
        for subtask in task.get("subtasks", []):
            found = self.search_task_recursive(subtask, file_path)
            if found:
                return found
        return None

    def backup(self):
        print("Running backup of user input JSON files before commit...")
        backup_dir = self.bm.create_backup()
        if backup_dir is None:
            print("Backup failed. Aborting commit.")
            exit(1)
        else:
            print(f"Backup successful: {backup_dir}")

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
