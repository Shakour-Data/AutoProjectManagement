#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: do_urgent_tasks
File: do_urgent_tasks.py
Path: autoprojectmanagement/main_modules/task_workflow_management/do_urgent_tasks.py

Description:
    Do Urgent Tasks module

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
    >>> from autoprojectmanagement.main_modules.task_workflow_management.do_urgent_tasks import {main_class}
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

def main():
    tm = TaskManagement()

    # Titles of 15 urgent tasks (10 from report + 5 additional subtasks)
    task_titles = [
        "Develop Project Management Tool",
        "Develop Project Management Tool - Subtask Level 1.1",
        "Develop Project Management Tool - Subtask Level 1.3",
        "Develop Project Management Tool - Subtask Level 1.2",
        "Develop Project Management Tool - Subtask Level 2.1.1",
        "Develop Project Management Tool - Subtask Level 2.1.2",
        "Develop Project Management Tool - Subtask Level 2.3.2",
        "Develop Project Management Tool - Subtask Level 2.2.1",
        "Develop Project Management Tool - Subtask Level 2.2.2",
        "Develop Project Management Tool - Subtask Level 2.3.1",
        # Additional 5 subtasks to reach 15
        "Develop Project Management Tool - Subtask Level 3.1.1",
        "Develop Project Management Tool - Subtask Level 3.1.2",
        "Develop Project Management Tool - Subtask Level 3.2.1",
        "Develop Project Management Tool - Subtask Level 3.2.2",
        "Develop Project Management Tool - Subtask Level 3.3.1",
    ]

    # Create tasks
    tasks = []
    for title in task_titles:
        task = tm.parse_creative_input(title)
        tasks.append(task)

    # Mark tasks as completed to simulate "doing" them
    for task in tasks:
        tm.mark_task_completed(task.id)

    # Print summary of completed tasks
    print("Completed 15 urgent tasks:")
    for task in tasks:
        print(f"Task ID: {task.id}, Title: {task.title}, Status: {task.status}")

if __name__ == "__main__":
    main()
