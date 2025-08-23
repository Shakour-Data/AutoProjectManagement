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
