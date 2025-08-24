# Wiki Services Documentation

## Overview
Wiki Services provide automated synchronization between local documentation files and GitHub wiki repositories. These services handle file mapping, wiki creation, and change management.

## Services
### 1. Wiki Page Mapper
The `wiki_page_mapper.py` module converts file paths to GitHub wiki page names using standardized formatting rules.

**Key Features:**
- Character replacement and formatting
- Directory structure mapping
- Wiki page name generation
- File path validation

**Documentation:** [wiki_page_mapper.md](./wiki_page_mapper.md)

### 2. Wiki Sync Service
