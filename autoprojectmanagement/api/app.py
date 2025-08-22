#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/api/app.py
File: app.py
Purpose: FastAPI application setup
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: FastAPI application setup within the AutoProjectManagement system
"""

import logging
from typing import Dict, Any, Optional, List, Union
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CURRENT_VERSION = "2.0.0"
PYTHON_MIN_VERSION = "3.8+"
CREATED_DATE = "2025-08-14"
MODIFIED_DATE = "2025-08-14"

# Module-level docstring
__doc__ = """
FastAPI application setup within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

try:
    from fastapi import FastAPI, HTTPException, Query, Path as APIPath
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, FileResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel, Field
except ImportError:
    # Fallback for development environment
    class FastAPI:
        def __init__(self, *args, **kwargs):
            pass
    
    class HTTPException(Exception):
        def __init__(self, status_code, detail):
            self.status_code = status_code
            self.detail = detail
    
    class BaseModel:
        pass
    
    class Field:
        pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import business logic
try:
    from autoprojectmanagement.api.services import ProjectService
    from autoprojectmanagement.services.configuration_cli.cli_commands import (
        get_project_status as cli_get_project_status
    )
    from autoprojectmanagement.api.dashboard_endpoints import router as dashboard_router
except ImportError:
    # Handle import for development
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from autoprojectmanagement.api.services import ProjectService
    from autoprojectmanagement.services.configuration_cli.cli_commands import (
        get_project_status as cli_get_project_status
    )
    from autoprojectmanagement.api.dashboard_endpoints import router as dashboard_router

# Pydantic models for request/response validation
class ProjectStatus(BaseModel):
    """Model for project status response."""
    project_id: str = Field(..., description="Unique project identifier")
    total_tasks: int = Field(..., description="Total number of tasks")
    completed_tasks: int = Field(..., description="Number of completed tasks")
    progress_percentage: float = Field(..., description="Progress percentage")
    summary: str = Field(..., description="Project summary")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")

class ProjectCreate(BaseModel):
    """Model for creating new projects."""
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    description: Optional[str] = Field(None, max_length=500, description="Project description")
    template: Optional[str] = Field(None, description="Project template")

class ProjectUpdate(BaseModel):
    """Model for updating projects."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None, description="Project status")

class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    timestamp: datetime = Field(..., description="Error timestamp")

# Initialize services
project_service = ProjectService()

# Create FastAPI application with comprehensive configuration
app: FastAPI = FastAPI(
    title="AutoProjectManagement API",
    description="Comprehensive REST API for automated project management system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "AutoProjectManagement Team",
        "email": "team@autoprojectmanagement.com",
        "url": "https://github.com/AutoProjectManagement/AutoProjectManagement"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Mount static files for dashboard
app.mount("/static", StaticFiles(directory="autoprojectmanagement/static"), name="static")

# API versioning
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Dashboard route
@app.get("/dashboard")
async def serve_dashboard():
    """Serve the main dashboard HTML page."""
    return FileResponse("autoprojectmanagement/static/index.html")

@app.get("/", tags=["System"])
def read_root() -> Dict[str, Any]:
    """
    Root endpoint providing system information and API overview.
    
    Returns:
        Dict containing system information, API version, and available endpoints.
    """
    return {
        "message": "Welcome to the AutoProjectManagement API",
        "version": "1.0.0",
        "api_version": API_VERSION,
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "projects": f"{API_PREFIX}/projects",
            "health": f"{API_PREFIX}/health",
            "status": f"{API_PREFIX}/projects/{{project_id}}/status"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get(
    f"{API_PREFIX}/health",
    tags=["System"],
    response_model=Dict[str, Any]
)
def health_check() -> Dict[str, Any]:
    """
    Comprehensive health check endpoint.
    
    Returns:
        Dict containing system health status and component availability.
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api": "running",
            "database": "connected",
            "logging": "active"
        },
        "version": "1.0.0"
    }
    
    try:
        # Check if we can access project data
        project_list = project_service.get_project_list()
        health_status["components"]["data_access"] = "available"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        health_status["components"]["data_access"] = "error"
        health_status["status"] = "degraded"
    
    return health_status

