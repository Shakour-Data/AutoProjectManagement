#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: vscode_extension_installer
File: vscode_extension_installer.py
Path: autoprojectmanagement/services/integration_services/vscode_extension_installer.py

Description:
    Vscode Extension Installer module

Author: AutoProjectManagement Team
Contact: team@autoprojectmanagement.com
Repository: https://github.com/autoprojectmanagement/autoprojectmanagement

Version Information:
    Current Version: 1.0.0
    Last Updated: 2025-08-14
    Python Version: 3.8+
    
Development Status:
    Status: Production/Stable
    Created: 2024-01-01
    Last Modified: 2025-08-14
    Modified By: AutoProjectManagement Team

Dependencies:
    - Python 3.8+
    - See requirements.txt for full dependency list

License: MIT License
Copyright: (c) 2024 AutoProjectManagement Team

Usage:
    This module is part of the AutoProjectManagement package.
    Import and use as needed within the package ecosystem.

Example:
    >>> from autoprojectmanagement.services.integration_services.vscode_extension_installer import {main_class}
    >>> instance = {main_class}()
    >>> instance.run()

Notes:
    - This file follows the AutoProjectManagement coding standards
    - All changes should be documented in the changelog below
    - Ensure compatibility with Python 3.8+

Changelog:
    1.0.0 (2024-01-01): Initial release
    1.0.1 (2025-08-14): {change_description}

TODO:
    - [ ] Add comprehensive error handling
    - [ ] Implement logging throughout
    - [ ] Add unit tests
    - [ ] Update documentation

================================================================================
"""


import subprocess

# List of recommended VS Code extensions to install
extensions = [
    "blackboxai.blackbox",  # BLACKBOX AI
    "github.vscode-pull-request-github",  # GitHub Pull Requests and Issues
    "ms-python.python",  # Python
    "yzhang.markdown-all-in-one",  # Markdown All in One
    "alefragnani.project-manager",  # Project Manager
    "mhutchie.git-graph",  # Git Graph
    "vstirbu.vscode-mermaid-preview",  # Mermaid diagram preview
    "hediet.vscode-drawio",  # Draw.io integration
    "bierner.markdown-mermaid"  # Mermaid diagrams in markdown
]

def install_extensions():
    for ext in extensions:
        print(f"Installing VS Code extension: {ext}")
        subprocess.run(["code", "--install-extension", ext], check=True)
    print("All extensions installed.")

if __name__ == "__main__":
    install_extensions()
