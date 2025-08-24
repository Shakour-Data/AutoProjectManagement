# UML Diagram Template (Three Levels)

## Level 1: High-Level Overview

```mermaid
classDiagram
    class System {
        +String name
        +String version
        +String description
        +initialize()
        +start()
        +stop()
    }
    
    class Component {
        +String name
        +String description
        +initialize()
        +process()
    }
    
    System "1" *-- "*" Component : contains
```

## Level 2: Detailed Component Structure

```mermaid
classDiagram
    class MainComponent {
        +String name
        +List~SubComponent~ subcomponents
        +Configuration config
        +initialize(config: Configuration)
        +processData(data: Any)
        +getStatus() Status
    }
    
    class SubComponent {
        +String componentId
        +String type
        +process(input: Any) Any
        +validate() Boolean
    }
    
    class Configuration {
        +Map~String, Any~ settings
        +loadFromFile(path: String)
        +saveToFile(path: String)
        +getSetting(key: String) Any
    }
    
    class Status {
        +String state
        +List~String~ messages
        +Map~String, Any~ metrics
        +isHealthy() Boolean
    }
    
    MainComponent "1" *-- "*" SubComponent : manages
    MainComponent "1" *-- "1" Configuration : uses
    MainComponent "1" *-- "1" Status : maintains
```

## Level 3: Complete Implementation Details

```mermaid
classDiagram
    direction TB
    
    class MainSystem {
        -String systemName
        -String systemVersion
        -List~BaseComponent~ components
        -SystemConfiguration config
        -SystemStatus status
        +MainSystem(name: String, version: String)
        +initialize(configPath: String) Boolean
        +start() Boolean
        +stop() Boolean
        +addComponent(component: BaseComponent)
        +removeComponent(componentId: String)
        +getComponent(componentId: String) BaseComponent
        +updateConfiguration(key: String, value: Any)
        +getStatusReport() SystemStatusReport
    }
    
    class BaseComponent {
        <<abstract>>
        #String componentId
        #String componentType
        #ComponentConfiguration config
        #ComponentStatus status
        +BaseComponent(id: String, type: String)
        +initialize(config: ComponentConfiguration) Boolean
        +process(inputData: Any) ProcessingResult
        +validateInput(input: Any) ValidationResult
        +getMetrics() ComponentMetrics
        +updateStatus(newStatus: ComponentStatus)
    }
    
    class ConcreteComponentA {
        -SpecializedConfigA specialConfig
        -List~ProcessingStep~ processingSteps
        +ConcreteComponentA(id: String)
        +initialize(config: ComponentConfiguration) Boolean
        +process(inputData: InputDataA) ProcessingResultA
        +applyTransformation(data: Any) TransformedData
        +validateConstraints(data: Any) ConstraintValidation
    }
    
    class ConcreteComponentB {
        -SpecializedConfigB specialConfig
        -Cache cache
        +ConcreteComponentB(id: String)
        +initialize(config: ComponentConfiguration) Boolean
        +process(inputData: InputDataB) ProcessingResultB
        +cacheData(key: String, data: Any)
        +getCachedData(key: String) Any
        +clearCache()
    }
    
    class SystemConfiguration {
        -Map~String, Any~ globalSettings
        -Map~String, ComponentConfiguration~ componentConfigs
        +SystemConfiguration()
        +loadFromJson(jsonData: String) Boolean
        +saveToJson() String
        +getGlobalSetting(key: String) Any
        +setGlobalSetting(key: String, value: Any)
        +getComponentConfig(componentId: String) ComponentConfiguration
        +setComponentConfig(componentId: String, config: ComponentConfiguration)
    }
    
    class ComponentConfiguration {
        -Map~String, Any~ settings
        -List~String~ dependencies
        +ComponentConfiguration()
        +getSetting(key: String) Any
        +setSetting(key: String, value: Any)
        +hasDependency(componentId: String) Boolean
        +addDependency(componentId: String)
        +removeDependency(componentId: String)
    }
    
    class SystemStatus {
        -String overallState
        -Map~String, ComponentStatus~ componentStatuses
        -List~SystemEvent~ recentEvents
        -SystemMetrics metrics
        +SystemStatus()
        +updateComponentStatus(componentId: String, status: ComponentStatus)
        +getComponentStatus(componentId: String) ComponentStatus
        +addEvent(event: SystemEvent)
        +getRecentEvents(count: Int) List~SystemEvent~
        +calculateHealthScore() Double
    }
    
    class ComponentStatus {
        -String state
        -String lastError
        -DateTime lastUpdate
        -ComponentMetrics metrics
        +ComponentStatus()
        +setState(newState: String)
        +setError(errorMessage: String)
        +clearError()
        +updateMetrics(newMetrics: ComponentMetrics)
        +isOperational() Boolean
    }
    
    MainSystem "1" *-- "*" BaseComponent : manages
    MainSystem "1" *-- "1" SystemConfiguration : uses
    MainSystem "1" *-- "1" SystemStatus : maintains
    BaseComponent <|-- ConcreteComponentA
    BaseComponent <|-- ConcreteComponentB
    SystemConfiguration "1" *-- "*" ComponentConfiguration : contains
    SystemStatus "1" *-- "*" ComponentStatus : tracks
```

## Usage Guidelines

### For Level 1 Diagrams:
- Use for executive summaries and high-level architecture overviews
- Focus on major system components and their relationships
- Keep it simple with 3-5 main classes

### For Level 2 Diagrams:
- Use for technical documentation and component design
- Include key methods and attributes
- Show relationships and dependencies between components

### For Level 3 Diagrams:
- Use for detailed implementation documentation
- Include all relevant classes, methods, and attributes
- Show inheritance, composition, and association relationships
- Include abstract classes and interfaces

### Best Practices:
1. Use consistent naming conventions
2. Maintain proper abstraction levels
3. Include only relevant details for each level
4. Use proper UML notation
5. Keep diagrams readable and well-organized
6. Use comments for complex relationships
7. Validate diagrams for consistency

### Mermaid.js Syntax Notes:
- Use `classDiagram` for class diagrams
- Use `+` for public methods/attributes
- Use `-` for private methods/attributes  
- Use `#` for protected methods/attributes
- Use `*--` for composition relationships
- Use `o--` for aggregation relationships
- Use `<|--` for inheritance relationships
- Use `-->` for association relationships

---

*Template last updated: 2025-08-14*
