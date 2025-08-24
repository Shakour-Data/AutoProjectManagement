# Wiki Page Mapper Documentation

## Overview
The `wiki_page_mapper.py` module provides functionality to map file paths to GitHub wiki page names and vice versa. It handles character replacement, formatting, and directory structure mapping for automated wiki synchronization.

## Class: WikiPageMapper
### Purpose
The `WikiPageMapper` class converts markdown file paths to GitHub wiki page names using standardized formatting rules and character replacements.

### Attributes
- **invalid_chars_pattern**: Regular expression pattern for invalid characters
- **space_chars_pattern**: Regular expression pattern for space characters

### Methods
- **__init__(self)**: Initializes the WikiPageMapper with regex patterns.
- **map_file_to_wiki_page(self, file_path: Path, docs_root: Path) -> str**: Converts a markdown file path to a GitHub wiki page name.
- **get_directory_structure(self, docs_root: Path) -> Dict[str, List[str]]**: Gets the directory structure of the docs directory.

## Character Replacement Rules
### Invalid Characters
The following characters are replaced with hyphens:
- `<`, `>`, `:`, `"`, `/`, `\`, `|`, `?`, `*`

### Space Characters
The following characters are replaced with single hyphens:
- Spaces (` `), underscores (`_`), hyphens (`-`)

### Formatting Rules
1. Remove `.md` extension
2. Replace invalid characters with hyphens
3. Replace space characters with single hyphens
4. Remove duplicate hyphens
5. Strip leading/trailing hyphens
6. Capitalize each word in path segments

## Examples
### File Path to Wiki Page Mapping
- `Docs/SystemDesign/Architectural_Design.md` → `System-Design/Architectural-Design`
- `Docs/ModuleDocs/main_modules_doc/communication_management.md` → `Module-Docs/Main-Modules-Doc/Communication-Management`
- `Docs/JSON-Inputs-Standard/Deployment/docker_setup.md` → `JSON-Inputs-Standard/Deployment/Docker-Setup`

## Diagrams
### UML Class Diagram
```mermaid
classDiagram
    class WikiPageMapper {
        +str invalid_chars_pattern
        +str space_chars_pattern
        +__init__()
        +map_file_to_wiki_page(file_path: Path, docs_root: Path)
        +get_directory_structure(docs_root: Path)
    }
```

### Data Flow Diagram
```mermaid
flowchart TD
    subgraph Input
        A[Markdown File Path]
    end
    
    subgraph Processing
        B[WikiPageMapper]
        C[Character Replacement]
        D[Formatting Rules]
        F[Directory Structure Analysis]
    end
    
    subgraph Output
        E[Wiki Page Name]
        G[Wiki Structure Mapping]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    B --> F
    F --> G
```

## Directory Structure Mapping
The `get_directory_structure` method analyzes the documentation directory and creates a mapping of directories to their corresponding wiki pages, enabling organized wiki navigation.

## Error Handling
The module includes error handling for:
- File path validation
- Character encoding issues
- Directory traversal errors

## Usage
### Basic Usage
```python
from pathlib import Path
from autoprojectmanagement.services.wiki_services.wiki_page_mapper import WikiPageMapper

mapper = WikiPageMapper()
docs_root = Path("/path/to/Docs")
file_path = Path("/path/to/Docs/SystemDesign/Architectural_Design.md")

wiki_page = mapper.map_file_to_wiki_page(file_path, docs_root)
# Result: "System-Design/Architectural-Design"
```

### Directory Structure Analysis
```python
structure = mapper.get_directory_structure(docs_root)
# Returns dictionary mapping directories to wiki pages
```

## Integration with Wiki Sync
The WikiPageMapper is designed to work seamlessly with the `WikiSyncService` to provide automated wiki synchronization from the documentation directory.

## Benefits
- **Consistency**: Ensures uniform wiki page naming
- **Automation**: Enables automatic wiki synchronization
- **Organization**: Maintains directory structure in wiki navigation
- **Compatibility**: Follows GitHub wiki naming conventions

## Conclusion
The Wiki Page Mapper is an essential component for automated documentation management, providing reliable file-to-wiki page mapping that maintains organizational structure and follows GitHub wiki standards.

---
*Last updated: 2025-08-14*
