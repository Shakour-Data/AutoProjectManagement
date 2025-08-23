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
    GanttChartData, generate_gantt_chart
)

# Method 1: Load from file
generator = GanttChartData()
generator.load_tasks()
gantt_data = generator.build_gantt_data()
print(f"Generated {len(gantt_data)} Gantt tasks")

# Method 2: Direct generation
tasks = [
    {
        "id": "task-1",
        "name": "Design Phase",
        "start": "2025-08-15",
        "end": "2025-08-22",
        "progress": 50
    }
]
result = generate_gantt_chart(tasks)
print(f"Gantt chart data: {result}")
```

**Custom Input Directory:**
```python
# Custom input directory
generator = GanttChartData(input_dir='custom/inputs')
generator.load_tasks()
data = generator.build_gantt_data()
```

**Error Handling:**
```python
try:
    tasks = [{"id": "task-1", "start": "invalid-date", "end": "2025-08-22"}]
    result = generate_gantt_chart(tasks)
except ValueError as e:
    print(f"Date validation error: {e}")
except TypeError as e:
    print(f"Type error: {e}")
```

#### Processing Logic

**Date Calculation:**
```
end_date = start_date + timedelta(days=duration_days)
```

**Progress Conversion:**
```
progress_percentage = progress_float * 100  # Convert 0.0-1.0 to 0-100
```

**Dependency Handling:**
- Maintains task dependency lists
- Supports complex dependency chains
- Handles circular dependency prevention

**Subtask Processing:**
- Recursive subtask processing
- Parent-child relationship maintenance
- Inherited start dates for subtasks

#### Error Handling

**Common Errors:**
- Invalid date formats
- Missing required fields
- File not found errors
- JSON parsing errors

**Exception Types:**
- `TypeError`: Invalid input types
- `ValueError`: Invalid date formats or values
- `KeyError`: Missing required fields
- `IOError`: File operation errors

**Error Responses:**
- Returns empty lists for file errors
- Raises specific exceptions for validation failures
- Provides detailed error messages

#### Dependencies

**Internal Dependencies:**
- Standard library modules: os, json, datetime, typing
- No external package dependencies

**External Dependencies:**
- Python 3.8+
- Valid task JSON files
- Proper file system access

#### Performance Considerations

**File I/O:**
- Efficient JSON file loading
- Proper error handling for missing files
- Memory-efficient data structures

**Date Processing:**
- Efficient date parsing and calculation
- Optimized datetime operations
- Minimal overhead for large task sets

**Recursive Processing:**
- Efficient subtask traversal
- Proper depth limiting
- Memory management for deep hierarchies

#### Integration Points

**With WBS Systems:**
- Integrates with Work Breakdown Structure data
- Supports hierarchical task structures
- Handles complex project hierarchies

**With Timeline Visualization:**
- Provides data for Gantt chart rendering
- Supports timeline visualization tools
- Integrates with project management dashboards

**With Progress Tracking:**
- Incorporates progress information
- Supports real-time progress updates
- Integrates with progress reporting systems

**With Dependency Management:**
- Handles task dependencies
- Supports critical path analysis
- Integrates with scheduling systems

#### Best Practices

**Data Validation:**
- Comprehensive input validation
- Strict date format enforcement
- Required field checking

**Error Handling:**
- Graceful degradation for file errors
- Detailed error messages for validation failures
- Proper exception handling

**Performance Optimization:**
- Efficient data structures for large projects
- Optimized date calculations
- Memory management for recursive processing

**File Management:**
- Regular backup of Gantt data
- Version control for timeline configurations
- Proper file permission settings

#### Use Cases

**Project Planning:**
- Timeline development and visualization
- Schedule creation and management
- Milestone tracking

**Progress Monitoring:**
- Real-time progress tracking
- Schedule variance analysis
- Performance measurement

**Resource Planning:**
- Resource allocation timeline
- Team capacity planning
- Workload distribution

**Client Reporting:**
- Project status reporting
- Timeline visualization for stakeholders
- Progress demonstration

#### Security Considerations

**Data Privacy:**
- Handle sensitive timeline data appropriately
- Protect Gantt chart configuration files
- Implement access controls

**File Permissions:**
- Set appropriate file permissions
- Protect configuration data
- Regular security audits

**Input Validation:**
- Validate all input data thoroughly
- Prevent injection attacks
- Sanitize external inputs

**Date Security:**
- Validate date ranges appropriately
- Prevent timeline manipulation
- Ensure realistic scheduling

---

*This documentation follows the API Documentation Template standards. Last updated: 2025-08-14*
