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
import subprocess

# Add src directory to path for imports
src_path = Path(__file__).resolve().parent.parent.parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import the module directly
import importlib.util
spec = importlib.util.spec_from_file_location(
    "auto_file_watcher", 
    str(src_path / "autoprojectmanagement" / "services" / "automation_services" / "auto_file_watcher.py")
)
auto_file_watcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auto_file_watcher)

# Import classes directly
AutoCommitFileWatcher = auto_file_watcher.AutoCommitFileWatcher
ScheduledAutoCommit = auto_file_watcher.ScheduledAutoCommit
AutoFileWatcherService = auto_file_watcher.AutoFileWatcherService


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
        with patch('autoprojectmanagement.services.automation_services.auto_commit.UnifiedAutoCommit') as mock:
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
