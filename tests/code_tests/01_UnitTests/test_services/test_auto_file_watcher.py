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
        with open(test_file, 'w') as f:
            f.write("test content")
        
        # Remove read permissions
        os.chmod(test_file, 0o000)
        
        try:
            result = handler.should_monitor_file(test_file)
            # Should return False due to permission error
            assert result == False
        finally:
            # Restore permissions for cleanup
            os.chmod(test_file, 0o644)
    
    def test_nonexistent_file_handling(self, temp_project_dir, mock_auto_commit):
        """Test handling of non-existent files"""
        handler = AutoCommitFileWatcher(temp_project_dir)
        
        nonexistent_file = os.path.join(temp_project_dir, 'nonexistent.py')
        result = handler.should_monitor_file(nonexistent_file)
        
        assert result == False
    
    def test_directory_events_ignored(self, temp_project_dir, mock_auto_commit):
        """Test that directory events are ignored"""
        handler = AutoCommitFileWatcher(temp_project_dir)
        
        # Create a directory
        test_dir = os.path.join(temp_project_dir, 'test_dir')
        os.makedirs(test_dir)
        
        # Simulate directory event
        mock_event = Mock()
        mock_event.is_directory = True
        mock_event.src_path = test_dir
        
        handler.on_modified(mock_event)
        
        # Should not trigger auto-commit for directories
        assert not mock_auto_commit.run_complete_workflow_guaranteed.called
    
    def test_file_extensions_boundary_cases(self, temp_project_dir, mock_auto_commit):
        """Test boundary cases for file extensions"""
        handler = AutoCommitFileWatcher(temp_project_dir)
        
        # Test files with unusual extensions
        test_cases = [
            ('test.PY', True),      # Uppercase extension
            ('test.', False),       # No extension after dot
            ('test', False),        # No extension
            ('.hidden', False),     # Hidden file without extension
        ]
        
        for filename, expected in test_cases:
            file_path = os.path.join(temp_project_dir, filename)
            with open(file_path, 'w') as f:
                f.write("test content")
            
            result = handler.should_monitor_file(file_path)
            assert result == expected


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.fixture
    def temp_project_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    
    def test_realtime_service_import_failure(self, temp_project_dir):
        """Test behavior when realtime service import fails"""
        with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.publish_file_change_event', None):
            # Should not crash when realtime service is not available
            handler = AutoCommitFileWatcher(temp_project_dir)
            
            test_file = os.path.join(temp_project_dir, 'test.py')
            with open(test_file, 'w') as f:
                f.write("test content")
            
            mock_event = Mock()
            mock_event.is_directory = False
            mock_event.src_path = test_file
            
            # Should handle gracefully without realtime service
            handler.on_modified(mock_event)
    
    def test_auto_commit_failure_handling(self, temp_project_dir, mock_auto_commit):
        """Test error handling when auto-commit fails"""
        with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.UnifiedAutoCommit') as mock_commit:
            mock_instance = Mock()
            mock_instance.run_complete_workflow_guaranteed.return_value = False
            mock_commit.return_value = mock_instance
            
            handler = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=0.1)
            
            test_file = os.path.join(temp_project_dir, 'test.py')
            with open(test_file, 'w') as f:
                f.write("test content")
            
            mock_event = Mock()
            mock_event.is_directory = False
            mock_event.src_path = test_file
            
            handler.on_modified(mock_event)
            
            # Wait for debounce timer
            time.sleep(0.2)
            
            # Should handle auto-commit failure gracefully
            assert mock_instance.run_complete_workflow_guaranteed.called
    
    def test_file_system_error_handling(self, temp_project_dir):
        """Test error handling for file system operations"""
        handler = AutoCommitFileWatcher(temp_project_dir)
        
        # Test with invalid file path that causes OS error
        invalid_path = "/invalid/path/that/does/not/exist"
        result = handler.should_monitor_file(invalid_path)
        
        # Should return False and not crash
        assert result == False
    
    def test_timer_callback_error_handling(self, temp_project_dir):
        """Test error handling in timer callbacks"""
        with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.UnifiedAutoCommit') as mock_commit:
            mock_instance = Mock()
            mock_instance.run_complete_workflow_guaranteed.side_effect = Exception("Test error")
            mock_commit.return_value = mock_instance
            
            handler = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=0.1)
            
            test_file = os.path.join(temp_project_dir, 'test.py')
            with open(test_file, 'w') as f:
                f.write("test content")
            
            mock_event = Mock()
            mock_event.is_directory = False
            mock_event.src_path = test_file
            
            handler.on_modified(mock_event)
            
            # Wait for debounce timer - should not crash despite error
            time.sleep(0.2)
            
            # Should have attempted auto-commit despite error
            assert mock_instance.run_complete_workflow_guaranteed.called
    
    def test_invalid_project_path_handling(self):
        """Test error handling for invalid project paths"""
        with pytest.raises(FileNotFoundError):
            AutoCommitFileWatcher("/invalid/path/that/does/not/exist")


