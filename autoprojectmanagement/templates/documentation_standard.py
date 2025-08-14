#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/templates/documentation_standard.py
File: documentation_standard.py
Purpose: Documentation standards
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Documentation standards within the AutoProjectManagement system
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
CREATED_DATE = "2025-08-14"
MODIFIED_DATE = "2025-08-14"

# Module-level docstring
__doc__ = """
Documentation standards within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for better maintainability
DEFAULT_ENCODING = "utf-8"
DEFAULT_LINE_ENDINGS = "LF"
MAX_LINE_LENGTH = 79
DOCUMENTATION_VERSION = "2.0.0"
DEFAULT_LICENSE = "MIT License"
DEFAULT_LANGUAGE = "Persian/English"

# Document type constants
DOCUMENT_TYPE_README = "README"
DOCUMENT_TYPE_API = "API Documentation"
DOCUMENT_TYPE_USER_GUIDE = "User Guide"
DOCUMENT_TYPE_TECHNICAL_SPEC = "Technical Specification"

# Status constants
STATUS_ACTIVE = "Active"
STATUS_DRAFT = "Draft"
STATUS_DEPRECATED = "Deprecated"

# Priority constants
PRIORITY_HIGH = "High"
PRIORITY_MEDIUM = "Medium"
PRIORITY_LOW = "Low"


class DocumentationGenerator:
    """
    Generate standardized documentation for AutoProjectManagement and managed projects.
    
    This class provides comprehensive documentation generation capabilities
    with support for multiple document types, bilingual content, and
    consistent formatting across all project documentation.
    
    Attributes:
        project_name: Name of the project being documented
        project_root: Root directory of the project
        metadata: Dictionary containing project metadata
        templates: Dictionary of document templates
        
    Example:
        >>> generator = DocumentationGenerator("MyProject")
        >>> generator.setup_project_documentation("docs/")
    """
    
    def __init__(self, project_name: str, project_root: Optional[Path] = None) -> None:
        """
        Initialize the documentation generator.
        
        Args:
            project_name: Name of the project to document
            project_root: Root directory of the project (defaults to current directory)
            
        Raises:
            ValueError: If project_name is empty or invalid
        """
        if not project_name or not isinstance(project_name, str):
            raise ValueError("Project name must be a non-empty string")
            
        self.project_name: str = project_name
        self.project_root: Path = project_root or Path.cwd()
        self.metadata: Dict[str, str] = self._initialize_metadata()
        self.templates: Dict[str, str] = self._load_templates()
        
        logger.info(f"Initialized documentation generator for {project_name}")
    
    def _initialize_metadata(self) -> Dict[str, str]:
        """
        Initialize project metadata with default values.
        
        Returns:
            Dictionary containing all required metadata fields
        """
        current_date: str = datetime.now().strftime('%Y-%m-%d')
        next_review: str = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
        
        return {
            'PROJECT_NAME': self.project_name,
            'PROJECT_DESCRIPTION': f'Automated project management system for {self.project_name}',
            'AUTHOR_NAME': 'AutoProjectManagement Team',
            'TEAM_NAME': 'AutoProjectManagement Team',
            'CONTACT_EMAIL': 'team@autoprojectmanagement.com',
            'REPOSITORY_URL': 'https://github.com/autoprojectmanagement/autoprojectmanagement',
            'LICENSE_TYPE': DEFAULT_LICENSE,
            'COPYRIGHT_HOLDER': 'AutoProjectManagement Team',
            'YEAR': str(datetime.now().year),
            'DOC_VERSION': DOCUMENTATION_VERSION,
            'PROJECT_VERSION': '1.0.0',
            'CREATION_DATE': current_date,
            'LAST_UPDATED': current_date,
            'NEXT_REVIEW_DATE': next_review,
            'LANGUAGE': DEFAULT_LANGUAGE,
            'CLASSIFICATION': 'Public',
            'TARGET_AUDIENCE': 'Developers, Project Managers',
            'STATUS': STATUS_ACTIVE,
            'PRIORITY_LEVEL': PRIORITY_HIGH,
            'DOCUMENT_FORMAT': 'Markdown',
            'APM_VERSION': '2.0.0',
            'REQUIRED_TOOLS': 'AutoProjectManagement Package',
            'PREREQUISITES': 'Python 3.8+',
            'ENCODING': DEFAULT_ENCODING,
            'LINE_ENDINGS': DEFAULT_LINE_ENDINGS,
            'WORD_COUNT': '0',
            'READING_TIME': '0 min'
        }
    
    def _load_templates(self) -> Dict[str, str]:
        """
        Load all document templates.
        
        Returns:
            Dictionary mapping template names to their content
        """
        return {
            'README': self._get_readme_template(),
            'API': self._get_api_template(),
            'USER_GUIDE': self._get_user_guide_template(),
            'TECHNICAL_SPEC': self._get_technical_spec_template(),
            'HEADER': self._get_header_template(),
            'SECTIONS': self._get_sections_template()
        }
    
    def _get_header_template(self) -> str:
        """Get the standard header template."""
        return """
