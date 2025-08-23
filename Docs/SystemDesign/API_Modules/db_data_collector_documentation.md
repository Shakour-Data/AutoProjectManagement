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
- **Parameters:** `data_type` - Type of data to retrieve ('tasks', 'resource_allocation', 'progress_metrics', 'feature_weights')
- **Returns:** The collected data or None if file doesn't exist

**`close() -> None`**
- Cleans up resources and closes any open connections

#### Constants

**File Paths:**
- `DEFAULT_DATA_DIR = 'SystemInputs/user_inputs'`
- `tasks_file = 'tasks.json'`
- `resource_allocation_file = 'resource_allocation.json'`
- `progress_metrics_file = 'progress_metrics.json'`
- `feature_weights_file = 'feature_weights.json'`

**Configuration:**
- `ENCODING = 'utf-8'`
- `JSON_INDENT = 4`

#### Response Format

**Tasks Data Format:**
```json
[
  {
    "id": "task-001",
    "name": "Develop API endpoints",
    "assigned_to": ["developer1", "developer2"],
    "progress": 75,
    "priority": "high",
    "deadline": "2025-08-31"
  }
]
```

**Resource Allocation Format:**
```json
{
  "developer1": 3,
  "developer2": 2,
  "tester1": 1
}
```

**Progress Metrics Format:**
```json
{
  "task-001": 75,
  "task-002": 50,
  "task-003": 100
}
```

**Feature Weights Format:**
```json
{
  "urgency_weights": {
    "deadline": 0.4,
    "priority": 0.6
  },
  "importance_weights": {
    "impact": 0.5,
    "effort": 0.5
  },
  "metadata": {
    "created_at": "2025-08-14T10:30:00.000Z",
    "version": "1.0.0"
  }
}
```

#### Example Usage

**Basic Data Collection:**
```python
from autoprojectmanagement.main_modules.data_collection_processing.db_data_collector import DBDataCollector

# Initialize collector
collector = DBDataCollector()

# Collect and store tasks
tasks = [task1, task2, task3]  # Your task objects
success = collector.collect_and_store_tasks(tasks)

if success:
    print("Tasks successfully stored")

# Retrieve collected data
stored_tasks = collector.get_collected_data('tasks')
print(f"Retrieved {len(stored_tasks)} tasks")
```

**Resource Allocation Analysis:**
```python
# Analyze resource allocation
resource_success = collector.collect_resource_allocation(tasks)
if resource_success:
    allocation = collector.get_collected_data('resource_allocation')
    print(f"Resource allocation: {allocation}")
```

**Progress Metrics Collection:**
```python
# Collect progress metrics
progress_success = collector.collect_progress_metrics(tasks)
if progress_success:
    metrics = collector.get_collected_data('progress_metrics')
    print(f"Progress metrics: {metrics}")
```

**Feature Weights Management:**
```python
# Insert feature weights
urgency_weights = {'deadline': 0.4, 'priority': 0.6}
importance_weights = {'impact': 0.5, 'effort': 0.5}

weights_success = collector.insert_feature_weights(urgency_weights, importance_weights)
if weights_success:
    print("Feature weights successfully stored")
```

**Context Manager Usage:**
```python
# Using context manager for automatic cleanup
with DBDataCollector() as collector:
    collector.collect_and_store_tasks(tasks)
    # Data is automatically saved and collector closed
```

#### Validation Rules

**Task Validation:**
- Tasks must be a list
- Each task must have `__dict__` attribute
- Empty lists are allowed but generate warnings

**Weight Validation:**
- Weights must be dictionaries
- Weight values must be numbers between 0 and 1
- Invalid weights cause operation failure

**File Operations:**
- Directory creation with proper error handling
- JSON encoding with proper error handling
- File existence checks before reading

#### Error Handling

**Common Errors:**
- Invalid data directory paths
- JSON encoding/decoding errors
- File I/O errors
- Invalid data types or structures

**Error Responses:**
- Returns False for operation failures
- Logs detailed error messages
- Provides warnings for non-critical issues

#### Dependencies

**Internal Dependencies:**
- `feature_weights` from utility modules
- Standard library modules: json, datetime, logging, os, pathlib, typing

**External Dependencies:**
- Python 3.8+
- No external package dependencies

#### Performance Considerations

**File I/O:**
- Efficient JSON serialization/deserialization
- Proper file encoding handling
- Directory creation optimization

**Memory Usage:**
- Efficient data structures for large task lists
- Minimal memory footprint for file operations
- Proper resource cleanup

**Concurrency:**
- Thread-safe file operations
- Proper error handling for concurrent access
- File locking considerations for production use

#### Integration Points

**With Task Management:**
- Collects data from task objects
- Supports various task attribute structures
- Integrates with progress calculation systems

**With Resource Management:**
- Analyzes resource allocation patterns
- Provides resource usage statistics
- Supports resource optimization

**With Progress Reporting:**
- Collects progress metrics
- Supports progress tracking and reporting
- Integrates with dashboard systems

**With Feature Weight Systems:**
- Stores urgency and importance weights
- Supports priority calculation systems
- Integrates with task prioritization

#### Best Practices

**Data Directory Management:**
- Use meaningful directory structures
- Implement proper backup strategies
- Monitor disk space usage
- Regular cleanup of old data files

**Data Validation:**
- Validate input data before storage
- Implement comprehensive error checking
- Provide meaningful error messages
- Log all validation failures

**File Management:**
- Use consistent file naming conventions
- Implement versioning for data files
- Regular integrity checks
- Backup and recovery procedures

**Performance Optimization:**
- Batch processing for large datasets
- Efficient memory usage patterns
- Optimized file I/O operations
- Caching strategies for frequently accessed data

#### Use Cases

**Project Data Collection:**
- Regular collection of project metrics
- Comprehensive data storage for analysis
- Historical data tracking

**Reporting and Analytics:**
- Data source for progress reports
- Resource utilization analysis
- Performance trend tracking

**System Integration:**
- Data exchange between modules
- Integration with external systems
- API data provisioning

**Backup and Recovery:**
- Data persistence for system restarts
- Disaster recovery data storage
- Audit trail maintenance

#### Security Considerations

**Data Privacy:**
- Handle sensitive project data appropriately
- Implement access controls for data files
- Follow organizational data protection policies

**File Permissions:**
- Set appropriate file permissions
- Protect sensitive configuration data
- Regular security audits

**Data Integrity:**
- Implement data validation checks
- Regular integrity verification
- Backup and recovery procedures

---

*This documentation follows the API Documentation Template standards. Last updated: 2025-08-14*
