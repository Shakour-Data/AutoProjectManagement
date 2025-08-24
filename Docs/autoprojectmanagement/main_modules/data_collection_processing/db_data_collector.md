# Database Data Collector Module Documentation

*Last updated: 2025-08-14*

## Overview

The `db_data_collector.py` module is a core component of the AutoProjectManagement system that provides comprehensive data collection and storage capabilities for project management data. This module handles the collection, validation, serialization, and storage of various project data types including tasks, resource allocation, progress metrics, and feature weights.

## Architecture Diagram

```mermaid
graph TD
    A[DBDataCollector] --> B[__init__]
    A --> C[_ensure_directory_exists]
    A --> D[_validate_tasks]
    A --> E[_write_json_file]
    A --> F[collect_and_store_tasks]
    A --> G[collect_resource_allocation]
    A --> H[collect_progress_metrics]
    A --> I[insert_feature_weights]
    A --> J[get_collected_data]
    A --> K[close]
    A --> L[__enter__]
    A --> M[__exit__]
    
    F --> D
    F --> E
    G --> D
    G --> E
    H --> D
    H --> E
    I --> E
    J --> E
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style F fill:#e8f5e8
    style G fill:#e8f5e8
    style H fill:#e8f5e8
