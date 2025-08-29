#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/api/audit_endpoints.py
File: audit_endpoints.py
Purpose: REST API endpoints for audit trail access and management
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: FastAPI endpoints for querying and managing audit trail data
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from fastapi import APIRouter, HTTPException, Query, Path as APIPath, Request, status
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field

# Import audit service and models
try:
    from ..services.audit_service import audit_service
    from ..models.audit import (
        AuditEntry, AuditFilter, AuditActionType, AuditResourceType,
        AuditSeverity, AuditStatus, AuditReportRequest
    )
except ImportError:
    # Handle import for development
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from autoprojectmanagement.services.audit_service import audit_service
    from autoprojectmanagement.models.audit import (
        AuditEntry, AuditFilter, AuditActionType, AuditResourceType,
        AuditSeverity, AuditStatus, AuditReportRequest
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/audit", tags=["Audit Trail"])

# Response models
class AuditEntryResponse(BaseModel):
    """Response model for audit entries."""
    audit_id: str = Field(..., description="Unique audit identifier")
    timestamp: datetime = Field(..., description="Event timestamp")
    action: str = Field(..., description="Type of action performed")
    resource_type: str = Field(..., description="Type of resource affected")
    resource_id: str = Field(..., description="Identifier of the affected resource")
    resource_name: Optional[str] = Field(None, description="Name of the affected resource")
    user_id: Optional[str] = Field(None, description="User who performed the action")
    user_email: Optional[str] = Field(None, description="Email of the user")
    severity: str = Field(..., description="Severity level")
    status: str = Field(..., description="Action status")
    description: str = Field(..., description="Human-readable description")
    source: Optional[str] = Field(None, description="Source of the event")
    duration_ms: Optional[int] = Field(None, description="Duration in milliseconds")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AuditListResponse(BaseModel):
    """Response model for list of audit entries."""
    entries: List[AuditEntryResponse] = Field(..., description="List of audit entries")
    total_count: int = Field(..., description="Total number of entries")
    limit: int = Field(..., description="Maximum entries returned")
    offset: int = Field(..., description="Number of entries skipped")
    has_more: bool = Field(..., description="Whether more entries are available")

class AuditSummaryResponse(BaseModel):
    """Response model for audit summary."""
    total_entries: int = Field(..., description="Total number of audit entries")
    entries_by_action: Dict[str, int] = Field(..., description="Count by action type")
    entries_by_resource: Dict[str, int] = Field(..., description="Count by resource type")
    entries_by_severity: Dict[str, int] = Field(..., description="Count by severity")
    entries_by_status: Dict[str, int] = Field(..., description="Count by status")
    entries_by_user: Dict[str, int] = Field(..., description="Count by user")
    start_date: Optional[str] = Field(None, description="Earliest entry timestamp")
    end_date: Optional[str] = Field(None, description="Latest entry timestamp")

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")
    timestamp: str = Field(..., description="Error timestamp")

# Endpoints
@router.get(
    "/entries",
    response_model=AuditListResponse,
    responses={
        200: {"description": "Audit entries retrieved successfully"},
        400: {"description": "Invalid filter parameters", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
async def get_audit_entries(
    request: Request,
    action: Optional[AuditActionType] = Query(None, description="Filter by action type"),
    resource_type: Optional[AuditResourceType] = Query(None, description="Filter by resource type"),
    resource_id: Optional[str] = Query(None, description="Filter by resource ID"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    severity: Optional[AuditSeverity] = Query(None, description="Filter by severity"),
    status: Optional[AuditStatus] = Query(None, description="Filter by status"),
    source: Optional[str] = Query(None, description="Filter by source"),
    start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of entries to return"),
    offset: int = Query(0, ge=0, description="Number of entries to skip")
):
    """
    Retrieve audit entries with comprehensive filtering capabilities.
    
    This endpoint allows querying audit trail data with multiple filter criteria
    including action type, resource type, user, severity, status, and date ranges.
    """
    try:
        # Create filter criteria
        filter_criteria = AuditFilter(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            severity=severity,
            status=status,
            source=source,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset
        )
        
        # Get entries
        entries = audit_service.get_entries(filter_criteria)
        total_count = audit_service.get_entry_count(filter_criteria)
        
        # Convert to response format
        response_entries = []
        for entry in entries:
            response_entries.append(AuditEntryResponse(
                audit_id=entry.audit_id,
                timestamp=entry.timestamp,
                action=entry.action.value,
                resource_type=entry.resource_type.value,
                resource_id=entry.resource_id,
                resource_name=entry.resource_name,
                user_id=entry.user_id,
                user_email=entry.user_email,
                severity=entry.severity.value,
                status=entry.status.value,
                description=entry.description,
                source=entry.source,
                duration_ms=entry.duration_ms
            ))
        
        return AuditListResponse(
            entries=response_entries,
            total_count=total_count,
            limit=limit,
            offset=offset,
            has_more=(offset + limit) < total_count
        )
        
    except Exception as e:
        logger.error(f"Error retrieving audit entries: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving audit entries: {str(e)}"
        )

@router.get(
    "/entries/{audit_id}",
    response_model=AuditEntryResponse,
    responses={
        200: {"description": "Audit entry retrieved successfully"},
        404: {"description": "Audit entry not found", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
async def get_audit_entry(
    request: Request,
    audit_id: str = APIPath(..., description="Audit entry identifier")
):
    """
    Retrieve a specific audit entry by ID.
    
    Returns comprehensive details for a single audit event including
    changes, before/after states, and error information if available.
    """
    try:
        entry = audit_service.get_entry(audit_id)
        
        if not entry:
            raise HTTPException(
                status_code=404,
                detail=f"Audit entry '{audit_id}' not found"
            )
        
        return AuditEntryResponse(
            audit_id=entry.audit_id,
            timestamp=entry.timestamp,
            action=entry.action.value,
            resource_type=entry.resource_type.value,
            resource_id=entry.resource_id,
            resource_name=entry.resource_name,
            user_id=entry.user_id,
            user_email=entry.user_email,
            severity=entry.severity.value,
            status=entry.status.value,
            description=entry.description,
            source=entry.source,
            duration_ms=entry.duration_ms
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving audit entry {audit_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving audit entry: {str(e)}"
        )

@router.get(
    "/summary",
    response_model=AuditSummaryResponse,
    responses={
        200: {"description": "Audit summary retrieved successfully"},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
async def get_audit_summary(
    request: Request,
    action: Optional[AuditActionType] = Query(None, description="Filter by action type"),
    resource_type: Optional[AuditResourceType] = Query(None, description="Filter by resource type"),
    resource_id: Optional[str] = Query(None, description="Filter by resource ID"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    severity: Optional[AuditSeverity] = Query(None, description="Filter by severity"),
    status: Optional[AuditStatus] = Query(None, description="Filter by status"),
    source: Optional[str] = Query(None, description="Filter by source"),
    start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering")
):
    """
    Get summary statistics for audit entries.
    
    Provides aggregated counts by action type, resource type, severity,
    status, and user for comprehensive audit trail analysis.
    """
    try:
        # Create filter criteria
        filter_criteria = AuditFilter(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            severity=severity,
            status=status,
            source=source,
            start_date=start_date,
            end_date=end_date
        )
        
        # Get summary
        summary = audit_service.get_summary(filter_criteria)
        
        return AuditSummaryResponse(**summary)
        
    except Exception as e:
        logger.error(f"Error retrieving audit summary: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving audit summary: {str(e)}"
        )

@router.get(
    "/count",
    responses={
        200: {"description": "Audit entry count retrieved successfully"},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
async def get_audit_count(
    request: Request,
    action: Optional[AuditActionType] = Query(None, description="Filter by action type"),
    resource_type: Optional[AuditResourceType] = Query(None, description="Filter by resource type"),
    resource_id: Optional[str] = Query(None, description="Filter by resource ID"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    severity: Optional[AuditSeverity] = Query(None, description="Filter by severity"),
    status: Optional[AuditStatus] = Query(None, description="Filter by status"),
    source: Optional[str] = Query(None, description="Filter by source"),
    start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering")
):
    """
    Get count of audit entries matching filter criteria.
    
    Useful for pagination and monitoring audit trail volume.
    """
    try:
        # Create filter criteria
        filter_criteria = AuditFilter(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            severity=severity,
            status=status,
            source=source,
            start_date=start_date,
            end_date=end_date
        )
        
        count = audit_service.get_entry_count(filter_criteria)
        
        return {"count": count}
        
    except Exception as e:
        logger.error(f"Error retrieving audit count: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving audit count: {str(e)}"
        )

@router.post(
    "/export",
    responses={
        200: {"description": "Audit data exported successfully"},
        400: {"description": "Invalid export format", "model": ErrorResponse},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
async def export_audit_data(
    request: Request,
    export_request: AuditReportRequest
):
    """
    Export audit data in various formats.
    
    Supports JSON and CSV formats with comprehensive filtering options.
    Returns a file download response with the exported data.
    """
    try:
        # Create filter criteria from request
        filter_criteria = None
        if export_request.filter:
            filter_criteria = AuditFilter(**export_request.filter.dict())
        
        # Export data
        export_path = audit_service.export_data(
            export_request.format,
            filter_criteria
        )
        
        if not export_path:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported export format: {export_request.format}"
            )
        
        # Return file download response
        return FileResponse(
            path=export_path,
            filename=f"audit_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_request.format}",
            media_type="application/octet-stream"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting audit data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error exporting audit data: {str(e)}"
        )

@router.post(
    "/cleanup",
    responses={
        200: {"description": "Audit data cleaned up successfully"},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
async def cleanup_audit_data(
    request: Request,
    max_age_days: int = Query(90, ge=1, le=365, description="Maximum age of entries to keep in days")
):
    """
    Clean up old audit entries.
    
    Removes audit entries older than the specified number of days
    to manage storage usage and maintain performance.
    """
    try:
        cleaned_count = audit_service.cleanup_old_entries(max_age_days)
        
        return {
            "message": f"Cleaned up {cleaned_count} audit entries older than {max_age_days} days",
            "cleaned_count": cleaned_count,
            "max_age_days": max_age_days
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up audit data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error cleaning up audit data: {str(e)}"
        )

@router.get(
    "/stats",
    responses={
        200: {"description": "Storage statistics retrieved successfully"},
        500: {"description": "Internal server error", "model": ErrorResponse}
    }
)
async def get_audit_stats(request: Request):
    """
    Get audit storage statistics.
    
    Returns information about storage usage, entry counts, and
    maintenance information for the audit trail system.
    """
    try:
        stats = audit_service.get_storage_stats()
        
        return stats
        
    except Exception as e:
        logger.error(f"Error retrieving audit stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving audit stats: {str(e)}"
        )

# Health check endpoint
@router.get("/health")
async def audit_health_check(request: Request):
    """
    Health check for audit service.
    
    Verifies that the audit service is operational and can
    access storage resources properly.
    """
    try:
        # Simple health check - try to get entry count
        count = audit_service.get_entry_count()
        
        return {
            "status": "healthy",
            "total_entries": count,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Audit service health check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Audit service health check failed: {str(e)}"
        )
