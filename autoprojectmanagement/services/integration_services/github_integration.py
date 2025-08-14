#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: github_integration
File: github_integration.py
Path: autoprojectmanagement/services/integration_services/github_integration.py

Description:
    Github Integration module

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
    >>> from autoprojectmanagement.services.integration_services.github_integration import {main_class}
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


import requests
import os
import logging
import time
import json
from typing import Dict, List, Optional, Any

class GitHubIntegration:
    def __init__(self, repo_owner, repo_name, token=None, max_retries=3, retry_delay=2):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AutoProjectManagement/1.0"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def _request(self, method, url, data=None, params=None):
        """Generic request method with retry logic"""
        retries = 0
        while retries < self.max_retries:
            try:
                if method.upper() == 'GET':
                    response = requests.get(url, headers=self.headers, params=params, timeout=10)
                elif method.upper() == 'POST':
                    response = requests.post(url, headers=self.headers, json=data, timeout=10)
                elif method.upper() == 'PUT':
                    response = requests.put(url, headers=self.headers, json=data, timeout=10)
                elif method.upper() == 'PATCH':
                    response = requests.patch(url, headers=self.headers, json=data, timeout=10)
                elif method.upper() == 'DELETE':
                    response = requests.delete(url, headers=self.headers, timeout=10)
                
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}. Retry {retries + 1} of {self.max_retries}")
                retries += 1
                time.sleep(self.retry_delay)
        self.logger.error(f"Failed to complete {method} request to {url} after {self.max_retries} retries.")
        return None

    def create_repository(self, repo_name, description="", private=True, has_issues=True, has_projects=True, has_wiki=True):
        """Create a new repository in GitHub"""
        url = f"{self.api_base}/user/repos"
        data = {
            "name": repo_name,
            "description": description,
            "private": private,
            "has_issues": has_issues,
            "has_projects": has_projects,
            "has_wiki": has_wiki,
            "auto_init": True
        }
        return self._request('POST', url, data)

    def create_project_board(self, repo_name, project_name, description=""):
        """Create a new project board in GitHub"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{repo_name}/projects"
        data = {
            "name": project_name,
            "body": description,
            "state": "open"
        }
        return self._request('POST', url, data)

    def create_issue(self, repo_name, title, body="", labels=None, assignees=None, milestone=None):
        """Create a new issue in GitHub"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{repo_name}/issues"
        data = {
            "title": title,
            "body": body,
            "labels": labels or [],
            "assignees": assignees or [],
            "milestone": milestone
        }
        return self._request('POST', url, data)

    def create_milestone(self, repo_name, title, description="", due_date=None):
        """Create a new milestone in GitHub"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{repo_name}/milestones"
        data = {
            "title": title,
            "description": description,
            "state": "open"
        }
        if due_date:
            data["due_on"] = due_date
        return self._request('POST', url, data)

    def create_label(self, repo_name, name, color="ffffff", description=""):
        """Create a new label in GitHub"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{repo_name}/labels"
        data = {
            "name": name,
            "color": color,
            "description": description
        }
        return self._request('POST', url, data)

    def create_pull_request(self, repo_name, title, head, base, body="", draft=False):
        """Create a new pull request in GitHub"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{repo_name}/pulls"
        data = {
            "title": title,
            "head": head,
            "base": base,
            "body": body,
            "draft": draft
        }
        return self._request('POST', url, data)

    def create_release(self, repo_name, tag_name, name, body="", draft=False, prerelease=False):
        """Create a new release in GitHub"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{repo_name}/releases"
        data = {
            "tag_name": tag_name,
            "name": name,
            "body": body,
            "draft": draft,
            "prerelease": prerelease
        }
        return self._request('POST', url, data)

    def create_discussion(self, repo_name, title, body, category="General"):
        """Create a new discussion in GitHub"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{repo_name}/discussions"
        data = {
            "title": title,
            "body": body,
            "category": category
        }
        return self._request('POST', url, data)

    def create_wiki_page(self, repo_name, page_name, content):
        """Create a new wiki page in GitHub"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{repo_name}/wiki/pages/{page_name}"
        data = {
            "content": content
        }
        return self._request('PUT', url, data)

    def create_github_actions_workflow(self, repo_name, workflow_name, workflow_content):
        """Create a new GitHub Actions workflow"""
        url = f"{self.api_base}/repos/{self.repo_owner}/{repo_name}/contents/.github/workflows/{workflow_name}"
        data = {
            "message": f"Add {workflow_name} workflow",
            "content": workflow_content.encode('utf-8').hex()
        }
        return self._request('PUT', url, data)

    def generate_all_github_reports(self, repo_name, project_data):
        """Generate all possible GitHub reports and artifacts"""
        reports = {
            'repository_created': None,
            'project_board_created': None,
            'issues_created': [],
            'milestones_created': [],
            'labels_created': [],
            'pull_requests_created': [],
            'releases_created': [],
            'discussions_created': [],
            'wiki_pages_created': [],
            'workflows_created': []
        }

        # Create repository
        repo = self.create_repository(repo_name, project_data.get('description', ''))
        reports['repository_created'] = repo

        # Create project board
        project = self.create_project_board(repo_name, project_data.get('name', ''), project_data.get('description', ''))
        reports['project_board_created'] = project

        # Create milestones from project phases
        for phase in project_data.get('phases', []):
            milestone = self.create_milestone(repo_name, phase['name'], phase.get('description', ''))
            reports['milestones_created'].append(milestone)

        # Create labels from categories
        for category in project_data.get('categories', []):
            label = self.create_label(repo_name, category['name'], category.get('color', 'ffffff'))
            reports['labels_created'].append(label)

        # Create issues from tasks
        for task in project_data.get('tasks', []):
            issue = self.create_issue(
                repo_name, 
                task['title'], 
                task.get('description', ''), 
                task.get('labels', []),
                task.get('assignees', [])
            )
            reports['issues_created'].append(issue)

        # Create initial release
        release = self.create_release(repo_name, "v0.1.0", "Initial Release", "Initial project setup")
        reports['releases_created'].append(release)

        # Create welcome discussion
        discussion = self.create_discussion(
            repo_name, 
            "Welcome to the project", 
            "Welcome to our new project! Please read the documentation and get started."
        )
        reports['discussions_created'].append(discussion)

        # Create wiki pages
        wiki_content = f"# {project_data.get('name', 'Project')} Documentation\n\n## Overview\n{project_data.get('description', '')}"
        wiki = self.create_wiki_page(repo_name, "Home", wiki_content)
        reports['wiki_pages_created'].append(wiki)

        # Create GitHub Actions workflow
        workflow_content = self._generate_default_workflow()
        workflow = self.create_github_actions_workflow(repo_name, "ci.yml", workflow_content)
        reports['workflows_created'].append(workflow)

        return reports

    def _generate_default_workflow(self):
        """Generate default GitHub Actions workflow"""
        return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
