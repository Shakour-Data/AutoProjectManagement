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
            f.write("initial content")
        
        # Initialize watcher
        watcher = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=0.1)
        
        # Simulate file modification
        with open(test_file, "w") as f:
            f.write("modified content")
        
        # Trigger modification event
        from watchdog.events import FileModifiedEvent
        event = FileModifiedEvent(test_file)
        watcher.on_modified(event)
        
        # Check that change was recorded
        assert len(watcher.pending_changes) == 1
        assert ("modified", test_file) in [(c[1], c[0]) for c in watcher.pending_changes]
    
    def test_file_creation_detection(self, temp_project_dir, mock_auto_commit, mock_realtime_service):
        """Test that file creations are properly detected and processed."""
        watcher = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=0.1)
        
        # Create a new file
        test_file = os.path.join(temp_project_dir, "new_file.py")
        with open(test_file, "w") as f:
            f.write("new content")
        
        # Trigger creation event
        from watchdog.events import FileCreatedEvent
        event = FileCreatedEvent(test_file)
        watcher.on_created(event)
        
        # Check that change was recorded
        assert len(watcher.pending_changes) == 1
        assert ("created", test_file) in [(c[1], c[0]) for c in watcher.pending_changes]
    
    def test_file_deletion_detection(self, temp_project_dir, mock_auto_commit, mock_realtime_service):
        """Test that file deletions are properly detected and processed."""
        # Create a test file first
        test_file = os.path.join(temp_project_dir, "to_delete.py")
        with open(test_file, "w") as f:
            f.write("content")
        
        watcher = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=0.1)
        
        # Delete the file
        os.remove(test_file)
        
        # Trigger deletion event
        from watchdog.events import FileDeletedEvent
        event = FileDeletedEvent(test_file)
        watcher.on_deleted(event)
        
        # Check that change was recorded
        assert len(watcher.pending_changes) == 1
        assert ("deleted", test_file) in [(c[1], c[0]) for c in watcher.pending_changes]
    
    def test_file_move_detection(self, temp_project_dir, mock_auto_commit, mock_realtime_service):
        """Test that file moves/renames are properly detected and processed."""
        # Create source file
        src_file = os.path.join(temp_project_dir, "source.py")
        dest_file = os.path.join(temp_project_dir, "destination.py")
        
        with open(src_file, "w") as f:
            f.write("content")
        
        watcher = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=0.1)
        
        # Trigger move event
        from watchdog.events import FileMovedEvent
        event = FileMovedEvent(src_file, dest_file)
        watcher.on_moved(event)
        
        # Check that both move events were recorded
        assert len(watcher.pending_changes) == 2
        changes = [(c[1], c[0]) for c in watcher.pending_changes]
        assert ("moved_from", src_file) in changes
        assert ("moved_to", dest_file) in changes
    
    def test_file_filtering_logic(self, temp_project_dir, mock_auto_commit, mock_realtime_service):
        """Test that file filtering logic works correctly."""
        watcher = AutoCommitFileWatcher(temp_project_dir)
        
        # Test monitored file (should return True)
        monitored_file = os.path.join(temp_project_dir, "test.py")
        assert watcher.should_monitor_file(monitored_file) is True
        
        # Test excluded directory file (should return False)
        excluded_dir = os.path.join(temp_project_dir, ".git")
        os.makedirs(excluded_dir, exist_ok=True)
        excluded_file = os.path.join(excluded_dir, "config")
        assert watcher.should_monitor_file(excluded_file) is False
        
        # Test directory (should return False)
        assert watcher.should_monitor_file(temp_project_dir) is False
        
        # Test non-monitored extension (should return False)
        non_monitored = os.path.join(temp_project_dir, "test.log")
        assert watcher.should_monitor_file(non_monitored) is False
    
    # ==================== EDGE CASE TESTS ====================
    
    def test_rapid_file_changes_debouncing(self, temp_project_dir, mock_auto_commit, mock_realtime_service):
        """Test that rapid file changes are properly debounced."""
        watcher = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=0.5)
        
        # Create multiple rapid changes
        test_file = os.path.join(temp_project_dir, "rapid.py")
        
        for i in range(5):
            with open(test_file, "w") as f:
