#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

print("Testing imports...")

try:
    from autoprojectmanagement.services.integration_services.github_integration import GitHubIntegration
    print("✓ GitHubIntegration imported successfully")
except Exception as e:
    print(f"✗ GitHubImportError: {e}")
    import traceback
    traceback.print_exc()

try:
    from autoprojectmanagement.services.audit_service import AuditActionType, AuditResourceType, AuditSeverity, AuditStatus
    print("✓ Audit service imports successful")
    print(f"  ISSUE: {AuditResourceType.ISSUE}")
    print(f"  COMMENT: {AuditResourceType.COMMENT}")
    print(f"  WEBHOOK: {AuditResourceType.WEBHOOK}")
except Exception as e:
    print(f"✗ Audit import error: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting mock imports...")
try:
    from unittest.mock import patch, MagicMock
    print("✓ Mock imports successful")
except Exception as e:
    print(f"✗ Mock import error: {e}")
    import traceback
    traceback.print_exc()

print("\nAll imports completed")
