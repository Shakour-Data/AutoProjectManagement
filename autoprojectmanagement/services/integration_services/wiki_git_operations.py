#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: wiki_git_operations
File: wiki_git_operations.py
Path: autoprojectmanagement/services/integration_services/wiki_git_operations.py

Description:
    Wiki Git Operations module

Author: AutoProjectManagement Team
Contact: team@autoprojectmanagement.com
Repository: https://github.com/autoprojectmanagement/autoprojectmanagement

Version Information:
    Current Version: 1.0.0
    Last Updated: 2025-08-14
    Python Version: 3.8+
    
Development Status:
    Status: Production/Stable
    Created: 2024-01-01
    Last Modified: 2025-08-14
    Modified By: AutoProjectManagement Team

Dependencies:
    - Python 3.8+
    - See requirements.txt for full dependency list

License: MIT License
Copyright: (c) 2024 AutoProjectManagement Team

Usage:
    This module is part of the AutoProjectManagement package.
    Import and use as needed within the package ecosystem.

Example:
    >>> from autoprojectmanagement.services.integration_services.wiki_git_operations import {main_class}
    >>> instance = {main_class}()
    >>> instance.run()

Notes:
    - This file follows the AutoProjectManagement coding standards
    - All changes should be documented in the changelog below
    - Ensure compatibility with Python 3.8+

Changelog:
    1.0.0 (2024-01-01): Initial release
    1.0.1 (2025-08-14): {change_description}

TODO:
    - [ ] Add comprehensive error handling
    - [ ] Implement logging throughout
    - [ ] Add unit tests
    - [ ] Update documentation

================================================================================
"""


import os
import shutil
import tempfile
import logging
from pathlib import Path
from typing import Optional, List
from git import Repo, GitCommandError
from datetime import datetime


class WikiGitOperations:
    """Handles git operations for wiki synchronization"""
    
    def __init__(self, wiki_repo_url: str, github_token: Optional[str] = None):
        self.wiki_repo_url = wiki_repo_url
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.logger = logging.getLogger(__name__)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def clone_wiki_repo(self, target_dir: Optional[str] = None) -> str:
        """
        Clone the wiki repository to a temporary directory.
        
        Args:
            target_dir: Optional target directory. If None, creates temp dir.
            
        Returns:
            Path to the cloned repository
        """
        if target_dir is None:
            target_dir = tempfile.mkdtemp(prefix="wiki_sync_")
        
        target_path = Path(target_dir)
        
        try:
            # Clone the repository
            self.logger.info(f"Cloning wiki repository to {target_path}")
            repo = Repo.clone_from(self.wiki_repo_url, target_path)
            self.logger.info("Wiki repository cloned successfully")
            return str(target_path)
            
        except GitCommandError as e:
            if "Repository not found" in str(e):
                self.logger.error("Wiki repository not found. Please enable wiki in repository settings.")
                raise
            else:
                self.logger.error(f"Failed to clone wiki repository: {e}")
                raise
    
    def commit_changes(self, repo_path: str, message: str, files: Optional[List[str]] = None) -> bool:
        """
        Commit changes to the wiki repository.
        
        Args:
            repo_path: Path to the repository
            message: Commit message
            files: Optional list of specific files to commit
            
        Returns:
            True if changes were committed, False otherwise
        """
        try:
            repo = Repo(repo_path)
            
            # Check if there are changes to commit
            if not repo.is_dirty(untracked_files=True):
                self.logger.info("No changes to commit")
                return False
            
            # Add files
            if files:
                for file_path in files:
                    repo.index.add([file_path])
            else:
                repo.git.add(A=True)
            
            # Commit changes
            repo.index.commit(message)
            self.logger.info(f"Committed changes: {message}")
            return True
            
        except GitCommandError as e:
            self.logger.error(f"Failed to commit changes: {e}")
            return False
    
    def push_changes(self, repo_path: str, branch: str = "master") -> bool:
        """
        Push changes to the remote repository.
        
        Args:
            repo_path: Path to the repository
            branch: Branch to push to
            
        Returns:
            True if changes were pushed successfully, False otherwise
        """
        try:
            repo = Repo(repo_path)
            origin = repo.remotes.origin
            
            # Push changes
            origin.push(refspec=f"{branch}:{branch}")
            self.logger.info("Changes pushed to remote repository")
            return True
            
        except GitCommandError as e:
            self.logger.error(f"Failed to push changes: {e}")
            return False
    
    def get_changed_files(self, repo_path: str) -> List[str]:
        """
        Get list of changed files in the repository.
        
        Args:
            repo_path: Path to the repository
            
        Returns:
            List of changed file paths
        """
        try:
            repo = Repo(repo_path)
            
            # Get changed files
            changed_files = []
            
            # Modified files
            for item in repo.index.diff(None):
                changed_files.append(item.a_path)
            
            # Untracked files
            for file_path in repo.untracked_files:
                changed_files.append(file_path)
            
            return changed_files
            
        except GitCommandError as e:
            self.logger.error(f"Failed to get changed files: {e}")
            return []
    
    def create_branch(self, repo_path: str, branch_name: str) -> bool:
        """
        Create a new branch in the repository.
        
        Args:
            repo_path: Path to the repository
            branch_name: Name of the branch to create
            
        Returns:
            True if branch was created successfully, False otherwise
        """
        try:
            repo = Repo(repo_path)
            new_branch = repo.create_head(branch_name)
            new_branch.checkout()
            self.logger.info(f"Created and checked out branch: {branch_name}")
            return True
            
        except GitCommandError as e:
            self.logger.error(f"Failed to create branch: {e}")
            return False
    
    def get_commit_history(self, repo_path: str, max_count: int = 10) -> List[dict]:
        """
        Get commit history from the repository.
        
        Args:
            repo_path: Path to the repository
            max_count: Maximum number of commits to return
            
        Returns:
            List of commit information dictionaries
        """
        try:
            repo = Repo(repo_path)
            commits = list(repo.iter_commits(max_count=max_count))
            
            commit_history = []
            for commit in commits:
                commit_info = {
                    'hash': commit.hexsha[:8],
                    'message': commit.message.strip(),
                    'author': str(commit.author),
                    'date': commit.committed_datetime.isoformat(),
                    'files_changed': len(commit.stats.files)
                }
                commit_history.append(commit_info)
            
            return commit_history
            
        except GitCommandError as e:
            self.logger.error(f"Failed to get commit history: {e}")
            return []
    
    def cleanup_repository(self, repo_path: str) -> bool:
        """
        Clean up the repository directory.
        
        Args:
            repo_path: Path to the repository
            
        Returns:
            True if cleanup was successful, False otherwise
        """
        try:
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
                self.logger.info(f"Cleaned up repository directory: {repo_path}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup repository: {e}")
            return False
    
    def generate_commit_message(self, changes: dict) -> str:
        """
        Generate a commit message based on changes.
        
        Args:
            changes: Dictionary containing change information
            
        Returns:
            Generated commit message
        """
        messages = []
        
        if changes.get('files_added'):
            messages.append(f"Added {len(changes['files_added'])} wiki pages")
        
        if changes.get('files_updated'):
            messages.append(f"Updated {len(changes['files_updated'])} wiki pages")
        
        if changes.get('files_deleted'):
            messages.append(f"Deleted {len(changes['files_deleted'])} wiki pages")
        
        if not messages:
            return "Wiki sync: no changes detected"
        
        message = "Wiki sync: " + "; ".join(messages)
        message += f" - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return message
