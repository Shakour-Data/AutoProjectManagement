### Progress Data Generator Module

- **Method:** N/A (Core Module)
- **Path:** `/main_modules/data_collection_processing/progress_data_generator.py`
- **Description:** Progress data generation module that combines Git commit history and workflow definitions to calculate and generate task progress metrics.
- **Authentication:** N/A (Git repository access)
- **Rate Limit:** N/A

#### Class: ProgressDataGenerator

**Description:** Generates progress data by analyzing Git commit history and workflow definitions to calculate task completion percentages.

**Constructor:**
```python
ProgressDataGenerator(
    db_progress_json_path: str = 'docs/project_management/task_progress.json',
    workflow_definition_path: str = 'docs/db_json/workflow_definition.json',
    commit_task_id_pattern: str = r'\b\d+\.\d+\b',
    commit_weight: float = 0.6,
    workflow_weight: float = 0.4,
    commit_json_path: str = None
)
```

**Parameters:**
- `db_progress_json_path`: Path to save progress JSON file
- `workflow_definition_path`: Path to workflow definition JSON file
- `commit_task_id_pattern`: Regex pattern to extract task IDs from commit messages
- `commit_weight`: Weight for commit-based progress calculation (0.0-1.0)
- `workflow_weight`: Weight for workflow-based progress calculation (0.0-1.0)
- `commit_json_path`: Optional path to commit JSON file (not used in current implementation)

#### Methods

**`run_git_log() -> Optional[str]`**
- Runs git log command to get commit history with messages and files changed
- **Returns:** Git log output as string, or None if command fails

**`parse_git_log(log_text: str) -> List[Dict]`**
- Parses git log output into structured commit data
- **Parameters:** `log_text` - Git log output text
- **Returns:** List of commit dictionaries with hash, message, and files

**`load_workflow_definition() -> List[Dict]`**
- Loads workflow definition from JSON file
- **Returns:** List of workflow steps or empty list on error

**`map_commits_to_tasks(commits: List[Dict]) -> Dict[str, float]`**
- Maps commits to tasks based on commit messages using regex pattern
- **Parameters:** `commits` - List of parsed commit data
- **Returns:** Dictionary mapping task IDs to progress percentages (0-100)

**`calculate_workflow_progress() -> Dict[str, float]`**
- Calculates progress based on workflow steps completion
- **Returns:** Dictionary mapping task IDs to workflow-based progress percentages

**`combine_progress(commit_progress: Dict[str, float], workflow_progress: Dict[str, float]) -> Dict[str, float]`**
- Combines commit-based and workflow-based progress using configured weights
- **Parameters:**
  - `commit_progress` - Commit-based progress data
  - `workflow_progress` - Workflow-based progress data
- **Returns:** Combined progress data with weighted scores

**`save_progress_to_json(progress_data: Dict[str, float]) -> None`**
- Saves progress data to JSON file
- **Parameters:** `progress_data` - Progress data to save

**`generate_progress() -> None`**
- Executes the complete progress generation workflow

#### Standalone Function

**`generate_progress_data(input_data: Dict) -> Dict[str, Any]`**
- Generates progress data from input data and Git logs
- **Parameters:** `input_data` - Input data dictionary containing tasks
- **Returns:** Generated progress data with task statuses
- **Raises:** `TypeError` for invalid input types, `RuntimeError` for file loading errors

#### Constants

**Default Configuration:**
- `db_progress_json_path = 'docs/project_management/task_progress.json'`
- `workflow_definition_path = 'docs/db_json/workflow_definition.json'`
- `commit_task_id_pattern = r'\b\d+\.\d+\b'` (matches WBS-style task IDs)
- `commit_weight = 0.6`
- `workflow_weight = 0.4`

#### Response Format

**Generated Progress Data:**
```json
{
  "1.1": 75.0,
  "1.2": 50.0,
  "2.1": 100.0,
  "2.2": 25.0
}
```

**Commit Data Structure:**
```json
[
  {
    "hash": "abc123def456",
    "message": "Implement feature X for task 1.1",
    "files": ["src/feature_x.py", "tests/test_feature_x.py"]
  }
]
```

**Workflow Definition Structure:**
```json
[
  {
    "step_id": "step-1",
    "name": "Requirements Analysis",
    "weight": 0.2
  },
  {
    "step_id": "step-2", 
    "name": "Implementation",
    "weight": 0.6
  }
]
```

#### Example Usage

