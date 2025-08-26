# AutoProjectManagement Code Header Standards

## Overview
This directory contains standardized header templates and tools for maintaining consistent code documentation across all Python files in the AutoProjectManagement package.

## Files Included
- `standard_header.py` - Template for new Python files
- `header_updater.py` - Script to automatically update headers
- `header_config.json` - Configuration for header customization

## Usage Instructions

### 1. For New Files
Copy the header from `standard_header.py` and customize the variables:
- Replace `{module_name}` with actual module name
- Replace `{filename}` with actual filename
- Replace `{description}` with brief description

### 2. For Existing Files
Run the header updater script:

```bash
# Update all files
python autoprojectmanagement/templates/header_updater.py

# Dry run (see what would be updated)
python autoprojectmanagement/templates/header_updater.py --dry-run

# Update specific file
python autoprojectmanagement/templates/header_updater.py --file path/to/file.py
```

### 3. Header Format Structure
Each file should include:
- **Project Information**: Name, description, team
- **File Details**: Path, description, author
- **Version Control**: Version, dates, changes
- **Technical Info**: Python version, dependencies
- **Usage**: Examples and notes
- **Changelog**: Version history
- **TODO**: Future improvements

## Template Variables
The following variables are automatically replaced:
- `{module_name}` - Module name (e.g., "project_management")
- `{filename}` - File name (e.g., "project_manager.py")
- `{relative_path}` - Relative path from project root
- `{current_date}` - Current date (YYYY-MM-DD)
- `{description}` - File description
- `{developer_name}` - Developer/team name

## Integration with Development Workflow
1. **Pre-commit hooks**: Add header validation
2. **IDE templates**: Configure templates in your IDE
3. **CI/CD**: Include header checks in build process

## Example Header
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: project_management
File: project_manager.py
Path: autoprojectmanagement/main_modules/project_management.py

Description:
    Core project management functionality for handling projects, tasks, and workflows

Author: AutoProjectManagement Team
Contact: team@autoprojectmanagement.com
Repository: https://github.com/autoprojectmanagement/autoprojectmanagement

Version Information:
    Current Version: 1.0.0
    Last Updated: 2024-01-15
    Python Version: 3.8+
    
Development Status:
    Status: Production/Stable
    Created: 2024-01-01
    Last Modified: 2024-01-15
    Modified By: AutoProjectManagement Team

Dependencies:
    - Python 3.8+
    - See requirements.txt for full dependency list

License: MIT License
Copyright: (c) 2024 AutoProjectManagement Team
================================================================================
"""
```

## Best Practices
1. **Keep headers updated** when making significant changes
2. **Use consistent formatting** across all files
3. **Include relevant TODO items** for future work
4. **Document breaking changes** in changelog
5. **Maintain version history** for tracking

## Troubleshooting
- **Encoding issues**: Ensure UTF-8 encoding
- **Template variables**: Check all variables are properly replaced
- **File permissions**: Ensure write access to target files
