"""
path: autoprojectmanagement/services/json_data_linker.py
File: json_data_linker.py
Purpose: Link and manage JSON data relationships across the AutoProjectManagement system
Author: BLACKBOXAI
Version: 1.0.0
License: MIT
Description: Provides comprehensive JSON data linking, validation, and relationship management
for project management data structures including WBS, resources, tasks, and progress tracking.
"""

import json
import os
import logging
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime
import hashlib
from contextlib import contextmanager

# Constants
MAX_JSON_FILE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_JSON_VERSIONS = ["1.0", "1.1", "2.0"]
DEFAULT_ENCODING = "utf-8"
BACKUP_SUFFIX = ".backup"

# Configure logging
logger = logging.getLogger(__name__)


class JSONDataLinker:
    """
    Manages JSON data linking and relationships across the AutoProjectManagement system.
    
    This class provides functionality to:
    - Link JSON files and maintain relationships
    - Validate JSON data structures
    - Manage data integrity across files
    - Handle backup and recovery
    - Track changes and versions
    
    Example:
        >>> linker = JSONDataLinker()
        >>> linker.link_files(['wbs.json', 'resources.json'])
        >>> relationships = linker.get_relationships()
    """
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the JSON data linker.
        
        Args:
            base_path: Base directory for JSON files. Defaults to current directory.
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.linked_files: Dict[str, Dict[str, Any]] = {}
        self.relationships: Dict[str, List[str]] = {}
        self.validation_errors: List[str] = []
        
    def link_files(self, file_paths: List[str]) -> bool:
        """
        Link multiple JSON files and establish relationships.
        
        Args:
            file_paths: List of JSON file paths to link
            
        Returns:
            True if all files linked successfully, False otherwise
            
        Example:
            >>> linker = JSONDataLinker()
            >>> success = linker.link_files(['data1.json', 'data2.json'])
        """
        success = True
        for file_path in file_paths:
            if not self._link_single_file(file_path):
                success = False
        return success
    
    def _link_single_file(self, file_path: str) -> bool:
        """
        Link a single JSON file and validate its structure.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            True if file linked successfully, False otherwise
        """
        try:
            full_path = self.base_path / file_path
            if not full_path.exists():
                logger.error(f"File not found: {full_path}")
                return False
            
            if full_path.stat().st_size > MAX_JSON_FILE_SIZE:
                logger.error(f"File too large: {file_path}")
                return False
            
            with open(full_path, 'r', encoding=DEFAULT_ENCODING) as f:
                data = json.load(f)
            
            file_hash = self._calculate_hash(full_path)
            self.linked_files[file_path] = {
                'data': data,
                'hash': file_hash,
                'last_modified': datetime.now().isoformat()
            }
            
            logger.info(f"Successfully linked: {file_path}")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            self.validation_errors.append(f"{file_path}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error linking {file_path}: {e}")
            return False
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file contents."""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def validate_json_structure(self, data: Dict[str, Any]) -> bool:
        """
        Validate JSON data structure against schema requirements.
        
        Args:
            data: JSON data to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['version', 'type', 'data']
        for field in required_fields:
            if field not in data:
                self.validation_errors.append(f"Missing required field: {field}")
                return False
        
        if data.get('version') not in SUPPORTED_JSON_VERSIONS:
            self.validation_errors.append(
                f"Unsupported version: {data.get('version')}"
            )
            return False
        
        return True
    
    def get_relationships(self) -> Dict[str, List[str]]:
        """
        Get all established relationships between linked files.
        
        Returns:
            Dictionary mapping file paths to their related files
        """
        return self.relationships.copy()
    
    def create_backup(self, file_path: str) -> bool:
        """
        Create a backup of a JSON file before modification.
        
        Args:
            file_path: Path to the file to backup
            
        Returns:
            True if backup created successfully, False otherwise
        """
        try:
            full_path = self.base_path / file_path
            backup_path = full_path.with_suffix(full_path.suffix + BACKUP_SUFFIX)
            
            with open(full_path, 'rb') as source:
                with open(backup_path, 'wb') as backup:
                    backup.write(source.read())
            
            logger.info(f"Backup created: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return False
    
    def restore_from_backup(self, file_path: str) -> bool:
        """
        Restore a JSON file from its backup.
        
        Args:
            file_path: Path to the file to restore
            
        Returns:
            True if restored successfully, False otherwise
        """
        try:
            full_path = self.base_path / file_path
            backup_path = full_path.with_suffix(full_path.suffix + BACKUP_SUFFIX)
            
            if not backup_path.exists():
                logger.error(f"Backup not found: {backup_path}")
                return False
            
            with open(backup_path, 'rb') as backup:
                with open(full_path, 'wb') as target:
                    target.write(backup.read())
            
            logger.info(f"Restored from backup: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore from backup: {e}")
            return False
    
    def get_validation_errors(self) -> List[str]:
        """
        Get list of validation errors from recent operations.
        
        Returns:
            List of error messages
        """
        return self.validation_errors.copy()
    
    def clear_validation_errors(self) -> None:
        """Clear all validation errors."""
        self.validation_errors.clear()
    
    def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a linked file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information or None if not found
        """
        return self.linked_files.get(file_path)
    
    def unlink_file(self, file_path: str) -> bool:
        """
        Remove a file from the linked files.
        
        Args:
            file_path: Path to the file to unlink
            
        Returns:
            True if unlinked successfully, False otherwise
        """
        if file_path in self.linked_files:
            del self.linked_files[file_path]
            self.relationships.pop(file_path, None)
            logger.info(f"Unlinked file: {file_path}")
            return True
        return False
    
    def get_linked_files_count(self) -> int:
        """
        Get the number of currently linked files.
        
        Returns:
            Count of linked files
        """
        return len(self.linked_files)
    
    def export_relationships(self, output_path: str) -> bool:
        """
        Export relationships to a JSON file.
        
        Args:
            output_path: Path to save the relationships file
            
        Returns:
            True if exported successfully, False otherwise
        """
        try:
            export_data = {
                'timestamp': datetime.now().isoformat(),
                'linked_files': list(self.linked_files.keys()),
                'relationships': self.relationships,
                'total_files': len(self.linked_files)
            }
            
            with open(self.base_path / output_path, 'w', encoding=DEFAULT_ENCODING) as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"Relationships exported to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export relationships: {e}")
            return False
    
    def import_relationships(self, input_path: str) -> bool:
        """
        Import relationships from a JSON file.
        
        Args:
            input_path: Path to the relationships file
            
        Returns:
            True if imported successfully, False otherwise
        """
        try:
            with open(self.base_path / input_path, 'r', encoding=DEFAULT_ENCODING) as f:
                data = json.load(f)
            
            self.relationships = data.get('relationships', {})
            logger.info(f"Relationships imported from: {input_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import relationships: {e}")
            return False
    
    @contextmanager
    def atomic_operation(self, file_path: str):
        """
        Context manager for atomic file operations with automatic backup.
        
        Args:
            file_path: Path to the file for atomic operations
            
        Example:
            >>> with linker.atomic_operation('data.json') as data:
            ...     data['new_key'] = 'new_value'
        """
        full_path = self.base_path / file_path
        
        # Create backup
        self.create_backup(file_path)
        
        try:
            # Load current data
            with open(full_path, 'r', encoding=DEFAULT_ENCODING) as f:
                data = json.load(f)
            
            yield data
            
            # Save modified data
            with open(full_path, 'w', encoding=DEFAULT_ENCODING) as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            # Restore from backup on error
            logger.error(f"Error during atomic operation: {e}")
            self.restore_from_backup(file_path)
            raise


# Utility functions
def validate_json_file(file_path: str) -> bool:
    """
    Validate a JSON file without linking it.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        True if valid, False otherwise
        
    Example:
        >>> is_valid = validate_json_file('data.json')
    """
    try:
        with open(file_path, 'r', encoding=DEFAULT_ENCODING) as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, FileNotFoundError):
        return False


def merge_json_files(file_paths: List[str], output_path: str) -> bool:
    """
    Merge multiple JSON files into a single file.
    
    Args:
        file_paths: List of JSON files to merge
        output_path: Path for the merged output
        
    Returns:
        True if merged successfully, False otherwise
        
    Example:
        >>> success = merge_json_files(['file1.json', 'file2.json'], 'merged.json')
    """
    try:
        merged_data = {}
        
        for file_path in file_paths:
            with open(file_path, 'r', encoding=DEFAULT_ENCODING) as f:
                data = json.load(f)
                merged_data.update(data)
        
        with open(output_path, 'w', encoding=DEFAULT_ENCODING) as f:
            json.dump(merged_data, f, indent=2)
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to merge JSON files: {e}")
        return False


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    linker = JSONDataLinker()
    
    # Test linking files
    test_files = ['test1.json', 'test2.json']
    if linker.link_files(test_files):
        print(f"Linked {linker.get_linked_files_count()} files")
        relationships = linker.get_relationships()
        print("Relationships:", relationships)
    else:
        print("Failed to link files")
        errors = linker.get_validation_errors()
        for error in errors:
            print(f"Error: {error}")
