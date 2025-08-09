"""
Test suite for BackupManager service
"""
import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock, mock_open
import json
from datetime import datetime

from autoprojectmanagement.services.backup_manager import BackupManager


class TestBackupManager:
    """Test cases for BackupManager class"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def backup_manager(self):
        """Create BackupManager instance"""
        return BackupManager()
    
    def test_backup_manager_initialization(self, backup_manager):
        """Test BackupManager initialization"""
        assert backup_manager is not None
        assert hasattr(backup_manager, 'backup_dir')
    
    def test_create_backup_success(self, backup_manager, temp_dir):
        """Test successful backup creation"""
        # Create test files
        test_file = os.path.join(temp_dir, 'test.json')
        with open(test_file, 'w') as f:
            json.dump({'test': 'data'}, f)
        
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.create_backup(source_dir=temp_dir)
            assert result is not None
            assert os.path.exists(result)
    
    def test_create_backup_with_custom_path(self, backup_manager, temp_dir):
        """Test backup creation with custom path"""
        custom_backup_dir = os.path.join(temp_dir, 'custom_backups')
        
        with patch.object(backup_manager, 'backup_dir', custom_backup_dir):
            result = backup_manager.create_backup()
            assert result is not None
            assert custom_backup_dir in result
    
    def test_restore_backup_success(self, backup_manager, temp_dir):
        """Test successful backup restoration"""
        # Create backup
        backup_name = 'test_backup'
        backup_path = os.path.join(temp_dir, backup_name)
        os.makedirs(backup_path)
        
        # Create test file in backup
        test_file = os.path.join(backup_path, 'test.json')
        with open(test_file, 'w') as f:
            json.dump({'restored': 'data'}, f)
        
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.restore_backup(backup_name)
            assert result is True
    
    def test_restore_backup_nonexistent(self, backup_manager, temp_dir):
        """Test restoring non-existent backup"""
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.restore_backup('nonexistent_backup')
            assert result is False
    
    def test_list_backups_empty(self, backup_manager, temp_dir):
        """Test listing backups when none exist"""
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            backups = backup_manager.list_backups()
            assert isinstance(backups, list)
            assert len(backups) == 0
    
    def test_list_backups_with_files(self, backup_manager, temp_dir):
        """Test listing existing backups"""
        # Create test backups
        backup1 = os.path.join(temp_dir, 'backup_20240101_120000')
        backup2 = os.path.join(temp_dir, 'backup_20240102_130000')
        os.makedirs(backup1)
        os.makedirs(backup2)
        
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            backups = backup_manager.list_backups()
            assert len(backups) == 2
            assert 'backup_20240101_120000' in backups
            assert 'backup_20240102_130000' in backups
    
    def test_delete_backup_success(self, backup_manager, temp_dir):
        """Test successful backup deletion"""
        backup_name = 'test_backup'
        backup_path = os.path.join(temp_dir, backup_name)
        os.makedirs(backup_path)
        
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.delete_backup(backup_name)
            assert result is True
            assert not os.path.exists(backup_path)
    
    def test_delete_backup_nonexistent(self, backup_manager, temp_dir):
        """Test deleting non-existent backup"""
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.delete_backup('nonexistent_backup')
            assert result is False
    
    def test_check_backup_integrity_valid(self, backup_manager, temp_dir):
        """Test checking integrity of valid backup"""
        backup_name = 'test_backup'
        backup_path = os.path.join(temp_dir, backup_name)
        os.makedirs(backup_path)
        
        # Create valid backup files
        manifest_file = os.path.join(backup_path, 'manifest.json')
        with open(manifest_file, 'w') as f:
            json.dump({'files': [], 'timestamp': str(datetime.now())}, f)
        
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.check_backup_integrity(backup_name)
            assert result is True
    
    def test_check_backup_integrity_invalid(self, backup_manager, temp_dir):
        """Test checking integrity of invalid backup"""
        backup_name = 'invalid_backup'
        backup_path = os.path.join(temp_dir, backup_name)
        os.makedirs(backup_path)
        
        # Create invalid backup (missing manifest)
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.check_backup_integrity(backup_name)
            assert result is False
    
    def test_backup_with_unicode_paths(self, backup_manager, temp_dir):
        """Test backup with Unicode characters in paths"""
        unicode_dir = os.path.join(temp_dir, 'پوشه_تست')
        os.makedirs(unicode_dir)
        
        test_file = os.path.join(unicode_dir, 'فایل_تست.json')
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump({'test': 'داده'}, f, ensure_ascii=False)
        
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.create_backup(source_dir=unicode_dir)
            assert result is not None
    
    def test_backup_with_special_characters(self, backup_manager, temp_dir):
        """Test backup with special characters in paths"""
        special_dir = os.path.join(temp_dir, 'test-dir_with.special@chars')
        os.makedirs(special_dir)
        
        test_file = os.path.join(special_dir, 'test-file.json')
        with open(test_file, 'w') as f:
            json.dump({'test': 'data'}, f)
        
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.create_backup(source_dir=special_dir)
            assert result is not None
    
    def test_backup_large_files(self, backup_manager, temp_dir):
        """Test backup with large files"""
        large_file = os.path.join(temp_dir, 'large.json')
        large_data = {'data': 'x' * 1000000}  # 1MB of data
        
        with open(large_file, 'w') as f:
            json.dump(large_data, f)
        
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.create_backup(source_dir=temp_dir)
            assert result is not None
    
    def test_backup_empty_directory(self, backup_manager, temp_dir):
        """Test backup of empty directory"""
        empty_dir = os.path.join(temp_dir, 'empty')
        os.makedirs(empty_dir)
        
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.create_backup(source_dir=empty_dir)
            assert result is not None
    
    def test_backup_nested_directories(self, backup_manager, temp_dir):
        """Test backup with nested directory structure"""
        nested_dir = os.path.join(temp_dir, 'level1', 'level2', 'level3')
        os.makedirs(nested_dir)
        
        test_file = os.path.join(nested_dir, 'test.json')
        with open(test_file, 'w') as f:
            json.dump({'nested': 'data'}, f)
        
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            result = backup_manager.create_backup(source_dir=temp_dir)
            assert result is not None
    
    def test_concurrent_backup_operations(self, backup_manager, temp_dir):
        """Test handling concurrent backup operations"""
        with patch.object(backup_manager, 'backup_dir', temp_dir):
            # Create multiple backups
            result1 = backup_manager.create_backup()
            result2 = backup_manager.create_backup()
            
            assert result1 is not None
            assert result2 is not None
            assert result1 != result2
    
    def test_backup_with_permissions_error(self, backup_manager, temp_dir):
        """Test handling permission errors during backup"""
        restricted_dir = os.path.join(temp_dir, 'restricted')
        os.makedirs(restricted_dir)
        
        with patch('shutil.copy2', side_effect=PermissionError("Access denied")):
            with patch.object(backup_manager, 'backup_dir', temp_dir):
                result = backup_manager.create_backup(source_dir=restricted_dir)
                assert result is None
    
    def test_backup_cleanup_on_failure(self, backup_manager, temp_dir):
        """Test cleanup when backup fails"""
        with patch('shutil.copy2', side_effect=Exception("Copy failed")):
            with patch.object(backup_manager, 'backup_dir', temp_dir):
                with patch('shutil.rmtree') as mock_rmtree:
                    result = backup_manager.create_backup()
                    assert result is None
                    mock_rmtree.assert_called()
