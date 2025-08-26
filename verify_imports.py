#!/usr/bin/env python3
"""
Verification script to check that all required imports for backup_system.py are working
"""

import sys

def verify_imports():
    """Verify all required imports for the backup system"""
    
    print("Verifying imports for backup_system.py...")
    
    # Test core imports
    try:
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
        print("✓ Core imports successful")
    except ImportError as e:
        print(f"✗ Core import failed: {e}")
        return False
    
    # Test optional imports with try/except blocks
    try:
        import boto3
        from botocore.exceptions import ClientError
        print("✓ boto3 and botocore imports successful")
    except ImportError as e:
        print(f"✗ AWS imports failed: {e}")
        # These are optional, so we don't fail the test
    
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        print("✓ psycopg2 imports successful")
    except ImportError as e:
        print(f"✗ PostgreSQL imports failed: {e}")
        # These are optional, so we don't fail the test
    
    # Test BackupSystem class import
    try:
        sys.path.insert(0, '.')
        from backup_system import BackupSystem
        print("✓ BackupSystem import successful")
        
        # Test creating an instance
        backup = BackupSystem('backup_config.yaml')
        print("✓ BackupSystem instance creation successful")
        
    except Exception as e:
        print(f"✗ BackupSystem test failed: {e}")
        return False
    
    print("\n✅ All imports verified successfully!")
    print("The backup system is ready to use.")
    return True

if __name__ == "__main__":
    success = verify_imports()
    sys.exit(0 if success else 1)
