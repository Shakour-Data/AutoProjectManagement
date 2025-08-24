"""
CLI Commands for AutoProjectManagement Configuration
Purpose: Command-line interface for project setup, GitHub integration, and status checking
Author: AutoProjectManagement System
Version: 2.0.0
License: MIT
Description: Comprehensive CLI tool for project initialization, GitHub project creation, and system status monitoring
"""

import argparse
import os
import subprocess
import logging
import json
import shutil
from typing import Dict, List, Optional, Any

from autoprojectmanagement.main_modules.utility_modules.setup_initialization import (
    initialize_git_repo, 
    create_virtualenv, 
    install_dependencies, 
    create_requirements_file, 
    ensure_gitignore_excludes_venv
)
from autoprojectmanagement.services.integration_services.github_project_manager import GitHubProjectManager

# Configure logging
logger = logging.getLogger("cli_commands")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def run_command(command: List[str]) -> bool:
    """
    Execute a shell command with error handling.
    
    Args:
        command: List of command arguments
        
    Returns:
        bool: True if command executed successfully, False otherwise
    """
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command {command} failed with error: {e}")
        return False


def prompt_user(question: str, default: Optional[str] = None) -> str:
    """
    Prompt user for input with optional default value.
    
    Args:
        question: The question to ask the user
        default: Optional default value
        
    Returns:
        str: User input or default value
    """
    prompt = f"{question}"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    response = input(prompt)
    if not response and default is not None:
        return default
    return response


def setup_project() -> None:
    """
    Complete project setup including Git initialization, virtual environment creation,
    dependency installation, and directory structure preparation.
    """
    logger.info("🚀 Starting comprehensive project setup...")

    # Remove obsolete PM_UserInputs folder if it exists
    pm_userinputs_path = os.path.join(os.getcwd(), 'PM_UserInputs')
    if os.path.exists(pm_userinputs_path) and os.path.isdir(pm_userinputs_path):
        shutil.rmtree(pm_userinputs_path)
        logger.info("✅ Removed obsolete PM_UserInputs directory")

    # Initialize git repository
    if initialize_git_repo():
        logger.info("✅ Git repository initialized")
    else:
        logger.warning("⚠️  Git repository initialization may have issues")

    # Ensure .gitignore excludes venv
    if ensure_gitignore_excludes_venv():
        logger.info("✅ .gitignore configured to exclude virtual environment")
    else:
        logger.warning("⚠️  .gitignore configuration may have issues")

    # Create requirements.txt
    if create_requirements_file():
        logger.info("✅ requirements.txt file created")
    else:
        logger.warning("⚠️  requirements.txt creation may have issues")

    # Create virtual environment
    if create_virtualenv():
        logger.info("✅ Virtual environment created")
    else:
        logger.warning("⚠️  Virtual environment creation may have issues")

    # Install dependencies
    if install_dependencies():
        logger.info("✅ Dependencies installed")
    else:
        logger.warning("⚠️  Dependency installation may have issues")

    # Create necessary directories
    required_dirs = [
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
