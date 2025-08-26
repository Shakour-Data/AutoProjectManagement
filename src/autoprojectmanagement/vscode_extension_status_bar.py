#!/usr/bin/env python3
"""
VS Code Status Bar Integration - Provides real-time project management status
"""

import os
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime

class VSCodeStatusBar:
    """VS Code Status Bar for AutoProjectManagement"""
    
    def __init__(self, project_path=None):
        self.project_path = project_path or os.getcwd()
        self.extension_dir = os.path.join(self.project_path, '.vscode')
        self.logger = logging.getLogger('VSCodeStatusBar')
        
    def create_status_bar_extension(self):
        """Create VS Code extension with status bar support"""
        
        # Create extension.js with status bar functionality
        extension_js = '''
const vscode = require('vscode');
const path = require('path');
const fs = require('fs');

let statusBarItem;

function activate(context) {
    console.log('AutoProjectManagement Status Bar extension is now active!');
    
    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    
    // Set initial status
    updateStatusBar('Initializing...');
    statusBarItem.show();
    
    // Register commands
    let startCommand = vscode.commands.registerCommand('autoProjectManagement.start', function () {
        updateStatusBar('Running...');
        vscode.window.showInformationMessage('Auto Project Management started');
    });
    
    let stopCommand = vscode.commands.registerCommand('autoProjectManagement.stop', function () {
        updateStatusBar('Stopped');
        vscode.window.showInformationMessage('Auto Project Management stopped');
    });
    
    let refreshCommand = vscode.commands.registerCommand('autoProjectManagement.refreshStatus', function () {
        refreshProjectStatus();
    });
    
    let showDetailsCommand = vscode.commands.registerCommand('autoProjectManagement.showDetails', function () {
        showProjectDetails();
    });
    
    // Auto refresh every 30 seconds
    setInterval(refreshProjectStatus, 30000);
    
    // Initial refresh
    refreshProjectStatus();
    
    context.subscriptions.push(statusBarItem);
    context.subscriptions.push(startCommand);
    context.subscriptions.push(stopCommand);
    context.subscriptions.push(refreshCommand);
    context.subscriptions.push(showDetailsCommand);
}

function deactivate() {
    if (statusBarItem) {
        statusBarItem.dispose();
    }
}

function updateStatusBar(text, tooltip = null) {
    statusBarItem.text = `$(sync~spin) AutoPM: ${text}`;
    if (tooltip) {
        statusBarItem.tooltip = tooltip;
    }
}

function refreshProjectStatus() {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceFolder) return;
    
    const statusFile = path.join(workspaceFolder, 'JSonDataBase', 'OutPuts', 'progress_report.md');
    
    if (fs.existsSync(statusFile)) {
        const content = fs.readFileSync(statusFile, 'utf8');
        
        // Parse status from progress report
        const lines = content.split('\\n');
        let status = 'Ready';
        let progress = '0%';
        
        for (const line of lines) {
            if (line.includes('Overall Progress:')) {
                const match = line.match(/(\\d+)%/);
                if (match) {
                    progress = match[1] + '%';
                    status = progress === '100%' ? 'Complete' : 'In Progress';
                }
            }
        }
        
        updateStatusBar(`${status} (${progress})`, `Last updated: ${new Date().toLocaleString()}`);
    } else {
        updateStatusBar('No data', 'Run auto management to see status');
    }
}

function showProjectDetails() {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceFolder) return;
    
    const statusFile = path.join(workspaceFolder, 'JSonDataBase', 'OutPuts', 'progress_report.md');
    
    if (fs.existsSync(statusFile)) {
        const content = fs.readFileSync(statusFile, 'utf8');
        vscode.window.showInformationMessage('Project details opened in new editor');
        
        vscode.workspace.openTextDocument(statusFile).then(doc => {
            vscode.window.showTextDocument(doc);
        });
    } else {
        vscode.window.showWarningMessage('No progress report found. Run auto management first.');
    }
}

module.exports = {
    activate,
    deactivate
};
'''

        # Create package.json with status bar support
        package_json = {
            "name": "auto-project-management-status",
            "displayName": "Auto Project Management Status",
            "description": "Real-time status bar for automatic project management",
            "version": "1.0.0",
            "publisher": "autoprojectmanagement",
            "engines": {
                "vscode": "^1.60.0"
            },
            "activationEvents": [
                "onStartupFinished"
            ],
            "main": "./out/extension.js",
            "contributes": {
                "commands": [
                    {
                        "command": "autoProjectManagement.refreshStatus",
                        "title": "Refresh Project Status",
                        "category": "AutoPM"
                    },
                    {
                        "command": "autoProjectManagement.showDetails",
                        "title": "Show Project Details",
                        "category": "AutoPM"
                    },
                    {
                        "command": "autoProjectManagement.start",
                        "title": "Start Auto Management",
                        "category": "AutoPM"
                    },
                    {
                        "command": "autoProjectManagement.stop",
                        "title": "Stop Auto Management",
                        "category": "AutoPM"
                    }
                ],
                "menus": {
                    "statusBar": [
                        {
                            "command": "autoProjectManagement.showDetails",
                            "when": "true",
                            "group": "navigation"
                        }
                    ]
                }
            }
        }

        # Create the extension files
        out_dir = os.path.join(self.extension_dir, 'out')
        os.makedirs(out_dir, exist_ok=True)
        
        extension_path = os.path.join(out_dir, 'extension.js')
        with open(extension_path, 'w') as f:
            f.write(extension_js)
            
        package_path = os.path.join(self.extension_dir, 'package.json')
        with open(package_path, 'w') as f:
            json.dump(package_json, f, indent=2)
            
    def create_status_bar_html(self):
        """Create HTML status bar for web interface"""
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto Project Management - Status</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        
        .status-bar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .status-icon {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background-color: #4CAF50;
            animation: pulse 2s infinite;
        }
        
        .status-icon.running {
            background-color: #4CAF50;
        }
        
        .status-icon.stopped {
            background-color: #f44336;
        }
        
        .status-icon.idle {
            background-color: #ff9800;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .progress-bar {
            width: 200px;
            height: 8px;
            background-color: rgba(255,255,255,0.3);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background-color: #4CAF50;
            transition: width 0.3s ease;
        }
        
        .last-updated {
            font-size: 0.8em;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="status-bar">
        <div class="status-item">
            <div class="status-icon running" id="statusIcon"></div>
            <span id="statusText">Auto Project Management - Running</span>
        </div>
        
        <div class="status-item">
            <span>Progress:</span>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill" style="width: 0%"></div>
            </div>
            <span id="progressText">0%</span>
        </div>
        
        <div class="status-item last-updated" id="lastUpdated">
            Last updated: Never
        </div>
    </div>

    <script>
        async function updateStatus() {
            try {
                const response = await fetch('/api/v1/projects/current/status');
                const data = await response.json();
                
                // Update status
                const statusIcon = document.getElementById('statusIcon');
                const statusText = document.getElementById('statusText');
                const progressFill = document.getElementById('progressFill');
                const progressText = document.getElementById('progressText');
                const lastUpdated = document.getElementById('lastUpdated');
                
                // Update based on data
                if (data.progress === 100) {
                    statusIcon.className = 'status-icon idle';
                    statusText.textContent = 'Auto Project Management - Complete';
                } else {
                    statusIcon.className = 'status-icon running';
                    statusText.textContent = 'Auto Project Management - Running';
                }
                
                progressFill.style.width = data.progress + '%';
                progressText.textContent = data.progress + '%';
                lastUpdated.textContent = 'Last updated: ' + new Date().toLocaleString();
                
            } catch (error) {
                console.error('Error updating status:', error);
                document.getElementById('statusText').textContent = 'Auto Project Management - Error';
                document.getElementById('statusIcon').className = 'status-icon stopped';
            }
        }
        
        // Update every 30 seconds
        setInterval(updateStatus, 30000);
        
        // Initial update
        updateStatus();
    </script>
</body>
</html>'''
        
        web_dir = os.path.join(self.extension_dir, 'web')
        os.makedirs(web_dir, exist_ok=True)
        
        html_path = os.path.join(web_dir, 'status.html')
        with open(html_path, 'w') as f:
            f.write(html_content)
            
    def create_status_service(self):
        """Create Python service for status updates"""
        service_py = '''#!/usr/bin/env python3
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
                for line in content.split('\\n'):
                    if 'Overall Progress:' in line:
                        import re
                        match = re.search(r'(\\d+)%', line)
                        if match:
                            status['progress'] = int(match.group(1))
                    elif 'Tasks Completed:' in line:
                        import re
                        match = re.search(r'(\\d+)/(\\d+)', line)
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
'''

        services_dir = os.path.join(self.project_path, 'autoprojectmanagement', 'services')
        os.makedirs(services_dir, exist_ok=True)
        
        service_path = os.path.join(services_dir, 'status_service.py')
        with open(service_path, 'w') as f:
            f.write(service_py)
            
    def setup_complete_status_bar(self):
        """Setup complete status bar system"""
        self.logger.info("Setting up complete status bar system...")
        
        # Create VS Code extension
        self.create_status_bar_extension()
        
        # Create web interface
        self.create_status_bar_html()
        
        # Create status service
        self.create_status_service()
        
        # Update existing extension to include status bar
        self.update_existing_extension()
        
        self.logger.info("Status bar system setup complete")
        
    def update_existing_extension(self):
        """Update existing VS Code extension to include status bar"""
        # Update package.json to include new commands
        package_path = os.path.join(self.extension_dir, 'package.json')
        
        if os.path.exists(package_path):
            with open(package_path, 'r') as f:
                package = json.load(f)
                
            # Add new commands
            new_commands = [
                {
                    "command": "autoProjectManagement.refreshStatus",
                    "title": "Refresh Project Status",
                    "category": "AutoPM"
                },
                {
                    "command": "autoProjectManagement.showDetails",
                    "title": "Show Project Details",
                    "category": "AutoPM"
                }
            ]
            
            package['contributes']['commands'].extend(new_commands)
            
            with open(package_path, 'w') as f:
                json.dump(package, f, indent=2)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup Status Bar for AutoProjectManagement')
    parser.add_argument('--path', help='Project path', default=os.getcwd())
    
    args = parser.parse_args()
    
    status_bar = VSCodeStatusBar(args.path)
    status_bar.setup_complete_status_bar()
    
    print("Status bar setup complete!")
    print("1. Reload VS Code to see the status bar")
    print("2. Visit http://localhost:8000/web/status.html for web status")
    print("3. Use Ctrl+Shift+P and search for 'AutoPM' commands")


if __name__ == "__main__":
    main()