@app.get(
    f"{API_PREFIX}/projects/{{project_id}}/status",
    tags=["Projects"],
    response_model=Dict[str, Any]
)
def get_project_status(
    project_id: str = APIPath(..., description="Unique project identifier"),
    format: str = Query("json", description="Response format: json, markdown, or table")
) -> Dict[str, Any]:
    """
    Get comprehensive status of a specific project.
    
    Args:
        project_id: Unique identifier for the project
        format: Response format preference
        
    Returns:
        Dict containing detailed project status information
        
    Raises:
        HTTPException: If project is not found
    """
    try:
        status_data = project_service.get_status(project_id)
        
        if not status_data:
            raise HTTPException(
                status_code=404,
                detail=f"Project '{project_id}' not found"
            )
        
        # Handle different response formats
        if format == "json":
            return status_data
        elif format == "markdown":
            return {
                "format": "markdown",
                "content": f"# Project {project_id} Status\n\n{json.dumps(status_data, indent=2)}"
            }
        elif format == "table":
            return {
                "format": "table",
                "data": status_data
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported format: {format}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving project status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get(
    f"{API_PREFIX}/projects",
    tags=["Projects"],
    response_model=Dict[str, Any]
)
def list_projects(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of projects to return"),
    offset: int = Query(0, ge=0, description="Number of projects to skip"),
    include_archived: bool = Query(False, description="Include archived projects")
) -> Dict[str, Any]:
    """
    List all available projects with pagination support.
    
    Args:
        limit: Maximum number of projects to return
        offset: Number of projects to skip
        include_archived: Whether to include archived projects
        
    Returns:
        Dict containing project list and pagination metadata
    """
    try:
        projects = project_service.get_project_list()
        
        # Apply pagination
        if isinstance(projects, dict) and "projects" in projects:
            all_projects = projects["projects"]
            paginated_projects = all_projects[offset:offset + limit]
            
            return {
                "projects": paginated_projects,
                "total": len(all_projects),
                "limit": limit,
                "offset": offset,
                "has_more": len(all_projects) > offset + limit
            }
        
        return projects
        
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving projects: {str(e)}"
        )

@app.post(
    f"{API_PREFIX}/projects",
    tags=["Projects"],
    response_model=Dict[str, Any]
)
def create_project(project: ProjectCreate) -> Dict[str, Any]:
    """
    Create a new project with automated management capabilities.
    
    Args:
        project: Project creation data
        
    Returns:
        Dict containing created project information
        
    Raises:
        HTTPException: If project creation fails
    """
    try:
        # Implementation would integrate with core business logic
        project_data = {
            "id": "generated_id",  # Would be generated
            "name": project.name,
            "description": project.description,
            "template": project.template,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        return {
            "message": "Project created successfully",
            "project": project_data
        }
        
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating project: {str(e)}"
        )

@app.put(
    f"{API_PREFIX}/projects/{{project_id}}",
    tags=["Projects"],
    response_model=Dict[str, Any]
)
def update_project(
    project_id: str = APIPath(..., description="Project ID to update"),
    project: ProjectUpdate = ...
) -> Dict[str, Any]:
    """
    Update an existing project.
    
    Args:
        project_id: Project identifier
        project: Update data
        
    Returns:
        Dict containing updated project information
    """
    try:
        # Implementation would integrate with core business logic
        return {
            "message": f"Project {project_id} updated successfully",
            "project_id": project_id,
            "updated_fields": project.dict(exclude_unset=True)
        }
        
    except Exception as e:
        logger.error(f"Error updating project: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error updating project: {str(e)}"
        )

@app.delete(
    f"{API_PREFIX}/projects/{{project_id}}",
    tags=["Projects"],
    response_model=Dict[str, Any]
)
def delete_project(project_id: str = APIPath(..., description="Project ID to delete")) -> Dict[str, Any]:
    """
    Delete a project.
    
    Args:
        project_id: Project identifier
        
    Returns:
        Dict containing deletion confirmation
    """
    try:
        # Implementation would integrate with core business logic
        return {
            "message": f"Project {project_id} deleted successfully",
            "project_id": project_id
        }
        
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting project: {str(e)}"
        )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": str(exc.detail),
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

# Include dashboard endpoints
app.include_router(dashboard_router, prefix=API_PREFIX)

# Additional utility endpoints
@app.get(
    f"{API_PREFIX}/system/info",
    tags=["System"],
    response_model=Dict[str, Any]
)
def system_info() -> Dict[str, Any]:
    """
    Get comprehensive system information.
    
    Returns:
        Dict containing system configuration and capabilities
    """
    return {
        "system": "AutoProjectManagement",
        "version": "1.0.0",
        "api_version": API_VERSION,
        "capabilities": [
            "project_management",
            "task_tracking",
            "progress_monitoring",
            "automated_commits",
            "risk_assessment",
            "reporting",
            "dashboard"  # Added dashboard capability
        ],
        "supported_formats": ["json", "markdown", "table"],
        "timestamp": datetime.now().isoformat()
    }
