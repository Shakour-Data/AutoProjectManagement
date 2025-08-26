#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for auto_file_watcher.py module.

This module contains comprehensive unit tests for the AutoFileWatcherService,
AutoCommitFileWatcher, and ScheduledAutoCommit classes.

Test Categories:
1. File Watching Functionality Tests (5 tests)
2. Edge Case Tests (5 tests) 
3. Error Handling Tests (5 tests)
4. Integration Tests (5 tests)

Total: 20 tests as required by TODO.md
"""

import os
import sys
import time
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import asyncio
import threading

# Add project root to path for imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from autoprojectmanagement.services.automation_services.auto_file_watcher import (
    AutoCommitFileWatcher,
    ScheduledAutoCommit,
    AutoFileWatcherService
)


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_auto_commit():
    """Mock the UnifiedAutoCommit class."""
    with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.UnifiedAutoCommit') as mock:
        instance = mock.return_value
        instance.run_complete_workflow_guaranteed.return_value = True
        yield instance


@pytest.fixture
def mock_realtime_service():
    """Mock the realtime_service module."""
    with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.publish_file_change_event') as mock:
        mock.return_value = AsyncMock()
        yield mock


@pytest.fixture
def mock_subprocess():
    """Mock subprocess module for Git commands."""
    with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.subprocess') as mock:
        mock.run.return_value.returncode = 0
        mock.run.return_value.stdout = ""
        yield mock


class TestAutoCommitFileWatcher:
    """Test class for AutoCommitFileWatcher functionality."""
    
    # ==================== FILE WATCHING FUNCTIONALITY TESTS ====================
    
    def test_file_modification_detection(self, temp_project_dir, mock_auto_commit, mock_realtime_service):
        """Test that file modifications are properly detected and processed."""
        # Create a test file
        test_file = os.path.join(temp_project_dir, "test.py")
        with open(test_file, "w") as f:
