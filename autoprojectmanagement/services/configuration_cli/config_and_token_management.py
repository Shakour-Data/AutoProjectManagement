#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: config_and_token_management
File: config_and_token_management.py
Path: autoprojectmanagement/services/configuration_cli/config_and_token_management.py

Description:
    Config And Token Management module

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
    >>> from autoprojectmanagement.services.configuration_cli.config_and_token_management import {main_class}
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


import os
import json
from cryptography.fernet import Fernet

CONFIG_FILE = 'config.json'
TOKEN_FILE = 'token.enc'
KEY_FILE = 'secret.key'

def generate_key():
    """Generate a key for encryption and save it."""
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load the encryption key."""
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read()
    return key

def encrypt_token(token):
    key = load_key()
    f = Fernet(key)
    encrypted = f.encrypt(token.encode())
    with open(TOKEN_FILE, 'wb') as token_file:
        token_file.write(encrypted)

def decrypt_token():
    key = load_key()
    f = Fernet(key)
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, 'rb') as token_file:
        encrypted = token_file.read()
    decrypted = f.decrypt(encrypted)
    return decrypted.decode()

def save_config(config_data):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)

if __name__ == '__main__':
    # Example usage
    config = {
        "github_repo": "user/repo",
        "user_name": "username"
    }
    save_config(config)
    token = "your_github_token_here"
    encrypt_token(token)
    print("Config and token saved securely.")
