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
