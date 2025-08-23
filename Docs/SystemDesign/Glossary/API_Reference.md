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