================================================================================
{PROJECT_NAME} - {PROJECT_DESCRIPTION}
================================================================================
Document: {DOCUMENT_TITLE}
Type: {DOCUMENT_TYPE}
Path: {RELATIVE_PATH}
Language: {LANGUAGE}

Description:
    {DESCRIPTION}

Author: {AUTHOR_NAME}
Team: {TEAM_NAME}
Contact: {CONTACT_EMAIL}
Repository: {REPOSITORY_URL}

Version Information:
    Document Version: {DOC_VERSION}
    Project Version: {PROJECT_VERSION}
    Last Updated: {LAST_UPDATED}
    Created: {CREATION_DATE}
    Review Date: {NEXT_REVIEW_DATE}

Document Metadata:
    Classification: {CLASSIFICATION}
    Audience: {TARGET_AUDIENCE}
    Status: {STATUS}
    Priority: {PRIORITY_LEVEL}

Technical Information:
    Format: {DOCUMENT_FORMAT}
    Encoding: {ENCODING}
    Line Endings: {LINE_ENDINGS}
    Word Count: {WORD_COUNT}
    Reading Time: {READING_TIME}

Dependencies:
    - AutoProjectManagement Package: {APM_VERSION}
    - Required Tools: {REQUIRED_TOOLS}
    - Prerequisites: {PREREQUISITES}

License: {LICENSE_TYPE}
Copyright: (c) {YEAR} {COPYRIGHT_HOLDER}

================================================================================
"""
    
    def _get_sections_template(self) -> str:
        """Get the sections template."""
        return """
================================================================================
فهرست مطالب / Table of Contents
================================================================================
{TOC_CONTENT}

================================================================================
خلاصه اجرایی / Executive Summary
================================================================================
{SUMMARY_CONTENT}

================================================================================
تاریخچه نسخه‌ها / Version History
================================================================================
{VERSION_TABLE}

================================================================================
مقدمه / Introduction
================================================================================
{INTRODUCTION_CONTENT}

================================================================================
محتوای اصلی / Main Content
================================================================================
{MAIN_CONTENT}

================================================================================
پیوست‌ها / Appendices
================================================================================
{APPENDICES_CONTENT}

================================================================================
پانویس / Footer
================================================================================
{FOOTER_CONTENT}
================================================================================
"""
    
    def _get_readme_template(self) -> str:
        """Get the README template."""
        return """
# {PROJECT_NAME}

## معرفی / Introduction
{PROJECT_DESCRIPTION}

## ویژگی‌ها / Features
- Automated project management
- Git integration
- Progress tracking
- Resource management
- Risk assessment
- Quality assurance

## نصب و راه‌اندازی / Installation
```bash
pip install autoprojectmanagement
```

## استفاده / Usage
```python
from autoprojectmanagement import AutoProjectManagement

project = AutoProjectManagement("MyProject")
project.setup()
```

## مستندات / Documentation
- [API Documentation](API_DOCUMENTATION.md)
- [User Guide](USER_GUIDE.md)
- [Technical Specification](TECHNICAL_SPECIFICATION.md)

