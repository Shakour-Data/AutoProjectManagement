#!/usr/bin/env python3
"""
Setup Auto Environment - Creates a complete automatic project management environment
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

class AutoEnvironmentSetup:
    """Setup automatic project management environment"""
    
    def __init__(self, project_path=None):
        self.project_path = project_path or os.getcwd()
        self.logger = self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for setup process"""
        import logging
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger('AutoEnvironmentSetup')
        
    def create_project_structure(self):
        """Create project structure for automatic management"""
        self.logger.info("Creating project structure...")
        
        directories = [
            '.auto_project',
            '.auto_project/logs',
            '.auto_project/config',
            '.auto_project/data',
            '.auto_project/reports',
            '.auto_project/backups',
            'project_inputs/PM_JSON/user_inputs',
            'project_inputs/PM_JSON/system_inputs'
        ]
        
        for directory in directories:
            path = os.path.join(self.project_path, directory)
            os.makedirs(path, exist_ok=True)
            
    def create_auto_config(self):
        """Create automatic configuration file"""
        config = {
            "auto_management": {
                "enabled": True,
                "auto_commit": True,
                "auto_progress": True,
                "auto_risk_assessment": True,
                "auto_reporting": True,
                "auto_backup": True
            },
            "monitoring": {
                "file_extensions": [".py", ".js", ".java", ".cpp", ".c", ".h", ".json", ".yml", ".yaml", ".md"],
                "exclude_patterns": [".git", "__pycache__", "node_modules", ".auto_project"],
                "check_interval": 300
            },
            "git": {
                "auto_commit": True,
                "commit_message_template": "Auto commit: {changes}",
                "push_on_commit": True
            },
            "reporting": {
                "daily_reports": True,
                "weekly_reports": True,
                "report_format": "markdown"
            },
            "notifications": {
                "desktop_notifications": True,
                "email_notifications": False,
                "webhook_notifications": False
            }
        }
        
        config_path = os.path.join(self.project_path, '.auto_project/config/auto_config.json')
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
    def create_startup_script(self):
        """Create startup script for automatic management"""
        startup_script = '''#!/bin/bash
# Auto Project Management Startup Script

echo "🚀 Starting Auto Project Management Environment..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Install required packages
echo "📦 Installing required packages..."
pip install watchdog psutil python-daemon

# Start auto runner
echo "🔄 Starting automatic project management..."
nohup python3 -m autoprojectmanagement.auto_runner --path "$(pwd)" > .auto_project/logs/auto_runner.log 2>&1 &

# Save PID
echo $! > .auto_project/auto_runner.pid

echo "✅ Auto project management started!"
echo "📊 Logs: .auto_project/logs/auto_runner.log"
echo "🛑 To stop: ./stop_auto_management.sh"
'''
        
        startup_path = os.path.join(self.project_path, 'start_auto_management.sh')
        with open(startup_path, 'w') as f:
            f.write(startup_script)
        os.chmod(startup_path, 0o755)
        
    def create_stop_script(self):
        """Create stop script for automatic management"""
        stop_script = '''#!/bin/bash
# Auto Project Management Stop Script

echo "🛑 Stopping Auto Project Management Environment..."

if [ -f .auto_project/auto_runner.pid ]; then
    PID=$(cat .auto_project/auto_runner.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        rm .auto_project/auto_runner.pid
        echo "✅ Auto project management stopped!"
    else
        echo "⚠️  Process not found or already stopped"
        rm .auto_project/auto_runner.pid
    fi
else
    echo "⚠️  No PID file found. Process may not be running."
fi

# Kill any remaining Python processes
pkill -f "auto_runner.py"
echo "🧹 Cleanup complete!"
'''
        
        stop_path = os.path.join(self.project_path, 'stop_auto_management.sh')
        with open(stop_path, 'w') as f:
            f.write(stop_script)
        os.chmod(stop_path, 0o755)
        
    def create_status_script(self):
        """Create status script for checking automatic management"""
        status_script = '''#!/bin/bash
# Auto Project Management Status Script

echo "📊 Auto Project Management Status"
echo "================================"

if [ -f .auto_project/auto_runner.pid ]; then
    PID=$(cat .auto_project/auto_runner.pid)
    if kill -0 $PID 2>/dev/null; then
        echo "✅ Status: Running (PID: $PID)"
    else
        echo "❌ Status: Process not running (stale PID file)"
    fi
else
    echo "❌ Status: Not running"
fi

if [ -f .auto_project/logs/auto_runner.log ]; then
    echo "📋 Last 5 log entries:"
    tail -5 .auto_project/logs/auto_runner.log
fi

echo ""
echo "📁 Project Structure:"
ls -la .auto_project/
'''
        
        status_path = os.path.join(self.project_path, 'status_auto_management.sh')
        with open(status_path, 'w') as f:
            f.write(status_script)
        os.chmod(status_path, 0o755)
        
    def create_vscode_workspace(self):
        """Create VS Code workspace configuration"""
        workspace = {
            "folders": [
                {
                    "path": "."
                }
            ],
            "settings": {
                "files.autoSave": "afterDelay",
                "files.autoSaveDelay": 1000,
                "git.autofetch": True,
                "git.enableSmartCommit": True,
                "extensions.autoUpdate": True,
                "python.defaultInterpreterPath": "./venv/bin/python",
                "python.terminal.activateEnvironment": True
            },
            "launch": {
                "configurations": [
                    {
                        "name": "Auto Project Management",
                        "type": "python",
                        "request": "launch",
                        "program": "${workspaceFolder}/.vscode/auto_runner.py",
                        "console": "integratedTerminal",
                        "cwd": "${workspaceFolder}"
                    }
                ]
            },
            "tasks": {
                "version": "2.0.0",
                "tasks": [
                    {
                        "label": "Start Auto Management",
                        "type": "shell",
                        "command": "./start_auto_management.sh",
                        "group": "build",
                        "presentation": {
                            "echo": True,
                            "reveal": "always",
                            "focus": False
                        }
                    },
                    {
                        "label": "Stop Auto Management",
                        "type": "shell",
                        "command": "./stop_auto_management.sh",
                        "group": "build"
                    }
                ]
            }
        }
        
        workspace_path = os.path.join(self.project_path, 'auto_project_management.code-workspace')
        with open(workspace_path, 'w') as f:
            json.dump(workspace, f, indent=2)
            
    def create_requirements_file(self):
        """Create requirements file for auto environment"""
        requirements = [
            "watchdog>=2.1.0",
            "psutil>=5.8.0",
            "python-daemon>=2.3.0",
            "schedule>=1.1.0",
            "plyer>=2.1.0",
            "rich>=10.0.0"
        ]
        
        requirements_path = os.path.join(self.project_path, '.auto_project/requirements.txt')
        with open(requirements_path, 'w') as f:
            f.write('\n'.join(requirements))
            
    def create_gitignore(self):
        """Create .gitignore for auto project management"""
        gitignore_content = '''
# Auto Project Management
.auto_project/logs/
.auto_project/backups/
.auto_project/data/cache/
*.pid
*.log

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
'''
        
        gitignore_path = os.path.join(self.project_path, '.gitignore')
        with open(gitignore_path, 'a') as f:
            f.write(gitignore_content)
            
    def install_dependencies(self):
        """Install required dependencies"""
        self.logger.info("Installing dependencies...")
        
        requirements_path = os.path.join(self.project_path, '.auto_project/requirements.txt')
        if os.path.exists(requirements_path):
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', requirements_path
                ], check=True)
                self.logger.info("Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Failed to install dependencies: {e}")
                
    def setup_complete_environment(self):
        """Setup complete automatic project management environment"""
        self.logger.info("Setting up complete automatic project management environment...")
        
        # Create project structure
        self.create_project_structure()
        
        # Create configuration
        self.create_auto_config()
        
        # Create scripts
        self.create_startup_script()
        self.create_stop_script()
        self.create_status_script()
        
        # Create VS Code workspace
        self.create_vscode_workspace()
        
        # Create requirements
        self.create_requirements_file()
        
        # Update .gitignore
        self.create_gitignore()
        
        # Install dependencies
        self.install_dependencies()
        
        self.logger.info("✅ Complete automatic project management environment setup!")
        self.logger.info("📁 Use './start_auto_management.sh' to start automatic management")
        self.logger.info("📊 Use './status_auto_management.sh' to check status")
        self.logger.info("🛑 Use './stop_auto_management.sh' to stop automatic management")
        self.logger.info("💻 Open 'auto_project_management.code-workspace' in VS Code")


def main():
    """Main entry point for setup"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup Auto Project Management Environment')
    parser.add_argument('--path', help='Project path', default=os.getcwd())
    
    args = parser.parse_args()
    
    setup = AutoEnvironmentSetup(args.path)
    setup.setup_complete_environment()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Run './start_auto_management.sh' to start automatic management")
    print("2. Open 'auto_project_management.code-workspace' in VS Code")
    print("3. Start coding - project management will happen automatically!")


if __name__ == "__main__":
    main()
