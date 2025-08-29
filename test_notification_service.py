#!/usr/bin/env python3
"""
Simple test script to verify the notification service functionality.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from autoprojectmanagement.services.notification_service import NotificationService

def test_notification_service():
    """Test the notification service functionality."""
    print("Testing Notification Service...")
    
    # Initialize the service
    service = NotificationService()
    
    # Test 1: Basic initialization
    print("✓ Service initialized successfully")
    
    # Test 2: Send scope change notification
    change_data = {
        'task_id': 'task_001',
        'change_type': 'add',
        'requester': 'test_user',
        'details': {
            'parent_id': 'phase_1',
            'task': {
                'name': 'Test Task',
                'id': 'task_001'
            }
        },
        'approval_status': {
            'status': 'pending'
        }
    }
    
    impact_analysis = {
        'schedule_impact': 3,
        'cost_impact': 1500,
        'resource_impact': 1,
        'risk_level': 'low'
    }
    
    recipients = ['test@example.com']
    
    success = service.send_scope_change_notification(
        change_data, impact_analysis, recipients
    )
    
    print(f"✓ Scope change notification sent: {success}")
    
    # Test 3: Send quality alert
    quality_data = {
        'quality_level': 'MEDIUM',
        'quality_score': 75.5,
        'poor_quality_tasks': 2,
        'task_quality': {
            'task_001': {
                'level': 'LOW',
                'metrics': {
                    'code_coverage': {
                        'score': 60,
                        'target': 80
                    }
                }
            }
        },
        'recommendations': [
            "Improve code coverage for task_001",
            "Add more documentation"
        ]
    }
    
    success = service.send_quality_alert(
        'Test Project', quality_data, recipients
    )
    
    print(f"✓ Quality alert sent: {success}")
    
    # Test 4: Check delivery history
    history = service.get_delivery_history()
    print(f"✓ Delivery history: {len(history)} records")
    
    for record in history:
        print(f"  - {record['template']}: {record['success']}")
    
    print("\n✅ All notification service tests passed!")
    return True

if __name__ == "__main__":
    try:
        test_notification_service()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
