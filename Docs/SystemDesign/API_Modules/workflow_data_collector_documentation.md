### Workflow Data Collector Module

- **Method:** N/A (Core Module)
- **Path:** `/main_modules/data_collection_processing/workflow_data_collector.py`
- **Description:** Workflow data collection module for managing Scrum workflow data including sprints, tasks, and burndown charts using JSON file storage.
- **Authentication:** N/A (File-based operations)
- **Rate Limit:** N/A

#### Class: WorkflowDataCollector

**Description:** Manages Scrum workflow data including sprints, tasks, and burndown charts using JSON file storage instead of database tables.

**Constructor:**
```python
WorkflowDataCollector(data_dir: str = 'SystemInputs/user_inputs')
```

**Parameters:**
- `data_dir`: Directory path for storing JSON files (default: 'SystemInputs/user_inputs')

#### Methods

**`create_scrum_workflow_tables() -> None`**
- Ensures JSON files exist for Scrum workflow data
- Creates empty JSON arrays if files don't exist

**`update_scrum_task(task_id: str, sprint_id: str, title: str, status: str, priority: str, progress: float) -> None`**
- Updates or creates a Scrum task in the tasks JSON file
- **Parameters:**
  - `task_id`: Unique task identifier
  - `sprint_id`: Sprint identifier
  - `title`: Task title
  - `status`: Task status
  - `priority`: Task priority
  - `progress`: Task progress percentage

