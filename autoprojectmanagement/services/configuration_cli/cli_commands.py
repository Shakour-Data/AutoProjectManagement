#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: cli_commands
File: cli_commands.py
Path: autoprojectmanagement/services/configuration_cli/cli_commands.py

Description:
    Cli Commands module

Author: AutoProjectManagement Team
Contact: team@autoprojectmanagement.com
Repository: https://github.com/autoprojectmanagement/autoprojectmanagement

Version Information:
    Current Version: 1.0.0
    Last Updated: 2025-08-14
    Python Version: 3.8+
    
Development Status:
    Status: Production/Stable
    Created: 2024-01-01
    Last Modified: 2025-08-14
    Modified By: AutoProjectManagement Team

Dependencies:
    - Python 3.8+
    - See requirements.txt for full dependency list

License: MIT License
Copyright: (c) 2024 AutoProjectManagement Team

Usage:
    This module is part of the AutoProjectManagement package.
    Import and use as needed within the package ecosystem.

Example:
    >>> from autoprojectmanagement.services.configuration_cli.cli_commands import {main_class}
    >>> instance = {main_class}()
    >>> instance.run()

Notes:
    - This file follows the AutoProjectManagement coding standards
    - All changes should be documented in the changelog below
    - Ensure compatibility with Python 3.8+

Changelog:
    1.0.0 (2024-01-01): Initial release
    1.0.1 (2025-08-14): {change_description}

TODO:
    - [ ] Add comprehensive error handling
    - [ ] Implement logging throughout
    - [ ] Add unit tests
    - [ ] Update documentation

