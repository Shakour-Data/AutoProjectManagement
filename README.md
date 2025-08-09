# AutoProjectManagement System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

**AutoProjectManagement** is a comprehensive, CLI-based automated project management system that revolutionizes software project management through intelligent automation, GitHub-native workflows, and JSON-driven configurations.

### Key Features
- **100% CLI-based**: No web frontend required
- **GitHub-Native**: Deep integration with GitHub Actions and APIs
- **JSON-Driven**: All configurations and workflows use JSON
- **Automated Progress Tracking**: Real-time progress monitoring via Git commits
- **Self-Managing**: Automatic project setup, monitoring, and reporting

## 🏗️ System Architecture

### High-Level Architecture
```mermaid
graph TD
    User[User CLI] --> CLI[CLI Interface]
    CLI --> Engine[Automation Engine]
    Engine --> GitHub[GitHub API]
    Engine --> JSON[JSON Database]
    Engine --> Actions[GitHub Actions]
    
    style User fill:#f9f,stroke:#333
    style CLI fill:#bbf,stroke:#333
    style Engine fill:#9f9,stroke:#333
    style GitHub fill:#ff9,stroke:#333
    style JSON fill:#f96,stroke:#333
    style Actions fill:#9ff,stroke:#333
```

### Detailed System Architecture
```mermaid
graph TB
    subgraph "User Interface Layer"
        CLI[CLI Commands]
        Config[Configuration Files]
        Scripts[Automation Scripts]
    end
    
    subgraph "Processing Layer"
        Engine[Automation Engine]
        Parser[JSON Parser]
        Scheduler[Task Scheduler]
        Tracker[Progress Tracker]
    end
    
    subgraph "Integration Layer"
        GitHubAPI[GitHub API]
        Actions[GitHub Actions]
        Webhooks[Webhooks Handler]
    end
    
    subgraph "Data Layer"
        JSONDB[(JSON Database)]
        Logs[(Log Files)]
        Reports[(Generated Reports)]
    end
    
    CLI --> Engine
    Config --> Parser
    Engine --> Scheduler
    Scheduler --> GitHubAPI
    Engine --> Tracker
    Tracker --> JSONDB
    Actions --> Webhooks
    Webhooks --> Engine
```

## 📊 Business Process Diagrams (Flowchart Style)

### Project Initialization Process
```mermaid
flowchart TD
    A[User Starts Setup] --> B{Validate Inputs}
    B -->|Valid| C[Create Repository Structure]
    B -->|Invalid| D[Show Error Message]
    D --> B
    C --> E[Setup GitHub Actions]
    E --> F[Initialize JSON Files]
    F --> G[Create Initial Configuration]
    G --> H[Generate Welcome Report]
    H --> I[Setup Complete]
    I --> J[Send Notification]
```

### Task Management Workflow
```mermaid
flowchart TD
    A[Developer Adds Task] --> B[Parse Task Details]
    B --> C{Validate Task}
    C -->|Valid| D[Store in JSON Database]
    C -->|Invalid| E[Show Validation Error]
    E --> A
    D --> F[Create GitHub Issue]
    F --> G[Assign Resources]
    G --> H[Update Task Status]
    H --> I[Trigger Automation]
    I --> J[Send Confirmation]
    J --> K[Update Dashboard]
```

### Progress Tracking Process
```mermaid
flowchart TD
    A[Git Commit Detected] --> B[Parse Commit Message]
    B --> C{Valid Format?}
    C -->|Yes| D[Extract Task Info]
    C -->|No| E[Log Invalid Format]
    E --> F[Skip Processing]
    D --> G[Update Task Progress]
    G --> H[Calculate New Metrics]
    H --> I[Update JSON Database]
    I --> J[Generate Progress Report]
    J --> K[Update GitHub PR Status]
    K --> L[Send Notifications]
```

