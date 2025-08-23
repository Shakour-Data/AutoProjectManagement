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
