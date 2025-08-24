# DFD (Data Flow Diagrams)

## Level 0: Context Diagram

```mermaid
flowchart TD
    External[External Systems<br/>GitHub, VS Code] --> AutoProjectManagement[AutoProjectManagement System]
    AutoProjectManagement --> External
    
    Users[Users<br/>Developers, Managers] --> AutoProjectManagement
    AutoProjectManagement --> Users
    
    DataStores[Data Stores<br/>JSON Databases, Files] --> AutoProjectManagement
    AutoProjectManagement --> DataStores
```

## Level 1: System Overview

```mermaid
flowchart TD
    subgraph AutoProjectManagement[AutoProjectManagement System]
        API[API Gateway]
        Core[Core Processing]
        Dashboard[Dashboard Services]
        Integration[Integration Services]
        DataProcessing[Data Processing]
    end
    
    External[External Systems] --> API
    API --> External
    
    Users[Users] --> Dashboard
    Dashboard --> Users
    
    API --> Core
    Core --> API
    
    Core --> Dashboard
    Dashboard --> Core
    
    Core --> Integration
    Integration --> Core
    
    Core --> DataProcessing
    DataProcessing --> Core
    
    DataProcessing --> DataStores[Data Stores]
    DataStores --> DataProcessing
```

## Level 2: API Gateway Data Flow

```mermaid
flowchart TD
    subgraph APIGateway[API Gateway]
        HTTP[HTTP Endpoints]
        WebSocket[WebSocket Gateway]
        SSE[SSE Endpoints]
        Auth[Authentication]
        Validation[Request Validation]
    end
    
    Clients[Clients] --> HTTP
    HTTP --> Clients
    
    Clients --> WebSocket
    WebSocket --> Clients
    
    Clients --> SSE
    SSE --> Clients
    
    HTTP --> Auth
    WebSocket --> Auth
    SSE --> Auth
    
    Auth --> Validation
    Validation --> Auth
    
    Validation --> CoreProcessing[Core Processing]
    CoreProcessing --> Validation
    
    Validation --> DashboardServices[Dashboard Services]
    DashboardServices --> Validation
```

## Level 2: Core Processing Data Flow

```mermaid
flowchart TD
    subgraph CoreProcessing[Core Processing]
        ProjectMgmt[Project Management]
        TaskMgmt[Task Management]
        ResourceMgmt[Resource Management]
        RiskMgmt[Risk Management]
        ProgressMgmt[Progress Management]
    end
    
    API[API Gateway] --> ProjectMgmt
    ProjectMgmt --> API
    
    API --> TaskMgmt
    TaskMgmt --> API
    
    API --> ResourceMgmt
    ResourceMgmt --> API
    
    API --> RiskMgmt
    RiskMgmt --> API
    
    API --> ProgressMgmt
    ProgressMgmt --> API
    
    ProjectMgmt --> DataStores[Data Stores]
    DataStores --> ProjectMgmt
    
    TaskMgmt --> DataStores
    DataStores --> TaskMgmt
    
    ResourceMgmt --> DataStores
    DataStores --> ResourceMgmt
    
    RiskMgmt --> DataStores
    DataStores --> RiskMgmt
    
    ProgressMgmt --> DataStores
    DataStores --> ProgressMgmt
```

## Level 2: Dashboard Services Data Flow

```mermaid
flowchart TD
    subgraph DashboardServices[Dashboard Services]
        Overview[Dashboard Overview]
        Metrics[Metrics & Analytics]
        Alerts[Alert System]
        Layout[Layout Management]
        RealTime[Real-time Updates]
    end
    
    API[API Gateway] --> Overview
    Overview --> API
    
    API --> Metrics
    Metrics --> API
    
    API --> Alerts
    Alerts --> API
    
    API --> Layout
    Layout --> API
    
    API --> RealTime
    RealTime --> API
    
    Overview --> DataStores[Data Stores]
    DataStores --> Overview
    
    Metrics --> DataStores
    DataStores --> Metrics
    
    Alerts --> DataStores
    DataStores --> Alerts
    
    Layout --> DataStores
    DataStores --> Layout
    
    RealTime --> DataStores
    DataStores --> RealTime
```

## Level 2: Integration Services Data Flow

```mermaid
flowchart TD
    subgraph IntegrationServices[Integration Services]
        GitHub[GitHub Integration]
        VSCode[VS Code Integration]
        Wiki[Wiki Services]
        ExternalAPIs[External APIs]
    end
    
    Core[Core Processing] --> GitHub
    GitHub --> Core
    
    Core --> VSCode
    VSCode --> Core
    
