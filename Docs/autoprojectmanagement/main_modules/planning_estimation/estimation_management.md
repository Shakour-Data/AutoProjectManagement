# Estimation Management Module Documentation

*Last updated: 2025-08-14*

## Overview

The `estimation_management.py` module is a core component of the AutoProjectManagement system that provides comprehensive project estimation capabilities. This module handles task duration estimation based on complexity levels, cost estimation based on resources and duration, and project-level duration and cost aggregation. It supports multiple estimation methodologies including parametric estimation with configurable complexity mapping.

## Architecture Diagram

```mermaid
graph TD
    A[EstimationManagement] --> B[BaseManagement]
    B --> C[load_json]
    B --> D[save_json]
    B --> E[load_inputs]
    B --> F[validate_inputs]
    B --> G[run]
    A --> H[analyze]
    
    H --> I[Task Duration Estimation]
    H --> J[Task Cost Estimation]
    H --> K[Project Aggregation]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style H fill:#e8f5e8
```

## Module Structure

### Class Hierarchy

| Class | Description | Inheritance |
|-------|-------------|-------------|
| `BaseManagement` | Base class for file-based operations | - |
| `EstimationManagement` | Project estimation management | Inherits from `BaseManagement` |

### Key Components

| Component | Type | Purpose | Default Value |
|-----------|------|---------|---------------|
| `detailed_wbs_path` | Configuration | Path to detailed WBS JSON file | `project_inputs/PM_JSON/user_inputs/detailed_wbs.json` |
| `output_path` | Configuration | Path for estimation output | `project_inputs/PM_JSON/system_outputs/estimation_management.json` |
| `inputs` | Data Storage | Loaded input data | `{}` |
| `output` | Data Storage | Processed estimation results | `{}` |

### Constants and Configuration

| Constant | Value | Description |
|----------|-------|-------------|
| `DEFAULT_COST_PER_RESOURCE` | `100.0` | Base cost per resource unit |
| `DEFAULT_COMPLEXITY_MAPPING` | Dictionary | Maps complexity levels to duration multipliers |
| `MAX_LINE_LENGTH` | `79` | Maximum line length for code formatting |
| `DEFAULT_ENCODING` | `'utf-8'` | Default file encoding |
| `JSON_INDENT` | `2` | JSON indentation level |

### Complexity Mapping

| Complexity Level | Duration Multiplier | Description |
|------------------|---------------------|-------------|
| `low` | `1.0` | Simple, well-understood tasks |
| `medium` | `3.0` | Standard complexity tasks |
| `high` | `5.0` | Complex tasks requiring expertise |
| `extreme` | `8.0` | Highly complex, uncertain tasks |

## Detailed Method Documentation

### BaseManagement Class

#### Constructor
```python
def __init__(self, input_paths: Dict[str, str], output_path: str) -> None
```

**Purpose:** Initializes the base management class with input and output file paths.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `input_paths` | `Dict[str, str]` | Yes | Dictionary mapping input names to file paths |
| `output_path` | `str` | Yes | Path where output will be saved |

**Validation Rules:**
- `input_paths` must be a non-empty dictionary
- `output_path` must be a non-empty string

**Raises:**
- `ValueError`: If input_paths or output_path are empty

#### load_json Method
```python
def load_json(self, path: str) -> Optional[Dict[str, Any]]
```

**Purpose:** Loads JSON data from a specified file path with comprehensive error handling.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | `str` | Yes | Path to the JSON file |

**Returns:** `Optional[Dict[str, Any]]` - Dictionary containing JSON data or None if file doesn't exist

**Error Handling:**
- `json.JSONDecodeError`: If file contains invalid JSON, error is logged and exception is raised
- `Exception`: General file reading errors are caught and logged

#### save_json Method
```python
def save_json(self, data: Dict[str, Any], path: str) -> None
```

**Purpose:** Saves data as JSON to a specified file path with proper formatting.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `data` | `Dict[str, Any]` | Yes | Dictionary to save as JSON |
| `path` | `str` | Yes | Path where to save the file |

**Features:**
- Creates parent directories if they don't exist
- Uses proper JSON formatting with indentation
- Handles file writing errors gracefully

**Error Handling:**
- `IOError`: If there's an error writing the file, exception is raised

#### load_inputs Method
```python
def load_inputs(self) -> None
```

**Purpose:** Loads all input JSON files into memory.

**Process:**
- Iterates through all input paths
- Loads each JSON file using `load_json` method
- Stores loaded data in `inputs` dictionary
- Logs successful loading operations

#### validate_inputs Method
```python
def validate_inputs(self) -> bool
```

**Purpose:** Validates loaded inputs before analysis.

**Returns:** `bool` - True if all inputs are valid (non-empty), False otherwise

**Validation:**
- Checks that all input values in `inputs` dictionary are truthy
- Returns False if any input is empty or None

#### run Method
```python
def run(self) -> None
```

**Purpose:** Executes the complete management workflow.

**Process Flow:**
1. Loads all input files
2. Validates loaded inputs
3. Performs analysis (calls `analyze` method)
4. Saves output to JSON file
5. Logs completion status

**Raises:**
- `ValueError`: If inputs are invalid after validation

### EstimationManagement Class

#### Constructor
```python
def __init__(self,
             detailed_wbs_path: str = 'project_inputs/PM_JSON/user_inputs/detailed_wbs.json',
             output_path: str = 'project_inputs/PM_JSON/system_outputs/estimation_management.json') -> None
```

**Purpose:** Initializes estimation management with WBS data path and output path.

