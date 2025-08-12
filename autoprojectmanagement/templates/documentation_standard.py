"""
================================================================================
AutoProjectManagement - Documentation Standards
================================================================================
Template: Documentation Header for All Documents
File: documentation_standard.py
Path: autoprojectmanagement/templates/documentation_standard.py

Description:
    Standardized header format for all documentation files (README, API docs,
    user guides, technical specifications, etc.) within AutoProjectManagement
    and all projects managed by this package.

Author: AutoProjectManagement Team
Contact: team@autoprojectmanagement.com
Repository: https://github.com/autoprojectmanagement/autoprojectmanagement

Version Information:
    Current Version: 1.0.0
    Last Updated: 2024-01-15
    Document Type: Documentation Template
    
Development Status:
    Status: Production/Stable
    Created: 2024-01-15
    Last Modified: 2024-01-15
    Modified By: AutoProjectManagement Team

Document Classification:
    Type: Template/Standard
    Audience: Developers, Project Managers, Documentation Writers
    Language: English

License: MIT License
Copyright: (c) 2024 AutoProjectManagement Team
================================================================================
"""

# ================================================================================
# DOCUMENTATION HEADER TEMPLATE
# ================================================================================
DOCUMENTATION_HEADER = """
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
    Encoding: UTF-8
    Line Endings: LF
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

# ================================================================================
# DOCUMENTATION SECTIONS TEMPLATE
# ================================================================================

SECTIONS_TEMPLATE = {
    "header": """
================================================================================
{PROJECT_NAME}
================================================================================
""",
    
    "table_of_contents": """
================================================================================
فهرست مطالب / Table of Contents
================================================================================
{TOC_CONTENT}
""",
    
    "executive_summary": """
================================================================================
خلاصه اجرایی / Executive Summary
================================================================================
{SUMMARY_CONTENT}
""",
    
    "version_history": """
================================================================================
تاریخچه نسخه‌ها / Version History
================================================================================
{VERSION_TABLE}
""",
    
    "introduction": """
================================================================================
مقدمه / Introduction
================================================================================
{INTRODUCTION_CONTENT}
""",
    
    "main_content": """
================================================================================
محتوای اصلی / Main Content
================================================================================
{MAIN_CONTENT}
""",
    
    "appendices": """
================================================================================
پیوست‌ها / Appendices
================================================================================
{APPENDICES_CONTENT}
""",
    
    "footer": """
================================================================================
پانویس / Footer
================================================================================
{FOOTER_CONTENT}
================================================================================
"""
}

# ================================================================================
# DOCUMENTATION TYPES SPECIFIC TEMPLATES
# ================================================================================

README_TEMPLATE = """
================================================================================
README - {PROJECT_NAME}
================================================================================
# {PROJECT_NAME}

## معرفی / Introduction
{PROJECT_DESCRIPTION}

## ویژگی‌ها / Features
{FEATURES_LIST}

## نصب و راه‌اندازی / Installation
{INSTALLATION_GUIDE}

## استفاده / Usage
{USAGE_EXAMPLES}

## مستندات / Documentation
{DOCUMENTATION_LINKS}

## مشارکت / Contributing
{CONTRIBUTING_GUIDE}

## مجوز / License
{LICENSE_INFORMATION}

## تماس / Contact
{CONTACT_INFORMATION}
================================================================================
"""

API_DOCUMENTATION_TEMPLATE = """
================================================================================
API Documentation - {PROJECT_NAME}
================================================================================
# API Reference

## Authentication
{AUTH_INFO}

## Endpoints
{ENDPOINTS_LIST}

## نمونه کد / Code Examples
{CODE_EXAMPLES}

## خطاها / Error Handling
{ERROR_HANDLING}

## نرخ محدودیت / Rate Limiting
{RATE_LIMITS}
================================================================================
"""

USER_GUIDE_TEMPLATE = """
================================================================================
User Guide - {PROJECT_NAME}
================================================================================
# راهنمای کاربر

## پیش‌نیازها / Prerequisites
{PREREQUISITES}

## راهنمای گام به گام / Step-by-Step Guide
{STEP_BY_STEP}

## عیب‌یابی / Troubleshooting
{TROUBLESHOOTING}

## پرسش‌های متداول / FAQ
{FAQ_SECTION}

## پشتیبانی / Support
{SUPPORT_INFO}
================================================================================
"""

TECHNICAL_SPECIFICATION_TEMPLATE = """
================================================================================
Technical Specification - {PROJECT_NAME}
================================================================================
# مشخصات فنی

## معماری سیستم / System Architecture
{ARCHITECTURE}