## مشارکت / Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## مجوز / License
This project is licensed under the MIT License - see the LICENSE file for details.

## تماس / Contact
{CONTACT_EMAIL}
"""

    def _get_api_template(self) -> str:
        """Get the API documentation template."""
        return """
# API Documentation - {PROJECT_NAME}

## Authentication
All API endpoints require authentication using API keys passed in the Authorization header.

## Endpoints

### GET /api/projects
Retrieve all projects.

**Response:**
```json
{
    "projects": [...]
}
```

### POST /api/projects
Create a new project.

**Request:**
```json
{
    "name": "MyProject",
    "description": "Project description"
}
```

## نمونه کد / Code Examples
```python
import requests

response = requests.get(
    'https://api.autoprojectmanagement.com/projects',
    headers={'Authorization': 'Bearer YOUR_API_KEY'}
)
```

## خطاها / Error Handling
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## نرخ محدودیت / Rate Limiting
100 requests per minute per API key.
"""

    def _get_user_guide_template(self) -> str:
        """Get the user guide template."""
        return """
# User Guide - {PROJECT_NAME}

## پیش‌نیازها / Prerequisites
- Python 3.8 or higher
- Git installed
- Internet connection

## راهنمای گام به گام / Step-by-Step Guide
1. Install the package
2. Initialize your project
3. Configure settings
4. Start managing your project

## عیب‌یابی / Troubleshooting
### Common Issues
- **Import Error**: Ensure Python 3.8+ is installed
- **Permission Error**: Check file permissions
- **Network Error**: Verify internet connection

## پرسش‌های متداول / FAQ
**Q: What Python versions are supported?**
A: Python 3.8 and above.

**Q: Is there a web interface?**
A: Yes, available at http://localhost:8000

## پشتیبانی / Support
For support, email {CONTACT_EMAIL}
"""

    def _get_technical_spec_template(self) -> str:
        """Get the technical specification template."""
        return """
# Technical Specification - {PROJECT_NAME}

## معماری سیستم / System Architecture
The system follows a modular architecture with clear separation of concerns.

## اجزای سیستم / System Components
- **Core Engine**: Main project management logic
- **API Layer**: RESTful API endpoints
- **Database Layer**: SQLite/PostgreSQL support
- **UI Layer**: Web interface and CLI

## جریان داده / Data Flow
1. User input → API → Core Engine → Database
2. Database → Core Engine → API → User output

## امنیت / Security
- API key authentication
- Input validation
- SQL injection prevention
- XSS protection

## عملکرد / Performance
- Response time < 100ms for simple queries
- Support for 1000+ concurrent users
- Efficient database indexing

