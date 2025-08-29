#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/services/audit_service.py
File: audit_service.py
Purpose: Comprehensive audit trail service for tracking system changes and user actions
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Centralized audit logging service with real-time integration capabilities
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import json

# Import models and storage
try:
    from ..models.audit import (
        AuditEntry, AuditActionType, AuditResourceType, 
        AuditSeverity, AuditStatus, AuditFilter, generate_audit_id
    )
    from ..storage.audit_storage import audit_storage_service
except ImportError:
    # Handle import for development
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from autoprojectmanagement.models.audit import (
        AuditEntry, AuditActionType, AuditResourceType, 
        AuditSeverity, AuditStatus, AuditFilter, generate_audit_id
    )
    from autoprojectmanagement.storage.audit_storage import audit_storage_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AuditService:
    """
    Comprehensive audit trail service for tracking system changes and user actions.
    
    This service provides centralized audit logging capabilities with integration
    to various system components and real-time event publishing.
    """
    
    def __init__(self):
        """Initialize the audit service."""
        self.storage = audit_storage_service
        logger.info("AuditService initialized")
    
    def log_event(
        self,
        action: AuditActionType,
        resource_type: AuditResourceType,
        resource_id: str,
        description: str,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        user_ip: Optional[str] = None,
        user_agent: Optional[str] = None,
        severity: AuditSeverity = AuditSeverity.INFO,
        status: AuditStatus = AuditStatus.SUCCESS,
        details: Optional[Dict[str, Any]] = None,
        changes: Optional[Dict[str, Any]] = None,
        before_state: Optional[Dict[str, Any]] = None,
        after_state: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        correlation_id: Optional[str] = None,
        session_id: Optional[str] = None,
        duration_ms: Optional[int] = None,
        error_message: Optional[str] = None,
        stack_trace: Optional[str] = None,
        resource_name: Optional[str] = None
    ) -> Optional[AuditEntry]:
        """
        Log a comprehensive audit event.
        
        Args:
            action: Type of action performed
            resource_type: Type of resource affected
            resource_id: Identifier of the affected resource
            description: Human-readable description of the event
            user_id: User who performed the action
            user_email: Email of the user
            user_ip: IP address of the user
            user_agent: User agent string
            severity: Severity level of the event
            status: Status of the action
            details: Additional event details
            changes: Detailed changes made
            before_state: State before changes
            after_state: State after changes
            source: Source of the event
            correlation_id: Correlation ID for related events
            session_id: Session identifier
            duration_ms: Duration of the action in milliseconds
            error_message: Error message if action failed
            stack_trace: Stack trace for errors
            resource_name: Name of the affected resource
            
        Returns:
            Optional[AuditEntry]: The created audit entry if successful, None otherwise
        """
        try:
            # Create audit entry
            audit_entry = AuditEntry(
                audit_id=generate_audit_id(),
                timestamp=datetime.now(),
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                resource_name=resource_name,
                user_id=user_id,
                user_email=user_email,
                user_ip=user_ip,
                user_agent=user_agent,
                severity=severity,
                status=status,
                description=description,
                details=details,
                changes=changes,
                before_state=before_state,
                after_state=after_state,
                source=source,
                correlation_id=correlation_id,
                session_id=session_id,
                duration_ms=duration_ms,
                error_message=error_message,
                stack_trace=stack_trace
            )
            
            # Store the entry
            success = self.storage.add_entry(audit_entry)
            
            if success:
                logger.debug(f"Audit event logged: {audit_entry.audit_id} - {action.value} {resource_type.value}")
                
                # Publish real-time event if available
                self._publish_audit_event(audit_entry)
                
                return audit_entry
            else:
                logger.error(f"Failed to store audit entry: {audit_entry.audit_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error logging audit event: {e}")
            return None
    
    def _publish_audit_event(self, audit_entry: AuditEntry):
        """
        Publish audit event to real-time service if available.
        
        Args:
            audit_entry: The audit entry to publish
        """
        try:
            # Try to import real-time service
            from ..api.realtime_service import publish_audit_event
            publish_audit_event(audit_entry)
        except ImportError:
            # Real-time service not available, log debug message
            logger.debug("Real-time service not available for audit events")
        except Exception as e:
            logger.warning(f"Failed to publish audit event to real-time service: {e}")
    
    # Convenience methods for common audit scenarios
    
    def log_user_login(
        self,
        user_id: str,
        user_email: str,
        user_ip: str,
        user_agent: str,
        status: AuditStatus = AuditStatus.SUCCESS,
        error_message: Optional[str] = None
    ) -> Optional[AuditEntry]:
        """Log user login event."""
        return self.log_event(
            action=AuditActionType.LOGIN,
            resource_type=AuditResourceType.USER,
            resource_id=user_id,
            resource_name=user_email,
            user_id=user_id,
            user_email=user_email,
            user_ip=user_ip,
            user_agent=user_agent,
            description=f"User login attempt: {user_email}",
            status=status,
            error_message=error_message,
            source="authentication"
        )
    
    def log_user_logout(
        self,
        user_id: str,
        user_email: str,
        user_ip: str,
        user_agent: str
    ) -> Optional[AuditEntry]:
        """Log user logout event."""
        return self.log_event(
            action=AuditActionType.LOGOUT,
            resource_type=AuditResourceType.USER,
            resource_id=user_id,
            resource_name=user_email,
            user_id=user_id,
            user_email=user_email,
            user_ip=user_ip,
            user_agent=user_agent,
            description=f"User logout: {user_email}",
            source="authentication"
        )
    
    def log_project_create(
        self,
        project_id: str,
        project_name: str,
        user_id: str,
        user_email: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Optional[AuditEntry]:
        """Log project creation event."""
        return self.log_event(
            action=AuditActionType.CREATE,
            resource_type=AuditResourceType.PROJECT,
            resource_id=project_id,
            resource_name=project_name,
            user_id=user_id,
            user_email=user_email,
            description=f"Project created: {project_name}",
            details=details,
            source="project_management"
        )
    
    def log_project_update(
        self,
        project_id: str,
        project_name: str,
        user_id: str,
        user_email: str,
        changes: Dict[str, Any],
        before_state: Optional[Dict[str, Any]] = None,
        after_state: Optional[Dict[str, Any]] = None
    ) -> Optional[AuditEntry]:
        """Log project update event."""
        return self.log_event(
            action=AuditActionType.UPDATE,
            resource_type=AuditResourceType.PROJECT,
            resource_id=project_id,
            resource_name=project_name,
            user_id=user_id,
            user_email=user_email,
            description=f"Project updated: {project_name}",
            changes=changes,
            before_state=before_state,
            after_state=after_state,
            source="project_management"
        )
    
    def log_file_change(
        self,
        file_path: str,
        change_type: str,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Optional[AuditEntry]:
        """Log file change event."""
        return self.log_event(
            action=AuditActionType.UPDATE,
            resource_type=AuditResourceType.FILE,
            resource_id=file_path,
            resource_name=Path(file_path).name,
            user_id=user_id,
            user_email=user_email,
            description=f"File {change_type}: {file_path}",
            details=details,
            source="file_watcher"
        )
    
    def log_config_change(
        self,
        config_key: str,
        user_id: str,
        user_email: str,
        changes: Dict[str, Any],
        before_state: Optional[Dict[str, Any]] = None,
        after_state: Optional[Dict[str, Any]] = None
    ) -> Optional[AuditEntry]:
        """Log configuration change event."""
        return self.log_event(
            action=AuditActionType.UPDATE,
            resource_type=AuditResourceType.CONFIG,
            resource_id=config_key,
            resource_name=config_key,
            user_id=user_id,
            user_email=user_email,
            description=f"Configuration changed: {config_key}",
            changes=changes,
            before_state=before_state,
            after_state=after_state,
            source="configuration"
        )
    
    def log_error_event(
        self,
        error_message: str,
        resource_type: AuditResourceType,
        resource_id: str,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        stack_trace: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Optional[AuditEntry]:
        """Log error event."""
        return self.log_event(
            action=AuditActionType.EXECUTE,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            user_email=user_email,
            description=f"Error occurred: {error_message}",
            severity=AuditSeverity.ERROR,
            status=AuditStatus.FAILURE,
            error_message=error_message,
            stack_trace=stack_trace,
            details=details,
            source="error_handler"
        )
    
    # Query methods
    
    def get_entries(self, filter_criteria: Optional[AuditFilter] = None) -> List[AuditEntry]:
        """
        Get audit entries with optional filtering.
        
        Args:
            filter_criteria: Optional filter criteria
            
        Returns:
            List[AuditEntry]: List of audit entries
        """
        return self.storage.get_entries(filter_criteria)
    
    def get_entry(self, audit_id: str) -> Optional[AuditEntry]:
        """
        Get a specific audit entry by ID.
        
        Args:
            audit_id: Audit entry ID
            
        Returns:
            Optional[AuditEntry]: The audit entry if found
        """
        return self.storage.get_entry(audit_id)
    
    def get_summary(self, filter_criteria: Optional[AuditFilter] = None) -> Dict[str, Any]:
        """
        Get summary statistics for audit entries.
        
        Args:
            filter_criteria: Optional filter criteria
            
        Returns:
            Dict[str, Any]: Summary statistics
        """
        return self.storage.get_summary(filter_criteria)
    
    def get_entry_count(self, filter_criteria: Optional[AuditFilter] = None) -> int:
        """
        Get count of audit entries.
        
        Args:
            filter_criteria: Optional filter criteria
            
        Returns:
            int: Number of audit entries
        """
        return self.storage.get_entry_count(filter_criteria)
    
    # Maintenance methods
    
    def cleanup_old_entries(self, max_age_days: int = 90) -> int:
        """
        Clean up audit entries older than specified days.
        
        Args:
            max_age_days: Maximum age in days
            
        Returns:
            int: Number of entries cleaned up
        """
        return self.storage.cleanup_old_entries(max_age_days)
    
    def export_data(self, export_format: str = "json", filter_criteria: Optional[AuditFilter] = None) -> Optional[str]:
        """
        Export audit data.
        
        Args:
            export_format: Export format
            filter_criteria: Optional filter criteria
            
        Returns:
            Optional[str]: Path to export file
        """
        return self.storage.export_data(export_format, filter_criteria)
    
    def backup_data(self, backup_dir: str = "audit_backups") -> Optional[str]:
        """
        Create backup of audit data.
        
        Args:
            backup_dir: Backup directory
            
        Returns:
            Optional[str]: Path to backup
        """
        return self.storage.backup_data(backup_dir)
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.
        
        Returns:
            Dict[str, Any]: Storage statistics
        """
        return {
            "total_entries": self.get_entry_count(),
            "storage_directory": str(self.storage.storage_dir),
            "last_cleanup": datetime.now().isoformat()
        }

# Global audit service instance
audit_service = AuditService()

# Utility function for quick audit logging
def log_audit_event(
    action: AuditActionType,
    resource_type: AuditResourceType,
    resource_id: str,
    description: str,
    **kwargs
) -> Optional[AuditEntry]:
    """
    Quick utility function for logging audit events.
    
    Args:
        action: Type of action
        resource_type: Type of resource
        resource_id: Resource identifier
        description: Event description
        **kwargs: Additional audit entry parameters
        
    Returns:
        Optional[AuditEntry]: The created audit entry
    """
    return audit_service.log_event(
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        **kwargs
    )
