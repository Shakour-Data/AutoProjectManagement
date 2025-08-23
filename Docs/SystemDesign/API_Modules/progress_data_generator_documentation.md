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
