### Estimation Management Module

- **Method:** N/A (Core Module)
- **Path:** `/main_modules/planning_estimation/estimation_management.py`
- **Description:** Comprehensive project estimation management module providing task duration and cost estimation, project-level aggregation, and multiple estimation methodologies.
- **Authentication:** N/A (File-based operations)
- **Rate Limit:** N/A

#### Class: BaseManagement

**Description:** Base class for management operations with JSON I/O capabilities, providing common functionality for loading inputs, processing data, and saving outputs.

**Constructor:**
```python
BaseManagement(input_paths: Dict[str, str], output_path: str)
```

**Parameters:**
- `input_paths`: Dictionary mapping input names to file paths
- `output_path`: Path where output JSON will be saved

#### Methods (BaseManagement)

**`load_json(path: str) -> Optional[Dict[str, Any]]`**
- Loads JSON data from file with error handling
- **Parameters:** `path` - File path to load
- **Returns:** Parsed JSON data or None if error

**`save_json(data: Dict[str, Any], path: str) -> None`**
- Saves data to JSON file with proper formatting
- **Parameters:**
  - `data` - Data to save
  - `path` - File path to save to

**`load_inputs() -> None`**
- Loads all input JSON files into memory

**`analyze() -> None`**
- Abstract method for data analysis (must be implemented by subclasses)

**`validate_inputs() -> bool`**
- Validates loaded inputs before analysis
- **Returns:** True if all inputs are valid

**`run() -> None`**
- Executes the complete management workflow

#### Standalone Functions

**`estimate_task_duration(task: Dict[str, Any]) -> float`**
- Estimates task duration based on complexity level
- **Parameters:** `task` - Task dictionary
- **Returns:** Estimated duration
- **Raises:** `TypeError` for invalid input

**`estimate_task_cost(task: Dict[str, Any]) -> float`**
- Estimates task cost based on resources and duration
- **Parameters:** `task` - Task dictionary
- **Returns:** Estimated cost
- **Raises:** `TypeError` for invalid input

**`estimate_project_duration(project: Dict[str, Any]) -> float`**
- Estimates project duration by summing task durations
- **Parameters:** `project` - Project dictionary
- **Returns:** Total project duration
- **Raises:** `TypeError` for invalid input

**`estimate_project_cost(project: Dict[str, Any]) -> float`**
- Estimates project cost by summing task costs
- **Parameters:** `project` - Project dictionary
- **Returns:** Total project cost
- **Raises:** `TypeError` for invalid input

#### Class: EstimationManagement

**Description:** Project estimation management class with advanced estimation capabilities, extending BaseManagement.

**Constructor:**
```python
EstimationManagement(
    detailed_wbs_path: str = 'project_inputs/PM_JSON/user_inputs/detailed_wbs.json',
    output_path: str = 'project_inputs/PM_JSON/system_outputs/estimation_management.json'
)
```

**Parameters:**
- `detailed_wbs_path`: Path to detailed WBS JSON file
- `output_path`: Path for saving estimation results

#### Methods (EstimationManagement)

**`analyze() -> None`**
- Performs comprehensive project estimation analysis
- Processes WBS data to generate task and project estimates

#### Constants

**Cost and Complexity:**
- `DEFAULT_COST_PER_RESOURCE = 100.0`