**Parameters:**
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `detailed_wbs_path` | `str` | No | Path to detailed WBS JSON file | `project_inputs/PM_JSON/user_inputs/detailed_wbs.json` |
| `output_path` | `str` | No | Path for estimation output | `project_inputs/PM_JSON/system_outputs/estimation_management.json` |

#### analyze Method
```python
def analyze(self) -> None
```

**Purpose:** Performs comprehensive project estimation analysis.

**Process:**
1. Extracts tasks from loaded WBS data
2. Estimates duration for each task based on complexity
3. Estimates cost for each task based on resources and duration
4. Aggregates project-level totals
5. Structures output with summary and detailed estimates

**Output Structure:**
```json
{
  "summary": {
    "total_tasks": 15,
    "total_duration": 42.5,
    "total_cost": 4250.0
  },
  "details": {
    "task_estimates": [
      {
        "id": "task_001",
        "name": "Design Phase",
        "duration": 5.0,
        "cost": 500.0,
        "complexity": "high"
      }
    ]
  }
}
```

### Utility Functions

#### estimate_task_duration Function
```python
def estimate_task_duration(task: Dict[str, Any]) -> float
```

**Purpose:** Estimates task duration based on complexity level.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task` | `Dict[str, Any]` | Yes | Task dictionary containing complexity |

**Returns:** `float` - Estimated duration based on complexity mapping

**Validation:**
- Task must be a non-None dictionary
- Uses 'medium' complexity as default if not specified

**Raises:**
- `TypeError`: If task is None or not a dictionary

#### estimate_task_cost Function
```python
def estimate_task_cost(task: Dict[str, Any]) -> float
```

**Purpose:** Estimates task cost based on resources and duration.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task` | `Dict[str, Any]` | Yes | Task dictionary containing resources |

**Returns:** `float` - Estimated cost (duration × resources × cost_per_resource)

**Formula:**
```
cost = duration × resources × DEFAULT_COST_PER_RESOURCE
```

**Validation:**
- Task must be a non-None dictionary
- Uses 1 resource as default if not specified

**Raises:**
- `TypeError`: If task is None or not a dictionary

#### estimate_project_duration Function
```python
def estimate_project_duration(project: Dict[str, Any]) -> float
```

**Purpose:** Estimates project duration by summing task durations.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project` | `Dict[str, Any]` | Yes | Project dictionary containing tasks |

**Returns:** `float` - Total project duration

**Process:**
- Extracts tasks list from project
- Sums duration estimates for all tasks
- Returns 0.0 if no tasks found

**Raises:**
- `TypeError`: If project is None or not a dictionary

#### estimate_project_cost Function
```python
def estimate_project_cost(project: Dict[str, Any]) -> float
```

**Purpose:** Estimates project cost by summing task costs.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project` | `Dict[str, Any]` | Yes | Project dictionary containing tasks |

**Returns:** `float` - Total project cost

**Process:**
- Extracts tasks list from project
- Sums cost estimates for all tasks
- Returns 0.0 if no tasks found

**Raises:**
- `TypeError`: If project is None or not a dictionary

## Data Flow Diagram

```mermaid
flowchart TD
    A[Detailed WBS JSON] --> B[load_inputs]
    B --> C[analyze]
    C --> D[Task Extraction]
    C --> E[Duration Estimation]
    C --> F[Cost Estimation]
    C --> G[Aggregation]
    D --> H[Task Estimates]
    E --> H
    F --> H
    G --> I[Project Summary]
    H --> J[Output JSON]
    I --> J
```

## Validation Rules

### Input Validation
| Requirement | Validation | Error Handling |
|-------------|------------|----------------|
| WBS Structure | Must be a dictionary | Empty output with warning |
| Tasks List | Must be a list if present | Empty list used if missing |
| Task Complexity | Must be valid complexity level | 'medium' used as default |
| Task Resources | Must be numeric if present | 1 used as default |

### Estimation Validation
| Requirement | Validation | Error Handling |
|-------------|------------|----------------|
| Duration Calculation | Uses complexity mapping | Default mapping for unknown levels |
| Cost Calculation | Resources × Duration × Base Cost | Handles missing values gracefully |
| Project Aggregation | Sums all valid estimates | Skips invalid tasks |

## Error Handling and Logging

### Log Levels
| Level | Usage | Example |
|-------|-------|---------|
| `INFO` | Successful operations | "Estimation completed successfully" |
| `WARNING` | Non-critical issues | "Using default complexity: medium" |
| `ERROR` | Critical failures | "Invalid JSON in WBS file" |

### Common Error Scenarios
1. **Invalid JSON Files**: Error logged, exception raised
2. **Missing WBS Data**: Warning logged, empty results returned
3. **Invalid Task Structure**: Task skipped, warning logged
4. **File Write Errors**: Error logged, exception raised
5. **Missing Complexity**: Default complexity used, warning logged

## Usage Examples

### Basic Usage
```python
from autoprojectmanagement.main_modules.planning_estimation.estimation_management import EstimationManagement

# Initialize with default paths
manager = EstimationManagement()
manager.run()

# Access results
results = manager.output
print(f"Total cost: ${results['summary']['total_cost']:,.2f}")
```

### Custom Configuration
```python
manager = EstimationManagement(
    detailed_wbs_path='custom/wbs.json',
    output_path='custom/estimations.json'
)
manager.run()
```

### Programmatic Usage
```python
# Use utility functions directly
from autoprojectmanagement.main_modules.planning_estimation.estimation_management import estimate_task_duration, estimate_task_cost

task = {'complexity': 'high', 'resources': 2}
