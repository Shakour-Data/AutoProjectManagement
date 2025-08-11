#!/usr/bin/env python3
"""
AutoProjectManagement Reorganization Migration Script
This script implements the reorganization based on REORGANIZATION_MAPPING.md
"""

import os
import shutil
import sys
from pathlib import Path

class ReorganizationMigrator:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.main_modules_path = self.base_path / "autoprojectmanagement" / "main_modules"
        self.services_path = self.base_path / "autoprojectmanagement" / "services"
        
    def create_directories(self):
        """Create new directory structure"""
        directories = [
            self.main_modules_path / "task_workflow_management",
            self.main_modules_path / "progress_reporting",
            self.main_modules_path / "data_collection_processing",
            self.main_modules_path / "planning_estimation",
            self.main_modules_path / "communication_risk",
            self.main_modules_path / "resource_management",
            self.main_modules_path / "quality_commit_management",
            self.main_modules_path / "utility_modules",
            self.services_path / "automation_services",
            self.services_path / "integration_services",
            self.services_path / "configuration_cli"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            # Create __init__.py files
            init_file = directory / "__init__.py"
            init_file.touch(exist_ok=True)
            
    def migrate_main_modules(self):
        """Migrate main modules to new structure"""
        migrations = {
            "task_workflow_management": [
                "check_progress_dashboard_update.py",
                "do_important_tasks.py",
                "do_urgent_tasks.py",
                "task_management.py"
            ],
            "progress_reporting": [
                "progress_calculator_refactored.py",
                "progress_data_generator_refactored.py",
                "progress_report.py",
                "dashboards_reports.py"
            ],
            "data_collection_processing": [
