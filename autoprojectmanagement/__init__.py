"""
AutoProjectManagement - Automated Project Management System

A comprehensive Python package for automated project management,
task tracking, and workflow optimization for software development teams.
"""

__version__ = "1.0.0"
__author__ = "AutoProjectManagement Team"
__email__ = "team@autoprojectmanagement.com"

from .main_modules.project_management_system import ProjectManagementSystem
from .main_modules.task_management import TaskManager
from .main_modules.progress_report import ProgressReporter

# Main exports
__all__ = [
    "ProjectManagementSystem",
    "TaskManager", 
    "ProgressReporter",
]
