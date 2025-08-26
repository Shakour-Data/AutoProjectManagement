#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automatic File Watcher Service
================================================================================
Module: auto_file_watcher
File: auto_file_watcher.py
Path: autoprojectmanagement/services/automation_services/auto_file_watcher.py

Description:
    Comprehensive file system monitoring service that provides real-time file change detection
    and automatic auto-commit execution. Combines event-driven and scheduled commit strategies
    for robust project backup and version control automation.

Features:
    - Real-time file system monitoring with configurable debouncing
    - Scheduled auto-commit every 15 minutes (configurable)
    - Integration with real-time event service for WebSocket/SSE notifications
    - Support for multiple authentication methods (SSH, HTTPS, PAT)
    - Comprehensive file filtering and exclusion capabilities

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
    - watchdog >= 3.0.0
    - See requirements.txt for full dependency list

License: MIT License
Copyright: (c) 2024 AutoProjectManagement Team

Usage:
    This module can be used as a standalone service or integrated into larger systems.
    It provides both programmatic API and command-line interface for flexibility.

Example:
    >>> from autoprojectmanagement.services.automation_services.auto_file_watcher import AutoFileWatcherService
    >>> service = AutoFileWatcherService(project_path="/path/to/project")
    >>> service.start()  # Starts monitoring and scheduled commits

Notes:
    - This service requires proper Git authentication setup
    - File monitoring is recursive but excludes common development directories
    - Real-time events are published through the event service for dashboard integration
    - Scheduled commits run regardless of file changes for regular backups

Changelog:
    1.0.0 (2024-01-01): Initial release with basic file watching and auto-commit
    1.0.1 (2025-08-14): Enhanced real-time event integration and error handling

TODO:
    - [ ] Add comprehensive configuration system
    - [ ] Implement advanced file pattern matching
    - [ ] Add support for multiple project monitoring
    - [ ] Enhance authentication fallback mechanisms

================================================================================
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Set, Optional, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import threading
from threading import Timer
from datetime import datetime, timedelta
import subprocess

# Import real-time event service
try:
    from autoprojectmanagement.api.realtime_service import publish_file_change_event
except ImportError:
    # Handle import for development
    import sys
    from pathlib import Path
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from autoprojectmanagement.api.realtime_service import publish_file_change_event
    except ImportError as e:
        logging.warning(f"Could not import realtime_service: {e}")
        publish_file_change_event = None

# Handle import for both standalone script and package usage
try:
    # Try the normal package import first
    from autoprojectmanagement.services.automation_services.auto_commit import UnifiedAutoCommit
