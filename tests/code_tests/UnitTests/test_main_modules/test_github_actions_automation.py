"""
Unit tests for github_actions_automation module
"""

import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock, mock_open
from autoprojectmanagement.main_modules.github_actions_automation import GitHubActionsAutomation


class TestGitHubActionsAutomation:
    """Test cases for GitHubActionsAutomation class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.automation = GitHubActionsAutomation()
        self.test_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_init(self):
        """Test initialization"""
        assert self.automation is not None
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    @patch('os.path.exists')
    def test_create_workflow_success(self, mock_exists, mock_makedirs, mock_file):
        """Test successful workflow creation"""
        mock_exists.return_value = False
        workflow_config = {
            'name': 'Test Workflow',
            'on': ['push', 'pull_request'],
            'jobs': {
                'test': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v2'},
                        {'name': 'Run tests', 'run': 'pytest'}
                    ]
                }
            }
        }
        
        result = self.automation.create_workflow('test.yml', workflow_config)
        assert result is True
        mock_makedirs.assert_called_once()
        mock_file.assert_called_once()
    
    def test_create_workflow_invalid_config(self):
        """Test workflow creation with invalid config"""
        result = self.automation.create_workflow('test.yml', None)
        assert result is False
    
    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_workflow_success(self, mock_remove, mock_exists):
        """Test successful workflow deletion"""
        mock_exists.return_value = True
        result = self.automation.delete_workflow('test.yml')
        assert result is True
        mock_remove.assert_called_once()
    
    @patch('os.path.exists')
    def test_delete_workflow_not_found(self, mock_exists):
        """Test workflow deletion when file doesn't exist"""
        mock_exists.return_value = False
        result = self.automation.delete_workflow('test.yml')
        assert result is False
