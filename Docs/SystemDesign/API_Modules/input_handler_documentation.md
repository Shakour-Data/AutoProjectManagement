### Input Handler Module

- **Method:** N/A (Core Module)
- **Path:** `/main_modules/data_collection_processing/input_handler.py`
- **Description:** Input data handling and validation module for reading, validating, and processing JSON input files for the project management system.
- **Authentication:** N/A (File-based operations)
- **Rate Limit:** N/A

#### Class: InputHandler

**Description:** Handles reading and processing JSON input files for the project management system, providing methods to read JSON files from a specified directory, validate their contents, and return structured data.

**Constructor:**
```python
InputHandler(input_dir: str = 'project_inputs/PM_JSON/user_inputs')
```

**Parameters:**
