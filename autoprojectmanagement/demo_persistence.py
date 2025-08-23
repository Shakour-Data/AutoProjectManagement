#!/usr/bin/env python3
"""
Demo script to demonstrate the persistence functionality of the Project Management System.
"""

import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    
    # Check if we already have data
    if len(pms.projects) == 0:
        # Add a new project only if none exist
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
            print(f"✓ Added task: {task['title']} to project {project['name']}")
        else:
            print(f"✗ Failed to add task: {task['title']}")
    else:
        print("✓ Existing data loaded from storage")
        print("  No new data added to avoid duplicates")
    
    print()
    print("Data has been saved to JSON files in the .auto_project_data directory.")
    print()
    
    # Show the current state
    print("Current state:")
    print(f"Projects: {len(pms.projects)}")
    for project_id, project_data in pms.projects.items():
        print(f"  - Project {project_id}: {project_data['name']}")
        if project_id in pms.tasks:
            print(f"    Tasks: {len(pms.tasks[project_id])}")
            for task_id, task_data in pms.tasks[project_id].items():
                print(f"      - Task {task_id}: {task_data['title']}")
    
    print()
    print("To verify persistence, run this script again to see the data loaded from files.")
    print("The data will persist between script executions.")

if __name__ == "__main__":
    demo_persistence()
