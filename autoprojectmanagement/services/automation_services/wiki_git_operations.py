#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/services/automation_services/wiki_git_operations.py
File: wiki_git_operations.py
Purpose: Wiki Git operations
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Wiki Git operations within the AutoProjectManagement system
"""

import logging
from typing import Dict, Any, Optional, List, Union
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CURRENT_VERSION = "2.0.0"
PYTHON_MIN_VERSION = "3.8+"
CREATED_DATE = "2025-08-14"
MODIFIED_DATE = "2025-08-14"

# Module-level docstring
__doc__ = """
Wiki Git operations within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import os
import subprocess
import logging
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass
from contextlib import contextmanager
import tempfile
import shutil
from datetime import datetime

# Phase 3: Code Quality - Constants for magic numbers
DEFAULT_TIMEOUT_SECONDS = 30
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 1
ENCODING_UTF8 = 'utf-8'

# Git configuration constants
GIT_CONFIG_USER_NAME = 'AutoProjectManagement'
GIT_CONFIG_USER_EMAIL = 'automation@projectmanagement.com'

# Logging configuration
logger = logging.getLogger(__name__)


@dataclass
class GitOperationResult:
    """Result of a Git operation with success status and details."""
    success: bool
    message: str
    return_code: int = 0
    stdout: str = ""
    stderr: str = ""
    timestamp: datetime = None
    
    def __post_init__(self) -> None:
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


