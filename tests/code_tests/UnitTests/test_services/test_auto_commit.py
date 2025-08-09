"""
Test suite for AutoCommit service
"""
import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock, mock_open
import subprocess
import json
from datetime import datetime

from autoprojectmanagement.services.auto_commit import (
    format_commit_message,
    AutoCommit
)


class TestFormatCommitMessage:
    """Test cases for format_commit_message function"""
    
    def test_format_commit_message_valid_input(self):
        """Test formatting valid commit messages"""
        assert format_commit_message("Fix bug in module") == "Fix bug in module"
        assert format_commit_message("  Fix bug  ") == "Fix bug"
        assert format_commit_message("Fix\tbug\nin module") == "Fix bug in module"
    
    def test_format_commit_message_empty_string(self):
        """Test handling empty strings"""
        assert format_commit_message("") == ""
    
    def test_format_commit_message_none_raises_error(self):
        """Test that None raises TypeError"""
        with pytest.raises(TypeError, match="Commit message cannot be None"):
            format_commit_message(None)
    
    def test_format_commit_message_non_string_raises_error(self):
        """Test that non-string input raises TypeError"""
        with pytest.raises(TypeError, match="Commit message must be a string"):
            format_commit_message(123)
    
    def test_format_commit_message_length_limit(self):
        """Test message length limiting"""
        long_message = "a" * 300
        result = format_commit_message(long_message)
        assert len(result) <= 255
        assert result.startswith("a" * 255)
    
    def test_format_commit_message_unicode_support(self):
        """Test Unicode character support"""
        assert format_commit_message("Fix bug in 模块") == "Fix bug in 模块"
        assert format_commit_message("Fix bug 😊") == "Fix bug 😊"
    
    def test_format_commit_message_special_characters(self):
        """Test handling special characters"""
        assert format_commit_message("Fix issue #123! @user") == "Fix issue #123! @user"
        assert format_commit_message("Fix bug <script>alert('xss')</script>") == "Fix bug <script>alert('xss')</script>"


