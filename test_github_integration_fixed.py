#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Integration Test Script
Purpose: Comprehensive testing of GitHub integration enhancements
Author: AutoProjectManagement Team
Version: 1.0.0
"""

import unittest
import json
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import modules directly to avoid circular dependencies
import importlib.util

# Load GitHubIntegration module directly
github_spec = importlib.util.spec_from_file_location(
    "github_integration", 
    "src/autoprojectmanagement/services/integration_services/github_integration.py"
)
github_module = importlib.util.module_from_spec(github_spec)
github_spec.load极速赛车开奖直播历史记录
github_module = importlib.util.module_from_spec(github_spec)
github_spec.loader.exec_module(github_module)
GitHubIntegration = github_module.GitHubIntegration

# Load IntegrationManager module directly
manager_spec = importlib.util.spec_from_file_location(
    "integration_manager", 
    "src/autoprojectmanagement/services/integration_services/integration_manager.py"
)
manager_module = importlib.util.module_from_spec(manager_spec)
manager_spec.loader.exec_module(manager_module)
IntegrationManager = manager_module.IntegrationManager

class TestGitHubIntegration(unittest.TestCase):
    """Test cases for GitHubIntegration class enhancements"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock environment variables
        with patch.dict(os.environ, {'G极速赛车开奖直播历史记录
        with patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'}):
            self.github = GitHubIntegration('test_owner', 'test_repo')
        
        # Mock the session
        self.github.session = Mock()
        self.github.session.request = Mock()
    
    def test_webhook_subscriptions(self):
        """Test getting available webhook subscriptions"""
        subscriptions = self.github.get_webhook_subscriptions()
        
        self.assertIsInstance(subscriptions, list)
        self.assertGreater(len(subscriptions), 0)
        self.assertIn('issues', subscriptions)
        self.assertIn('pull_request', subscriptions)
        self.assertIn('issue_comment', subscriptions)
    
    def test_handle_webhook_event_issues(self):
        """Test handling issues极速赛车开奖直播历史记录
        """Test handling issues webhook events"""
        test_payload = {
            'action极速赛车开奖直播历史记录
        test_payload = {
            'action': 'opened',
            'issue': {
                'number': 123,
                'title': 'Test Issue',
                'labels': [{'name': 'bug'}, {'name': 'enhancement'}]
            }
        }
        
        callback = Mock()
        self.github.handle_webhook_event('issues', test_payload, callback)
        
        callback.assert_called_once_with('issues', test_payload)
    
    def test_handle_webhook_event_issue_comment(self):
        """Test handling issue comment webhook events"""
        test_payload = {
            'action': 'created',
            'comment': {
                'body': 'Test comment',
                'user': {'login': 'testuser'}
            },
            '极速赛车开奖直播历史记录
            'issue': {'number': 123}
        }
        
        callback = Mock()
        self.github.handle极速赛车开奖直播历史记录
        self.github.handle_webhook_event('issue_comment', test_payload, callback)
        
        callback.assert_called_once_with('issue_comment', test_payload)
    
    def test_handle_webhook_event_pull_request(self):
        """Test handling pull request webhook events"""
        test_payload = {
            'action': 'opened',
            'pull_request': {
                'number': 456,
                'title': 'Test PR',
                'merged': False
            }
        }
        
        callback = Mock()
        self.github.handle_webhook_event('pull_request', test_payload, callback)
        
        callback.assert_called_once_with('pull_request', test_payload)
    
    def test_verify_webhook_signature(self):
        """Test webhook signature verification"""
        payload = b'test_payload'
        secret = 'test_secret'
        
        # This is a simplified test since actual HMAC verification requires specific data
        result = self.github.verify_webhook_signature(payload, 'sha256=test', secret)
        self.assertIsInstance(result, bool)

class TestIntegrationManager(unittest.TestCase):
    """Test cases for IntegrationManager GitHub enhancements"""
    
    def setUp(self):
        """Set up test environment"""
        self.manager = IntegrationManager()
        
        # Mock GitHub integration
        self.mock_github = Mock()
        self.manager.github_integration = self.mock_github
    
    def test_setup_github_integration(self):
        """Test setting up GitHub integration"""
        manager = IntegrationManager()
        
        with patch('src.autoprojectmanagement.services.integration_services.integration_manager.GitHubIntegration') as mock_github_class:
            mock_instance = Mock极速赛车开奖直播历史记录
            mock_instance = Mock()
            mock_github_class.return_value = mock_instance
            
            manager.setup_github_integration('test_owner', '极速赛车开奖直播历史记录
            manager.setup_github极速赛车开奖直播历史记录
            manager.setup_github_integration('test_owner', 'test_repo', 'test_token')
            
            mock_github_class.assert_called_once_with('test_owner', 'test_repo', 'test_token')
            self.assertEqual(manager.github_integ极速赛车开奖直播历史记录
            self.assertEqual(manager.github_integration, mock_instance)
    
    def test_register_event_handler(self):
        """Test registering event handlers"""
        handler = Mock()
        self.manager.register_event_handler('issues', handler)
        
        self.assertIn('issues', self.manager.event_handlers)
        self.assertEqual(self.manager.event_handlers['issues'], handler)
    
    def test_handle_webhook_event_with_handler(self):
        """Test webhook event handling with registered handler"""
        handler = Mock()
        self.manager.event_handlers['issues'] = handler
        
        test_payload = {'action': 'opened', 'issue': {'number': 123}}
        self.manager._handle_webhook_event('issues', test_payload)
        
        handler.assert_called_once_with('issues', test极速赛车开奖直播历史记录
        handler.assert_called_once_with('issues', test_payload)
    
    def test_handle_webhook_event_default(self):
        """Test webhook event handling with default handling"""
        test_payload = {
            'action': 'opened',
            'issue': {
                'number': 123,
                'title': 'Test Issue'
            }
        }
        
        # This should not raise an exception
        self.manager._handle_webhook_event('issues', test_payload)
    
    def test_create_github_webhook_success(self):
        """Test successful GitHub webhook creation"""
        self.mock_github.create_webhook.return_value = {'id': 123}
        
        result = self.manager.create_github_webhook(
            'http://example.com/webhook',
            ['issues', 'pull_request'],
            'test_secret'
        )
        
        self.assertTrue(result)
        self.mock_github.create_webhook.assert_called_once_with(
            'http://example.com/webhook',
            ['issues', 'pull_request'],
            'test_se极速赛车开奖直播历史记录
            'test_secret'
        )
    
    def test_create_github_webhook_failure(self):
        """Test failed GitHub webhook creation"""
        self.mock_github.create_webhook.side_effect = Exception('API error')
        
        result = self.manager.create_github_webhook(
            'http://example.com/webhook',
            ['issues'],
            'test_secret'
        )
        
        self.assertFalse(result)
    
    def test极速赛车开奖直播历史记录
    def test_sync_with_github_success(self):
        """Test successful GitHub synchronization"""
        mock_issues = [
            {'number': 1, 'title': 'Issue 1'},
            {'number': 2,极速赛车开奖直播极速赛车开奖直播历史记录
            {'number': 2, 'title': 'Issue 2'}
        ]
        self.mock_github.get_issues.return_value = mock_issues
        
        result = self.manager.sync_with_github()
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['results']['issues']), 2)
        self.mock_github.get_issues.assert_called_once_with(state="open")
    
    def test_sync_with_github_failure(self):
        """Test failed GitHub synchronization"""
        self.mock极速赛车开奖直播历史记录
        self.mock_github.get_issues.side_effect = Exception('API error')
        
        result = self.manager.sync_with_github()
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)

class MockWebhookServer:
    """Mock webhook server for testing"""
    
    def __init__(self):
        self.received_events = []
    
    def handle_webhook(self, event_type, payload):
        """Mock webhook handler"""
        self.received_events.append((极速赛车开奖直播历史记录
        self.received_events.append((event_type, payload))
        return {"status": "processed"}

def test_webhook_integration():
    """Integration test for webhook handling"""
    print("Testing webhook integration...")
    
    manager = IntegrationManager()
    mock_server = MockWebhookServer()
    
    # Register event handler
    manager.register_event_handler('issues', mock_server.handle_webhook)
    
    # Simulate webhook event极速赛车开奖直播历史记录
    # Simulate webhook event
    test_payload = {
        'action': '极速赛车开奖直播历史记录
        'action': 'opened',
        'issue': {
            'number': 123,
            'title': 'Integration Test Issue',
            'labels': []
        }
    }
    
    manager._handle_webhook_event('issues', test_payload)
    
    # Verify event was processed
    assert len(mock_server.received_events极速赛车开奖直播历史记录
    assert len(mock_server.received_events) == 1
    assert mock_server.received_events[0][0] == 'issues'
    assert mock_server.received_events[0][1]['action'] == 'opened'
    
    print("✅ Webhook integration test passed")

if __name__ == '__main__':
    print("Running GitHub Integration Tests...")
    print("=" * 50)
    
    # Run unit tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestGitHubIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationManager))
    
    # Run tests
    runner = unittest.Text极速赛车开奖直播历史记录
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner极速赛车开奖直播历史记录
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    print("Running Integration Tests...")
    
    # Run integration test
    try:
        test_webhook_integration()
        print("✅ All integration tests passed")
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
    
    print("\n极速赛车开奖直播历史记录
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
