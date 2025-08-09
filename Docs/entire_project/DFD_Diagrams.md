# Data Flow Diagrams (DFD) - Auto Project Management System

This document provides Data Flow Diagrams (DFD) for the Auto Project Management System based on the actual implementation.

---

## Level 0 - Context Diagram

```mermaid
graph TD
    User[/"User (Developer/PM)"/]
    System[/"Auto Project Management System"/]
    GitHub[/"GitHub Repository"/]
    VSCode[/"VSCode Extension"/]
    
    User -->|Inputs and Commands| System
    System -->|Reports and Notifications| User
    System <-->|Push/Pull commits| GitHub
    System <-->|Commands and Data| VSCode
    
    style System fill:#f9f,stroke:#333,stroke-width:4px
```

---

## Level 1 - High-Level Processes

```mermaid
graph TD
    User[/"User"/]
    
    %% Main Processes
    CLI_Handler((CLI Command Handler))
    Task_Manager((Task Management))
    Progress_Tracker((Progress Tracking))
    Git_Automation((Git Automation))
    Report_Generator((Report Generator))
    Backup_Service((Backup Service))
    
    %% Databases
    Task_DB[(Task Database)]
    Progress_DB[(Progress Database)]
    Config_DB[(Configuration Database)]
    Commit_DB[(Commit History DB)]
    Backup_Storage[(Backup Storage)]
    
    %% Data Flows
    User -->|CLI Commands| CLI_Handler
    CLI_Handler --> Task_Manager
    CLI_Handler --> Progress_Tracker
    CLI_Handler --> Git_Automation
    
    Task_Manager --> Task_DB
    Progress_Tracker --> Progress_DB
    Git_Automation --> Commit_DB
    Git_Automation --> Backup_Service
    
    Backup_Service --> Backup_Storage
    Report_Generator --> Progress_DB
    Report_Generator --> Task_DB
    Report_Generator --> Commit_DB
    
    Report_Generator -->|Reports| User
```

---

## Level 2 - Task Management and Progress Tracking

```mermaid
graph TD
    User[/"User"/]
    
    %% Input Modules
    Input_Parser((Input Parser))
    Task_Validator((Task Validator))
    
    %% Processing Modules
    WBS_Parser((WBS Parser))
    Importance_Calc((Importance Calculator))
    Urgency_Calc((Urgency Calculator))
    Task_Scheduler((Task Scheduler))
    Progress_Calc((Progress Calculator))
    
    %% Output Modules
    Dashboard((Dashboard Generator))
    Report_Builder((Report Builder))
    
    %% Databases
    Raw_Tasks[(Raw Tasks)]
    Parsed_Tasks[(Parsed Tasks)]
    Calculated_Priority[(Priority Data)]
    Progress_Data[(Progress Data)]
    Reports[(Reports)]
    
    %% Data Flows
    User -->|Raw Input| Input_Parser
    Input_Parser --> Raw_Tasks
    Input_Parser --> Task_Validator
    
    Task_Validator -->|Validated Data| WBS_Parser
    WBS_Parser --> Parsed_Tasks
    
    Parsed_Tasks --> Importance_Calc
    Parsed_Tasks --> Urgency_Calc
    
    Importance_Calc --> Calculated_Priority
    Urgency_Calc --> Calculated_Priority
    
    Calculated_Priority --> Task_Scheduler
    Task_Scheduler --> Progress_Calc
    
    Progress_Calc --> Progress_Data
    Progress_Data --> Dashboard
    Progress_Data --> Report_Builder
    
    Dashboard -->|Live Dashboard| User
    Report_Builder -->|Reports| User
```

---

## Level 2 - Git Automation and Commit Management

```mermaid
graph TD
    Task_Scheduler((Task Scheduler))
    
    %% Git Modules
    Commit_Manager((Commit Manager))
    Message_Generator((Commit Message Generator))
    Git_CLI((Git CLI Interface))
    GitHub_API((GitHub API))
    
    %% Backup Modules
    Backup_Manager((Backup Manager))
    Progress_Sync((Progress Sync))
    
    %% Databases
    Commit_Tasks[(Commit Tasks)]
    Git_History[(Git History)]
    Local_Backup[(Local Backup)]
    Cloud_Backup[(Cloud Backup)]
    
    %% Data Flows
    Task_Scheduler -->|Ready Tasks| Commit_Manager
    Commit_Manager -->|Task Info| Message_Generator
    Message_Generator -->|Commit Message| Git_CLI
    
    Git_CLI -->|commit/push| GitHub_API
    Git_CLI -->|Logs| Git_History
    
    Commit_Manager -->|Backup Info| Backup_Manager
    Backup_Manager --> Local_Backup
    Backup_Manager --> Cloud_Backup
    
    Progress_Sync --> Git_History
    Progress_Sync --> Commit_Tasks
```