## اجزای سیستم / System Components
{COMPONENTS}

## جریان داده / Data Flow
{DATA_FLOW}

## امنیت / Security
{SECURITY_SPEC}

## عملکرد / Performance
{PERFORMANCE_SPEC}

## مقیاس‌پذیری / Scalability
{SCALABILITY_SPEC}
================================================================================
"""

# ================================================================================
# DOCUMENTATION GENERATOR CLASS
# ================================================================================

class DocumentationGenerator:
    """Generate standardized documentation for AutoProjectManagement and managed projects"""
    
    def __init__(self, project_name, project_root=None):
        self.project_name = project_name
        self.project_root = project_root or Path.cwd()
        self.metadata = {
            'PROJECT_NAME': project_name,
            'PROJECT_DESCRIPTION': f'Automated project management system for {project_name}',
            'AUTHOR_NAME': 'AutoProjectManagement Team',
            'TEAM_NAME': 'AutoProjectManagement Team',
            'CONTACT_EMAIL': 'team@autoprojectmanagement.com',
            'REPOSITORY_URL': 'https://github.com/autoprojectmanagement/autoprojectmanagement',
            'LICENSE_TYPE': 'MIT License',
            'COPYRIGHT_HOLDER': 'AutoProjectManagement Team',
            'YEAR': str(datetime.now().year),
            'DOC_VERSION': '1.0.0',
            'PROJECT_VERSION': '1.0.0',
            'CREATION_DATE': datetime.now().strftime('%Y-%m-%d'),
            'LAST_UPDATED': datetime.now().strftime('%Y-%m-%d'),
            'NEXT_REVIEW_DATE': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
            'LANGUAGE': 'Persian/English',
            'CLASSIFICATION': 'Public',
            'TARGET_AUDIENCE': 'Developers, Project Managers',
            'STATUS': 'Active',
            'PRIORITY_LEVEL': 'High',
            'DOCUMENT_FORMAT': 'Markdown',
            'APM_VERSION': '1.0.0',
            'REQUIRED_TOOLS': 'AutoProjectManagement Package',
            'PREREQUISITES': 'Python 3.8+'
        }
    
    def generate_documentation_header(self, document_type, document_path):
        """Generate standardized header for any document"""
        metadata = self.metadata.copy()
        metadata.update({
            'DOCUMENT_TITLE': f'{document_type} Documentation',
            'DOCUMENT_TYPE': document_type,
            'RELATIVE_PATH': str(document_path),
            'DESCRIPTION': f'{document_type} documentation for {self.project_name}'
        })
        
        header = DOCUMENTATION_HEADER
        for key, value in metadata.items():
            header = header.replace(f'{{{key}}}', str(value))
        
        return header
    
    def create_readme(self, target_path):
        """Create README.md with standard format"""
        content = README_TEMPLATE.format(**self.metadata)
        with open(target_path / 'README.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def create_api_docs(self, target_path):
        """Create API documentation with standard format"""
        content = API_DOCUMENTATION_TEMPLATE.format(**self.metadata)
        with open(target_path / 'API_DOCUMENTATION.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def create_user_guide(self, target_path):
        """Create user guide with standard format"""
        content = USER_GUIDE_TEMPLATE.format(**self.metadata)
        with open(target_path / 'USER_GUIDE.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def create_technical_spec(self, target_path):
        """Create technical specification with standard format"""
        content = TECHNICAL_SPECIFICATION_TEMPLATE.format(**self.metadata)
        with open(target_path / 'TECHNICAL_SPECIFICATION.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def setup_project_documentation(self, target_path):
        """Setup complete documentation structure for a project"""
        target_path = Path(target_path)
        target_path.mkdir(parents=True, exist_ok=True)
        
        # Create all standard documentation
        self.create_readme(target_path)
        self.create_api_docs(target_path)
        self.create_user_guide(target_path)
        self.create_technical_spec(target_path)
        
        # Create documentation index
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
"""
        
        with open(target_path / 'DOCUMENTATION_INDEX.md', 'w', encoding='utf-8') as f:
            f.write(index_content)

# ================================================================================
# USAGE EXAMPLES
# ================================================================================

if __name__ == "__main__":
    # Example usage for AutoProjectManagement itself
    apm_docs = DocumentationGenerator("AutoProjectManagement")
    apm_docs.setup_project_documentation("Docs")
    
    # Example usage for a managed project
    project_docs = DocumentationGenerator("MyManagedProject")
    project_docs.setup_project_documentation("MyManagedProject/Docs")
    
    print("Documentation templates created successfully!")
