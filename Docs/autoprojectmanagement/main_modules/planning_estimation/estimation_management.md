# Estimation Management Module Documentation

*Last updated: 2025-08-14*

## Overview

The `estimation_management.py` module is a core component of the AutoProjectManagement system that provides comprehensive project estimation capabilities. This module handles task duration estimation based on complexity levels, cost estimation based on resources and duration, and project-level duration and cost aggregation. It supports multiple estimation methodologies including parametric estimation with configurable complexity mapping.

## Architecture Diagram

```mermaid
graph TD
    A[EstimationManagement] --> B[BaseManagement]
    B --> C[load_json]
    B --> D[save_json]
    B --> E[load_inputs]
    B --> F[validate_inputs]
    B --> G[run]
    A --> H[analyze]
    
    H --> I[Task Duration Estimation]
    H --> J[Task Cost Estimation]
    H --> K[Project Aggregation]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style H fill:#e8f5e8
```

## Module Structure

### Class Hierarchy

| Class | Description | Inheritance |
|-------|-------------|-------------|
| `BaseManagement` | Base class for file-based operations | - |
| `EstimationManagement` | Project estimation management | Inherits from `BaseManagement` |

### Key Components

| Component | Type | Purpose | Default Value |
|-----------|------|---------|---------------|
| `detailed_wbs_path` | Configuration | Path to detailed WBS JSON file | `project_inputs/PM_JSON/user_inputs/detailed_wbs.json` |
| `output_path` | Configuration | Path for estimation output | `project_inputs/PM_JSON/system_outputs/estimation_management.json` |
| `inputs` | Data Storage | Loaded input data | `{}` |
| `output` | Data Storage | Processed estimation results | `{}` |

