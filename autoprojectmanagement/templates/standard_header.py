#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/templates/standard_header.py
File: standard_header.py
Purpose: Standardized header template for AutoProjectManagement modules
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Provides a consistent header format for all Python modules in the
AutoProjectManagement system, ensuring uniform documentation and metadata
standards across the entire codebase.
"""

import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
import logging

# Constants for the module
MODULE_NAME = "standard_header"
CURRENT_VERSION = "2.0.0"
PYTHON_MIN_VERSION = (3, 8)
DEFAULT_ENCODING = "utf-8"
MAX_LINE_LENGTH = 79

# Configure logging for the module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StandardHeader:
    """
    Manages standardized headers for AutoProjectManagement modules.
    
    This class provides a template system for consistent documentation
    across all Python files in the project, ensuring compliance with
    coding standards and best practices.
    
    Attributes:
        module_name (str): Name of the current module
        file_path (str): Full path to the current file
        metadata (Dict[str, Any]): Dictionary containing header metadata
        
    Example:
        >>> header = StandardHeader("my_module", "/path/to/file.py")
        >>> header.generate_header()
        >>> print(header.get_metadata())
    """
    
    def __init__(self, module_name: str, file_path: str) -> None:
        """
        Initialize the StandardHeader with module information.
        
        Args:
            module_name (str): Name of the module
            file_path (str): Full path to the file
            
        Raises:
            ValueError: If module_name or file_path is empty
        """
        if not module_name or not module_name.strip():
            raise ValueError("Module name cannot be empty")
        if not file_path or not file_path.strip():
            raise ValueError("File path cannot be empty")
            
        self.module_name = module_name.strip()
        self.file_path = file_path.strip()
        self.metadata = self._initialize_metadata()
        
    def _initialize_metadata(self) -> Dict[str, Any]:
        """Initialize the metadata dictionary with default values."""
        return {
            'path': self.file_path,
            'file': os.path.basename(self.file_path),
            'purpose': 'Auto-generated module',
            'author': 'AutoProjectManagement Team',
            'version': CURRENT_VERSION,
            'license': 'MIT',
            'description': 'Module description to be updated',
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat(),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}+"
        }
    
    def generate_header(self, 
                     purpose: str = "",
                     author: str = "AutoProjectManagement Team",
                     version: str = CURRENT_VERSION,
                     license_type: str = "MIT",
                     description: str = "") -> str:
        """
        Generate a standardized header string for a Python module.
        
        Args:
            purpose (str): The purpose of the module
            author (str): Author name
            version (str): Version number
            license_type (str): License type
            description (str): Detailed description
            
        Returns:
            str: Formatted header string ready to be inserted into a Python file
            
        Example:
            >>> header = StandardHeader("test_module", "/test/path.py")
            >>> result = header.generate_header(
            ...     purpose="Testing module",
            ...     description="A test module for demonstration"
            ... )
            >>> assert "Testing module" in result
        """
        try:
            # Update metadata with provided values
            self.metadata.update({
                'purpose': purpose or self.metadata['purpose'],
                'author': author,
                'version': version,
                'license': license_type,
                'description': description or self.metadata['description'],
                'modified': datetime.now().isoformat()
            })
            
            header_template = self._build_header_template()
            return header_template
            
        except Exception as e:
            logger.error(f"Error generating header: {str(e)}")
            raise RuntimeError(f"Failed to generate header: {str(e)}")
    
    def _build_header_template(self) -> str:
        """Build the actual header template string."""
        metadata = self.metadata
        
        header = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: {metadata['path']}
File: {metadata['file']}
Purpose: {metadata['purpose']}
Author: {metadata['author']}
Version: {metadata['version']}
License: {metadata['license']}
Description: {metadata['description']}
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
CURRENT_VERSION = "{metadata['version']}"
PYTHON_MIN_VERSION = "3.8+"
CREATED_DATE = "{metadata['created']}"
MODIFIED_DATE = "{metadata['modified']}"

# Module-level docstring
__doc__ = """
{metadata['description']}

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "{metadata['author']}"
__license__ = "{metadata['license']}"
'''
        return header
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get the current metadata dictionary.
        
        Returns:
            Dict[str, Any]: Complete metadata for the header
            
        Example:
            >>> header = StandardHeader("test", "/test.py")
            >>> metadata = header.get_metadata()
            >>> assert 'path' in metadata
            >>> assert 'file' in metadata
        """
        return self.metadata.copy()
    
    def update_metadata(self, **kwargs) -> None:
        """
        Update specific metadata fields.
        
        Args:
            **kwargs: Key-value pairs to update in metadata
            
        Example:
            >>> header = StandardHeader("test", "/test.py")
            >>> header.update_metadata(version="2.1.0", author="New Author")
            >>> assert header.metadata['version'] == "2.1.0"
        """
        valid_keys = {'purpose', 'author', 'version', 'license', 'description'}
        
        for key, value in kwargs.items():
            if key in valid_keys:
                self.metadata[key] = value
            else:
                logger.warning(f"Ignoring invalid metadata key: {key}")
                
        self.metadata['modified'] = datetime.now().isoformat()
    
    def validate_python_version(self) -> bool:
        """
        Validate that the current Python version meets minimum requirements.
        
        Returns:
            bool: True if Python version is compatible
            
        Example:
            >>> header = StandardHeader("test", "/test.py")
            >>> assert header.validate_python_version() is True
        """
        current_version = sys.version_info
        min_version = PYTHON_MIN_VERSION
        
        if current_version < min_version:
            logger.warning(
                f"Python {'.'.join(map(str, min_version))}+ required, "
                f"but Python {'.'.join(map(str, current_version[:2]))} found"
            )
            return False
        
        return True
    
    def get_file_info(self) -> Dict[str, str]:
        """
        Get comprehensive file information.
        
        Returns:
            Dict[str, str]: File information including size, modification time
            
        Example:
            >>> import tempfile
            >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as f:
            ...     f.write("# test file")
            ...     f.flush()
            ...     header = StandardHeader("test", f.name)
            ...     info = header.get_file_info()
            ...     assert 'size' in info
        """
        try:
            stat_info = os.stat(self.file_path)
            return {
                'size': str(stat_info.st_size),
                'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                'created': datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                'permissions': oct(stat_info.st_mode)[-3:]
            }
        except OSError as e:
            logger.error(f"Error getting file info: {str(e)}")
            return {'error': str(e)}


def create_standard_header(module_name: str, 
                         file_path: str,
                         purpose: str = "",
                         description: str = "") -> str:
    """
    Convenience function to create a standard header.
    
    Args:
        module_name (str): Name of the module
        file_path (str): Path to the file
        purpose (str): Purpose of the module
        description (str): Description of the module
        
    Returns:
        str: Generated header string
        
    Example:
        >>> header = create_standard_header(
        ...     "test_module",
        ...     "/path/to/test.py",
        ...     "Testing purposes",
        ...     "A test module"
        ... )
        >>> assert "Testing purposes" in header
    """
    header = StandardHeader(module_name, file_path)
    return header.generate_header(
        purpose=purpose,
        description=description
    )


def main():
    """Main function for testing the standard header functionality."""
    try:
        # Example usage
        header = StandardHeader("example_module", __file__)
        header_content = header.generate_header(
            purpose="Demonstration of standard header",
            description="This module demonstrates the standard header format"
        )
        
        print("Generated Header:")
        print("=" * 50)
        print(header_content)
        print("=" * 50)
        
        # Display metadata
        metadata = header.get_metadata()
        print("\nMetadata:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")
            
        # Validate Python version
        if header.validate_python_version():
            print("\n✅ Python version is compatible")
        else:
            print("\n❌ Python version is not compatible")
            
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
