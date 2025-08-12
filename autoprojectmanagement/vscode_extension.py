#!/usr/bin/env python3
"""
VS Code Extension Integration - Provides automatic project management within VS Code
"""

import os
import json
import logging
import subprocess
from pathlib import Path

class VSCodeExtension:
    """VS Code Extension for automatic project management"""
    
    def __init__(self, project_path=None):
        self.project_path = project_path or os.getcwd()
        self.extension_dir = os.path.join(self.project_path, '.vscode')
        self.logger = logging.getLogger('VSCodeExtension')
        
    def setup_extension(self):
        """Setup VS Code extension for automatic project management"""
        self.logger.info("Setting up VS Code extension...")
        
        # Create .vscode directory
        os.makedirs(self.extension_dir, exist_ok=True)
        
        # Create extension configuration
        self.create_extension_config()
        
        # Create tasks.json for automatic operations
        self.create_tasks_json()
        
        # Create settings.json for automatic features
        self.create_settings_json()
        
        # Create launch.json for debugging
        self.create_launch_json()
        
        self.logger.info("VS Code extension setup complete")
        
    def create_extension_config(self):
        """Create extension configuration file"""
        config = {
            "name": "AutoProjectManagement",
            "displayName": "Auto Project Management",
            "description": "Automatic project management without user interaction",
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
                        "command": "autoProjectManagement.start",
                        "title": "Start Auto Management"
                    },
                    {
                        "command": "autoProjectManagement.stop",
                        "title": "Stop Auto Management"
                    },
                    {
                        "command": "autoProjectManagement.status",
                        "title": "Show Status"
                    }
                ],
                "configuration": {
                    "title": "Auto Project Management",
                    "properties": {
                        "autoProjectManagement.enabled": {
                            "type": "boolean",
                            "default": True,
                            "description": "Enable automatic project management"
                        },
                        "autoProjectManagement.autoCommit": {
                            "type": "boolean",
                            "default": True,
                            "description": "Enable automatic commits"
                        },
                        "autoProjectManagement.autoProgress": {
                            "type": "boolean",
                            "default": True,
                            "description": "Enable automatic progress tracking"
                        }
                    }
                }
            }
        }
        
        config_path = os.path.join(self.extension_dir, 'package.json')
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
    def create_tasks_json(self):
        """Create tasks.json for automatic operations"""
        tasks = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Auto Project Management",
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
                        "reveal": "silent",
                        "focus": False,
                        "panel": "shared"
                    },
                    "runOptions": {
                        "runOn": "folderOpen"
                    }
                },
                {
                    "label": "Auto Commit",
                    "type": "shell",
                    "command": "python",
                    "args": [
                        "-c",
                        "from autoprojectmanagement.services.auto_commit import AutoCommit; AutoCommit().run_auto_commit()"
                    ],
                    "group": "build",
                    "presentation": {
                        "echo": False,
                        "reveal": "never"
                    },
                    "runOptions": {
                        "runOn": "default"
                    }
                }
            ]
        }
        
        tasks_path = os.path.join(self.extension_dir, 'tasks.json')
        with open(tasks_path, 'w') as f:
            json.dump(tasks, f, indent=2)
            
    def create_settings_json(self):
        """Create settings.json for automatic features"""
        settings = {
            "files.autoSave": "afterDelay",
            "files.autoSaveDelay": 1000,
            "git.autofetch": True,
            "git.enableSmartCommit": True,
            "git.postCommitCommand": "push",
            "extensions.autoUpdate": True,
            "autoProjectManagement.enabled": True,
            "autoProjectManagement.autoCommit": True,
            "autoProjectManagement.autoProgress": True
        }
        
        settings_path = os.path.join(self.extension_dir, 'settings.json')
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)
            
    def create_launch_json(self):
        """Create launch.json for debugging"""
        launch = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Auto Project Management",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/.vscode/auto_runner.py",
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}",
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}"
                    }
                }
            ]
        }
        
        launch_path = os.path.join(self.extension_dir, 'launch.json')
        with open(launch_path, 'w') as f:
            json.dump(launch, f, indent=2)
            
    def create_extension_files(self):
        """Create extension JavaScript files"""
        extension_js = '''
const vscode = require('vscode');
const { exec } = require('child_process');

function activate(context) {
    console.log('Auto Project Management extension is now active!');
    
    let disposable = vscode.commands.registerCommand('autoProjectManagement.start', function () {
        const terminal = vscode.window.createTerminal('Auto Project Management');
        terminal.sendText('python -m autoprojectmanagement.auto_runner');
        terminal.show();
    });
    
    let disposable2 = vscode.commands.registerCommand('autoProjectManagement.stop', function () {
        vscode.window.showInformationMessage('Stopping auto project management...');
    });
    
    let disposable3 = vscode.commands.registerCommand('autoProjectManagement.status', function () {
        vscode.window.showInformationMessage('Auto project management is running');
    });
    
    context.subscriptions.push(disposable);
    context.subscriptions.push(disposable2);
    context.subscriptions.push(disposable3);
    
    // Auto start on workspace open
    const config = vscode.workspace.getConfiguration('autoProjectManagement');
    if (config.get('enabled')) {
        const terminal = vscode.window.createTerminal('Auto Project Management');
        terminal.sendText('python -m autoprojectmanagement.auto_runner');
        terminal.hide();
    }
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
'''
        
        out_dir = os.path.join(self.extension_dir, 'out')
        os.makedirs(out_dir, exist_ok=True)
        
        extension_path = os.path.join(out_dir, 'extension.js')
        with open(extension_path, 'w') as f:
            f.write(extension_js)
            
    def install_extension(self):
        """Install the extension in VS Code"""
        try:
            subprocess.run(['code', '--install-extension', '.'], cwd=self.extension_dir, check=True)
            self.logger.info("VS Code extension installed successfully")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install extension: {e}")
            
    def setup_complete_environment(self):
        """Setup complete VS Code environment"""
        self.setup_extension()
        self.create_extension_files()
        self.logger.info("VS Code environment setup complete")


def main():
    """Main entry point for VS Code extension setup"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup VS Code Extension')
    parser.add_argument('--path', help='Project path', default=os.getcwd())
    
    args = parser.parse_args()
    
    extension = VSCodeExtension(args.path)
    extension.setup_complete_environment()
    
    print("VS Code extension setup complete!")
    print("Please reload VS Code window to activate the extension")


if __name__ == "__main__":
    main()