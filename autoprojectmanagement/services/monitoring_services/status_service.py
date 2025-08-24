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
