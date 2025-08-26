#!/usr/bin/env python3
"""
AutoProjectManagement Backup System
Automated data backup procedures for production environment
"""

import os
import sys
import json
import yaml
import logging
import subprocess
import datetime
import shutil
import tarfile
import gzip
from pathlib import Path
from typing import Dict, List, Optional

# Optional imports for cloud storage and database backup
try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    boto3 = None
    ClientError = None

try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
except ImportError:
    psycopg2 = None
    ISOLATION_LEVEL_AUTOCOMMIT = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/autoprojectmanagement/backup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BackupSystem:
    """Automated backup system for AutoProjectManagement"""
    
    def __init__(self, config_path: str = '/etc/autoprojectmanagement/backup_config.yaml'):
        self.config = self.load_config(config_path)
        self.setup_directories()
        
    def load_config(self, config_path: str) -> Dict:
        """Load backup configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self.get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Return default backup configuration"""
        return {
            'backup': {
                'enabled': True,
                'schedule': '0 2 * * *',  # Daily at 2 AM
                'retention_days': 30,
                'backup_dir': '/var/backups/autoprojectmanagement',
                'include_database': True,
                'include_files': True,
                'include_logs': False,
                'compression': 'gzip',
                'encryption': {
                    'enabled': False,
                    'key_path': None
                }
            },
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'autoprojectmanagement',
                'user': 'postgres',
                'password': None
            },
            'storage': {
                'local': {
                    'enabled': True,
                    'path': '/var/backups/autoprojectmanagement'
                },
                's3': {
                    'enabled': False,
                    'bucket': None,
                    'region': 'us-east-1',
                    'access_key': None,
                    'secret_key': None
                },
                'gcs': {
                    'enabled': False,
                    'bucket': None,
                    'credentials_path': None
                }
            },
            'notifications': {
                'email': {
                    'enabled': False,
                    'smtp_server': None,
                    'smtp_port': 587,
                    'username': None,
                    'password': None,
                    'to_address': None
                },
                'slack': {
                    'enabled': False,
                    'webhook_url': None
                }
            }
        }
    
    def setup_directories(self):
        """Create necessary directories for backups"""
        backup_dir = self.config['backup']['backup_dir']
        os.makedirs(backup_dir, exist_ok=True)
        os.makedirs(f"{backup_dir}/database", exist_ok=True)
        os.makedirs(f"{backup_dir}/files", exist_ok=True)
        os.makedirs(f"{backup_dir}/logs", exist_ok=True)
    
    def backup_database(self) -> Optional[str]:
        """Create database backup using pg_dump"""
        if not self.config['backup']['include_database']:
            return None
            
        db_config = self.config['database']
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{self.config['backup']['backup_dir']}/database/backup_{timestamp}.sql"
        
        try:
            # Use pg_dump for PostgreSQL backup
            cmd = [
                'pg_dump',
                '-h', db_config['host'],
                '-p', str(db_config['port']),
                '-U', db_config['user'],
                '-d', db_config['name'],
                '-F', 'c',  # Custom format
                '-f', backup_file
            ]
            
            # Set password environment variable
            env = os.environ.copy()
            if db_config['password']:
                env['PGPASSWORD'] = db_config['password']
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Database backup failed: {result.stderr}")
                return None
            
            logger.info(f"Database backup created: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"Error creating database backup: {e}")
            return None
    
    def backup_files(self) -> List[str]:
        """Backup important files and directories"""
        if not self.config['backup']['include_files']:
            return []
            
        backup_files = []
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = f"{self.config['backup']['backup_dir']}/files"
        
        # Define files and directories to backup
        files_to_backup = [
            '/etc/autoprojectmanagement',
            '/var/lib/autoprojectmanagement',
            '/opt/autoprojectmanagement/config',
        ]
        
        for file_path in files_to_backup:
            if os.path.exists(file_path):
                backup_name = f"{backup_dir}/{os.path.basename(file_path)}_{timestamp}.tar.gz"
                
                try:
                    with tarfile.open(backup_name, 'w:gz') as tar:
                        tar.add(file_path, arcname=os.path.basename(file_path))
                    
                    backup_files.append(backup_name)
                    logger.info(f"File backup created: {backup_name}")
                    
                except Exception as e:
                    logger.error(f"Error backing up {file_path}: {e}")
        
        return backup_files
    
    def backup_logs(self) -> List[str]:
        """Backup log files"""
        if not self.config['backup']['include_logs']:
            return []
            
        backup_files = []
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = f"{self.config['backup']['backup_dir']}/logs"
        
        log_files = [
            '/var/log/autoprojectmanagement/app.log',
            '/var/log/autoprojectmanagement/error.log',
            '/var/log/autoprojectmanagement/access.log',
        ]
        
        for log_file in log_files:
            if os.path.exists(log_file):
                backup_name = f"{backup_dir}/{os.path.basename(log_file)}_{timestamp}.gz"
                
                try:
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(backup_name, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    backup_files.append(backup_name)
                    logger.info(f"Log backup created: {backup_name}")
                    
                except Exception as e:
                    logger.error(f"Error backing up log {log_file}: {e}")
        
        return backup_files
    
    def compress_backup(self, file_path: str) -> Optional[str]:
        """Compress backup file if not already compressed"""
        if self.config['backup']['compression'] == 'none':
            return file_path
            
        compressed_path = f"{file_path}.gz"
        
        try:
            with open(file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            os.remove(file_path)
            logger.info(f"Compressed backup: {compressed_path}")
            return compressed_path
            
        except Exception as e:
            logger.error(f"Error compressing backup: {e}")
            return file_path
    
    def upload_to_s3(self, file_path: str) -> bool:
        """Upload backup file to S3"""
        s3_config = self.config['storage']['s3']
        if not s3_config['enabled']:
            return False
            
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=s3_config['access_key'],
                aws_secret_access_key=s3_config['secret_key'],
                region_name=s3_config['region']
            )
            
            bucket_name = s3_config['bucket']
            s3_key = f"backups/{os.path.basename(file_path)}"
            
            s3_client.upload_file(file_path, bucket_name, s3_key)
            logger.info(f"Uploaded to S3: s3://{bucket_name}/{s3_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error uploading to S3: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Remove backups older than retention period"""
        retention_days = self.config['backup']['retention_days']
        backup_dir = self.config['backup']['backup_dir']
        cutoff_time = datetime.datetime.now() - datetime.timedelta(days=retention_days)
        
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if file_time < cutoff_time:
                    try:
                        os.remove(file_path)
                        logger.info(f"Removed old backup: {file_path}")
                    except Exception as e:
                        logger.error(f"Error removing old backup {file_path}: {e}")
    
    def send_notification(self, success: bool, backup_files: List[str]):
        """Send backup completion notification"""
        # Implementation for email/Slack notifications would go here
        if success:
            logger.info("Backup completed successfully")
        else:
            logger.error("Backup failed")
    
    def run_backup(self):
        """Execute complete backup procedure"""
        logger.info("Starting backup procedure")
        
        try:
            backup_files = []
            
            # Database backup
            db_backup = self.backup_database()
            if db_backup:
                backup_files.append(db_backup)
            
            # File backups
            file_backups = self.backup_files()
            backup_files.extend(file_backups)
            
            # Log backups
            log_backups = self.backup_logs()
            backup_files.extend(log_backups)
            
            # Compress backups if needed
            if self.config['backup']['compression'] != 'none':
                compressed_files = []
                for file_path in backup_files:
                    compressed = self.compress_backup(file_path)
                    if compressed:
                        compressed_files.append(compressed)
                backup_files = compressed_files
            
            # Upload to cloud storage
            for file_path in backup_files:
                if self.config['storage']['s3']['enabled']:
                    self.upload_to_s3(file_path)
                # Add other storage providers here
            
            # Cleanup old backups
            self.cleanup_old_backups()
            
            # Send success notification
            self.send_notification(True, backup_files)
            logger.info("Backup procedure completed successfully")
            
        except Exception as e:
            logger.error(f"Backup procedure failed: {e}")
            self.send_notification(False, [])
            raise
    
    def create_restore_script(self, backup_path: str):
        """Create a restoration script for a specific backup"""
        backup_basename = os.path.basename(backup_path)
        current_time = datetime.datetime.now()
        
        script_content = f"""#!/bin/bash
# AutoProjectManagement Restore Script
# Backup: {backup_basename}
# Created: {current_time}

set -e

echo "Starting restoration from backup: {backup_path}"

# Extract backup if compressed
if [[ "{backup_path}" == *.gz ]]; then
    echo "Decompressing backup..."
    gunzip -c "{backup_path}" > "{backup_path[:-3]}"
    backup_path="{backup_path[:-3]}"
fi

# Restore database
if [[ "{backup_path}" == *.sql ]]; then
    echo "Restoring database..."
    pg_restore -h localhost -U postgres -d autoprojectmanagement "{backup_path}"
fi

# Restore files
if [[ "{backup_path}" == *.tar.gz ]]; then
    echo "Restoring files..."
    tar -xzf "{backup_path}" -C /
fi

echo "Restoration completed successfully"
"""
        
        script_path = f"{os.path.dirname(backup_path)}/restore_{os.path.basename(backup_path)}.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        os.chmod(script_path, 0o755)
        logger.info(f"Restore script created: {script_path}")

def main():
    """Main function for command-line usage"""
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = '/etc/autoprojectmanagement/backup_config.yaml'
    
    try:
        backup_system = BackupSystem(config_path)
        backup_system.run_backup()
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
