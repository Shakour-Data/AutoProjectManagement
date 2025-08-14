#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/__init__.py
File: __init__.py
Purpose: Package initialization and module exports
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Package initialization and module exports within the AutoProjectManagement system
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
Package initialization and module exports within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


__version__ = "1.0.0"
__author__ = "AutoProjectManagement Team"
__email__ = "team@autoprojectmanagement.com"
__license__ = "MIT"
__copyright__ = "2024 AutoProjectManagement Team"

from typing import List, Dict, Any, Optional
import logging

# Import main system components
from .main_modules.project_management_system import ProjectManagementSystem
from .auto_runner import AutoRunner
from .cli import main as cli_main

# Configure package-level logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Main exports for package users
__all__: List[str] = [
    "ProjectManagementSystem",
    "AutoRunner",
    "cli_main",
]

# Package metadata for external reference
PACKAGE_INFO: Dict[str, Any] = {
    "name": "AutoProjectManagement",
    "version": __version__,
    "description": "Automated Project Management System",
    "author": __author__,
    "email": __email__,
    "license": __license__,
    "url": "https://github.com/AutoProjectManagement/AutoProjectManagement",
    "keywords": [
        "project-management",
        "automation",
        "task-tracking",
        "workflow-optimization",
        "git-integration",
        "risk-management",
    ],
}
