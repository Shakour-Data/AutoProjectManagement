"""
path: autoprojectmanagement/services/configuration_cli/config_and_token_management.py
File: config_and_token_management.py
Purpose: Secure configuration and token management for GitHub API integration
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Provides secure storage and retrieval of configuration data and authentication tokens
using encryption. Manages GitHub repository settings, user credentials, and API tokens
with Fernet symmetric encryption for security.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidToken

# Constants
CONFIG_FILE = 'config.json'
TOKEN_FILE = 'token.enc'
KEY_FILE = 'secret.key'
MAX_CONFIG_SIZE = 1024 * 1024  # 1MB max config file size
DEFAULT_CONFIG = {
    "github_repo": "",
    "user_name": "",
    "api_base_url": "https://api.github.com"
}

# Set up logging
logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages configuration and token storage with encryption."""
    
    def __init__(self, config_dir: Optional[str] = None) -> None:
        """
        Initialize the configuration manager.
        
        Args:
            config_dir: Directory to store configuration files. Defaults to current directory.
            
        Example:
            >>> manager = ConfigManager('/path/to/config')
            >>> manager.save_config({'key': 'value'})
        """
        self.config_dir = Path(config_dir) if config_dir else Path.cwd()
        self.config_file = self.config_dir / CONFIG_FILE
        self.token_file = self.config_dir / TOKEN_FILE
        self.key_file = self.config_dir / KEY_FILE
        
    def generate_key(self) -> bytes:
        """
        Generate a new encryption key and save it securely.
        
        Returns:
            Generated encryption key as bytes
            
        Raises:
            OSError: If unable to write key file
        """
        try:
            key = Fernet.generate_key()
            # Ensure directory exists
            self.key_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write key with restricted permissions (owner read/write only)
            with open(self.key_file, 'wb') as key_file:
                os.chmod(self.key_file, 0o600)
                key_file.write(key)
                
            logger.info(f"Encryption key generated and saved to {self.key_file}")
            return key
            
        except OSError as e:
            logger.error(f"Failed to generate encryption key: {e}")
            raise
    
    def load_key(self) -> bytes:
        """
        Load the encryption key from file.
        
        Returns:
            Encryption key as bytes
            
        Raises:
            OSError: If unable to read key file
        """
        try:
            if not self.key_file.exists():
                return self.generate_key()
                
            with open(self.key_file, 'rb') as key_file:
                key = key_file.read()
                
            if not key:
                logger.warning("Empty key file detected, regenerating")
                return self.generate_key()
                
            return key
            
        except OSError as e:
            logger.error(f"Failed to load encryption key: {e}")
            raise
    
    def encrypt_token(self, token: str) -> None:
        """
        Encrypt and save a token securely.
        
        Args:
            token: The token to encrypt and store
            
        Raises:
            ValueError: If token is empty or None
            OSError: If unable to write token file
        """
        if not token or not token.strip():
            raise ValueError("Token cannot be empty")
            
        try:
            key = self.load_key()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(token.encode())
            
            # Ensure directory exists
            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write token with restricted permissions
            with open(self.token_file, 'wb') as token_file:
                os.chmod(self.token_file, 0o600)
                token_file.write(encrypted)
                
            logger.info("Token encrypted and saved successfully")
            
        except OSError as e:
            logger.error(f"Failed to save encrypted token: {e}")
            raise
    
    def decrypt_token(self) -> Optional[str]:
        """
        Decrypt and retrieve the stored token.
        
        Returns:
            Decrypted token string, or None if no token exists
            
        Raises:
            InvalidToken: If token decryption fails (corrupted file)
            OSError: If unable to read token file
        """
        try:
            if not self.token_file.exists():
                logger.debug("No token file found")
                return None
                
            key = self.load_key()
            fernet = Fernet(key)
            
            with open(self.token_file, 'rb') as token_file:
                encrypted = token_file.read()
                
            if not encrypted:
                logger.warning("Empty token file")
                return None
                
            decrypted = fernet.decrypt(encrypted)
            return decrypted.decode()
            
        except InvalidToken:
            logger.error("Token decryption failed - file may be corrupted")
            raise
        except OSError as e:
            logger.error(f"Failed to read token file: {e}")
            raise
    
    def save_config(self, config_data: Dict[str, Any]) -> None:
        """
        Save configuration data to JSON file.
        
        Args:
            config_data: Dictionary containing configuration
            
        Raises:
            ValueError: If config_data is not a dict
            OSError: If unable to write config file
        """
        if not isinstance(config_data, dict):
            raise ValueError("Configuration must be a dictionary")
            
        try:
            # Validate config size
            config_json = json.dumps(config_data, indent=2)
            if len(config_json.encode()) > MAX_CONFIG_SIZE:
                raise ValueError(f"Config file too large (> {MAX_CONFIG_SIZE} bytes)")
                
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write config with restricted permissions
            with open(self.config_file, 'w') as config_file:
                os.chmod(self.config_file, 0o600)
                json.dump(config_data, config_file, indent=2, sort_keys=True)
                
            logger.info(f"Configuration saved to {self.config_file}")
            
        except OSError as e:
            logger.error(f"Failed to save configuration: {e}")
            raise
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from JSON file.
        
        Returns:
            Dictionary containing configuration data
            
        Raises:
            json.JSONDecodeError: If config file is invalid JSON
            OSError: If unable to read config file
        """
        try:
            if not self.config_file.exists():
                logger.debug("No config file found, returning defaults")
                return DEFAULT_CONFIG.copy()
                
            # Check file size
            if self.config_file.stat().st_size > MAX_CONFIG_SIZE:
                raise ValueError("Config file too large")
                
            with open(self.config_file, 'r') as config_file:
                config = json.load(config_file)
                
            # Merge with defaults to ensure all required keys exist
            merged_config = DEFAULT_CONFIG.copy()
            merged_config.update(config)
            
            logger.info(f"Configuration loaded from {self.config_file}")
            return merged_config
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            raise
        except OSError as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """
        Update existing configuration with new values.
        
        Args:
            updates: Dictionary containing updates to merge
            
        Raises:
            ValueError: If updates is not a dict
            OSError: If unable to read/write config file
        """
        if not isinstance(updates, dict):
            raise ValueError("Updates must be a dictionary")
            
        current_config = self.load_config()
        current_config.update(updates)
        self.save_config(current_config)
    
    def delete_config(self) -> None:
        """Delete configuration file."""
        try:
            if self.config_file.exists():
                self.config_file.unlink()
                logger.info("Configuration file deleted")
        except OSError as e:
            logger.error(f"Failed to delete configuration: {e}")
            raise
    
    def delete_token(self) -> None:
        """Delete token file."""
        try:
            if self.token_file.exists():
                self.token_file.unlink()
                logger.info("Token file deleted")
        except OSError as e:
            logger.error(f"Failed to delete token: {e}")
            raise
    
    def validate_config(self) -> Dict[str, bool]:
        """
        Validate current configuration.
        
        Returns:
            Dictionary with validation results for each key
        """
        config = self.load_config()
        validation = {
            'github_repo': bool(config.get('github_repo', '').strip()),
            'user_name': bool(config.get('user_name', '').strip()),
            'api_base_url': bool(config.get('api_base_url', '').strip()),
            'config_file_exists': self.config_file.exists(),
            'token_file_exists': self.token_file.exists(),
            'key_file_exists': self.key_file.exists()
        }
        
        logger.debug(f"Config validation: {validation}")
        return validation
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive status of configuration and token files.
        
        Returns:
            Dictionary with status information
        """
        return {
            'config_file': str(self.config_file),
            'token_file': str(self.token_file),
            'key_file': str(self.key_file),
            'config_exists': self.config_file.exists(),
            'token_exists': self.token_file.exists(),
            'key_exists': self.key_file.exists(),
            'validation': self.validate_config()
        }


