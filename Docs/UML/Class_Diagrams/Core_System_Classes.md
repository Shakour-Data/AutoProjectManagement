# Core System Classes Documentation

## Overview

This document provides comprehensive documentation for the core system classes in the AutoProjectManagement system. It includes detailed class descriptions, relationships, diagrams, and visual representations using Mermaid diagrams.

## Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Core System Classes](#core-system-classes)
3. [Class Relationships](#class-relationships)
4. [Detailed Class Descriptions](#detailed-class-descriptions)
5. [Data Models](#data-models)
6. [Sequence Diagrams](#sequence-diagrams)
7. [State Diagrams](#state-diagrams)
8. [Tables and Specifications](#tables-and-specifications)

---

## System Architecture Overview

The AutoProjectManagement system is built around a modular architecture with the following core components:

```mermaid
graph TB
    subgraph "AutoProjectManagement System"
        PMS[ProjectManagementSystem]
        TM[TaskManagement]
        EM[EstimationManagement]
        RM[ResourceManagement]
        CM[CommunicationManagement]
        PM[PlanningManagement]
    end
    
    PMS --> TM
    PMS --> EM
    PMS --> RM
    PMS --> CM
    PMS --> PM
    
    TM --> EM
    TM --> RM
    EM --> PM
    RM --> PM
```

---

## Core System Classes

### 1. ProjectManagementSystem

The central orchestrator class that manages all project-related operations.

```mermaid
classDiagram
    class ProjectManagementSystem {
        -projects: Dict[int, Dict[str, Any]]
        -tasks: Dict[int, Dict[int, Dict[str, Any]]]
        -is_initialized: bool
        +initialize_system(config: Optional[Dict[str, Any]]) -> bool
        +shutdown_system() -> bool
        +reset_system() -> bool
        +add_project(project: Dict[str, Any]) -> bool
        +remove_project(project_id: int) -> bool
        +update_project(project: Dict[str, Any]) -> bool
        +get_project(project_id: int) -> Optional[Dict[str, Any]]
        +list_projects() -> List[Dict[str, Any]]
        +add_task_to_project(project_id: int, task: Dict[str, Any]) -> bool
        +remove_task_from_project(project_id: int, task_id: int) -> bool
        +update_task_in_project(project_id: int, task: Dict[str, Any]) -> bool
        +get_task_from_project(project_id: int, task_id: int) -> Optional[Dict[str, Any]]
        +list_tasks_in_project(project_id: int) -> List[Dict[str, Any]]
    }
```

### 2. TaskManagement

Comprehensive task management with workflow tracking and GitHub integration.

```mermaid
classDiagram
    class Task {
        -id: int
        -title: str
        -description: str
        -deadline: Optional[datetime.date]
        -dependencies: List[int]
        -assigned_to: List[str]
        -status: str
        -priority: int
        -parent_id: Optional[int]
        -urgency: Optional[float]
        -importance: Optional[float]
        -github_issue_number: Optional[int]
        -workflow_steps: Dict[str, bool]
        +mark_workflow_step_completed(step_name: str) -> bool
        +workflow_progress_percentage() -> float
        +is_workflow_completed() -> bool
        +to_dict() -> Dict[str, Any]
    }

    class TaskManagement {
        -tasks: Dict[int, Task]
        -next_task_id: int
        +create_task(title: str, description: str = "", ...) -> Task
        +update_workflow_steps_from_commit_message(commit_message: str) -> None
        +parse_creative_input(input_text: str) -> Task
        +generate_wbs_from_idea(input_text: str, max_depth: int = 5) -> List[Task]
        +load_scores(scores_path: str) -> None
        +calculate_urgency_importance() -> None
        +classify_tasks_eisenhower() -> Dict[str, List[Task]]
        +prioritize_tasks() -> List[Task]
        +schedule_tasks() -> List[Task]
        +detect_conflicts() -> List[str]
        +assign_task(task_id: int, users: List[str]) -> bool
        +mark_task_completed(task_id: int) -> bool
        +export_tasks(export_path: str) -> None
        +import_tasks(import_path: str) -> None
    }
```

### 3. EstimationManagement

Project estimation with advanced methodologies including COCOMO II and parametric estimation.

```mermaid
classDiagram
    class EstimationManagement {
        -input_paths: Dict[str, str]
        -output_path: str
        -inputs: Dict[str, Any]
        -output: Dict[str, Any]
        +__init__(detailed_wbs_path: str, output_path: str)
        +load_json(path: str) -> Optional[Dict[str, Any]]
        +save_json(data: Dict[str, Any], path: str) -> None
        +load_inputs() -> None
        +analyze() -> None
        +run() -> None
        +estimate_task_duration(task: Dict[str, Any]) -> float
        +estimate_task_cost(task: Dict[str, Any]) -> float
        +estimate_project_duration(project: Dict[str, Any]) -> float
        +estimate_project_cost(project: Dict[str, Any]) -> float
    }
```

### 4. ResourceManagement

Comprehensive resource allocation and optimization.

```mermaid
classDiagram
    class ResourceManagement {
        -input_paths: Dict[str, str]
        -output_path: str
        -inputs: Dict[str, Any]
        -output: Dict[str, Any]
        +__init__(resource_allocation_path: str, output_path: str)
        +load_json(path: str) -> Optional[Dict[str, Any]]
        +save_json(data: Dict[str, Any], path: str) -> None
        +load_inputs() -> None
        +analyze() -> None
        +run() -> None
        +analyze_resource_utilization(resource_data: Dict[str, Any]) -> Dict[str, Any]
        +resolve_conflicts(resource_data: Dict[str, Any]) -> Dict[str, Any]
        +generate_recommendations(plan: Dict[str, Any], utilization: Dict[str, Any], conflicts: Dict[str, Any]) -> List[Dict[str, Any]]
    }
```

### 5. CommunicationManagement

Communication tracking and effectiveness analysis.

```mermaid
classDiagram
    class CommunicationManagement {
        -input_paths: Dict[str, str]
        -output_path: str
        -inputs: Dict[str, Any]
        -output: Dict[str, Any]
        +__init__(communication_plan_path: str, communication_logs_path: str, output_path: str)
        +load_json(path: str) -> Optional[Dict[str, Any]]
        +save_json(data: Dict[str, Any], path: str) -> None
        +load_inputs() -> None
        +analyze() -> None
        +run() -> None
        +_validate_communication_plan(plan: Dict[str, Any]) -> Dict[str, Any]
        +_analyze_communication_logs(logs: Dict[str, Any]) -> Dict[str, Any]
        +_calculate_effectiveness(plan: Dict[str, Any], logs: Dict[str, Any]) -> Dict[str, Any]
        +_generate_recommendations(plan_validation: Dict[str, Any], log_analysis: Dict[str, Any], effectiveness: Dict[str, Any]) -> List[str]
    }
```

---

## Class Relationships

### Inheritance Hierarchy

```mermaid
classDiagram
    class BaseManagement {
        +load_json(path: str) -> Optional[Dict[str, Any]]
        +save_json(data: Dict[str, Any], path: str) -> None
        +load_inputs() -> None
        +analyze() -> None
        +run() -> None
    }

    class ProjectManagementSystem {
        +initialize_system(config: Optional[Dict[str, Any]]) -> bool
        +add_project(project: Dict[str, Any]) -> bool
        +add_task_to_project(project_id: int, task: Dict[str, Any]) -> bool
    }

    class TaskManagement {
        +create_task(title: str, description: str = "", ...) -> Task
        +classify_tasks_eisenhower() -> Dict[str, List[Task]]
    }

    class EstimationManagement {
        +estimate_task_duration(task: Dict[str, Any]) -> float
        +estimate_project_cost(project: Dict[str, Any]) -> float
    }

    class ResourceManagement {
        +analyze_resource_utilization(resource_data: Dict[str, Any]) -> Dict[str, Any]
    }

    class CommunicationManagement {
        +_validate_communication_plan(plan: Dict[str, Any]) -> Dict[str, Any]
    }

    BaseManagement <|-- EstimationManagement
    BaseManagement <|-- ResourceManagement
    BaseManagement <|-- CommunicationManagement
```

### Composition Relationships

```mermaid
classDiagram
    class ProjectManagementSystem {
        -projects: Dict[int, Dict[str, Any]]
        -tasks: Dict[int, Dict[int, Dict[str, Any]]]
    }

    class TaskManagement {
        -tasks: Dict[int, Task]
    }

    class Task {
        -id: int
        -title: str
        -description: str
    }

    ProjectManagementSystem *-- TaskManagement
    TaskManagement *-- Task
```

---

## Detailed Class Descriptions

### ProjectManagementSystem Class

**Purpose**: Central orchestrator for all project management operations.

**Key Features**:

- Project lifecycle management

- Task management with workflow tracking

- Resource allocation

- Progress monitoring

- Data integrity maintenance

**Methods**:

- `initialize_system()`: System initialization

- `add_project()`: Add new project

- `add_task_to_project()`: Add task to project

- `list_projects()`: List all projects

- `list_tasks_in_project()`: List tasks in project

### TaskManagement Class

**Purpose**: Comprehensive task management with workflow tracking and GitHub integration.

**Key Features**:

- Task lifecycle management

- Workflow step tracking

- GitHub integration via commit message parsing

- Eisenhower matrix classification

- Task prioritization and scheduling

**Methods**:

- `create_task()`: Create new task

- `classify_tasks_eisenhower()`: Classify tasks using Eisenhower matrix

- `prioritize_tasks()`: Prioritize tasks

- `schedule_tasks()`: Schedule tasks

### EstimationManagement Class

**Purpose**: Project estimation with advanced methodologies.

**Key Features**:

- Task duration estimation

- Cost estimation

- Project-level estimation

- Multiple estimation methodologies (COCOMO II, parametric)

**Methods**:
- `estimate_task_duration()`: Estimate task duration
- `estimate_task_cost()`: Estimate task cost
- `estimate_project_duration()`: Estimate project duration
- `estimate_project_cost()`: Estimate project cost

### ResourceManagement Class

**Purpose**: Comprehensive resource allocation and optimization.

**Key Features**:

- Resource allocation analysis

- Resource leveling optimization

- Utilization tracking

- Conflict detection and resolution

**Methods**:

- `analyze_resource_utilization()`: Analyze resource utilization

- `resolve_conflicts()`: Resolve conflicts

- `generate_recommendations()`: Generate recommendations

### CommunicationManagement Class

**Purpose**: Communication tracking and effectiveness analysis.

**Key Features**:

- Communication plan validation

- Log analysis

- Effectiveness metrics

- Gap identification

**Methods**:

- `_validate_communication_plan()`: Validate communication plan

- `_analyze_communication_logs()`: Analyze communication logs

- `_calculate_effectiveness()`: Calculate effectiveness

---

## Data Models

### Project Data Model

```mermaid
erDiagram
    Project {
        int id
        string name
        string description
        datetime start_date
        datetime end_date
        string status
        float budget
        string priority
    }
    
    Task {
        int id
        string title
        string description
        datetime deadline
        int priority
        string status
        int project_id
        List[int] dependencies
    }
    
    Resource {
        int id
        string name
        string type
        int capacity
        float cost_per_hour
    }
    
    Communication {
        int id
        string type
        string stakeholder
        string message
        datetime timestamp
        string status
    }
    
    Project ||--o{ Task : contains
    Project ||--o{ Resource : uses
    Project ||--o{ Communication : has
```

### Task Workflow Model

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> InProgress
    InProgress --> Completed
    InProgress --> Blocked
    Blocked --> InProgress
    Completed --> [*]
    
    state Pending {
        [*] --> Ready
        Ready --> Assigned
    }
    
    state InProgress {
        [*] --> Coding
        Coding --> Testing
        Testing --> Review
        Review --> Documentation
        Documentation --> Deployment
    }
```

---

## Sequence Diagrams

### Project Creation Flow

```mermaid
sequenceDiagram
    participant User
    participant PMS as ProjectManagementSystem
    participant TM as TaskManagement
    participant EM as EstimationManagement
    
    User->>PMS: initialize_system()
    PMS->>PMS: initialize data structures
    PMS-->>User: system initialized
    
    User->>PMS: add_project(project_data)
    PMS->>PMS: validate project data
    PMS->>PMS: add project to system
    PMS-->>User: project added
    
    User->>PMS: add_task_to_project(project_id, task_data)
    PMS->>TM: create_task(task_data)
    TM->>TM: validate task data
    TM->>TM: add task to project
    TM-->>PMS: task added
    
    PMS->>EM: estimate_task_duration(task_data)
    EM->>EM: calculate duration
    EM-->>PMS: duration estimated
    
    PMS-->>User: task added with estimation
```

### Task Workflow Execution

```mermaid
sequenceDiagram
    participant User
    participant TM as TaskManagement
    participant GitHub
    participant Workflow
    
    User->>TM: create_task("Implement feature", ...)
    TM->>TM: create task object
    TM-->>User: task created
    
    User->>TM: mark_workflow_step_completed("Code Review")
    TM->>Workflow: update workflow step
    Workflow-->>TM: step updated
    
    TM->>GitHub: update_workflow_steps_from_commit_message(commit_message)
    GitHub-->>TM: workflow updated
    
    TM-->>User: workflow progress updated
```

---

## State Diagrams

### Task Lifecycle States

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> InProgress : start
    InProgress --> Completed : complete
    InProgress --> Blocked : blocked
    Blocked --> InProgress : resolved
    Completed --> [*]
    
    state Pending {
        [*] --> Ready
        Ready --> Assigned
    }
    
    state InProgress {
        [*] --> Coding
        Coding --> Testing
        Testing --> Review
        Review --> Documentation
        Documentation --> Deployment
    }
```

### Resource Allocation States

```mermaid
stateDiagram-v2
    [*] --> Available
    Available --> Allocated : allocate
    Allocated --> InUse : use
    InUse --> Available : release
    Available --> Reserved : reserve
    Reserved --> InUse : activate
```

---

## Tables and Specifications

### Core System Classes Table

| Class Name | Purpose | Key Methods | Relationships |
|------------|---------|-------------|---------------|
| ProjectManagementSystem | Central orchestrator | initialize_system, add_project, add_task_to_project | Contains TaskManagement |
| TaskManagement | Task lifecycle management | create_task, classify_tasks_eisenhower, prioritize_tasks | Uses Task objects |
| EstimationManagement | Project estimation | estimate_task_duration, estimate_project_cost | Extends BaseManagement |
| ResourceManagement | Resource allocation | analyze_resource_utilization, resolve_conflicts | Extends BaseManagement |
| CommunicationManagement | Communication tracking | _validate_communication_plan, _analyze_communication_logs | Extends BaseManagement |

### Task Attributes Table

| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| id | int | Unique task identifier | Yes |
| title | str | Task title | Yes |
| description | str | Task description | No |
| deadline | datetime | Task deadline | No |
| priority | int | Task priority (0-100) | No |
| status | str | Task status | Yes |
| dependencies | List[int] | Task dependencies | No |
| assigned_to | List[str] | Assigned users | No |

### Resource Attributes Table

| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| id | int | Unique resource identifier | Yes |
| name | str | Resource name | Yes |
| type | str | Resource type | Yes |
| capacity | int | Resource capacity | Yes |
| cost_per_hour | float | Cost per hour | Yes |

### Communication Attributes Table

| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| id | int | Unique communication identifier | Yes |
| type | str | Communication type | Yes |
| stakeholder | str | Target stakeholder | Yes |
| message | str | Communication message | Yes |
| timestamp | datetime | Communication timestamp | Yes |
| status | str | Communication status | Yes |

---

## Configuration Tables

### System Configuration

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| DEFAULT_PROJECT_FIELDS | {"id", "name"} | Default project fields |
| REQUIRED_TASK_FIELDS | {"id", "title"} | Required task fields |
| MAX_PROJECT_NAME_LENGTH | 100 | Maximum project name length |
| MAX_TASK_TITLE_LENGTH | 200 | Maximum task title length |
| DEFAULT_COST_PER_RESOURCE | 100.0 | Default cost per resource unit |

### Estimation Configuration

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| DEFAULT_COMPLEXITY_MAPPING | {"low": 1.0, "medium": 3.0, "high": 5.0, "extreme": 8.0} | Complexity mapping for estimation |
| ESTIMATION_METHODS | {"PARAMETRIC": "parametric", "COCOMO_II": "cocomo_ii", "AGILE": "agile"} | Available estimation methods |

---

## Conclusion

This documentation provides a comprehensive overview of the core system classes in the AutoProjectManagement system. The modular architecture allows for flexible project management with specialized components for different aspects of project management including task management, resource allocation, estimation, and communication tracking.

All classes are designed to work together seamlessly, providing a complete project management solution with advanced features like workflow tracking, GitHub integration, and comprehensive estimation methodologies.
