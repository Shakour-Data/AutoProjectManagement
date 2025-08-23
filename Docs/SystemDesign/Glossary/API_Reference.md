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
    "projects": [
      {
        "id": "project-001",
        "name": "Sample Project",
        "description": "Sample project description",
        "status": "active",
        "created_at": "2025-08-14T10:00:00.000Z"
      }
    ],
    "total": 1,
    "limit": 100,
    "offset": 0,
    "has_more": false
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

---

## Dashboard Endpoints

### Dashboard Overview

#### Get Dashboard Overview
- **Method:** GET
- **Path:** /api/v1/dashboard/overview
- **Description:** Get comprehensive dashboard overview for a project
- **Parameters:**
  - `project_id` (query, string, required): Project ID for dashboard overview
- **Response:** 
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
- **Response:** 
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

#### Get Dashboard Health
- **Method:** GET
- **Path:** /api/v1/dashboard/health
- **Description:** Get comprehensive project health status for dashboard
- **Parameters:**
  - `project_id` (query, string, required): Project ID for health check
- **Response:** Detailed health assessment data

#### Get Team Performance
- **Method:** GET
- **Path:** /api/v1/dashboard/team-performance
- **Description:** Get team performance metrics for dashboard
- **Parameters:**
  - `project_id` (query, string, required): Project ID for team performance
- **Response:** Team performance statistics

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
      "widgets": [...],
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

#### Get Available Layouts
- **Method:** GET
- **Path:** /api/v1/dashboard/layouts
- **Description:** Get list of available layout configurations
- **Parameters:** None
- **Response:** List of layout type strings

#### Delete Dashboard Layout
- **Method:** DELETE
- **Path:** /api/v1/dashboard/layout/{layout_type}
- **Description:** Delete dashboard layout configuration
- **Parameters:**
  - `layout_type` (path, string, required): Layout type to delete
- **Response:** Success message

#### Get Available Widgets
- **Method:** GET
- **Path:** /api/v1/dashboard/widgets
- **Description:** Get list of available widgets
- **Parameters:** None
- **Response:** List of widget identifiers

### Real-time WebSocket Endpoints

#### WebSocket Connection
- **Protocol:** WebSocket
- **Path:** /api/v1/dashboard/ws
- **Description:** Real-time dashboard updates using event-driven architecture
- **Features:**
  - Live updates for all dashboard metrics
  - Event subscription system
  - Reconnection support with event replay
  - Heartbeat mechanism
  - Comprehensive error handling

#### WebSocket Statistics
- **Method:** GET
- **Path:** /api/v1/dashboard/ws/stats
- **Description:** Get WebSocket connection statistics
- **Parameters:** None
- **Response:** Connection statistics and metrics

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

#### ProjectCreate
- `name`: string (Project name, 1-100 characters)
- `description`: string (Project description, optional)
- `template`: string (Project template, optional)

#### ProjectUpdate
- `name`: string (Project name, optional)
- `description`: string (Project description, optional)
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
- `refresh_rate`: int (Refresh rate in milliseconds)
- `theme`: string (Theme: light, dark)
- `created_at`: datetime (Creation timestamp)
- `updated_at`: datetime (Last update timestamp)

#### WidgetPosition
- `widget_id`: string (Widget identifier)
- `position`: int (Position in layout, 0-based)
- `enabled`: bool (Whether widget is enabled)
- `settings`: Dict[str, Any] (Widget-specific settings)

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

## Event Types for WebSocket

The WebSocket connection supports subscription to these event types:
- `system_status`: System health and status updates
- `dashboard_update`: Dashboard data refresh events
- `health_check`: Health monitoring events
- `progress_update`: Task progress updates
- `risk_alert`: Risk assessment alerts
- `quality_metric`: Quality metric updates
- `team_performance`: Team performance updates

---

This concludes the API Reference Document for AutoProjectManagement system.
