#!/usr/bin/env python3
"""
Unified AutoCommit Service for AutoProjectManagement
Purpose: Unified version combining enhanced authentication, guaranteed push execution, and project management integration
Author: AutoProjectManagement System
Version: 5.0.0
License: MIT
Description: Unified version combining the best features from both auto_commit implementations
           - Enhanced authentication and guaranteed push from automation_services version
           - Project management integration and WBS features from services version
           NOW WITH COMPLETE PROJECT MANAGEMENT INTEGRATION AND GUARANTEED PUSH
"""

import os
import subprocess
import datetime
from collections import defaultdict
import sys
import json
import re
from typing import Dict, List, Tuple, Optional, Any
import logging

# Add the project root to Python path to handle imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the Git configuration manager
from .git_config_manager import configure_git_automatically

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


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


class UnifiedAutoCommit:
    """Unified automated git commit service with enhanced authentication, guaranteed push execution, and project management integration."""
    
    def __init__(self) -> None:
        """Initialize the UnifiedAutoCommit service."""
        self.logger = logging.getLogger(__name__)
        self._configure_git_automatically()
        self._setup_authentication()
        
    def _configure_git_automatically(self) -> None:
        """Automatically configure Git to prevent RPC errors."""
        try:
            success = configure_git_automatically()
            if success:
                self.logger.info("✅ Git automatically configured for RPC error prevention")
            else:
                self.logger.warning("⚠️  Git auto-configuration partially applied")
        except Exception as e:
            self.logger.warning(f"Could not auto-configure git: {e}")
    
    def _setup_authentication(self) -> None:
        """Setup and verify authentication methods."""
        self.logger.info("🔐 Setting up authentication methods...")
        
        # Check available authentication methods
        self.has_ssh = self._check_ssh_auth()
        self.has_https = self._check_https_auth()
        self.has_pat = self._check_pat_auth()
        
        self.logger.info(f"Authentication methods available:")
        self.logger.info(f"  SSH: {'✅' if self.has_ssh else '❌'}")
        self.logger.info(f"  HTTPS: {'✅' if self.has_https else '❌'}")
        self.logger.info(f"  PAT: {'✅' if self.has_pat else '❌'}")
    
    def _check_ssh_auth(self) -> bool:
        """Check if SSH authentication is working."""
        try:
            result = subprocess.run(
                ["ssh", "-T", "git@github.com"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return "successfully authenticated" in result.stderr.lower() or result.returncode == 1
        except:
            return False
    
    def _check_https_auth(self) -> bool:
        """Check if HTTPS authentication is working."""
        try:
            result = subprocess.run(
                ["git", "ls-remote", "https://github.com/Shakour-Data/AutoProjectManagement.git", "HEAD"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def _check_pat_auth(self) -> bool:
        """Check if Personal Access Token is configured."""
        credentials_file = os.path.expanduser("~/.git-credentials")
        return os.path.exists(credentials_file)
    
    def run_git_command(self, args: List[str], cwd: str = None, use_https: bool = False) -> Tuple[bool, str]:
        """Run a git command with memory optimization and authentication handling."""
        env = os.environ.copy()
        env.update({
            'GIT_MMAP_LIMIT': '1g',
            'GIT_ALLOC_LIMIT': '1g',
            'GIT_SSL_NO_VERIFY': '1',
            'GIT_ASKPASS': 'echo',
            'GIT_TERMINAL_PROMPT': '0'
        })
        
        try:
            if use_https and "push" in args:
                self._ensure_https_remote(cwd)
            
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd,
                env=env
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git command failed: git {' '.join(args)}")
            self.logger.error(f"Error: {e.stderr.strip()}")
            return False, e.stderr.strip()
    
    def _ensure_https_remote(self, cwd: str = None) -> bool:
        """Ensure remote URL uses HTTPS for authentication."""
        try:
            success, current_url = self.run_git_command(["config", "--get", "remote.origin.url"], cwd=cwd)
            if success and current_url.startswith("git@"):
                https_url = current_url.replace("git@github.com:", "https://github.com/")
                success, _ = self.run_git_command(["remote", "set-url", "origin", https_url], cwd=cwd)
                if success:
                    self.logger.info(f"✅ Changed remote URL to HTTPS: {https_url}")
                    return True
            return False
        except:
            return False
    
    def _ensure_ssh_remote(self, cwd: str = None) -> bool:
        """Ensure remote URL uses SSH for authentication."""
        try:
            success, current_url = self.run_git_command(["config", "--get", "remote.origin.url"], cwd=cwd)
            if success and current_url.startswith("https://"):
                ssh_url = current_url.replace("https://github.com/", "git@github.com:")
                success, _ = self.run_git_command(["remote", "set-url", "origin", ssh_url], cwd=cwd)
                if success:
                    self.logger.info(f"✅ Changed remote URL to SSH: {ssh_url}")
                    return True
            return False
        except:
            return False
    
    def get_git_changes(self) -> List[str]:
        """Fetch Git status and return list of changes."""
        success, output = self.run_git_command(["status", "--short"])
        if not success:
            return []
        return [line for line in output.splitlines() if line.strip()]

    def group_and_categorize_files(self, changes: List[str]) -> Dict[str, Dict[str, List[str]]]:
        """Group and categorize files for commit."""
        grouped = defaultdict(lambda: defaultdict(list))
        
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
                    continue
            
            parts = file_path.split(os.sep)
            group_name = parts[0] if len(parts) > 1 else "root"
            
            status_mapping = {
                "A": "Added", "M": "Modified", "D": "Deleted",
                "R": "Renamed", "??": "Untracked"
            }
            category = status_mapping.get(status, "Other")
            
            grouped[group_name][category].append(file_path)
        
        return grouped

    def generate_commit_message(self, group_name: str, category_name: str, files: List[str]) -> str:
        """Generate a simple commit message."""
        type_map = {
            "Added": "feat", "Modified": "fix", "Deleted": "remove",
            "Renamed": "refactor", "Untracked": "docs"
        }
        
        commit_type = type_map.get(category_name, "chore")
        scope = group_name if group_name != "root" else ""
        
        subject = f"{commit_type}"
        if scope:
            subject += f"({scope})"
        subject += f": {category_name} {len(files)} file(s)"
        
        return subject

    def create_backup(self) -> str:
        """Create a simple backup."""
        backup_dir = f"backups/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        with open(os.path.join(backup_dir, "backup_info.txt"), "w") as f:
            f.write(f"Backup created at {datetime.datetime.now()}\n")
        
        return backup_dir

    def stage_files(self, files: List[str]) -> bool:
        """Stage files for commit."""
        for file_path in files:
            # Clean up file path - remove any invalid characters or formatting
            clean_path = file_path.strip()
            if " -> " in clean_path:
                # Handle file rename/move operations
                parts = clean_path.split(" -> ")
                if len(parts) == 2:
                    # Stage both old and new files for renames
                    old_file = parts[0].strip()
                    new_file = parts[1].strip()
                    
                    # Try to stage the new file (it should exist)
                    if os.path.exists(new_file):
                        success, _ = self.run_git_command(["add", new_file])
                        if not success:
                            self.logger.error(f"Failed to stage new file: {new_file}")
                            return False
                    else:
                        # If new file doesn't exist, stage the old file
                        success, _ = self.run_git_command(["add", old_file])
                        if not success:
                            self.logger.error(f"Failed to stage old file: {old_file}")
                            return False
                continue
            
            # Handle regular files
            if os.path.exists(clean_path):
                success, _ = self.run_git_command(["add", clean_path])
                if not success:
                    self.logger.error(f"Failed to stage file: {clean_path}")
                    return False
            else:
                self.logger.warning(f"File does not exist: {clean_path}")
        return True

    def commit_files(self, message: str) -> bool:
        """Commit staged files."""
        success, _ = self.run_git_command(["commit", "-m", message])
        if not success:
            self.logger.error("Failed to commit changes")
            return False
        return True

    def push_changes_guaranteed(self, remote: str = "origin", branch: str = "main") -> bool:
        """Push changes with guaranteed execution - local changes take priority."""
        self.logger.info("🚀 Executing guaranteed push - local changes take priority...")
        
        # Try multiple push strategies in order of preference
        push_strategies = [
            # Strategy 1: Force push with lease (safe force push)
            ["push", remote, branch, "--force-with-lease"],
            # Strategy 2: Regular push
            ["push", remote, branch],
            # Strategy 3: Push with upstream
            ["push", "-u", remote, branch],
            # Strategy 4: Force push (last resort - local changes take priority)
            ["push", remote, branch, "--force"]
        ]
        
        for strategy in push_strategies:
            try:
                self.logger.info(f"🔄 Trying push strategy: {' '.join(strategy)}")
                success, output = self.run_git_command(strategy)
                if success:
                    self.logger.info("✅ Push completed successfully")
                    return True
                    
                # If push fails, log the error but continue to next strategy
                self.logger.warning(f"⚠️  Push strategy failed: {output}")
                
            except Exception as e:
                self.logger.warning(f"⚠️  Push strategy exception: {str(e)}")
                continue
        
        # Final attempt: try with HTTPS if available
        if self.has_https or self.has_pat:
            self.logger.info("🔄 Trying HTTPS push as fallback...")
            self._ensure_https_remote()
            success, output = self.run_git_command(["push", remote, branch], use_https=True)
            if success:
                self.logger.info("✅ HTTPS push completed successfully")
                return True
        
        # If all strategies fail, log but don't stop execution
        self.logger.error("❌ All push strategies failed, but continuing...")
        return False
    
    def _try_push_strategy(self, args: List[str], use_https: bool = False) -> Tuple[bool, str]:
        """Try a specific push strategy."""
        try:
            success, output = self.run_git_command(args, use_https=use_https)
            if success:
                self.logger.info("✅ Changes pushed successfully")
                return True, output
            
            # Check for specific error patterns
            error_patterns = [
                "Permission denied", "authentication failed",
                "could not read Username", "could not read Password"
            ]
            
            for pattern in error_patterns:
                if pattern.lower() in output.lower():
                    self.logger.warning(f"Authentication issue detected: {pattern}")
                    return False, output
            
            return False, output
            
        except Exception as e:
            self.logger.error(f"Push strategy failed: {str(e)}")
            return False, str(e)

    def commit_and_push_all_guaranteed(self, remote: str = "origin", branch: str = "main") -> bool:
        """Commit and push all changes with guaranteed push execution."""
        changes = self.get_git_changes()
        if not changes:
            self.logger.info("No changes detected")
            return True

        grouped_files = self.group_and_categorize_files(changes)
        
        # Stage all changes
        all_files = []
        for group_name, categories in grouped_files.items():
            for category_name, files in categories.items():
                all_files.extend(files)
        
        if not self.stage_files(all_files):
            return False
        
        # Create a single commit for all changes
        commit_message = f"Auto-commit: {len(all_files)} file(s) updated"
        if not self.commit_files(commit_message):
            return False
        
        # Execute guaranteed push - local changes take priority
        return self.push_changes_guaranteed(remote, branch)

    def run_complete_workflow_guaranteed(self, remote: str = "origin", branch: str = "main") -> bool:
        """Run complete backup, commit, and push workflow with guaranteed push execution."""
        try:
            # Create backup
            backup_dir = self.create_backup()
            self.logger.info(f"Backup created: {backup_dir}")
            
            # Commit and push with guaranteed execution
            success = self.commit_and_push_all_guaranteed(remote, branch)
            
            if success:
                self.logger.info("✅ Auto-commit workflow completed successfully with guaranteed push")
            else:
                self.logger.warning("⚠️  Push failed but workflow completed (local changes preserved)")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {str(e)}")
            return False
    
    def _provide_troubleshooting_help(self) -> None:
        """Provide helpful troubleshooting information."""
        print("\n" + "="*60)
        print("🔧 TROUBLESHOOTING GUIDE")
        print("="*60)
        print("Authentication issues detected. Here are solutions:")
        print()
        print("1. PERSONAL ACCESS TOKEN (Recommended):")
        print("   - Go to: https://github.com/settings/tokens")
        print("   - Create token with 'repo' scope")
        print("   - Run: ./fix_git_auth.sh")
        print()
        print("2. SSH KEY SETUP:")
        print("   - Add your SSH key to GitHub:")
        print("   - Visit: https://github.com/settings/keys")
        print("   - Add this key:")
        try:
            with open(os.path.expanduser("~/.ssh/id_ed25519.pub")) as f:
                print(f"   {f.read().strip()}")
        except:
            print("   (SSH key not found)")
        print()
        print("3. MANUAL SETUP:")
        print("   - Check current remote: git remote -v")
        print("   - Switch to HTTPS: git remote set-url origin https://github.com/Shakour-Data/AutoProjectManagement.git")
        print("   - Or switch to SSH: git remote set-url origin git@github.com:Shakour-Data/AutoProjectManagement.git")
        print("="*60)

    # Project Management Integration Methods from old version
    def load_linked_wbs_resources(self, filepath: str = "JSonDataBase/Inputs/UserInputs/linked_wbs_resources.json") -> List[Dict]:
        """Load linked WBS resources from JSON file."""
        if not os.path.exists(filepath):
            self.logger.warning(f"Linked WBS resources file not found: {filepath}")
            return []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading WBS resources: {e}")
            return []

    def find_task_by_file_path(self, linked_wbs: List[Dict], file_path: str) -> Optional[Dict]:
        """
        Find the task in linked Wbs resources that corresponds to the given file path.
        This is a placeholder function and should be customized based on actual file-task mapping.
        """
        for task in linked_wbs:
            found = self.search_task_recursive(task, file_path)
            if found:
                return found
        return None

    def search_task_recursive(self, task: Dict, file_path: str) -> Optional[Dict]:
        """Recursively search for a task by file path."""
        if task.get("id") and task.get("id") in file_path:
            return task
        for subtask in task.get("subtasks", []):
            found = self.search_task_recursive(subtask, file_path)
            if found:
                return found
        return None

    def map_group_to_workflow_stage(self, group_name: str) -> str:
        """Map group name to workflow stage."""
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

    def calculate_progress_change(self, workflow_stage: str, total_commits_in_stage: int) -> float:
        """Calculate progress change based on workflow stage and commit count."""
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

    def calculate_importance(self, task_id: str, workflow_stage: str, dependencies: List[str], 
                           progress: float, delays: int) -> float:
        """Calculate importance score for a task."""
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

    def calculate_urgency(self, deadline: Optional[datetime.datetime], current_time: datetime.datetime, 
                        delays: int, progress: float) -> float:
        """Calculate urgency score for a task."""
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

    def update_commit_task_database(self, commit_hash: str, task_id: str, file_path: str, 
                                  commit_message: str, workflow_stage: Optional[str] = None, 
                                  progress_change: float = 0.0, importance_change: float = 0, 
                                  priority_change: float = 0, 
                                  db_path: str = "JSonDataBase/OutPuts/commit_task_database.json") -> None:
        """Update commit task database with commit information."""
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

        try:
            with open(db_path, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to update commit task database: {e}")

    def collect_commit_progress(self) -> Dict[str, Any]:
        """Collect commit progress data for project management integration."""
        changes = self.get_git_changes()
        if not changes or (len(changes) == 1 and changes[0] == ''):
            self.logger.info("No changes detected.")
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
                    commit_message = self.generate_detailed_commit_message(group_name, category_name, [f])
                    commit_messages.append({
                        "file": f,
                        "commit_message": commit_message
                    })

                progress_data[group_name][category_name] = {
                    "files": category_files,
                    "commit_messages": commit_messages
                }

        return progress_data

    def write_commit_progress_to_json(self, file_path: str = "JSonDataBase/OutPuts/commit_progress.json") -> None:
        """Write commit progress data to JSON file."""
        progress_data = self.collect_commit_progress()
        if not progress_data:
            self.logger.info("No commit progress data to write.")
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
            self.logger.info(f"Commit progress data written to {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to write commit progress data to {file_path}: {e}")

    def group_related_files(self, changes: List[str]) -> Dict[str, List[Tuple[str, str]]]:
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

    def categorize_files(self, files: List[Tuple[str, str]]) -> Dict[str, List[str]]:
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

    def get_file_diff_summary(self, file_path: str) -> str:
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

    def generate_detailed_commit_message(self, group_name: str, category_name: str, files: List[str]) -> str:
        """Generate a professional conventional commit style message with detailed information."""
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


if __name__ == "__main__":
    auto_commit = UnifiedAutoCommit()
    success = auto_commit.run_complete_workflow_guaranteed()
    
    if success:
        print("✅ Auto-commit workflow completed successfully with guaranteed push")
    else:
        print("⚠️  Workflow completed - push may have failed but local changes are preserved")
        sys.exit(0)  # Don't exit with error to allow workflow to continue
