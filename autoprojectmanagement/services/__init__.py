"""
Services module for AutoProjectManagement
"""

from .automation_services.auto_commit import AutoCommit
from .automation_services.backup_manager import BackupManager
from .configuration_cli.cli_commands import *
from .github_integration import GitHubIntegration
from .integration_services.integration_manager import IntegrationManager

__all__ = [
    "AutoCommit",
    "BackupManager",
    "GitHubIntegration",
    "IntegrationManager",
]
