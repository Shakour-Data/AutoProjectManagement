# UML Diagrams

## Class Diagram

```mermaid
classDiagram
    class Project {
        - id: int
        - name: string
        - description: string
        - start_date: date
        - end_date: date
    }
    class Task {
        - id: int
        - name: string
        - description: string
        - status: string
        - priority: int
        - due_date: date
    }
    class SubTask {
        - id: int
        - name: string
        - status: string
    }
    class Resource {
        - id: int
        - name: string
        - role: string
    }
    class Allocation {
        - id: int
        - resource_id: int
        - task_id: int
        - allocation_percent: int
    }

    Project "1" -- "0..*" Task : contains
    Task "1" -- "0..*" SubTask : contains
    Resource "1" -- "0..*" Allocation : allocated to
    Task "1" -- "0..*" Allocation : has
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant BackendAPI
    participant Database

    User ->> Frontend: Fill task form and submit
    Frontend ->> BackendAPI: POST /tasks
    BackendAPI ->> Database: Insert new task record
    BackendAPI ->> Frontend: Return success response
    Frontend ->> User: Display confirmation message
```

## Component Diagram

```mermaid
graph TD
    Frontend --> BackendAPI
    BackendAPI --> Database
    InstallerGUI --> EnvironmentSetupScripts
    BackendAPI --> ServicesLayer
    ServicesLayer --> RepositoriesLayer
```

## Additional UML Diagrams

### Activity Diagram for Task Creation

```mermaid
graph TD
    User --> FillTaskForm
    FillTaskForm --> Submit
    Submit --> BackendAPI
    BackendAPI --> Validate
    Validate --> StoreInDatabase
    StoreInDatabase --> ReturnResponse
    ReturnResponse --> UserConfirmation
```

### State Diagram for Task Status

```mermaid
stateDiagram-v2
    [*] --> New
    New --> InProgress: When work starts
    InProgress --> Completed: When task is done
    Completed --> Archived: When task is archived