## مقیاس‌پذیری / Scalability
- Horizontal scaling support
- Database sharding
- Caching layer
- Load balancing
"""

    def generate_documentation_header(
        self, 
        document_type: str, 
        document_path: str,
        custom_metadata: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Generate standardized header for any document.
        
        Args:
            document_type: Type of document being created
            document_path: Path to the document
            custom_metadata: Optional custom metadata to override defaults
            
        Returns:
            Formatted header string
            
        Raises:
            ValueError: If document_type or document_path is invalid
        """
        if not document_type or not isinstance(document_type, str):
            raise ValueError("Document type must be a non-empty string")
            
        if not document_path or not isinstance(document_path, str):
            raise ValueError("Document path must be a non-empty string")
        
        # Merge custom metadata if provided
        metadata = self.metadata.copy()
        if custom_metadata:
            metadata.update(custom_metadata)
        
        # Update document-specific metadata
        metadata.update({
            'DOCUMENT_TITLE': f'{document_type} Documentation',
            'DOCUMENT_TYPE': document_type,
            'RELATIVE_PATH': str(document_path),
            'DESCRIPTION': f'{document_type} documentation for {self.project_name}'
        })
        
        header = self.templates['HEADER']
        for key, value in metadata.items():
            header = header.replace(f'{{{key}}}', str(value))
        
        return header
    
    def create_readme(self, target_path: Path) -> None:
        """
        Create README.md with standard format.
        
        Args:
            target_path: Directory where README.md should be created
            
        Raises:
            OSError: If file cannot be written
            ValueError: If target_path is invalid
        """
        if not isinstance(target_path, Path):
            raise ValueError("target_path must be a Path object")
            
        try:
            content = self.templates['README'].format(**self.metadata)
            readme_path = target_path / 'README.md'
            
            with open(readme_path, 'w', encoding=DEFAULT_ENCODING) as f:
                f.write(content)
                
            logger.info(f"Created README.md at {readme_path}")
            
        except OSError as e:
            logger.error(f"Failed to create README.md: {e}")
            raise
    
    def create_api_docs(self, target_path: Path) -> None:
        """
        Create API documentation with standard format.
        
        Args:
            target_path: Directory where API documentation should be created
            
        Raises:
            OSError: If file cannot be written
            ValueError: If target_path is invalid
        """
        if not isinstance(target_path, Path):
            raise ValueError("target_path must be a Path object")
            
        try:
            content = self.templates['API'].format(**self.metadata)
            api_path = target_path / 'API_DOCUMENTATION.md'
            
            with open(api_path, 'w', encoding=DEFAULT_ENCODING) as f:
                f.write(content)
                
            logger.info(f"Created API_DOCUMENTATION.md at {api_path}")
            
        except OSError as e:
            logger.error(f"Failed to create API documentation: {e}")
            raise
    
    def create_user_guide(self, target_path: Path) -> None:
        """
        Create user guide with standard format.
        
        Args:
            target_path: Directory where user guide should be created
            
        Raises:
            OSError: If file cannot be written
            ValueError: If target_path is invalid
        """
        if not isinstance(target_path, Path):
            raise ValueError("target_path must be a Path object")
            
        try:
            content = self.templates['USER_GUIDE'].format(**self.metadata)
            guide_path = target_path / 'USER_GUIDE.md'
            
            with open(guide_path, 'w', encoding=DEFAULT_ENCODING) as f:
                f.write(content)
                
            logger.info(f"Created USER_GUIDE.md at {guide_path}")
            
        except OSError as e:
            logger.error(f"Failed to create user guide: {e}")
            raise
    
    def create_technical_spec(self, target_path: Path) -> None:
        """
        Create technical specification with standard format.
        
        Args:
            target_path: Directory where technical specification should be created
            
        Raises:
            OSError: If file cannot be written
            ValueError: If target_path is invalid
        """
        if not isinstance(target_path, Path):
            raise ValueError("target_path must be a Path object")
            
        try:
            content = self.templates['TECHNICAL_SPEC'].format(**self.metadata)
            spec_path = target_path / 'TECHNICAL_SPECIFICATION.md'
            
            with open(spec_path, 'w', encoding=DEFAULT_ENCODING) as f:
                f.write(content)
                
            logger.info(f"Created TECHNICAL_SPECIFICATION.md at {spec_path}")
            
        except OSError as e:
            logger.error(f"Failed to create technical specification: {e}")
            raise
    
    def setup_project_documentation(self, target_path: Union[str, Path]) -> None:
        """
        Setup complete documentation structure for a project.
        
        This method creates all standard documentation files including:
        - README.md
        - API_DOCUMENTATION.md
        - USER_GUIDE.md
        - TECHNICAL_SPECIFICATION.md
        - DOCUMENTATION_INDEX.md
        
        Args:
            target_path: Directory where documentation should be created
            
        Raises:
            OSError: If directory cannot be created or files cannot be written
            ValueError: If target_path is invalid
        """
        if isinstance(target_path, str):
            target_path = Path(target_path)
            
        if not isinstance(target_path, Path):
            raise ValueError("target_path must be a string or Path object")
        
        try:
            # Create directory structure
            target_path.mkdir(parents=True, exist_ok=True)
            
            # Create all standard documentation files
            self.create_readme(target_path)
            self.create_api_docs(target_path)
            self.create_user_guide(target_path)
            self.create_technical_spec(target_path)
            
            # Create documentation index
            self._create_documentation_index(target_path)
            
            logger.info(f"Complete documentation structure created at {target_path}")
            
        except OSError as e:
            logger.error(f"Failed to setup project documentation: {e}")
            raise
    
    def _create_documentation_index(self, target_path: Path) -> None:
        """
        Create documentation index file.
        
        Args:
            target_path: Directory where index should be created
            
        Raises:
            OSError: If file cannot be written
        """
        index_content = f"""
# Documentation Index - {self.project_name}

## Available Documentation:
1. [README.md](README.md) - Project overview and quick start
2. [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference and examples
3. [USER_GUIDE.md](USER_GUIDE.md) - Comprehensive user guide
4. [TECHNICAL_SPECIFICATION.md](TECHNICAL_SPECIFICATION.md) - Technical specifications

## Documentation Standards:
All documents follow AutoProjectManagement documentation standards
with bilingual (Persian/English) support and consistent formatting.

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        index_path = target_path / 'DOCUMENTATION_INDEX.md'
        with open(index_path, 'w', encoding=DEFAULT_ENCODING) as f:
            f.write(index_content)
    
    def validate_documentation(self, target_path: Path) -> List[str]:
        """
        Validate created documentation for completeness.
        
        Args:
            target_path: Directory containing documentation
            
        Returns:
            List of validation issues found (empty if valid)
        """
        issues: List[str] = []
        required_files = [
            'README.md',
            'API_DOCUMENTATION.md',
            'USER_GUIDE.md',
            'TECHNICAL_SPECIFICATION.md',
            'DOCUMENTATION_INDEX.md'
        ]
        
        for file_name in required_files:
            file_path = target_path / file_name
            if not file_path.exists():
                issues.append(f"Missing required file: {file_name}")
            elif file_path.stat().st_size == 0:
                issues.append(f"Empty file: {file_name}")
        
        return issues


# ================================================================================
# UTILITY FUNCTIONS
# ================================================================================

def validate_project_name(name: str) -> bool:
    """
    Validate project name for documentation purposes.
    
    Args:
        name: Project name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    
    # Check for invalid characters
    invalid_chars = r'[<>:\"/\\|?*]'
    return not bool(re.search(invalid_chars, name))


