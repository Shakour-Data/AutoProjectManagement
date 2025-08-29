#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple GitHub Integration Test
Purpose: Basic testing of GitHub integration enhancements
Author: AutoProjectManagement Team
Version: 1.0.0
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_github_integration_import():
    """Test that GitHubIntegration can be imported and instantiated"""
    print("Testing GitHubIntegration import...")
    
    try:
        # Import the module directly
        import importlib.util
        
        spec = importlib.util.spec_from_file_location(
            "github_integration", 
            "src/autoprojectmanagement/services/integration_services/github_integration.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Test instantiation
        github = module.GitHubIntegration('test_owner', 'test_repo')
        print("✅ GitHubIntegration imported and instantiated successfully")
        
        # Test webhook subscriptions
        subscriptions = github.get_webhook_subscriptions()
        print(f"✅ Webhook subscriptions: {len(subscriptions)} available events")
        
        return True
        
    except Exception as e:
        print(f"❌ GitHubIntegration test failed: {e}")
        return False

def test_integration_manager_import():
    """Test that IntegrationManager can be imported and instantiated"""
    print("Testing IntegrationManager import...")
    
    try:
        # Import the module directly
        import importlib.util
        
        spec = importlib.util.spec_from_file_location(
            "integration_manager", 
            "src/autoprojectmanagement/services/integration_services/integration_manager.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Test instantiation
        manager = module.IntegrationManager()
        print("✅ IntegrationManager imported and instantiated successfully")
        
        # Test GitHub integration setup
        manager.setup_github_integration('test_owner', 'test_repo')
        print("✅ GitHub integration setup completed")
        
        return True
        
    except Exception as e:
        print(f"❌ IntegrationManager test failed: {e}")
        return False

def test_webhook_functionality():
    """Test webhook handling functionality"""
    print("Testing webhook functionality...")
    
    try:
        # Import both modules
        import importlib.util
        
        # Import GitHubIntegration
        github_spec = importlib.util.spec_from_file_location(
            "github_integration", 
            "src/autoprojectmanagement/services/integration_services/github_integration.py"
        )
        github_module = importlib.util.module_from_spec(github_spec)
        github_spec.loader.exec_module(github_module)
        
        # Import IntegrationManager
        manager_spec = importlib.util.spec_from_file_location(
            "integration_manager", 
            "src/autoprojectmanagement/services/integration_services/integration_manager.py"
        )
        manager_module = importlib.util.module_from_spec(manager_spec)
        manager_spec.loader.exec_module(manager_module)
        
        # Create instances
        github = github_module.GitHubIntegration('test_owner', 'test_repo')
        manager = manager_module.IntegrationManager()
        
        # Test webhook event handling
        test_payload = {
            'action': 'opened',
            'issue': {
                'number': 123,
                'title': 'Test Issue'
            }
        }
        
        # Test GitHub's handle_webhook_event
        callback_called = [False]
        def test_callback(event_type, payload):
            callback_called[0] = True
            print(f"✅ Callback received {event_type} event")
        
        github.handle_webhook_event('issues', test_payload, test_callback)
        
        if callback_called[0]:
            print("✅ GitHub webhook event handling works")
        else:
            print("❌ GitHub webhook event handling failed")
            return False
        
        # Test IntegrationManager's webhook handling
        manager.setup_github_integration('test_owner', 'test_repo')
        
        event_handled = [False]
        def test_handler(event_type, payload):
            event_handled[0] = True
            print(f"✅ Manager handled {event_type} event")
        
        manager.register_event_handler('issues', test_handler)
        manager._handle_webhook_event('issues', test_payload)
        
        if event_handled[0]:
            print("✅ IntegrationManager webhook handling works")
        else:
            print("❌ IntegrationManager webhook handling failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Webhook functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running GitHub Integration Tests...")
    print("=" * 50)
    
    tests = [
        test_github_integration_import,
        test_integration_manager_import,
        test_webhook_functionality
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
            print()
    
    print("=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i}. {test.__name__}: {status}")
    
    print("=" * 50)
    if all(results):
        print("🎉 All tests passed!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
