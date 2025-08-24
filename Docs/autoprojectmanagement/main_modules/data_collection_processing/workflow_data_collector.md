# Workflow Data Collector Module Documentation

*Last updated: 2025-08-14*

## Overview

The `workflow_data_collector.py` module is a specialized component of the AutoProjectManagement system that manages Scrum workflow data collection and reporting. This module handles the storage, updating, and retrieval of Scrum-related data including sprints, tasks, and burndown charts using JSON files as the data storage mechanism.

## Architecture Diagram

```mermaid
graph TD
    A[WorkflowDataCollector] --> B[__init__]
    A --> C[create_scrum_workflow_tables]
    A --> D[update_scrum_task]
    A --> E[update_scrum_burndown]
    A --> F[generate_scrum_report]
    A --> G[close]
    
    style A fill:#e1f5fe
    style C fill:#e8f5e8
    style D fill:#e8f5e8
    style E fill:#e8f5e8
    style F fill:#e8f5e8
```

## Module Structure

### Class Hierarchy

| Class | Description | Inheritance |
|-------|-------------|-------------|
| `WorkflowDataCollector` | Scrum workflow data management | - |

### Key Components

| Component | Type | Purpose |
|-----------|------|---------|
| `data_dir` | Configuration | Directory path for JSON file storage |
| `scrum_sprints_file` | Configuration | Path to Scrum sprints JSON file |
| `scrum_tasks_file` | Configuration | Path to Scrum tasks JSON file |
| `scrum_burndown_file` | Configuration | Path to Scrum burndown JSON file |

## Detailed Method Documentation

### WorkflowDataCollector Class

#### Constructor
```python
def __init__(self, data_dir='SystemInputs/user_inputs') -> None
```

**Purpose:** Initializes the WorkflowDataCollector with the specified data directory.

**Parameters:**
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `data_dir` | `str` | No | Directory path for JSON file storage | `'SystemInputs/user_inputs'` |

**File Paths Initialized:**
- `scrum_sprints_file`: `{data_dir}/scrum_sprints.json`
- `scrum_tasks_file`: `{data_dir}/scrum_tasks.json`
- `scrum_burndown_file`: `{data_dir}/scrum_burndown.json`

#### create_scrum_workflow_tables Method
```python
def create_scrum_workflow_tables(self) -> None
```

**Purpose:** Ensures all Scrum JSON files exist, creating them with empty arrays if they don't.

**Process:**
- Checks existence of each Scrum JSON file
- Creates file with empty JSON array `[]` if it doesn't exist
- Uses UTF-8 encoding for proper character handling

**Files Created:**
1. `scrum_sprints.json` - Sprint definitions and metadata
2. `scrum_tasks.json` - Task assignments and status
3. `scrum_burndown.json` - Burndown chart data

#### update_scrum_task Method
```python