class TestAutoCommit:
    """Test cases for AutoCommit class"""
    
    @pytest.fixture
    def temp_git_repo(self):
        """Create a temporary git repository for testing"""
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        
        # Initialize git repo
        subprocess.run(['git', 'init'], cwd=temp_dir, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=temp_dir, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=temp_dir, check=True)
        
        # Create initial commit
        test_file = os.path.join(temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('initial content')
        subprocess.run(['git', 'add', 'test.txt'], cwd=temp_dir, check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=temp_dir, check=True)
        
        yield temp_dir
        
        # Cleanup
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def auto_commit(self):
        """Create AutoCommit instance"""
        return AutoCommit()
    
    def test_auto_commit_initialization(self, auto_commit):
        """Test AutoCommit class initialization"""
        assert auto_commit is not None
        assert hasattr(auto_commit, 'bm')
    
    def test_run_git_command_success(self, temp_git_repo, auto_commit):
        """Test successful git command execution"""
        os.chdir(temp_git_repo)
        success, output = auto_commit.run_git_command(['status', '--porcelain'])
        assert success is True
        assert isinstance(output, str)
    
    def test_run_git_command_failure(self, auto_commit):
        """Test git command failure handling"""
        success, output = auto_commit.run_git_command(['invalid-command'])
        assert success is False
        assert isinstance(output, str)
    
    def test_get_git_changes_empty_repo(self, temp_git_repo, auto_commit):
        """Test getting changes from empty repository"""
        os.chdir(temp_git_repo)
        changes = auto_commit.get_git_changes()
        assert isinstance(changes, list)
    
    def test_get_git_changes_with_changes(self, temp_git_repo, auto_commit):
        """Test getting changes with modified files"""
        os.chdir(temp_git_repo)
        
        # Create a new file
        new_file = os.path.join(temp_git_repo, 'new_file.txt')
        with open(new_file, 'w') as f:
            f.write('new content')
        
        changes = auto_commit.get_git_changes()
        assert len(changes) > 0
        assert any('new_file.txt' in change for change in changes)
    
    def test_group_related_files(self, auto_commit):
        """Test file grouping functionality"""
        changes = [
            'M src/main.py',
            'M src/utils.py',
            'A tests/test_main.py',
            '?? docs/README.md'
        ]
        
        groups = auto_commit.group_related_files(changes)
        assert 'src' in groups
        assert 'tests' in groups
        assert 'docs' in groups
        
        # Verify file categorization
        src_files = groups['src']
        assert len(src_files) == 2
        assert any('main.py' in str(file_info) for file_info in src_files)
    
    def test_categorize_files(self, auto_commit):
        """Test file categorization"""
        files = [
            ('A', 'new_file.py'),
            ('M', 'modified_file.py'),
            ('D', 'deleted_file.py'),
            ('??', 'untracked_file.py')
        ]
        
        categories = auto_commit.categorize_files(files)
        assert 'Added' in categories
        assert 'Modified' in categories
        assert 'Deleted' in categories
        assert 'Untracked' in categories
        
        assert 'new_file.py' in categories['Added']
        assert 'modified_file.py' in categories['Modified']
        assert 'deleted_file.py' in categories['Deleted']
        assert 'untracked_file.py' in categories['Untracked']
    
    def test_generate_commit_message(self, auto_commit):
        """Test commit message generation"""
        message = auto_commit.generate_commit_message(
            'src', 'Modified', ['main.py', 'utils.py']
        )
        
        assert isinstance(message, str)
        assert 'feat' in message or 'fix' in message
        assert 'src' in message
        assert 'Modified files updated' in message
    
    def test_load_linked_wbs_resources_file_not_found(self, auto_commit):
        """Test loading WBS resources when file doesn't exist"""
        with patch('os.path.exists', return_value=False):
            result = auto_commit.load_linked_wbs_resources('nonexistent.json')
            assert result == []
    
    def test_load_linked_wbs_resources_success(self, auto_commit):
        """Test successful loading of WBS resources"""
        mock_data = [{"id": "task1", "name": "Test Task"}]
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
            with patch('os.path.exists', return_value=True):
                result = auto_commit.load_linked_wbs_resources()
                assert result == mock_data
    
    def test_map_group_to_workflow_stage(self, auto_commit):
        """Test workflow stage mapping"""
        assert auto_commit.map_group_to_workflow_stage('requirements') == 'Requirements Gathering'
        assert auto_commit.map_group_to_workflow_stage('design') == 'Design'
        assert auto_commit.map_group_to_workflow_stage('unknown') == 'Implementation'
    
    def test_calculate_progress_change(self, auto_commit):
        """Test progress change calculation"""
        progress = auto_commit.calculate_progress_change('Implementation', 10)
        assert 0 <= progress <= 0.05
    
    def test_calculate_importance(self, auto_commit):
        """Test importance calculation"""
        importance = auto_commit.calculate_importance(
            'task1', 'Implementation', ['dep1', 'dep2'], 0.5, 2
        )
        assert 0 <= importance <= 1
    
    def test_calculate_urgency(self, auto_commit):
        """Test urgency calculation"""
        from datetime import datetime, timedelta
        
        deadline = datetime.now() + timedelta(days=5)
        urgency = auto_commit.calculate_urgency(
            deadline, datetime.now(), 1, 0.3
        )
        assert 0 <= urgency <= 1
    
    @patch('subprocess.run')
    def test_backup_method(self, mock_run, auto_commit):
        """Test backup functionality"""
        mock_run.return_value = MagicMock(returncode=0)
        
        with patch.object(auto_commit.bm, 'create_backup', return_value='/tmp/backup'):
            auto_commit.backup()
    
    def test_write_commit_progress_to_json(self, auto_commit):
        """Test writing commit progress to JSON"""
        with patch.object(auto_commit, 'collect_commit_progress', return_value={}):
            with patch('builtins.open', mock_open()):
                auto_commit.write_commit_progress_to_json()
