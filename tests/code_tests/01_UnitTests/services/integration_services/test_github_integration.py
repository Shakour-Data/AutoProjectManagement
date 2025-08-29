"""
Unit tests for GitHub Integration Service
Purpose: Test GitHub API integration functionality
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
from src.autoprojectmanagement.services.integration_services.github_integration import (
    GitHubIntegration, GitHubIntegrationError
)


class TestGitHubIntegration:
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

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session')
    def test_get_headers_with_token(self, mock_session):
        """Test _get_headers method with token"""
        github = GitHubIntegration("test-owner", "test-repo", "test-token")
        headers = github._get_headers()
        
        assert headers["Accept"] == "application/vnd.github.v3+json"
        assert headers["Authorization"] == "token test-token"
        assert headers["User-Agent"] == "AutoProjectManagement/2.0.0"

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session')
    def test_get_headers_without_token(self, mock_session):
        """Test _get_headers method without token"""
        github = GitHubIntegration("test-owner", "test-repo")
        headers = github._get_headers()
        
        assert headers["Accept"] == "application/vnd.github.v3+json"
        assert "Authorization" not in headers
        assert headers["User-Agent"] == "AutoProjectManagement/2.0.0"

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_get_issues_success(self, mock_request, github_integration, mock_response):
        """Test successful get_issues call"""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "title": "Test Issue"}]
        
        issues = github_integration.get_issues(state="open")
        
        assert len(issues) == 1
        assert issues[0]["title"] == "Test Issue"
        mock_request.assert_called_once()

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_get_issues_with_labels(self, mock_request, github_integration, mock_response):
        """Test get_issues with labels filter"""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "title": "Test Issue"}]
        
        issues = github_integration.get_issues(state="open", labels=["bug", "enhancement"])
        
        assert len(issues) == 1
        mock_request.assert_called_once()

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_create_issue_success(self, mock_request, github_integration, mock_response):
        """Test successful create_issue call"""
        mock_request.return_value = mock_response
        
        issue = github_integration.create_issue("Test Issue", "Test body", ["bug"])
        
        assert issue["title"] == "Test Issue"
        mock_request.assert_called_once()

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_create_issue_empty_title(self, mock_request, github_integration):
        """Test create_issue with empty title"""
        with pytest.raises(ValueError, match="Issue title cannot be empty"):
            github_integration.create_issue("", "Test body")

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_sync_issue_status_success(self, mock_request, github_integration, mock_response):
        """Test successful sync_issue_status call"""
        mock_request.return_value = mock_response
        
        updated_issue = github_integration.sync_issue_status(1, "closed")
        
        assert updated_issue["title"] == "Test Issue"
        mock_request.assert_called_once()

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_sync_issue_status_invalid_state(self, mock_request, github_integration):
        """Test sync_issue_status with invalid state"""
        with pytest.raises(ValueError, match="State must be 'open' or 'closed'"):
            github_integration.sync_issue_status(1, "invalid")

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_get_issue_comments_success(self, mock_request, github_integration, mock_response):
        """Test successful get_issue_comments call"""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "body": "Test comment"}]
        
        comments = github_integration.get_issue_comments(1)
        
        assert len(comments) == 1
        assert comments[0]["body"] == "Test comment"
        mock_request.assert_called_once()

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_add_issue_comment_success(self, mock_request, github_integration, mock_response):
        """Test successful add_issue_comment call"""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "body": "Test comment"}
        
        comment = github_integration.add_issue_comment(1, "Test comment")
        
        assert comment["body"] == "Test comment"
        mock_request.assert_called_once()

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_add_issue_comment_empty_body(self, mock_request, github_integration):
        """Test add_issue_comment with empty body"""
        with pytest.raises(ValueError, match="Comment body cannot be empty"):
            github_integration.add_issue_comment(1, "")

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_create_webhook_success(self, mock_request, github_integration, mock_response):
        """Test successful create_webhook call"""
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"id": 1, "url": "https://example.com/webhook"}
        
        webhook = github_integration.create_webhook(
            "https://example.com/webhook", 
            ["issues", "issue_comment"],
            "test-secret"
        )
        
        assert webhook["url"] == "https://example.com/webhook"
        mock_request.assert_called_once()

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_get_webhooks_success(self, mock_request, github_integration, mock_response):
        """Test successful get_webhooks call"""
        mock_request.return_value = mock_response
        mock_response.json.return_value = [{"id": 1, "url": "https://example.com/webhook"}]
        
        webhooks = github_integration.get_webhooks()
        
        assert len(webhooks) == 1
        assert webhooks[0]["url"] == "https://example.com/webhook"
        mock_request.assert_called_once()

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_delete_webhook_success(self, mock_request, github_integration, mock_response):
        """Test successful delete_webhook call"""
        mock_request.return_value = mock_response
        mock_response.status_code = 204
        
        result = github_integration.delete_webhook(1)
        
        assert result is True
        mock_request.assert_called_once()

    def test_verify_webhook_signature_valid(self):
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
        
        result = GitHubIntegration.verify_webhook_signature(payload, signature, secret)
        assert result is True

    def test_verify_webhook_signature_invalid(self):
        """Test verify_webhook_signature with invalid signature"""
        payload = b'{"test": "data"}'
        secret = "test-secret"
        invalid_signature = "sha256=invalid_signature_hash"
        
        result = GitHubIntegration.verify_webhook_signature(payload, invalid_signature, secret)
        assert result is False

    def test_verify_webhook_signature_malformed(self):
        """Test verify_webhook_signature with malformed signature"""
        payload = b'{"test": "data"}'
        secret = "test-secret"
        malformed_signature = "invalid_format"
        
        result = GitHubIntegration.verify_webhook_signature(payload, malformed_signature, secret)
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

    def test_handle_webhook_event_issue_comment(self, github_integration):
        """Test handle_webhook_event for issue_comment"""
        mock_callback = Mock()
        event_type = "issue_comment"
        payload = {
            "action": "created",
            "comment": {"id": 1, "body": "Test comment"},
            "issue": {"number": 1, "title": "Test Issue"}
        }
        
        github_integration.handle_webhook_event(event_type, payload, mock_callback)
        
        mock_callback.assert_called_once_with(event_type, payload)

    def test_handle_webhook_event_unknown_type(self, github_integration):
        """Test handle_webhook_event for unknown event type"""
        mock_callback = Mock()
        event_type = "unknown_event"
        payload = {"test": "data"}
        
        github_integration.handle_webhook_event(event_type, payload, mock_callback)
        
        mock_callback.assert_called_once_with(event_type, payload)

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_make_request_rate_limit(self, mock_request, github_integration):
        """Test _make_request with rate limiting"""
        # First response: rate limit error
        rate_limit_response = Mock()
        rate_limit_response.status_code = 403
        rate_limit_response.text = "API rate limit exceeded"
        rate_limit_response.headers = {"X-RateLimit-Reset": str(int(time.time()) + 60)}
        
        # Second response: success
        success_response = Mock()
        success_response.status_code = 200
        success_response.json.return_value = {"success": True}
        
        mock_request.side_effect = [rate_limit_response, success_response]
        
        response = github_integration._make_request("GET", "test")
        
        assert response.status_code == 200
        assert mock_request.call_count == 2

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_make_request_network_error_retry(self, mock_request, github_integration):
        """Test _make_request with network error and retry"""
        # First two attempts: network errors
        mock_request.side_effect = [
            requests.exceptions.ConnectionError("Network error"),
            requests.exceptions.ConnectionError("Network error"),
            Mock(status_code=200, json=lambda: {"success": True})
        ]
        
        response = github_integration._make_request("GET", "test")
        
        assert response.status_code == 200
        assert mock_request.call_count == 3

    @patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session.request')
    def test_make_request_max_retries_exceeded(self, mock_request, github_integration):
        """Test _make_request with max retries exceeded"""
        mock_request.side_effect = requests.exceptions.ConnectionError("Network error")
        
        with pytest.raises(GitHubIntegrationError, match="Max retries exceeded"):
            github_integration._make_request("GET", "test")
        
        assert mock_request.call_count == 3

    def test_context_manager(self):
        """Test GitHubIntegration context manager functionality"""
        with patch('src.autoprojectmanagement.services.integration_services.github_integration.requests.Session') as mock_session:
            mock_session_instance = Mock()
            mock_session.return_value = mock_session_instance
            
            with GitHubIntegration("test-owner", "test-repo") as github:
                assert github.owner == "test-owner"
                assert github.repo == "test-repo"
            
            # Verify session was closed
            mock_session_instance.close.assert_called_once()
