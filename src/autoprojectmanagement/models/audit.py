#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/models/audit.py
File: audit.py
Purpose: Audit trail models for tracking system changes and user actions
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Pydantic models for audit trail entries and change tracking
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from pydantic import BaseModel, Field, validator
import json

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuditActionType(str, Enum):
    """Types of audit actions that can be tracked."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    READ = "read"
    LOGIN = "login"
    LOGOUT = "logout"
    EXECUTE = "execute"
    CONFIGURE = "configure"
    BACKUP = "backup"
    RESTORE = "restore"
    EXPORT = "export"
    IMPORT = "import"
    VALIDATE = "validate"
    APPROVE = "approve"
    REJECT = "reject"
    COMMENT = "comment"
    NOTIFY = "notify"
    SCHEDULE = "schedule"
    UNSCHEDULE = "unschedule"

class AuditResourceType(str, Enum):
    """Types of resources that can be audited."""
    PROJECT = "project"
    TASK = "task"
    USER = "user"
    SESSION = "session"
    CONFIG = "config"
    FILE = "file"
    DIRECTORY = "directory"
    COMMIT = "commit"
    BRANCH = "branch"
    REPOSITORY = "repository"
    NOTIFICATION = "notification"
    REPORT = "report"
    BACKUP = "backup"
    AUDIT = "audit"
    SYSTEM = "system"
    ISSUE = "issue"
    COMMENT = "comment"
    WEBHOOK = "webhook"

class AuditSeverity(str, Enum):
    """Severity levels for audit events."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AuditStatus(str, Enum):
    """Status of audit events."""
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"

class AuditEntry(BaseModel):
    """
    Base model for audit trail entries.
    
    Represents a single audit event with comprehensive metadata.
    """
    audit_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique audit identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Event timestamp")
    action: AuditActionType = Field(..., description="Type of action performed")
    resource_type: AuditResourceType = Field(..., description="Type of resource affected")
    resource_id: str = Field(..., description="Identifier of the affected resource")
    resource_name: Optional[str] = Field(None, description="Name of the affected resource")
    
    user_id: Optional[str] = Field(None, description="User who performed the action")
    user_email: Optional[str] = Field(None, description="Email of the user who performed the action")
    user_ip: Optional[str] = Field(None, description="IP address of the user")
    user_agent: Optional[str] = Field(None, description="User agent string")
    
    severity: AuditSeverity = Field(AuditSeverity.INFO, description="Severity level")
    status: AuditStatus = Field(AuditStatus.SUCCESS, description="Action status")
    
    description: str = Field(..., description="Human-readable description of the event")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional event details")
    
    changes: Optional[Dict[str, Any]] = Field(None, description="Detailed changes made")
    before_state: Optional[Dict[str, Any]] = Field(None, description="State before changes")
    after_state: Optional[Dict[str, Any]] = Field(None, description="State after changes")
    
    source: Optional[str] = Field(None, description="Source of the event (API, CLI, UI, etc.)")
    correlation_id: Optional[str] = Field(None, description="Correlation ID for related events")
    session_id: Optional[str] = Field(None, description="Session identifier")
    
    duration_ms: Optional[int] = Field(None, description="Duration of the action in milliseconds", ge=0)
    error_message: Optional[str] = Field(None, description="Error message if action failed")
    stack_trace: Optional[str] = Field(None, description="Stack trace for errors")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    @validator('resource_id')
    def validate_resource_id(cls, v):
        """Validate that resource ID is not empty."""
        if not v or not v.strip():
            raise ValueError('Resource ID cannot be empty')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        """Validate that description is not empty."""
        if not v or not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()

class AuditFilter(BaseModel):
    """
    Model for filtering audit entries.
    """
    action: Optional[AuditActionType] = Field(None, description="Filter by action type")
    resource_type: Optional[AuditResourceType] = Field(None, description="Filter by resource type")
    resource_id: Optional[str] = Field(None, description="Filter by resource ID")
    user_id: Optional[str] = Field(None, description="Filter by user ID")
    severity: Optional[AuditSeverity] = Field(None, description="Filter by severity")
    status: Optional[AuditStatus] = Field(None, description="Filter by status")
    start_date: Optional[datetime] = Field(None, description="Start date for filtering")
    end_date: Optional[datetime] = Field(None, description="End date for filtering")
    source: Optional[str] = Field(None, description="Filter by source")
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of entries to return")
    offset: int = Field(0, ge=0, description="Number of entries to skip")

class AuditSummary(BaseModel):
    """
    Summary statistics for audit entries.
    """
    total_entries: int = Field(..., description="Total number of audit entries")
    entries_by_action: Dict[AuditActionType, int] = Field(..., description="Count by action type")
    entries_by_resource: Dict[AuditResourceType, int] = Field(..., description="Count by resource type")
    entries_by_severity: Dict[AuditSeverity, int] = Field(..., description="Count by severity")
    entries_by_status: Dict[AuditStatus, int] = Field(..., description="Count by status")
    entries_by_user: Dict[str, int] = Field(..., description="Count by user")
    start_date: Optional[datetime] = Field(None, description="Earliest entry timestamp")
    end_date: Optional[datetime] = Field(None, description="Latest entry timestamp")

class AuditReportRequest(BaseModel):
    """
    Model for audit report generation requests.
    """
    format: str = Field("json", description="Report format: json, csv, pdf, markdown")
    filter: Optional[AuditFilter] = Field(None, description="Filter criteria for the report")
    include_summary: bool = Field(True, description="Include summary statistics")
    include_details: bool = Field(True, description="Include detailed entries")
    group_by: Optional[List[str]] = Field(None, description="Fields to group by")

# Utility functions
def generate_audit_id() -> str:
    """Generate a unique audit ID."""
    return str(uuid.uuid4())

def get_current_timestamp() -> datetime:
    """Get current timestamp."""
    return datetime.now()

# Global audit storage structure (in-memory)
class AuditStorage:
    """In-memory audit storage structure."""
    entries: Dict[str, AuditEntry] = {}
    
    def __init__(self):
        """Initialize audit storage."""
        self.entries = {}

# Global audit storage instance
audit_storage = AuditStorage()
