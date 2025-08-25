# AutoProjectManagement CLI & Dashboard Guide

## Overview

This guide covers the enhanced command-line interface (CLI) and dashboard features of AutoProjectManagement, including improved error handling, user experience, and comprehensive documentation.

## CLI Commands

### Basic Usage

```bash
# Show help
autoprojectmanagement --help
autoprojectmanagement help

# Show version
autoprojectmanagement --version
```

### Project Management

```bash
# Initialize the system
autoprojectmanagement init

# Create a new project
autoprojectmanagement create-project "My Project" --description "Project description"

# Show project status
autoprojectmanagement status 1
autoprojectmanagement status 1 --format json

# Add tasks to project
autoprojectmanagement add-task 1 --task-name "Implement feature" --priority high
autoprojectmanagement add-task 1 --task-name "Fix bug" --priority urgent --assignee "John Doe"

# Update task status
autoprojectmanagement update-task-status 1 1 --new-status in_progress
```

### Dashboard Management

```bash
# Start dashboard server
autoprojectmanagement dashboard start
autoprojectmanagement dashboard start --port 8080

# Stop dashboard server
autoprojectmanagement dashboard stop

# Check dashboard status
autoprojectmanagement dashboard status

# Open dashboard in browser
autoprojectmanagement dashboard open

# Export dashboard data
autoprojectmanagement dashboard export --format json
autoprojectmanagement dashboard export --format markdown --output report.md

# Create custom dashboard views
autoprojectmanagement dashboard create-view --name "My View" --widgets "health,progress,alerts"

# Schedule automated reports
autoprojectmanagement dashboard schedule-report --type overview --schedule "0 9 * * *"
```

## Enhanced Error Handling

### Improved Error Messages

The CLI now provides more helpful error messages with troubleshooting tips:

```bash
# Example error with guidance
❌ Error: Project with ID 999 not found
💡 Use 'autoprojectmanagement status' to list available projects

# Validation errors with details
❌ Error: Invalid due date format '2024/12/31'. Use YYYY-MM-DD format.

# Network connectivity issues
❌ Error: Cannot connect to dashboard endpoint
💡 The server might not be fully initialized yet. Please wait and try again.
```

### Verbose Mode

Use `--verbose` flag for detailed debugging information:

```bash
autoprojectmanagement add-task 1 --task-name "Test" --verbose
autoprojectmanagement update-task-status 1 1 --new-status done --verbose
```

### Error Categories

The system categorizes errors for better troubleshooting:

- **Validation Errors**: Input validation failures
- **Authentication Errors**: Login and credential issues  
- **Authorization Errors**: Permission and access issues
- **Database Errors**: Data storage and retrieval problems
- **Network Errors**: Connectivity and API issues
- **External Service Errors**: Third-party service failures

## Dashboard Features

### Real-time Monitoring

The dashboard provides real-time project monitoring with:
- Live progress tracking
- Health status indicators
- Team performance metrics
- Risk assessment alerts
- Quality metrics visualization

### Customizable Layouts

Create personalized dashboard views:
```bash
# Create custom layout
autoprojectmanagement dashboard create-view --name "Developer View" --widgets "progress,quality,alerts"

# Share layouts with team
autoprojectmanagement dashboard share-view --name "Developer View" --format json
```

### Automated Reporting

Schedule regular reports:
```bash
# Daily reports at 9 AM
autoprojectmanagement dashboard schedule-report --type overview --schedule "0 9 * * *"

# Weekly reports on Monday
autoprojectmanagement dashboard schedule-report --type detailed --schedule "0 9 * * 1"
```

## Troubleshooting Guide

### Common Issues and Solutions

#### Dashboard Server Won't Start
```bash
# Check if port is available
autoprojectmanagement dashboard start --port 3001

# Install required dependencies
pip install fastapi uvicorn
```

#### Cannot Connect to API
```bash
# Check server status
autoprojectmanagement dashboard status

# Verify network connectivity
curl http://localhost:3000/api/v1/health
```

#### Task Management Errors
```bash
# List available projects
autoprojectmanagement status

# Check specific project tasks
autoprojectmanagement status <project_id>
```

### Performance Optimization

For better performance:
1. Use appropriate refresh rates (1000-60000ms)
2. Enable caching where available
3. Schedule resource-intensive operations during off-peak hours
4. Monitor system resources during heavy usage

## Best Practices

### CLI Usage
- Use `--verbose` flag when troubleshooting
- Always validate inputs before execution
- Regularly check system status with `autoprojectmanagement status`
- Use appropriate output formats for different use cases

### Dashboard Configuration
- Set appropriate refresh rates based on needs
- Create role-specific dashboard views
- Schedule regular data exports for backup
- Monitor system health through the dashboard

### Error Handling
- Implement proper input validation
- Use try-catch blocks for external service calls
- Log errors with appropriate severity levels
- Provide user-friendly error messages

## API Integration

The dashboard exposes RESTful APIs for integration:

```bash
# Health check
curl http://localhost:3000/api/v1/health

# Project overview
curl http://localhost:3000/api/v1/dashboard/overview?project_id=1

# Real-time metrics
curl http://localhost:3000/api/v1/dashboard/metrics?project_id=1&timeframe=24h
```

## Support Resources

- **Documentation**: https://github.com/AutoProjectManagement/AutoProjectManagement
- **Issue Tracking**: https://github.com/AutoProjectManagement/AutoProjectManagement/issues
- **Community Support**: GitHub Discussions

## Version Information

- Current Version: 1.0.0
- API Version: v1
- Minimum Python Version: 3.8+
- Dependencies: FastAPI, Uvicorn, Click, Requests

---

*For additional assistance, please refer to the comprehensive documentation or create an issue on GitHub.*
