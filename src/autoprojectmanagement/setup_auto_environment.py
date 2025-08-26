#!/usr/bin/env python3
"""
Setup Auto Environment - Creates a complete automatic project management environment.

This module provides comprehensive setup functionality for the AutoProjectManagement
system, creating all necessary directories, configuration files, scripts, and
development environment configurations for seamless automated project management.

Key Features:
    - Complete project structure creation
    - Configuration file generation
    - Shell script automation
    - VS Code workspace setup
    - Dependency management
    - Git integration setup

Usage:
    Command line usage:
        $ python -m autoprojectmanagement.setup_auto_environment --path /path/to/project
    
    Programmatic usage:
        >>> from autoprojectmanagement.setup_auto_environment import AutoEnvironmentSetup
        >>> setup = AutoEnvironmentSetup('/path/to/project')
        >>> setup.setup_complete_environment()

Configuration:
    The setup creates:
    - .auto_project/ directory structure
    - Configuration files (JSON format)
    - Shell scripts for automation
    - VS Code workspace configuration
    - Requirements files
    - Git ignore patterns

Examples:
    Basic setup:
        >>> setup = AutoEnvironmentSetup()
        >>> setup.setup_complete_environment()
    
    Custom project path:
        >>> setup = AutoEnvironmentSetup('/custom/path')
        >>> setup.setup_complete_environment()

For more information, visit: https://github.com/AutoProjectManagement/AutoProjectManagement
"""

import os
import sys
import json
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

# Constants for setup configuration
DEFAULT_PROJECT_STRUCTURE: List[str] = [
    '.auto_project',
    '.auto_project/logs',
    '.auto_project/config',
    '.auto_project/data',
    '.auto_project/reports',
    '.auto_project/backups',
    'project_inputs/PM_JSON/user_inputs',
    'project_inputs/PM_JSON/system_inputs'
]

DEFAULT_REQUIREMENTS: List[str] = [
    "watchdog>=2.1.0",
    "psutil>=5.8.0",
    "python-daemon>=2.3.0",
    "schedule>=1.1.0",
    "plyer>=2.1.0",
    "rich>=10.0.0",
    "click>=8.0.0",
    "fastapi>=0.68.0",
    "uvicorn>=0.15.0"
]

DEFAULT_GITIGNORE_PATTERNS: List[str] = [
    '# Auto Project Management',
    '.auto_project/logs/',
    '.auto_project/backups/',
    '.auto_project/data/cache/',
    '*.pid',
    '*.log',
    '',
    '# Python',
    '__pycache__/',
    '*.py[cod]',
    '*$py.class',
    '*.so',
    '.Python',
    'env/',
    'venv/',
    'ENV/',
    '.venv',
    '',
    '# IDE',
    '.vscode/',
    '.idea/',
    '*.swp',
    '*.swo',
    '*~',
    '',
    '# OS',
    '.DS_Store',
    'Thumbs.db'
]


