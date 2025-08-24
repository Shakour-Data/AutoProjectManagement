# JSON Data Linker Documentation

## Overview
The `json_data_linker.py` module manages JSON data linking and relationships across the AutoProjectManagement system. It provides functionality to link JSON files, validate data structures, and maintain data integrity.

## Class: JSONDataLinker
### Purpose
The `JSONDataLinker` class manages JSON data linking and relationships, ensuring data integrity and providing backup and recovery capabilities.

### Attributes
- **linked_files**: Dictionary of linked JSON files
- **relationships**: Dictionary of relationships between files
- **validation_errors**: List of validation errors

### Methods
- **__init__(self, base_path: Optional[str] = None)**: Initializes the JSON data linker.
- **link_files(self, file_paths: List[str]) -> bool**: Links multiple JSON files and establishes relationships.
- **_link_single_file(self, file_path: str) -> bool**: Links a single JSON file and validates its structure.
- **_calculate_hash(self, file_path: Path) -> str**: Calculates MD5 hash of file contents.
- **validate_json_structure(self, data: Dict[str, Any]) -> bool**: Validates JSON data structure against schema requirements.
- **get_relationships(self) -> Dict[str, List[str]]**: Gets all established relationships between linked files.
- **create_backup(self, file_path: str) -> bool**: Creates a backup of a JSON file before modification.
- **restore_from_backup(self, file_path: str) -> bool**: Restores a JSON file from its backup.
- **get_validation_errors(self) -> List[str]**: Gets list of validation errors from recent operations.
