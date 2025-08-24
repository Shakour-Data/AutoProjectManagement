# User Guide

## Overview
This guide provides comprehensive instructions for using the AutoProjectManagement system. It covers installation, configuration, and usage of all system features.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [API Usage](#api-usage)
- [Dashboard Features](#dashboard-features)
- [Real-time Updates](#real-time-updates)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for source installation)

### Installation Methods

#### Method 1: From Source
```bash
# Clone the repository
git clone https://github.com/AutoProjectManagement/AutoProjectManagement.git
cd AutoProjectManagement

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Method 2: Using Docker
```bash
# Build the Docker image
docker build -t autoprojectmanagement .

# Run the container
docker run -p 8000:8000 autoprojectmanagement
```

#### Method 3: Using pip
```bash
pip install fastapi uvicorn python-multipart
```

### Starting the Server

```bash
# Start the development server
uvicorn autoprojectmanagement.api.app:app --host 0.0.0.0 --port 8000 --reload

# Start production server
uvicorn autoprojectmanagement.api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

## Configuration

### Environment Variables
Set the following environment variables for configuration:

```bash
export API_KEY=your-api-key
export DATABASE_URL=sqlite:///./autoprojectmanagement.db
export LOG_LEVEL=INFO
export CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Configuration File
Create a `config.json` file in the project root:

```json
{
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": false
  },
  "database": {
    "url": "sqlite:///./autoprojectmanagement.db",
    "echo": false
  },
  "security": {
    "api_key": "development-key",
    "cors_origins": ["http://localhost:3000", "http://localhost:8000"]
  }
}
```

## API Usage

### Base URL
All API endpoints are prefixed with:
```
http://localhost:8000/api/v1
```

### Authentication
Include the API key in requests:
```bash
curl -H "X-API-Key: development-key" http://localhost:8000/api/v1/health
```

### Core API Endpoints

#### System Endpoints
```bash
# Health check
curl http://localhost:8000/api/v1/health

# System information
curl http://localhost:8000/api/v1/system/info

# Root endpoint
curl http://localhost:8000/
```

#### Project Management
```bash
# List projects
curl http://localhost:8000/api/v1/projects?limit=10

# Create project
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project", "description": "Project description"}'

# Get project status
curl http://localhost:8000/api/v1/projects/project-001/status
```

#### Dashboard Endpoints
```bash
# Dashboard overview
curl http://localhost:8000/api/v1/dashboard/overview?project_id=project-001

# Dashboard metrics
curl http://localhost:8000/api/v1/dashboard/metrics?project_id=project-001

# Dashboard alerts
curl http://localhost:8000/api/v1/dashboard/alerts?project_id=project-001
```

### Response Formats
The API supports multiple response formats:
```bash
# JSON (default)
curl http://localhost:8000/api/v1/projects/project-001/status

# Markdown
curl http://localhost:8000/api/v1/projects/project-001/status?format=markdown

# Table format
curl http://localhost:8000/api/v1/projects/project-001/status?format=table
```

## Dashboard Features

### Overview Dashboard
The overview dashboard provides:
- Project health score
- Progress tracking
- Risk assessment
- Team performance metrics
- Quality metrics

### Custom Layouts
Create custom dashboard layouts:
```bash
curl -X POST http://localhost:8000/api/v1/dashboard/layout \
  -H "Content-Type: application/json" \
  -d '{
    "layout_type": "custom",
    "widgets": [
      {"widget_id": "health", "position": 0, "enabled": true},
      {"widget_id": "progress", "position": 1, "enabled": true},
      {"widget_id": "alerts", "position": 2, "enabled": true}
    ],
    "refresh_rate": 5000,
    "theme": "dark"
  }'
```

### Available Widgets
- `health`: Project health monitoring
- `progress`: Progress tracking and visualization
- `risks`: Risk assessment and management
- `team`: Team performance metrics
- `quality`: Quality assurance metrics
- `alerts`: Real-time alert notifications

## Real-time Updates

### WebSocket Integration
```javascript
const socket = new WebSocket('ws://localhost:8000/api/v1/dashboard/ws');

socket.onopen = () => {
    console.log('Connected to AutoProjectManagement WebSocket');
    
    // Subscribe to events
    socket.send(JSON.stringify({
        type: 'subscribe',
        event_types: ['progress_update', 'risk_alert', 'dashboard_update'],
        project_id: 'project-001'
    }));
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Real-time update:', data);
};
```

### Server-Sent Events (SSE)
```javascript
const eventSource = new EventSource('/api/v1/sse/events?event_types=progress_update,risk_alert&project_id=project-001');

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('SSE update:', data);
};

eventSource.onerror = (error) => {
    console.error('SSE error:', error);
};
```

### Supported Event Types
- `progress_update`: Task progress updates
- `risk_alert`: Risk assessment alerts
- `dashboard_update`: Dashboard data refresh
- `health_check`: System health updates
- `quality_metric`: Quality assurance updates
- `team_performance`: Team performance updates
- `system_status`: System status changes

## Troubleshooting

### Common Issues

#### API Connection Issues
- Verify the server is running: `curl http://localhost:8000/api/v1/health`
- Check API key configuration
- Verify CORS settings

#### WebSocket Connection Issues
- Check WebSocket URL: `ws://localhost:8000/api/v1/dashboard/ws`
- Verify event types are valid
- Check browser console for errors

#### Data Loading Issues
- Verify database connection
- Check data file permissions
- Review application logs

### Logging
Enable debug logging for troubleshooting:
```bash
export LOG_LEVEL=DEBUG
uvicorn autoprojectmanagement.api.app:app --host 0.0.0.0 --port 8000 --reload
```

### Getting Help
1. Check the [API Documentation](http://localhost:8000/docs)
2. Review the [Troubleshooting Guide](Docs/SystemDesign/Guides/Maintenance_and_Troubleshooting_Guide.md)
3. Search [GitHub Issues](https://github.com/AutoProjectManagement/AutoProjectManagement/issues)
4. Create a new issue if your problem isn't documented

## Best Practices

### Performance Optimization
- Use appropriate pagination for large datasets
- Implement client-side caching
- Use WebSocket/SSE for real-time updates
- Optimize database queries

### Security Considerations
- Use HTTPS in production
- Rotate API keys regularly
- Implement rate limiting
- Validate all input data

### Monitoring and Alerting
- Monitor system health endpoints
- Set up alerting for critical events
- Track performance metrics
- Monitor error rates

---

*Last updated: 2025-08-14*
