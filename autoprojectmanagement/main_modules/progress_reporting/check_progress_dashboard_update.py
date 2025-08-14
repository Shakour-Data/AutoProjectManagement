#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: check_progress_dashboard_update
File: check_progress_dashboard_update.py
Path: autoprojectmanagement/main_modules/progress_reporting/check_progress_dashboard_update.py

Description:
    Check Progress Dashboard Update module

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
    >>> from autoprojectmanagement.main_modules.progress_reporting.check_progress_dashboard_update import {main_class}
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


from project_management.modules.main_modules.task_management import TaskManagement
from project_management.modules.main_modules.progress_report import generate_report

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def main():
    path = "docs/project_management/progress_dashboard.md"
    before = read_file(path)
    print("Content length before update:", len(before))

    tm = TaskManagement()
    tm.generate_wbs_from_idea("Develop Project Management Tool")
    generate_report(tm)

    after = read_file(path)
    print("Content length after update:", len(after))

    if before == after:
        print("No changes detected in progress_dashboard.md after update.")
    else:
        print("progress_dashboard.md updated successfully.")

if __name__ == "__main__":
    main()
