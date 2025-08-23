# Usage Instructions

This document provides detailed instructions on how to use the AutoProjectManagement system effectively.

## System Overview

AutoProjectManagement is a comprehensive API-driven project management automation system that provides:
- Automated project tracking and monitoring
- Real-time dashboard with WebSocket support
- Progress reporting and analytics
- Risk assessment and management
- Quality assurance metrics
- Team performance tracking

## Getting Started

### Prerequisites
- Python 3.8+
- FastAPI and required dependencies
- Web browser for API documentation

### Starting the System

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API Server**:
   ```bash
   uvicorn autoprojectmanagement.api.app:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Access API Documentation**:
   - Open your browser and navigate to: `http://localhost:8000/docs`
   - Or use the ReDoc interface: `http://localhost:8000/redoc`

### API Authentication
The system currently uses a simple API key authentication (to be implemented in production):
- Include `X-API-Key` header in requests
- Default development key: `development-key`

## Key Features

### Project Management

#### Creating Projects
```bash
curl -X POST "http://localhost:8000/api/v1/projects" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: development-key" \
  -d '{
    "name": "My New Project",
    "description": "Project description here",
    "template": "standard"
  }'
```

#### Listing Projects
```bash
curl -X GET "http://localhost:8000/api/v1/projects?limit=10&offset=0" \
  -H "X-API-Key: development-key"
```

#### Getting Project Status
```bash
curl -X GET "http://localhost:8000/api/v1/projects/project-001/status" \
  -H "X-API-Key: development-key"
```

### Dashboard Features

#### Real-time Dashboard Overview
```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/overview?project_id=project-001" \
  -H "X-API-Key: development-key"
```

#### Dashboard Metrics
```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/metrics?project_id=project-001&timeframe=24h" \
  -H "X-API-Key: development-key"
```

#### Dashboard Alerts
```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/alerts?project_id=project-001" \
  -H "X-API-Key: development-key"
```

### Real-time WebSocket Integration

#### WebSocket Connection Example (JavaScript)
```javascript
const socket = new WebSocket('ws://localhost:8000/api/v1/dashboard/ws');

socket.onopen = function(event) {
  console.log('WebSocket connection established');
  
  // Subscribe to events
  socket.send(JSON.stringify({
    type: 'subscribe',
    event_types: ['progress_update', 'risk_alert', 'dashboard_update'],
    project_id: 'project-001'
  }));
};

socket.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Received update:', data);
  
  // Handle different event types
  switch(data.type) {
    case 'progress_update':
      updateProgress(data.data);
      break;
    case 'risk_alert':
      showAlert(data.data);
      break;
    case 'dashboard_update':
      refreshDashboard(data.data);
      break;
  }
};

socket.onclose = function(event) {
  console.log('WebSocket connection closed');
};
```

### Dashboard Layout Management

#### Saving Custom Layout
```bash
curl -X POST "http://localhost:8000/api/v1/dashboard/layout" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: development-key" \
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

#### Retrieving Layout
```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/layout?layout_type=custom" \
  -H "X-API-Key: development-key"
```

## Data Formats

### Supported Response Formats
The API supports multiple response formats:
- **JSON** (default): `?format=json`
- **Markdown**: `?format=markdown`
- **Table**: `?format=table`

Example:
```bash
curl -X GET "http://localhost:8000/api/v1/projects/project-001/status?format=markdown" \
  -H "X-API-Key: development-key"
```

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "error": "Bad Request",
  "detail": "Invalid parameter format",
  "timestamp": "2025-08-14T10:30:00.000Z"
}
```

#### 404 Not Found
```json
{
  "error": "Not Found",
  "detail": "Project 'project-001' not found",
  "timestamp": "2025-08-14T10:30:00.000Z"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "detail": "An unexpected error occurred",
  "timestamp": "2025-08-14T10:30:00.000Z"
}
```

### Logging and Debugging
- Check server logs for detailed error information
- Enable debug mode with `--log-level debug` when starting the server
- Logs are written to stdout and can be redirected to files

## Best Practices

### Project Management
1. **Use Descriptive Project Names**: Clear naming helps with organization
2. **Regular Status Checks**: Monitor project health frequently
3. **Set Realistic Timeframes**: Use appropriate timeframe parameters for metrics

### Dashboard Usage
1. **Customize Layouts**: Create layouts that match your monitoring needs
2. **Subscribe to Relevant Events**: Only subscribe to events you need to reduce bandwidth
3. **Handle Reconnections**: Implement reconnection logic for WebSocket connections

### API Usage
1. **Use Pagination**: For large datasets, use limit and offset parameters
2. **Cache Responses**: Cache frequently accessed data to reduce API calls
3. **Handle Rate Limiting**: Implement retry logic with exponential backoff

### Security Considerations
1. **Secure API Keys**: Never expose API keys in client-side code
2. **Validate Input**: Always validate and sanitize input parameters
3. **Use HTTPS**: In production, always use HTTPS for API communication

## Performance Tips

### Optimizing Dashboard Performance
1. **Adjust Refresh Rates**: Set appropriate refresh rates based on needs
2. **Use Efficient Queries**: Filter data to only what's necessary
3. **Implement Client-side Caching**: Cache data locally when possible

### WebSocket Optimization
1. **Batch Updates**: Combine multiple updates into single messages when possible
2. **Connection Pooling**: Reuse WebSocket connections
3. **Heartbeat Management**: Implement proper heartbeat handling

## Integration Examples

### Python Client Example
```python
import requests
import json

class AutoProjectManagementClient:
    def __init__(self, base_url="http://localhost:8000", api_key="development-key"):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    def get_project_status(self, project_id, format="json"):
        url = f"{self.base_url}/api/v1/projects/{project_id}/status?format={format}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def create_project(self, name, description=None, template=None):
        url = f"{self.base_url}/api/v1/projects"
        data = {
            "name": name,
            "description": description,
            "template": template
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

# Usage
client = AutoProjectManagementClient()
status = client.get_project_status("project-001")
print(status)
```

### JavaScript/TypeScript Example
```typescript
class AutoProjectManagementClient {
    private baseUrl: string;
    private apiKey: string;

    constructor(baseUrl: string = 'http://localhost:8000', apiKey: string = 'development-key') {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    }

    async getDashboardOverview(projectId: string): Promise<any> {
        const response = await fetch(
            `${this.baseUrl}/api/v1/dashboard/overview?project_id=${projectId}`,
            {
                headers: {
                    'X-API-Key': this.apiKey
                }
            }
        );
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return response.json();
    }

    // Additional methods for other endpoints
}

// Usage
const client = new AutoProjectManagementClient();
const overview = await client.getDashboardOverview('project-001');
console.log(overview);
```

## Troubleshooting

### Common Issues

#### API Server Not Starting
- Check if port 8000 is available
- Verify all dependencies are installed
- Check Python version compatibility

#### WebSocket Connection Issues
- Verify CORS settings
- Check firewall configurations
- Ensure WebSocket protocol support

#### Performance Problems
- Monitor server resource usage
- Check database connection pooling
- Review query optimization

### Getting Help

1. **Check Documentation**: Always refer to the API documentation first
2. **Review Logs**: Server logs contain detailed error information
3. **Community Support**: Check GitHub issues and discussions
4. **Contact Support**: For critical issues, contact the development team

## Support and Resources

- **API Documentation**: `http://localhost:8000/docs`
- **GitHub Repository**: https://github.com/AutoProjectManagement/AutoProjectManagement
- **Issue Tracker**: GitHub Issues page
- **Community Forum**: GitHub Discussions

---

This usage instructions document will be updated as new features are added to the AutoProjectManagement system.
