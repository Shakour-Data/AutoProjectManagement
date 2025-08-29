#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: update_all_python_headers.py
File: update_all_python_headers.py
Purpose: Update headers of all Python files in AutoProjectManagement
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Script to update all Python files with standardized headers
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import List

# Standard header template
STANDARD_HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: {path}
File: {filename}
Purpose: {purpose}
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: {description}
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
CREATED_DATE = "{created_date}"
MODIFIED_DATE = "{modified_date}"

# Module-level docstring
__doc__ = """
{description}

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"
'''

# File purposes mapping
FILE_PURPOSES = {
    '__init__.py': 'Package initialization and module exports',
    'auto_runner.py': 'Main automation runner for AutoProjectManagement system',
    'cli.py': 'Command-line interface for AutoProjectManagement',
    'setup_auto_environment.py': 'Environment setup and initialization',
    'vscode_extension.py': 'VS Code extension integration',
    'vscode_extension_status_bar.py': 'VS Code status bar integration',
    'app.py': 'Flask application setup',
    'main.py': 'API main entry point',
    'server.py': 'API server configuration',
    'services.py': 'API services and endpoints',
    'project_management_system.py': 'Core project management system',
    'communication_management.py': 'Communication management module',
    'risk_management.py': 'Risk management functionality',
    'risk_management_improved.py': 'Enhanced risk management system',
    'communication_risk_doc_integration.py': 'Communication risk documentation integration',
    'db_data_collector.py': 'Database data collection',
    'input_handler.py': 'Input data handling and validation',
    'progress_data_generator.py': 'Progress data generation',
    'workflow_data_collector.py': 'Workflow data collection',
    'estimation_management.py': 'Project estimation management',
    'estimation_management_improved.py': 'Enhanced estimation management',
    'gantt_chart_data.py': 'Gantt chart data generation',
    'scheduler.py': 'Task scheduling system',
    'scope_management.py': 'Project scope management',
    'scope_management_improved.py': 'Enhanced scope management',
    'wbs_aggregator.py': 'WBS (Work Breakdown Structure) aggregation',
    'wbs_merger.py': 'WBS merging functionality',
    'wbs_parser.py': 'WBS parsing and processing',
    'check_progress_dashboard_update.py': 'Progress dashboard update checking',
    'dashboards_reports.py': 'Dashboard and report generation',
    'progress_calculator.py': 'Progress calculation engine',
    'progress_report.py': 'Progress report generation',
    'reporting.py': 'General reporting functionality',
    'commit_progress_manager.py': 'Commit progress tracking',
    'git_progress_updater.py': 'Git progress updates',
    'github_actions_automation.py': 'GitHub Actions automation',
    'quality_management.py': 'Quality management system',
    'resource_allocation_manager.py': 'Resource allocation management',
    'resource_leveling.py': 'Resource leveling optimization',
    'resource_management.py': 'Resource management system',
    'do_important_tasks.py': 'Important task execution',
    'do_urgent_tasks.py': 'Urgent task execution',
    'importance_urgency_calculator.py': 'Importance and urgency calculation',
    'task_executor.py': 'Task execution engine',
    'task_management_integration.py': 'Task management integration',
    'task_management.py': 'Task management system',
    'feature_weights.py': 'Feature weight calculation',
    'project_views_generator.py': 'Project views generation',
    'setup_automation.py': 'Setup automation functionality',
    'setup_initialization.py': 'System initialization',
    'time_management.py': 'Time management and scheduling',
    'github_integration.py': 'GitHub integration services',
    'json_data_linker.py': 'JSON data linking and management',
    'status_service.py': 'Status service functionality',
    'auto_commit.py': 'Automated commit functionality',
    'backup_manager.py': 'Backup management system',
    'wiki_git_operations.py': 'Wiki Git operations',
    'cli_commands.py': 'CLI command implementations',
    'config_and_token_management.py': 'Configuration and token management',
    'github_project_manager.py': 'GitHub project management',
    'integration_manager.py': 'Integration management',
    'vscode_extension_installer.py': 'VS Code extension installer',
    'wiki_page_mapper.py': 'Wiki page mapping',
    'wiki_sync_service.py': 'Wiki synchronization service',
    'documentation_standard.py': 'Documentation standards',
    'header_updater.py': 'Header update functionality',
    'standard_header.py': 'Standard header template'
}

def get_file_purpose(filename: str) -> str:
    """Get the purpose for a given filename."""
    return FILE_PURPOSES.get(filename, f'Module for {filename.replace("_", " ").title()}')

def get_file_description(filename: str) -> str:
    """Get the description for a given filename."""
    base_purpose = get_file_purpose(filename)
    return f'{base_purpose} within the AutoProjectManagement system'

def update_file_header(file_path: str) -> bool:
    """Update the header of a single Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has standard header
        if content.startswith('#!/usr/bin/env python3'):
            print(f"Skipping {file_path} - already has header")
            return True
            
        filename = os.path.basename(file_path)
        purpose = get_file_purpose(filename)
        description = get_file_description(filename)
        
        # Create new header
        new_header = STANDARD_HEADER.format(
            path=file_path,
            filename=filename,
            purpose=purpose,
            description=description,
            created_date=datetime.now().strftime('%Y-%m-%d'),
            modified_date=datetime.now().strftime('%Y-%m-%d')
        )
        
        # Remove old shebang if exists
        if content.startswith('#!'):
            content = re.sub(r'^#!.*\n', '', content)
        
        # Remove old encoding if exists
        content = re.sub(r'^# -\*- coding:.*\n', '', content)
        
        # Remove old docstring if exists at start
        content = re.sub(r'^""".*?"""\n', '', content, flags=re.DOTALL)
        
        # Combine new header with content
        new_content = new_header + '\n\n' + content.lstrip()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"✅ Updated: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False

def find_python_files(root_dir: str) -> List[str]:
    """Find all Python files in the given directory."""
    python_files = []
    for path in Path(root_dir).rglob('*.py'):
        # Skip __pycache__ and backup files
        if '__pycache__' not in str(path) and not path.name.endswith('.backup'):
            python_files.append(str(path))
    return python_files

def main():
    """Main function to update all Python file headers."""
    print("🔄 Starting header update process...")
    
    # Find all Python files
    root_dir = 'autoprojectmanagement'
    python_files = find_python_files(root_dir)
    
    print(f"📊 Found {len(python_files)} Python files to process")
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for file_path in python_files:
        if update_file_header(file_path):
            updated_count += 1
        else:
            error_count += 1
    
    print("\n📈 Update Summary:")
    print(f"✅ Updated: {updated_count} files")
    print(f"⏭️  Skipped: {skipped_count} files")
    print(f"❌ Errors: {error_count} files")
    
    if error_count == 0:
        print("\n🎉 All headers updated successfully!")
    else:
        print("\n⚠️ Some files had errors. Check the output above.")

if __name__ == "__main__":
    main()
