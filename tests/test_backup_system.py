#!/usr/bin/env python3
"""
Test script for the backup system
"""

import os
import tempfile
import shutil
from backup_system import BackupSystem

def test_backup_system():
    """Test the backup system functionality"""
    
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp()
    backup_dir = os.path.join(test_dir, 'backups')
    config_path = os.path.join(test_dir, 'backup_config.yaml')
    
    # Create test config
    config_content = """
backup:
  enabled: true
  schedule: "0 2 * * *"
  retention_days: 7
  backup_dir: "{backup_dir}"
  include_database: false
  include_files: true
  include_logs: false
  compression: gzip
  encryption:
    enabled: false
    key_path: null

database:
  host: localhost
  port: 5432
  name: test_db
  user: postgres
  password: null

storage:
  local:
    enabled: true
    path: "{backup_dir}"
  s3:
    enabled: false
    bucket: null
    region: us-east-1
    access_key: null
    secret_key: null
  gcs:
    enabled: false
    bucket: null
    credentials_path: null

notifications:
  email:
    enabled: false
    smtp_server: null
    smtp_port: 587
    username: null
    password: null
    to_address: null
  slack:
    enabled: false
    webhook_url: null
""".format(backup_dir=backup_dir.replace('\\', '/'))
    
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    # Create test files to backup
    test_files_dir = os.path.join(test_dir, 'test_files')
    os.makedirs(test_files_dir, exist_ok=True)
    
    # Create some test files
    with open(os.path.join(test_files_dir, 'test1.txt'), 'w') as f:
        f.write("Test file 1 content")
    
    with open(os.path.join(test_files_dir, 'test2.txt'), 'w') as f:
        f.write("Test file 2 content")
    
    try:
        # Initialize backup system
        backup_system = BackupSystem(config_path)
        
        # Test file backup
        print("Testing file backup...")
        backup_files = backup_system.backup_files()
        print(f"Backup files created: {backup_files}")
        
        # Test cleanup
        print("Testing cleanup...")
        backup_system.cleanup_old_backups()
        print("Cleanup completed")
        
        print("Backup system test completed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        raise
    finally:
        # Cleanup
        shutil.rmtree(test_dir, ignore_errors=True)

if __name__ == "__main__":
    test_backup_system()
