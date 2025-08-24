"""
GitHub Integration for AutoProjectManagement
Purpose: Integrate with GitHub API for project management operations
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Provides methods to interact with GitHub repositories, issues, pull requests, and project boards.
"""

import logging
import os
import requests
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"

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
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None,
                      data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> requests.Response:
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
        
        for attempt in range(3):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    timeout=30
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
                
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                if attempt == 2:
                    raise GitHubIntegrationError(f"Network error after 3 attempts: {str(e)}")
                logger.warning(f"Network error on attempt {attempt + 1}, retrying...")
                time.sleep(1)
                
        raise GitHubIntegrationError("Max retries exceeded")
    
    def get_issues(self, state: str = "open", labels: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve issues from the repository with filtering options.
        
        Args:
            state: Issue state (open, closed, all)
            labels: List of label names to filter by
            
        Returns:
            List of issue dictionaries containing issue details
            
        Raises:
            GitHubIntegrationError: If API request fails
        """
        params = {
            "state": state,
            "labels": ",".join(labels) if labels else None
        }
        
        try:
            response = self._make_request("GET", "issues", params=params)
            issues = response.json()
            logger.info(f"Retrieved {len(issues)} issues with state={state}")
            return issues
            
        except Exception as e:
            logger.error(f"Failed to get issues: {str(e)}")
            raise GitHubIntegrationError(f"Failed to retrieve issues: {str(e)}")
    
    def create_issue(self, title: str, body: str = "", labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a new issue in the repository.
        
        Args:
            title: Issue title
            body: Issue description/body
            labels: List of label names to apply
            
        Returns:
            Dictionary containing created issue details
            
        Raises:
            GitHubIntegrationError: If issue creation fails
        """
        if not title or not title.strip():
            raise ValueError("Issue title cannot be empty")
            
        data = {
            "title": title.strip(),
            "body": body.strip()
        }
        
        if labels:
            data["labels"] = labels
            
        try:
            response = self._make_request("POST", "issues", json_data=data)
            issue = response.json()
            logger.info(f"Created issue #{issue['number']}: {title}")
            return issue
            
        except Exception as e:
            logger.error(f"Failed to create issue: {str(e)}")
            raise GitHubIntegrationError(f"Failed to create issue: {str(e)}")
    
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
            
            # Create a new issue
            new_issue = github.create_issue("Test Issue", "This is a test issue.")
            print(f"Created issue: {new_issue['html_url']}")
            
    except GitHubIntegrationError as e:
        logger.error(f"GitHub integration error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
