# Scope Management Module Documentation

*Last updated: 2025-08-14*

## Overview

The `scope_management.py` module is a core component of the AutoProjectManagement system that provides comprehensive scope change management capabilities. This module handles the complete lifecycle of scope management including loading WBS data, processing scope changes with impact analysis, generating detailed scope management reports, and maintaining audit trails for all scope modifications.

## Architecture Diagram

```mermaid
graph TD
    A[ScopeManagement] --> B[__init__]
    A --> C[load_json]
    A --> D[save_json]
    A --> E[load_inputs]
    A --> F[validate_scope_change]
    A --> G[apply_scope_changes]
    A --> H[_process_single_change]
    A --> I[_process_add_change]
    A --> J[_process_remove_change]
    A --> K[_process_modify_change]
    A --> L[find_task_by_id]
    A --> M[remove_task_by_id]
    A --> N[get_scope_summary]
    A --> O[run]
    
    G --> H
    H --> I
    H --> J
    H --> K
    I --> L
    J --> M
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style G fill:#e8f5e8
```

## Module Structure

### Class Hierarchy

| Class | Description | Inheritance |
|-------|-------------|-------------|
| `ScopeManagementError` | Base exception for scope management errors | `Exception` |
| `InvalidScopeChangeError` | Raised when invalid scope change is detected | `ScopeManagementError` |
| `FileNotFoundError` | Raised when required files are not found | `ScopeManagementError` |
| `ScopeManagement` | Comprehensive scope management system | - |

### Key Components

| Component | Type | Purpose | Default Value |
|-----------|------|---------|---------------|
| `detailed_wbs_path` | Configuration | Path to detailed WBS JSON file | `JSonDataBase/Inputs/UserInputs/detailed_wbs.json` |
| `scope_changes_path` | Configuration | Path to scope changes JSON file | `JSonDataBase/Inputs/UserInputs/scope_changes.json` |
