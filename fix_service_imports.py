#!/usr/bin/env python3
"""
Script to fix service import statements in module files
"""

import os
import re
from pathlib import Path

def fix_service_imports_in_file(file_path):
    """Fix service import statements in a single module file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix github_integration imports
        content = re.sub(
            r'from autoprojectmanagement\.services\.github_integration import',
            'from autoprojectmanagement.services.integration_services.github_integration import',
            content
        )
        
        content = re.sub(
            r'import autoprojectmanagement\.services\.github_integration',
            'import autoprojectmanagement.services.integration_services.github_integration',
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed service imports in: {file_path}")
        return True
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix service imports in all module files"""
    modules_dir = Path("autoprojectmanagement/main_modules")
    
    if not modules_dir.exists():
        print(f"Modules directory not found: {modules_dir}")
        return
    
    # Find all Python files in the modules directory
    python_files = list(modules_dir.rglob("*.py"))
    
    print(f"Found {len(python_files)} Python files to check")
    
    fixed_count = 0
    for file_path in python_files:
        if fix_service_imports_in_file(file_path):
            fixed_count += 1
    
    print(f"\nFixed service imports in {fixed_count} module files")

if __name__ == "__main__":
    main()
