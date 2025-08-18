#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: test_wiki_git_operations
File: test_wiki_git_operations.py
Path: tests/code_tests/01_UnitTests/test_services/test_wiki_git_operations.py

Description:
    Test Wiki Git Operations module

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
    >>> from tests.code_tests.01_UnitTests.test_services.test_wiki_git_operations import {main_class}
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


import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

try:
    from git import Repo, GitCommandError
except ImportError:
    # Mock git module for testing when not available
    class Repo:
        @staticmethod
        def clone_from(url, path, **kwargs):
            pass
    
    class GitCommandError(Exception):
        pass

from autoprojectmanagement.services.wiki_git_operations import WikiGitOperations


class TestWikiGitOperations:
    """Test class for WikiGitOperations"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.wiki_repo_url = "https://github.com/test/test-repo.wiki.git"
        self.github_token = "test_token"
        self.git_ops = WikiGitOperations(self.wiki_repo_url, self.github_token)
    
    def test_init(self):
        """Test initialization of WikiGitOperations"""
        assert self.git_ops.wiki_repo_url == self.wiki_repo_url
        assert self.git_ops.github_token == self.github_token
        assert self.git_ops.logger is not None
    
    @patch('git.Repo.clone_from')
    def test_clone_wiki_repo_success(self, mock_clone):
        """Test successful repository cloning"""
        mock_repo = Mock()
        mock_clone.return_value = mock_repo
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.git_ops.clone_wiki_repo(temp_dir)
            
            assert result == temp_dir
            mock_clone.assert_called_once()
    
    @patch('git.Repo.clone_from')
    def test_clone_wiki_repo_not_found(self, mock_clone):
        """Test repository cloning when repo not found"""
        mock_clone.side_effect = GitCommandError("clone", "Repository not found")
        
        with pytest.raises(GitCommandError):
            self.git_ops.clone_wiki_repo()
    
    @patch('git.Repo')
    def test_commit_changes_success(self, mock_repo_class):
        """Test successful commit of changes"""
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        mock_repo.is_dirty.return_value = True
        
        repo_path = "/fake/path"
        message = "Test commit"
        
        result = self.git_ops.commit_changes(repo_path, message)
        
        assert result is True
        mock_repo.index.add.assert_called_once_with(A=True)
        mock_repo.index.commit.assert_called_once_with(message)
    
    @patch('git.Repo')
    def test_commit_changes_no_changes(self, mock_repo_class):
        """Test commit when no changes exist"""
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        mock_repo.is_dirty.return_value = False
        
        repo_path = "/fake/path"
        message = "Test commit"
        
        result = self.git_ops.commit_changes(repo_path, message)
        
        assert result is False
    
    @patch('git.Repo')
    def test_commit_changes_specific_files(self, mock_repo_class):
        """Test commit with specific files"""
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        mock_repo.is_dirty.return_value = True
        
        repo_path = "/fake/path"
        message = "Test commit"
        files = ["file1.md", "file2.md"]
        
        result = self.git_ops.commit_changes(repo_path, message, files)
        
        assert result is True
        mock_repo.index.add.assert_called_with(files)
    
    @patch('git.Repo')
    def test_push_changes_success(self, mock_repo_class):
        """Test successful push of changes"""
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        mock_origin = Mock()
        mock_repo.remotes.origin = mock_origin
        
        repo_path = "/fake/path"
        
        result = self.git_ops.push_changes(repo_path)
        
        assert result is True
        mock_origin.push.assert_called_once()
    
    @patch('git.Repo')
    def test_push_changes_failure(self, mock_repo_class):
        """Test push failure"""
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        mock_origin = Mock()
        mock_origin.push.side_effect = GitCommandError("push", "Push failed")
        mock_repo.remotes.origin = mock_origin
        
        repo_path = "/fake/path"
        
        result = self.git_ops.push_changes(repo_path)
        
        assert result is False
    
    @patch('git.Repo')
    def test_get_changed_files(self, mock_repo_class):
        """Test getting changed files"""
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        
        # Mock diff items
        mock_diff_item = Mock()
        mock_diff_item.a_path = "changed_file.md"
        mock_repo.index.diff.return_value = [mock_diff_item]
        
        # Mock untracked files
        mock_repo.untracked_files = ["new_file.md"]
        
        repo_path = "/fake/path"
        
        result = self.git_ops.get_changed_files(repo_path)
        
        assert len(result) == 2
        assert "changed_file.md" in result
        assert "new_file.md" in result
    
    @patch('git.Repo')
    def test_create_branch_success(self, mock_repo_class):
        """Test successful branch creation"""
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        mock_head = Mock()
        mock_repo.create_head.return_value = mock_head
        
        repo_path = "/fake/path"
        branch_name = "test-branch"
        
        result = self.git_ops.create_branch(repo_path, branch_name)
        
        assert result is True
        mock_repo.create_head.assert_called_once_with(branch_name)
        mock_head.checkout.assert_called_once()
    
    @patch('git.Repo')
    def test_get_commit_history(self, mock_repo_class):
        """Test getting commit history"""
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        
        # Mock commits
        mock_commit = Mock()
        mock_commit.hexsha = "a1b2c3d4e5f6"
        mock_commit.message = "Test commit"
        mock_commit.author = "Test Author"
        mock_commit.committed_datetime.isoformat.return_value = "2023-01-01T00:00:00"
        mock_commit.stats.files = {"file1.md": {}, "file2.md": {}}
        
        mock_repo.iter_commits.return_value = [mock_commit]
        
        repo_path = "/fake/path"
        
        result = self.git_ops.get_commit_history(repo_path)
        
        assert len(result) == 1
        assert result[0]['hash'] == "a1b2c3d4"
        assert result[0]['message'] == "Test commit"
        assert result[0]['files_changed'] == 2
    
    def test_cleanup_repository(self):
        """Test repository cleanup"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test directory
            test_dir = Path(temp_dir) / "test_repo"
            test_dir.mkdir()
            (test_dir / "test_file.txt").write_text("test")
            
            result = self.git_ops.cleanup_repository(str(test_dir))
            
            assert result is True
            assert not test_dir.exists()
    
    def test_cleanup_nonexistent_repository(self):
        """Test cleanup of non-existent repository"""
        nonexistent_path = "/nonexistent/path"
        
        result = self.git_ops.cleanup_repository(nonexistent_path)
        
        assert result is False
    
    def test_generate_commit_message(self):
        """Test commit message generation"""
        changes = {
            'files_added': ['file1.md', 'file2.md'],
            'files_updated': ['file3.md'],
            'files_deleted': ['file4.md']
        }
        
        message = self.git_ops.generate_commit_message(changes)
        
        assert "Added 2 wiki pages" in message
        assert "Updated 1 wiki pages" in message
        assert "Deleted 1 wiki pages" in message
        assert "Wiki sync:" in message
    
    def test_generate_commit_message_no_changes(self):
        """Test commit message when no changes"""
        changes = {}
        
        message = self.git_ops.generate_commit_message(changes)
        
        assert message == "Wiki sync: no changes detected"