### Complete Workflow Sequence
```mermaid
flowchart TD
    subgraph "Initialization Phase"
        A1[Start] --> A2[Load Configuration]
        A2 --> A3[Setup GitHub Integration]
        A3 --> A4[Initialize Database]
    end
    
    subgraph "Operation Phase"
        B1[Receive Command] --> B2[Parse Arguments]
        B2 --> B3[Execute Business Logic]
        B3 --> B4[Update Database]
        B4 --> B5[Trigger GitHub Actions]
    end
    
    subgraph "Reporting Phase"
        C1[Collect Metrics] --> C2[Generate Reports]
        C2 --> C3[Update Dashboards]
        C3 --> C4[Send Notifications]
    end
    
    A4 --> B1
    B5 --> C1
    
    style A1 fill:#e1f5fe
    style B1 fill:#f3e5f5
    style C1 fill:#e8f5e9
```

## 📈 Data Flow Diagrams (DFD)

### Context Level DFD (Level 0)
```mermaid
graph LR
    User[User/Developer]
    System[AutoProjectManagement System]
    GitHub[GitHub Platform]
    Storage[JSON Storage]
    
    User -->|Commands & Data| System
    System -->|API Calls| GitHub
    System -->|Read/Write| Storage
    GitHub -->|Webhooks| System
    Storage -->|Reports| User
    
    style User fill:#e1f5fe
    style System fill:#fff3e0
    style GitHub fill:#f3e5f5
    style Storage fill:#e8f5e9
```

### Level 1 DFD - System Decomposition
```mermaid
graph TD
    subgraph "AutoProjectManagement System"
        CLI[CLI Interface]
        Engine[Automation Engine]
        GitHubInt[GitHub Integration]
        JSONProc[JSON Processor]
        Reporter[Report Generator]
    end
    
    User[User] --> CLI
    CLI --> Engine
    Engine --> GitHubInt
    Engine --> JSONProc
    JSONProc --> Storage[(JSON Files)]
    GitHubInt --> GitHubAPI[GitHub API]
    Reporter --> Reports[(Reports)]
    
    style CLI fill:#bbf,stroke:#333
    style Engine fill:#9f9,stroke:#333
    style GitHubInt fill:#ff9,stroke:#333
    style JSONProc fill:#f96,stroke:#333
```

### Level 2 DFD - Data Processing Details
```mermaid
graph TD
    subgraph "Input Processing"
        CLI[CLI Commands]
        Parser[Input Parser]
        Validator[Data Validator]
    end
    
    subgraph "Business Logic"
        Scheduler[Task Scheduler]
        Calculator[Progress Calculator]
        Allocator[Resource Allocator]
    end
    
    subgraph "Data Management"
        JSONDB[(JSON Database)]
        Cache[(Cache Layer)]
        Logger[(Log Files)]
    end
    
    subgraph "External Services"
        GitHubAPI[GitHub API Client]
        Actions[Actions Runner]
        Notifications[Notification Service]
    end
    
    CLI --> Parser
    Parser --> Validator
    Validator --> Scheduler
    Scheduler --> Calculator
    Calculator --> JSONDB
    JSONDB --> Cache
    Cache --> Logger
    Engine --> GitHubAPI
    Actions --> Notifications
```

## 🏗️ UML Diagrams

### Class Diagram - Core System
```mermaid
classDiagram
    class AutoProjectManagement {
        +str project_name
        +dict config
        +setup()
        +run()
        +cleanup()
    }
    
    class CLIInterface {
        +parse_args()
        +execute_command()
        +display_output()
    }
    
    class GitHubIntegration {
        +authenticate()
        +create_issue()
        +update_pr()
        +get_commits()
    }
    
    class JSONDatabase {
        +load_data()
        +save_data()
        +update_record()
        +query_data()
    }
    
    class TaskManager {
        +create_task()
        +update_status()
        +assign_resources()
        +calculate_progress()
    }
    
    class ReportGenerator {
        +generate_summary()
        +create_gantt_chart()
        +export_data()
        +send_notifications()
    }
    
    AutoProjectManagement --> CLIInterface
    AutoProjectManagement --> GitHubIntegration
    AutoProjectManagement --> JSONDatabase
    CLIInterface --> TaskManager
    TaskManager --> ReportGenerator
    GitHubIntegration --> JSONDatabase
```

