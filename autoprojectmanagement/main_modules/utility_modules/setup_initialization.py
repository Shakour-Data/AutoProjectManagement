#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: setup_initialization
File: setup_initialization.py
Path: autoprojectmanagement/main_modules/utility_modules/setup_initialization.py

Description:
    Setup Initialization module

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
    >>> from autoprojectmanagement.main_modules.utility_modules.setup_initialization import {main_class}
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


import os
import subprocess
import sys
import venv

def create_virtualenv(env_dir='venv'):
    """Create a virtual environment in the specified directory."""
    if not os.path.exists(env_dir):
        print(f"Creating virtual environment at {env_dir}...")
        venv.create(env_dir, with_pip=True)
        print("Virtual environment created.")
    else:
        print(f"Virtual environment already exists at {env_dir}.")

def install_dependencies(env_dir='venv', requirements_file='../requirements.txt'):
    """Install dependencies from requirements.txt into the virtual environment."""
    pip_executable = os.path.join(env_dir, 'bin', 'pip')
    if not os.path.exists(pip_executable):
        print("pip not found in virtual environment. Please check the environment setup.")
        return
    if not os.path.exists(requirements_file):
        print(f"{requirements_file} not found. Skipping dependency installation.")
        return
    print(f"Installing dependencies from {requirements_file}...")
    subprocess.check_call([pip_executable, 'install', '-r', requirements_file])
    print("Dependencies installed.")

def initialize_git_repo():
    """Initialize a git repository in the current directory if not already a git repo."""
    if os.path.exists('.git'):
        print("Git repository already initialized.")
        return
    print("Initializing git repository...")
    subprocess.run(['git', 'init'], check=True)
    print("Git repository initialized.")

def ensure_gitignore_excludes_venv(gitignore_path='.gitignore', venv_dirs=None):
    if venv_dirs is None:
        venv_dirs = ['venv/', '.venv/', 'ENV/', 'env/']
    if not os.path.exists(gitignore_path):
        print(f"{gitignore_path} not found. Creating a new one.")
        lines = []
    else:
        with open(gitignore_path, 'r') as f:
            lines = f.read().splitlines()
    updated = False
    for venv_dir in venv_dirs:
        if venv_dir not in lines:
            lines.append(venv_dir)
            updated = True
    if updated:
        with open(gitignore_path, 'w') as f:
            f.write('\n'.join(lines) + '\n')
        print(f"Updated {gitignore_path} to exclude virtual environment directories.")
    else:
        print(f"{gitignore_path} already excludes virtual environment directories.")

def create_requirements_file(requirements_file='requirements.txt'):
    """Create an empty requirements.txt file if it does not exist."""
    if not os.path.exists(requirements_file):
        with open(requirements_file, 'w') as f:
            f.write("# Add your project dependencies here\n")
        print(f"Created {requirements_file}. Please add your project dependencies to this file.")
    else:
        print(f"{requirements_file} already exists.")

def main():
    ensure_gitignore_excludes_venv()
    initialize_git_repo()
    create_requirements_file()
    create_virtualenv()
    install_dependencies()

if __name__ == '__main__':
    main()
