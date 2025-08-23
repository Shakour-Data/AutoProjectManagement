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

