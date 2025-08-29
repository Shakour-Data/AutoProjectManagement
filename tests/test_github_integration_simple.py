"""
Simple test for GitHub Integration Service
Purpose: Test GitHub API integration functionality without circular imports
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
"""

import pytest
import time
import hmac
import hashlib
import requests
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to Python path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the module directly
from autoprojectmanagement.services.integration_services.github_integration import (
    GitHubIntegration, GitHubIntegrationError
)


class TestGitHubIntegrationSimple:
    """Test class for GitHubIntegration functionality"""

    @pytest.fixture
    def github_integration(self):
        """Fixture to create a GitHubIntegration instance for testing"""
        return GitHubIntegration("test-owner", "test-repo", "test-token")

    @pytest.fixture
    def mock_response(self):
        """Fixture to create a mock response"""
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"id": 123, "number": 1, "title": "Test Issue"}
        return mock_resp

    def test_initialization(self):
        """Test GitHubIntegration initialization"""
        github = GitHubIntegration("test-owner", "test-repo")
        assert github.owner == "test-owner"
        assert github.repo == "test-repo"
        assert github.api_url == "https://api.github.com/repos/test-owner/test-repo"

    def test_initialization_with_token(self):
        """Test GitHubIntegration initialization with token"""
        github = GitHubIntegration("test-owner", "test-repo", "test-token")
        assert github.token == "test-token"

    def test_initialization_empty_owner(self):
        """Test GitHubIntegration initialization with empty owner"""
        with pytest.raises(ValueError, match="Repository owner cannot be empty"):
            GitHubIntegration("", "test-repo")

    def test_initialization_empty_repo(self):
        """Test GitHubIntegration initialization with empty repo"""
        with pytest.raises(ValueError, match="Repository name cannot be empty"):
            GitHubIntegration("test-owner", "")

    @patch('autoprojectmanagement.services.integration_services.github_integration.requests.Session')
    def test_get_headers_with_token(self, mock_session):
        """Test _get_headers method with token"""
        github = GitHubIntegration("test-owner", "test-repo", "test-token")
        headers = github._get_headers()
        
        assert headers["Accept"] == "application/vnd.github.v3+json"
        assert headers["Authorization"] == "token test-token"
        assert headers["User-Agent"] == "AutoProjectManagement/2.0.0"

    @patch('autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_get_issues_success(self, mock_request, github_integration, mock_response):
        """Test successful get_issues call"""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "title": "Test Issue"}]
        
        issues = github_integration.get_issues(state="open")
        
        assert len(issues) == 1
        assert issues[0]["title"] == "Test Issue"
        mock_request.assert_called_once()

    @patch('autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_create_issue_success(self, mock_request, github_integration, mock_response):
        """Test successful create_issue call"""
        mock_request.return_value = mock_response
        
        issue = github_integration.create_issue("Test Issue", "Test body", ["bug"])
        
        assert issue["title"] == "Test Issue"
        mock_request.assert_called_once()

    @patch('autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_sync_issue_status_success(self, mock_request, github_integration, mock_response):
        """Test successful sync_issue_status call"""
        mock_request.return_value = mock_response
        
        updated_issue = github_integration.sync_issue_status(1, "closed")
        
        assert updated_issue["title"] == "Test Issue"
        mock_request.assert_called_once()

    @patch('autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_get_issue_comments_success(self, mock_request, github_integration, mock_response):
        """Test successful get_issue_comments call"""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "body": "Test comment"}]
        
        comments = github_integration.get_issue_comments(1)
        
        assert len(comments) == 1
        assert comments[0]["body"] == "Test comment"
        mock_request.assert_called_once()

    @patch('autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_add_issue_comment_success(self, mock_request, github_integration, mock_response):
        """Test successful add_issue_comment call"""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "body": "Test comment"}
        
        comment = github_integration.add_issue_comment(1, "Test comment")
        
        assert comment["body"] == "Test comment"
        mock_request.assert_called_once()

    def test_verify_webhook_signature_valid(self, github_integration):
        """Test verify_webhook_signature with valid signature"""
        payload = b'{"test": "data"}'
        secret = "test-secret"
        
        # Generate a valid signature
        computed_signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        signature = f"sha256={computed_signature}"
        
        result = github_integration.verify_webhook_signature(payload, signature, secret)
        assert result is True

    def test_verify_webhook_signature_invalid(self, github_integration):
        """Test verify_webhook_signature with invalid signature"""
        payload = b'{"test": "data"}'
        secret = "test-secret"
        invalid_signature = "sha256=invalid_signature_hash"
        
        result = github_integration.verify_webhook_signature(payload, invalid_signature, secret)
        assert result is False

    def test_handle_webhook_event_issues(self, github_integration):
        """Test handle_webhook_event for issues"""
        mock_callback = Mock()
        event_type = "issues"
        payload = {
            "action": "opened",
            "issue": {"number": 1, "title": "Test Issue"}
        }
        
        github_integration.handle_webhook_event(event_type, payload, mock_callback)
        
        mock_callback.assert_called_once_with(event_type, payload)

    def test_context_manager(self):
        """Test GitHubIntegration context manager functionality"""
        with patch('autoprojectmanagement.services.integration_services.github_integration.requests.Session') as mock_session:
            mock_session_instance = Mock()
            mock_session.return_value = mock_session_instance
            
            with GitHubIntegration("test-owner", "test-repo") as github:
                assert github.owner == "test-owner"
                assert github.repo == "test-repo"
            
            # Verify session was closed
            mock_session_instance.close.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
