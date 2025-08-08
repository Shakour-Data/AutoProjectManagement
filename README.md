# AutoProjectManagement

A comprehensive Python package for automated project management, task tracking, and workflow optimization for software development teams.

## Features

- **Automated Project Management**: Intelligent project planning and tracking
- **Task Management**: Advanced task prioritization and scheduling
- **Progress Tracking**: Real-time progress monitoring and reporting
- **Resource Management**: Efficient resource allocation and leveling
- **Risk Management**: Proactive risk identification and mitigation
- **Git Integration**: Seamless GitHub and Git integration
- **CLI Interface**: Powerful command-line interface for all operations
- **JSON-based Configuration**: Flexible JSON-based project configuration

## Installation

### From PyPI (when published)
```bash
pip install autoprojectmanagement
```

### From Source
```bash
git clone https://github.com/autoprojectmanagement/autoprojectmanagement.git
cd autoprojectmanagement
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/autoprojectmanagement/autoprojectmanagement.git
cd autoprojectmanagement
pip install -e ".[dev]"
```

## Quick Start

### Command Line Interface
```bash
# Initialize a new project
apm init

# Create a new project
apm create-project my-project --description "My awesome project"

# Add tasks to a project
apm add-task 1 --task-name "Implement feature X" --priority high

# Check project status
apm status 1

# Generate reports
apm report 1 --report-type summary --output report.md
```

### Python API
```python
from autoprojectmanagement import ProjectManagementSystem

# Initialize the system
system = ProjectManagementSystem()
system.initialize_system()

# Create a project
project = {
    "id": 1,
    "name": "My Project",
    "description": "Project description"
}
system.add_project(project)

# Add a task
task = {
    "id": 1,
    "name": "Implement feature",
    "priority": "high",
    "status": "pending"
}
system.add_task_to_project(1, task)
```

## Project Structure

```
autoprojectmanagement/
├── main_modules/          # Core project management modules
│   ├── project_management_system.py
│   ├── task_management.py
│   ├── scheduler.py
│   ├── resource_management.py
│   └── ...
├── services/             # Utility services
│   ├── auto_commit.py
│   ├── github_integration.py
│   ├── backup_manager.py
│   └── ...
├── cli.py               # Command-line interface
└── ...
```

## Configuration

### JSON Configuration Files
The system uses JSON files for configuration:

- `commit_task_database.json`: Task database
- `wbs_parts/`: Work Breakdown Structure components
- `progress_report.md`: Progress reports

### Environment Variables
- `APM_CONFIG_PATH`: Path to configuration directory
- `APM_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `APM_GITHUB_TOKEN`: GitHub API token for integration

## CLI Commands

### Project Management
- `apm init`: Initialize the system
- `apm create-project`: Create new projects
- `apm list-projects`: List all projects
- `apm delete-project`: Delete projects

### Task Management
- `apm add-task`: Add tasks to projects
- `apm update-task`: Update task information
- `apm list-tasks`: List project tasks
- `apm complete-task`: Mark tasks as complete

### Reporting
- `apm status`: Show project status
- `apm report`: Generate various reports
- `apm export`: Export project data

### Git Integration
- `apm commit`: Automated commits with intelligent messages
- `apm push`: Push changes to remote
- `apm sync`: Sync with remote repository

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black autoprojectmanagement/
isort autoprojectmanagement/
```

### Type Checking
```bash
mypy autoprojectmanagement/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [https://autoprojectmanagement.readthedocs.io](https://autoprojectmanagement.readthedocs.io)
- Issues: [https://github.com/autoprojectmanagement/autoprojectmanagement/issues](https://github.com/autoprojectmanagement/autoprojectmanagement/issues)
- Discussions: [https://github.com/autoprojectmanagement/autoprojectmanagement/discussions](https://github.com/autoprojectmanagement/autoprojectmanagement/discussions)
