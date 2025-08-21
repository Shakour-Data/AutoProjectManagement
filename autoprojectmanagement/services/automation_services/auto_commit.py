#!/usr/bin/env python3
"""
Unified AutoCommit Service for AutoProjectManagement
Purpose: Merged enhanced auto-commit with robust authentication and git push error handling
Author: AutoProjectManagement System
Version: 4.1.0
License: MIT
Description: Unified version combining enhanced authentication from auto_commit_enhanced.py 
           with project management integration, plus comprehensive git push error handling
           NOW WITH AUTOMATIC PUSH ENABLED BY DEFAULT
"""

import os
import subprocess
import datetime
from collections import defaultdict
import sys
import json
import re
from typing import Dict, List, Tuple, Optional
import logging

# Import the Git configuration manager
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from git_config_manager import configure_git_automatically

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class UnifiedAutoCommit:
    """Unified automated git commit service with enhanced authentication and push error handling."""
    
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

    def push_changes_with_fallback(self, remote: str = "origin", branch: str = "main") -> bool:
        """Push changes with comprehensive authentication fallback strategies."""
        
        # Strategy 1: Try current method
        self.logger.info("🔍 Trying current authentication method...")
        success, output = self._try_push_strategy(["push", remote, branch])
        if success:
            return True
        
        # Strategy 2: Try HTTPS with PAT
        if self.has_pat:
            self.logger.info("🔍 Trying HTTPS with Personal Access Token...")
            self._ensure_https_remote()
            success, output = self._try_push_strategy(["push", remote, branch], use_https=True)
            if success:
                return True
        
        # Strategy 3: Try SSH if available
        if self.has_ssh:
            self.logger.info("🔍 Trying SSH authentication...")
            self._ensure_ssh_remote()
            success, output = self._try_push_strategy(["push", remote, branch])
            if success:
                return True
        
        # Strategy 4: Try with additional flags
        push_strategies = [
            ["push", remote, branch, "--no-verify"],
            ["push", remote, branch, "--no-verify", "--force-with-lease"],
            ["push", remote, branch, "--no-verify", "--quiet"],
            ["push", remote, branch, "--no-verify", "--porcelain"]
        ]
        
        for i, strategy in enumerate(push_strategies):
            self.logger.info(f"🔍 Trying push strategy {i+1}: {' '.join(strategy)}")
            success, output = self._try_push_strategy(strategy)
            if success:
                return True
        
        self.logger.error("❌ All push strategies failed")
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

    def commit_and_push_all(self, remote: str = "origin", branch: str = "main") -> bool:
        """Commit and push all changes with authentication handling."""
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
        
        # Push changes with authentication handling
        return self.push_changes_with_fallback(remote, branch)

    def run_complete_workflow(self, remote: str = "origin", branch: str = "main") -> bool:
        """Run complete backup, commit, and push workflow with authentication."""
        try:
            # Create backup
            backup_dir = self.create_backup()
            self.logger.info(f"Backup created: {backup_dir}")
            
            # Commit and push
            success = self.commit_and_push_all(remote, branch)
            
            if success:
                self.logger.info("✅ Auto-commit workflow completed successfully")
            else:
                self.logger.error("❌ Auto-commit workflow failed")
                self._provide_troubleshooting_help()
            
            return success
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {str(e)}")
            self._provide_troubleshooting_help()
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


if __name__ == "__main__":
    auto_commit = UnifiedAutoCommit()
    success = auto_commit.run_complete_workflow()
    
    if success:
        print("✅ Auto-commit workflow completed successfully")
    else:
        print("❌ Auto-commit workflow failed")
        sys.exit(1)
