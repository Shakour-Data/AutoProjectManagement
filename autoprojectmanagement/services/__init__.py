"""
Services module for AutoProjectManagement
"""

from .auto_commit import AutoCommit
from .backup_manager import BackupManager
from .cli_commands import CLICommands
from .github_integration import GitHubIntegration
from .integration_manager import IntegrationManager

__all__ = [
    "AutoCommit",
    "BackupManager",
    "CLICommands",
    "GitHubIntegration",
    "IntegrationManager",
]
