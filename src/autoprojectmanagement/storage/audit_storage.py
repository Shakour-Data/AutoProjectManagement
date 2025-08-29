#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/storage/audit_storage.py
File: audit_storage.py
Purpose: JSON-based audit trail storage service
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: JSON file-based storage for audit trail entries with comprehensive management
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import shutil
from ..models.audit import AuditEntry, AuditFilter, AuditStorage, audit_storage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JSONAuditStorage:
    """JSON-based audit storage service with comprehensive management."""
    
    def __init__(self, storage_dir: str = "audit_data"):
        """
        Initialize JSON audit storage.
        
        Args:
            storage_dir: Directory path for storing audit JSON files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.audit_file = self.storage_dir / "audit_entries.json"
        self.archive_dir = self.storage_dir / "archive"
        self.archive_dir.mkdir(exist_ok=True)
        
        # Initialize empty file if it doesn't exist
        self._initialize_files()
        
        # Load data from file
        self.load_data()
    
    def _initialize_files(self):
        """Initialize empty JSON files if they don't exist."""
        if not self.audit_file.exists():
            with open(self.audit_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2)
            logger.info(f"Created empty audit storage file: {self.audit_file}")
    
    def load_data(self):
        """Load audit data from JSON file into memory."""
        try:
            with open(self.audit_file, 'r', encoding='utf-8') as f:
                audit_data = json.load(f)
                audit_storage.entries = {
                    audit_id: AuditEntry(**entry_data) 
                    for audit_id, entry_data in audit_data.items()
                }
            
            logger.info(f"Loaded {len(audit_storage.entries)} audit entries from storage")
            
        except Exception as e:
            logger.error(f"Error loading audit data from storage: {e}")
            # Initialize empty storage on error
            audit_storage.entries = {}
    
    def save_data(self):
        """Save audit data from memory to JSON file."""
        try:
            audit_data = {
                audit_id: entry.dict() 
                for audit_id, entry in audit_storage.entries.items()
            }
            
            with open(self.audit_file, 'w', encoding='utf-8') as f:
                json.dump(audit_data, f, indent=2, default=str)
            
            logger.info(f"Audit data saved successfully: {len(audit_storage.entries)} entries")
            
        except Exception as e:
            logger.error(f"Error saving audit data to storage: {e}")
            raise
    
    def add_entry(self, audit_entry: AuditEntry) -> bool:
        """
        Add a new audit entry to storage.
        
        Args:
            audit_entry: The audit entry to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            audit_storage.entries[audit_entry.audit_id] = audit_entry
            self.save_data()
            logger.debug(f"Added audit entry: {audit_entry.audit_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding audit entry: {e}")
            return False
    
    def get_entry(self, audit_id: str) -> Optional[AuditEntry]:
        """
        Get a specific audit entry by ID.
        
        Args:
            audit_id: The audit entry ID
            
        Returns:
            Optional[AuditEntry]: The audit entry if found, None otherwise
        """
        return audit_storage.entries.get(audit_id)
    
    def get_entries(self, filter_criteria: Optional[AuditFilter] = None) -> List[AuditEntry]:
        """
        Get audit entries with optional filtering.
        
        Args:
            filter_criteria: Optional filter criteria
            
        Returns:
            List[AuditEntry]: List of filtered audit entries
        """
        entries = list(audit_storage.entries.values())
        
        if filter_criteria:
            entries = self._filter_entries(entries, filter_criteria)
        
        # Sort by timestamp (newest first)
        entries.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply pagination
        if filter_criteria:
            entries = entries[filter_criteria.offset:filter_criteria.offset + filter_criteria.limit]
        
        return entries
    
    def _filter_entries(self, entries: List[AuditEntry], filter_criteria: AuditFilter) -> List[AuditEntry]:
        """Filter audit entries based on criteria."""
        filtered_entries = entries
        
        if filter_criteria.action:
            filtered_entries = [e for e in filtered_entries if e.action == filter_criteria.action]
        
        if filter_criteria.resource_type:
            filtered_entries = [e for e in filtered_entries if e.resource_type == filter_criteria.resource_type]
        
        if filter_criteria.resource_id:
            filtered_entries = [e for e in filtered_entries if e.resource_id == filter_criteria.resource_id]
        
        if filter_criteria.user_id:
            filtered_entries = [e for e in filtered_entries if e.user_id == filter_criteria.user_id]
        
        if filter_criteria.severity:
            filtered_entries = [e for e in filtered_entries if e.severity == filter_criteria.severity]
        
        if filter_criteria.status:
            filtered_entries = [e for e in filtered_entries if e.status == filter_criteria.status]
        
        if filter_criteria.source:
            filtered_entries = [e for e in filtered_entries if e.source == filter_criteria.source]
        
        if filter_criteria.start_date:
            filtered_entries = [e for e in filtered_entries if e.timestamp >= filter_criteria.start_date]
        
        if filter_criteria.end_date:
            filtered_entries = [e for e in filtered_entries if e.timestamp <= filter_criteria.end_date]
        
        return filtered_entries
    
    def get_entry_count(self, filter_criteria: Optional[AuditFilter] = None) -> int:
        """
        Get count of audit entries with optional filtering.
        
        Args:
            filter_criteria: Optional filter criteria
            
        Returns:
            int: Number of matching audit entries
        """
        if filter_criteria:
            entries = self.get_entries(filter_criteria)
            return len(entries)
        return len(audit_storage.entries)
    
    def get_summary(self, filter_criteria: Optional[AuditFilter] = None) -> Dict[str, Any]:
        """
        Get summary statistics for audit entries.
        
        Args:
            filter_criteria: Optional filter criteria
            
        Returns:
            Dict[str, Any]: Summary statistics
        """
        entries = self.get_entries(filter_criteria) if filter_criteria else list(audit_storage.entries.values())
        
        if not entries:
            return {
                "total_entries": 0,
                "entries_by_action": {},
                "entries_by_resource": {},
                "entries_by_severity": {},
                "entries_by_status": {},
                "entries_by_user": {},
                "start_date": None,
                "end_date": None
            }
        
        # Calculate statistics
        entries_by_action = {}
        entries_by_resource = {}
        entries_by_severity = {}
        entries_by_status = {}
        entries_by_user = {}
        
        timestamps = [e.timestamp for e in entries]
        
        for entry in entries:
            # Count by action
            entries_by_action[entry.action] = entries_by_action.get(entry.action, 0) + 1
            
            # Count by resource type
            entries_by_resource[entry.resource_type] = entries_by_resource.get(entry.resource_type, 0) + 1
            
            # Count by severity
            entries_by_severity[entry.severity] = entries_by_severity.get(entry.severity, 0) + 1
            
            # Count by status
            entries_by_status[entry.status] = entries_by_status.get(entry.status, 0) + 1
            
            # Count by user
            if entry.user_id:
                entries_by_user[entry.user_id] = entries_by_user.get(entry.user_id, 0) + 1
        
        return {
            "total_entries": len(entries),
            "entries_by_action": entries_by_action,
            "entries_by_resource": entries_by_resource,
            "entries_by_severity": entries_by_severity,
            "entries_by_status": entries_by_status,
            "entries_by_user": entries_by_user,
            "start_date": min(timestamps).isoformat() if timestamps else None,
            "end_date": max(timestamps).isoformat() if timestamps else None
        }
    
    def cleanup_old_entries(self, max_age_days: int = 90) -> int:
        """
        Clean up audit entries older than specified days.
        
        Args:
            max_age_days: Maximum age of entries to keep in days
            
        Returns:
            int: Number of entries cleaned up
        """
        try:
            cutoff_date = datetime.now() - datetime.timedelta(days=max_age_days)
            entries_to_remove = []
            
            for audit_id, entry in audit_storage.entries.items():
                if entry.timestamp < cutoff_date:
                    entries_to_remove.append(audit_id)
            
            # Remove old entries
            for audit_id in entries_to_remove:
                del audit_storage.entries[audit_id]
            
            if entries_to_remove:
                self.save_data()
                logger.info(f"Cleaned up {len(entries_to_remove)} audit entries older than {max_age_days} days")
            
            return len(entries_to_remove)
            
        except Exception as e:
            logger.error(f"Error cleaning up old audit entries: {e}")
            return 0
    
    def backup_data(self, backup_dir: str = "audit_backups") -> Optional[str]:
        """
        Create a backup of audit data.
        
        Args:
            backup_dir: Backup directory path
            
        Returns:
            Optional[str]: Path to backup directory if successful, None otherwise
        """
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"audit_backup_{timestamp}"
            backup_dir_path = backup_path / backup_name
            
            # Copy audit file
            shutil.copy2(self.audit_file, backup_dir_path / "audit_entries.json")
            
            logger.info(f"Audit backup created successfully: {backup_dir_path}")
            return str(backup_dir_path)
            
        except Exception as e:
            logger.error(f"Error creating audit backup: {e}")
            return None
    
    def export_data(self, export_format: str = "json", filter_criteria: Optional[AuditFilter] = None) -> Optional[str]:
        """
        Export audit data in specified format.
        
        Args:
            export_format: Export format (json, csv)
            filter_criteria: Optional filter criteria
            
        Returns:
            Optional[str]: Path to export file if successful, None otherwise
        """
        try:
            entries = self.get_entries(filter_criteria)
            
            if export_format == "json":
                export_data = {
                    "audit_entries": [entry.dict() for entry in entries],
                    "export_timestamp": datetime.now().isoformat(),
                    "total_entries": len(entries),
                    "filter_criteria": filter_criteria.dict() if filter_criteria else None
                }
                
                export_file = self.storage_dir / f"audit_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, default=str)
                
                logger.info(f"Audit data exported to: {export_file}")
                return str(export_file)
            
            elif export_format == "csv":
                # CSV export implementation would go here
                logger.warning("CSV export not yet implemented")
                return None
            
            else:
                logger.error(f"Unsupported export format: {export_format}")
                return None
                
        except Exception as e:
            logger.error(f"Error exporting audit data: {e}")
            return None

# Global audit storage instance
audit_storage_service = JSONAuditStorage()
