"""
Unit Tests for WikiPageMapper
Tests the file path mapping functionality for wiki pages
"""

import pytest
import tempfile
from pathlib import Path

from autoprojectmanagement.services.wiki_page_mapper import WikiPageMapper


class TestWikiPageMapper:
    """Test class for WikiPageMapper"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.mapper = WikiPageMapper()
        self.test_docs_root = Path("/test/docs")
    
    def test_init(self):
        """Test initialization of WikiPageMapper"""
        assert self.mapper.invalid_chars_pattern is not None
        assert self.mapper.space_chars_pattern is not None
    
    def test_map_file_to_wiki_page_simple(self):
        """Test mapping simple file path to wiki page name"""
        file_path = self.test_docs_root / "README.md"
        
        result = self.mapper.map_file_to_wiki_page(file_path, self.test_docs_root)
        
        assert result == "README"
    
    def test_map_file_to_wiki_page_with_spaces(self):
        """Test mapping file path with spaces"""
        file_path = self.test_docs_root / "getting started guide.md"
        
        result = self.mapper.map_file_to_wiki_page(file_path, self.test_docs_root)
        
        assert result == "Getting-Started-Guide"
    
    def test_map_file_to_wiki_page_with_underscores(self):
        """Test mapping file path with underscores"""
        file_path = self.test_docs_root / "user_guide_documentation.md"
        
        result = self.mapper.map_file_to_wiki_page(file_path, self.test_docs_root)
        
        assert result == "User-Guide-Documentation"
    
    def test_map_file_to_wiki_page_with_hyphens(self):
        """Test mapping file path with hyphens"""
        file_path = self.test_docs_root / "api-documentation-guide.md"
        
        result = self.mapper.map_file_to_wiki_page(file_path, self.test_docs_root)
        
        assert result == "Api-Documentation-Guide"
    
    def test_map_file_to_wiki_page_nested_directory(self):
        """Test mapping nested directory file path"""
        file_path = self.test_docs_root / "guides" / "api" / "getting-started.md"
        
        result = self.mapper.map_file_to_wiki_page(file_path, self.test_docs_root)
        
        assert result == "Guides/Api/Getting-Started"
    
    def test_map_file_to_wiki_page_invalid_characters(self):
        """Test mapping file path with invalid characters"""
        file_path = self.test_docs_root / "file<with>invalid:characters.md"
        
        result = self.mapper.map_file_to_wiki_page(file_path, self.test_docs_root)
        
        assert result == "File-With-Invalid-Characters"
    
    def test_map_file_to_wiki_page_multiple_spaces(self):
        """Test mapping file path with multiple consecutive spaces"""
        file_path = self.test_docs_root / "file  with   multiple    spaces.md"
        
        result = self.mapper.map_file_to_wiki_page(file_path, self.test_docs_root)
        
        assert result == "File-With-Multiple-Spaces"
    
    def test_map_file_to_wiki_page_mixed_case(self):
        """Test mapping file path preserves mixed case"""
        file_path = self.test_docs_root / "MyCustomFile.md"
        
        result = self.mapper.map_file_to_wiki_page(file_path, self.test_docs_root)
        
        assert result == "MyCustomFile"
    
    def test_map_file_to_wiki_page_complex_path(self):
        """Test mapping complex nested path"""
        file_path = self.test_docs_root / "Docs" / "SystemDesign" / "API-Reference.md"
        
        result = self.mapper.map_file_to_wiki_page(file_path, self.test_docs_root)
        
        assert result == "Docs/SystemDesign/Api-Reference"
    
    def test_get_directory_structure_empty(self):
        """Test getting directory structure for empty directory"""
        with pytest.MonkeyPatch().context() as mp:
            # Mock Path.rglob to return empty list
            mp.setattr(Path, "rglob", lambda self, pattern: [])
            
            structure = self.mapper.get_directory_structure(Path("/empty/docs"))
            
            assert structure == {}
    
    def test_get_directory_structure_single_file(self):
        """Test getting directory structure with single file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_root = Path(temp_dir)
            test_file = docs_root / "README.md"
            test_file.write_text("# Test")
            
            structure = self.mapper.get_directory_structure(docs_root)
            
            assert "" in structure
            assert "README" in structure[""]
    
    def test_get_directory_structure_nested_files(self):
        """Test getting directory structure with nested files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_root = Path(temp_dir)
            
            # Create nested structure
            guides_dir = docs_root / "guides"
            guides_dir.mkdir()
            
            api_dir = guides_dir / "api"
            api_dir.mkdir()
            
            # Create files
            (docs_root / "README.md").write_text("# README")
            (guides_dir / "index.md").write_text("# Guides")
            (api_dir / "reference.md").write_text("# API Reference")
            
            structure = self.mapper.get_directory_structure(docs_root)
            
            assert "" in structure
            assert "guides" in structure
            assert "guides/api" in structure
            
            assert "README" in structure[""]
            assert "Guides/Index" in structure["guides"]
            assert "Guides/Api/Reference" in structure["guides/api"]
    
    def test_get_directory_structure_mixed_extensions(self):
        """Test getting directory structure ignores non-markdown files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_root = Path(temp_dir)
            
            # Create mixed files
            (docs_root / "README.md").write_text("# README")
            (docs_root / "config.json").write_text("{}")
            (docs_root / "script.py").write_text("print('test')")
            
            structure = self.mapper.get_directory_structure(docs_root)
            
            assert len(structure) == 1
            assert "" in structure
            assert len(structure[""]) == 1
            assert "README" in structure[""]
    
    def test_edge_case_empty_filename(self):
        """Test edge case with empty filename after processing"""
        file_path = self.test_docs_root / ".md"
        
        result = self.mapper.map_file_to_wiki_page(file_path, self.test_docs_root)
        
        assert result == ""
    
    def test_edge_case_only_special_chars(self):
        """Test edge case with only special characters"""
        file_path = self.test_docs_root / "<>@#$%.md"
        
        result = self.mapper.map_file_to_wiki_page(file_path, self.test_docs_root)
        
        assert result == ""
