#!/usr/bin/env python3
"""
Auto Runner Module - Provides automatic project management without user interaction
"""

import os
import sys
import time
import json
import logging
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .main_modules.project_management_system import ProjectManagementSystem
from .main_modules.task_management import TaskManager
from .main_modules.progress_calculator_refactored import ProgressCalculator
from .main_modules.git_progress_updater import GitProgressUpdater
from .services.auto_commit import AutoCommit
from .services.github_integration import GitHubIntegration

class AutoRunner:
    """Main class for automatic project management"""
    
    def __init__(self, project_path=None):
        self.project_path = project_path or os.getcwd()
        self.system = ProjectManagementSystem()
        self.task_manager = TaskManager()
        self.progress_calculator = ProgressCalculator()
        self.git_updater = GitProgressUpdater()
        self.auto_commit = AutoCommit()
        self.github_integration = GitHubIntegration()
        
        self.observer = None
        self.running = False
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for auto runner"""
        log_dir = os.path.join(self.project_path, '.auto_project_logs')
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'auto_runner.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('AutoRunner')
        
    def initialize_environment(self):
        """Initialize the automatic project management environment"""
        self.logger.info("Initializing automatic project management environment...")
        
        # Initialize system
        self.system.initialize_system()
        
        # Setup file monitoring
        self.setup_file_monitoring()
        
        # Start background services
        self.start_background_services()
        
        self.logger.info("Environment initialized successfully")
        
    def setup_file_monitoring(self):
        """Setup file system monitoring for automatic updates"""
        event_handler = ProjectFileHandler(self)
        self.observer = Observer()
        self.observer.schedule(
            event_handler, 
            self.project_path, 
            recursive=True
        )
        
    def start_background_services(self):
        """Start background services for automatic management"""
        services = [
            self.auto_commit_service,
            self.progress_tracking_service,
            self.risk_assessment_service,
            self.report_generation_service
        ]
        
        for service in services:
            thread = threading.Thread(target=service, daemon=True)
            thread.start()
            
    def auto_commit_service(self):
        """Automatic commit service"""
        while self.running:
            try:
                changes = self.detect_code_changes()
                if changes:
                    self.auto_commit.process_changes(changes)
                    self.update_progress()
                time.sleep(300)  # Check every 5 minutes
            except Exception as e:
                self.logger.error(f"Error in auto commit service: {e}")
                
    def progress_tracking_service(self):
        """Automatic progress tracking service"""
        while self.running:
            try:
                self.calculate_progress()
                self.update_dashboards()
                time.sleep(600)  # Update every 10 minutes
            except Exception as e:
                self.logger.error(f"Error in progress tracking service: {e}")
                
    def risk_assessment_service(self):
        """Automatic risk assessment service"""
        while self.running:
            try:
                self.assess_risks()
                time.sleep(3600)  # Check every hour
            except Exception as e:
                self.logger.error(f"Error in risk assessment service: {e}")
                
    def report_generation_service(self):
        """Automatic report generation service"""
        while self.running:
            try:
                self.generate_reports()
                time.sleep(86400)  # Generate daily reports
            except Exception as e:
                self.logger.error(f"Error in report generation service: {e}")
                
    def detect_code_changes(self):
        """Detect changes in code files"""
        changes = []
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(('.py', '.js', '.java', '.cpp', '.c', '.h')):
                    file_path = os.path.join(root, file)
                    # Check for recent changes
                    stat = os.stat(file_path)
                    if time.time() - stat.st_mtime < 300:  # Changed in last 5 minutes
                        changes.append({
                            'file': file_path,
                            'type': 'code_change',
                            'timestamp': stat.st_mtime
                        })
        return changes
        
    def calculate_progress(self):
        """Calculate project progress automatically"""
        try:
            progress = self.progress_calculator.calculate_project_progress()
            self.logger.info(f"Project progress: {progress}%")
            return progress
        except Exception as e:
            self.logger.error(f"Error calculating progress: {e}")
            return 0
            
    def update_progress(self):
        """Update project progress based on changes"""
        progress = self.calculate_progress()
        self.update_project_status(progress)
        
    def update_project_status(self, progress):
        """Update project status in system"""
        # This would integrate with the project management system
        pass
        
    def assess_risks(self):
        """Automatically assess project risks"""
        # This would integrate with risk management modules
        pass
        
    def generate_reports(self):
        """Automatically generate project reports"""
        # This would integrate with reporting modules
        pass
        
    def update_dashboards(self):
        """Update project dashboards"""
        # This would integrate with dashboard modules
        pass
        
    def start(self):
        """Start the automatic project management"""
        self.logger.info("Starting automatic project management...")
        self.running = True
        
        # Initialize environment
        self.initialize_environment()
        
        # Start file monitoring
        self.observer.start()
        
        # Keep running
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
            
    def stop(self):
        """Stop the automatic project management"""
        self.logger.info("Stopping automatic project management...")
        self.running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
            
    def get_status(self):
        """Get current status of automatic management"""
        return {
            'running': self.running,
            'project_path': self.project_path,
            'last_update': time.time(),
            'services': {
                'auto_commit': 'running',
                'progress_tracking': 'running',
                'risk_assessment': 'running',
                'report_generation': 'running'
            }
        }


class ProjectFileHandler(FileSystemEventHandler):
    """File system event handler for project changes"""
    
    def __init__(self, auto_runner):
        self.auto_runner = auto_runner
        self.logger = logging.getLogger('FileHandler')
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        file_path = event.src_path
        if self.is_project_file(file_path):
            self.logger.info(f"Detected change in: {file_path}")
            self.auto_runner.update_progress()
            
    def on_created(self, event):
        if event.is_directory:
            return
            
        file_path = event.src_path
        if self.is_project_file(file_path):
            self.logger.info(f"Detected new file: {file_path}")
            self.auto_runner.update_progress()
            
    def on_deleted(self, event):
        if event.is_directory:
            return
            
        file_path = event.src_path
        if self.is_project_file(file_path):
            self.logger.info(f"Detected deleted file: {file_path}")
            self.auto_runner.update_progress()
            
    def is_project_file(self, file_path):
        """Check if file is a project file we should track"""
        project_files = ['.py', '.js', '.java', '.cpp', '.c', '.h', '.json', '.yml', '.yaml']
        return any(file_path.endswith(ext) for ext in project_files)


def main():
    """Main entry point for auto runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto Project Management Runner')
    parser.add_argument('--path', help='Project path', default=os.getcwd())
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    
    args = parser.parse_args()
    
    runner = AutoRunner(args.path)
    
    if args.daemon:
        # Run as daemon
        try:
            import daemon
            with daemon.DaemonContext():
                runner.start()
        except ImportError:
            print("python-daemon package not installed. Running in foreground...")
            runner.start()
    else:
        runner.start()


if __name__ == "__main__":
    main()
