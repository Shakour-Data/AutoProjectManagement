# UML Diagrams

## Class Diagram

The class diagram below represents the main classes and their relationships in
the Project Management software:

```
+------------------------+          +------------------------+
|        Project         | - - - - -|        Task            |
+------------------------+          +------------------------+
| - id: int              |          | - id: int              |
| - name: string         |          | - name: string         |
| - description: string  |          | - description: string  |
| - start_date: date     |          | - status: string       |
| - end_date: date       |          | - priority: int        |
+------------------------+          | - due_date: date       |
                                    +------------------------+
                                            - - - - -
                                            |
                                    +------------------------+
                                    |      SubTask           |
                                    +------------------------+
                                    | - id: int              |
                                    | - name: string         |
                                    | - status: string       |
                                    +------------------------+

+------------------------+          +------------------------+
|       Resource         | - - - - -|      Allocation        |
+------------------------+          +------------------------+
| - id: int              |          | - id: int              |
| - name: string         |          | - resource_id: int     |
| - role: string         |          | - task_id: int         |
+------------------------+          | - allocation_percent: int |
                                    +------------------------+

## Sequence Diagram

The sequence diagram below illustrates the interaction for creating a new task:

User - - - - > Frontend: Fill task form and submit
Frontend - - - - > Backend API: POST /tasks
Backend API - - - - > Database: Insert new task record
Backend API - - - - > Frontend: Return success response
Frontend - - - - > User: Display confirmation message

## Component Diagram

The component diagram shows the main components and their interactions:

[Frontend] - - - - <--> [Backend API] - - - - <--> [Database]
[Installer GUI] - - - - --> [Environment Setup Scripts]
[Backend API] - - - - --> [Services Layer] - - - - --> [Repositories Layer]

## Additional UML Diagrams

### Activity Diagram for Task Creation

User - - - - > Fill task form - - - - > Submit - - - - > Backend API - - - - > Validate - - - - > Store in Database - - - - > Return Response - - - - > User Confirmation

### State Diagram for Task Status

States: New - - - - > In Progress - - - - > Completed - - - - > Archived

Transitions:
- New to In Progress: When work starts
- In Progress to Completed: When task is done
- Completed to Archived: When task is archived

(To be expanded with detailed diagrams)
```