class TestIntegration:
    """Test integration scenarios"""
    
    @pytest.fixture
    def temp_project_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Initialize git repo for testing
            subprocess.run(['git', 'init'], cwd=temp_dir, capture_output=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=temp_dir, capture_output=True)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=temp_dir, capture_output=True)
            yield temp_dir
    
    @pytest.fixture
    def mock_auto_commit(self):
        with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.UnifiedAutoCommit') as mock:
            mock_instance = Mock()
            mock_instance.run_complete_workflow_guaranteed.return_value = True
            mock.return_value = mock_instance
            yield mock_instance
    
    @pytest.fixture
    def mock_realtime_service(self):
        with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.publish_file_change_event') as mock:
            async_mock = AsyncMock()
            mock.return_value = async_mock
            yield async_mock
    
    def test_integration_with_auto_commit_service(self, temp_project_dir, mock_auto_commit, mock_realtime_service):
        """Test integration with UnifiedAutoCommit service"""
        handler = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=0.1)
        
        test_file = os.path.join(temp_project_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write("test content")
        
        mock_event = Mock()
        mock_event.is_directory = False
        mock_event.src_path = test_file
        
        handler.on_modified(mock_event)
        
        # Wait for debounce timer
        time.sleep(0.2)
        
        # Verify integration with auto-commit service
        assert mock_auto_commit.run_complete_workflow_guaranteed.called
    
    def test_realtime_event_publishing(self, temp_project_dir, mock_auto_commit, mock_realtime_service):
        """Test integration with real-time event service"""
        handler = AutoCommitFileWatcher(temp_project_dir, debounce_seconds=0.1)
        
        test_file = os.path.join(temp_project_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write("test content")
        
        mock_event = Mock()
        mock_event.is_directory = False
        mock_event.src_path = test_file
        
        handler.on_modified(mock_event)
        
        # Verify real-time event was published
        assert mock_realtime_service.called
    
    def test_scheduled_commit_integration(self, temp_project_dir):
        """Test integration of scheduled commit with file system"""
        with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.UnifiedAutoCommit') as mock_commit:
            mock_instance = Mock()
            mock_instance.run_complete_workflow_guaranteed.return_value = True
            mock_commit.return_value = mock_instance
            
            scheduler = ScheduledAutoCommit(temp_project_dir, interval_minutes=0.1)
            
            # Create a file change
            test_file = os.path.join(temp_project_dir, 'test.py')
            with open(test_file, 'w') as f:
                f.write("test content")
            
            # Manually trigger scheduled commit (simulating timer)
            scheduler._execute_scheduled_commit()
            
            # Verify auto-commit was called
            assert mock_instance.run_complete_workflow_guaranteed.called
    
    def test_git_change_detection_integration(self, temp_project_dir):
        """Test integration with Git change detection"""
        scheduler = ScheduledAutoCommit(temp_project_dir)
        
        # Initially should have no changes
        has_changes = scheduler._has_uncommitted_changes()
        assert has_changes == False
        
        # Create a file - should detect changes
        test_file = os.path.join(temp_project_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write("test content")
        
        has_changes = scheduler._has_uncommitted_changes()
        assert has_changes == True
    
    def test_service_lifecycle_integration(self, temp_project_dir):
        """Test complete service lifecycle integration"""
        with patch('autoprojectmanagement.services.automation_services.auto_file_watcher.Observer') as mock_observer:
            mock_observer_instance = Mock()
            mock_observer.return_value = mock_observer_instance
            
            service = AutoFileWatcherService(temp_project_dir, interval_minutes=0.1)
            
            # Test start
            service.start()
            assert service.running == True
            assert mock_observer_instance.start.called
            
            # Test stop
            service.stop()
            assert service.running == False
            assert mock_observer_instance.stop.called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
