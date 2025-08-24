# BPMN Diagrams

## Project Management Process

```mermaid
flowchart TD
    Start([Start]) --> CreateProject[Create Project]
    CreateProject --> DefineTasks[Define Tasks]
    DefineTasks --> AllocateResources[Allocate Resources]
    AllocateResources --> MonitorProgress[Monitor Progress]
    MonitorProgress --> GenerateReports[Generate Reports]
    GenerateReports --> End([End])
    
    MonitorProgress -->|Issue Detected| ResolveIssues[Resolve Issues]
    ResolveIssues --> MonitorProgress
```

## Task Creation Process

```mermaid
flowchart TD
|Monitoring & Control|
:Track Progress;
:Identify & Manage Risks;
:Adjust Plans;
|Reporting|
:Generate Reports;
:Distribute to Stakeholders;
|Project Closure|
:Complete Deliverables;
:Obtain Acceptance;
:Archive Documents;
stop
@enduml
```

## Detailed BPMN Processes

### Project Initiation

```plantuml
@startuml
start
:Identify Stakeholders;
:Define Goals & Scope;
:Obtain Approvals;
stop
@enduml
```

### Task Planning

```plantuml
@startuml
start
:Decompose Project;
:Assign Resources & Deadlines;
:Review & Approve Plan;
stop
@enduml
```

### Task Execution

```plantuml
@startuml
start
:Perform Tasks;
:Update Status;
:Communicate Progress;
stop
@enduml
```

### Monitoring and Controlling

```plantuml
@startuml
start
:Track Progress;
:Identify & Manage Risks;
:Adjust Plans;
stop
@enduml
```

### Reporting

```plantuml
@startuml
start
:Generate Reports;
:Distribute to Stakeholders;
stop
@enduml
```

### Project Closure

```plantuml
@startuml
start
:Complete Deliverables;
:Obtain Acceptance;
:Archive Documents;
stop
@enduml
```

(To be expanded with detailed BPMN diagrams)
