#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: test_password_hashing.py
File: test_password_hashing.py
Purpose: Test password hashing functionality
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
"""

from autoprojectmanagement.utils.security import password_hasher

def test_password_hashing():
    password = "SecurePass123!"
    hashed_password = password_hasher.hash_password(password)
    
    print(f"Original Password: {password}")
    print(f"Hashed Password: {hashed_password}")
    
    # Verify the password
    is_valid = password_hasher.verify_password(password, hashed_password)
    print(f"Password verification result: {is_valid}")

if __name__ == "__main__":
    test_password_hashing()
