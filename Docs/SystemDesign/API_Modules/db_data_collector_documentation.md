### DB Data Collector Module

- **Method:** N/A (Core Module)
- **Path:** `/main_modules/data_collection_processing/db_data_collector.py`
- **Description:** Comprehensive database data collection module for project management data including tasks, resource allocation, progress metrics, and feature weights.
- **Authentication:** N/A (File-based operations)
- **Rate Limit:** N/A

#### Class: DBDataCollector

**Description:** A comprehensive data collector for project management data that provides methods to collect, validate, and store various types of project management data.

**Constructor:**
```python
DBDataCollector(data_dir: str = 'SystemInputs/user_inputs')
```

**Parameters:**
- `data_dir`: Directory path for storing JSON files (default: 'SystemInputs/user_inputs')

#### Methods

**`collect_and_store_tasks(tasks: List[Any]) -> bool`**
- Collects task data including progress, resource allocation, and stores in JSON file
- **Parameters:** `tasks` - List of task objects to collect and store
- **Returns:** True if successful, False otherwise

**`collect_resource_allocation(tasks: List[Any]) -> bool`**
- Analyzes resource allocation and stores summary in JSON file
- **Parameters:** `tasks` - List of task objects to analyze
- **Returns:** True if successful, False otherwise

**`collect_progress_metrics(tasks: List[Any]) -> bool`**
- Collects progress percentages and stores/updates in JSON file
- **Parameters:** `tasks` - List of task objects to collect progress from
- **Returns:** True if successful, False otherwise

**`insert_feature_weights(urgency_weights: Dict[str, float], importance_weights: Dict[str, float]) -> bool`**
- Inserts predefined weights for urgency and importance features into JSON file
- **Parameters:**
  - `urgency_weights` - Dictionary of urgency feature weights
  - `importance_weights` - Dictionary of importance feature weights
- **Returns:** True if successful, False otherwise

**`get_collected_data(data_type: str) -> Optional[Dict[str, Any]]`**
- Retrieves previously collected data from JSON files
