#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: task_management_integration
File: task_management_integration.py
Path: autoprojectmanagement/main_modules/task_workflow_management/task_management_integration.py

Description:
    Task Management Integration module

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
    >>> from autoprojectmanagement.main_modules.task_workflow_management.task_management_integration import {main_class}
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


from .task_management import TaskManagement
from project_management.modules.services.github_integration import GitHubIntegration

def main():
    # Initialize Task Management and GitHub Integration
    tm = TaskManagement()
    gh = GitHubIntegration(token=None, repo='user/repo')  # Replace with actual repo

    # Example: Generate WBS from a project idea
    wbs_tasks = tm.generate_wbs_from_idea("Develop Project Management Tool")

    # Calculate urgency and importance, prioritize tasks
    tm.calculate_urgency_importance()
    prioritized_tasks = tm.prioritize_tasks()

    # Sync tasks to GitHub issues
    synced_tasks = gh.sync_tasks_to_github(prioritized_tasks)

    # Print synced tasks with GitHub issue numbers
    for task in synced_tasks:
        print(f"Task ID: {task.id}, Title: {task.title}, GitHub Issue #: {task.github_issue_number}")

if __name__ == "__main__":
    main()