---

## Level 3 - Task Management Details

### 3.1 - Priority Calculation and Scheduling

```mermaid
graph TD
    Task_Input[(Task Input)]
    
    Priority_Engine((Priority Engine))
    Importance_Weight((Importance Weight))
    Urgency_Weight((Urgency Weight))
    Deadline_Check((Deadline Check))
    
    Task_Queue[(Priority Queue)]
    Scheduler((Scheduler))
    Resource_Allocator((Resource Allocator))
    
    Task_Input --> Priority_Engine
    Priority_Engine --> Importance_Weight
    Priority_Engine --> Urgency_Weight
    Priority_Engine --> Deadline_Check
    
    Importance_Weight --> Task_Queue
    Urgency_Weight --> Task_Queue
    Deadline_Check --> Task_Queue
    
    Task_Queue --> Scheduler
    Scheduler --> Resource_Allocator
```

### 3.2 - Progress Reporting

```mermaid
graph TD
    Progress_Data[(Progress Data)]
    
    Data_Aggregator((Data Aggregator))
    Progress_Analyzer((Progress Analyzer))
    Report_Formatter((Report Formatter))
    
    Markdown_Generator((Markdown Generator))
    JSON_Exporter((JSON Exporter))
    
    Progress_Data --> Data_Aggregator
    Data_Aggregator --> Progress_Analyzer
    Progress_Analyzer --> Report_Formatter
    
    Report_Formatter --> Markdown_Generator
    Report_Formatter --> JSON_Exporter
    
    Markdown_Generator -->|progress_report.md| User
    JSON_Exporter -->|commit_progress.json| System
```

### 3.3 - Commit Automation and Sync

```mermaid
graph TD
    Ready_Tasks[(Ready Tasks)]
    
    Commit_Prep((Commit Preparation))
    Staging_Area((Staging Area))
    Commit_Execute((Commit Execution))
    Push_Handler((Push Handler))
    
    Ready_Tasks --> Commit_Prep
    Commit_Prep --> Staging_Area
    Staging_Area --> Commit_Execute
    Commit_Execute --> Push_Handler
    
    Push_Handler -->|Push to GitHub| GitHub_API
    Push_Handler -->|Update local| Local_Repo
```

---

## Data Flows and Descriptions

| Data Flow Name       | Source           | Destination       | Description                      |
|----------------------|------------------|-------------------|---------------------------------|
| raw_task_input       | User             | Input_Parser      | Raw task input from user         |
| validated_tasks      | Task_Validator   | WBS_Parser        | Validated tasks                  |
| parsed_wbs           | WBS_Parser       | Task_Scheduler    | Parsed WBS structure             |
| priority_scores      | Priority_Calc    | Task_Queue        | Calculated priority scores       |
| scheduled_tasks      | Scheduler        | Progress_Calc     | Scheduled tasks                  |
| progress_updates     | Progress_Calc    | Report_Generator  | Progress updates                 |
| commit_messages      | Message_Generator| Git_CLI           | Generated commit messages        |
| git_operations       | Git_CLI          | GitHub_API        | Git operations (push/pull)       |
| backup_data          | Backup_Manager   | Cloud_Storage     | Backup data                     |
| reports              | Report_Generator | User              | Final reports                   |

---

## Databases and Storage

### 1. Task Database
- **Path**: `JSonDataBase/Inputs/UserInputs/`
- **Content**: Raw tasks input by user
- **Format**: JSON

### 2. Progress Database
- **Path**: `JSonDataBase/OutPuts/`
- **Content**: Calculated progress data
- **Files**: 
  - `commit_progress.json`
  - `commit_task_database.json`

---

This documentation now fully uses English language and accurately reflects the actual implementation of the Auto Project Management System.
