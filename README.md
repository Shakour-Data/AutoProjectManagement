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
- **Wiki Documentation**: Automatic synchronization of Docs/ to GitHub Wiki

## 🏗️ System Architecture

### High-Level Architecture
```mermaid
graph TD
    User([User]) --> CLI([CLI Interface])
    CLI --> Engine([Automation Engine])
    Engine --> GitHub([GitHub API])
    Engine --> JSON([JSON Database])
    Engine --> Actions([GitHub Actions])
    Engine --> Wiki([Wiki Sync Service])
    Wiki --> GitHubWiki([GitHub Wiki])
```

### Detailed System Architecture
```mermaid
graph TB
    CLI[CLI Commands] --> Engine[Automation Engine]
    Config[Config Files] --> Parser[JSON Parser]
    Engine --> Scheduler[Task Scheduler]
    Scheduler --> Tracker[Tracker]
    Tracker --> JSONDB[(JSON Database)]
    JSONDB --> Reports[Reports]
    Actions[GitHub Actions] --> Webhooks[Webhooks]
    Webhooks --> Engine
    Engine --> WikiSync[Wiki Sync Service]
    WikiSync --> WikiGit[Wiki Git Operations]
    WikiGit --> GitHubWiki[(GitHub Wiki)]
    WikiSync --> PageMapper[Wiki Page Mapper]
    PageMapper --> Docs[(Docs Directory)]
```

## 📊 Business Process Diagrams

### Project Initialization Process
```mermaid
flowchart TD
    A([Start]) --> B{Validate Inputs}
    B -->|Valid| C([Create Repository])
    B -->|Invalid| D([Show Error])
    D --> B
    C --> E([Setup Actions])
    E --> F([Initialize JSON])
    F --> G([Create Config])
    G --> H([Generate Report])
    H --> I([Complete])
```

### Wiki Synchronization Process
```mermaid
flowchart TD
    A([Start Sync]) --> B{Wiki Exists?}
    B -->|No| C[Create Initial Wiki]
    B -->|Yes| D[Clone Wiki Repo]
    C --> D
    D --> E[Scan Docs/ Directory]
    E --> F[Generate Sync Plan]
    F --> G{Changes Detected?}
    G -->|Yes| H[Apply Changes]
    G -->|No| I[Skip - No Changes]
    H --> J[Commit & Push]
    J --> K[Sync Complete]
    I --> K
```

### Task Management Workflow
```mermaid
flowchart TD
    A([Add Task]) --> B([Parse Details])
    B --> C{Validate}
    C -->|Valid| D([Store JSON])
    C -->|Invalid| E([Show Error])
    E --> A
    D --> F([Create Issue])
    F --> G([Assign Resources])
    G --> H([Update Status])
    H --> I([Trigger Automation])
    I --> J([Send Confirmation])
```

### Progress Tracking Process
```mermaid
flowchart TD
    A([Git Commit]) --> B([Parse Message])
    B --> C{Valid Format?}
    C -->|Yes| D([Extract Info])
    C -->|No| E([Log Error])
    E --> F([Skip])
    D --> G([Update Progress])
    G --> H([Calculate Metrics])
    H --> I([Update JSON])
    I --> J([Generate Report])
    J --> K([Update PR])
```

## 📈 Data Flow Diagrams

### Context Level DFD
```mermaid
flowchart LR
    User([User]) --> System([AutoProjectManagement])
    System --> GitHub([GitHub])
    System --> Storage([JSON Storage])
    GitHub --> System
    Storage --> User
```

### System Decomposition
```mermaid
flowchart TD
    CLI --> Engine
    Engine --> Scheduler
    Scheduler --> Tracker
    Tracker --> JSONDB
    JSONDB --> Reports
```

## 🏗️ UML Diagrams

### Class Diagram
```mermaid
classDiagram
    class AutoProjectManagement {
        +setup()
        +run()
        +cleanup()
    }
    
    class CLIInterface {
        +parse_args()
        +execute_command()
    }
    
    class GitHubIntegration {
        +authenticate()
        +create_issue()
    }
    
    class JSONDatabase {
        +load_data()
        +save_data()
    }
    
    class WikiSyncService {
        +sync_to_wiki()
        +_generate_sync_plan()
        +_execute_sync()
    }
    
    class WikiGitOperations {
        +clone_wiki_repo()
        +commit_changes()
        +push_changes()
    }
    
    class WikiPageMapper {
        +map_file_to_wiki_page()
        +get_directory_structure()
    }
    
    AutoProjectManagement --> CLIInterface
    AutoProjectManagement --> GitHubIntegration
    AutoProjectManagement --> JSONDatabase
    AutoProjectManagement --> WikiSyncService
    WikiSyncService --> WikiGitOperations
    WikiSyncService --> WikiPageMapper
```

