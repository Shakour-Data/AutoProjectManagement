# API Reference Document

*Last updated: 2025-08-14*

This document provides a detailed reference for the backend API endpoints of the AutoProjectManagement system. It describes each endpoint's purpose, HTTP method, URL path, parameters, request body, and response.

## Base URL

All endpoints are prefixed with:

```
/api/v1
```

---

## System Endpoints

### Root Endpoint

#### Get System Information
- **Method:** GET
- **Path:** /
- **Description:** Root endpoint providing system information and API overview
- **Parameters:** None
- **Response:** 
  ```json
  {
    "message": "Welcome to the AutoProjectManagement API",
    "version": "1.0.0",
    "api_version": "v1",
    "documentation": {
      "swagger": "/docs",
      "redoc": "/redoc",
      "openapi": "/openapi.json"
    },
    "endpoints": {
      "projects": "/api/v1/projects",
      "health": "/api/v1/health",
      "status": "/api/v1/projects/{project_id}/status"
    },
    "timestamp": "2025-08-14T10:30:00.000Z"
  }
  ```

#### Health Check
- **Method:** GET
- **Path:** /api/v1/health
- **Description:** Comprehensive health check endpoint
- **Parameters:** None
- **Response:** 
  ```json
  {
    "status": "healthy",
    "timestamp": "2025-08-14T10:30:00.000Z",
    "components": {
      "api": "running",
      "database": "connected",
      "logging": "active",
      "data_access": "available"
    },
    "version": "1.0.0"
  }
  ```

#### System Information
- **Method:** GET
- **Path:** /api/v1/system/info
- **Description:** Get comprehensive system information
- **Parameters:** None
- **Response:** 
  ```json
  {
    "system": "AutoProjectManagement",
    "version": "1.0.0",
    "api_version": "v1",
    "capabilities": [
      "project_management",
      "task_tracking",
      "progress_monitoring",
      "automated_commits",
      "risk_assessment",
      "reporting"
    ],
    "supported_formats": ["json", "markdown", "table"],
    "timestamp": "2025-08-14T10:30:00.000Z"
  }
  ```

---

## Project Management Endpoints

### Project Operations

#### List Projects
- **Method:** GET
- **Path:** /api/v1/projects
- **Description:** List all available projects with pagination support
- **Parameters:**
  - `limit` (query, integer, optional, default=100): Maximum number of projects to return (1-1000)
  - `offset` (query, integer, optional, default=0): Number of projects to skip
  - `include_archived` (query, boolean, optional, default=false): Include archived projects
- **Response:** 
  ```json
  {
    "projects": [],
    "count": 0,
    "message": "Project listing not yet implemented"
  }
  ```

#### Create Project
- **Method:** POST
- **Path:** /api/v1/projects
- **Description:** Create a new project with automated management capabilities
- **Request Body:**
  ```json
  {
    "name": "New Project",
    "description": "Project description",
    "template": "standard"
  }
  ```
- **Response:** 
  ```json
  {
    "message": "Project created successfully",
    "project": {
      "id": "generated_id",
      "name": "New Project",
      "description": "Project description",
      "template": "standard",
      "created_at": "2025-08-14T10:30:00.000Z",
      "status": "active"
    }
  }
  ```

#### Update Project
- **Method:** PUT
- **Path:** /api/v1/projects/{project_id}
- **Description:** Update an existing project
- **Parameters:**
  - `project_id` (path, string, required): Project identifier
- **Request Body:**
  ```json
  {
    "name": "Updated Project Name",
    "description": "Updated description",
    "status": "active"
  }
  ```
- **Response:** 
  ```json
  {
    "message": "Project project-001 updated successfully",
    "project_id": "project-001",
    "updated_fields": {
      "name": "Updated Project Name",
      "description": "Updated description"
    }
  }
  ```

#### Delete Project
- **Method:** DELETE
- **Path:** /api/v1/projects/{project_id}
- **Description:** Delete a project
- **Parameters:**
  - `project_id` (path, string, required): Project identifier
