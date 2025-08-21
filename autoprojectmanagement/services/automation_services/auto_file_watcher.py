#!/usr/bin/env python3
"""
Automatic File Watcher Service for AutoProjectManagement
Purpose: Provides real-time file monitoring and automatic auto-commit execution
Author: AutoProjectManagement System
Version: 1.0.0
License: MIT
Description: Monitors file system changes and triggers auto-commit automatically
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

# Import the auto-commit service
from autoprojectmanagement.services.automation_services.auto_commit import UnifiedAutoCommit

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class AutoCommitFileWatcher(FileSystemEventHandler):
    """
    File system event handler that triggers auto-commit on file changes.
    
    This class monitors file system events and automatically triggers
    the auto-commit process when relevant files are modified.
    """
    
    def __init__(self, project_path: str, debounce_seconds: float = 5.0):
        """
        Initialize the file watcher.
        
        Args:
            project_path: Path to the project directory to monitor
            debounce_seconds: Delay before triggering auto-commit to avoid rapid triggers
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
            '.venv', '.env', 'dist', 'build', '.pytest_cache', '.mypy_cache'
        }
        
        logger.info(f"Initialized AutoCommitFileWatcher for {self.project_path}")
    
    def should_monitor_file(self, file_path: str) -> bool:
        """
        Determine if a file should be monitored for changes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            bool: True if the file should be monitored
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
        """Handle file modification events."""
        if not event.is_directory and self.should_monitor_file(event.src_path):
            self._handle_file_change(event.src_path, 'modified')
    
    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        if not event.is_directory and self.should_monitor_file(event.src_path):
            self._handle_file_change(event.src_path, 'created')
    
    def on_deleted(self, event: FileSystemEvent) -> None:
        """Handle file deletion events."""
        if not event.is_directory and self.should_monitor_file(event.src_path):
            self._handle_file_change(event.src_path, 'deleted')
    
    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle file move/rename events."""
        if not event.is_directory:
            if self.should_monitor_file(event.src_path):
                self._handle_file_change(event.src_path, 'moved_from')
            if self.should_monitor_file(event.dest_path):
                self._handle_file_change(event.dest_path, 'moved_to')
    
    def _handle_file_change(self, file_path: str, change_type: str) -> None:
        """
        Handle a file change event with debouncing.
        
        Args:
            file_path: Path to the changed file
            change_type: Type of change (created, modified, deleted, etc.)
        """
        with self.lock:
            self.pending_changes.add((file_path, change_type))
            
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
        """Execute the auto-commit process for pending changes."""
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
            
            # Execute auto-commit
            success = self.auto_commit.run_complete_workflow_guaranteed()
            
            if success:
                logger.info("✅ Auto-commit completed successfully")
            else:
                logger.warning("⚠️  Auto-commit completed with warnings")
                
        except Exception as e:
            logger.error(f"Error during auto-commit: {e}")


class AutoFileWatcherService:
    """
    Main service class for automatic file watching and auto-commit.
    
    This class provides a complete service that monitors file system changes
    and automatically triggers auto-commit without any manual intervention.
    """
    
    def __init__(self, project_path: Optional[str] = None):
        """
        Initialize the auto file watcher service.
        
        Args:
            project_path: Path to the project directory. If None, uses current directory.
        """
        if project_path is None:
            self.project_path = os.getcwd()
        else:
            self.project_path = os.path.abspath(project_path)
        
        self.observer = None
        self.event_handler = None
        self.running = False
        
        logger.info(f"AutoFileWatcherService initialized for {self.project_path}")
    
    def start(self) -> None:
        """
        Start the automatic file watching service.
        
        This method begins monitoring the project directory for file changes
        and automatically triggers auto-commit when changes are detected.
        """
        if self.running:
            logger.warning("AutoFileWatcherService is already running")
            return
        
        try:
            self.event_handler = AutoCommitFileWatcher(self.project_path)
            self.observer = Observer()
            self.observer.schedule(
                self.event_handler,
                str(self.project_path),
                recursive=True
            )
            
            self.observer.start()
            self.running = True
            
            logger.info("🚀 AutoFileWatcherService started - monitoring for file changes")
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
        """Stop the automatic file watching service."""
        if not self.running:
            return
        
        self.running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        logger.info("AutoFileWatcherService stopped")
    
    def get_status(self) -> dict:
        """Get the current status of the service."""
        observer_alive = False
        if self.observer:
            observer_alive = self.observer.is_alive()
        
        return {
            'running': self.running,
            'project_path': self.project_path,
            'monitoring': observer_alive
        }


def main():
    """Main entry point for the auto file watcher service."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Auto File Watcher - Automatic auto-commit on file changes'
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
        help='Debounce delay in seconds (default: 5.0)'
    )
    
    args = parser.parse_args()
    
    service = AutoFileWatcherService(args.path)
    
    try:
        service.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        service.stop()


if __name__ == "__main__":
    main()