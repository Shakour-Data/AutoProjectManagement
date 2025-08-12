#!/usr/bin/env python3
"""
Header Updater Script for AutoProjectManagement
Automatically applies standardized headers to all Python files
"""

import os
import re
from datetime import datetime
from pathlib import Path

class HeaderUpdater:
    def __init__(self, project_root=None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.templates_dir = Path(__file__).parent
        self.header_template = self._load_template()
        
    def _load_template(self):
        """Load the standard header template"""
        template_path = self.templates_dir / "standard_header.py"
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _get_file_info(self, file_path):
        """Extract file information for template variables"""
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
            'change_description': 'Updated header format',
            'main_class': module_name.title().replace('_', ''),
            'description': f'{module_name.replace("_", " ").title()} module for AutoProjectManagement'
        }
    
    def _should_update_header(self, file_path):
        """Check if file should have header updated"""
        # Skip certain files
        skip_patterns = [
            '__pycache__',
            '.git',
            'venv',
            'env',
            'node_modules',
            'header_updater.py',
            'standard_header.py'
        ]
        
        file_str = str(file_path)
        return not any(pattern in file_str for pattern in skip_patterns)
    
    def _has_header(self, content):
        """Check if file already has a header"""
        header_patterns = [
            r'""".*?AutoProjectManagement.*?"',
            r'""".*?File:.*?"',
            r'""".*?Author:.*?"',
            r'""".*?Version:.*?"'
        ]
        
        for pattern in header_patterns:
            if re.search(pattern, content, re.DOTALL):
                return True
        return False
    
    def _remove_existing_header(self, content):
        """Remove existing header if present"""
        # Remove docstring at the beginning
        if content.startswith('"""'):
            end = content.find('"""', 3)
            if end != -1:
                return content[end+3:].lstrip()
        
        # Remove single quotes docstring
        if content.startswith("'''"):
            end = content.find("'''", 3)
            if end != -1:
                return content[end+3:].lstrip()
                
        return content
    
    def _generate_header(self, file_path):
        """Generate header for specific file"""
        info = self._get_file_info(file_path)
        header = self.header_template
        
        # Replace template variables
        for key, value in info.items():
            header = header.replace(f'{{{key}}}', str(value))
        
        return header
    
    def update_file(self, file_path):
        """Update header for a single file"""
        if not self._should_update_header(file_path):
            return False
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has header
        if self._has_header(content):
            return False
            
        # Remove existing header
        content = self._remove_existing_header(content)
        
        # Generate new header
        new_header = self._generate_header(file_path)
        
        # Combine header with content
        new_content = new_header + '\n\n' + content.lstrip()
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        return True
    
    def update_all_files(self, dry_run=False):
        """Update headers for all Python files in the project"""
        python_files = list(self.project_root.rglob('*.py'))
        updated_count = 0
        
        print(f"Found {len(python_files)} Python files")
        
        for file_path in python_files:
            if file_path.name == 'header_updater.py':
                continue
                
            if self.update_file(file_path):
                if not dry_run:
                    print(f"✓ Updated: {file_path.relative_to(self.project_root)}")
                updated_count += 1
            else:
                if dry_run:
                    print(f"○ Skipped: {file_path.relative_to(self.project_root)}")
        
        print(f"\n{'Would update' if dry_run else 'Updated'} {updated_count} files")
        return updated_count
    
    def create_header_config(self):
        """Create configuration file for header customization"""
        config = {
            "project_name": "AutoProjectManagement",
            "version": "1.0.0",
            "author": "AutoProjectManagement Team",
            "email": "team@autoprojectmanagement.com",
            "license": "MIT",
            "python_version": "3.8+",
            "include_git_info": True,
            "include_changelog": True,
            "include_todo": True
        }
        
        config_path = self.templates_dir / "header_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            import json
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return config

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Update headers for AutoProjectManagement')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be updated without making changes')
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
