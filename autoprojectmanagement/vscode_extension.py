#!/usr/bin/env python3
"""
VS Code Extension Integration - Provides automatic project management within VS Code.

This module creates comprehensive VS Code extension support for the AutoProjectManagement
system, including workspace configuration, tasks, debugging, and extension development.

Key Features:
    - VS Code workspace configuration
    - Extension manifest generation
    - Task automation setup
    - Debugging configuration
    - Extension development environment
    - Integration with VS Code API

Usage:
    Command line usage:
        $ python -m autoprojectmanagement.vscode_extension --path /path/to/project
    
    Programmatic usage:
        >>> from autoprojectmanagement.vscode_extension import VSCodeExtension
        >>> extension = VSCodeExtension('/path/to/project')
        >>> extension.setup_complete_environment()

Configuration:
    The extension creates:
    - VS Code workspace file
    - Extension manifest (package.json)
    - Task configurations
    - Debug launch configurations
    - Settings and preferences

Examples:
    Basic setup:
        >>> extension = VSCodeExtension()
        >>> extension.setup_complete_environment()
    
    Custom project path:
        >>> extension = VSCodeExtension('/custom/path')
        >>> extension.setup_complete_environment()

For more information, visit: https://github.com/AutoProjectManagement/AutoProjectManagement
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('VSCodeExtension')

# Constants for extension configuration
EXTENSION_NAME = "AutoProjectManagement"
EXTENSION_DISPLAY_NAME = "Auto Project Management"
EXTENSION_DESCRIPTION = "Automatic project management without user interaction"
EXTENSION_VERSION = "1.0.0"
EXTENSION_PUBLISHER = "autoprojectmanagement"
EXTENSION_ENGINE = "^1.60.0"

# VS Code configuration paths
VSCODE_DIR = ".vscode"
TASKS_FILE = "tasks.json"
LAUNCH_FILE = "launch.json"
SETTINGS_FILE = "settings.json"
EXTENSIONS_FILE = "extensions.json"
WORKSPACE_FILE = "auto_project_management.code-workspace"

class VSCodeExtension:
    """
    Comprehensive VS Code extension setup for AutoProjectManagement.

    This class provides complete VS Code integration including workspace
    configuration, extension development, and task automation.

    Attributes:
        project_path: Absolute path to the project directory
        vscode_dir: Path to VS Code configuration directory
        logger: Configured logger instance

    Example:
        >>> extension = VSCodeExtension('/path/to/project')
        >>> extension.setup_complete_environment()
    """

    def __init__(self, project_path: Optional[str] = None) -> None:
        """
        Initialize VS Code extension with comprehensive configuration.

        Args:
            project_path: Optional path to the project directory.
                         If None, uses current working directory.

        Raises:
            ValueError: If the provided project_path does not exist
        """
        self.project_path = project_path or os.getcwd()
        self.vscode_dir = os.path.join(self.project_path, VSCODE_DIR)
        self.logger = logging.getLogger('VSCodeExtension')

        # Validate project path
        if not os.path.exists(self.project_path):
            raise ValueError(f"Project path does not exist: {self.project_path}")

        self.logger.info(f"Initializing VS Code extension for: {self.project_path}")

    def create_vscode_directory(self) -> None:
        """Create VS Code configuration directory if it doesn't exist."""
        os.makedirs(self.vscode_dir, exist_ok=True)
        self.logger.debug(f"Created VS Code directory: {self.vscode_dir}")

    def create_tasks_configuration(self) -> None:
        """Create comprehensive tasks.json for automation."""
        tasks_config = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Start Auto Management",
                    "type": "shell",
                    "command": "python",
                    "args": [
                        "-m",
                        "autoprojectmanagement.auto_runner",
                        "--path",
                        "${workspaceFolder}"
                    ],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    },
                    "problemMatcher": []
                },
                {
                    "label": "Stop Auto Management",
                    "type": "shell",
                    "command": "./stop_auto_management.sh",
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Check Status",
                    "type": "shell",
                    "command": "./status_auto_management.sh",
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Setup Environment",
                    "type": "shell",
                    "command": "python",
                    "args": [
                        "-m",
                        "autoprojectmanagement.setup_auto_environment"
                    ],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Run Tests",
                    "type": "shell",
                    "command": "python",
                    "args": [
                        "-m",
                        "pytest",
                        "tests/"
                    ],
                    "group": "test",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                }
            ]
        }

        tasks_path = os.path.join(self.vscode_dir, TASKS_FILE)
        with open(tasks_path, 'w', encoding='utf-8') as f:
            json.dump(tasks_config, f, indent=2)
        
        self.logger.info(f"Created tasks configuration: {tasks_path}")

    def create_launch_configuration(self) -> None:
        """Create comprehensive launch.json for debugging."""
        launch_config = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Auto Project Management",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/start_auto_management.sh",
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}",
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}"
                    }
                },
                {
                    "name": "Debug Auto Runner",
                    "type": "python",
                    "request": "launch",
                    "module": "autoprojectmanagement.auto_runner",
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}",
                    "args": ["--path", "${workspaceFolder}", "--verbose"],
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}"
                    }
                },
                {
                    "name": "Debug API Server",
                    "type": "python",
                    "request": "launch",
                    "module": "uvicorn",
                    "args": [
                        "autoprojectmanagement.api.app:app",
                        "--reload",
                        "--host",
                        "127.0.0.1",
                        "--port",
                        "8000"
                    ],
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}",
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}"
                    }
                }
            ]
        }

        launch_path = os.path.join(self.vscode_dir, LAUNCH_FILE)
        with open(launch_path, 'w', encoding='utf-8') as f:
            json.dump(launch_config, f, indent=2)
        
        self.logger.info(f"Created launch configuration: {launch_path}")

    def create_settings_configuration(self) -> None:
        """Create comprehensive settings.json for VS Code."""
        settings_config = {
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
            },
            "search.exclude": {
                "**/node_modules": True,
                "**/venv": True,
                "**/.venv": True,
                "**The attempt to edit the file failed due to an error opening the diff editor. I will try a different approach by reading the first 20 lines of the file to confirm the import section, then I will rewrite the import section with the added `import sys` line to fix the issue. This will ensure the file is updated correctly.

<read_file>
<path>autoprojectmanagement/vscode_extension.py</path>
</read_file>
