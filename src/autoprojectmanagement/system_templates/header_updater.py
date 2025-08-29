#!/usr/bin/env python3
"""
path: autoprojectmanagement/templates/header_updater.py
File: header_updater.py
Purpose: Automatically apply standardized headers to all Python files in the AutoProjectManagement project
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: This script automatically applies standardized headers to all Python files
in the AutoProjectManagement codebase, ensuring consistent documentation and metadata.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

# Constants for better maintainability
SUPPORTED_FILE_EXTENSIONS = {'.py'}
SKIP_PATTERNS = [
    '__pycache__',
    '.git',
    'venv',
    'env',
    'node_modules',
    'header_updater.py',
    'standard_header.py'
]
HEADER_TEMPLATE_FILE = "standard_header.py"
CONFIG_FILE = "header_config.json"


class HeaderUpdater:
    """
    A class to manage and update standardized headers for Python files.
    
    This class provides functionality to automatically apply consistent headers
    to Python files across the AutoProjectManagement project.
    """
    
    def __init__(self, project_root: Optional[Path] = None) -> None:
        """Initialize the HeaderUpdater with project configuration."""
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.templates_dir = Path(__file__).parent
        self.header_template = self._load_template()
        
    def _load_template(self) -> str:
        """Load the standard header template from file."""
        template_path = self.templates_dir / HEADER_TEMPLATE_FILE
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return '"""Default header template"""'

    def _get_file_info(self, file_path: Path) -> Dict[str, str]:
        """Extract file information for template variables."""
        relative_path = file_path.relative_to(self.project_root)
        module_name = file_path.stem
        module_path = str(relative_path).replace('.py', '').replace('/', '.')
        
        return {
            'module_name': module_name,
            'filename': file_path.name,
            'relative_path': str(relative_path),
            'module_path': module_path,
            'current_date': datetime.now().strftime('%Y-%m-%d'),
            'developer_name': 'AutoProjectManagement Team',
            'description': f'{module_name.replace("_", " ").title()} module'
        }

    def _should_update_header(self, file_path: Path) -> bool:
        """Check if file should have header updated."""
        file_str = str(file_path)
        return not any(pattern in file_str for pattern in SKIP_PATTERNS)

    def _has_header(self, content: str) -> bool:
        """Check if file already has a header."""
        header_patterns = [
            r'""".*?AutoProjectManagement.*?"',
            r'""".*?File:.*?"',
            r'""".*?Author:.*?"'
        ]
        
        for pattern in header_patterns:
            if re.search(pattern, content, re.DOTALL):
                return True
        return False

    def _remove_existing_header(self, content: str) -> str:
        """Remove existing header if present."""
        if content.startswith('"""'):
            end = content.find('"""', 3)
            if end != -1:
                return content[end+3:].lstrip()
        return content

    def update_file(self, file_path: Path) -> bool:
        """Update header for a single file."""
        if not self._should_update_header(file_path):
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return False
        
        if self._has_header(content):
            return False
            
        content = self._remove_existing_header(content)
        
        # Generate new header
        info = self._get_file_info(file_path)
        new_header = self.header_template
        
        # Replace template variables
        for key, value in info.items():
            new_header = new_header.replace(f'{{{key}}}', str(value))
        
        new_content = new_header + '\n\n' + content.lstrip()
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        except Exception:
            return False
    
    def update_all_files(self, dry_run: bool = False) -> int:
        """Update headers for all Python files in the project."""
        python_files = list(self.project_root.rglob('*.py'))
        updated_count = 0
        
        for file_path in python_files:
            if file_path.name == 'header_updater.py':
                continue
                
            if self.update_file(file_path):
                if not dry_run:
                    print(f"✓ Updated: {file_path.relative_to(self.project_root)}")
                updated_count += 1
            elif dry_run:
                print(f"○ Skipped: {file_path.relative_to(self.project_root)}")
        
        print(f"\n{'Would update' if dry_run else 'Updated'} {updated_count} files")
        return updated_count

    def create_header_config(self) -> Dict[str, str]:
        """Create configuration file for header customization."""
        config = {
            "project_name": "AutoProjectManagement",
            "version": "2.0.0",
            "author": "AutoProjectManagement Team",
            "license": "MIT",
            "python_version": "3.8+"
        }
        
        config_path = self.templates_dir / CONFIG_FILE
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return config


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Update headers for AutoProjectManagement')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be updated')
    parser.add_argument('--file', help='Update specific file')
    
    args = parser.parse_args()
    
    updater = HeaderUpdater()
    
    if args.file:
        file_path = Path(args.file)
        if file_path.exists():
            if updater.update_file(file_path):
                print(f"✓ Updated: {file_path}")
            else:
                print(f"○ Skipped: {file_path}")
        else:
            print(f"✗ File not found: {args.file}")
    else:
        updater.update_all_files(dry_run=args.dry_run)
