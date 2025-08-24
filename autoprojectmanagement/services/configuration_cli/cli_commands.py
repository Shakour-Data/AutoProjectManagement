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
        'project_inputs/PM_JSON/user_inputs',
        'github_reports',
        'backups',
        'JSonDataBase/Inputs',
        'JSonDataBase/OutPuts'
    ]
    
    for directory in required_dirs:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"✅ Created directory: {directory}")

    logger.info("\n🎉 Project setup completed successfully!")
    logger.info("📋 Next steps:")
    logger.info("   - Add your project dependencies to requirements.txt")
    logger.info("   - Place JSON input files in 'project_inputs/PM_JSON/user_inputs'")
    logger.info("   - Run 'status' command to verify setup")


def create_github_project(args: argparse.Namespace) -> None:
    """
    Create a new GitHub project with full integration including repository,
    project board, issues, and documentation.
    
    Args:
        args: Command line arguments containing project details
    """
    manager = GitHubProjectManager()
    
    project_name = args.project_name
    description = args.description or ""
    github_username = args.github_username
    
    if not github_username:
        github_username = prompt_user("Enter your GitHub username")
    
    logger.info(f"🚀 Creating GitHub project '{project_name}'...")
    
    try:
        reports = manager.create_github_project_cli(project_name, description, github_username)
        
        logger.info("\n✅ GitHub project created successfully!")
        logger.info(f"📊 Repository: https://github.com/{github_username}/{project_name}")
        logger.info(f"📋 Project Board: https://github.com/{github_username}/{project_name}/projects")
        logger.info(f"📝 Issues: https://github.com/{github_username}/{project_name}/issues")
        
        # Save detailed report
        reports_dir = "github_reports"
        os.makedirs(reports_dir, exist_ok=True)
        report_file = os.path.join(reports_dir, f"{project_name}_setup_report.json")
        
        sync_with_github(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