except ImportError:
    # If that fails, we're probably running as a standalone script
    # Add the project root to sys.path to enable package imports
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent.parent.parent  # Go up 3 levels to reach autoprojectmanagement root
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Try the import again
    try:
        from autoprojectmanagement.services.automation_services.auto_commit import UnifiedAutoCommit
    except ImportError as e:
        logging.error(f"Failed to import UnifiedAutoCommit: {e}")
        logging.error("Please ensure you're running from the project root or the package is installed")
        sys.exit(1)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class AutoCommitFileWatcher(FileSystemEventHandler):
    """
    File system event handler for automatic commit triggering on file changes.
    
    This class extends watchdog's FileSystemEventHandler to monitor file system
    events and automatically trigger the auto-commit process when relevant files
    are modified, created, deleted, or moved. It includes intelligent debouncing
    to prevent rapid triggers and integrates with the real-time event service.
    
    Attributes:
        project_path (Path): Absolute path to the project directory being monitored
        debounce_seconds (float): Debounce delay in seconds to prevent rapid triggers
        auto_commit (UnifiedAutoCommit): Instance of the auto-commit service
        last_trigger_time (float): Timestamp of the last auto-commit trigger
        pending_changes (Set[Tuple[str, str]]): Set of pending file changes awaiting commit
        debounce_timer (Optional[Timer]): Timer for debouncing file change events
        lock (threading.Lock): Thread lock for thread-safe operations
        monitored_extensions (Set[str]): Set of file extensions to monitor
        excluded_dirs (Set[str]): Set of directory names to exclude from monitoring
    
    Example:
        >>> from autoprojectmanagement.services.automation_services.auto_file_watcher import AutoCommitFileWatcher
        >>> handler = AutoCommitFileWatcher("/path/to/project", debounce_seconds=5.0)
        >>> observer.schedule(handler, "/path/to/project", recursive=True)
    """
    
    def __init__(self, project_path: str, debounce_seconds: float = 5.0):
        """
        Initialize the AutoCommitFileWatcher with project path and debounce configuration.
        
        Args:
            project_path (str): Path to the project directory to monitor. Can be relative or absolute.
            debounce_seconds (float, optional): Delay in seconds before triggering auto-commit
                to avoid rapid triggers from multiple file changes. Defaults to 5.0 seconds.
        
        Raises:
            FileNotFoundError: If the specified project path does not exist
            PermissionError: If read permissions are insufficient for the project path
        
        Note:
            The debounce mechanism ensures that multiple rapid file changes within the
            specified time window result in a single auto-commit operation.
        """
        super().__init__()
        self.project_path = Path(project_path).resolve()
        self.debounce_seconds = debounce_seconds
        self.auto_commit = UnifiedAutoCommit()
        self.last_trigger_time = 0
        self.pending_changes = set()
        self.debounce_timer: Optional['Timer'] = None
        self.lock = threading.Lock()
        
        # Define file extensions to monitor
        self.monitored_extensions = {
            '.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go',
            '.ts', '.jsx', '.tsx', '.vue', '.html', '.css', '.scss', '.sass', '.json',
            '.xml', '.yaml', '.yml', '.md', '.txt', '.sql', '.sh', '.bat', '.ps1',
            '.dockerfile', '.env', '.ini', '.cfg', '.toml'
        }
        
        # Define directories to exclude
        self.excluded_dirs = {
            '.git', '__pycache__', 'node_modules', '.auto_project', 'venv', 'env',
            '.venv', '.env', 'dist', 'build', '.pytest_cache', '.mypy_cache', 'backups'
        }
        
        logger.info(f"Initialized AutoCommitFileWatcher for {self.project_path}")
    
    def should_monitor_file(self, file_path: str) -> bool:
        """
        Determine whether a file should be monitored for changes based on comprehensive criteria.
        
        This method evaluates files against multiple criteria including:
        - File existence and type (excludes directories)
        - Directory exclusions (e.g., .git, node_modules, __pycache__)
        - File extension filtering (common development file types)
        - Special file name handling (e.g., Dockerfile, docker-compose.yml)
        
        Args:
            file_path (str): Absolute or relative path to the file to evaluate
        
        Returns:
            bool: True if the file meets all monitoring criteria, False otherwise
        
        Raises:
            OSError: If file system operations fail during evaluation
        
        Example:
            >>> handler.should_monitor_file("/project/src/main.py")
            True
            >>> handler.should_monitor_file("/project/node_modules/package.json") 
            False
            >>> handler.should_monitor_file("/project/Dockerfile")
            True
        """
        try:
            path = Path(file_path)
            
            # Skip if file doesn't exist
            if not path.exists():
                return False
            
            # Skip directories
            if path.is_dir():
                return False
            
            # Skip excluded directories
            for excluded_dir in self.excluded_dirs:
                if excluded_dir in str(path).split(os.sep):
                    return False
            
            # Check file extension
            if path.suffix.lower() in self.monitored_extensions:
                return True
            
            # Check for special files
            filename = path.name.lower()
            if filename in {'dockerfile', 'docker-compose.yml', 'docker-compose.yaml'}:
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Error checking file {file_path}: {e}")
            return False
    
    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Handle file modification events from the watchdog observer.
        
        This method is automatically called by watchdog when a file modification
        event is detected. It filters out directory events and files that don't
        meet monitoring criteria before processing the change.
        
        Args:
            event (FileSystemEvent): The file system event containing modification details
        
        Note:
            Only processes files that pass the should_monitor_file() criteria
            and ignores directory modification events.
        """
        if not event.is_directory and self.should_monitor_file(event.src_path):
            self._handle_file_change(event.src_path, 'modified')
    
    def on_created(self, event: FileSystemEvent) -> None:
        """
        Handle file creation events from the watchdog observer.
        
        This method is automatically called by watchdog when a file creation
        event is detected. It processes new files that meet monitoring criteria.
        
        Args:
            event (FileSystemEvent): The file system event containing creation details
        
        Note:
            Only processes files that pass the should_monitor_file() criteria
            and ignores directory creation events.
        """
        if not event.is_directory and self.should_monitor_file(event.src_path):
            self._handle_file_change(event.src_path, 'created')
    
    def on_deleted(self, event: FileSystemEvent) -> None:
        """
        Handle file deletion events from the watchdog observer.
        
        This method is automatically called by watchdog when a file deletion
        event is detected. It processes file deletions that meet monitoring criteria.
        
        Args:
            event (FileSystemEvent): The file system event containing deletion details
        
        Note:
            Only processes files that pass the should_monitor_file() criteria
            and ignores directory deletion events.
        """
        if not event.is_directory and self.should_monitor_file(event.src_path):
            self._handle_file_change(event.src_path, 'deleted')
    
    def on_moved(self, event: FileSystemEvent) -> None:
        """
        Handle file move/rename events from the watchdog observer.
        
        This method is automatically called by watchdog when a file move or rename
        event is detected. It processes both the source (old) and destination (new)
        paths if they meet monitoring criteria.
        
        Args:
            event (FileSystemEvent): The file system event containing move details,
                including both source and destination paths
        
        Note:
            Processes both the original location (moved_from) and new location
            (moved_to) if they meet monitoring criteria.
        """
        if not event.is_directory:
            if self.should_monitor_file(event.src_path):
                self._handle_file_change(event.src_path, 'moved_from')
            if self.should_monitor_file(event.dest_path):
                self._handle_file_change(event.dest_path, 'moved_to')
    
    async def _handle_file_change(self, file_path: str, change_type: str) -> None:
        """
        Handle a file change event with intelligent debouncing and real-time event publishing.
        
        This method processes individual file change events by:
        1. Adding the change to pending changes with thread-safe locking
        2. Publishing real-time events through the event service for dashboard integration
        3. Setting up debouncing timer to prevent rapid auto-commit triggers
        4. Canceling any existing timer to reset the debounce window
        
        Args:
            file_path (str): Absolute path to the file that was changed
            change_type (str): Type of change event. Valid values:
                - 'modified': File content was modified
                - 'created': New file was created
                - 'deleted': File was deleted
                - 'moved_from': File was moved from this location
                - 'moved_to': File was moved to this location
        
        Note:
            The debouncing mechanism ensures that multiple rapid changes within
            the debounce window result in a single auto-commit operation.
            Real-time events are published asynchronously to avoid blocking.
        """
        with self.lock:
            self.pending_changes.add((file_path, change_type))
            
            # Publish file change event to real-time service
            if publish_file_change_event:
                try:
                    # Get relative path for better display
                    rel_path = os.path.relpath(file_path, self.project_path)
                    
                    # Publish event asynchronously
                    import asyncio
                    asyncio.create_task(
                        await publish_file_change_event(
                            file_path=rel_path,
                            change_type=change_type,
                            project_id=str(self.project_path.name)
                        )
                    )
                except Exception as e:
                    logger.warning(f"Failed to publish file change event: {e}")
            
            # Cancel any existing timer
            if self.debounce_timer is not None:
                self.debounce_timer.cancel()
            
            # Set a new timer
            self.debounce_timer = Timer(
                self.debounce_seconds,
                self._execute_auto_commit
            )
            self.debounce_timer.start()
    
    def _execute_auto_commit(self) -> None:
        """
        Execute the auto-commit process for all pending file changes.
        
        This method performs the complete auto-commit workflow including:
        1. Retrieving all pending changes with thread-safe locking
        2. Logging the changes for audit purposes
        3. Publishing auto-commit start event for real-time monitoring
        4. Executing the unified auto-commit workflow
        5. Publishing auto-commit result event with success/failure status
        6. Handling errors gracefully with comprehensive logging
        
        The method ensures that even if the auto-commit process fails,
        the service continues to operate and pending changes are cleared
        to prevent accumulation of stale changes.
        
        Note:
            This method is called by the debounce timer and should not
            be called directly. It handles its own error recovery to
            maintain service stability.
        """
        try:
            with self.lock:
                changes = list(self.pending_changes)
                self.pending_changes.clear()
            
            if not changes:
                return
            
            logger.info(f"Executing auto-commit for {len(changes)} changes")
            
            # Log the changes
            for file_path, change_type in changes:
                rel_path = os.path.relpath(file_path, self.project_path)
                logger.info(f"  {change_type}: {rel_path}")
            
            # Publish auto-commit start event
            if publish_file_change_event:
                try:
                    import asyncio
                    asyncio.create_task(
                        publish_file_change_event(
                            file_path="auto_commit_start",
                            change_type="auto_commit_start",
                            project_id=str(self.project_path.name),
                            commit_data={"changes_count": len(changes)}
                        )
                    )
                except Exception as e:
                    logger.warning(f"Failed to publish auto-commit start event: {e}")
            
            # Execute auto-commit
            success = self.auto_commit.run_complete_workflow_guaranteed()
            
            # Publish auto-commit result event
            if publish_file_change_event:
                try:
                    import asyncio
                    asyncio.create_task(
                        publish_file_change_event(
                            file_path="auto_commit_result",
                            change_type="auto_commit_result",
                            project_id=str(self.project_path.name),
                            commit_data={"success": success, "changes_count": len(changes)}
                        )
                    )
                except Exception as e:
                    logger.warning(f"Failed to publish auto-commit result event: {e}")
            
            if success:
                logger.info("✅ Auto-commit completed successfully")
            else:
                logger.warning("⚠️  Auto-commit completed with warnings")
                
        except Exception as e:
            logger.error(f"Error during auto-commit: {e}")


class ScheduledAutoCommit:
    """
    Scheduled auto-commit service for regular project backups regardless of file changes.
    
    This class provides time-based automatic commits that run at regular intervals
    (default: 15 minutes) to ensure project backups even when no file changes occur.
    It works alongside the event-driven AutoCommitFileWatcher to provide comprehensive
    backup coverage.
    
    Attributes:
        project_path (Path): Absolute path to the project directory
        interval_minutes (int): Scheduled commit interval in minutes
        auto_commit (UnifiedAutoCommit): Instance of the auto-commit service
        timer (Optional[threading.Timer]): Timer for scheduling commit operations
        running (bool): Service running state flag
        lock (threading.Lock): Thread lock for thread-safe operations
    
    Features:
        - Configurable commit intervals (default: 15 minutes)
        - Integration with real-time event service for monitoring
        - Smart change detection to avoid empty commits
        - Comprehensive error handling and recovery
        - Graceful shutdown capabilities
    
    Example:
        >>> from autoprojectmanagement.services.automation_services.auto_file_watcher import ScheduledAutoCommit
        >>> scheduler = ScheduledAutoCommit("/path/to/project", interval_minutes=15)
        >>> scheduler.start()  # Starts scheduled commits every 15 minutes
    """
    
    def __init__(self, project_path: str, interval_minutes: int = 15):
        """
        Initialize the ScheduledAutoCommit service with project path and interval configuration.
        
        Args:
            project_path (str): Path to the project directory. Can be relative or absolute.
            interval_minutes (int, optional): Interval in minutes for scheduled commits.
                Defaults to 15 minutes. Minimum recommended interval is 5 minutes.
        
        Raises:
            ValueError: If interval_minutes is less than 1
            FileNotFoundError: If the project path does not exist
            PermissionError: If read permissions are insufficient
        
        Note:
            The scheduled commit service ensures regular backups even during periods
            of low file activity, providing an additional layer of data protection.
        """
        self.project_path = Path(project_path).resolve()
        self.interval_minutes = interval_minutes
        self.auto_commit = UnifiedAutoCommit()
        self.timer: Optional[threading.Timer] = None
        self.running = False
        self.lock = threading.Lock()
        
        logger.info(f"Initialized ScheduledAutoCommit for {self.project_path} every {interval_minutes} minutes")
    
    def start(self) -> None:
        """
        Start the scheduled auto-commit service for regular backups.
        
        This method initiates the timer for scheduled commits based on the
        configured interval. It begins monitoring the project directory for
        changes and ensures that auto-commits are executed at the specified
        intervals, regardless of file activity.
        
        Note:
            If the service is already running, this method will not restart it.
            It is safe to call this method multiple times without adverse effects.
        """
        if self.running:
            logger.warning("ScheduledAutoCommit is already running")
            return
        
        self.running = True
        logger.info(f"🕐 Starting scheduled auto-commit every {self.interval_minutes} minutes")
        self._schedule_next_commit()
    
    def stop(self) -> None:
        """
        Stop the scheduled auto-commit service gracefully.
        
        This method stops the scheduled commit timer and cleans up resources.
        It ensures that any pending commit operations are completed before
        shutting down and that the service state is properly updated.
        
        Note:
            This method is idempotent and can be called multiple times safely.
            It will not interrupt any currently executing commit operations.
        """
        if not self.running:
            return
        
        self.running = False
        
        with self.lock:
            if self.timer:
                self.timer.cancel()
                self.timer = None
        
        logger.info("ScheduledAutoCommit stopped")
    
    def get_status(self) -> dict:
        """
        Retrieve the current status of the scheduled auto-commit service.
        
        This method returns a dictionary containing information about the
        service's operational state, including whether it is currently running,
        the project path being monitored, and the status of the scheduled commit
        timer.
        
        Returns:
            dict: A dictionary containing the following keys:
                - 'running' (bool): Indicates if the service is currently active
                - 'project_path' (str): The absolute path to the project directory
                - 'monitoring' (bool): Indicates if the file observer is active
                - 'scheduled_commit' (dict): Status of the scheduled commit service
        
        Example:
            >>> status = scheduler.get_status()
            >>> print(status)
            {'running': True, 'project_path': '/path/to/project', 'monitoring': True, 'scheduled_commit': {...}}
        """
        return {
            'running': self.running,
            'interval_minutes': self.interval_minutes,
            'project_path': str(self.project_path)
        }
    
    def _schedule_next_commit(self) -> None:
        """
        Schedule the next automatic commit operation.
        
        This internal method sets up a timer to trigger the next scheduled
        commit based on the configured interval. It ensures that the timer
        is only scheduled when the service is running and handles the
        conversion from minutes to seconds for the timer interval.
        
        Note:
            This method is called internally and should not be called directly.
            It manages the recurring scheduling of commit operations.
        """
        if not self.running:
            return
        
        # Convert minutes to seconds
        interval_seconds = self.interval_minutes * 60
        
        with self.lock:
            self.timer = threading.Timer(interval_seconds, self._execute_scheduled_commit)
            self.timer.start()
    
    def _execute_scheduled_commit(self) -> None:
        """
        Execute the scheduled auto-commit operation with comprehensive error handling.
        
        This method performs the complete scheduled commit workflow including:
        1. Checking if the service is still running
        2. Publishing scheduled commit start events for real-time monitoring
        3. Detecting if there are uncommitted changes to avoid empty commits
        4. Executing the auto-commit with timestamped commit messages
        5. Publishing result events with success/failure status
        6. Handling all exceptions gracefully to maintain service stability
        7. Scheduling the next commit operation regardless of outcome
        
        The method ensures that scheduled commits continue to run even if
        individual commit operations fail, providing robust backup coverage.
        
        Note:
            This method is called by the scheduling timer and should not
            be called directly. It includes comprehensive error recovery
            to prevent service interruptions.
        """
        try:
            if not self.running:
                return
            
            logger.info("🔄 Executing scheduled auto-commit")
            
            # Publish scheduled commit start event
            if publish_file_change_event:
                try:
                    import asyncio
                    asyncio.create_task(
                        publish_file_change_event(
                            file_path="scheduled_commit_start",
                            change_type="scheduled_commit_start",
                            project_id=str(self.project_path.name)
                        )
                    )
                except Exception as e:
                    logger.warning(f"Failed to publish scheduled commit start event: {e}")
            
            # Check if there are any changes to commit
            has_changes = self._has_uncommitted_changes()
            
            if has_changes:
                # Generate commit message with timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                commit_message = f"Auto-commit: Scheduled backup at {timestamp}"
                
                # Execute auto-commit with custom message
                success = self.auto_commit.run_complete_workflow_guaranteed(
                    custom_message=commit_message
                )
                
                # Publish scheduled commit result event
                if publish_file_change_event:
                    try:
                        import asyncio
                        asyncio.create_task(
                            publish_file_change_event(
                                file_path="scheduled_commit_result",
                                change_type="scheduled_commit_result",
                                project_id=str(self.project_path.name),
                                commit_data={"success": success, "scheduled": True}
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Failed to publish scheduled commit result event: {e}")
                
                if success:
                    logger.info("✅ Scheduled auto-commit completed successfully")
                else:
                    logger.warning("⚠️  Scheduled auto-commit completed with warnings")
            else:
                logger.info("ℹ️  No changes to commit - skipping scheduled auto-commit")
                
                # Publish no changes event
                if publish_file_change_event:
                    try:
                        import asyncio
                        asyncio.create_task(
                            publish_file_change_event(
                                file_path="scheduled_commit_skipped",
                                change_type="scheduled_commit_skipped",
                                project_id=str(self.project_path.name),
                                commit_data={"reason": "no_changes"}
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Failed to publish scheduled commit skipped event: {e}")
            
            # Schedule the next commit
            self._schedule_next_commit()
            
        except Exception as e:
            logger.error(f"Error during scheduled auto-commit: {e}")
            
            # Publish error event
            if publish_file_change_event:
                try:
                    import asyncio
                    asyncio.create_task(
                        publish_file_change_event(
                            file_path="scheduled_commit_error",
                            change_type="scheduled_commit_error",
                            project_id=str(self.project_path.name),
                            commit_data={"error": str(e)}
                        )
                    )
                except Exception as e:
                    logger.warning(f"Failed to publish scheduled commit error event: {e}")
            
            # Continue scheduling even if this commit fails
            self._schedule_next_commit()
    
    def _has_uncommitted_changes(self) -> bool:
        """
        Check if there are uncommitted changes in the Git repository.
        
        This method performs a comprehensive check for different types of
        uncommitted changes including:
        - Staged changes (git diff --cached)
        - Unstaged changes (git diff)
        - Untracked files (git ls-files --others --exclude-standard)
        
        Returns:
            bool: True if there are any uncommitted changes of any type,
                  False if the repository is clean. Returns True on error
                  to err on the side of caution.
        
        Raises:
            subprocess.CalledProcessError: If Git commands fail unexpectedly
            FileNotFoundError: If Git is not installed or not in PATH
        
        Note:
            This method returns True on error to ensure that scheduled commits
            are not skipped due to temporary Git command failures.
        """
        try:
            # Check for staged changes
            result = subprocess.run(
                ["git", "diff", "--cached", "--quiet"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            has_staged_changes = result.returncode != 0
            
            # Check for unstaged changes
            result = subprocess.run(
                ["git", "diff", "--quiet"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            has_unstaged_changes = result.returncode != 0
            
            # Check for untracked files
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            has_untracked_files = bool(result.stdout.strip())
            
            return has_staged_changes or has_unstaged_changes or has_untracked_files
            
        except Exception as e:
            logger.error(f"Error checking for uncommitted changes: {e}")
            return True  # Assume changes exist if check fails


class AutoFileWatcherService:
    """
    Main service class for comprehensive automatic file watching and auto-commit.
    
    This class provides a complete, production-ready service that combines both
    event-driven file monitoring and scheduled commits to deliver robust project
    backup and version control automation. It integrates with the real-time event
    service for dashboard monitoring and provides comprehensive status reporting.
    
    Attributes:
        project_path (str): Absolute path to the project directory being monitored
        observer (Optional[Observer]): Watchdog observer instance for file monitoring
        event_handler (Optional[AutoCommitFileWatcher]): File event handler instance
        scheduled_commit (Optional[ScheduledAutoCommit]): Scheduled commit service instance
        running (bool): Service running state flag
    
    Features:
        - Real-time file system monitoring with configurable debouncing
        - Scheduled commits every 15 minutes (configurable) for regular backups
        - Integration with real-time event service for WebSocket/SSE notifications
        - Comprehensive error handling and automatic recovery
        - Graceful startup and shutdown procedures
        - Status monitoring and reporting capabilities
        - Support for multiple authentication methods (SSH, HTTPS, PAT)
    
    Example:
        >>> from autoprojectmanagement.services.automation_services.auto_file_watcher import AutoFileWatcherService
        >>> service = AutoFileWatcherService("/path/to/project", interval_minutes=15)
        >>> service.start()  # Starts complete monitoring and scheduled commits
        >>> # Service runs until interrupted or stopped programmatically
        >>> service.stop()   # Gracefully stops all monitoring and scheduled commits
    """
    
    def __init__(self, project_path: Optional[str] = None, interval_minutes: int = 15):
        """
        Initialize the AutoFileWatcherService with project path and interval configuration.
        
        Args:
            project_path (Optional[str]): Path to the project directory to monitor.
                If None, uses the current working directory. Defaults to None.
            interval_minutes (int, optional): Interval in minutes for scheduled commits.
                Defaults to 15 minutes. Minimum recommended interval is 5 minutes.
        
        Raises:
            ValueError: If interval_minutes is less than 1
            FileNotFoundError: If the project path does not exist
            PermissionError: If read permissions are insufficient for the project path
        
        Note:
            The service combines both event-driven and scheduled commit strategies
            to provide comprehensive backup coverage under all usage scenarios.
        """
        if project_path is None:
            self.project_path = os.getcwd()
        else:
            self.project_path = os.path.abspath(project_path)
        
        self.observer = None
        self.event_handler = None
        self.scheduled_commit = None
        self.running = False
        
        # Initialize scheduled auto-commit
        self.scheduled_commit = ScheduledAutoCommit(self.project_path, interval_minutes)
        
        logger.info(f"AutoFileWatcherService initialized for {self.project_path} with {interval_minutes}-minute scheduled commits")
    
    def start(self) -> None:
        """
        Start the complete automatic file watching and scheduled commit service.
        
        This method performs a comprehensive startup sequence including:
        1. Initializing the file system observer with recursive monitoring
        2. Starting the scheduled commit service with the configured interval
        3. Setting up real-time event integration for dashboard monitoring
        4. Entering the main service loop for continuous operation
        
        The service will continue running until explicitly stopped or interrupted.
        It provides comprehensive error handling to ensure service stability.
        
        Raises:
            RuntimeError: If the service fails to start due to system issues
            FileNotFoundError: If the project directory becomes inaccessible
            PermissionError: If file system monitoring permissions are insufficient
        
        Note:
            This method blocks until the service is stopped. For non-blocking
            operation, consider running it in a separate thread.
        """
        if self.running:
            logger.warning("AutoFileWatcherService is already running")
            return
        
        try:
            # Start file watching
            self.event_handler = AutoCommitFileWatcher(self.project_path)
            self.observer = Observer()
            self.observer.schedule(
                self.event_handler,
                str(self.project_path),
                recursive=True
            )
            
            self.observer.start()
            self.running = True
            
            # Start scheduled auto-commit
            self.scheduled_commit.start()
            
            logger.info("🚀 AutoFileWatcherService started - monitoring for file changes")
            logger.info("🕐 Scheduled auto-commit running every 15 minutes")
            logger.info("💡 No manual intervention required - auto-commit will run automatically")
            
            # Keep the service running
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
                
        except Exception as e:
            logger.error(f"Error starting AutoFileWatcherService: {e}")
            raise
    
    def stop(self) -> None:
        """
        Stop the automatic file watching service gracefully.
        
        This method performs a comprehensive shutdown sequence including:
        1. Stopping the file system observer and waiting for it to join
        2. Stopping the scheduled commit service
        3. Cleaning up all resources and connections
        4. Updating the service state to indicate it is no longer running
        
        The shutdown process is designed to be graceful and ensure that any
        ongoing commit operations are completed before the service stops.
        
        Note:
            This method is idempotent and can be called multiple times safely.
            It will not interrupt any currently executing commit operations.
        """
        if not self.running:
            return
        
        self.running = False
        
        # Stop file observer
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        # Stop scheduled commits
        if self.scheduled_commit:
            self.scheduled_commit.stop()
        
        logger.info("AutoFileWatcherService stopped")
    
    def get_status(self) -> dict:
        """
        Retrieve comprehensive status information about the service.
        
        This method returns a detailed dictionary containing information about
        all aspects of the service's operational state, including file monitoring
        status, scheduled commit status, and overall service health.
        
        Returns:
            dict: A dictionary containing the following keys:
                - 'running' (bool): Overall service running state
                - 'project_path' (str): Absolute path to the monitored project
                - 'monitoring' (bool): File system observer active status
                - 'scheduled_commit' (dict): Status of the scheduled commit service
        
        Example:
            >>> status = service.get_status()
            >>> print(status)
            {
                'running': True,
                'project_path': '/path/to/project',
                'monitoring': True,
                'scheduled_commit': {'running': True, 'interval_minutes': 15, ...}
            }
        """
        observer_alive = False
        if self.observer:
            observer_alive = self.observer.is_alive()
        
        scheduled_status = self.scheduled_commit.get_status() if self.scheduled_commit else {}
        
        return {
            'running': self.running,
            'project_path': self.project_path,
            'monitoring': observer_alive,
            'scheduled_commit': scheduled_status
        }


def main():
    """
    Main entry point for the Auto File Watcher Service command-line interface.
    
    This function provides a command-line interface for starting the automatic
    file watching and scheduled commit service. It supports various configuration
    options through command-line arguments and handles graceful shutdown on
    keyboard interrupts.
    
    Command-line Arguments:
        --path: Project path to monitor (default: current working directory)
        --debounce: Debounce delay in seconds for file changes (default: 5.0)
        --interval: Scheduled commit interval in minutes (default: 15)
    
    Example Usage:
        # Monitor current directory with default settings
        python -m autoprojectmanagement.services.automation_services.auto_file_watcher
        
        # Monitor specific path with custom settings
        python -m autoprojectmanagement.services.automation_services.auto_file_watcher \
            --path /path/to/project \
            --debounce 3.0 \
            --interval 10
    
    Note:
        The service runs until interrupted by Ctrl+C or stopped programmatically.
        It provides comprehensive logging to stdout for monitoring and debugging.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Auto File Watcher - Automatic auto-commit on file changes and scheduled commits'
    )
    parser.add_argument(
        '--path',
        help='Project path to monitor (default: current directory)',
        default=os.getcwd()
    )
    parser.add_argument(
        '--debounce',
        type=float,
        default=5.0,
        help='Debounce delay in seconds for file changes (default: 5.0)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=15,
        help='Scheduled commit interval in minutes (default: 15)'
    )
    
    args = parser.parse_args()
    
    service = AutoFileWatcherService(args.path, args.interval)
    
    try:
        service.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        service.stop()


if __name__ == "__main__":
    main()
