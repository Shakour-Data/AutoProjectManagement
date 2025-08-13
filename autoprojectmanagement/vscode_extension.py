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
                "**/.auto_project": True
            }
        }

        settings_path = os.path.join(self.vscode_dir, SETTINGS_FILE)
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings_config, f, indent=2)
        
        self.logger.info(f"Created settings configuration: {settings_path}")

    def create_extensions_configuration(self) -> None:
        """Create extensions.json with recommended extensions."""
        extensions_config = {
            "recommendations": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-python.black-formatter",
                "visualstudioexptteam.vscodeintellicode",
                "ms-vscode.makefile-tools",
                "eamodio.gitlens",
                "ms-azuretools.vscode-docker",
                "ms-vscode-remote.remote-containers"
            ]
        }

        extensions_path = os.path.join(self.vscode_dir, EXTENSIONS_FILE)
        with open(extensions_path, 'w', encoding='utf-8') as f:
            json.dump(extensions_config, f, indent=2)
        
        self.logger.info(f"Created extensions configuration: {extensions_path}")

    def create_workspace_configuration(self) -> None:
        """Create comprehensive workspace configuration."""
        workspace_config = {
            "folders": [
                {
                    "path": self.project_path
                }
            ],
            "settings": {
                "python.pythonPath": "./venv/bin/python",
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                "python.formatting.provider": "black",
                "editor.formatOnSave": True
            }
        }

        workspace_path = os.path.join(self.project_path, WORKSPACE_FILE)
        with open(workspace_path, 'w', encoding='utf-8') as f:
            json.dump(workspace_config, f, indent=2)
        
        self.logger.info(f"Created workspace configuration: {workspace_path}")

    def create_extension_manifest(self) -> None:
        """Create package.json for VS Code extension development."""
        manifest = {
            "name": EXTENSION_NAME,
            "displayName": EXTENSION_DISPLAY_NAME,
            "description": EXTENSION_DESCRIPTION,
            "version": EXTENSION_VERSION,
            "publisher": EXTENSION_PUBLISHER,
            "engines": {
                "vscode": EXTENSION_ENGINE
            },
            "categories": [
                "Other"
            ],
            "activationEvents": [
                "onCommand:autoprojectmanagement.start",
                "onCommand:autoprojectmanagement.stop",
                "onCommand:autoprojectmanagement.configure"
            ],
            "main": "./out/extension.js",
            "contributes": {
                "commands": [
                    {
                        "command": "autoprojectmanagement.start",
                        "title": "Start Auto Project Management"
                    },
                    {
                        "command": "autoprojectmanagement.stop",
                        "title": "Stop Auto Project Management"
                    },
                    {
                        "command": "autoprojectmanagement.configure",
                        "title": "Configure Auto Project Management"
                    }
                ],
                "configuration": {
                    "title": "Auto Project Management",
                    "properties": {
                        "autoprojectmanagement.projectPath": {
                            "type": "string",
                            "default": "${workspaceFolder}",
                            "description": "Path to the project root"
                        },
                        "autoprojectmanagement.autoStart": {
                            "type": "boolean",
                            "default": True,
                            "description": "Automatically start management on workspace load"
                        }
                    }
                }
            },
            "scripts": {
                "vscode:prepublish": "npm run compile",
                "compile": "tsc -p ./",
                "watch": "tsc -watch -p ./",
                "pretest": "npm run compile",
                "test": "node ./out/test/runTest.js"
            },
            "devDependencies": {
                "@types/vscode": "^1.60.0",
                "@types/node": "14.x",
                "@types/mocha": "^8.2.2",
                "typescript": "^4.4.3"
            }
        }

        manifest_path = os.path.join(self.project_path, "package.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        self.logger.info(f"Created extension manifest: {manifest_path}")

    def setup_complete_environment(self) -> None:
        """
        Setup complete VS Code environment with all configurations.
        
        This includes:
        - VS Code directory
        - Tasks configuration
        - Launch configuration
        - Settings
        - Recommended extensions
        - Workspace configuration
        - Extension manifest
        """
        self.create_vscode_directory()
        self.create_tasks_configuration()
        self.create_launch_configuration()
        self.create_settings_configuration()
        self.create_extensions_configuration()
        self.create_workspace_configuration()
        self.create_extension_manifest()
        
        self.logger.info("Completed VS Code environment setup")

def main() -> None:
    """Command line interface for VS Code extension setup."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Setup VS Code environment for AutoProjectManagement"
    )
    parser.add_argument(
        "--path",
        type=str,
        default=os.getcwd(),
        help="Path to the project directory"
    )
    
    args = parser.parse_args()
    
    try:
        extension = VSCodeExtension(args.path)
        extension.setup_complete_environment()
        print("VS Code environment setup completed successfully")
    except Exception as e:
        logger.error(f"Error setting up VS Code environment: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()