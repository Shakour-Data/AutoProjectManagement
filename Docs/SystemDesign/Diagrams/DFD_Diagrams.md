# DFD (Data Flow Diagrams)

## Level 0: Context Diagram

```mermaid
flowchart TD
    External[External Systems<br/>GitHub, VS Code] --> AutoProjectManagement[AutoProjectManagement System]
    AutoProjectManagement --> External
    
    Users[Users<br/>Developers, Managers] --> AutoProjectManagement
    AutoProjectManagement --> Users
    
    DataStores[Data Stores<br/>JSON Databases, Files] --> AutoProjectManagement

User -> Frontend : Interacts
Frontend -> Backend : Sends requests
Backend -> Database : Queries/Updates
Database -> Backend : Returns data
Backend -> Reports : Generates reports
Reports -> User : Displays reports
@enduml
```

## Level 1 DFD

The Level 1 DFD breaks down the Backend processes:

```plantuml
@startuml
rectangle "Task Management" as TaskMgmt
rectangle "Resource Allocation" as ResourceAlloc
rectangle "Progress Tracking" as ProgressTrack
rectangle "Reporting" as Reporting

TaskMgmt --> ResourceAlloc
ResourceAlloc --> ProgressTrack
ProgressTrack --> Reporting
@enduml
```

(Data stores: Project Database, Task Database, Resource Database)

## Detailed DFDs

### Task Management Process

```plantuml
@startuml
actor User
participant Frontend
participant Backend_API
participant TaskDB

User -> Frontend : Submit task data
Frontend -> Backend_API : Send task data
Backend_API -> TaskDB : Validate and store task
Backend_API -> Frontend : Confirm task creation
@enduml
```

### Resource Allocation Process

```plantuml
@startuml
actor User
participant Frontend
participant Backend_API
participant ResourceDB

User -> Frontend : Submit resource allocation
Frontend -> Backend_API : Send allocation data
Backend_API -> ResourceDB : Validate and update allocation
Backend_API -> Frontend : Confirm allocation update
@enduml
```

### Progress Tracking Process

```plantuml
@startuml
participant Backend_API
participant TaskDB
participant Reporting

Backend_API -> TaskDB : Retrieve task status
Backend_API -> Reporting : Update progress reports
@enduml
```

### Reporting Process

```plantuml
@startuml
participant Reporting
participant Frontend

Reporting -> Frontend : Provide reports data
@enduml
```

(To be expanded with detailed diagrams)
