# Data Flow Diagrams (DFD) - AutoProjectManagement System

## Overview
This document provides comprehensive Data Flow Diagrams for the AutoProjectManagement system, illustrating how data moves through various components and modules based on the actual implementation.

## Table of Contents
1. [Context Diagram (Level 0)](#context-diagram-level-0)
2. [Level 1 DFD - System Overview](#level-1-dfd-system-overview)
3. [Level 2 DFD - Core Modules](#level-2-dfd-core-modules)
4. [Level 3 DFD - Detailed Module Flows](#level-3-dfd-detailed-module-flows)
5. [Data Stores](#data-stores)
6. [Data Flow Descriptions](#data-flow-descriptions)

---

## Context Diagram (Level 0)

```mermaid
graph TD
    Developer[/"Developer/Project Manager"/]
    System[/"AutoProjectManagement System"/]
    GitHub[/"GitHub Repository"/]
    VSCode[/"VSCode Extension"/]
    Wiki[/"Wiki Documentation"/]
    Backup[/"Backup System"/]
    
    Developer -->|Task Input & Commands| System
    System -->|Progress Reports & Status| Developer
    System <-->|Push/Pull Commits| GitHub
    System <-->|Real-time Updates| VSCode
    System <-->|Documentation Sync| Wiki
    System -->|Backup Data| Backup
    
    style System fill:#f9f,stroke:#333,stroke-width:4px
```

---

## Level 1 DFD - System Overview

### Major Processes
| Process ID | Process Name | Description |
|------------|--------------|-------------|
| P1 | **CLI Interface** | Command-line interface for user interaction |
| P2 | **Project Management Core** | Central orchestrator managing all project activities |
| P3 | **Data Collection & Processing** | Collects and processes project data from various sources |
| P4 | **Planning & Estimation** | Creates project plans, schedules, and estimates |
| P5 | **Task & Workflow Management** | Manages task execution and workflow automation |
| P6 | **Progress Reporting** | Generates progress reports and dashboards |
| P7 | **Quality & Commit Management** | Handles code quality and automated commits |
| P8 | **Resource Management** | Manages resource allocation and leveling |
| P9 | **Communication & Risk** | Handles communication and risk management |
| P10 | **Backup & Recovery** | Manages system backups and recovery |

```mermaid
graph TD
    User[/"User"/]
    
    P1[("CLI Interface")]
    P2[("Project Management Core")]
    P3[("Data Collection & Processing")]
    P4[("Planning & Estimation")]
    P5[("Task & Workflow Management")]
    P6[("Progress Reporting")]
    P7[("Quality & Commit Management")]
    P8[("Resource Management")]
    P9[("Communication & Risk")]
    P10[("Backup & Recovery")]
    
    DS1[(Task Database)]
    DS2[(Progress Database)]
    DS3[(Configuration Database)]
    DS4[(Commit History)]
    DS5[(Backup Storage)]
    
    User -->|CLI Commands| P1
    P1 --> P2
    P2 --> P3
    P2 --> P4
    P2 --> P5
    P2 --> P6
    P2 --> P7
    P2 --> P8
    P2 --> P9
    P2 --> P10
    
    P3 --> DS1
    P4 --> DS1
    P5 --> DS2
    P6 --> DS2
    P7 --> DS4
    P8 --> DS1
    P9 --> DS2
    P10 --> DS5
```

---

## Level 2 DFD - Core Modules

### 2.1 - Data Collection & Processing
```mermaid
graph TD
    subgraph "Data Collection & Processing"
        Input_Handler[("Input Handler")]
        Workflow_Collector[("Workflow Data Collector")]
        Progress_Generator[("Progress Data Generator")]
        
        Raw_Input[(Raw Input)]
        Processed_Data[(Processed Data)]
        Progress_Data[(Progress Data)]
        
        CLI_Input[/"CLI Input"/] --> Input_Handler
        JSON_Input[/"JSON Files"/] --> Input_Handler
        Git_Data[/"Git Data"/] --> Workflow_Collector
        
        Input_Handler --> Raw_Input
        Workflow_Collector --> Processed_Data
        Raw_Input --> Progress_Generator
        Processed_Data --> Progress_Generator
        Progress_Generator --> Progress_Data
    end
```

### 2.2 - Task & Workflow Management
```mermaid
graph TD
    subgraph "Task & Workflow Management"
        Task_Management[("Task Management")]
        Importance_Calc[("Importance Calculator")]
        Urgency_Calc[("Urgency Calculator")]
        Task_Executor[("Task Executor")]
        
        Task_Queue[(Task Queue)]
        Priority_Data[(Priority Data)]
        
        Scheduled_Tasks[/"Scheduled Tasks"/] --> Task_Management
        Task_Management --> Importance_Calc
        Task_Management --> Urgency_Calc
        Importance_Calc --> Priority_Data
        Urgency_Calc --> Priority_Data
        Priority_Data --> Task_Executor
        Task_Executor --> Task_Queue
    end
```

### 2.3 - Git Automation & Commit Management
```mermaid
graph TD
    subgraph "Git Automation & Commit Management"
        Commit_Manager[("Commit Manager")]
        Message_Generator[("Commit Message Generator")]
        Quality_Checker[("Quality Checker")]
        Git_Progress[("Git Progress Updater")]
        
        Ready_Commits[(Ready Commits)]
        Git_History[(Git History)]
        
        Completed_Tasks[/"Completed Tasks"/] --> Commit_Manager
        Commit_Manager --> Quality_Checker
        Quality_Checker -->|Pass/Fail| Commit_Manager
        Commit_Manager --> Message_Generator
        Message_Generator --> Git_Progress
        Git_Progress --> Git_History
        Git_Progress -->|"Push to GitHub"| GitHub[/"GitHub"/]
    end
```

---

## Level 3 DFD - Detailed Module Flows

### 3.1 - Progress Reporting
```mermaid
graph TD
    subgraph "Progress Reporting"
        Data_Aggregator[("Data Aggregator")]
        Progress_Analyzer[("Progress Analyzer")]
        Report_Formatter[("Report Formatter")]
        
        Progress_Data[(Progress Data)]
        Reports[(Reports)]
        
        Task_Progress[/"Task Progress"/] --> Data_Aggregator
        Commit_Data[/"Commit Data"/] --> Data_Aggregator
        Data_Aggregator --> Progress_Data
        Progress_Data --> Progress_Analyzer
        Progress_Analyzer --> Report_Formatter
        Report_Formatter --> Reports
        Reports -->|"progress_report.md"| User[/"User"/]
    end
```

### 3.2 - Resource Management
```mermaid
graph TD
    subgraph "Resource Management"
        Resource_Allocator[("Resource Allocator")]
        Resource_Leveling[("Resource Leveling")]
        
        Resource_Requests[(Resource Requests)]
        Allocated_Resources[(Allocated Resources)]
        
        Task_Requirements[/"Task Requirements"/] --> Resource_Allocator
        Resource_Availability[/"Resource Availability"/] --> Resource_Allocator
        Resource_Allocator --> Resource_Requests
        Resource_Requests --> Resource_Leveling
        Resource_Leveling --> Allocated_Resources
    end
```

---

## Data Stores

### Primary Data Stores
| Data Store | Location | Description | Format |
|------------|----------|-------------|---------|
| **Task Database** | `JSonDataBase/Inputs/UserInputs/` | User-defined tasks and configurations | JSON |
| **Progress Database** | `JSonDataBase/OutPuts/` | Calculated progress and status data | JSON |
| **Configuration Database** | `autoproject_configuration.py` | System configuration parameters | Python |
| **Commit History** | `.git/` directory | Git commit history and metadata | Git |
| **Backup Storage** | `backups/` | System backups and archives | ZIP/JSON |

### Data Store Schemas

#### Task Database Schema
```json
{
  "task_id": "string",
  "task_name": "string",
  "description": "string",
  "priority": "integer",
  "urgency": "integer",
  "importance": "integer",
  "estimated_hours": "float",
  "actual_hours": "float",
  "status": "string",
  "dependencies": ["task_id"],
  "assigned_resources": ["resource_id"],
  "due_date": "date"
}
```

#### Progress Database Schema
```json
{
  "progress_id": "string",
  "task_id": "string",
  "completion_percentage": "float",
  "hours_spent": "float",
  "status": "string",
  "last_updated": "datetime"
}
```

---

## Data Flow Descriptions

### Primary Data Flows

| Flow ID | Flow Name | Source | Destination | Data Elements | Frequency |
|---------|-----------|--------|-------------|---------------|-----------|
| F1 | Task Input | CLI Interface | Task Management | Raw task data, commands | On-demand |
| F2 | Validated Tasks | Task Validator | WBS Parser | Validated task objects | Real-time |
| F3 | WBS Structure | WBS Parser | Scheduler | Hierarchical task structure | On task creation |
| F4 | Progress Update | Task Executor | Progress Reporting | Task completion data | Continuous |
| F5 | Commit Data | Commit Manager | Git History | Commit information | On task completion |
| F6 | Backup Request | System Monitor | Backup Manager | Backup trigger | Scheduled |
| F7 | Resource Allocation | Resource Allocator | Task System | Resource assignments | On task scheduling |

### Implementation Mapping
- **CLI Interface**: `autoprojectmanagement/cli.py`
- **Project Management Core**: `autoprojectmanagement/main_modules/project_management_system.py`
- **Data Collection**: `autoprojectmanagement/main_modules/data_collection_processing/`
- **Task Management**: `autoprojectmanagement/main_modules/task_workflow_management/`
- **Progress Reporting**: `autoprojectmanagement/main_modules/progress_reporting/`
- **Quality Management**: `autoprojectmanagement/main_modules/quality_commit_management/`
- **Resource Management**: `autoprojectmanagement/main_modules/resource_management/`
- **Backup System**: `autoprojectmanagement/services/automation_services/backup_manager.py`

---

This document provides a complete and accurate representation of the AutoProjectManagement system's data flow based on the actual implementation.
