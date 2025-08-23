### Dashboard Endpoints Module

- **Method:** N/A
- **Path:** `/api/v1/dashboard`
- **Description:** Dashboard-specific API endpoints for AutoProjectManagement.
- **Authentication:** Optional
- **Rate Limit:** N/A

#### Parameters
N/A

#### Response
**Success Response (200 OK):**
```json
{
  "message": "Dashboard endpoints available",
  "endpoints": {
    "overview": "/api/v1/dashboard/overview",
    "metrics": "/api/v1/dashboard/metrics",
    "alerts": "/api/v1/dashboard/alerts",
    "health": "/api/v1/dashboard/health",
    "team-performance": "/api/v1/dashboard/team-performance",
    "ws": "/api/v1/dashboard/ws",
    "ws/stats": "/api/v1/dashboard/ws/stats",
    "layout": "/api/v1/dashboard/layout",
    "layouts": "/api/v1/dashboard/layouts",
    "widgets": "/api/v1/dashboard/widgets"
  },
  "timestamp": "2025-08-14T10:30:00.000Z"
}
```

**Error Responses:**
- `500 Internal Server Error`: If there is an issue with the dashboard endpoints.

#### Example Request
```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/overview?project_id=123"
```

#### Example Response
```json
{
  "project_id": "123",
  "total_tasks": 100,
  "completed_tasks": 50,
  "progress_percentage": 50.0,
  "health_score": 85.0,
  "risk_level": "low",
  "last_updated": "2025-08-14T10:30:00.000Z",
  "team_performance": 90.0,
  "quality_metrics": {
    "test_coverage": 85.0,
    "code_quality": 88.0,
    "bug_density": 2.5
  }
}
```

#### Notes
- This module provides comprehensive dashboard API endpoints for real-time data, metrics, and project health monitoring.
- Ensure compatibility with Python 3.8+.
