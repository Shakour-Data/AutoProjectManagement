# Communication Management Module Documentation

*Last updated: 2025-08-14*

## Overview

The `communication_management.py` module is a core component of the AutoProjectManagement system that provides comprehensive communication analysis and management capabilities. This module processes communication plans and logs to generate actionable insights and recommendations for improving project communication effectiveness.

## Architecture Diagram

```mermaid
graph TD
    A[CommunicationManagement] --> B[BaseManagement]
    B --> C[load_json]
    B --> D[save_json]
    B --> E[load_inputs]
    A --> F[analyze]
    A --> G[_validate_communication_plan]
    A --> H[_analyze_communication_logs]
    A --> I[_calculate_effectiveness]
    A --> J[_generate_recommendations]
    
    F --> G
    F --> H
    F --> I
    F --> J
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style F fill:#e8f5e8
```

## Module Structure

### Class Hierarchy

| Class | Description | Inheritance |
|-------|-------------|-------------|
| `BaseManagement` | Base class for file-based operations | - |
| `CommunicationManagement` | Communication analysis and management | Inherits from `BaseManagement` |

### Key Components

| Component | Type | Purpose |
|-----------|------|---------|
| `communication_plan_path` | Configuration | Path to communication plan JSON file |
| `communication_logs_path` | Configuration | Path to communication logs JSON file |
| `output_path` | Configuration | Path for saving analysis results |
| `inputs` | Data Storage | Loaded input data from JSON files |
| `output` | Data Storage | Processed analysis results |

## Detailed Method Documentation

### BaseManagement Class

#### Constructor
```python
def __init__(self, input_paths: Dict[str, str], output_path: str) -> None
```

**Purpose:** Initializes the base management class with input and output file paths.

**Parameters:**
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `input_paths` | `Dict[str, str]` | Yes | Dictionary mapping input names to file paths | - |
| `output_path` | `str` | Yes | Path where output will be saved | - |

**Validation Rules:**
- `input_paths` must be a non-empty dictionary
- `output_path` must be a non-empty string

#### load_json Method
```python
def load_json(self, path: str) -> Optional[Dict[str, Any]]
```

**Purpose:** Loads JSON data from a specified file path.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | `str` | Yes | Path to the JSON file |

**Returns:** `Optional[Dict[str, Any]]` - Dictionary containing JSON data or None if file doesn't exist

**Error Handling:**
- `json.JSONDecodeError`: If file contains invalid JSON
- `OSError`: If there's an error reading the file

#### save_json Method
```python
def save_json(self, data: Dict[str, Any], path: str) -> None
```

**Purpose:** Saves data as JSON to a specified file path.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `data` | `Dict[str, Any]` | Yes | Dictionary to save as JSON |
| `path` | `str` | Yes | Path where to save the file |

**Error Handling:**
- `TypeError`: If data is not JSON serializable
- `OSError`: If there's an error writing the file

### CommunicationManagement Class

#### Constructor
```python
def __init__(self, communication_plan_path: str = DEFAULT_COMMUNICATION_PLAN_PATH,
             communication_logs_path: str = DEFAULT_COMMUNICATION_LOGS_PATH,
             output_path: str = DEFAULT_OUTPUT_PATH) -> None
```

**Purpose:** Initializes communication management with default or custom file paths.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `communication_plan_path` | `str` | No | `project_inputs/PM_JSON/user_inputs/communication_plan.json` | Path to communication plan |
| `communication_logs_path` | `str` | No | `project_inputs/PM_JSON/user_inputs/communication_logs.json` | Path to communication logs |
