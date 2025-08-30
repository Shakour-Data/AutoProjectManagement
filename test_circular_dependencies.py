#!/usr/bin/env python3
"""
Test script for circular dependency detection
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the dependency manager directly
from src.autoprojectmanagement.main_modules.planning_estimation.dependency_manager import DependencyManager

# Test with circular dependencies
circular_wbs = {
    "id": "project_root",
    "name": "Circular Test Project",
    "subtasks": [
        {
            "id": "task_1",
            "name": "Task 1",
            "dependencies": ["task_3"]  # Circular: depends on task 3
        },
        {
            "id": "task_2", 
            "name": "Task 2",
            "dependencies": ["task_1"]  # Normal dependency
        },
        {
            "id": "task_3",
            "name": "Task 3", 
            "dependencies": ["task_2"]  # Circular: depends on task 2 which depends on task 1 which depends on task 3
        }
    ]
}

print("Testing circular dependency detection...")
manager = DependencyManager()
manager.load_dependencies_from_wbs(circular_wbs)

# Validate dependencies
errors = manager.validate_dependencies()
if errors:
    print("Dependency validation errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Dependencies are valid!")

# Test circular dependency detection
circular_deps = manager.detect_circular_dependencies()
if circular_deps:
    print("Circular dependencies found:")
    for chain in circular_deps:
        print(f"  - {' -> '.join(chain)}")
else:
    print("No circular dependencies found")

# Test missing dependency
missing_dep_wbs = {
    "id": "project_root",
    "name": "Missing Dependency Test",
    "subtasks": [
        {
            "id": "task_1",
            "name": "Task 1",
            "dependencies": ["non_existent_task"]  # Missing dependency
        }
    ]
}

print("\nTesting missing dependency detection...")
manager2 = DependencyManager()
manager2.load_dependencies_from_wbs(missing_dep_wbs)

errors = manager2.validate_dependencies()
if errors:
    print("Dependency validation errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Dependencies are valid!")
