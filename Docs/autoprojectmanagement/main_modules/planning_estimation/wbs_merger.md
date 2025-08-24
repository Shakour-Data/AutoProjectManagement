# WBS Merger Module Documentation

*Last updated: 2025-08-14*

## Overview

The `wbs_merger.py` module is a core component of the AutoProjectManagement system that merges multiple Work Breakdown Structure (WBS) parts into a single detailed WBS. This module handles the merging of tasks, subtasks, and their relationships, ensuring that all components are integrated into a unified project structure.

## Architecture Diagram

```mermaid
graph TD
    A[WBSMerger] --> B[__init__]
    A --> C[load_part]
