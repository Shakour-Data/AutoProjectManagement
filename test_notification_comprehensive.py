#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Test Script for Notification Service
Purpose: Test all notification channels and integration scenarios
"""

import os
import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from autoprojectmanagement.services.notification_service import NotificationService

class TestNotificationService:
    """Comprehensive test class for NotificationService"""
    
    def setup_method(self):
        """Setup test environment"""
        self.service = NotificationService()
        
    def test_config_loading(self):
        """Test configuration loading from file and environment"""
        print("Testing configuration loading...")
        
        # Test that config is loaded
        assert 'email' in self.service.config
        assert 'slack' in self.service.config
        assert 'teams' in self.service.config
        assert 'console' in self.service.config
        
        # Test default values
        assert self.service.config['email']['enabled'] == True
        assert self.service.config['email']['smtp_server'] == 'smtp.gmail.com'
        assert self.service.config['email']['smtp_port'] == 587
        
        print("✅ Configuration loading test passed")
    
    def test_template_loading(self):
        """Test template loading functionality"""
        print("Testing template loading...")
        
        # Test that templates are loaded
        required_templates = [
            'scope_change_add', 'scope_change_remove', 'scope_change_modify',
            'approval_required', 'quality_alert'
        ]
        
        for template in required_templates:
            assert template in self.service.templates, f"Missing template: {template}"
            assert 'subject' in self.service.templates[template]
            assert 'body' in self.service.templates[template]
            assert 'priority' in self.service.templates[template]
        
        print("✅ Template loading test passed")
    
    def test_scope_change_notification(self):
        """Test scope change notification with different change types"""
        print("Testing scope change notifications...")
        
        test_cases = [
            {
                'name': 'Add task',
                'change_type': 'add',
                'expected_template': 'scope_change_add'
            },
            {
                'name': 'Remove task', 
                'change_type': 'remove',
                'expected_template': 'scope_change_remove'
            },
            {
                'name': 'Modify task',
                'change_type': 'modify', 
                'expected_template': 'scope_change_modify'
            }
        ]
        
        for test_case in test_cases:
            change_data = {
                'task_id': f'test_{test_case["change_type"]}_001',
                'change_type': test_case['change_type'],
                'requester': 'test_user',
                'details': {
                    'parent_id': 'project_root',
                    'task': {'name': f'Test {test_case["name"]}', 'id': f'test_{test_case["change_type"]}_001'}
                },
                'approval_status': {'status': 'pending'}
            }
            
            impact_analysis = {
                'schedule_impact': 2,
                'cost_impact': 1000,
                'resource_impact': 1,
                'risk_level': 'low'
            }
            
            recipients = ['test@example.com']
            
            # Mock the send_notification method to avoid actual email sending
            with patch.object(self.service, 'send_notification') as mock_send:
                mock_send.return_value = True
                
                success = self.service.send_scope_change_notification(
                    change_data, impact_analysis, recipients
                )
                
                assert success == True
                mock_send.assert_called_once()
                called_template = mock_send.call_args[0][0]  # First argument is template_key
                assert called_template == test_case['expected_template']
                
                print(f"✅ {test_case['name']} notification test passed")
    
    def test_approval_required_notification(self):
        """Test approval required notification"""
        print("Testing approval required notification...")
        
        change_data = {
            'task_id': 'test_approval_001',
            'change_type': 'add',
            'requester': 'test_user',
            'details': {
                'parent_id': 'project_root',
                'task': {'name': 'Test Approval Task', 'id': 'test_approval_001'}
            },
            'approval_status': {
                'status': 'requires_approval',
                'conditions': ['Budget approval required', 'Schedule impact > 5 days']
            }
        }
        
        impact_analysis = {
            'schedule_impact': 10,
            'cost_impact': 5000,
            'resource_impact': 3,
            'risk_level': 'high'
        }
        
        recipients = ['manager@example.com']
        
        with patch.object(self.service, 'send_notification') as mock_send:
            mock_send.return_value = True
            
            success = self.service.send_scope_change_notification(
                change_data, impact_analysis, recipients
            )
            
            assert success == True
            mock_send.assert_called_once()
            called_template = mock_send.call_args[0][0]
            assert called_template == 'approval_required'
            
            # Check that approval conditions are included
            context = mock_send.call_args[0][1]
            assert 'approval_conditions' in context
            assert 'Budget approval required' in context['approval_conditions']
            
        print("✅ Approval required notification test passed")
    
    def test_quality_alert_notification(self):
        """Test quality alert notification"""
        print("Testing quality alert notification...")
        
        quality_data = {
            'quality_level': 'POOR',
            'quality_score': 45,
            'poor_quality_tasks': 3,
            'task_quality': {
                'task_001': {
                    'level': 'POOR',
                    'metrics': {
                        'completeness': {'score': 30, 'target': 80},
                        'accuracy': {'score': 40, 'target': 90}
                    }
                }
            },
            'recommendations': [
                'Review task completion criteria',
                'Conduct quality training session'
            ]
        }
        
        recipients = ['qa_team@example.com', 'manager@example.com']
        
        with patch.object(self.service, 'send_notification') as mock_send:
            mock_send.return_value = True
            
            success = self.service.send_quality_alert(
                'Test Project', quality_data, recipients
            )
            
            assert success == True
            mock_send.assert_called_once()
            called_template = mock_send.call_args[0][0]
            assert called_template == 'quality_alert'
            
            # Check context contains quality data
            context = mock_send.call_args[0][1]
            assert context['project_name'] == 'Test Project'
            assert context['quality_level'] == 'POOR'
            assert context['quality_score'] == 45
            
        print("✅ Quality alert notification test passed")
    
    def test_delivery_history(self):
        """Test delivery history functionality"""
        print("Testing delivery history...")
        
        # Clear existing history
        self.service.delivery_history = []
        
        # Send a test notification
        with patch.object(self.service, '_send_email') as mock_email:
            mock_email.return_value = True
            
            success = self.service.send_notification(
                'scope_change_add',
                {
                    'task_id': 'test_history_001',
                    'task_name': 'Test History Task',
                    'parent_id': 'root',
                    'requester': 'test_user',
                    'timestamp': '2024-01-01T00:00:00',
                    'schedule_impact': 1,
                    'cost_impact': 500,
                    'resource_impact': 1,
                    'risk_level': 'low',
                    'approval_status': 'pending',
                    'next_steps': 'Review',
                    'changes_summary': 'N/A'
                },
                ['test@example.com']
            )
            
            assert success == True
            
            # Check delivery history
            history = self.service.get_delivery_history()
            assert len(history) == 1
            assert history[0]['template'] == 'scope_change_add'
            assert history[0]['success'] == True
            assert len(history[0]['channels']) > 0
            
        print("✅ Delivery history test passed")
    
    def test_channel_fallback(self):
        """Test channel fallback mechanism"""
        print("Testing channel fallback...")
        
        # Test with email disabled but console enabled
        original_config = self.service.config.copy()
        self.service.config['email']['enabled'] = False
        
        with patch.object(self.service, '_send_console') as mock_console:
            mock_console.return_value = True
            
            success = self.service.send_notification(
                'scope_change_add',
                {
                    'task_id': 'test_fallback_001',
                    'task_name': 'Test Fallback Task',
                    'parent_id': 'root',
                    'requester': 'test_user',
                    'timestamp': '2024-01-01T00:00:00',
                    'schedule_impact': 1,
                    'cost_impact': 500,
                    'resource_impact': 1,
                    'risk_level': 'low',
                    'approval_status': 'pending',
                    'next_steps': 'Review',
                    'changes_summary': 'N/A'
                },
                ['test@example.com']
            )
            
            assert success == True
            mock_console.assert_called_once()
            
        # Restore original config
        self.service.config = original_config
        
        print("✅ Channel fallback test passed")
    
    def test_configuration_precedence(self):
        """Test configuration loading precedence"""
        print("Testing configuration precedence...")
        
        # Test that file config takes precedence over defaults
        service_with_config = NotificationService(
            config_path='data/inputs/UserInputs/notification_config.json'
        )
        
        # Should load from file if it exists
        assert service_with_config.config is not None
        
        print("✅ Configuration precedence test passed")

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("=" * 60)
    print("COMPREHENSIVE NOTIFICATION SERVICE TESTS")
    print("=" * 60)
    
    test_suite = TestNotificationService()
    
    try:
        test_suite.setup_method()
        test_suite.test_config_loading()
        test_suite.test_template_loading()
        test_suite.test_scope_change_notification()
        test_suite.test_approval_required_notification()
        test_suite.test_quality_alert_notification()
        test_suite.test_delivery_history()
        test_suite.test_channel_fallback()
        test_suite.test_configuration_precedence()
        
        print("=" * 60)
        print("✅ ALL COMPREHENSIVE TESTS PASSED!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
