# WBS Parser Module Documentation

*Last updated: 2025-08-14*

## Overview

The `wbs_parser.py` module is a core component of the AutoProjectManagement system that parses different Work Breakdown Structure (WBS) formats into structured data. This module supports both JSON and text formats, validates WBS structure integrity, and provides utilities for extracting detailed task information and hierarchy.

## Architecture Diagram

```mermaid
graph TD
    A[WBSParser] --> B[__init__]
    A --> C[parse_json_wbs]
    A --> D[parse_text_wbs]
    A --> E[_validate_wbs_structure]
    A --> F[_parse_text_lines]
    A --> G[extract_task_details]
    A --> H[validate_wbs_integrity]
    A --> I[get_task_hierarchy]
    
    C --> E
    D --> F
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#e8f5e8
```

## Module Structure

### Class Hierarchy

| Class | Description | Inheritance |
|-------|-------------|-------------|
