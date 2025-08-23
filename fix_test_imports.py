#!/usr/bin/env python3
"""
Script to fix import statements in test files by replacing backslashes with forward slashes.
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix import statements in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace backslashes with forward slashes in import statements
        fixed_content = re.sub(
            r'from autoprojectmanagement\\', 
            'from autoprojectmanagement.', 
            content
        )
        
        if content != fixed_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Fixed imports in: {file_path}")
            return True
        else:
            print(f"No changes needed in: {file_path}")
            return False
            
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