"""

    def get_issues(self, state="open"):
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/issues"
        params = {"state": state}
        data = self._request('GET', url, params)
        if data is None:
            self.logger.error("Failed to retrieve issues.")
            return []
        return data

    def get_commits(self, per_page=30):
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/commits"
        params = {"per_page": per_page}
        data = self._request('GET', url, params)
        if data is None:
            self.logger.error("Failed to retrieve commits.")
            return []
        return data

    def get_pull_requests(self, state="open"):
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/pulls"
        params = {"state": state}
        data = self._request('GET', url, params)
        if data is None:
            self.logger.error("Failed to retrieve pull requests.")
            return []
        return data

    def get_project_progress(self):
        """Get comprehensive project progress from GitHub"""
        issues = self.get_issues()
        prs = self.get_pull_requests()
        commits = self.get_commits()
        
        return {
            "total_issues": len(issues),
            "open_issues": len([i for i in issues if i['state'] == 'open']),
            "closed_issues": len([i for i in issues if i['state'] == 'closed']),
            "total_prs": len(prs),
            "open_prs": len([p for p in prs if p['state'] == 'open']),
            "closed_prs": len([p for p in prs if p['state'] == 'closed']),
            "total_commits": len(commits),
            "last_commit": commits[0] if commits else None
        }

if __name__ == "__main__":
    # Example usage
    repo_owner = "your_org_or_username"
    repo_name = "ProjectManagement"
    github = GitHubIntegration(repo_owner, repo_name)
    
    # Example project data
    project_data = {
        "name": "New Project",
        "description": "A new project with GitHub integration",
        "phases": [
            {"name": "Planning", "description": "Project planning phase"},
            {"name": "Development", "description": "Development phase"},
            {"name": "Testing", "description": "Testing phase"}
        ],
        "categories": [
            {"name": "bug", "color": "d73a4a"},
            {"name": "feature", "color": "a2eeef"},
            {"name": "documentation", "color": "0075ca"}
        ],
        "tasks": [
            {"title": "Setup project structure", "description": "Initialize project structure", "labels": ["setup"]},
            {"title": "Create documentation", "description": "Create project documentation", "labels": ["documentation"]}
        ]
    }
    
    # Generate all reports
    reports = github.generate_all_github_reports("test-project", project_data)
    print(json.dumps(reports, indent=2, default=str))
