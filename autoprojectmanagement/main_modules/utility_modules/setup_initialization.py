#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/utility_modules/setup_initialization.py
File: setup_initialization.py
Purpose: System initialization
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: System initialization within the AutoProjectManagement system
"""

import logging
from typing import Dict, Any, Optional, List, Union
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CURRENT_VERSION = "2.0.0"
PYTHON_MIN_VERSION = "3.8+"
CREATED_DATE = "2025-08-14"
MODIFIED_DATE = "2025-08-14"

# Module-level docstring
__doc__ = """
System initialization within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import logging
import os
import subprocess
import sys
import venv
from pathlib import Path
from typing import List, Optional, Tuple, Union

# Constants
DEFAULT_ENV_DIR = 'venv'
DEFAULT_REQUIREMENTS_FILE = 'requirements.txt'
DEFAULT_GITIGNORE_FILE = '.gitignore'
VENV_EXCLUDE_PATTERNS = ['venv/', '.venv/', 'ENV/', 'env/', '.env/']
PYTHON_EXECUTABLE = 'python3'
PIP_EXECUTABLE = 'pip'

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SetupInitializationError(Exception):
    """Custom exception for setup initialization errors."""
    pass


class SetupInitialization:
    """
    Comprehensive setup initialization class for AutoProjectManagement development environment.
    
    This class provides methods for:
    - Creating virtual environments
    - Installing project dependencies
    - Initializing git repositories
    - Configuring .gitignore files
    - Setting up development environment prerequisites
    
    Attributes:
        project_root (Path): The root directory of the project
        env_dir (Path): Path to the virtual environment directory
        requirements_file (Path): Path to the requirements.txt file
    """
    
    def __init__(self, project_root: Optional[Union[str, Path]] = None) -> None:
        """
        Initialize the SetupInitialization instance.
        
        Args:
            project_root: The root directory of the project. If None, uses current working directory.
        
        Example:
            >>> setup = SetupInitialization('/path/to/project')
            >>> setup.run_full_setup()
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.env_dir = self.project_root / DEFAULT_ENV_DIR
        self.requirements_file = self.project_root / DEFAULT_REQUIREMENTS_FILE
        self.gitignore_file = self.project_root / DEFAULT_GITIGNORE_FILE
        
    def create_virtual_environment(self, env_dir: Optional[str] = None) -> bool:
        """
        Create a virtual environment in the specified directory.
        
        Args:
            env_dir: Directory name for the virtual environment. Defaults to 'venv'.
        
        Returns:
            bool: True if environment was created, False if it already exists.
        
        Raises:
            SetupInitializationError: If virtual environment creation fails.
        
        Example:
            >>> setup = SetupInitialization()
            >>> success = setup.create_virtual_environment('myenv')
            >>> print(f"Environment created: {success}")
        """
        target_dir = self.project_root / (env_dir or DEFAULT_ENV_DIR)
        
        if target_dir.exists():
            logger.info(f"Virtual environment already exists at {target_dir}")
            return False
            
        try:
            logger.info(f"Creating virtual environment at {target_dir}...")
            venv.create(str(target_dir), with_pip=True)
            logger.info("Virtual environment created successfully")
            return True
        except Exception as e:
            raise SetupInitializationError(
                f"Failed to create virtual environment: {str(e)}"
            ) from e
    
    def install_dependencies(
        self, 
        env_dir: Optional[str] = None,
        requirements_file: Optional[str] = None
    ) -> bool:
        """
        Install dependencies from requirements.txt into the virtual environment.
        
        Args:
            env_dir: Virtual environment directory name. Defaults to 'venv'.
            requirements_file: Path to requirements file. Defaults to 'requirements.txt'.
        
        Returns:
            bool: True if dependencies were installed, False if skipped.
        
        Raises:
            SetupInitializationError: If dependency installation fails.
        
        Example:
            >>> setup = SetupInitialization()
            >>> if setup.create_virtual_environment():
            ...     setup.install_dependencies()
        """
        target_env_dir = self.project_root / (env_dir or DEFAULT_ENV_DIR)
        target_requirements = self.project_root / (requirements_file or DEFAULT_REQUIREMENTS_FILE)
        
        # Determine pip executable based on OS
        if os.name == 'nt':  # Windows
            pip_executable = target_env_dir / 'Scripts' / 'pip.exe'
        else:  # Unix-like
            pip_executable = target_env_dir / 'bin' / 'pip'
            
        if not pip_executable.exists():
            raise SetupInitializationError(
                f"pip not found in virtual environment at {pip_executable}"
            )
            
        if not target_requirements.exists():
            logger.warning(
                f"{target_requirements} not found. Creating empty requirements file."
            )
            self.create_requirements_file(str(target_requirements))
            return False
            
        try:
            logger.info(f"Installing dependencies from {target_requirements}...")
            subprocess.check_call([
                str(pip_executable), 
                'install', 
                '-r', 
                str(target_requirements)
            ])
            logger.info("Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            raise SetupInitializationError(
                f"Failed to install dependencies: {str(e)}"
            ) from e
    
    def initialize_git_repository(self) -> bool:
        """
        Initialize a git repository in the project directory if not already initialized.
        
        Returns:
            bool: True if repository was initialized, False if it already exists.
        
        Raises:
            SetupInitializationError: If git initialization fails.
        
        Example:
            >>> setup = SetupInitialization()
            >>> if setup.initialize_git_repository():
            ...     print("Git repository initialized")
        """
        git_dir = self.project_root / '.git'
        
        if git_dir.exists():
            logger.info("Git repository already initialized")
            return False
            
        try:
            logger.info("Initializing git repository...")
            subprocess.run(
                ['git', 'init'], 
                cwd=str(self.project_root), 
                check=True,
                capture_output=True,
                text=True
            )
            logger.info("Git repository initialized successfully")
            return True
        except subprocess.CalledProcessError as e:
            raise SetupInitializationError(
                f"Failed to initialize git repository: {str(e)}"
            ) from e
    
    def ensure_gitignore_excludes_venv(
        self, 
        gitignore_path: Optional[str] = None,
        venv_patterns: Optional[List[str]] = None
    ) -> bool:
        """
        Ensure .gitignore excludes virtual environment directories.
        
        Args:
            gitignore_path: Path to .gitignore file. Defaults to '.gitignore'.
            venv_patterns: List of virtual environment patterns to exclude.
        
        Returns:
            bool: True if .gitignore was updated, False if no changes needed.
        
        Example:
            >>> setup = SetupInitialization()
            >>> updated = setup.ensure_gitignore_excludes_venv()
            >>> print(f"Gitignore updated: {updated}")
        """
        target_gitignore = self.project_root / (gitignore_path or DEFAULT_GITIGNORE_FILE)
        patterns = venv_patterns or VENV_EXCLUDE_PATTERNS
        
        # Read existing .gitignore content
        if target_gitignore.exists():
            with open(target_gitignore, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
        else:
            lines = []
            logger.info(f"{target_gitignore} not found. Creating new file.")
        
        # Check which patterns are missing
        missing_patterns = [p for p in patterns if p not in lines]
        
        if not missing_patterns:
            logger.info("Gitignore already excludes virtual environment directories")
            return False
            
        # Add missing patterns
        if lines and lines[-1].strip():
            lines.append('')  # Add empty line before new patterns
            
        lines.extend(missing_patterns)
        
        try:
            with open(target_gitignore, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines) + '\n')
            logger.info(f"Updated {target_gitignore} with virtual environment exclusions")
            return True
        except IOError as e:
            raise SetupInitializationError(
                f"Failed to update .gitignore: {str(e)}"
            ) from e
    
    def create_requirements_file(
        self, 
        requirements_path: Optional[str] = None,
        initial_packages: Optional[List[str]] = None
    ) -> bool:
        """
        Create a requirements.txt file with initial content if it doesn't exist.
        
        Args:
            requirements_path: Path to requirements file. Defaults to 'requirements.txt'.
            initial_packages: List of initial packages to include.
        
        Returns:
            bool: True if file was created, False if it already exists.
        
        Example:
            >>> setup = SetupInitialization()
            >>> setup.create_requirements_file(initial_packages=['requests', 'click'])
        """
        target_requirements = self.project_root / (requirements_path or DEFAULT_REQUIREMENTS_FILE)
        
        if target_requirements.exists():
            logger.info(f"{target_requirements} already exists")
            return False
            
        default_content = [
            "# AutoProjectManagement Dependencies",
            "# Add your project dependencies here",
            "# Example:",
            "# requests>=2.25.1",
            "# click>=8.0.0",
            "",
            "# Development dependencies",
            "# pytest>=6.2.0",
            "# black>=21.0.0",
            "# flake8>=3.9.0",
        ]
        
        if initial_packages:
            default_content.extend([
                "",
                "# Initial packages",
                *[pkg for pkg in initial_packages]
            ])
            
        try:
            with open(target_requirements, 'w', encoding='utf-8') as f:
                f.write('\n'.join(default_content) + '\n')
            logger.info(f"Created {target_requirements}")
            return True
        except IOError as e:
            raise SetupInitializationError(
                f"Failed to create requirements file: {str(e)}"
            ) from e
    
    def check_python_version(self) -> Tuple[bool, str]:
        """
        Check if the Python version meets minimum requirements.
        
        Returns:
            Tuple[bool, str]: (is_compatible, message)
        
        Example:
            >>> setup = SetupInitialization()
            >>> compatible, msg = setup.check_python_version()
            >>> print(msg)
        """
        min_version = (3, 8)
        current_version = sys.version_info[:2]
        
        if current_version >= min_version:
            return True, f"Python {sys.version} is compatible"
        else:
            return False, (
                f"Python {'.'.join(map(str, current_version))} detected. "
                f"Python {'.'.join(map(str, min_version))}+ is required"
            )
    
    def run_full_setup(self) -> bool:
        """
        Run the complete setup process.
        
        Returns:
            bool: True if setup completed successfully, False otherwise.
        
        Example:
            >>> setup = SetupInitialization()
            >>> success = setup.run_full_setup()
            >>> print(f"Setup completed: {success}")
        """
        try:
            logger.info("Starting AutoProjectManagement setup...")
            
            # Check Python version
            compatible, msg = self.check_python_version()
            if not compatible:
                logger.error(msg)
                return False
            logger.info(msg)
            
            # Ensure gitignore excludes venv
            self.ensure_gitignore_excludes_venv()
            
            # Initialize git repository
            self.initialize_git_repository()
            
            # Create requirements file
            self.create_requirements_file()
            
            # Create virtual environment
            venv_created = self.create_virtual_environment()
            
            # Install dependencies if venv was created
            if venv_created:
                self.install_dependencies()
            else:
                logger.info("Skipping dependency installation (venv already exists)")
            
            logger.info("AutoProjectManagement setup completed successfully!")
            return True
            
        except SetupInitializationError as e:
            logger.error(f"Setup failed: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during setup: {str(e)}")
            return False
    
    def get_setup_status(self) -> dict:
        """
        Get the current setup status for diagnostic purposes.
        
        Returns:
            dict: Dictionary containing setup status information.
        
        Example:
            >>> setup = SetupInitialization()
            >>> status = setup.get_setup_status()
            >>> print(status)
        """
        return {
            'project_root': str(self.project_root),
            'venv_exists': self.env_dir.exists(),
            'requirements_exists': self.requirements_file.exists(),
            'git_initialized': (self.project_root / '.git').exists(),
            'gitignore_exists': self.gitignore_file.exists(),
            'python_version': sys.version,
            'platform': sys.platform,
        }


def main() -> None:
    """
    Main entry point for command-line usage.
    
    This function provides a simple CLI interface for running the setup process.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AutoProjectManagement Setup Initialization'
    )
    parser.add_argument(
        '--project-root',
        type=str,
        help='Project root directory (default: current directory)'
    )
    parser.add_argument(
        '--env-dir',
        type=str,
        default=DEFAULT_ENV_DIR,
        help='Virtual environment directory name (default: venv)'
    )
    parser.add_argument(
        '--requirements',
        type=str,
        default=DEFAULT_REQUIREMENTS_FILE,
        help='Requirements file path (default: requirements.txt)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    setup = SetupInitialization(args.project_root)
    success = setup.run_full_setup()
    
    if success:
        print("\n✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Activate the virtual environment:")
        if os.name == 'nt':  # Windows
            print(f"   .\\{args.env_dir}\\Scripts\\activate")
        else:  # Unix-like
            print(f"   source {args.env_dir}/bin/activate")
        print("2. Install additional dependencies as needed")
        print("3. Start developing with AutoProjectManagement!")
    else:
        print("\n❌ Setup failed. Check the logs above for details.")
        sys.exit(1)


if __name__ == '__main__':
    main()
