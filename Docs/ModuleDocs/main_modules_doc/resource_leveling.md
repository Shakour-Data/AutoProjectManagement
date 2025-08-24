# Resource Leveling Module Documentation

## Level 1: Executive Overview

### Module Purpose and Functionality
The `resource_leveling` module provides a sophisticated system for optimizing resource allocation schedules within the AutoProjectManagement framework. It focuses on preventing resource conflicts by adjusting task start times and ensuring efficient resource utilization.

### Business Value
This module enables project teams to effectively manage resource allocation, prevent scheduling conflicts, and optimize task execution timelines. By providing insights into resource leveling, it helps organizations maximize productivity and minimize project delays.

---

## Level 2: Technical Architecture

### System Integration Architecture
```mermaid
graph TB
    subgraph InputLayer [Input Sources]
        A[Tasks JSON]
        B[Allocations JSON]
    end
    
    subgraph ProcessingLayer [Processing Engine]
        C[ResourceLeveler<br/>Core Engine]
        D[Task Flattening<br/>Nested Task Structure]
        E[Resource Leveling<br/>Conflict Prevention]
    end
    
    subgraph OutputLayer [Output Destinations]
        F[Leveled Schedule JSON]
        G[Conflict Report JSON]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
    E --> F
    E --> G
    
    style InputLayer fill:#e1f5fe
    style ProcessingLayer fill:#e8f5e8
    style OutputLayer fill:#fff3e0
```

### Class Hierarchy and Relationships
```mermaid
classDiagram
    class ResourceLeveler {
        +__init__(tasks_filepath, allocations_filepath, output_filepath, duration_type)
        +load_json_file(filepath) Dict[str, Any]
        +save_json_file(data, filepath) None
        +flatten_tasks(tasks, parent_id) List[Dict[str, Any]]
        +resource_leveling() Dict[str, Dict[str, Any]]
        +run() None
    }
```

### Data Flow Architecture
```mermaid
flowchart LR
    subgraph InputPhase [Input Processing]
        A[Load Tasks] --> B[Load Allocations]
    end
    
    subgraph ProcessingPhase [Resource Leveling]
        C[Flatten Tasks] --> D[Perform Resource Leveling]
    end
    
    subgraph OutputPhase [Output Generation]
        E[Save Leveled Schedule] --> F[Return Conflict Report]
    end
    
    InputPhase --> ProcessingPhase
    ProcessingPhase --> OutputPhase
    
    style InputPhase fill:#e1f5fe
    style ProcessingPhase fill:#e8f5e8
    style OutputPhase fill:#fff3e0
```

---

## Level 3: Detailed Implementation

### Core Class: ResourceLeveler
```python
class ResourceLeveler:
    """
    A class to handle resource leveling for project tasks.
    
    This class loads task and allocation data, flattens nested task structures,
    and performs resource leveling to prevent resource conflicts.
    """
    
    def __init__(self, tasks_filepath: str, allocations_filepath: str, 
                 output_filepath: str, duration_type: str = 'normal') -> None:
        """
        Initialize the ResourceLeveler with file paths and configuration.
        
        Args:
            tasks_filepath: Path to the tasks JSON file
            allocations_filepath: Path to the allocations JSON file
            output_filepath: Path where the leveled schedule will be saved
            duration_type: Type of duration to use ('optimistic', 'normal', 'pessimistic')
        """
```

### Resource Leveling Algorithm
```python
def resource_leveling(self) -> Dict[str, Dict[str, Any]]:
    """
    Perform resource leveling to prevent resource conflicts.
    
    This algorithm ensures that tasks assigned to the same resource
