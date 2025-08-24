# BPMN Diagram Template (Three Levels)

## Level 1: High-Level Overview

```mermaid
bpmnDiagram
    participant User
    participant System
    participant Database

    User->>System: Start Process
    System->>Database: Retrieve Data
    Database-->>System: Return Data
    System-->>User: Display Data
```

## Level 2: Detailed Process Flow

```mermaid
bpmnDiagram
    participant User
    participant System
    participant Database
    participant NotificationService

    User->>System: Start Process
    System->>Database: Retrieve Data
    Database-->>System: Return Data
    System->>NotificationService: Send Notification
    NotificationService-->>User: Notify User
    System-->>User: Display Data
```

## Level 3: Complete Implementation Details

```mermaid
bpmnDiagram
    participant User
    participant System
    participant Database
    participant NotificationService
    participant LoggingService

    User->>System: Start Process
    System->>Database: Retrieve Data
    Database-->>System: Return Data
    System->>LoggingService: Log Process Start
    System->>NotificationService: Send Notification
    NotificationService-->>User: Notify User
    System-->>User: Display Data
    System->>LoggingService: Log Process End
```

## Usage Guidelines

### For Level 1 Diagrams:
- Use for executive summaries and high-level process overviews
- Focus on major process steps and interactions
- Keep it simple with 3-5 main activities

### For Level 2 Diagrams:
- Use for technical documentation and detailed process flows
- Include key activities and decision points
- Show interactions between participants

### For Level 3 Diagrams:
- Use for detailed implementation documentation
- Include all relevant activities, events, and gateways
- Show error handling and alternative flows

### Best Practices:
1. Use consistent naming conventions for activities and events
2. Maintain proper abstraction levels
3. Include only relevant details for each level
4. Use proper BPMN notation
5. Keep diagrams readable and well-organized
6. Use comments for complex relationships
7. Validate diagrams for consistency

---

*Template last updated: 2025-08-14*
