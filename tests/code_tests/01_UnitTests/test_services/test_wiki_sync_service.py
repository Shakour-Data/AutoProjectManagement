#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: test_wiki_sync_service
File: test_wiki_sync_service.py
Path: tests/code_tests/01_UnitTests/test_services/test_wiki_sync_service.py

Description:
    Test Wiki Sync Service module

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
    >>> from tests.code_tests.01_UnitTests.test_services.test_wiki_sync_service import {main_class}
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
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile

from autoprojectmanagement.services.wiki_sync_service import WikiSyncService


class TestWikiSyncService:
    """Test class for WikiSyncService"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.repo_owner = "test_owner"
        self.repo_name = "test_repo"
        self.github_token = "test_token"
        self.service = WikiSyncService(self.repo_owner, self.repo_name, self.github_token)
    
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiGitOperations.clone_wiki_repo')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiSyncService._wiki_exists')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiSyncService._create_initial_wiki')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiSyncService._discover_markdown_files')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiSyncService._generate_sync_plan')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiGitOperations.commit_changes')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiGitOperations.push_changes')
    def test_sync_to_wiki_dry_run(self, mock_push, mock_commit, mock_generate_plan, mock_discover, mock_create_initial, mock_wiki_exists, mock_clone):
        """Test sync_to_wiki method with dry_run=True"""
        mock_wiki_exists.return_value = True
        mock_clone.return_value = "/tmp/wiki"
        mock_discover.return_value = [Path("/docs/file1.md")]
        mock_generate_plan.return_value = {
            'files_to_add': [],
            'files_to_update': [],
            'files_to_delete': [],
            'total_files': 1
        }
        
        result = self.service.sync_to_wiki(dry_run=True)
        
        assert 'files_to_add' in result
        assert 'files_to_update' in result
        assert 'files_to_delete' in result
        assert 'total_files' in result
        mock_create_initial.assert_not_called()
        mock_commit.assert_not_called()
        mock_push.assert_not_called()
    
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiGitOperations.clone_wiki_repo')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiSyncService._wiki_exists')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiSyncService._create_initial_wiki')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiSyncService._discover_markdown_files')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiSyncService._generate_sync_plan')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiGitOperations.commit_changes')
    @patch('autoprojectmanagement.services.wiki_sync_service.WikiGitOperations.push_changes')
    def test_sync_to_wiki_commit_and_push(self, mock_push, mock_commit, mock_generate_plan, mock_discover, mock_create_initial, mock_wiki_exists, mock_clone):
        """Test sync_to_wiki method with commit and push"""
        mock_wiki_exists.return_value = True
        mock_clone.return_value = "/tmp/wiki"
        mock_discover.return_value = [Path("/docs/file1.md")]
        mock_generate_plan.return_value = {
            'files_to_add': [{'source': Path("/docs/file1.md"), 'target': Path("/tmp/wiki/File1.md"), 'wiki_name': 'File1'}],
            'files_to_update': [],
            'files_to_delete': [],
            'total_files': 1,
            'files_changed': 1
        }
        mock_commit.return_value = True
        mock_push.return_value = True
        
        result = self.service.sync_to_wiki(dry_run=False)
        
        assert 'files_to_add' in result
        assert mock_commit.called
        assert mock_push.called
    
    @patch('autoprojectmanagement.services.wiki_sync_service.requests.get')
    def test_wiki_exists_true(self, mock_get):
        """Test _wiki_exists returns True"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'has_wiki': True}
        mock_get.return_value = mock_response
        
        result = self.service._wiki_exists()
        
        assert result is True
    
    @patch('autoprojectmanagement.services.wiki_sync_service.requests.get')
    def test_wiki_exists_false(self, mock_get):
        """Test _wiki_exists returns False"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.service._wiki_exists()
        
        assert result is False
    
    def test_create_initial_wiki_calls_github_integration(self):
        """Test _create_initial_wiki calls GitHubIntegration.create_wiki_page"""
        with patch('autoprojectmanagement.services.wiki_sync_service.GitHubIntegration') as mock_github:
            mock_instance = mock_github.return_value
            self.service._create_initial_wiki()
            mock_instance.create_wiki_page.assert_called_once()
    
    def test_discover_markdown_files(self, tmp_path):
        """Test _discover_markdown_files returns markdown files"""
        docs_dir = tmp_path / "Docs"
        docs_dir.mkdir()
        file1 = docs_dir / "file1.md"
        file1.write_text("# Test")
        file2 = docs_dir / "file2.txt"
        file2.write_text("Not markdown")
        
        self.service.docs_path = docs_dir
        
        result = self.service._discover_markdown_files()
        
        assert file1 in result
        assert file2 not in result
    
    def test_generate_sync_plan_empty(self):
        """Test _generate_sync_plan returns empty plan if no temp_dir"""
        self.service.temp_dir = None
        result = self.service._generate_sync_plan([])
        assert result['files_to_add'] == []
        assert result['files_to_update'] == []
        assert result['files_to_delete'] == []
    
    def test_generate_sync_plan_basic(self, tmp_path):
        """Test _generate_sync_plan with basic add and update"""
        self.service.temp_dir = str(tmp_path)
        
        # Create existing wiki file
        existing_file = tmp_path / "ExistingPage.md"
        existing_file.write_text("Old content")
        
        # Create markdown files
        md_file = tmp_path / "NewPage.md"
        md_file.write_text("New content")
        
        # Patch mapper to map md_file to NewPage
        self.service.mapper.map_file_to_wiki_page = lambda f, d: "NewPage"
        
        # Patch _file_needs_update to True for update
        self.service._file_needs_update = lambda src, tgt: True
        
        # Add existing file to current wiki files
        self.service._get_current_wiki_files = lambda: {"ExistingPage.md"}
        
        markdown_files = [md_file]
        
        result = self.service._generate_sync_plan(markdown_files)
        
        assert 'files_to_add' in result
        assert 'files_to_update' in result
        assert 'files_to_delete' in result