- **Response:** 
  ```json
  {
    "message": "Project project-001 deleted successfully",
    "project_id": "project-001"
  }
  ```

#### Get Project Status
- **Method:** GET
- **Path:** /api/v1/projects/{project_id}/status
- **Description:** Get comprehensive status of a specific project
- **Parameters:**
  - `project_id` (path, string, required): Unique project identifier
  - `format` (query, string, optional, default=json): Response format (json, markdown, table)
- **Response:** Detailed project status information in requested format
- **Example Response (JSON):**
  ```json
  {
    "project_id": "project-001",
    "total_tasks": 100,
    "completed_tasks": 75,
    "progress_percentage": 75.0,
    "summary": "Project is in progress.",
    "source_file": "/path/to/task/database.json"
  }
  ```

---

## Dashboard Endpoints

### Dashboard Overview

#### Get Dashboard Overview
- **Method:** GET
- **Path:** /api/v1/dashboard/overview
- **Description:** Get comprehensive dashboard overview for a project
- **Parameters:**
  - `project_id` (query, string, required): Project ID for dashboard overview
- **Response:** DashboardOverview model
- **Example Response:**
  ```json
  {
    "project_id": "project-001",
    "total_tasks": 100,
    "completed_tasks": 75,
    "progress_percentage": 75.0,
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

#### Get Dashboard Metrics
- **Method:** GET
- **Path:** /api/v1/dashboard/metrics
- **Description:** Get detailed metrics and trends for dashboard visualization
- **Parameters:**
  - `project_id` (query, string, required): Project ID for metrics
  - `timeframe` (query, string, optional, default="24h"): Timeframe for metrics (1h, 24h, 7d, 30d)
- **Response:** DashboardMetrics model
- **Example Response:**
  ```json
  {
    "timestamp": "2025-08-14T10:30:00.000Z",
    "metrics": {
      "velocity": 25,
      "throughput": 18,
      "cycle_time": 2.5,
      "lead_time": 4.2
    },
    "trends": {
      "velocity": [20, 22, 25, 23, 26],
      "throughput": [15, 16, 18, 17, 19]
    }
  }
  ```

#### Get Dashboard Alerts
- **Method:** GET
- **Path:** /api/v1/dashboard/alerts
- **Description:** Get active alerts and notifications for the dashboard
- **Parameters:**
  - `project_id` (query, string, optional): Filter alerts by project ID
  - `severity` (query, string, optional): Filter by severity
  - `resolved` (query, boolean, optional, default=false): Include resolved alerts
- **Response:** List of DashboardAlert objects
- **Example Response:**
  ```json
  [
    {
      "id": "alert-001",
      "type": "risk",
      "severity": "warning",
      "message": "Progress slowing down in sprint",
      "timestamp": "2025-08-14T10:30:00.000Z",
      "project_id": "project-001",
      "resolved": false
    }
  ]
  ```

#### Get Dashboard Health
- **Method:** GET
- **Path:** /api/v1/dashboard/health
- **Description:** Get comprehensive project health status for dashboard
- **Parameters:**
  - `project_id` (query, string, required): Project ID for health check
- **Response:** Detailed health assessment data
- **Example Response:**
  ```json
  {
    "overall_health": 85,
    "components": {
      "code_quality": "healthy",
      "test_coverage": "degraded",
      "documentation": "healthy",
      "deployment": "healthy"
    }
  }
  ```

#### Get Team Performance
- **Method:** GET
- **Path:** /api/v1/dashboard/team-performance
- **Description:** Get team performance metrics for dashboard
- **Parameters:**
  - `project_id` (query, string, required): Project ID for team performance
- **Response:** Team performance statistics
- **Example Response:**
  ```json
  {
    "team_velocity": 25,
    "individual_performance": {
      "developer1": 95,
      "developer2": 88,
      "developer3": 92
    }
  }
  ```

### Dashboard Layout Management

#### Save Dashboard Layout
- **Method:** POST
- **Path:** /api/v1/dashboard/layout
- **Description:** Save dashboard layout configuration
- **Request Body:** DashboardLayout object
- **Response:** 
  ```json
  {
    "message": "Layout saved successfully",
    "layout": {
      "layout_type": "standard",
      "widgets": [
        {
          "widget_id": "health",
          "position": 0,
          "enabled": true,
          "settings": {}
        }
      ],
      "refresh_rate": 3000,
      "theme": "light",
      "created_at": "2025-08-14T10:30:00.000Z",
      "updated_at": "2025-08-14T10:30:00.000Z"
    }
  }
  ```

#### Get Dashboard Layout
- **Method:** GET
- **Path:** /api/v1/dashboard/layout
- **Description:** Get saved dashboard layout configuration
- **Parameters:**
  - `layout_type` (query, string, optional, default="standard"): Layout type to retrieve
- **Response:** DashboardLayout object
- **Example Response:**
  ```json
  {
    "layout_type": "standard",
    "widgets": [
      {
        "widget_id": "health",
        "position": 0,
        "enabled": true,
        "settings": {}
      }
    ],
    "refresh_rate": 3000,
    "theme": "light",
    "created_at": "2025-08-14T10:30:00.000Z",
    "updated_at": "2025-08-14T10:30:00.000Z"
  }
  ```

#### Get Available Layouts
- **Method:** GET
- **Path:** /api/v1/dashboard/layouts
- **Description:** Get list of available layout configurations
- **Parameters:** None
- **Response:** List of layout type strings
- **Example Response:**
  ```json
  ["standard", "minimal", "custom"]
  ```

#### Delete Dashboard Layout
- **Method:** DELETE
- **Path:** /api/v1/dashboard/layout/{layout_type}
- **Description:** Delete dashboard layout configuration
- **Parameters:**
  - `layout_type` (path, string, required): Layout type to delete
- **Response:** Success message
- **Example Response:**
  ```json
  {
    "message": "Layout 'standard' deleted successfully"
  }
  ```

#### Get Available Widgets
- **Method:** GET
- **Path:** /api/v1/dashboard/widgets
- **Description:** Get list of available widgets
- **Parameters:** None
- **Response:** List of widget identifiers
- **Example Response:**
  ```json
  ["health", "progress", "risks", "team", "quality", "alerts"]
  ```

### Real-time WebSocket Endpoints

#### WebSocket Connection
- **Protocol:** WebSocket
- **Path:** /api/v1/dashboard/ws
- **Description:** Real-time dashboard updates using event-driven architecture
- **Features:**
  - Live updates for all dashboard metrics
  - Event subscription system
  - Reconnection support with event replay
  - Heartbeat mechanism (every 30 seconds)
  - Comprehensive error handling
- **Supported Event Types:**
  - `system_status`: System health and status updates
  - `dashboard_update`: Dashboard data refresh events
  - `health_check`: Health monitoring events
  - `progress_update`: Task progress updates
  - `risk_alert`: Risk assessment alerts
  - `quality_metric`: Quality metric updates
  - `team_performance`: Team performance updates

#### WebSocket Statistics
- **Method:** GET
- **Path:** /api/v1/dashboard/ws/stats
- **Description:** Get WebSocket connection statistics
- **Parameters:** None
- **Response:** Connection statistics and metrics
- **Example Response:**
  ```json
  {
    "total_connections": 5,
    "failed_connections": 2,
    "reconnections": 3,
    "active_connections": 2,
    "event_service_stats": {
      "total_connections": 5,
      "active_connections": 2,
      "subscription_counts": {
        "dashboard_update": 2,
        "progress_update": 1
      },
      "message_queue_size": 0,
      "uptime_seconds": 3600
    }
  }
  ```

---

## Server-Sent Events (SSE) Endpoints

### SSE Events Stream
- **Method:** GET
- **Path:** /api/v1/sse/events
- **Description:** Server-Sent Events endpoint for real-time updates
- **Parameters:**
  - `event_types` (query, string, optional): Comma-separated event types to subscribe to
  - `project_id` (query, string, optional): Project ID filter
  - `last_event_id` (query, string, optional): Last received event ID for reconnection
- **Response:** Event stream with media type `text/event-stream`
- **Features:**
  - Browser-compatible real-time event streaming
  - Event type subscriptions
  - Project filtering
  - Reconnection support with last event ID
  - Heartbeat messages (every 30 seconds)
  - Automatic reconnection

### SSE Subscription Management
- **Method:** POST
- **Path:** /api/v1/sse/subscribe
- **Description:** Update SSE subscription for an existing connection
- **Parameters:**
  - `connection_id` (query, string, required): SSE connection ID
- **Request Body:** SSESubscriptionRequest model
- **Response:** Subscription confirmation
- **Example Request Body:**
  ```json
  {
    "event_types": ["dashboard_update", "progress_update"],
    "project_id": "project-001",
    "last_event_id": "event-12345"
  }
  ```

### SSE Statistics
- **Method:** GET
- **Path:** /api/v1/sse/stats
- **Description:** Get comprehensive SSE connection statistics
- **Parameters:** None
- **Response:** SSE connection statistics
- **Example Response:**
  ```json
  {
    "sse_connections": 3,
    "total_connections": 8,
    "subscription_counts": {
      "dashboard_update": 2,
      "progress_update": 1
    },
    "message_queue_size": 0,
    "uptime_seconds": 7200,
    "timestamp": "2025-08-14T10:30:00.000Z"
  }
  ```

### SSE Test Event
- **Method:** POST
- **Path:** /api/v1/sse/test-event
- **Description:** Send a test event to all SSE subscribers (for development/testing)
- **Parameters:**
  - `event_type` (query, string, required): Event type for test
  - `project_id` (query, string, optional): Project ID for test
- **Response:** Test event confirmation
- **Example Response:**
  ```json
  {
    "message": "Test dashboard_update event published",
    "project_id": "project-001",
    "timestamp": "2025-08-14T10:30:00.000Z",
    "event_id": "event-67890"
  }
  ```

### SSE Connections List
- **Method:** GET
- **Path:** /api/v1/sse/connections
- **Description:** List all active SSE connections with details
- **Parameters:** None
- **Response:** List of active SSE connections
- **Example Response:**
  ```json
  {
    "connections": [
      {
        "connection_id": "conn-12345",
        "connected_at": "2025-08-14T10:00:00.000Z",
        "last_activity": "2025-08-14T10:30:00.000Z",
        "subscriptions": ["dashboard_update", "progress_update"],
        "project_filter": "project-001"
      }
    ]
  }
  ```

---

## Data Models

### Project Models

#### ProjectStatus
- `project_id`: string (Unique project identifier)
- `total_tasks`: int (Total number of tasks)
- `completed_tasks`: int (Number of completed tasks)
- `progress_percentage`: float (Progress percentage)
- `summary`: string (Project summary)
- `last_updated`: datetime (Last update timestamp)
- `source_file`: string (Path to task database file)

#### ProjectCreate
- `name`: string (Project name, 1-100 characters)
- `description`: string (Project description, optional, max 500 characters)
- `template`: string (Project template, optional)

#### ProjectUpdate
- `name`: string (Project name, optional, 1-100 characters)
- `description`: string (Project description, optional, max 500 characters)
- `status`: string (Project status, optional)

### Dashboard Models

#### DashboardOverview
- `project_id`: string (Unique project identifier)
- `total_tasks`: int (Total number of tasks)
- `completed_tasks`: int (Number of completed tasks)
- `progress_percentage`: float (Progress percentage)
- `health_score`: float (Project health score 0-100)
- `risk_level`: string (Risk level: low, medium, high, critical)
- `last_updated`: datetime (Last update timestamp)
- `team_performance`: float (Team performance score)
- `quality_metrics`: Dict[str, float] (Quality metrics)

#### DashboardMetrics
- `timestamp`: datetime (Metrics timestamp)
- `metrics`: Dict[str, Any] (Comprehensive metrics data)
- `trends`: Dict[str, List[float]] (Historical trends)

#### DashboardAlert
- `id`: string (Alert identifier)
- `type`: string (Alert type: risk, progress, quality, team)
- `severity`: string (Severity: info, warning, error, critical)
- `message`: string (Alert message)
- `timestamp`: datetime (Alert timestamp)
- `project_id`: string (Affected project ID)
- `resolved`: bool (Whether alert is resolved)

#### DashboardLayout
- `layout_type`: string (Layout type: standard, minimal, custom)
- `widgets`: List[WidgetPosition] (List of widget positions)
- `refresh_rate`: int (Refresh rate in milliseconds, 1000-60000)
- `theme`: string (Theme: light, dark)
- `created_at`: datetime (Creation timestamp)
- `updated_at`: datetime (Last update timestamp)

#### WidgetPosition
- `widget_id`: string (Widget identifier)
- `position`: int (Position in layout, 0-based)
- `enabled`: bool (Whether widget is enabled)
- `settings`: Dict[str, Any] (Widget-specific settings)

### SSE Models

#### SSESubscriptionRequest
- `event_types`: List[str] (Event types to subscribe to)
- `project_id`: string (Project ID filter, optional)
- `last_event_id`: string (Last received event ID for reconnection, optional)

### Error Models

#### ErrorResponse
- `error`: string (Error message)
- `detail`: string (Error details, optional)
- `timestamp`: datetime (Error timestamp)

---

## Available Widgets

The dashboard supports the following widgets:
- `health`: Project health monitoring
- `progress`: Progress tracking and visualization
- `risks`: Risk assessment and management
- `team`: Team performance metrics
- `quality`: Quality assurance metrics
- `alerts`: Real-time alert notifications

---

## Event Types for Real-time Communication

Both WebSocket and SSE support subscription to these event types:
- `system_status`: System health and status updates
- `dashboard_update`: Dashboard data refresh events
- `health_check`: Health monitoring events
- `progress_update`: Task progress updates
- `risk_alert`: Risk assessment alerts
- `quality_metric`: Quality metric updates
- `team_performance`: Team performance updates

---

## Error Handling

### Common HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

### Error Response Format
All error responses follow the same format:
```json
{
  "error": "Error message describing what went wrong",
  "detail": "Additional error details (optional)",
  "timestamp": "2025-08-14T10:30:00.000Z"
}
```

### Common Error Scenarios
1. **Project Not Found**: When requesting status for a non-existent project
2. **Invalid Format**: When requesting an unsupported response format
3. **Database Error**: When unable to read task database files
4. **Subscription Error**: When subscribing to invalid event types
5. **Connection Error**: When WebSocket/SSE connection fails

---

## Rate Limiting and Quotas

- **API Rate Limit**: 100 requests per minute per IP address
- **WebSocket Connections**: Maximum 50 concurrent connections
- **SSE Connections**: Maximum 100 concurrent connections
- **Event History**: Last 1000 events stored for reconnection

---

## Authentication and Security

- **API Key**: Required for all endpoints (configured via environment variables)
- **CORS**: Enabled for all origins in development, configurable for production
- **HTTPS**: Required for production deployments
- **Data Validation**: All input data validated using Pydantic models

---

## Versioning

The API follows semantic versioning:
- **Major version**: Breaking changes
- **Minor version**: New features (backward compatible)
- **Patch version**: Bug fixes (backward compatible)

Current API version: **v1**

---

## Response Formats

The API supports multiple response formats:
- **JSON**: Default format for all endpoints
- **Markdown**: Available for status endpoints
- **Table**: Available for status endpoints (experimental)

---

This concludes the API Reference Document for AutoProjectManagement system.

*Documentation last verified against implementation: 2025-08-14*
