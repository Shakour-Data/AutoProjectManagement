#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: main
File: main.py
Path: autoprojectmanagement/api/main.py

Description:
    Main module

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
    >>> from autoprojectmanagement.api.main import {main_class}
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


import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Import the app and server
from autoprojectmanagement.api.app import app
from autoprojectmanagement.api.server import start_server

# Export the app for uvicorn
__all__ = ['app']

if __name__ == "__main__":
    start_server()
