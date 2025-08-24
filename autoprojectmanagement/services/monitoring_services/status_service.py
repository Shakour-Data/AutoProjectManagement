"""
Status Service for AutoProjectManagement
Purpose: Provide real-time status updates for VS Code extension and web interface
Author: AutoProjectManagement System
Version: 2.0.0
License: MIT
Description: Comprehensive status monitoring service with JSON output, progress tracking, and error handling
"""

import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class ProjectStatus:
    """Data class representing project status information."""
    status: str  # running, complete, idle, error
    progress: int  # 0-100 percentage
    last_updated: str  # ISO format timestamp
    tasks_completed: int
    tasks_total: int
    error: Optional[str] = None
    current_task: Optional[str] = None
    estimated_completion: Optional[str] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None


class StatusService:
    """
    Service to manage and provide comprehensive project status monitoring.
    
    This service provides real-time status updates, progress tracking, and system
    monitoring for the AutoProjectManagement system. It supports both VS Code
    extension integration and web interface status display.
    
    Features:
    - Real-time status monitoring
    - Progress percentage calculation
    - Error tracking and reporting
    - System resource monitoring
    - JSON status file generation
    - Periodic status updates
    
    Attributes:
        project_path (str): Path to the project directory
        status_file (str): Path to the status JSON output file
        logger (logging.Logger): Logger instance for operation tracking
    """
    
    def __init__(self, project_path: Optional[str] = None):
        """
        Initialize the Status Service.
        
        Args:
            project_path: Path to the project directory (defaults to current directory)
        """
        self.project_path = project_path or os.getcwd()
        self.status_file = os.path.join(self.project_path, 'JSonDataBase', 'OutPuts', 'status.json')
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        self.logger.info(f"Status Service initialized for project: {self.project_path}")
    
    def get_status(self) -> ProjectStatus:
        """
        Get comprehensive current project status.
        
        Returns:
            ProjectStatus: Complete status information including progress, tasks, and system metrics
            
        Raises:
            Exception: If status retrieval fails
        """
        try:
            # Read from progress report
            progress_file = os.path.join(self.project_path, 'JSonDataBase', 'OutPuts', 'progress_report.md')
            
            if os.path.exists(progress_file):
                with open(progress_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse status information
                status_data = self._parse_progress_report(content)
                
                # Get system metrics
                system_metrics = self._get_system_metrics()
                
                # Create comprehensive status object
                status = ProjectStatus(
                    status=status_data['status'],
                    progress=status_data['progress'],
                    last_updated=datetime.now().isoformat(),
                    tasks_completed=status_data['tasks_completed'],
                    tasks_total=status_data['tasks_total'],
                    current_task=status_data.get('current_task'),
                    estimated_completion=status_data.get('estimated_completion'),
                    memory_usage=system_metrics.get('memory_usage'),
                    cpu_usage=system_metrics.get('cpu_usage')
                )
                
                self.logger.info(f"Status retrieved: {status.status}, Progress: {status.progress}%")
                return status
                
            else:
                # No progress file found - return default status
                return ProjectStatus(
                    status='idle',
                    progress=0,
                    last_updated=datetime.now().isoformat(),
                    tasks_completed=0,
                    tasks_total=0,
                    current_task='Waiting for tasks...'
                )
                
        except Exception as e:
            self.logger.error(f"Error retrieving status: {e}")
            return ProjectStatus(
                status='error',
                progress=0,
                last_updated=datetime.now().isoformat(),
                tasks_completed=0,
                tasks_total=0,
                error=str(e)
            )
    
    def _parse_progress_report(self, content: str) -> Dict[str, Any]:
        """
        Parse progress report content to extract status information.
        
        Args:
            content: Progress report content as string
            
        Returns:
            Dict containing parsed status information
        """
        status_data = {
            'status': 'running',
            'progress': 0,
            'tasks_completed': 0,
            'tasks_total': 0,
            'current_task': None,
            'estimated_completion': None
        }
        
        try:
            # Extract progress percentage
            import re
            progress_match = re.search(r'Overall Progress:\s*(\d+)%', content)
            if progress_match:
                status_data['progress'] = int(progress_match.group(1))
            
            # Extract tasks information
            tasks_match = re.search(r'Tasks Completed:\s*(\d+)/(\d+)', content)
            if tasks_match:
                status_data['tasks_completed'] = int(tasks_match.group(1))
                status_data['tasks_total'] = int(tasks_match.group(2))
            
            # Extract current task
            task_match = re.search(r'Current Task:\s*(.+)', content)
            if task_match:
                status_data['current_task'] = task_match.group(1).strip()
            
            # Extract estimated completion
            completion_match = re.search(r'Estimated Completion:\s*(.+)', content)
            if completion_match:
                status_data['estimated_completion'] = completion_match.group(1).strip()
            
            # Determine overall status
            if status_data['progress'] == 100:
                status_data['status'] = 'complete'
            elif status_data['progress'] > 0:
                status_data['status'] = 'running'
            else:
                status_data['status'] = 'idle'
                
        except Exception as e:
            self.logger.warning(f"Error parsing progress report: {e}")
        
        return status_data
    
    def _get_system_metrics(self) -> Dict[str, float]:
        """
        Get system resource usage metrics.
        
        Returns:
            Dict containing memory and CPU usage percentages
        """
        try:
            import psutil
            
            metrics = {
                'memory_usage': psutil.virtual_memory().percent,
                'cpu_usage': psutil.cpu_percent(interval=1)
            }
            
            return metrics
            
        except ImportError:
            self.logger.warning("psutil not available - system metrics disabled")
            return {}
        except Exception as e:
            self.logger.warning(f"Error getting system metrics: {e}")
            return {}
    
    def save_status(self, status: ProjectStatus) -> bool:
        """
        Save status information to JSON file.
        
        Args:
            status: ProjectStatus object to save
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(self.status_file), exist_ok=True)
            
            status_dict = asdict(status)
            
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(status_dict, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"Status saved to: {self.status_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save status: {e}")
            return False
    
    def update_status_periodically(self, interval: int = 30) -> None:
        """
        Continuously update status at regular intervals.
        
        Args:
            interval: Update interval in seconds (default: 30)
        """
        self.logger.info(f"Starting periodic status updates every {interval} seconds")
        
        try:
            while True:
                status = self.get_status()
                self.save_status(status)
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.logger.info("Periodic status updates stopped")
        except Exception as e:
            self.logger.error(f"Error in periodic status updates: {e}")
    
    def get_status_json(self) -> str:
        """
        Get current status as JSON string.
        
        Returns:
            str: JSON formatted status information
        """
        status = self.get_status()
        return json.dumps(asdict(status), indent=2, ensure_ascii=False)
    
    def clear_status(self) -> bool:
        """
        Clear the status file and reset to idle state.
        
        Returns:
            bool: True if cleared successfully, False otherwise
        """
        try:
            if os.path.exists(self.status_file):
                os.remove(self.status_file)
                self.logger.info("Status file cleared")
            
            # Create fresh idle status
            idle_status = ProjectStatus(
                status='idle',
                progress=0,
                last_updated=datetime.now().isoformat(),
                tasks_completed=0,
                tasks_total=0,
                current_task='System ready'
            )
            
            return self.save_status(idle_status)
            
        except Exception as e:
            self.logger.error(f"Failed to clear status: {e}")
            return False


# Global instance for easy access
status_service = StatusService()


def get_current_status() -> ProjectStatus:
    """
    Get current project status using the global status service instance.
    
    Returns:
        ProjectStatus: Current project status information
    """
    return status_service.get_status()


def save_current_status() -> bool:
    """
    Save current project status to JSON file.
    
    Returns:
        bool: True if save was successful, False otherwise
    """
    status = get_current_status()
    return status_service.save_status(status)


# Example usage and testing
if __name__ == "__main__":
    # Configure logging for standalone usage
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create status service instance
    service = StatusService()
    
    try:
        # Get and display current status
        current_status = service.get_status()
        print("📊 Current Project Status:")
        print(f"   Status: {current_status.status}")
        print(f"   Progress: {current_status.progress}%")
        print(f"   Tasks: {current_status.tasks_completed}/{current_status.tasks_total}")
        print(f"   Current Task: {current_status.current_task}")
        
        # Save status to file
        if service.save_status(current_status):
            print(f"✅ Status saved to: {service.status_file}")
        else:
            print("❌ Failed to save status")
            
    except Exception as e:
        print(f"❌ Error: {e}")
