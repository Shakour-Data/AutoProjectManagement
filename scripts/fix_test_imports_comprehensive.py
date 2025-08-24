#!/usr/bin/env python3
"""
Comprehensive script to fix import statements in test files by updating them to use the correct subdirectory paths.
"""

import os
import re
from pathlib import Path

# Mapping of module names to their subdirectory paths
MODULE_TO_SUBDIRECTORY = {
    'check_progress_dashboard_update': 'progress_reporting',
    'commit_progress_manager': 'quality_commit_management',
    'communication_management': 'communication_risk',
    'communication_risk_doc_integration': 'communication_risk',
    'dashboards_reports': 'progress_reporting',
    'db_data_collector': 'data_collection_processing',
    'do_important_tasks': 'task_workflow_management',
    'do_urgent_tasks': 'task_workflow_management',
    'estimation_management': 'planning_estimation',
    'feature_weights': 'utility_modules',
    'gantt_chart_data': 'planning_estimation',
    'git_progress_updater': 'quality_commit_management',
    'github_actions_automation': 'quality_commit_management',
    'importance_urgency_calculator': 'task_workflow_management',
    'importance_urgency_calculator_refactored': 'task_workflow_management',
    'input_handler': 'data_collection_processing',
    'progress_calculator': 'progress_reporting',
    'progress_calculator_refactored': 'progress_reporting',
    'progress_data_generator': 'data_collection_processing',
    'progress_data_generator_refactored': 'data_collection_processing',
    'progress_report': 'progress_reporting',
    'project_management_system': 'project_management',
    'project_views_generator': 'utility_modules',
    'quality_management': 'quality_commit_management',
    'reporting': 'progress_reporting',
    'resource_allocation_manager': 'resource_management',
    'resource_leveling': 'resource_management',
    'resource_management': 'resource_management',
    'risk_management': 'communication_risk',
    'scheduler': 'planning_estimation',
    'scope_management': 'planning_estimation',
    'setup_automation': 'utility_modules',
    'setup_initialization': 'utility_modules',
    'task_executor': '极workflow_management',
    'task_management': 'task_workflow_management',
    'task_management_integration': 'task_workflow_management',
    'time_management': 'utility_modules',
    'wbs_aggregator': 'planning_estimation',
    'wbs_merger': 'planning_estimation',
    'wbs_parser': 'planning_estimation',
    'workflow_data_collector': 'data_collection_processing',
}

def fix_imports_in_file(file_path):
    """Fix import statements in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix backslashes first
        content = re.sub(
            r'from autoprojectmanagement\\', 
            'from autoprojectmanagement.', 
            content
        )
        
        # Fix incorrect import paths
        for module_name, subdirectory in MODULE_TO_SUBDIRECTORY.items():
            pattern = f'from autoprojectmanagement\\.main_modules import {module_name}'
            replacement = f'from autoprojectmanagement.main_modules.{subdirectory} import {module_name}'
            content = re.sub(pattern, replacement, content)
            
            pattern = f'from autoprojectmanagement\\.main_modules\\.{module_name} import'
            replacement = f'from autoprojectmanagement.main_modules.{subdirectory}.{module_name} import'
            content = re.sub(pattern, replacement, content)
        
        # Fix project_management.modules imports
        content = re.sub(
            r'from project_management\.modules\.main_modules\.',
            'from autoprojectmanagement.main_modules.',
            content
        )
        
        content = re.sub(
            r'from project_management\.modules\.main_modules import',
            'from autoprojectmanagement.main_modules import',
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed imports in: {file_path}")
        return True
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix imports in all test files"""
    test_dir = Path("tests/code_tests/01_UnitTests")
    
    if not test_dir.exists():
        print(f"Test directory not found: {test_dir}")
        return
    
    # Find all Python files in the test directory
    python_files = list(test_dir.rglob("*.py"))
    
    print(f"Found {len(python_files)} Python files to check")
    
    fixed_count = 0
    for file_path in python_files:
        if fix_imports_in_file(file_path):
            fixed_count += 1
    
    print(f"\nFixed imports in {fixed_count} files")

if __name__ == "__main__":
    main()