def get_reading_time(word_count: int) -> str:
    """
    Calculate estimated reading time based on word count.
    
    Args:
        word_count: Number of words in document
        
    Returns:
        Estimated reading time as string
    """
    if word_count <= 0:
        return "0 min"
    
    # Average reading speed: 200 words per minute
    minutes = max(1, word_count // 200)
    return f"{minutes} min"


# ================================================================================
# USAGE EXAMPLES AND TESTING
# ================================================================================

def main() -> None:
    """
    Demonstrate usage of the DocumentationGenerator class.
    
    This function provides examples of how to use the documentation
    generator for different types of projects.
    """
    try:
        # Example 1: AutoProjectManagement itself
        logger.info("Creating documentation for AutoProjectManagement...")
        apm_docs = DocumentationGenerator("AutoProjectManagement")
        apm_docs.setup_project_documentation("Docs")
        
        # Validate the created documentation
        issues = apm_docs.validate_documentation(Path("Docs"))
        if issues:
            logger.warning(f"Validation issues found: {issues}")
        else:
            logger.info("Documentation validation passed")
        
        # Example 2: A managed project
        logger.info("Creating documentation for managed project...")
        project_docs = DocumentationGenerator("MyManagedProject")
        project_docs.setup_project_documentation("MyManagedProject/Docs")
        
        # Example 3: Custom metadata
        custom_metadata = {
            'PROJECT_DESCRIPTION': 'Custom project with special requirements',
            'AUTHOR_NAME': 'Custom Team',
            'CONTACT_EMAIL': 'custom@example.com'
        }
        
        custom_docs = DocumentationGenerator("CustomProject")
        header = custom_docs.generate_documentation_header(
            "README", 
            "docs/README.md",
            custom_metadata
        )
        
        logger.info("Documentation templates created successfully!")
        logger.info(f"Sample header length: {len(header)} characters")
        
    except Exception as e:
        logger.error(f"Error in documentation generation: {e}")
        raise


if __name__ == "__main__":
    main()
