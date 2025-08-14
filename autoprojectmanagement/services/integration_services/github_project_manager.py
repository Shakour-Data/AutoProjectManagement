#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: github_project_manager
File: github_project_manager.py
Path: autoprojectmanagement/services/integration_services/github_project_manager.py

Description:
    Github Project Manager module

Author: AutoProjectManagement Team
Contact: team@autoprojectmanagement.com
Repository: https://github.com/autoprojectmanagement/autoprojectmanagement

Version Information:
    Current Version: 1.0.0
    Last Updated: 2025-08-14
    Python Version: 3.8+
    
Development Status:
    Status: Production/Stable
    Created: 2024-01-01
    Last Modified: 2025-08-14
    Modified By: AutoProjectManagement Team

Dependencies:
    - Python 3.8+
    - See requirements.txt for full dependency list

License: MIT License
Copyright: (c) 2024 AutoProjectManagement Team

Usage:
    This module is part of the AutoProjectManagement package.
    Import and use as needed within the package ecosystem.

Example:
    >>> from autoprojectmanagement.services.integration_services.github_project_manager import {main_class}
    >>> instance = {main_class}()
    >>> instance.run()

Notes:
    - This file follows the AutoProjectManagement coding standards
    - All changes should be documented in the changelog below
    - Ensure compatibility with Python 3.8+

Changelog:
    1.0.0 (2024-01-01): Initial release
    1.0.1 (2025-08-14): {change_description}

TODO:
    - [ ] Add comprehensive error handling
    - [ ] Implement logging throughout
    - [ ] Add unit tests
    - [ ] Update documentation

================================================================================
"""


import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from .github_integration import GitHubIntegration

class GitHubProjectManager:
    """Manager for creating and managing GitHub projects with full integration"""
    
    def __init__(self, github_token: str = None):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
    def create_github_project_from_json(self, project_json_path: str, github_username: str) -> Dict[str, Any]:
        """Create a complete GitHub project from JSON configuration"""
        
        # Load project data from JSON
        with open(project_json_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
            
        project_name = project_data.get('name', 'untitled-project')
        project_description = project_data.get('description', '')
        
        # Initialize GitHub integration
        github = GitHubIntegration(github_username, project_name, self.github_token)
        
        # Generate all GitHub artifacts
        reports = github.generate_all_github_reports(project_name, project_data)
        
        # Save reports
        self._save_project_reports(project_name, reports)
        
        return reports
    
    def create_project_from_wbs(self, wbs_data: Dict[str, Any], github_username: str) -> Dict[str, Any]:
        """Create GitHub project from Work Breakdown Structure"""
        
        project_name = wbs_data.get('project_name', 'new-project')
        project_description = wbs_data.get('project_description', '')
        
        # Convert WBS to GitHub project data
        project_data = self._convert_wbs_to_github_format(wbs_data)
        
        # Create GitHub integration
        github = GitHubIntegration(github_username, project_name, self.github_token)
        
        # Generate all GitHub artifacts
        reports = github.generate_all_github_reports(project_name, project_data)
        
        return reports
    
    def _convert_wbs_to_github_format(self, wbs_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert WBS data to GitHub project format"""
        
        project_data = {
            "name": wbs_data.get('project_name', 'Project'),
            "description": wbs_data.get('project_description', ''),
            "phases": [],
            "categories": [
                {"name": "feature", "color": "a2eeef"},
                {"name": "bug", "color": "d73a4a"},
                {"name": "documentation", "color": "0075ca"},
                {"name": "enhancement", "color": "a2eeef"},
                {"name": "help-wanted", "color": "008672"}
            ],
            "tasks": []
        }
        
        # Convert phases
        for phase in wbs_data.get('phases', []):
            project_data["phases"].append({
                "name": phase.get('name', ''),
                "description": phase.get('description', '')
            })
        
        # Convert tasks
        for task in wbs_data.get('tasks', []):
            project_data["tasks"].append({
                "title": task.get('name', ''),
                "description": task.get('description', ''),
                "labels": [task.get('category', 'feature')],
                "assignees": task.get('assignees', [])
            })
        
        return project_data
    
    def _save_project_reports(self, project_name: str, reports: Dict[str, Any]):
        """Save project creation reports"""
        
        reports_dir = "github_reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(reports_dir, f"{project_name}_github_setup_{timestamp}.json")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(reports, f, indent=2, default=str)
        
        self.logger.info(f"GitHub project reports saved to {report_file}")
    
    def sync_project_with_github(self, project_data: Dict[str, Any], github_username: str) -> Dict[str, Any]:
        """Sync existing project with GitHub"""
        
        project_name = project_data.get('name', 'synced-project')
        
        # Initialize GitHub integration
        github = GitHubIntegration(github_username, project_name, self.github_token)
        
        # Check if repository exists
        try:
            repo_url = f"https://api.github.com/repos/{github_username}/{project_name}"
            response = requests.get(repo_url, headers=github.headers)
            if response.status_code == 404:
                # Repository doesn't exist, create it
                repo = github.create_repository(project_name, project_data.get('description', ''))
            else:
                repo = response.json()
        except Exception as e:
            self.logger.error(f"Error checking repository: {e}")
            repo = github.create_repository(project_name, project_data.get('description', ''))
        
        # Update project with latest data
        reports = github.generate_all_github_reports(project_name, project_data)
        
        return reports
    
    def create_github_project_cli(self, project_name: str, description: str = "", github_username: str = None):
        """Create GitHub project from CLI"""
        
        if not github_username:
            github_username = input("Enter your GitHub username: ")
        
        project_data = {
            "name": project_name,
            "description": description,
            "phases": [
                {"name": "Planning", "description": "Project planning and requirements gathering"},
                {"name": "Development", "description": "Core development phase"},
                {"name": "Testing", "description": "Testing and quality assurance"},
                {"name": "Deployment", "description": "Deployment and release"}
            ],
            "categories": [
                {"name": "feature", "color": "a2eeef"},
                {"name": "bug", "color": "d73a4a"},
                {"name": "documentation", "color": "0075ca"},
                {"name": "enhancement", "color": "a2eeef"}
            ],
            "tasks": [
                {"title": "Setup project repository", "description": "Initialize GitHub repository", "labels": ["setup"]},
                {"title": "Create project documentation", "description": "Write comprehensive project documentation", "labels": ["documentation"]},
                {"title": "Setup CI/CD pipeline", "description": "Configure GitHub Actions for CI/CD", "labels": ["enhancement"]}
            ]
        }
        
        github = GitHubIntegration(github_username, project_name, self.github_token)
        reports = github.generate_all_github_reports(project_name, project_data)
        
        print(f"\n✅ GitHub project '{project_name}' created successfully!")
        print(f"📊 Repository: https://github.com/{github_username}/{project_name}")
        print(f"📋 Project Board: https://github.com/{github_username}/{project_name}/projects")
        print(f"📝 Issues: https://github.com/{github_username}/{project_name}/issues")
        
        return reports

if __name__ == "__main__":
    # Example usage
    manager = GitHubProjectManager()
    
    # Create project from CLI
    project_name = "my-new-project"
    description = "A new project with full GitHub integration"
    github_username = "your-username"
    
    reports = manager.create_github_project_cli(project_name, description, github_username)
    
    print("\n📊 Project Reports:")
    print(json.dumps(reports, indent=2, default=str))
