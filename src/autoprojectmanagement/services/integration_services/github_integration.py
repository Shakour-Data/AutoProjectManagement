"""
GitHub Integration for AutoProjectManagement
Purpose: Integrate with GitHub API for project management operations
Author: AutoProjectManagement Team
Version: 2.1.0
License: MIT
Description: Provides methods to interact with GitHub repositories, issues, pull requests, comments, and webhooks.
"""

import logging
import os
import requests
import time
import json
import hmac
import hashlib
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

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

    def sync_issue_status(self, issue_number: int, state: str) -> Dict[str, Any]:
        """
        Synchronize the status of an issue (open/closed).
        
        Args:
            issue_number: The GitHub issue number
            state: The desired state ('open' or 'closed')
        
        Returns:
            Dictionary containing updated issue details
        
        Raises:
            GitHubIntegrationError: If update fails
        """
        if state not in ['open', 'closed']:
            raise ValueError("State must be 'open' or 'closed'")
        
        data = {"state": state}
        try:
            response = self._make_request("PATCH", f"issues/{issue_number}", json_data=data)
            updated_issue = response.json()
            logger.info(f"Issue #{issue_number} status updated to {state}")
            return updated_issue
        except Exception as e:
            logger.error(f"Failed to update issue status: {str(e)}")
            raise GitHubIntegrationError(f"Failed to update issue status: {str(e)}")

    def get_issue_comments(self, issue_number: int) -> List[Dict[str, Any]]:
        """
        Retrieve comments for a specific issue.
        
        Args:
            issue_number: The GitHub issue number
        
        Returns:
            List of comment dictionaries
        
        Raises:
            GitHubIntegrationError: If retrieval fails
        """
        try:
            response = self._make_request("GET", f"issues/{issue_number}/comments")
            comments = response.json()
            logger.info(f"Retrieved {len(comments)} comments for issue #{issue_number}")
            return comments
        except Exception as e:
            logger.error(f"Failed to get comments: {str(e)}")
            raise GitHubIntegrationError(f"Failed to get comments: {str(e)}")

    def add_issue_comment(self, issue_number: int, comment_body: str) -> Dict[str, Any]:
        """
        Add a comment to a specific issue.
        
        Args:
            issue_number: The GitHub issue number
            comment_body: The comment text
        
        Returns:
            Dictionary containing created comment details
        
        Raises:
            GitHubIntegrationError: If comment creation fails
        """
        if not comment_body or not comment_body.strip():
            raise ValueError("Comment body cannot be empty")
        
        data = {"body": comment_body.strip()}
        try:
            response = self._make_request("POST", f"issues/{issue_number}/comments", json_data=data)
            comment = response.json()
            logger.info(f"Added comment to issue #{issue_number}")
            return comment
        except Exception as e:
            logger.error(f"Failed to add comment: {str(e)}")
            raise GitHubIntegrationError(f"Failed to add comment: {str(e)}")

    def create_webhook(self, url: str, events: List[str], secret: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a webhook for the repository.
        
        Args:
            url: The URL to receive webhook events
            events: List of events to subscribe to
            secret: Optional secret for webhook verification
        
        Returns:
            Dictionary containing created webhook details
        
        Raises:
            GitHubIntegrationError: If webhook creation fails
        """
        data = {
            "config": {
                "url": url,
                "content_type": "json"
            },
            "events": events
        }
        
        if secret:
            data["config"]["secret"] = secret
        
        try:
            response = self._make_request("POST", "hooks", json_data=data)
            webhook = response.json()
            logger.info(f"Created webhook for {len(events)} events")
            return webhook
        except Exception as e:
            logger.error(f"Failed to create webhook: {str(e)}")
            raise GitHubIntegrationError(f"Failed to create webhook: {str(e)}")

    def get_webhooks(self) -> List[Dict[str, Any]]:
        """
        Retrieve all webhooks for the repository.
        
        Returns:
            List of webhook dictionaries
        
        Raises:
            GitHubIntegrationError: If retrieval fails
        """
        try:
            response = self._make_request("GET", "hooks")
            webhooks = response.json()
            logger.info(f"Retrieved {len(webhooks)} webhooks")
            return webhooks
        except Exception as e:
            logger.error(f"Failed to get webhooks: {str(e)}")
            raise GitHubIntegrationError(f"Failed to get webhooks: {str(e)}")

    def delete_webhook(self, hook_id: int) -> bool:
        """
        Delete a webhook from the repository.
        
        Args:
            hook_id: The ID of the webhook to delete
        
        Returns:
            True if deletion was successful
        
        Raises:
            GitHubIntegrationError: If deletion fails
        """
        try:
            response = self._make_request("DELETE", f"hooks/{hook_id}")
            if response.status_code == 204:
                logger.info(f"Deleted webhook #{hook_id}")
                return True
            else:
                raise GitHubIntegrationError(f"Unexpected status code: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to delete webhook: {str(e)}")
            raise GitHubIntegrationError(f"Failed to delete webhook: {str(e)}")

    def verify_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """
        Verify GitHub webhook signature for security.
        
        Args:
            payload: The raw request payload
            signature: The X-Hub-Signature-256 header value
            secret: The webhook secret
        
        Returns:
            True if signature is valid, False otherwise
        """
        if not signature.startswith('sha256='):
            return False
        
        expected_signature = signature[7:]
        computed_signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, computed_signature)

    def handle_webhook_event(self, event_type: str, payload: Dict[str, Any], 
                           callback: Callable[[str, Dict[str, Any]], None]) -> None:
        """
        Process webhook events and trigger appropriate callbacks.
        
        Args:
            event_type: The GitHub event type (e.g., 'issues', 'issue_comment')
            payload: The webhook payload data
            callback: Function to call with event data
        
        Raises:
            GitHubIntegrationError: If event processing fails
        """
        try:
            if event_type == 'issues':
                action = payload.get('action')
                issue = payload.get('issue', {})
                logger.info(f"Received issue event: {action} for issue #{issue.get('number')}")
                
            elif event_type == 'issue_comment':
                action = payload.get('action')
                comment = payload.get('comment', {})
                issue = payload.get('issue', {})
                logger.info(f"Received comment event: {action} for issue #{issue.get('number')}")
            
            # Call the provided callback with event data
            callback(event_type, payload)
            
        except Exception as e:
            logger.error(f"Failed to process webhook event: {str(e)}")
            raise GitHubIntegrationError(f"Failed to process webhook event: {str(e)}")
    
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
