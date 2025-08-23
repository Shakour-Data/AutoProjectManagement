#!/usr/bin/env python3
"""
Demo script to demonstrate the persistence functionality of the Project Management System.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autoprojectmanagement.main_modules.project_management_system import ProjectManagementSystem

def demo_persistence():
    """Demonstrate the persistence functionality"""
    print("=== Project Management System Persistence Demo ===")
    print()
    
    # Create a new instance
    pms = ProjectManagementSystem()
    
    # Initialize the system (this will load any existing data)
    pms.initialize_system()
    print("System initialized. Loading existing data...")
    print(f"Number of projects: {len(pms.projects)}")
    print(f"Number of tasks: {sum(len(tasks) for tasks in pms.tasks.values())}")
    print()
    
    # Add a new project
    project = {
        "id": 1,
        "name": "Demo Project",
        "description": "A demonstration project for persistence testing",
        "status": "active"
    }
    
    if pms.add_project(project):
        print(f"✓ Added project: {project['name']}")
    else:
        print(f"✗ Failed to add project: {project['name']}")
    
    # Add a task to the project
    task = {
        "id": 1,
        "title": "Demo Task",
        "description": "A demonstration task",
        "status": "todo",
        "priority": "high"
    }
    
    if pms.add_task_to_project(1, task):
