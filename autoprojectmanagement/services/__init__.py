#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/services/__init__.py
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


from .automation_services.auto_commit import UnifiedAutoCommit as AutoCommit
from .automation_services.backup_manager import BackupManager
from .configuration_cli.cli_commands import *
from .github_integration import GitHubIntegration
from .integration_services.integration_manager import IntegrationManager

__all__ = [
    "AutoCommit",
    "BackupManager",
    "GitHubIntegration",
    "IntegrationManager",
]
