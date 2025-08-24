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
                
                for entry in type_entries:
                    scope_part = f"**{entry.scope}**: " if entry.scope else ""
                    output.append(f"- {scope_part}{entry.message} ({entry.sha}) - *{entry.author}*")
        
        return "\n".join(output)
    
    def _format_changelog_json(self, entries: List[ChangelogEntry]) -> str:
        """Format changelog entries as JSON."""
        entries_dict = [asdict(entry) for entry in entries]
        return json.dumps({
            "changelog": entries_dict,
            "generated_at": datetime.datetime.now().isoformat(),
            "total_entries": len(entries)
        }, indent=2)
    
    def _format_changelog_text(self, entries: List[ChangelogEntry]) -> str:
        """Format changelog entries as plain text."""
        output = ["CHANGELOG", "=========", ""]
        
        for entry in entries:
            output.append(f"{entry.date}: {entry.message} ({entry.sha}) - {entry.author}")
        
        return "\n".join(output)
    
    def generate_release_notes(self, tag_name: str, previous_tag: Optional[str] = None) -> ReleaseNotes:
        """
        Generate comprehensive release notes for a specific tag.
        
        Args:
            tag_name: The release tag name (e.g., "v1.0.0")
            previous_tag: Optional previous tag for comparison
            
        Returns:
            ReleaseNotes: Structured release notes object
        """
        try:
            # Get commits for this release
            commits = self.github.get_commits_since_tag(previous_tag) if previous_tag else self.github.get_commits()
            
            changes = []
            contributors = set()
            breaking_changes = []
            
            for commit in commits:
                message = commit['commit']['message']
                author = commit['commit']['author']['name']
                
                # Check for breaking changes
                if "BREAKING CHANGE" in message or "!" in message.split(':')[0]:
                    breaking_changes.append(message)
                
                commit_type, scope = self._parse_commit_message(message)
                
                entry = ChangelogEntry(
                    date=commit['commit']['author']['date'][:10],
                    message=message,
                    sha=commit['sha'][:7],
                    author=author,
                    type=commit_type,
                    scope=scope
                )
                changes.append(entry)
                contributors.add(author)
            
            # Create summary
            feat_count = sum(1 for entry in changes if entry.type == 'feat')
            fix_count = sum(1 for entry in changes if entry.type == 'fix')
            
            summary = f"Release {tag_name} includes {feat_count} new features and {fix_count} bug fixes."
            if breaking_changes:
                summary += f" Includes {len(breaking_changes)} breaking changes."
            
            return ReleaseNotes(
                version=tag_name,
                release_date=datetime.datetime.now().strftime('%Y-%m-%d'),
                changes=changes,
                summary=summary,
                breaking_changes=breaking_changes,
                contributors=list(contributors)
            )
            
        except Exception as e:
            self.logger.error(f"Error generating release notes: {e}")
            return ReleaseNotes(
                version=tag_name,
                release_date=datetime.datetime.now().strftime('%Y-%m-%d'),
                changes=[],
                summary=f"Error generating release notes: {e}"
            )
    
    def save_documentation(self, content: str, filename: str, output_dir: str = "docs") -> bool:
        """
        Save generated documentation to file.
        
        Args:
            content: Documentation content to save
            filename: Output filename
            output_dir: Output directory
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"✅ Documentation saved to: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save documentation: {e}")
            return False
    
    def generate_complete_documentation(self, output_dir: str = "docs") -> Dict[str, bool]:
        """
        Generate complete documentation suite including changelog and release notes.
        
        Args:
            output_dir: Output directory for documentation files
            
        Returns:
            Dict[str, bool]: Dictionary indicating success for each documentation type
        """
        results = {}
        
        # Generate and save changelog
        changelog = self.generate_changelog()
        results['changelog'] = self.save_documentation(changelog, "CHANGELOG.md", output_dir)
        
        # Generate and save latest release notes
        release_notes = self.generate_release_notes("Latest")
        release_notes_content = json.dumps(asdict(release_notes), indent=2)
        results['release_notes'] = self.save_documentation(release_notes_content, "RELEASE_NOTES.json", output_dir)
        
        return results


# Usage Example
if __name__ == "__main__":
    # Example usage
    repo_owner = "your_org_or_username"
    repo_name = "ProjectManagement"
    
    try:
        github = GitHubIntegration(repo_owner, repo_name)
        doc_auto = DocumentationAutomation(github)
        
        # Generate changelog
        changelog = doc_auto.generate_changelog(since_date="2024-01-01")
        print("📋 Changelog generated successfully")
        
        # Generate release notes
        release_notes = doc_auto.generate_release_notes("v1.0.0")
        print("📄 Release notes generated successfully")
        
        # Save documentation
        results = doc_auto.generate_complete_documentation()
        print(f"💾 Documentation saved: {results}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
