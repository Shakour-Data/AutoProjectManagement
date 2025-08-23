### Gantt Chart Data Module

- **Method:** N/A (Core Module)
- **Path:** `/main_modules/planning_estimation/gantt_chart_data.py`
- **Description:** Gantt chart data generation module for creating structured timeline data from task information, including date parsing, dependency handling, and progress tracking.
- **Authentication:** N/A (File-based operations)
- **Rate Limit:** N/A

#### Class: GanttChartData

**Description:** Generates Gantt chart data from task information, handling date parsing, dependency management, and progress calculation for timeline visualization.

**Constructor:**
```python
GanttChartData(input_dir: str = 'project_inputs/PM_JSON/user_inputs')
```

**Parameters:**
- `input_dir`: Directory path containing task JSON files (default: 'project_inputs/PM_JSON/user_inputs')

#### Methods

**`load_tasks() -> None`**
- Loads tasks from detailed_wbs.json file
- Handles file loading errors gracefully

**`parse_date(date_str: Optional[str]) -> Optional[datetime.date]`**
- Parses ISO format date strings into date objects
- **Parameters:** `date_str` - ISO format date string
- **Returns:** Date object or None if invalid

**`build_gantt_data() -> List[Dict[str, Any]]`**
- Builds Gantt chart data structure from loaded tasks
- **Returns:** List of Gantt task dictionaries with timeline information

#### Standalone Function

**`generate_gantt_chart(tasks: List[Dict]) -> Dict[str, List[Dict]]`**
- Generates Gantt chart data from a list of tasks with validation
- **Parameters:** `tasks` - List of task dictionaries
- **Returns:** Dictionary containing processed Gantt tasks
- **Raises:** Various validation errors for invalid input

#### Data Structures

**Input Task Format:**
```json
{
  "id": "task-001",
  "name": "Develop API",
  "start_date": "2025-08-15",
  "duration_days": 5,
  "dependencies": ["task-002"],
  "progress": 0.75,
  "subtasks": [
    {
      "id": "subtask-001",
      "name": "Design endpoints",
      "duration_days": 2
    }
  ]
}
```

**Output Gantt Data Format:**
```json
{
  "tasks": [
    {
      "id": "task-001",
      "name": "Develop API",
      "start_date": "2025-08-15",
      "end_date": "2025-08-20",
      "dependencies": ["task-002"],
      "progress": 75
    }
  ]
}
```

#### Validation Rules

**Task Validation:**
- Tasks cannot be None
- Tasks must be dictionaries
- Required fields: id, start, end
- Date format must be ISO format (YYYY-MM-DD)
- Start date cannot be after end date
- Name must be string or None
- Progress must be numeric (0-100)

**Date Validation:**
- ISO format date strings
- Valid date ranges
- Proper date parsing with error handling

#### Example Usage

**Basic Gantt Generation:**
```python
from autoprojectmanagement.main_modules.planning_estimation.gantt_chart_data import (
