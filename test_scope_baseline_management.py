#!/usr/bin/env python3
"""
Test script for scope baseline management functionality.
"""

import json
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from autoprojectmanagement.main_modules.planning_estimation.scope_management import ScopeManagement

def create_test_data():
    """Create test data for baseline management testing."""
    
    # Create test WBS data
    test_wbs = {
        'id': 'project_root',
        'name': 'Test Project',
        'description': 'Test project for baseline management',
        'estimated_duration': 30,
        'resource_cost': 5000,
        'subtasks': [
            {
                'id': 'task_1',
                'name': 'Task 1',
                'description': 'First task',
                'estimated_duration': 5,
                'resource_cost': 1000,
                'subtasks': []
            },
            {
                'id': 'task_2',
                'name': 'Task 2',
                'description': 'Second task',
                'estimated_duration': 10,
                'resource_cost': 2000,
                'subtasks': []
            }
        ]
    }
    
    # Create test scope changes
    test_changes = [
        {
            'task_id': 'task_3',
            'change_type': 'add',
            'details': {
                'parent_id': 'project_root',
                'task': {
                    'id': 'task_3',
                    'name': 'Task 3',
                    'description': 'Third task (added)',
                    'estimated_duration': 8,
                    'resource_cost': 1500
                }
            }
        }
    ]
    
    return test_wbs, test_changes

def setup_test_environment():
    """Set up test environment with test data."""
    
    # Create test directories
    test_dirs = [
        'data/inputs/UserInputs',
        'data/inputs/OutPuts'
    ]
    
    for dir_path in test_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Create test files
    test_wbs, test_changes = create_test_data()
    
    with open('data/inputs/UserInputs/detailed_wbs.json', 'w') as f:
        json.dump(test_wbs, f, indent=2)
    
    with open('data/inputs/UserInputs/scope_changes.json', 'w') as f:
        json.dump(test_changes, f, indent=2)
    
    print("Test environment setup complete")

def test_baseline_creation():
    """Test baseline creation functionality."""
    print("\n=== Testing Baseline Creation ===")
    
    manager = ScopeManagement()
    manager.load_inputs()
    
    # Create first baseline
    success = manager.create_baseline(
        "initial_baseline", 
        "Initial project baseline"
    )
    
    print(f"Baseline creation successful: {success}")
    
    # Create another baseline after making changes
    manager.apply_scope_changes()
    
    success = manager.create_baseline(
        "after_changes_baseline",
        "Baseline after applying scope changes"
    )
    
    print(f"Second baseline creation successful: {success}")
    
    return success

def test_baseline_listing():
    """Test baseline listing functionality."""
    print("\n=== Testing Baseline Listing ===")
    
    manager = ScopeManagement()
    
    baselines = manager.get_baseline_list()
    print(f"Available baselines: {len(baselines)}")
    
    for baseline in baselines:
        print(f"  - {baseline['name']}: {baseline['description']} (v{baseline['version']})")
    
    return baselines

def test_baseline_comparison():
    """Test baseline comparison functionality."""
    print("\n=== Testing Baseline Comparison ===")
    
    manager = ScopeManagement()
    manager.load_inputs()
    
    # Compare with initial baseline
    comparison = manager.compare_with_baseline("initial_baseline")
    
    print(f"Comparison with 'initial_baseline':")
    print(f"  Tasks added: {comparison['summary']['tasks_added']}")
    print(f"  Tasks removed: {comparison['summary']['tasks_removed']}")
    print(f"  Tasks modified: {comparison['summary']['tasks_modified']}")
    
    # Show detailed differences
    if comparison['differences']:
        print("\nDetailed differences:")
        for diff in comparison['differences'][:5]:  # Show first 5 differences
            print(f"  {diff['type']}: {diff.get('task_id', diff.get('field', 'unknown'))}")
    
    return comparison

def test_baseline_restoration():
    """Test baseline restoration functionality."""
    print("\n=== Testing Baseline Restoration ===")
    
    manager = ScopeManagement()
    manager.load_inputs()
    
    # Get current state
    current_tasks = len(manager.detailed_wbs.get('subtasks', []))
    print(f"Current tasks before restoration: {current_tasks}")
    
    # Restore to initial baseline
    success = manager.restore_baseline("initial_baseline")
    print(f"Restoration successful: {success}")
    
    # Check restored state
    restored_tasks = len(manager.detailed_wbs.get('subtasks', []))
    print(f"Tasks after restoration: {restored_tasks}")
    
    return success

def test_baseline_deletion():
    """Test baseline deletion functionality."""
    print("\n=== Testing Baseline Deletion ===")
    
    manager = ScopeManagement()
    
    # List baselines before deletion
    baselines_before = manager.get_baseline_list()
    print(f"Baselines before deletion: {len(baselines_before)}")
    
    # Delete a baseline
    success = manager.delete_baseline("after_changes_baseline")
    print(f"Deletion successful: {success}")
    
    # List baselines after deletion
    baselines_after = manager.get_baseline_list()
    print(f"Baselines after deletion: {len(baselines_after)}")
    
    return success

def main():
    """Main test function."""
    print("Starting Scope Baseline Management Tests")
    print("=" * 50)
    
    try:
        # Setup test environment
        setup_test_environment()
        
        # Run tests
        test_baseline_creation()
        test_baseline_listing()
        test_baseline_comparison()
        test_baseline_restoration()
        test_baseline_deletion()
        
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