**Basic Progress Generation:**
```python
from autoprojectmanagement.main_modules.data_collection_processing.progress_data_generator import ProgressDataGenerator

# Initialize generator
generator = ProgressDataGenerator()

# Generate progress data
generator.generate_progress()

# Or use standalone function
input_data = {"tasks": [{"id": "1.1", "status": "in_progress"}]}
progress_data = generate_progress_data(input_data)
print(f"Progress data: {progress_data}")
```

**Custom Configuration:**
```python
# Custom configuration
generator = ProgressDataGenerator(
    db_progress_json_path='custom/progress.json',
    workflow_definition_path='custom/workflow.json',
    commit_task_id_pattern=r'TASK-\d+',
    commit_weight=0.7,
    workflow_weight=0.3
)

# Generate with custom settings
generator.generate_progress()
```

**Manual Progress Calculation:**
```python
# Manual progress calculation steps
log_text = generator.run_git_log()
if log_text:
    commits = generator.parse_git_log(log_text)
    commit_progress = generator.map_commits_to_tasks(commits)
    workflow_progress = generator.calculate_workflow_progress()
    combined = generator.combine_progress(commit_progress, workflow_progress)
    generator.save_progress_to_json(combined)
```

#### Progress Calculation Algorithm

**Commit-Based Progress:**
1. Extract task IDs from commit messages using regex pattern
2. Count commits per task ID
3. Normalize counts to 0-100 scale based on maximum count

**Workflow-Based Progress:**
1. Load workflow definition with step weights
2. Track completed steps per task (TODO: implementation needed)
3. Calculate percentage based on completed step weights

**Combined Progress:**
```
combined_score = (commit_score * commit_weight) + (workflow_score * workflow_weight)
```

#### Error Handling

**Common Errors:**
- Git command execution failures
- JSON file loading errors
- Regex pattern matching failures
- File permission issues

**Error Responses:**
- Returns None for failed operations
- Logs detailed error messages
- Graceful degradation for partial failures

**Exception Types:**
- `TypeError` for invalid input data types
- `RuntimeError` for file loading failures
- `subprocess.CalledProcessError` for Git command failures

#### Dependencies

**Internal Dependencies:**
- Standard library modules: subprocess, json, os, re, logging, collections, typing
- No external package dependencies

**External Dependencies:**
- Python 3.8+
- Git command line tool
- Valid Git repository
- Workflow definition JSON files

#### Performance Considerations

**Git Operations:**
- Efficient git log command execution
- Parsing optimization for large commit histories
- Memory-efficient commit data structures

**File I/O:**
- Efficient JSON file operations
- Proper error handling for file access
- Directory creation when needed

**Pattern Matching:**
- Optimized regex pattern compilation
- Efficient task ID extraction
- Scalable pattern matching

#### Integration Points

**With Git Repositories:**
- Integrates with Git version control
- Analyzes commit history for progress tracking
- Supports various Git repository structures

**With Workflow Systems:**
- Integrates with workflow definition files
- Supports customizable workflow steps
- Extensible for different workflow types

**With Progress Reporting:**
- Provides progress data for reporting systems
- Integrates with dashboard systems
- Supports real-time progress updates

**With Task Management:**
- Maps commits to specific tasks
- Supports various task ID formats
- Integrates with task tracking systems

#### Best Practices

**Git Repository Management:**
- Use meaningful commit messages with task IDs
- Maintain consistent task ID patterns
- Regular repository maintenance

**Workflow Definition:**
- Use structured workflow definitions
- Maintain consistent step weighting
- Regular workflow updates

**Progress Calculation:**
- Regular progress generation cycles
- Monitor calculation accuracy
- Adjust weights based on project needs

**Error Handling:**
- Implement comprehensive error logging
- Graceful degradation for failures
- Regular system health checks

#### Use Cases

**Automated Progress Tracking:**
- Regular progress updates from Git history
- Automated progress reporting
- Real-time progress monitoring

**Project Health Monitoring:**
- Task completion tracking
- Team productivity analysis
- Project timeline forecasting

**Integration with CI/CD:**
- Automated progress updates in pipelines
- Build status integration
- Deployment progress tracking

**Reporting and Analytics:**
- Progress trend analysis
- Team performance metrics
- Project health dashboards

#### Security Considerations

**Repository Access:**
- Secure Git repository access
- Proper authentication for private repos
- Access control for sensitive repositories

**Data Privacy:**
- Handle sensitive commit data appropriately
- Protect progress data files
- Implement data encryption if needed

**File Permissions:**
- Set appropriate file permissions
- Protect configuration files
- Regular security audits

---

*This documentation follows the API Documentation Template standards. Last updated: 2025-08-14*
