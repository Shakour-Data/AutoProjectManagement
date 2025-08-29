import pytest
from unittest.mock import patch, MagicMock
from autoprojectmanagement.services.integration_services.github_integration import GitHubIntegration, GitHubIntegrationError
from autoprojectmanagement.services.audit_service import AuditActionType, AuditResourceType, AuditSeverity, AuditStatus

@pytest.fixture
def github():
    return GitHubIntegration("test-owner", "test-repo", "test-token")

@patch("autoprojectmanagement.services.integration_services.github_integration.audit_service")
@patch("autoprojectmanagement.services.integration_services.github_integration.requests.Session.request")
def test_get_issues_audit(mock_request, mock_audit_service, github):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = [{"id": 1, "title": "Issue 1"}]

    github.get_issues(state="open", labels=["bug"])

    assert mock_audit_service.log_event.call_count >= 1
    call_args = mock_audit_service.log_event.call_args_list[0][1]
    assert call_args["action"] == AuditActionType.READ
    assert call_args["resource_type"] == AuditResourceType.ISSUE
    assert "state" in call_args["details"]

@patch("autoprojectmanagement.services.integration_services.github_integration.audit_service")
@patch("autoprojectmanagement.services.integration_services.github_integration.requests.Session.request")
def test_create_issue_audit(mock_request, mock_audit_service, github):
    mock_request.return_value.status_code = 201
    mock_request.return_value.json.return_value = {"number": 123, "title": "New Issue"}

    github.create_issue("New Issue", "Body", labels=["enhancement"])

    assert mock_audit_service.log_event.call_count >= 1
    call_args = mock_audit_service.log_event.call_args_list[0][1]
    assert call_args["action"] == AuditActionType.CREATE
    assert call_args["resource_type"] == AuditResourceType.ISSUE
    assert "title" in call_args["details"]

@patch("autoprojectmanagement.services.integration_services.github_integration.audit_service")
@patch("autoprojectmanagement.services.integration_services.github_integration.requests.Session.request")
def test_sync_issue_status_audit(mock_request, mock_audit_service, github):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {"number": 1, "state": "closed"}

    github.sync_issue_status(1, "closed")

    assert mock_audit_service.log_event.call_count >= 1
    call_args = mock_audit_service.log_event.call_args_list[0][1]
    assert call_args["action"] == AuditActionType.UPDATE
    assert call_args["resource_type"] == AuditResourceType.ISSUE
    assert call_args["description"].startswith("Updating issue")

@patch("autoprojectmanagement.services.integration_services.github_integration.audit_service")
@patch("autoprojectmanagement.services.integration_services.github_integration.requests.Session.request")
def test_get_issue_comments_audit(mock_request, mock_audit_service, github):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = [{"id": 1, "body": "Comment"}]

    github.get_issue_comments(1)

    assert mock_audit_service.log_event.call_count >= 1
    call_args = mock_audit_service.log_event.call_args_list[0][1]
    assert call_args["action"] == AuditActionType.READ
    assert call_args["resource_type"] == AuditResourceType.COMMENT

@patch("autoprojectmanagement.services.integration_services.github_integration.audit_service")
@patch("autoprojectmanagement.services.integration_services.github_integration.requests.Session.request")
def test_add_issue_comment_audit(mock_request, mock_audit_service, github):
    mock_request.return_value.status_code = 201
    mock_request.return_value.json.return_value = {"id": 1, "body": "New Comment"}

    github.add_issue_comment(1, "New Comment")

    assert mock_audit_service.log_event.call_count >= 1
    call_args = mock_audit_service.log_event.call_args_list[0][1]
    assert call_args["action"] == AuditActionType.CREATE
    assert call_args["resource_type"] == AuditResourceType.COMMENT

@patch("autoprojectmanagement.services.integration_services.github_integration.audit_service")
@patch("autoprojectmanagement.services.integration_services.github_integration.requests.Session.request")
def test_create_webhook_audit(mock_request, mock_audit_service, github):
    mock_request.return_value.status_code = 201
    mock_request.return_value.json.return_value = {"id": 1}

    github.create_webhook("http://example.com/webhook", ["issues"])

    assert mock_audit_service.log_event.call_count >= 1
    call_args = mock_audit_service.log_event.call_args_list[0][1]
    assert call_args["action"] == AuditActionType.CREATE
    assert call_args["resource_type"] == AuditResourceType.WEBHOOK

@patch("autoprojectmanagement.services.integration_services.github_integration.audit_service")
@patch("autoprojectmanagement.services.integration_services.github_integration.requests.Session.request")
def test_get_webhooks_audit(mock_request, mock_audit_service, github):
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = [{"id": 1}]

    github.get_webhooks()

    assert mock_audit_service.log_event.call_count >= 1
    call_args = mock_audit_service.log_event.call_args_list[0][1]
    assert call_args["action"] == AuditActionType.READ
    assert call_args["resource_type"] == AuditResourceType.WEBHOOK

@patch("autoprojectmanagement.services.integration_services.github_integration.audit_service")
@patch("autoprojectmanagement.services.integration_services.github_integration.requests.Session.request")
def test_delete_webhook_audit(mock_request, mock_audit_service, github):
    mock_request.return_value.status_code = 204

    github.delete_webhook(1)

    assert mock_audit_service.log_event.call_count >= 1
    call_args = mock_audit_service.log_event.call_args_list[0][1]
    assert call_args["action"] == AuditActionType.DELETE
    assert call_args["resource_type"] == AuditResourceType.WEBHOOK

@patch("autoprojectmanagement.services.integration_services.github_integration.audit_service")
def test_handle_webhook_event_audit(mock_audit_service, github):
    mock_callback = MagicMock()
    event_type = "issues"
    payload = {"action": "opened", "issue": {"number": 1, "title": "Test"}}

    github.handle_webhook_event(event_type, payload, mock_callback)

    assert mock_audit_service.log_event.call_count >= 2  # start and success logs
    first_call = mock_audit_service.log_event.call_args_list[0][1]
    second_call = mock_audit_service.log_event.call_args_list[1][1]
    assert first_call["action"] == AuditActionType.PROCESS
    assert second_call["status"] == AuditStatus.SUCCESS