# Convenience functions for backward compatibility
def generate_key() -> bytes:
    """Generate encryption key using ConfigManager."""
    manager = ConfigManager()
    return manager.generate_key()


def load_key() -> bytes:
    """Load encryption key using ConfigManager."""
    manager = ConfigManager()
    return manager.load_key()


def encrypt_token(token: str) -> None:
    """Encrypt token using ConfigManager."""
    manager = ConfigManager()
    manager.encrypt_token(token)


def decrypt_token() -> Optional[str]:
    """Decrypt token using ConfigManager."""
    manager = ConfigManager()
    return manager.decrypt_token()


def save_config(config_data: Dict[str, Any]) -> None:
    """Save configuration using ConfigManager."""
    manager = ConfigManager()
    manager.save_config(config_data)


def load_config() -> Dict[str, Any]:
    """Load configuration using ConfigManager."""
    manager = ConfigManager()
    return manager.load_config()


if __name__ == '__main__':
    # Example usage and testing
    import tempfile
    import shutil
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print("=== Configuration and Token Management Demo ===")
        
        # Initialize manager
        manager = ConfigManager(temp_dir)
        
        # Test configuration
        test_config = {
            "github_repo": "example/user-repo",
            "user_name": "testuser",
            "api_base_url": "https://api.github.com"
        }
        
        print("\n1. Saving configuration...")
        manager.save_config(test_config)
        
        print("\n2. Loading configuration...")
        loaded_config = manager.load_config()
        print(f"Loaded: {loaded_config}")
        
        print("\n3. Encrypting token...")
        test_token = "ghp_1234567890abcdef"
        manager.encrypt_token(test_token)
        
        print("\n4. Decrypting token...")
        decrypted_token = manager.decrypt_token()
        print(f"Decrypted: {'***' if decrypted_token else 'None'}")
        
        print("\n5. Validation...")
        validation = manager.validate_config()
        print(f"Validation: {validation}")
        
        print("\n6. Status...")
        status = manager.get_status()
        print(f"Status: {json.dumps(status, indent=2)}")
        
        print("\n=== Demo Complete ===")
