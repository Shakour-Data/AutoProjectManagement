"""
AutoProjectManagement - Automated Project Management System.

A comprehensive Python package for automated project management, task tracking,
and workflow optimization for software development teams.

This package provides:
- Automated project management without manual intervention
- Real-time progress tracking and reporting
- Risk assessment and mitigation strategies
- Git integration with automatic commits
- Resource allocation and management
- Task prioritization based on importance and urgency
- Integration with development tools (VS Code, GitHub, etc.)

Example:
    Basic usage of the AutoProjectManagement system:

    >>> from autoprojectmanagement import ProjectManagementSystem
    >>> system = ProjectManagementSystem()
    >>> system.initialize_system()
    >>> system.start_auto_management()

Features:
    - Automatic project initialization and setup
    - Continuous monitoring and progress tracking
    - Intelligent task prioritization
    - Risk assessment and mitigation
    - Automated git commits and progress updates
    - Real-time reporting and dashboards
    - Integration with popular development tools
    - Customizable workflows and configurations

For more information, visit: https://github.com/AutoProjectManagement/AutoProjectManagement
"""

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
