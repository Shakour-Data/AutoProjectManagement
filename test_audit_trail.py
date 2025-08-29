#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the Audit Trail implementation.
This script tests the core functionality of the audit trail system.
"""

import sys
from pathlib import Path
import json
from datetime import datetime, timedelta

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

try:
    from src.autoprojectmanagement.services.audit_service import audit_service
    from src.autoprojectmanagement.models.audit import (
        AuditActionType, AuditResourceType, AuditSeverity, AuditStatus
    )
    print("✅ Successfully imported audit service and models")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Trying alternative import path...")
    try:
        from autoprojectmanagement.services.audit_service import audit_service
        from autoprojectmanagement.models.audit import (
            AuditActionType, AuditResourceType, AuditSeverity, AuditStatus
        )
        print("✅ Successfully imported using alternative path")
    except ImportError as e2:
        print(f"❌ Alternative import also failed: {e2}")
        sys.exit(1)

def test_basic_audit_logging():
    """Test basic audit logging functionality."""
    print("\n" + "="*60)
    print("TESTING BASIC AUDIT LOGGING")
    print("="*60)
    
    # Test 1: Basic audit entry creation
    print("\n1. Testing basic audit entry creation...")
    try:
        entry = audit_service.log_event(
            action=AuditActionType.CREATE,
            resource_type=AuditResourceType.PROJECT,
            resource_id="test-project-001",
            description="Test project created for audit testing",
            user_id="test-user-001",
            user_email="test@example.com",
            severity=AuditSeverity.INFO,
            status=AuditStatus.SUCCESS,
            source="test_script"
        )
        
        if entry:
            print(f"✅ Successfully created audit entry: {entry.audit_id}")
            print(f"   Action: {entry.action.value}")
            print(f"   Resource: {entry.resource_type.value}/{entry.resource_id}")
            print(f"   Description: {entry.description}")
        else:
            print("❌ Failed to create audit entry")
            return False
            
    except Exception as e:
        print(f"❌ Error creating audit entry: {e}")
        return False
    
    # Test 2: User login event
    print("\n2. Testing user login event...")
    try:
        login_entry = audit_service.log_user_login(
            user_id="test-user-001",
            user_email="test@example.com",
            user_ip="192.168.1.100",
            user_agent="TestBrowser/1.0"
        )
        
        if login_entry:
            print(f"✅ Successfully logged user login: {login_entry.audit_id}")
            print(f"   Action: {login_entry.action.value}")
            print(f"   User: {login_entry.user_email}")
        else:
            print("❌ Failed to log user login")
            return False
            
    except Exception as e:
        print(f"❌ Error logging user login: {e}")
        return False
    
    # Test 3: Project creation event
    print("\n3. Testing project creation event...")
    try:
        project_entry = audit_service.log_project_create(
            project_id="test-project-002",
            project_name="Test Project 002",
            user_id="test-user-001",
            user_email="test@example.com",
            details={"template": "basic", "tasks": 5}
        )
        
        if project_entry:
            print(f"✅ Successfully logged project creation: {project_entry.audit_id}")
            print(f"   Project: {project_entry.resource_name}")
            print(f"   Details: {project_entry.details}")
        else:
            print("❌ Failed to log project creation")
            return False
            
    except Exception as e:
        print(f"❌ Error logging project creation: {e}")
        return False
    
    return True

def test_audit_querying():
    """Test audit entry querying functionality."""
    print("\n" + "="*60)
    print("TESTING AUDIT QUERYING")
    print("="*60)
    
    # Test 1: Get all entries
    print("\n1. Testing get all audit entries...")
    try:
        entries = audit_service.get_entries()
        print(f"✅ Found {len(entries)} audit entries")
        
        if entries:
            for i, entry in enumerate(entries[:3]):  # Show first 3 entries
                print(f"   {i+1}. {entry.action.value} {entry.resource_type.value}/{entry.resource_id}")
                
    except Exception as e:
        print(f"❌ Error getting audit entries: {e}")
        return False
    
    # Test 2: Get entry count
    print("\n2. Testing entry count...")
    try:
        count = audit_service.get_entry_count()
        print(f"✅ Total audit entries: {count}")
        
    except Exception as e:
        print(f"❌ Error getting entry count: {e}")
        return False
    
    # Test 3: Get summary
    print("\n3. Testing summary statistics...")
    try:
        summary = audit_service.get_summary()
        print(f"✅ Summary statistics:")
        print(f"   Total entries: {summary['total_entries']}")
        print(f"   By action: {summary['entries_by_action']}")
        print(f"   By resource: {summary['entries_by_resource']}")
        
    except Exception as e:
        print(f"❌ Error getting summary: {e}")
        return False
    
    return True

def test_error_logging():
    """Test error logging functionality."""
    print("\n" + "="*60)
    print("TESTING ERROR LOGGING")
    print("="*60)
    
    # Test 1: Error event logging
    print("\n1. Testing error event logging...")
    try:
        error_entry = audit_service.log_error_event(
            error_message="Test error occurred during processing",
            resource_type=AuditResourceType.SYSTEM,
            resource_id="test-system-001",
            user_id="test-user-001",
            user_email="test@example.com",
            stack_trace="Traceback (most recent call last):\n  File \"test.py\", line 10, in <module>\n    raise ValueError('Test error')",
            details={"component": "processor", "input_data": "test_data"}
        )
        
        if error_entry:
            print(f"✅ Successfully logged error event: {error_entry.audit_id}")
            print(f"   Severity: {error_entry.severity.value}")
            print(f"   Status: {error_entry.status.value}")
            print(f"   Error: {error_entry.error_message}")
        else:
            print("❌ Failed to log error event")
            return False
            
    except Exception as e:
        print(f"❌ Error logging error event: {e}")
        return False
    
    return True

def test_storage_operations():
    """Test storage operations like backup and export."""
    print("\n" + "="*60)
    print("TESTING STORAGE OPERATIONS")
    print("="*60)
    
    # Test 1: Get storage stats
    print("\n1. Testing storage statistics...")
    try:
        stats = audit_service.get_storage_stats()
        print(f"✅ Storage statistics:")
        print(f"   Total entries: {stats['total_entries']}")
        print(f"   Storage directory: {stats['storage_directory']}")
        
    except Exception as e:
        print(f"❌ Error getting storage stats: {e}")
        return False
    
    # Test 2: Export data
    print("\n2. Testing data export...")
    try:
        export_path = audit_service.export_data("json")
        if export_path:
            print(f"✅ Successfully exported data to: {export_path}")
            # Verify file exists
            export_file = Path(export_path)
            if export_file.exists():
                print(f"   Export file size: {export_file.stat().st_size} bytes")
            else:
                print("❌ Export file does not exist")
                return False
        else:
            print("❌ Failed to export data")
            return False
            
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        return False
    
    return True

def main():
    """Main test function."""
    print("🧪 Starting Audit Trail Implementation Tests")
    print("="*60)
    
    # Run all tests
    tests = [
        ("Basic Audit Logging", test_basic_audit_logging),
        ("Audit Querying", test_audit_querying),
        ("Error Logging", test_error_logging),
        ("Storage Operations", test_storage_operations)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                print(f"\n🎉 {test_name}: PASSED")
            else:
                print(f"\n💥 {test_name}: FAILED")
        except Exception as e:
            print(f"\n💥 {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Audit Trail implementation is working correctly.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