### Sequence Diagram - Complete Workflow
```mermaid
sequenceDiagram
    participant U as User
    participant CLI as CLI Interface
    participant Engine as Automation Engine
    participant GitHub as GitHub API
    participant JSON as JSON Database
    participant Actions as GitHub Actions
    
    U->>CLI: Execute project setup
    CLI->>Engine: Initialize system
    Engine->>JSON: Load configuration
    Engine->>GitHub: Create repository structure
    GitHub->>Actions: Setup workflows
    Actions->>Engine: Confirm setup
    Engine->>JSON: Store project data
    Engine->>CLI: Return success
    
    U->>CLI: Add new task
    CLI->>Engine: Process task
    Engine->>JSON: Store task data
    Engine->>GitHub: Create issue
    GitHub->>Actions: Trigger workflow
    Actions->>Engine: Update progress
    Engine->>JSON: Update records
    Engine->>CLI: Display confirmation
    
    U->>CLI: Generate report
    CLI->>Engine: Request report
    Engine->>JSON: Fetch data
    Engine->>GitHub: Get commit history
    Engine->>Engine: Calculate metrics
    Engine->>CLI: Generate report
    CLI->>U: Display formatted report
```

### Component Diagram - System Architecture
```mermaid
graph TB
    subgraph "AutoProjectManagement System"
        subgraph "Presentation Layer"
            CLI[CLI Interface]
            Config[Config Manager]
        end
        
        subgraph "Business Logic Layer"
            Engine[Automation Engine]
            Scheduler[Task Scheduler]
            Tracker[Progress Tracker]
            Calculator[Metrics Calculator]
        end
        
        subgraph "Data Access Layer"
            JSONDB[(JSON Database)]
            Cache[(Cache Layer)]
            Logger[(Log Files)]
        end
        
        subgraph "External Services"
            GitHubAPI[GitHub API Client]
            Actions[Actions Runner]
            Notifications[Notification Service]
        end
    end
    
    CLI --> Engine
    Config --> Engine
    Engine --> Scheduler
    Scheduler --> Tracker
    Tracker --> Calculator
    Calculator --> JSONDB
    JSONDB --> Cache
    Cache --> Logger
    Engine --> GitHubAPI
    GitHubAPI --> Actions
    Actions --> Notifications
```

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- GitHub account with repository access
- Git installed and configured

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/AutoProjectManagement.git
cd AutoProjectManagement

# 2. Setup Python environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure GitHub
python -m autoprojectmanagement.cli config --github-token YOUR_TOKEN

# 4. Initialize project
python -m autoprojectmanagement.cli setup --project-name "MyProject"
```

## 📊 Usage Examples

### Basic Commands
```bash
# Initialize a new project
python -m autoprojectmanagement.cli init --name "MyProject"

# Add a new task
python -m autoprojectmanagement.cli task add --title "Implement feature X" --priority high

# View progress
python -m autoprojectmanagement.cli progress show

# Generate reports
python -m autoprojectmanagement.cli report generate --type weekly

# Update GitHub integration
python -m autoprojectmanagement.cli github sync
```

### Configuration Files
- `config.json`: Main system configuration
- `project.json`: Project-specific settings
- `tasks.json`: Task definitions and status
- `progress.json`: Progress tracking data
- `reports.json`: Generated reports metadata

## 🔧 Development

### Project Structure
```
AutoProjectManagement/
├── autoprojectmanagement/
│   ├── main_modules/          # Core business logic
│   │   ├── task_management.py
│   │   ├── progress_tracker.py
│   │   └── github_integration.py
│   ├── services/              # External integrations
│   │   ├── auto_commit.py
│   │   ├── github_integration.py
│   │   └── backup_manager.py
│   ├── cli.py                # Command-line interface
│   └── auto_runner.py        # Main execution engine
├── Docs/                     # Documentation
│   ├── BPMN_Diagrams.md
│   ├── DFD_Diagrams.md
│   └── UML_Diagrams.md
├── tests/                    # Test suites
├── requirements.txt          # Dependencies
└── README.md                # This file
```

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test category
python -m pytest tests/code_tests/UnitTests/

# Run integration tests
python -m pytest tests/code_tests/IntegrationTests/

# Generate coverage report
python -m pytest --cov=autoprojectmanagement tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and GitHub Actions
- Inspired by modern DevOps practices
- Designed for automation-first workflows
- Powered by JSON-driven configurations
