"""
Wiki Git Operations for AutoProjectManagement
Purpose: Manage Git operations related to wiki pages and synchronization
Author: AutoProjectManagement System
Version: 1.0.0
License: MIT
"""

import os
import subprocess
import logging

logger = logging.getLogger(__name__)

class WikiGitOperations:
    """Handles Git operations for wiki pages."""
    
    def __init__(self, wiki_path: str):
        """Initialize the WikiGitOperations with the path to the wiki."""
        self.wiki_path = wiki_path
        self.logger = logging.getLogger(__name__)
        
    def clone_wiki(self, repo_url: str) -> bool:
        """Clone the wiki repository from the given URL."""
        try:
            subprocess.run(["git", "clone", repo_url, self.wiki_path], check=True)
            self.logger.info(f"✅ Cloned wiki from {repo_url} to {self.wiki_path}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Failed to clone wiki: {e}")
            return False
    
    def pull_wiki(self) -> bool:
        """Pull the latest changes from the wiki repository."""
        try:
            subprocess.run(["git", "-C", self.wiki_path, "pull"], check=True)
            self.logger.info("✅ Pulled latest changes from wiki")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Failed to pull wiki: {e}")
            return False
    
    def add_wiki_file(self, file_path: str) -> bool:
        """Add a file to the wiki repository."""
        try:
            subprocess.run(["git", "-C", self.wiki_path, "add", file_path], check=True)
            self.logger.info(f"✅ Added {file_path} to wiki")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Failed to add file to wiki: {e}")
            return False
    
    def commit_wiki_changes(self, message: str) -> bool:
        """Commit changes to the wiki repository."""
        try:
            subprocess.run(["git", "-C", self.wiki_path, "commit", "-m", message], check=True)
            self.logger.info("✅ Committed changes to wiki")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Failed to commit changes to wiki: {e}")
            return False
    
    def push_wiki_changes(self) -> bool:
        """Push changes to the wiki repository."""
        try:
            subprocess.run(["git", "-C", self.wiki_path, "push"], check=True)
            self.logger.info("✅ Pushed changes to wiki")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Failed to push changes to wiki: {e}")
            return False

if __name__ == "__main__":
    wiki_operations = WikiGitOperations(wiki_path="./path/to/wiki")
    # Example usage
    wiki_operations.clone_wiki("https://github.com/username/wiki.git")
    wiki_operations.pull_wiki()
    wiki_operations.add_wiki_file("new_page.md")
    wiki_operations.commit_wiki_changes("Added new page")
    wiki_operations.push_wiki_changes()