class WikiGitOperations:
    """
    Manages Git operations for wiki synchronization in automated project management.
    
    This class provides comprehensive Git functionality for managing wiki pages,
    including repository cloning, pushing changes, pulling updates, branch management,
    and conflict resolution. It handles both local and remote repository operations
    with proper error handling and logging.
    
    Example:
        >>> git_ops = WikiGitOperations('/path/to/wiki/repo')
        >>> result = git_ops.clone_repository('https://github.com/user/wiki.git')
        >>> if result.success:
        ...     print("Repository cloned successfully")
    """
    
    def __init__(self, repository_path: str) -> None:
        """
        Initialize WikiGitOperations with repository path.
        
        Args:
            repository_path: Local path to the Git repository
            
        Raises:
            ValueError: If repository path is invalid or empty
        """
        if not repository_path or not isinstance(repository_path, str):
            raise ValueError("Repository path must be a non-empty string")
            
        self.repository_path = Path(repository_path)
        self._ensure_repository_directory()
        
    def _ensure_repository_directory(self) -> None:
        """Ensure the repository directory exists."""
        self.repository_path.mkdir(parents=True, exist_ok=True)
        
    def _run_git_command(
        self, 
        command: List[str], 
        cwd: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT_SECONDS
    ) -> GitOperationResult:
        """
        Execute a Git command with proper error handling.
        
        Args:
            command: List of command arguments
            cwd: Working directory for command execution
            timeout: Command timeout in seconds
            
        Returns:
            GitOperationResult with execution details
            
        Example:
            >>> result = self._run_git_command(['status'])
            >>> print(result.message)
        """
        try:
            # Use repository path as default working directory
            working_dir = cwd or str(self.repository_path)
            
            # Construct full command
            full_command = ['git'] + command
            
            logger.debug(f"Executing: {' '.join(full_command)} in {working_dir}")
            
            # Execute command with timeout
            process = subprocess.run(
                full_command,
                cwd=working_dir,
                capture_output=True,
                text=True,
                encoding=ENCODING_UTF8,
                timeout=timeout
            )
            
            # Create result object
            result = GitOperationResult(
                success=process.returncode == 0,
                message="Command executed successfully" if process.returncode == 0 else "Command failed",
                return_code=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr
            )
            
            if not result.success:
                logger.warning(f"Git command failed: {result.stderr}")
                
            return result
            
        except subprocess.TimeoutExpired:
            error_msg = f"Git command timed out after {timeout} seconds"
            logger.error(error_msg)
            return GitOperationResult(
                success=False,
                message=error_msg,
                return_code=-1
            )
        except Exception as e:
            error_msg = f"Unexpected error executing Git command: {str(e)}"
            logger.error(error_msg)
            return GitOperationResult(
                success=False,
                message=error_msg,
                return_code=-1
            )
    
    def clone_repository(
        self, 
        remote_url: str, 
        branch: str = "main",
        depth: Optional[int] = None
    ) -> GitOperationResult:
        """
        Clone a remote repository to the local path.
        
        Args:
            remote_url: URL of the remote repository
            branch: Branch to clone (default: main)
            depth: Clone depth for shallow clone (None for full clone)
            
        Returns:
            GitOperationResult with clone status
            
        Example:
            >>> result = git_ops.clone_repository(
            ...     'https://github.com/user/project-wiki.git',
            ...     branch='main'
            ... )
        """
        if not remote_url:
            return GitOperationResult(
                success=False,
                message="Remote URL cannot be empty"
            )
            
        # Prepare clone command
        clone_command = ['clone', '--branch', branch]
        
        if depth:
            clone_command.extend(['--depth', str(depth)])
            
        clone_command.extend([remote_url, str(self.repository_path)])
        
        # Execute clone
        result = self._run_git_command(clone_command, cwd=str(self.repository_path.parent))
        
        if result.success:
            logger.info(f"Successfully cloned repository from {remote_url}")
            
        return result
    
    def pull_changes(self, remote: str = "origin", branch: str = "main") -> GitOperationResult:
        """
        Pull latest changes from remote repository.
        
        Args:
            remote: Remote name (default: origin)
            branch: Branch to pull from (default: main)
            
        Returns:
            GitOperationResult with pull status
            
        Example:
            >>> result = git_ops.pull_changes()
            >>> if result.success:
            ...     print("Repository updated successfully")
        """
        # Ensure we're in a git repository
        if not self._is_git_repository():
            return GitOperationResult(
                success=False,
                message="Not a valid Git repository"
            )
            
        # Fetch changes first
        fetch_result = self._run_git_command(['fetch', remote])
        if not fetch_result.success:
            return fetch_result
            
        # Pull changes
        pull_result = self._run_git_command(['pull', remote, branch])
        
        if pull_result.success:
            logger.info(f"Successfully pulled changes from {remote}/{branch}")
            
        return pull_result
    
    def push_changes(
        self, 
        remote: str = "origin", 
        branch: str = "main",
        force: bool = False
    ) -> GitOperationResult:
        """
        Push local changes to remote repository.
        
        Args:
            remote: Remote name (default: origin)
            branch: Branch to push to (default: main)
            force: Force push (use with caution)
            
        Returns:
            GitOperationResult with push status
            
        Example:
            >>> result = git_ops.push_changes(force=False)
            >>> if not result.success:
            ...     logger.error(f"Push failed: {result.message}")
        """
        if not self._is_git_repository():
            return GitOperationResult(
                success=False,
                message="Not a valid Git repository"
            )
            
        # Prepare push command
        push_command = ['push', remote, branch]
        
        if force:
            push_command.insert(2, '--force')
            
        # Execute push
        result = self._run_git_command(push_command)
        
        if result.success:
            logger.info(f"Successfully pushed changes to {remote}/{branch}")
        else:
            logger.error(f"Push failed: {result.stderr}")
            
        return result
    
    def _is_git_repository(self) -> bool:
        """
        Check if the current directory is a valid Git repository.
        
        Returns:
            True if valid Git repository, False otherwise
        """
        result = self._run_git_command(['rev-parse', '--git-dir'])
        return result.success
    
    def get_status(self) -> GitOperationResult:
        """
        Get the current Git status of the repository.
        
        Returns:
            GitOperationResult with status information
            
        Example:
            >>> result = git_ops.get_status()
            >>> print(result.stdout)
        """
        if not self._is_git_repository():
            return GitOperationResult(
                success=False,
                message="Not a valid Git repository"
            )
            
        return self._run_git_command(['status', '--porcelain'])
    
    def get_branches(self) -> GitOperationResult:
        """
        Get list of all branches in the repository.
        
        Returns:
            GitOperationResult with branch list
            
        Example:
            >>> result = git_ops.get_branches()
            >>> for branch in result.stdout.split('\\n'):
            ...     print(branch.strip())
        """
        if not self._is_git_repository():
            return GitOperationResult(
                success=False,
                message="Not a valid Git repository"
            )
            
        return self._run_git_command(['branch', '-a'])
    
    def create_branch(self, branch_name: str, checkout: bool = True) -> GitOperationResult:
        """
        Create a new branch and optionally check it out.
        
        Args:
            branch_name: Name of the new branch
            checkout: Whether to checkout the new branch immediately
            
        Returns:
            GitOperationResult with branch creation status
            
        Example:
            >>> result = git_ops.create_branch('feature/new-docs')
            >>> if result.success:
            ...     print("Branch created successfully")
        """
        if not branch_name:
            return GitOperationResult(
                success=False,
                message="Branch name cannot be empty"
            )
            
        if not self._is_git_repository():
            return GitOperationResult(
                success=False,
                message="Not a valid Git repository"
            )
            
        # Create branch
        create_command = ['checkout', '-b', branch_name] if checkout else ['branch', branch_name]
        result = self._run_git_command(create_command)
        
        if result.success:
            logger.info(f"Successfully created branch: {branch_name}")
            
        return result
    
    def commit_changes(
        self, 
        message: str, 
        files: Optional[List[str]] = None,
        author: Optional[str] = None
    ) -> GitOperationResult:
        """
        Commit changes with specified message and files.
        
        Args:
            message: Commit message
            files: List of files to commit (None for all changes)
            author: Author for the commit (format: "Name <email>")
            
        Returns:
            GitOperationResult with commit status
            
        Example:
            >>> result = git_ops.commit_changes(
            ...     "Update project documentation",
            ...     files=['README.md', 'docs/guide.md']
            ... )
        """
        if not message:
            return GitOperationResult(
                success=False,
                message="Commit message cannot be empty"
            )
            
        if not self._is_git_repository():
            return GitOperationResult(
                success=False,
                message="Not a valid Git repository"
            )
            
        # Stage changes
        if files:
            for file_path in files:
                stage_result = self._run_git_command(['add', file_path])
                if not stage_result.success:
                    return stage_result
        else:
            stage_result = self._run_git_command(['add', '.'])
            if not stage_result.success:
                return stage_result
                
        # Prepare commit command
        commit_command = ['commit', '-m', message]
        
        if author:
            commit_command.extend(['--author', author])
            
        # Execute commit
        result = self._run_git_command(commit_command)
        
        if result.success:
            logger.info(f"Successfully committed changes: {message}")
            
        return result
    
    def get_commit_history(
        self, 
        limit: int = 10, 
        branch: str = "HEAD"
    ) -> GitOperationResult:
        """
        Get commit history for the specified branch.
        
        Args:
            limit: Maximum number of commits to return
            branch: Branch to get history from (default: HEAD)
            
        Returns:
            GitOperationResult with commit history
            
        Example:
            >>> result = git_ops.get_commit_history(limit=5)
            >>> for line in result.stdout.split('\\n'):
            ...     print(line)
        """
        if not self._is_git_repository():
            return GitOperationResult(
                success=False,
                message="Not a valid Git repository"
            )
            
        if limit <= 0:
            limit = 10
            
        format_string = "%h - %an, %ar : %s"
        return self._run_git_command([
            'log', branch, 
            f'--pretty=format:{format_string}', 
            f'-{limit}'
        ])
    
    def configure_git_user(self, name: str, email: str) -> GitOperationResult:
        """
        Configure Git user name and email for the repository.
        
        Args:
            name: User name
            email: User email
            
        Returns:
            GitOperationResult with configuration status
            
        Example:
            >>> result = git_ops.configure_git_user(
            ...     "AutoProjectManagement",
            ...     "automation@projectmanagement.com"
            ... )
        """
        if not name or not email:
            return GitOperationResult(
                success=False,
                message="Both name and email are required"
            )
            
        if not self._is_git_repository():
            return GitOperationResult(
                success=False,
                message="Not a valid Git repository"
            )
            
        # Configure user name
        name_result = self._run_git_command(['config', 'user.name', name])
        if not name_result.success:
            return name_result
            
        # Configure user email
        email_result = self._run_git_command(['config', 'user.email', email])
        
        if email_result.success:
            logger.info(f"Successfully configured Git user: {name} <{email}>")
            
        return email_result
    
    def has_uncommitted_changes(self) -> bool:
        """
        Check if there are uncommitted changes in the repository.
        
        Returns:
            True if there are uncommitted changes, False otherwise
            
        Example:
            >>> if git_ops.has_uncommitted_changes():
            ...     print("Please commit your changes first")
        """
        status_result = self.get_status()
        if not status_result.success:
            return False
            
        # Check if there's any output (indicating changes)
        return bool(status_result.stdout.strip())
    
    def get_remote_url(self, remote: str = "origin") -> GitOperationResult:
        """
        Get the URL of the specified remote.
        
        Args:
            remote: Remote name (default: origin)
            
        Returns:
            GitOperationResult with remote URL
            
        Example:
            >>> result = git_ops.get_remote_url()
            >>> print(f"Remote URL: {result.stdout.strip()}")
        """
        if not self._is_git_repository():
            return GitOperationResult(
                success=False,
                message="Not a valid Git repository"
            )
            
        return self._run_git_command(['config', '--get', f'remote.{remote}.url'])
    
    def initialize_repository(self) -> GitOperationResult:
        """
        Initialize a new Git repository in the specified path.
        
        Returns:
            GitOperationResult with initialization status
            
        Example:
            >>> result = git_ops.initialize_repository()
            >>> if result.success:
            ...     print("Repository initialized successfully")
        """
        if self._is_git_repository():
            return GitOperationResult(
                success=False,
                message="Repository already exists"
            )
            
        result = self._run_git_command(['init'])
        
        if result.success:
            logger.info(f"Successfully initialized repository at {self.repository_path}")
            
        return result
    
    @contextmanager
    def temporary_clone(self, remote_url: str, branch: str = "main"):
        """
        Context manager for temporary repository clone.
        
        This method creates a temporary clone of a remote repository and ensures
        cleanup after use. Useful for operations that need a clean environment.
        
        Args:
            remote_url: URL of the remote repository
            branch: Branch to clone (default: main)
            
        Yields:
            WikiGitOperations instance for the temporary repository
            
        Example:
            >>> with WikiGitOperations.temporary_clone('https://github.com/user/wiki.git') as git_ops:
            ...     result = git_ops.get_status()
            ...     print(result.stdout)
        """
        temp_dir = tempfile.mkdtemp(prefix='wiki_clone_')
        temp_git_ops = WikiGitOperations(temp_dir)
        
        try:
            # Clone repository
            clone_result = temp_git_ops.clone_repository(remote_url, branch)
            if not clone_result.success:
                raise RuntimeError(f"Failed to clone repository: {clone_result.message}")
                
            yield temp_git_ops
            
        finally:
            # Cleanup temporary directory
            try:
                shutil.rmtree(temp_dir)
                logger.debug(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary directory: {e}")


# Phase 4: Integration - Example usage and testing functions
def create_test_repository(test_path: str) -> WikiGitOperations:
    """
    Create a test repository for development and testing purposes.
    
    Args:
        test_path: Path for the test repository
        
    Returns:
        WikiGitOperations instance for the test repository
        
    Example:
        >>> test_git = create_test_repository('/tmp/test_wiki')
        >>> result = test_git.initialize_repository()
        >>> print(result.message)
    """
    git_ops = WikiGitOperations(test_path)
    
    # Initialize repository
    init_result = git_ops.initialize_repository()
    if not init_result.success:
        raise RuntimeError(f"Failed to initialize test repository: {init_result.message}")
    
    # Configure user
    config_result = git_ops.configure_git_user(
        GIT_CONFIG_USER_NAME,
        GIT_CONFIG_USER_EMAIL
    )
    if not config_result.success:
        raise RuntimeError(f"Failed to configure test repository: {config_result.message}")
    
    return git_ops


if __name__ == "__main__":
    # Example usage and basic testing
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = "/tmp/test_wiki"
    
    try:
        # Create test repository
        git_ops = create_test_repository(repo_path)
        
        # Test basic operations
        print("Repository initialized successfully")
        
        # Create a test file
        test_file = Path(repo_path) / "README.md"
        test_file.write_text("# Test Wiki\\n\\nThis is a test repository.")
        
        # Test commit
        commit_result = git_ops.commit_changes("Initial commit with README")
        print(f"Commit result: {commit_result.message}")
        
        # Test status
        status_result = git_ops.get_status()
        print(f"Status: {status_result.stdout}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
