#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from unittest.mock import patch, MagicMock
from autoprojectmanagement.services.integration_services.github_integration import GitHubIntegration
from autoprojectmanagement.services.audit_service import AuditActionType, AuditResourceType, AuditSeverity, AuditStatus

class TestGitHubIntegrationAudit(unittest.TestCase):
    
    def setUp(self):
        self.github = GitHubIntegration("test-owner", "test-repo", "test-token")
    
    @patch("autoprojectmanagement.services.integration_services.github_integration.audit_service")
    @patch("autoprojectmanagement.services.integration_services.github_integration.requests.Session.request")
    def test_get_issues_audit(self, mock_request, mock_audit_service):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = [{"id": 1, "title": "Issue 1"}]

        self.github.get_issues(state="open", labels=["bug"])

        self.assertGreaterEqual(mock_audit_service.log_event.call_count, 1)
        call_args = mock_audit_service.log_event.call_args_list[0][1]
        self.assertEqual(call_args["action"], AuditActionType.READ)
        self.assertEqual(call_args["resource_type"], AuditResourceType.ISSUE)
        self.assertIn("state", call_args["details"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
