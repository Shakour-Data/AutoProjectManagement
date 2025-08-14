#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/main_modules/__init__.py
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


from .project_management_system import ProjectManagementSystem
from .task_workflow_management.task_management import TaskManagement
from .progress_reporting.progress_report import ProgressReport
from .planning_estimation.scheduler import Scheduler
from .resource_management.resource_management import ResourceManagement
from .communication_risk.risk_management import RiskManagement

__all__ = [
    "ProjectManagementSystem",
    "TaskManagement",
    "ProgressReport",
    "Scheduler",
    "ResourceManagement",
    "RiskManagement",
]
