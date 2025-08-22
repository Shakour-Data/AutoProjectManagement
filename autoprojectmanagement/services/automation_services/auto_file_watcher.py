#!/usr/bin/env python3
"""
Automatic File Watcher Service for AutoProjectManagement
Purpose: Provides real-time file monitoring and automatic auto-commit execution
Author: AutoProjectManagement System
Version: 1.0.0
License: MIT
Description: Monitors file system changes and automatically triggers auto-commit every 15 minutes
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
            '.venv', '.env', 'dist', 'build', '.pytest_cache', '.mypy_cache', 'backups'
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
            
            # Publish file change event to real-time service
            if publish_file_change_event:
                try:
                    # Get relative path for better display
                    rel_path = os.path.relpath(file_path, self.project_path)
                    
                    # Publish event asynchronously
                    import asyncio
                    asyncio.create_task(
                        publish_file_change_event(
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
    Scheduled auto-commit service that runs every 15 minutes.
    
    This class provides scheduled automatic commits and pushes regardless of
    file system events, ensuring regular backups every 15 minutes.
    """
    
    def __init__(self, project_path: str, interval_minutes: int = 15):
        """
        Initialize the scheduled auto-commit service.
        
        Args:
            project_path: Path to the project directory
            interval_minutes: Interval in minutes for scheduled commits (default: 15)
        """
        self.project_path = Path(project_path).resolve()
        self.interval_minutes = interval_minutes
        self.auto_commit = UnifiedAutoCommit()
        self.timer: Optional[threading.Timer] = None
        self.running = False
        self.lock = threading.Lock()
        
        logger.info(f"Initialized ScheduledAutoCommit for {self.project_path} every {interval_minutes} minutes")
    
    def start(self) -> None:
        """Start the scheduled auto-commit service."""
        if self.running:
            logger.warning("ScheduledAutoCommit is already running")
            return
        
        self.running = True
        logger.info(f"🕐 Starting scheduled auto-commit every {self.interval_minutes} minutes")
        self._schedule_next_commit()
    
    def stop(self) -> None:
        """Stop the scheduled auto-commit service."""
        if not self.running:
            return
        
        self.running = False
        
        with self.lock:
            if self.timer:
                self.timer.cancel()
                self.timer = None
        
        logger.info("ScheduledAutoCommit stopped")
    
    def get_status(self) -> dict:
        """Get the current status of the scheduled auto-commit service."""
        return {
            'running': self.running,
            'interval_minutes': self.interval_minutes,
            'project_path': str(self.project_path)
        }
    
    def _schedule_next_commit(self) -> None:
        """Schedule the next automatic commit."""
        if not self.running:
            return
        
        # Convert minutes to seconds
        interval_seconds = self.interval_minutes * 60
        
        with self.lock:
            self.timer = threading.Timer(interval_seconds, self._execute_scheduled_commit)
            self.timer.start()
    
    def _execute_scheduled_commit(self) -> None:
        """Execute the scheduled auto-commit and push."""
        try:
            if not self.running:
                return
            
            logger.info("🔄 Executing scheduled auto-commit")
            
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
                
                if success:
                    logger.info("✅ Scheduled auto-commit completed successfully")
                else:
                    logger.warning("⚠️  Scheduled auto-commit completed with warnings")
            else:
                logger.info("ℹ️  No changes to commit - skipping scheduled auto-commit")
            
            # Schedule the next commit
            self._schedule_next_commit()
            
        except Exception as e:
            logger.error(f"Error during scheduled auto-commit: {e}")
            # Continue scheduling even if this commit fails
            self._schedule_next_commit()
    
    def _has_uncommitted_changes(self) -> bool:
        """
        Check if there are uncommitted changes in the repository.
        
        Returns:
            bool: True if there are uncommitted changes, False otherwise
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
    Main service class for automatic file watching and auto-commit.
    
    This class provides a complete service that monitors file system changes
    and automatically triggers auto-commit every 15 minutes, combining both
    event-driven and scheduled commits.
    """
    
    def __init__(self, project_path: Optional[str] = None, interval_minutes: int = 15):
        """
        Initialize the auto file watcher service.
        
        Args:
            project_path: Path to the project directory. If None, uses current directory.
            interval_minutes: Interval in minutes for scheduled commits (default: 15)
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
        Start the automatic file watching service.
        
        This method begins monitoring the project directory for file changes
        and starts the scheduled auto-commit every 15 minutes.
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
        """Stop the automatic file watching service."""
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
        """Get the current status of the service."""
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
    """Main entry point for the auto file watcher service."""
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
