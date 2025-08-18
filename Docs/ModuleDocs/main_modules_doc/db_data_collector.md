# DB Data Collector Module

## Overview
The `db_data_collector` module provides the `DBDataCollector` class to collect and store various project management data such as tasks, resource allocation, progress metrics, and feature weights into JSON files.

## Class: DBDataCollector

### Description
The `DBDataCollector` class manages data collection and storage for project management inputs and metrics. It writes collected data to JSON files in a specified data directory.

### Methods

- `__init__(self, data_dir='SystemInputs/user_inputs')`
  - Initializes file paths for tasks, resource allocation, progress metrics, and feature weights JSON files.

- `collect_and_store_tasks(self, tasks)`
  - Collects task data including progress and resource allocation, and stores it in a JSON file.

- `collect_resource_allocation(self, tasks)`
  - Analyzes resource allocation from tasks and stores a summary in a JSON file.

- `collect_progress_metrics(self, tasks)`
  - Collects progress percentages for tasks and stores or updates them in a JSON file.

- `insert_feature_weights(self, urgency_weights, importance_weights)`
  - Inserts predefined weights for urgency and importance features into a JSON file.

- `close(self)`
  - Placeholder method for cleanup if needed.

## Usage
The class is used to collect and persist project management data for further processing and analysis.

## Diagrams

### Mermaid Class Diagram

```mermaid
classDiagram
    class DBDataCollector {
        - data_dir: str
        - tasks_file: str
        - resource_allocation_file: str
        - progress_metrics_file: str
        - feature_weights_file: str
        + __init__(data_dir)
        + collect_and_store_tasks(tasks)
        + collect_resource_allocation(tasks)
        + collect_progress_metrics(tasks)
        + insert_feature_weights(urgency_weights, importance_weights)
        + close()
    }
```

### Mermaid Data Collection Flowchart

```mermaid
flowchart TD
    Start --> CollectTasks[Collect and store tasks data]
    CollectTasks --> CollectResource[Collect resource allocation]
    CollectResource --> CollectProgress[Collect progress metrics]
    CollectProgress --> InsertWeights[Insert feature weights]
    InsertWeights --> End
```

---

## Credits

This module uses Python's built-in `json` and `os` modules for file handling and data processing.

---

This documentation provides a detailed overview of the `db_data_collector` module to assist developers in understanding and using its functionality effectively.
