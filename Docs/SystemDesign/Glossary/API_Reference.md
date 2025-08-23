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
