"""
path: autoprojectmanagement/services/configuration_cli/cli_commands.py
File: cli_commands.py
Purpose: Command-line interface commands for AutoProjectManagement configuration and management
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Provides CLI commands for project configuration, token management, and system setup
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import logging
from datetime import datetime
from dataclasses import dataclass
import getpass
import hashlib
import secrets

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('autoproject_cli.log')
    ]
)
logger = logging.getLogger(__name__)

# Constants
CONFIG_DIR_NAME = '.autoprojectmanagement'
CONFIG_FILE_NAME = 'config.json'
TOKEN_FILE_NAME = '.tokens'
MAX_TOKEN_LENGTH = 255
DEFAULT_CONFIG = {
    "version": "1.0.0",
    "created_at": None,
    "updated_at": None,
    "github_token": None,
    "project_root": None,
    "auto_backup": True,
    "log_level": "INFO"
}

@dataclass
class CLIConfig:
    """Configuration data structure for CLI commands."""
    version: str
    created_at: Optional[str]
    updated_at: Optional[str]
    github_token: Optional[str]
    project_root: Optional[str]
    auto_backup: bool
    log_level: str

class CLICommands:
    """
    Command-line interface commands for AutoProjectManagement configuration.
    
    This class provides methods for handling CLI operations including:
    - Configuration management
    - Token management
    - System initialization
    - Environment setup
    
    Attributes:
        config_dir: Path to configuration directory
        config_file: Path to configuration file
        token_file: Path to token storage file
    """
    
    def __init__(self) -> None:
        """Initialize CLI commands with configuration paths."""
        self.config_dir: Path = Path.home() / CONFIG_DIR_NAME
        self.config_file: Path = self.config_dir / CONFIG_FILE_NAME
        self.token_file: Path = self.config_dir / TOKEN_FILE_NAME
        self._ensure_config_dir()
    
    def _ensure_config_dir(self) -> None:
        """Ensure configuration directory exists with proper permissions."""
        try:
            self.config_dir.mkdir(mode=0o700, exist_ok=True)
            logger.info(f"Configuration directory ensured at: {self.config_dir}")
        except PermissionError as e:
            logger.error(f"Permission denied creating config directory: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to create config directory: {e}")
            raise
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from JSON file with validation.
        
        Returns:
            Dict containing validated configuration data
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        try:
            if not self.config_file.exists():
                logger.warning("Configuration file not found, using defaults")
                return DEFAULT_CONFIG.copy()
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # Validate required fields
            validated_config = DEFAULT_CONFIG.copy()
            validated_config.update(config)
            validated_config['updated_at'] = datetime.now().isoformat()
            
            logger.info("Configuration loaded successfully")
            return validated_config
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """
        Save configuration to JSON file with backup.
        
        Args:
            config: Configuration dictionary to save
            
        Raises:
            PermissionError: If unable to write config file
            OSError: If file system error occurs
        """
        try:
            # Create backup of existing config
            if self.config_file.exists():
                backup_file = self.config_file.with_suffix('.json.backup')
                backup_file.write_text(self.config_file.read_text())
            
            # Update timestamps
            config['updated_at'] = datetime.now().isoformat()
            if not config.get('created_at'):
                config['created_at'] = config['updated_at']
            
            # Write new config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, sort_keys=True)
                
            # Set restrictive permissions
            os.chmod(self.config_file, 0o600)
            logger.info("Configuration saved successfully")
            
        except PermissionError as e:
            logger.error(f"Permission denied saving config: {e}")
            raise
        except OSError as e:
            logger.error(f"OS error saving config: {e}")
            raise
    
    def _secure_store_token(self, token: str, service: str = 'github') -> None:
        """
        Securely store authentication token.
        
        Args:
            token: Authentication token to store
            service: Service name for token identification
            
        Raises:
            ValueError: If token is invalid
            PermissionError: If unable to write token file
        """
        if not token or len(token) > MAX_TOKEN_LENGTH:
            raise ValueError("Invalid token length")
        
        try:
            # Create token storage structure
            token_data = {
                service: {
                    'token': token,
                    'created_at': datetime.now().isoformat(),
                    'last_used': None
                }
            }
            
            # Write token file with restrictive permissions
            with open(self.token_file, 'w', encoding='utf-8') as f:
                json.dump(token_data, f, indent=2)
            os.chmod(self.token_file, 0o600)
            
            logger.info(f"Token for {service} stored securely")
            
        except PermissionError as e:
            logger.error(f"Permission denied storing token: {e}")
            raise
    
    def _load_token(self, service: str = 'github') -> Optional[str]:
        """
        Load stored authentication token.
        
        Args:
            service: Service name for token identification
            
        Returns:
            Token string if found, None otherwise
        """
        try:
            if not self.token_file.exists():
                return None
            
            with open(self.token_file, 'r', encoding='utf-8') as f:
                token_data = json.load(f)
                
            return token_data.get(service, {}).get('token')
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error loading token: {e}")
            return None
    
    def init_config(self, project_root: Optional[str] = None, 
                   github_token: Optional[str] = None) -> bool:
        """
        Initialize configuration with user-provided values.
        
        Args:
            project_root: Path to project root directory
            github_token: GitHub personal access token
            
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            config = self._load_config()
            
            if project_root:
                project_path = Path(project_root).resolve()
                if not project_path.exists():
                    logger.error(f"Project root does not exist: {project_root}")
                    return False
                config['project_root'] = str(project_path)
            
            if github_token:
                self._secure_store_token(github_token)
                config['github_token'] = github_token
            
            self._save_config(config)
            logger.info("Configuration initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Configuration initialization failed: {e}")
            return False
    
    def show_config(self) -> None:
        """Display current configuration without sensitive data."""
        try:
            config = self._load_config()
            
            # Mask sensitive information
            display_config = config.copy()
            if display_config.get('github_token'):
                display_config['github_token'] = '***masked***'
            
            print("\nCurrent Configuration:")
            print("-" * 40)
            for key, value in display_config.items():
                print(f"{key}: {value}")
            print("-" * 40)
            
        except Exception as e:
            logger.error(f"Error displaying configuration: {e}")
            print(f"Error: {e}")
    
    def set_config(self, key: str, value: str) -> bool:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key to set
            value: Value to assign
            
        Returns:
            True if successful, False otherwise
        """
        try:
            config = self._load_config()
            
            # Validate key
            if key not in DEFAULT_CONFIG:
                logger.warning(f"Unknown configuration key: {key}")
                return False
            
            # Handle special cases
            if key == 'project_root':
                path = Path(value).resolve()
                if not path.exists():
                    logger.error(f"Path does not exist: {value}")
                    return False
                value = str(path)
            
            config[key] = value
            self._save_config(config)
            logger.info(f"Configuration updated: {key} = {value}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting configuration: {e}")
            return False
    
    def validate_setup(self) -> Dict[str, bool]:
        """
        Validate current setup and return status report.
        
        Returns:
            Dictionary with validation results
        """
        results = {
            'config_dir_exists': False,
            'config_file_valid': False,
            'token_file_secure': False,
            'project_root_valid': False,
            'github_token_valid': False
        }
        
        try:
            # Check config directory
            results['config_dir_exists'] = self.config_dir.exists()
            
            # Check config file
            if self.config_file.exists():
                try:
                    config = self._load_config()
                    results['config_file_valid'] = True
                    
                    # Check project root
                    if config.get('project_root'):
                        project_path = Path(config['project_root'])
                        results['project_root_valid'] = project_path.exists()
                    
                    # Check GitHub token
                    token = self._load_token()
                    results['github_token_valid'] = bool(token)
                    
                except Exception:
                    pass
            
            # Check token file permissions
            if self.token_file.exists():
                stat = self.token_file.stat()
                results['token_file_secure'] = bool(stat.st_mode & 0o600)
            
            return results
            
        except Exception as e:
            logger.error(f"Error validating setup: {e}")
            return results
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser for CLI commands."""
        parser = argparse.ArgumentParser(
            prog='autoproject',
            description='AutoProjectManagement CLI - Project configuration and management',
            epilog='Use "autoproject <command> --help" for command-specific help'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Init command
        init_parser = subparsers.add_parser('init', help='Initialize configuration')
        init_parser.add_argument('--project-root', help='Project root directory')
        init_parser.add_argument('--github-token', help='GitHub personal access token')
        
        # Config command
        config_parser = subparsers.add_parser('config', help='Manage configuration')
        config_subparsers = config_parser.add_subparsers(dest='config_action')
        
        config_subparsers.add_parser('show', help='Show current configuration')
        
        set_parser = config_subparsers.add_parser('set', help='Set configuration value')
        set_parser.add_argument('key', help='Configuration key')
        set_parser.add_argument('value', help='Configuration value')
        
        # Validate command
        validate_parser = subparsers.add_parser('validate', help='Validate current setup')
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Main entry point for CLI commands.
        
        Args:
            args: Command line arguments (defaults to sys.argv[1:])
            
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            parser = self.create_parser()
            parsed_args = parser.parse_args(args)
            
            if not parsed_args.command:
                parser.print_help()
                return 1
            
            if parsed_args.command == 'init':
                success = self.init_config(
                    project_root=getattr(parsed_args, 'project_root', None),
                    github_token=getattr(parsed_args, 'github_token', None)
                )
                return 0 if success else 1
            
            elif parsed_args.command == 'config':
                if parsed_args.config_action == 'show':
                    self.show_config()
                    return 0
                elif parsed_args.config_action == 'set':
                    success = self.set_config(parsed_args.key, parsed_args.value)
                    return 0 if success else 1
            
            elif parsed_args.command == 'validate':
                results = self.validate_setup()
                print("\nSetup Validation Results:")
                print("-" * 30)
                for check, result in results.items():
                    status = "✅ PASS" if result else "❌ FAIL"
                    print(f"{check}: {status}")
                
                all_passed = all(results.values())
                return 0 if all_passed else 1
            
            else:
                logger.error(f"Unknown command: {parsed_args.command}")
                return 1
                
        except KeyboardInterrupt:
            logger.info("Operation cancelled by user")
            return 130
        except Exception as e:
            logger.error(f"CLI error: {e}")
            return 1


def main():
    """Entry point for CLI script."""
    cli = CLICommands()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
