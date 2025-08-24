"""
Documentation Automation for AutoProjectManagement
Purpose: Automate generation of changelogs, release notes, and project documentation
Author: AutoProjectManagement System
Version: 2.0.0
License: MIT
Description: Unified version combining the best features from both auto_commit implementations
           - Enhanced authentication and guaranteed push from automation_services version
           - Project management integration and WBS features from services version
"""

from autoprojectmanagement.services.integration_services.github_integration import GitHubIntegration
import datetime
import logging
import json
import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class ChangelogEntry:
    """Data class representing a single changelog entry."""
    date: str
    message: str
    sha: str
    author: str
    type: str = "change"
    scope: str = ""


@dataclass
class ReleaseNotes:
    """Data class representing release notes."""
    version: str
    release_date: str
    changes: List[ChangelogEntry]
    summary: str = ""
    breaking_changes: List[str] = None
    contributors: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.breaking_changes is None:
            self.breaking_changes = []
        if self.contributors is None:
            self.contributors = []


class DocumentationAutomation:
    """
    Comprehensive documentation automation system for generating changelogs,
    release notes, and project documentation from GitHub commits and issues.
    
    Features:
    - Automated changelog generation from Git commits
    - Release notes creation with semantic versioning support
    - Documentation template generation
    - Integration with GitHub API for rich metadata
    - Retry mechanism for API calls
    - Customizable output formats
    
    Attributes:
        github (GitHubIntegration): GitHub integration instance
        max_retries (int): Maximum retry attempts for API calls
        retry_delay (int): Delay between retry attempts in seconds
        logger (logging.Logger): Logger instance for operation tracking
    """
    
    def __init__(self, github_integration: GitHubIntegration, max_retries: int = 3, retry_delay: int = 2):
        """
        Initialize the DocumentationAutomation service.
        
        Args:
            github_integration: GitHubIntegration instance for API access
            max_retries: Maximum number of retry attempts for API calls
            retry_delay: Delay between retry attempts in seconds
        """
        self.github = github_integration
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def generate_changelog(self, since_date: Optional[str] = None, format: str = "markdown") -> str:
        """
        Generate a comprehensive changelog from GitHub commits.
        
        Args:
            since_date: ISO format date string to filter commits (e.g., "2024-01-01")
            format: Output format ("markdown", "json", "text")
            
        Returns:
            str: Generated changelog in specified format
            
        Raises:
            ValueError: If invalid format is specified
        """
        retries = 0
        while retries < self.max_retries:
            try:
                commits = self.github.get_commits(per_page=100)
                changelog_entries = []
                
                for commit in commits:
                    commit_date = commit['commit']['author']['date']
                    commit_date_obj = datetime.datetime.fromisoformat(commit_date.replace('Z', '+00:00'))
                    
                    # Filter by date if specified
                    if since_date:
                        since_date_obj = datetime.datetime.fromisoformat(since_date)
                        if commit_date_obj < since_date_obj:
                            continue
                    
                    message = commit['commit']['message']
                    sha = commit['sha'][:7]
                    author = commit['commit']['author']['name']
                    
                    # Parse commit type and scope from message
                    commit_type, scope = self._parse_commit_message(message)
                    
                    entry = ChangelogEntry(
                        date=commit_date[:10],
                        message=message,
                        sha=sha,
                        author=author,
                        type=commit_type,
                        scope=scope
                    )
                    changelog_entries.append(entry)
                
                # Sort entries by date (newest first)
                changelog_entries.sort(key=lambda x: x.date, reverse=True)
                
                # Format output
                if format == "markdown":
                    return self._format_changelog_markdown(changelog_entries)
                elif format == "json":
                    return self._format_changelog_json(changelog_entries)
                elif format == "text":
                    return self._format_changelog_text(changelog_entries)
                else:
                    raise ValueError(f"Unsupported format: {format}")
                    
            except Exception as e:
                self.logger.error(f"Error generating changelog: {e}. Retry {retries + 1} of {self.max_retries}")
                retries += 1
                if retries >= self.max_retries:
                    self.logger.error("Failed to generate changelog after maximum retries")
                    return "Error: Failed to generate changelog"
    
    def _parse_commit_message(self, message: str) -> tuple:
        """
        Parse commit message to extract type and scope.
        
        Args:
            message: Raw commit message
            
        Returns:
            tuple: (commit_type, scope)
        """
        # Conventional commit pattern: type(scope): description
        import re
        pattern = r'^(\w+)(?:\(([^)]+)\))?:'
        match = re.match(pattern, message)
        
        if match:
            commit_type = match.group(1).lower()
            scope = match.group(2) or ""
            return commit_type, scope
        
        # Fallback: guess from message content
        message_lower = message.lower()
        if any(word in message_lower for word in ['feat', 'feature', 'add']):
            return "feat", ""
        elif any(word in message_lower for word in ['fix', 'bug', 'error']):
            return "fix", ""
        elif any(word in message_lower for word in ['docs', 'documentation']):
            return "docs", ""
        elif any(word in message_lower for word in ['refactor', 'cleanup']):
            return "refactor", ""
        else:
            return "chore", ""
    
    def _format_changelog_markdown(self, entries: List[ChangelogEntry]) -> str:
        """Format changelog entries as Markdown."""
        output = ["# Changelog\n", "All notable changes to this project will be documented in this file.\n"]
        
        # Group by date
        entries_by_date = {}
        for entry in entries:
            if entry.date not in entries_by_date:
                entries_by_date[entry.date] = []
            entries_by_date[entry.date].append(entry)
        
        # Generate sections
        for date, date_entries in sorted(entries_by_date.items(), reverse=True):
            output.append(f"\n## {date}\n")
            
            # Group by type within date
            entries_by_type = {}
            for entry in date_entries:
                if entry.type not in entries_by_type:
                    entries_by_type[entry.type] = []
                entries_by_type[entry.type].append(entry)
            
            for commit_type, type_entries in entries_by_type.items():
                type_display = {
                    'feat': '✨ Features',
                    'fix': '🐛 Bug Fixes',
                    'docs': '📝 Documentation',
                    'refactor': '♻️ Refactoring',
                    'chore': '🔧 Chores'
                }.get(commit_type, '📦 Changes')
                
                output.append(f"\n### {type_display}\n")
