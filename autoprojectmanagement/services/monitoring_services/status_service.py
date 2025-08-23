#!/usr/bin/env python3
"""
Status service for AutoProjectManagement
Provides real-time status updates for VS Code extension and web interface
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

class StatusService:
    """Service to manage and provide project status"""
    
    def __init__(self, project_path=None):
        self.project_path = project_path or os.getcwd()
        self.status_file = os.path.join(self.project_path, 'JSonDataBase', 'OutPuts', 'status.json')
        
    def get_status(self):
        """Get current project status"""
        try:
            # Read from progress report
            progress_file = os.path.join(self.project_path, 'JSonDataBase', 'OutPuts', 'progress_report.md')
            
            if os.path.exists(progress_file):
                with open(progress_file, 'r') as f:
                    content = f.read()
                
                # Parse status
                status = {
                    'status': 'running',
                    'progress': 0,
                    'last_updated': datetime.now().isoformat(),
                    'tasks_completed': 0,
                    'tasks_total': 0
                }
                
                # Extract progress
                for line in content.split('\n'):
                    if 'Overall Progress:' in line:
                        import re
                        match = re.search(r'(\d+)%', line)
                        if match:
                            status['progress'] = int(match.group(1))
                    elif 'Tasks Completed:' in line:
                        import re
                        match = re.search(r'(\d+)/(\d+)', line)
                        if match:
                            status['tasks_completed'] = int(match.group(1))
                            status['tasks_total'] = int(match.group(2))
                
                # Determine status
                if status['progress'] == 100:
                    status['status'] = 'complete'
                elif status['progress'] > 0:
                    status['status'] = 'running'
                else:
                    status['status'] = 'idle'
                
                return status
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'last_updated': datetime.now().isoformat()
            }
    
    def save_status(self, status):
        """Save status to JSON file"""
        os.makedirs(os.path.dirname(self.status_file), exist_ok=True)
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
    
    def update_status_periodically(self):
        """Update status every 30 seconds"""
        while True:
            status = self.get_status()
            self.save_status(status)
            time.sleep(30)

if __name__ == "__main__":
    service = StatusService()
    service.update_status_periodically()