### Sequence Diagram
```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Engine
    participant JSON
    participant GitHub
    participant Actions
    participant WikiSync
    participant Docs
    participant WikiGit
    participant GitHubWiki
    participant PageMapper
    
    User->>CLI: Setup project
    CLI->>Engine: Initialize system
    Engine->>JSON: Load configuration
    Engine->>GitHub: Create repository
    GitHub->>Actions: Setup GitHub Actions
    Actions->>Engine: Confirm setup complete
    Engine->>JSON: Store project data
    
    Note over WikiSync: Wiki Synchronization Process
    Engine->>WikiSync: Start wiki sync
    WikiSync->>Docs: Scan Docs/ directory
    Docs-->>WikiSync: Return markdown files
    WikiSync->>WikiGit: Clone wiki repository
    WikiGit-->>GitHubWiki: Fetch from GitHub
    WikiSync->>PageMapper: Map files to wiki pages
    PageMapper-->>WikiSync: Return page mappings
    WikiSync->>WikiGit: Apply changes
    WikiGit->>GitHubWiki: Push updates to wiki
    GitHubWiki-->>WikiSync: Confirm sync complete
    WikiSync-->>Engine: Report sync status
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

# Sync documentation to GitHub Wiki
python -m autoprojectmanagement.cli wiki sync --repo-owner your-username --repo-name your-repo
```

### Wiki Synchronization Commands
```bash
# Sync documentation to GitHub Wiki
python -m autoprojectmanagement.cli wiki sync --repo-owner your-username --repo-name your-repo

# Dry run to preview changes
python -m autoprojectmanagement.cli wiki sync --dry-run --repo-owner your-username --repo-name your-repo

# Force full sync (overwrite existing wiki)
python -m autoprojectmanagement.cli wiki sync --force --repo-owner your-username --repo-name your-repo
```

### Configuration Files
- `config.json`: Main system configuration
- `project.json`: Project-specific settings
- `tasks.json`: Task definitions and status
- `progress.json`: Progress tracking data
- `reports.json`: Generated reports metadata
- `wiki_config.json`: Wiki synchronization settings

## 🔧 Development

### Project Structure
```
AutoProjectManagement/
├── autoprojectmanagement/
│   ├── main_modules/          # Core business logic
│   ├── services/              # External integrations
│   │   ├── wiki_git_operations.py    # Git operations for wiki
│   │   ├── wiki_page_mapper.py       # File to wiki page mapping
│   │   └── wiki_sync_service.py      # Wiki synchronization service
│   ├── cli.py                # Command-line interface
│   └── auto_runner.py        # Main execution engine
├── Docs/                     # Documentation (auto-synced to wiki)
├── tests/                    # Test suites
├── requirements.txt          # Dependencies
└── README.md                # This file
```

### Wiki Synchronization Services

The system includes three new services for automatic GitHub Wiki synchronization:

#### WikiGitOperations
Handles all Git operations for the GitHub wiki repository:
- Clone wiki repositories
- Commit changes with proper messages
- Push updates to remote
- Manage branches and commit history
- Clean up temporary repositories

#### WikiPageMapper
Maps file paths to GitHub wiki page names:
- Convert file paths to wiki-compatible names
- Handle special characters and spaces
- Maintain directory structure in wiki
- Generate navigation-friendly page names

#### WikiSyncService
Main service for synchronizing Docs/ markdown files to GitHub Wiki:
- Automatic discovery of markdown files
- Intelligent change detection
- Dry-run capability for testing
- Comprehensive sync reporting
- Initial wiki setup and Home page creation

### Wiki Synchronization Workflow
```mermaid
flowchart TD
    A([Start Sync]) --> B{Wiki Exists?}
    B -->|No| C[Create Initial Wiki]
    B -->|Yes| D[Clone Wiki Repo]
    C --> D
    D --> E[Scan Docs/ Directory]
    E --> F[Generate Sync Plan]
    F --> G{Changes Detected?}
    G -->|Yes| H[Apply Changes]
    G -->|No| I[Skip - No Changes]
    H --> J[Commit & Push]
    J --> K[Sync Complete]
    I --> K
```

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test category
python -m pytest tests/code_tests/UnitTests/

# Generate coverage report
python -m pytest --cov=autoprojectmanagement tests/

# Test wiki synchronization
python -m autoprojectmanagement.cli wiki sync --dry-run --repo-owner test-user --repo-name test-repo
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
- Enhanced with automatic GitHub Wiki documentation