class AutoEnvironmentSetup:
    """
    Setup automatic project management environment with comprehensive configuration.

    This class provides complete setup functionality for creating an automated
    project management environment including directory structure, configuration
    files, shell scripts, and development tools integration.

    Attributes:
        project_path (str): Absolute path to the project directory
        extension_dir (str): Path to VS Code extension directory
        logger (logging.Logger): Configured logger instance

    Example:
        >>> setup = AutoEnvironmentSetup('/path/to/project')
        >>> setup.setup_complete_environment()
    """

    def __init__(self, project_path: Optional[str] = None) -> None:
        """
        Initialize the AutoEnvironmentSetup with comprehensive configuration.

        Args:
            project_path: Optional path to the project directory.
                         If None, uses current working directory.

        Raises:
            ValueError: If the provided project_path does not exist
            OSError: If unable to create required directories
        """
        self.project_path = project_path or os.getcwd()
        self.extension_dir = os.path.join(self.project_path, '.vscode')
        self.logger = self._setup_logging()

        # Validate project path
        if not os.path.exists(self.project_path):
            raise ValueError(f"Project path does not exist: {self.project_path}")

        self.logger.info(f"Initializing AutoEnvironmentSetup for: {self.project_path}")

    def _setup_logging(self) -> logging.Logger:
        """
        Set up comprehensive logging for the setup process.

        Returns:
            logging.Logger: Configured logger instance
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger('AutoEnvironmentSetup')

    def create_project_structure(self) -> None:
        """
        Create comprehensive project structure for automatic management.

        Creates all necessary directories for the AutoProjectManagement system
        including logs, configuration, data, reports, and backup directories.
        """
        self.logger.info("Creating project structure...")

        for directory in DEFAULT_PROJECT_STRUCTURE:
            path = Path(self.project_path) / directory
            path.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Created directory: {path}")

    def create_auto_config(self) -> None:
        """
        Create comprehensive automatic configuration file.

        Generates a JSON configuration file with all necessary settings
        for the AutoProjectManagement system including monitoring, git,
        reporting, and notification configurations.
        """
        config: Dict[str, Any] = {
            "auto_management": {
                "enabled": True,
                "auto_commit": True,
                "auto_progress": True,
                "auto_risk_assessment": True,
                "auto_reporting": True,
                "auto_backup": True,
                "auto_notifications": True
            },
            "monitoring": {
                "file_extensions": [".py", ".js", ".java", ".cpp", ".c", ".h", 
                                  ".json", ".yml", ".yaml", ".md", ".txt", ".sql"],
                "exclude_patterns": [".git", "__pycache__", "node_modules", 
                                   ".auto_project", "*.tmp", "*.log"],
                "check_interval": 300,
                "max_file_size_mb": 10
            },
            "git": {
                "auto_commit": True,
                "commit_message_template": "Auto commit: {changes} - {timestamp}",
                "push_on_commit": True,
                "commit_threshold": 5,
                "exclude_files": [".env", "*.log", "*.tmp"]
            },
            "reporting": {
                "daily_reports": True,
                "weekly_reports": True,
                "report_format": "markdown",
                "include_charts": True,
                "output_directory": ".auto_project/reports"
            },
            "notifications": {
                "desktop_notifications": True,
                "email_notifications": False,
                "webhook_notifications": False,
                "notification_threshold": "medium"
            },
            "backup": {
                "enabled": True,
                "backup_interval_hours": 24,
                "retention_days": 30,
                "backup_directory": ".auto_project/backups"
            }
        }

        config_path = Path(self.project_path) / '.auto_project' / 'config' / 'auto_config.json'
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Configuration file created: {config_path}")

    def create_startup_script(self) -> None:
        """
        Create comprehensive startup script for automatic management.

        Creates a shell script that starts the automatic project management
        system with proper logging and error handling.
        """
        startup_script = '''#!/bin/bash
# Auto Project Management Startup Script
# This script starts the automatic project management system

set -e  # Exit on any error

echo "🚀 Starting Auto Project Management Environment..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Install required packages if requirements file exists
REQUIREMENTS_FILE=".auto_project/requirements.txt"
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "📦 Installing required packages..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "⚠️  Requirements file not found, skipping package installation"
fi

# Create logs directory if it doesn't exist
mkdir -p .auto_project/logs

# Start auto runner in background
echo "🔄 Starting automatic project management..."
nohup python3 -m autoprojectmanagement.auto_runner \
    --path "$(pwd)" \
    > .auto_project/logs/auto_runner.log 2>&1 &

# Save PID for later management
echo $! > .auto_project/auto_runner.pid

echo "✅ Auto project management started successfully!"
echo "📊 Logs: .auto_project/logs/auto_runner.log"
echo "🛑 To stop: ./stop_auto_management.sh"
echo "📈 To check status: ./status_auto_management.sh"
'''
        
        startup_path = Path(self.project_path) / 'start_auto_management.sh'
        with open(startup_path, 'w', encoding='utf-8') as f:
            f.write(startup_script)
        os.chmod(startup_path, 0o755)
        self.logger.info(f"Startup script created: {startup_path}")

    def create_stop_script(self) -> None:
        """
        Create comprehensive stop script for automatic management.

        Creates a shell script that gracefully stops the automatic project
        management system and performs cleanup.
        """
        stop_script = '''#!/bin/bash
# Auto Project Management Stop Script
# This script gracefully stops the automatic project management system

set -e  # Exit on any error

echo "🛑 Stopping Auto Project Management Environment..."

PID_FILE=".auto_project/auto_runner.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 $PID 2>/dev/null; then
        echo "📋 Stopping process with PID: $PID"
        kill $PID
        rm "$PID_FILE"
        echo "✅ Auto project management stopped successfully!"
    else
        echo "⚠️  Process not found or already stopped"
        rm -f "$PID_FILE"
    fi
else
    echo "⚠️  No PID file found. Process may not be running."
fi

# Kill any remaining Python processes related to auto_runner
pkill -f "auto_runner.py" 2>/dev/null || true

# Clean up any stale lock files
rm -f .auto_project/*.lock 2>/dev/null || true

echo "🧹 Cleanup complete!"
'''
        
        stop_path = Path(self.project_path) / 'stop_auto_management.sh'
        with open(stop_path, 'w', encoding='utf-8') as f:
            f.write(stop_script)
        os.chmod(stop_path, 0o755)
        self.logger.info(f"Stop script created: {stop_path}")

    def create_status_script(self) -> None:
        """
        Create comprehensive status script for checking automatic management.

        Creates a shell script that displays the current status of the
        automatic project management system.
        """
        status_script = '''#!/bin/bash
# Auto Project Management Status Script
# This script displays comprehensive status information

set -e  # Exit on any error

echo "📊 Auto Project Management Status"
echo "================================"
echo ""

# Check if process is running
PID_FILE=".auto_project/auto_runner.pid"
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 $PID 2>/dev/null; then
        echo "✅ Status: Running (PID: $PID)"
        
        # Get process information
        if command -v ps &> /dev/null; then
            echo "📋 Process details:"
            ps -p $PID -o pid,ppid,cmd,etime 2>/dev/null || echo "  Unable to get process details"
        fi
    else
        echo "❌ Status: Process not running (stale PID file)"
        rm -f "$PID_FILE"
    fi
else
    echo "❌ Status: Not running"
fi

# Display recent log entries
LOG_FILE=".auto_project/logs/auto_runner.log"
if [ -f "$LOG_FILE" ]; then
    echo ""
    echo "📋 Last 10 log entries:"
    echo "------------------------"
    tail -10 "$LOG_FILE" 2>/dev/null || echo "  Unable to read log file"
else
    echo ""
    echo "⚠️  No log file found"
fi

# Display project structure
echo ""
echo "📁 Project Structure:"
echo "---------------------"
if [ -d ".auto_project" ]; then
    find .auto_project -type d -name ".*" -prune -o -type f -print | head -20
else
    echo "  .auto_project directory not found"
fi

# Check disk usage
echo ""
echo "💾 Disk Usage:"
echo "-------------"
if command -v du &> /dev/null; then
    du -sh .auto_project 2>/dev/null || echo "  Unable to check disk usage"
else
    echo "  du command not available"
fi
'''
        
        status_path = Path(self.project_path) / 'status_auto_management.sh'
        with open(status_path, 'w', encoding='utf-8') as f:
            f.write(status_script)
        os.chmod(status_path, 0o755)
        self.logger.info(f"Status script created: {status_path}")

    def create_vscode_workspace(self) -> None:
        """
        Create comprehensive VS Code workspace configuration.

        Creates a VS Code workspace file with optimized settings for
        automatic project management including debugging, tasks, and extensions.
        """
        workspace = {
            "folders": [{"path": "."}],
            "settings": {
                "files.autoSave": "afterDelay",
                "files.autoSaveDelay": 1000,
                "git.autofetch": True,
                "git.enableSmartCommit": True,
                "git.postCommitCommand": "push",
                "extensions.autoUpdate": True,
                "python.defaultInterpreterPath": "./venv/bin/python",
                "python.terminal.activateEnvironment": True,
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                "python.formatting.provider": "black",
                "editor.formatOnSave": True,
                "editor.rulers": [79, 120],
                "files.exclude": {
                    "**/.git": True,
                    "**/__pycache__": True,
                    "**/*.pyc": True,
                    "**/.auto_project/logs": True,
                    "**/.auto_project/backups": True
                }
            },
            "launch": {
                "version": "0.2.0",
                "configurations": [
                    {
                        "name": "Auto Project Management",
                        "type": "python",
                        "request": "launch",
                        "program": "${workspaceFolder}/start_auto_management.sh",
                        "console": "integratedTerminal",
                        "cwd": "${workspaceFolder}",
                        "env": {"PYTHONPATH": "${workspaceFolder}"}
                    },
                    {
                        "name": "Debug Auto Runner",
                        "type": "python",
                        "request": "launch",
                        "module": "autoprojectmanagement.auto_runner",
                        "console": "integratedTerminal",
                        "cwd": "${workspaceFolder}",
                        "args": ["--path", "${workspaceFolder}", "--verbose"]
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
                    },
                    {
                        "label": "Check Status",
                        "type": "shell",
                        "command": "./status_auto_management.sh",
                        "group": "test"
                    }
                ]
            }
        }
        
        workspace_path = Path(self.project_path) / 'auto_project_management.code-workspace'
        with open(workspace_path, 'w', encoding='utf-8') as f:
            json.dump(workspace, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"VS Code workspace created: {workspace_path}")

    def create_requirements_file(self) -> None:
        """
        Create comprehensive requirements file for auto environment.

        Creates a requirements.txt file with all necessary dependencies
        for the AutoProjectManagement system.
        """
        requirements_path = Path(self.project_path) / '.auto_project' / 'requirements.txt'
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(DEFAULT_REQUIREMENTS))
        
        self.logger.info(f"Requirements file created: {requirements_path}")

    def create_gitignore(self) -> None:
        """
        Create comprehensive .gitignore file for auto project management.

        Creates a .gitignore file with patterns for excluding temporary files,
        logs, backups, and other non-essential files from version control.
        """
        gitignore_path = Path(self.project_path) / '.gitignore'
        
        # Append to existing .gitignore or create new one
        with open(gitignore_path, 'a', encoding='utf-8') as f:
            f.write('\n\n# Auto Project Management - Generated patterns\n')
            f.write('\n'.join(DEFAULT_GITIGNORE_PATTERNS))
        
        self.logger.info(f"Git ignore patterns added to: {gitignore_path}")

    def install_dependencies(self) -> None:
        """
        Install required dependencies for the auto environment.

        Installs all necessary Python packages from the requirements file
        using the current Python environment.
        """
        self.logger.info("Installing dependencies...")
        
        requirements_path = Path(self.project_path) / '.auto_project' / 'requirements.txt'
        if requirements_path.exists():
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', str(requirements_path)
                ], check=True, capture_output=True)
                self.logger.info("Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Failed to install dependencies: {e}")
                self.logger.error(f"Error output: {e.stderr.decode()}")
        else:
            self.logger.warning("Requirements file not found, skipping dependency installation")

    def setup_complete_environment(self) -> None:
        """
        Setup complete automatic project management environment.

        Orchestrates the complete setup process including directory creation,
        configuration generation, script creation, and dependency installation.
        """
        self.logger.info("Setting up complete automatic project management environment...")
        
        try:
            # Create project structure
            self.create_project_structure()
            
            # Create configuration
            self.create_auto_config()
            
            # Create automation scripts
            self.create_startup_script()
            self.create_stop_script()
            self.create_status_script()
            
            # Create development environment
            self.create_vscode_workspace()
            self.create_requirements_file()
            self.create_gitignore()
            
            # Install dependencies
            self.install_dependencies()
            
            self.logger.info("✅ Complete automatic project management environment setup!")
            self.logger.info("📁 Use './start_auto_management.sh' to start automatic management")
            self.logger.info("📊 Use './status_auto_management.sh' to check status")
            self.logger.info("🛑 Use './stop_auto_management.sh' to stop automatic management")
            self.logger.info("💻 Open 'auto_project_management.code-workspace' in VS Code")
            
        except Exception as e:
            self.logger.error(f"Setup failed: {e}")
            raise


def main() -> None:
    """
    Main entry point for the setup script.

    Provides command line interface for setting up the automatic project
    management environment with customizable options.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Setup Auto Project Management Environment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Setup in current directory
  %(prog)s --path /path/to/project  # Setup in specific directory
  %(prog)s --verbose               # Enable verbose logging
        """
    )
    
    parser.add_argument(
        '--path',
        help='Project path for setup (default: current directory)',
        default=os.getcwd()
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    try:
        setup = AutoEnvironmentSetup(args.path)
        setup.setup_complete_environment()
        
        print("\n🎉 Setup complete!")
        print("\nNext steps:")
        print("1. Run './start_auto_management.sh' to start automatic management")
        print("2. Open 'auto_project_management.code-workspace' in VS Code")
        print("3. Start coding - project management will happen automatically!")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
