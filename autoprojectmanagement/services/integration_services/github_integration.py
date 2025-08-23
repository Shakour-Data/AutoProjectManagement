#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/services/github_integration.py
File: github_integration.py
Purpose: GitHub integration services
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: GitHub integration services within the AutoProjectManagement system
"""

import logging
from typing import Dict, Any, Optional, List, Union
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CURRENT_VERSION = "2.0.0"
PYTHON_MIN_VERSION = "3.8+"
CREATED_DATE = "2025-08-14"
MODIFIED_DATE = "2025-08-14"

# Module-level docstring
__doc__ = """
GitHub integration services within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import logging
import os
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import time

# Constants
GITHUB_API_BASE = "https://api.github.com"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
RATE_LIMIT_BUFFER = 100  # requests buffer before rate limit

# Configure logging
logger = logging.getLogger(__name__)


class GitHubIntegrationError(Exception):
    """Custom exception for GitHub integration errors."""
    pass


class GitHubIntegration:
    """
    Comprehensive GitHub API integration for project management operations.
    
    This class provides methods to interact with GitHub repositories, issues,
    pull requests, and project boards with proper error handling and rate limiting.
    
    Attributes:
        owner (str): Repository owner/organization name
        repo (str): Repository name
        token (str): GitHub personal access token
        api_url (str): Base API URL for the repository
        session (requests.Session): Configured session for API calls
    """
    
    def __init__(self, owner: str, repo: str, token: Optional[str] = None) -> None:
        """
        Initialize GitHub integration with repository details.
        
        Args:
            owner: Repository owner or organization name
            repo: Repository name
            token: GitHub personal access token (optional, can use GITHUB_TOKEN env var)
            
        Raises:
            ValueError: If owner or repo parameters are empty
            GitHubIntegrationError: If token is required but not provided
            
        Example:
            >>> github = GitHubIntegration("myorg", "myrepo", "ghp_xxx")
            >>> issues = github.get_issues()
        """
        if not owner or not owner.strip():
            raise ValueError("Repository owner cannot be empty")
        if not repo or not repo.strip():
            raise ValueError("Repository name cannot be empty")
            
        self.owner = owner.strip()
        self.repo = repo.strip()
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.api_url = f"{GITHUB_API_BASE}/repos/{self.owner}/{self.repo}"
        
        # Configure session with retry strategy
        self.session = requests.Session()
        self.session.headers.update(self._get_headers())
        
        logger.info(f"Initialized GitHub integration for {self.owner}/{self.repo}")
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Generate headers for GitHub API requests.
        
        Returns:
            Dictionary containing request headers including authorization
        """
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AutoProjectManagement/2.0.0"
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        Make authenticated request to GitHub API with retry logic.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint relative to base URL
            params: Query parameters
            data: Form data for POST/PUT requests
            json_data: JSON data for POST/PUT requests
            
        Returns:
            Response object from successful request
            
        Raises:
            GitHubIntegrationError: For API errors or rate limiting
            RequestException: For network-related errors
        """
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith("http") else endpoint
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    timeout=DEFAULT_TIMEOUT
                )
                
                # Handle rate limiting
                if response.status_code == 403 and "rate limit" in response.text.lower():
                    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                    wait_time = max(reset_time - int(time.time()), 60)
                    logger.warning(f"Rate limit hit, waiting {wait_time} seconds")
                    time.sleep(wait_time)
                    continue
                
                # Handle successful response
                if 200 <= response.status_code < 300:
                    return response
                
                # Handle specific error cases
                if response.status_code == 404:
                    raise GitHubIntegrationError(f"Resource not found: {url}")
                elif response.status_code == 401:
                    raise GitHubIntegrationError("Authentication failed - check token")
                elif response.status_code == 422:
                    error_msg = response.json().get("message", "Validation failed")
                    raise GitHubIntegrationError(f"Validation error: {error_msg}")
                
                # Generic error handling
                response.raise_for_status()
                
            except (Timeout, ConnectionError) as e:
                if attempt == MAX_RETRIES - 1:
                    raise GitHubIntegrationError(f"Network error after {MAX_RETRIES} attempts: {str(e)}")
                logger.warning(f"Network error on attempt {attempt + 1}, retrying...")
                time.sleep(RETRY_DELAY * (attempt + 1))
                
        raise GitHubIntegrationError("Max retries exceeded")
    
    def get_issues(
        self, 
        state: str = "open", 
        labels: Optional[List[str]] = None,
        assignee: Optional[str] = None,
        sort: str = "created",
        direction: str = "desc"
    ) -> List[Dict[str, Any]]:
        """
        Retrieve issues from the repository with filtering options.
        
        Args:
            state: Issue state (open, closed, all)
            labels: List of label names to filter by
            assignee: Username to filter assigned issues
            sort: Sort criteria (created, updated, comments)
            direction: Sort direction (asc, desc)
            
        Returns:
            List of issue dictionaries containing issue details
            
        Raises:
            GitHubIntegrationError: If API request fails
            
        Example:
            >>> github = GitHubIntegration("owner", "repo", "token")
            >>> open_issues = github.get_issues(state="open", labels=["bug"])
            >>> print(f"Found {len(open_issues)} open bugs")
        """
        params = {
            "state": state,
            "sort": sort,
            "direction": direction
        }
        
        if labels:
            params["labels"] = ",".join(labels)
        if assignee:
            params["assignee"] = assignee
            
        try:
            response = self._make_request("GET", "issues", params=params)
            issues = response.json()
            logger.info(f"Retrieved {len(issues)} issues with state={state}")
            return issues
            
        except Exception as e:
            logger.error(f"Failed to get issues: {str(e)}")
            raise GitHubIntegrationError(f"Failed to retrieve issues: {str(e)}")
    
    def create_issue(
        self,
        title: str,
        body: str = "",
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new issue in the repository.
        
        Args:
            title: Issue title
            body: Issue description/body
            labels: List of label names to apply
            assignees: List of usernames to assign
            
        Returns:
            Dictionary containing created issue details
            
        Raises:
            GitHubIntegrationError: If issue creation fails
            
        Example:
            >>> github = GitHubIntegration("owner", "repo", "token")
            >>> issue = github.create_issue(
            ...     "Bug in login flow",
            ...     "Users cannot login with special characters",
            ...     labels=["bug", "high-priority"]
            ... )
        """
        if not title or not title.strip():
            raise ValueError("Issue title cannot be empty")
            
        data = {
            "title": title.strip(),
            "body": body.strip()
        }
        
        if labels:
            data["labels"] = labels
        if assignees:
            data["assignees"] = assignees
            
        try:
            response = self._make_request("POST", "issues", json_data=data)
            issue = response.json()
            logger.info(f"Created issue #{issue['number']}: {title}")
            return issue
            
        except Exception as e:
            logger.error(f"Failed to create issue: {str(e)}")
            raise GitHubIntegrationError(f"Failed to create issue: {str(e)}")
    
    def update_issue(
        self,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing issue.
        
        Args:
            issue_number: Issue number to update
            title: New title (optional)
            body: New body (optional)
            state: New state (open or closed)
            labels: New list of labels (replaces existing)
            assignees: New list of assignees (replaces existing)
            
        Returns:
            Dictionary containing updated issue details
            
        Raises:
            GitHubIntegrationError: If update fails
            
        Example:
            >>> github.update_issue(123, state="closed", labels=["resolved"])
        """
        data = {}
        if title is not None:
            data["title"] = title.strip()
        if body is not None:
            data["body"] = body.strip()
        if state is not None:
            if state not in ["open", "closed"]:
                raise ValueError("State must be 'open' or 'closed'")
            data["state"] = state
        if labels is not None:
            data["labels"] = labels
        if assignees is not None:
            data["assignees"] = assignees
            
        try:
            response = self._make_request("PATCH", f"issues/{issue_number}", json_data=data)
            issue = response.json()
            logger.info(f"Updated issue #{issue_number}")
            return issue
            
        except Exception as e:
            logger.error(f"Failed to update issue #{issue_number}: {str(e)}")
            raise GitHubIntegrationError(f"Failed to update issue: {str(e)}")
    
    def get_pull_requests(
        self,
        state: str = "open",
        base: Optional[str] = None,
        head: Optional[str] = None,
        sort: str = "created",
        direction: str = "desc"
    ) -> List[Dict[str, Any]]:
        """
        Retrieve pull requests from the repository.
        
        Args:
            state: PR state (open, closed, all)
            base: Base branch name
            head: Head branch name (format: "user:branch")
            sort: Sort criteria (created, updated, popularity, long-running)
            direction: Sort direction (asc, desc)
            
        Returns:
            List of pull request dictionaries
            
        Raises:
            GitHubIntegrationError: If API request fails
        """
        params = {
            "state": state,
            "sort": sort,
            "direction": direction
        }
        
        if base:
            params["base"] = base
        if head:
            params["head"] = head
            
        try:
            response = self._make_request("GET", "pulls", params=params)
            prs = response.json()
            logger.info(f"Retrieved {len(prs)} pull requests with state={state}")
            return prs
            
        except Exception as e:
            logger.error(f"Failed to get pull requests: {str(e)}")
            raise GitHubIntegrationError(f"Failed to retrieve pull requests: {str(e)}")
    
    def create_pull_request(
        self,
        title: str,
        head: str,
        base: str = "main",
        body: str = "",
        draft: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new pull request.
        
        Args:
            title: PR title
            head: Head branch name
            base: Base branch name (default: main)
            body: PR description
            draft: Whether to create as draft PR
            
        Returns:
            Dictionary containing created PR details
            
        Raises:
            GitHubIntegrationError: If PR creation fails
        """
        if not title or not title.strip():
            raise ValueError("PR title cannot be empty")
        if not head or not head.strip():
            raise ValueError("Head branch cannot be empty")
            
        data = {
            "title": title.strip(),
            "head": head.strip(),
            "base": base.strip(),
            "body": body.strip(),
            "draft": draft
        }
        
        try:
            response = self._make_request("POST", "pulls", json_data=data)
            pr = response.json()
            logger.info(f"Created PR #{pr['number']}: {title}")
            return pr
            
        except Exception as e:
            logger.error(f"Failed to create pull request: {str(e)}")
            raise GitHubIntegrationError(f"Failed to create pull request: {str(e)}")
    
    def get_rate_limit(self) -> Dict[str, Any]:
        """
        Get current rate limit status for the authenticated user.
        
        Returns:
            Dictionary containing rate limit information
            
        Example:
            >>> limits = github.get_rate_limit()
            >>> print(f"Remaining: {limits['rate']['remaining']}")
        """
        try:
            response = self._make_request("GET", "https://api.github.com/rate_limit")
            return response.json()
            
        except Exception as e:
            logger.error(f"Failed to get rate limit: {str(e)}")
            raise GitHubIntegrationError(f"Failed to get rate limit: {str(e)}")
    
    def close(self) -> None:
        """Close the requests session to clean up resources."""
        if hasattr(self, 'session'):
            self.session.close()
            logger.info("GitHub integration session closed")
    
    def __enter__(self) -> 'GitHubIntegration':
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with cleanup."""
        self.close()


# Example usage and testing
if __name__ == "__main__":
    # Configure logging for standalone usage
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    try:
        with GitHubIntegration("owner", "repo") as github:
            # Get open issues
            issues = github.get_issues(state="open")
            print(f"Found {len(issues)} open issues")
            
            # Check rate limit
            limits = github.get_rate_limit()
            print(f"Rate limit remaining: {limits['rate']['remaining']}")
            
    except GitHubIntegrationError as e:
        logger.error(f"GitHub integration error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
