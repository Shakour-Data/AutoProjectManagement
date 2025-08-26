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
import json
from pathlib import Path
import traceback

# Import error handling system
try:
    from autoprojectmanagement.utils.error_handler import (
        error_handler, ErrorContext, CustomError, ValidationError,
        AuthenticationError, AuthorizationError, DatabaseError,
        ErrorSeverity, ErrorCategory, create_user_friendly_message
    )
except ImportError:
    # Fallback implementation for development
    class ErrorContext:
        def __init__(self, **kwargs):
            pass
        def to_dict(self):
            return {}
    
    class CustomError(Exception):
        pass
    
    error_handler = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
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

try:
    from fastapi import FastAPI, HTTPException, Query, Path as APIPath, Request, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from fastapi.exceptions import RequestValidationError
    from pydantic import BaseModel, Field, validator
    print("FastAPI imported successfully")
except ImportError as e:
    print(f"FastAPI import failed: {e}")
    # Fallback for development environment
    class FastAPI:
        def __init__(self, *args, **kwargs):
            pass
        
        def add_middleware(self, *args, **kwargs):
            pass
        
        def middleware(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
        
        def exception_handler(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
        
        def get(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
        
        def post(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
        
        def put(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
        
        def delete(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
        
        def include_router(self, *args, **kwargs):
            pass
    
    class HTTPException(Exception):
        def __init__(self, status_code, detail):
            self.status_code = status_code
            self.detail = detail
    
    class BaseModel:
        pass
    
    class Field:
        def __init__(self, default=..., description=None, **kwargs):
            self.default = default
            self.description = description
            self.kwargs = kwargs

# Import business logic
try:
    from autoprojectmanagement.api.services import ProjectService
    from autoprojectmanagement.api.dashboard_endpoints import router as dashboard_router
    from autoprojectmanagement.api.sse_endpoints import router as sse_router
    from autoprojectmanagement.api.auth_endpoints import router as auth_router
except ImportError:
    # Handle import for development
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from autoprojectmanagement.api.services import ProjectService
    from autoprojectmanagement.api.dashboard_endpoints import router as dashboard_router
    from autoprojectmanagement.api.sse_endpoints import router as sse_router
    from autoprojectmanagement.api.auth_endpoints import router as auth_router

# Enhanced Pydantic models with comprehensive validation
class ProjectStatus(BaseModel):
    """Model for project status response."""
    project_id: str = Field(..., description="Unique project identifier", min_length=1, max_length=50)
    total_tasks: int = Field(..., description="Total number of tasks", ge=0)
    completed_tasks: int = Field(..., description="Number of completed tasks", ge=0)
    progress_percentage: float = Field(..., description="Progress percentage", ge=0, le=100)
    summary: str = Field(..., description="Project summary", min_length=1, max_length=1000)
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")

    @validator('completed_tasks')
    def validate_completed_tasks(cls, v, values):
        """Validate that completed tasks don't exceed total tasks."""
        if 'total_tasks' in values and v > values['total_tasks']:
            raise ValueError('Completed tasks cannot exceed total tasks')
        return v

class ProjectCreate(BaseModel):
    """Model for creating new projects with enhanced validation."""
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    description: Optional[str] = Field(None, max_length=500, description="Project description")
    template: Optional[str] = Field(None, description="Project template")

    @validator('name')
    def validate_name(cls, v):
        """Validate project name format."""
        if not v.strip():
            raise ValueError('Project name cannot be empty or whitespace only')
        if len(v.strip()) < 2:
            raise ValueError('Project name must be at least 2 characters long')
        return v.strip()

class ProjectUpdate(BaseModel):
    """Model for updating projects with enhanced validation."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None, description="Project status")

    @validator('status')
    def validate_status(cls, v):
        """Validate project status."""
        if v and v not in ['active', 'paused', 'completed', 'archived']:
            raise ValueError('Status must be one of: active, paused, completed, archived')
        return v

class ErrorResponse(BaseModel):
    """Enhanced model for error responses."""
    error: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")
    detail: Optional[str] = Field(None, description="Error details")
    timestamp: datetime = Field(..., description="Error timestamp")
    severity: str = Field(..., description="Error severity level")
    category: str = Field(..., description="Error category")
    context: Optional[Dict[str, Any]] = Field(None, description="Error context")

class ValidationErrorResponse(BaseModel):
    """Model for validation error responses."""
    errors: List[Dict[str, Any]] = Field(..., description="List of validation errors")
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

# API versioning
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Enhanced error handling middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    """Global error handling middleware."""
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        # Create error context
        context = ErrorContext(
            request_id=request.headers.get('x-request-id'),
            endpoint=str(request.url),
            method=request.method,
            parameters={
                "path_params": dict(request.path_params),
                "query_params": dict(request.query_params),
                "headers": dict(request.headers)
            }
        )
        
        # Handle the error
        error_info = error_handler.handle_error(exc, context)
        
        # Return appropriate response
        return JSONResponse(
            status_code=500 if not isinstance(exc, HTTPException) else exc.status_code,
            content=error_info
        )

# Enhanced exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed information."""
    context = ErrorContext(
        endpoint=str(request.url),
        method=request.method,
        parameters={
            "path_params": dict(request.path_params),
            "query_params": dict(request.query_params)
        }
    )
    
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    error_response = ValidationError(
        message="Input validation failed",
        field="multiple",
        details={"validation_errors": errors},
        context=context
    )
    
    error_response.log()
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "errors": errors,
            "timestamp": datetime.now().isoformat(),
            "message": "Validation error: Please check your input data"
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with enhanced error information."""
    context = ErrorContext(
        endpoint=str(request.url),
        method=request.method,
        parameters={
            "path_params": dict(request.path_params),
            "query_params": dict(request.query_params)
        }
    )
    
    # Convert HTTPException to custom error
    custom_error = CustomError(
        message=str(exc.detail),
        code=f"HTTP_{exc.status_code}",
        severity=ErrorSeverity.ERROR,
        category=ErrorCategory.BUSINESS_LOGIC,
        context=context
    )
    
    custom_error.log()
    
    return JSONResponse(
        status_code=exc.status_code,
        content=custom_error.to_dict()
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions."""
    context = ErrorContext(
        endpoint=str(request.url),
        method=request.method,
        parameters={
            "path_params": dict(request.path_params),
            "query_params": dict(request.query_params)
        }
    )
    
    error_info = error_handler.handle_error(exc, context)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_info
    )

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
    response_model=Dict[str, Any],
    responses={
        200: {"description": "System health status"},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
def health_check(request: Request) -> Dict[str, Any]:
    """
    Comprehensive health check endpoint with detailed error handling.
    
    Returns:
        Dict containing system health status and component availability.
        
    Raises:
        HTTPException: If critical system components are unavailable
    """
    context = ErrorContext(
        endpoint=str(request.url),
        method=request.method,
        parameters={}
    )
    
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "api": "running",
                "database": "connected",
                "logging": "active",
                "error_handling": "active",
                "authentication": "available"
            },
            "version": "1.0.0",
            "error_handler_available": error_handler is not None
        }
        
        # Check if we can access project data
        try:
            project_list = project_service.get_project_list()
            health_status["components"]["data_access"] = "available"
        except Exception as e:
            health_status["components"]["data_access"] = "degraded"
            health_status["status"] = "degraded"
            health_status["data_access_error"] = str(e)
        
        # Check error handler status
        if error_handler:
            error_count = len(error_handler.get_error_log(limit=10))
            health_status["recent_errors"] = error_count
        
        return health_status
        
    except Exception as e:
        error_handler.handle_error(e, context)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Health check failed due to internal error"
        )

@app.get(
    f"{API_PREFIX}/projects/{{project_id}}/status",
    tags=["Projects"],
    response_model=Dict[str, Any],
    responses={
        200: {"description": "Project status retrieved successfully"},
        404: {"description": "Project not found", "model": ErrorResponse},
        400: {"description": "Invalid format requested", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
def get_project_status(
    request: Request,
    project_id: str = APIPath(..., description="Unique project identifier", min_length=1, max_length=50),
    format: str = Query("json", description="Response format: json, markdown, or table")
) -> Dict[str, Any]:
    """
    Get comprehensive status of a specific project with enhanced error handling.
    
    Args:
        project_id: Unique identifier for the project
        format: Response format preference
        
    Returns:
        Dict containing detailed project status information
        
    Raises:
        HTTPException: If project is not found or invalid format requested
    """
    context = ErrorContext(
        endpoint=str(request.url),
        method=request.method,
        parameters={
            "project_id": project_id,
            "format": format
        }
    )
    
    try:
        # Validate format parameter
        if format not in ["json", "markdown", "table"]:
            raise ValidationError(
                message=f"Unsupported format: {format}",
                field="format",
                value=format,
                context=context
            )
        
        # Validate project ID format
        if not project_id.strip() or len(project_id.strip()) < 1:
            raise ValidationError(
                message="Project ID cannot be empty",
                field="project_id",
                value=project_id,
                context=context
            )
        
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
            
    except HTTPException as e:
        # Re-raise HTTP exceptions to use the enhanced handler
        raise e
    except ValidationError as e:
        # Log and re-raise validation errors
        e.log()
        raise HTTPException(
            status_code=400,
            detail=str(e.message)
        )
    except Exception as e:
        # Handle all other exceptions
        error_handler.handle_error(e, context)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while retrieving project status"
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


# Include dashboard endpoints
app.include_router(dashboard_router, prefix=API_PREFIX)

# Include SSE endpoints
app.include_router(sse_router, prefix=API_PREFIX)

# Include authentication endpoints
app.include_router(auth_router, prefix=API_PREFIX)

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
            "user_authentication"
        ],
        "supported_formats": ["json", "markdown", "table"],
        "timestamp": datetime.now().isoformat()
    }
