#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Notification Service
Purpose: Test email notification functionality and configuration
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from autoprojectmanagement.services.notification_service import NotificationService

def test_notification_service():
    """Test the notification service functionality."""
    print("Testing Notification Service...")
    
    # Initialize the notification service
    service = NotificationService()
    
    print(f"Email enabled: {service.config['email']['enabled']}")
    print(f"SMTP Server: {service.config['email']['smtp_server']}")
    print(f"From Address: {service.config['email']['from_address']}")
    
    # Test configuration validation
    email_config = service.config['email']
    if not all([email_config['smtp_server'], email_config['username'], email_config['password']]):
        print("⚠️  Email configuration is incomplete. Please update notification_config.json")
        print("   Required fields: smtp_server, username, password, from_address")
        return False
    
    # Test template loading
    print(f"Loaded templates: {list(service.templates.keys())}")
    
    # Test scope change notification
    change_data = {
        'task_id': 'test_task_001',
        'change_type': 'add',
        'requester': 'test_user',
        'details': {
            'parent_id': 'project_root',
            'task': {
                'name': 'Test Task',
                'id': 'test_task_001'
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
    
    # Use test recipients from config or default
    test_recipients = service.config.get('default_recipients', ['test@example.com'])
    
    print(f"Testing with recipients: {test_recipients}")
    
    try:
        success = service.send_scope_change_notification(
            change_data,
            impact_analysis,
            test_recipients
        )
        
        if success:
            print("✅ Scope change notification test completed successfully!")
            print("Check your email inbox for the notification.")
        else:
            print("❌ Scope change notification failed")
            print("This might be due to SMTP configuration issues.")
            
    except Exception as e:
        print(f"❌ Error during notification test: {e}")
        return False
    
    # Test delivery history
    history = service.get_delivery_history()
    print(f"Delivery history entries: {len(history)}")
    
    if history:
        latest = history[-1]
        print(f"Latest notification: {latest['subject']}")
        print(f"Success: {latest['success']}")
    
    return True

def test_email_configuration():
    """Test email configuration specifically."""
    print("\nTesting Email Configuration...")
    
    service = NotificationService()
    
    # Check if email is enabled
    if not service.config['email']['enabled']:
        print("❌ Email notifications are disabled")
        return False
    
    # Check required configuration
    required_fields = ['smtp_server', 'username', 'password', 'from_address']
    email_config = service.config['email']
    
    missing_fields = []
    for field in required_fields:
        if not email_config.get(field):
            missing_fields.append(field)
    
    if missing_fields:
        print(f"❌ Missing email configuration fields: {missing_fields}")
        print("Please update notification_config.json with proper SMTP settings")
        return False
    
    print("✅ Email configuration appears valid")
    print(f"SMTP Server: {email_config['smtp_server']}:{email_config['smtp_port']}")
    print(f"Username: {email_config['username']}")
    print(f"From Address: {email_config['from_address']}")
    
    return True

if __name__ == "__main__":
    print("AutoProjectManagement Notification Service Test")
    print("=" * 50)
    
    # Test configuration first
    config_ok = test_email_configuration()
    
    if config_ok:
        # Test full notification service
        test_notification_service()
    else:
        print("\nPlease configure your email settings in:")
        print("data/inputs/UserInputs/notification_config.json")
        print("\nFor Gmail, you'll need:")
        print("- Enable 2-factor authentication")
        print("- Generate an App Password")
        print("- Use smtp.gmail.com:587")
        print("- Use your full email as username")
        print("- Use the app password (not your regular password)")
