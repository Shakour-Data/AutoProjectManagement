#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Unit Tests for Auto File Watcher Service
================================================================================
Module: test_auto_file_watcher
File: test_auto_file_watcher.py
Path: tests/code_tests/01_UnitTests/test_services/test_auto_file_watcher.py

Description:
    Comprehensive unit tests for the AutoFileWatcherService module.
    Includes 20+ tests covering functionality, edge cases, error handling, and integration.

Test Categories:
    1. File Watching Functionality Tests (5 tests)
    2. Edge Case Tests (5 tests) 
    3. Error Handling Tests (5 tests)
    4. Integration Tests (5 tests)

Author: AutoProjectManagement Team
Version: 1.0.0
================================================================================
"""

import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import asyncio
import threading
import time

# Add project root to path for imports
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from autoprojectmanagement.services.automation_services.auto_file_watcher import (
    AutoCommitFileWatcher,
    ScheduledAutoCommit,
    AutoFileWatcherService
)


class TestAutoCommitFileWatcher:
    """Test class for AutoCommitFileWatcher functionality"""
    
    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary project directory for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    @pytest.fixture
    def mock_auto_commit(self):
        """Mock the UnifiedAutoCommit class"""
        with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.UnifiedAutoCommit') as mock:
            mock_instance = Mock()
            mock_instance.run_complete_workflow_guaranteed.return_value = True
            mock.return_value = mock_instance
            yield mock_instance
    
    @pytest.fixture
    def mock_realtime_service(self):
        """Mock the realtime service"""
        with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.publish_file_change_event') as mock:
            yield mock
    
    def test_should_monitor_file_valid_extension(self, temp_project_dir, mock_auto_commit):
        """Test that files with valid extensions are monitored"""
        handler = AutoCommitFileWatcher(temp_project_dir)
        
        # Create test files with valid extensions
        test_files = [
            "test.py", "script.js", "style.css", "data.json", "readme.md"
        ]
        
        for filename in test_files:
            file_path = os.path.join(temp_project_dir, filename)
            with open(file_path, 'w') as f:
                f.write("test content")
            
            assert handler.should_monitor_file(file_path) == True
    
    def test_should_monitor_file_excluded_directories(self, temp_project_dir, mock_auto_commit):
        """Test that files in excluded directories are not monitored"""
        handler = AutoCommitFileWatcher(temp_project_dir)
        
        # Create excluded directories
        excluded_dirs = ['.git', 'node_modules', '__pycache__']
        for dir_name in excluded_dirs:
            dir_path = os.path.join(temp_project_dir, dir_name)
            os.makedirs(dir_path)
            
            # Create file in excluded directory
            file_path = os.path.join(dir_path, 'test.py')
            with open(file_path, 'w') as f:
                f.write("test content")
            
            assert handler.should_monitor_file(file_path) == False
    
    def test_should_monitor_file_special_files(self, temp_project_dir, mock_auto_commit):
        """Test that special files (Dockerfile, docker-compose.yml) are monitored"""
        handler = AutoCommitFileWatcher(temp_project_dir)
        
        special_files = ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml']
        for filename in special_files:
            file_path = os.path.join(temp_project_dir, filename)
            with open(file_path, 'w') as f:
                f.write("test content")
            
            assert handler.should_monitor_file(file_path) == True
    
    def test_file_modification_detection(self, temp_project_dir, mock_auto_commit, mock_realtime_service):
        """Test that file modifications are detected and processed"""
        handler = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=0.1)
        
        # Create a test file
        test_file = os.path.join(temp_project_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write("initial content")
        
        # Simulate file modification event
        mock_event = Mock()
        mock_event.is_directory = False
        mock_event.src_path = test_file
        
        handler.on_modified(mock_event)
        
        # Wait for debounce timer
        time.sleep(0.2)
        
        # Verify auto-commit was called
        assert mock_auto_commit.run_complete_workflow_guaranteed.called
    
    def test_file_creation_detection(self, temp_project_dir, mock_auto_commit, mock_realtime_service):
        """Test that file creations are detected and processed"""
        handler = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=0.1)
        
        # Create a test file
        test_file = os.path.join(temp_project_dir, 'new_file.py')
        with open(test_file, 'w') as f:
            f.write("new content")
        
        # Simulate file creation event
        mock_event = Mock()
        mock_event.is_directory = False
        mock_event.src_path = test_file
        
        handler.on_created(mock_event)
        
        # Wait for debounce timer
        time.sleep(0.2)
        
        # Verify auto-commit was called
        assert mock_auto_commit.run_complete_workflow_guaranteed.called


class TestEdgeCases:
    """Test edge cases for AutoCommitFileWatcher"""
    
    @pytest.fixture
    def temp_project_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    @pytest.fixture
    def mock_auto_commit(self):
        with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.UnifiedAutoCommit') as mock:
            mock_instance = Mock()
            mock_instance.run_complete_workflow_guaranteed.return_value = True
            mock.return_value = mock_instance
            yield mock_instance
    
    def test_rapid_file_changes_debouncing(self, temp_project_dir, mock_auto_commit):
        """Test that rapid file changes are debounced properly"""
        handler = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=1.0)
        
        test_file = os.path.join(temp_project_dir, 'test.py')
        
        # Create multiple rapid changes
        for i in range(5):
            with open(test_file, 'w') as f:
                f.write(f"content {i}")
            
            mock_event = Mock()
            mock_event.is_directory = False
            mock_event.src_path = test_file
            
            handler.on_modified(mock_event)
        
        # Wait for debounce timer
        time.sleep(1.1)
        
        # Should only trigger auto-commit once due to debouncing
        assert mock_auto_commit.run_complete_workflow_guaranteed.call_count == 1
    
    def test_permission_denied_scenario(self, temp_project_dir, mock_auto_commit):
        """Test behavior when file access is denied"""
        handler = AutoCommitFileWatcher(temp_project_dir)
        
        # Create a file with no read permissions
        test_file = os.path.join(temp_project_dir, 'no_access.py')
