"""
Wiki Page Mapper
Utility for mapping file paths to GitHub wiki page names
"""

import re
from pathlib import Path
from typing import Dict, List

class WikiPageMapper:
    """Maps file paths to GitHub wiki page names and vice versa"""
    
    def __init__(self):
        self.invalid_chars_pattern = r'[<>:"/\\|?*]'
        self.space_chars_pattern = r'[\s_-]+'
    
    def map_file_to_wiki_page(self, file_path: Path, docs_root: Path) -> str:
        """
        Convert a markdown file path to a GitHub wiki page name.
        
        Args:
            file_path: Path to the markdown file
            docs_root: Root directory of the docs
            
        Returns:
            Wiki page name (e.g., "JSON-Inputs-Standard/Design/Architectural-Design")
        """
        # Get relative path from docs root
        relative_path = file_path.relative_to(docs_root)
        
        # Remove .md extension
        path_str = str(relative_path.with_suffix(''))
        
        # Replace invalid characters with hyphens
        page_name = re.sub(self.invalid_chars_pattern, '-', path_str)
        
        # Replace spaces, underscores, and hyphens with single hyphen
        page_name = re.sub(self.space_chars_pattern, '-', page_name)
        
        # Remove duplicate hyphens
        page_name = re.sub(r'-+', '-', page_name)
        
        # Strip leading/trailing hyphens
        page_name = page_name.strip('-')
        
        # Capitalize each word in each path segment
        parts = page_name.split('/')
        capitalized_parts = []
        for part in parts:
            words = part.split('-')
            capitalized_words = [word.capitalize() for word in words]
            capitalized_parts.append('-'.join(capitalized_words))
        
        return '/'.join(capitalized_parts)
    
    def get_directory_structure(self, docs_root: Path) -> Dict[str, List[str]]:
        """
        Get the directory structure of the docs directory.
        
        Args:
            docs_root: Root directory of the docs
            
        Returns:
            Dictionary mapping directories to their markdown files
        """
        structure = {}
        
        for md_file in docs_root.rglob('*.md'):
            relative_path = md_file.relative_to(docs_root)
            directory = str(relative_path.parent) if relative_path.parent != Path('.') else ''
            wiki_page = self.map_file_to_wiki_page(md_file, docs_root)
            
            if directory not in structure:
                structure[directory] = []
            structure[directory].append(wiki_page)
        
        return structure
