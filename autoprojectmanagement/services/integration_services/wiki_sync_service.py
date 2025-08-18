#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/services/integration_services/wiki_sync_service.py
File: wiki_sync_service.py
Purpose: Wiki synchronization service
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Wiki synchronization service within the AutoProjectManagement system
"""

import logging
from typing import Dict, Any, Optional, List, Union
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CURRENT_VERSION = "2.0.0"
PYTHON_MIN_VERSION = "3.8+"
CREATED_DATE = "2025-08-14"
MODIFIED_DATE = "2025-08-14"

# Module-level docstring
__doc__ = """
Wiki synchronization service within the AutoProjectManagement system

This module is part of the AutoProjectManagement system.
For more information, visit: https://github.com/autoprojectmanagement/autoprojectmanagement
"""

# Version information
__version__ = CURRENT_VERSION
__author__ = "AutoProjectManagement Team"
__license__ = "MIT"


import os
import shutil
import tempfile
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from .wiki_git_operations import WikiGitOperations
from .wiki_page_mapper import WikiPageMapper
from ..services.github_integration import GitHubIntegration


class WikiSyncService:
    """Main service for synchronizing Docs/ markdown files to GitHub Wiki"""
    
    def __init__(self, repo_owner: str, repo_name: str, github_token: str = None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        
        self.wiki_repo_url = f"https://github.com/{repo_owner}/{repo_name}.wiki.git"
        self.wiki_git_url = f"https://{self.github_token}@github.com/{repo_owner}/{repo_name}.wiki.git"
        
        self.docs_path = Path("/home/gravitywavesdb/GravityProjects/AutoProjectManagement/Docs")
        self.temp_dir = None
        
        self.logger = logging.getLogger(__name__)
        self.mapper = WikiPageMapper()
        self.git_ops = WikiGitOperations(self.wiki_git_url, self.github_token)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def sync_to_wiki(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        Main synchronization method
        Returns sync results with statistics
        """
        self.logger.info("Starting wiki synchronization...")
        
        try:
            # Check if wiki exists
            if not self._wiki_exists():
                self.logger.warning("Wiki repository does not exist. Creating initial wiki...")
                self._create_initial_wiki()
            
            # Clone wiki repository
            self.temp_dir = self.git_ops.clone_wiki_repo()
            self.logger.info(f"Wiki cloned to: {self.temp_dir}")
            
            # Discover markdown files
            markdown_files = self._discover_markdown_files()
            self.logger.info(f"Found {len(markdown_files)} markdown files")
            
            # Process files and generate sync plan
            sync_plan = self._generate_sync_plan(markdown_files)
            
            if dry_run:
                return self._dry_run_report(sync_plan)
            
            # Execute sync plan
            results = self._execute_sync(sync_plan)
            
            # Commit and push changes
            if results['files_changed'] > 0:
                commit_message = self.git_ops.generate_commit_message(results)
                committed = self.git_ops.commit_changes(self.temp_dir, commit_message)
                if committed:
                    pushed = self.git_ops.push_changes(self.temp_dir)
                    if pushed:
                        self.logger.info("Changes pushed to wiki successfully")
                    else:
                        self.logger.error("Failed to push changes to wiki")
                else:
                    self.logger.info("No changes to commit")
            
            self.logger.info(f"Sync completed: {results['files_changed']} files changed")
            return results
            
        except Exception as e:
            self.logger.error(f"Sync failed: {str(e)}")
            raise
        finally:
            self._cleanup()

    def _wiki_exists(self) -> bool:
        """Check if wiki repository exists"""
        try:
            import requests
            headers = {}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            response = requests.get(
                f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}",
                headers=headers
            )
            if response.status_code == 200:
                repo_data = response.json()
                return repo_data.get('has_wiki', False)
            return False
        except Exception as e:
            self.logger.error(f"Error checking wiki existence: {e}")
            return False

    def _create_initial_wiki(self):
        """Create initial wiki with Home page"""
        self.logger.info("Creating initial wiki...")
        
        # Use GitHub API to create initial wiki page
        github = GitHubIntegration(self.repo_owner, self.repo_name, self.github_token)
        
        home_content = f"""# {self.repo_name} Documentation

Welcome to the {self.repo_name} documentation wiki!

This wiki contains automatically synchronized documentation from the project's Docs/ directory.

## Navigation

- **Home** - This page
- **Documentation** - Auto-synced from Docs/ directory

## Structure

Documentation is organized based on the original file structure:
- **SystemDesign** - System design documentation
- **ModuleDocs** - Module documentation
- **JSON-Inputs-Standard** - JSON input standards
- **Entire-Project** - Project-wide documentation

---

*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        github.create_wiki_page(self.repo_name, "Home", home_content)

    def _discover_markdown_files(self) -> List[Path]:
        """Discover all markdown files in Docs/ directory"""
        if not self.docs_path.exists():
            self.logger.warning(f"Docs directory not found: {self.docs_path}")
            return []
        
        markdown_files = list(self.docs_path.rglob("*.md"))
        return [f for f in markdown_files if f.is_file()]

    def _generate_sync_plan(self, markdown_files: List[Path]) -> Dict[str, Any]:
        """Generate synchronization plan with changes to apply"""
        plan = {
            'files_to_add': [],
            'files_to_update': [],
            'files_to_delete': [],
            'total_files': len(markdown_files)
        }
        
        if not self.temp_dir or not Path(self.temp_dir).exists():
            return plan
        
        # Get current wiki files
        current_wiki_files = self._get_current_wiki_files()
        
        # Map markdown files to wiki pages
        for md_file in markdown_files:
            wiki_page_name = self.mapper.map_file_to_wiki_page(md_file, self.docs_path)
            wiki_file_path = Path(self.temp_dir) / f"{wiki_page_name}.md"
            
            if wiki_file_path.exists():
                # Check if file needs update
                if self._file_needs_update(md_file, wiki_file_path):
                    plan['files_to_update'].append({
                        'source': md_file,
                        'target': wiki_file_path,
                        'wiki_name': wiki_page_name
                    })
            else:
                # New file to add
                plan['files_to_add'].append({
                    'source': md_file,
                    'target': wiki_file_path,
                    'wiki_name': wiki_page_name
                })
        
        # Check for files to delete
        expected_wiki_files = {self.mapper.map_file_to_wiki_page(f, self.docs_path) + '.md' 
                             for f in markdown_files}
        
        for wiki_file in current_wiki_files:
            if wiki_file not in expected_wiki_files and wiki_file != 'Home.md':
                plan['files_to_delete'].append(wiki_file)
        
        return plan