================================================================================
"""


import argparse
import os
import subprocess
import logging
import json
from autoprojectmanagement.main_modules.utility_modules.setup_initialization import initialize_git_repo, create_virtualenv, install_dependencies, create_requirements_file, ensure_gitignore_excludes_venv
from .github_project_manager import GitHubProjectManager

logger = logging.getLogger("cli_commands")
logging.basicConfig(level=logging.INFO)

class CLICommands:
    def __init__(self):
        self.github_manager = GitHubProjectManager()

    def create_project(self, project_name, description=None, template=None):
        # Placeholder implementation for creating a project
        # You can expand this with actual logic
        print(f"Creating project: {project_name}")
        return True

    def get_project_status(self, project_id, format='table'):
        # Placeholder implementation for getting project status
        # You can expand this with actual logic
        return f"Status for project {project_id} in format {format}"

    def add_task(self, project_id, task_name, priority, description=None, assignee=None, due_date=None):
        # Placeholder implementation for adding a task
        # You can expand this with actual logic
        print(f"Adding task '{task_name}' to project {project_id} with priority {priority}")
        return True

    def generate_report(self, project_id, report_type, format='markdown'):
        # Placeholder implementation for generating a report
        # You can expand this with actual logic
        return f"Report {report_type} for project {project_id} in format {format}"

    def update_task_status(self, project_id, task_id, new_status):
        # Placeholder implementation for updating task status
        # You can expand this with actual logic
        print(f"Updating task {task_id} status to {new_status} in project {project_id}")
        return True

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command {command} failed with error: {e}")

def prompt_user(question, default=None):
    prompt = f"{question}"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    response = input(prompt)
    if not response and default is not None:
        return default
    return response

def setup_project():
    import shutil
    import os

    logger.info("Starting project setup...")

    # Remove PM_UserInputs folder if it exists
    pm_userinputs_path = os.path.join(os.getcwd(), 'PM_UserInputs')
    if os.path.exists(pm_userinputs_path) and os.path.isdir(pm_userinputs_path):
        shutil.rmtree(pm_userinputs_path)
        logger.info("Removed obsolete PM_UserInputs directory.")

    # Initialize git repo
    initialize_git_repo()

    # Ensure .gitignore excludes venv
    ensure_gitignore_excludes_venv()

    # Create requirements.txt
    create_requirements_file()

    # Create virtual environment
    create_virtualenv()

    # Install dependencies
    install_dependencies()

    logger.info("\nSetup complete.")
    logger.info("Please add your project dependencies to requirements.txt if not already done.")
    logger.info("Place your JSON input files in the 'project_inputs/PM_JSON/user_inputs' directory.")
    logger.info("You can then proceed with other commands.")

def create_github_project(args):
    """Create a new GitHub project with full integration"""
    manager = GitHubProjectManager()
    
    project_name = args.project_name
    description = args.description or ""
    github_username = args.github_username
    
    if not github_username:
        github_username = input("Enter your GitHub username: ")
    
    print(f"🚀 Creating GitHub project '{project_name}'...")
    
    try:
        reports = manager.create_github_project_cli(project_name, description, github_username)
        
        print("\n✅ GitHub project created successfully!")
        print(f"📊 Repository: https://github.com/{github_username}/{project_name}")
        print(f"📋 Project Board: https://github.com/{github_username}/{project_name}/projects")
        print(f"📝 Issues: https://github.com/{github_username}/{project_name}/issues")
        
        # Save detailed report
        reports_dir = "github_reports"
        os.makedirs(reports_dir, exist_ok=True)
        report_file = os.path.join(reports_dir, f"{project_name}_setup_report.json")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(reports, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
    except Exception as e:
        logger.error(f"Failed to create GitHub project: {e}")
        print(f"❌ Error: {e}")

def sync_with_github(args):
    """Sync existing project with GitHub"""
    manager = GitHubProjectManager()
    
    project_json = args.project_json
    github_username = args.github_username
    
    if not os.path.exists(project_json):
        logger.error(f"Project JSON file not found: {project_json}")
        return
    
    try:
        reports = manager.create_github_project_from_json(project_json, github_username)
        
        print("\n✅ Project synced with GitHub successfully!")
        print(f"📄 Reports saved to github_reports directory")
        
    except Exception as e:
        logger.error(f"Failed to sync project with GitHub: {e}")
        print(f"❌ Error: {e}")

def status():
    logger.info("Project Management Tool Status:")
    if os.path.exists('.git'):
        logger.info("- Git repository initialized.")
    else:
        logger.info("- Git repository not found.")
    if os.path.exists('venv'):
        logger.info("- Virtual environment exists.")
    else:
        logger.info("- Virtual environment not found.")
    if os.path.exists('requirements.txt'):
        logger.info("- requirements.txt file exists.")
    else:
        logger.info("- requirements.txt file not found.")
    if os.path.exists('project_inputs/PM_JSON/user_inputs'):
        logger.info("- project_inputs/PM_JSON/user_inputs directory exists.")
    else:
        logger.info("- project_inputs/PM_JSON/user_inputs directory not found.")
    if os.path.exists('github_reports'):
        logger.info("- GitHub reports directory exists.")
    else:
        logger.info("- GitHub reports directory not found.")

def main():
    parser = argparse.ArgumentParser(description="Project Management Tool CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Setup the project environment')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check project status')
    
    # Create GitHub project command
    github_parser = subparsers.add_parser('create-github', help='Create GitHub project with full integration')
    github_parser.add_argument('project_name', help='Name of the GitHub project')
    github_parser.add_argument('--description', help='Project description')
    github_parser.add_argument('--github-username', help='GitHub username (optional)')
    
    # Sync with GitHub command
    sync_parser = subparsers.add_parser('sync-github', help='Sync existing project with GitHub')
    sync_parser.add_argument('project_json', help='Path to project JSON file')
    sync_parser.add_argument('github_username', help='GitHub username')
    
    args = parser.parse_args()

    if args.command == 'setup':
        setup_project()
    elif args.command == 'status':
        status()
    elif args.command == 'create-github':
        create_github_project(args)
    elif args.command == 'sync-github':
        sync_with_github(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

# Standalone function wrappers for API imports
_cli_commands_instance = CLICommands()

def get_project_status(project_id, format='table'):
    return _cli_commands_instance.get_project_status(project_id, format)

def create_project(project_name, description=None, template=None):
    return _cli_commands_instance.create_project(project_name, description, template)

def add_task(project_id, task_name, priority, description=None, assignee=None, due_date=None):
    return _cli_commands_instance.add_task(project_id, task_name, priority, description, assignee, due_date)

def generate_report(project_id, report_type, format='markdown'):
    return _cli_commands_instance.generate_report(project_id, report_type, format)

def update_task_status(project_id, task_id, new_status):
    return _cli_commands_instance.update_task_status(project_id, task_id, new_status)
