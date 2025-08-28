import unittest
import os
import tempfile
import shutil
from src.autoprojectmanagement.services.automation_services.backup_manager import BackupManager, BackupConfig, BackupStatus

class TestBackupManager(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for testing
        self.temp_dir = tempfile.mkdtemp()
        self.backup_dir = tempfile.mkdtemp()
        self.config = BackupConfig(
            source_paths=[self.temp_dir],
            backup_location=self.backup_dir,
            retention_days=1
        )
        self.manager = BackupManager(self.config)

    def tearDown(self):
        # Clean up temporary directories
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        shutil.rmtree(self.backup_dir, ignore_errors=True)

    def test_create_backup_empty_directory(self):
        """Test backup creation with empty directory."""
        metadata = self.manager.create_backup()
        self.assertEqual(metadata.total_files, 0)
        self.assertEqual(metadata.status, BackupStatus.COMPLETED.value)

    def test_backup_restore_cycle(self):
        """Test complete backup and restore cycle."""
        # Create test file
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")
        
        # Create backup
        metadata = self.manager.create_backup()
        self.assertTrue(metadata.total_files > 0)
        self.assertEqual(metadata.status, BackupStatus.COMPLETED.value)
        
        # Restore backup
        restore_dir = tempfile.mkdtemp()
        try:
            success = self.manager.restore_backup(metadata.backup_id, restore_dir)
            self.assertTrue(success)
            
            restored_file = os.path.join(restore_dir, "test.txt")
            self.assertTrue(os.path.exists(restored_file))
            
            with open(restored_file, "r") as f:
                self.assertEqual(f.read(), "test content")
        finally:
            shutil.rmtree(restore_dir, ignore_errors=True)

    def test_list_backups(self):
        """Test listing available backups."""
        # Create a backup first
        metadata = self.manager.create_backup()
        
        # List backups
        backups = self.manager.list_backups()
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].backup_id, metadata.backup_id)

    def test_get_backup_status(self):
        """Test getting backup status."""
        # Create a backup first
        metadata = self.manager.create_backup()
        
        # Get backup status
        status = self.manager.get_backup_status(metadata.backup_id)
        self.assertIsNotNone(status)
        self.assertEqual(status.backup_id, metadata.backup_id)
        self.assertEqual(status.status, BackupStatus.COMPLETED.value)

    def test_backup_with_multiple_files(self):
        """Test backup with multiple files."""
        # Create multiple test files
        for i in range(3):
            test_file = os.path.join(self.temp_dir, f"test_{i}.txt")
            with open(test_file, "w") as f:
                f.write(f"content {i}")
        
        # Create backup
        metadata = self.manager.create_backup()
        self.assertEqual(metadata.total_files, 3)
        self.assertEqual(metadata.status, BackupStatus.COMPLETED.value)

if __name__ == "__main__":
    unittest.main()
