"""
GitHub Project Manager for AutoProjectManagement
Purpose: Manage GitHub projects with CLI and programmatic interfaces
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Provides functionality to create GitHub projects, manage configurations, and synchronize project data from JSON templates.
"""

import argparse
import json
import logging
import os
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
GITHUB_API_BASE_URL = "https://api.github.com"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
CONFIG_FILE = ".github_project_config.json"

@dataclass
class GitHubProjectConfig:
    """Configuration for GitHub project creation."""
    project_name: str
    description: str
    github_username: str
    github_token: Optional[str] = None
    organization: Optional[str] = None
    private: bool = True
    auto_init: bool = True
    gitignore_template: Optional[str] = None
    license_template: Optional[str] = None

@dataclass
class ProjectReport:
    """Report structure for project creation results."""
    project_name: str
    github_username: str
    status: str
    url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: Optional[str] = None
    repository_id: Optional[int] = None

class GitHubAPIError(Exception):
    """Custom exception for GitHub API related errors."""
    pass

class GitHubProjectManager:
    """
    A comprehensive manager for GitHub projects with CLI and programmatic interfaces.
    
    This class provides functionality to create GitHub projects, manage configurations,
    and synchronize project data from JSON templates. It includes proper error handling,
    logging, and supports both interactive and automated workflows.
    
    Attributes:
        github_token (str): GitHub personal access token for authentication
        session (requests.Session): HTTP session for API calls
        config (Dict[str, Any]): Configuration dictionary loaded from file
    """
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the GitHub Project Manager.
        
        Args:
            github_token: GitHub personal access token. If not provided, will attempt
                         to load from environment variable GITHUB_TOKEN.
                         
        Raises:
            GitHubAPIError: If no GitHub token is available
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            raise GitHubAPIError(
                "GitHub token is required. Set GITHUB_TOKEN environment variable "
class GitHubAPIError(Exception):
    """Custom exception for GitHub API related errors."""
    pass

class GitHubProjectManager:
    """
    A comprehensive manager for GitHub projects with CLI and programmatic interfaces.
    
    This class provides functionality to create GitHub projects, manage configurations,
    and synchronize project data from JSON templates. It includes proper error handling,
    logging, and supports both interactive and automated workflows.
    
    Attributes:
        github_token (str): GitHub personal access token for authentication
        session (requests.Session): HTTP session for API calls
        config (Dict[str, Any]): Configuration dictionary loaded from file
        
    Example:
        >>> manager = GitHubProjectManager(github_token="ghp_xxx")
        >>> config = GitHubProjectConfig(
        ...     project_name="my-awesome-project",
        ...     description="A new awesome project",
        ...     github_username="myusername"
        ... )
        >>> report = manager.create_project(config)
        >>> print(f"Project created at: {report.url}")
    """
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the GitHub Project Manager.
        
        Args:
            github_token: GitHub personal access token. If not provided, will attempt
                         to load from environment variable GITHUB_TOKEN.
                         
        Raises:
            GitHubAPIError: If no GitHub token is available
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            raise GitHubAPIError(
                "GitHub token is required. Set GITHUB_TOKEN environment variable "
                "or pass token to constructor."
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHubProjectManager/1.0.0'
        })
        
        self.config = self._load_config()
        logger.info("GitHub Project Manager initialized successfully")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from local config file."""
        config_path = Path(CONFIG_FILE)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load config file: {e}")
        return {}
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to local config file."""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info("Configuration saved successfully")
        except IOError as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def _make_api_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make authenticated API request to GitHub.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            data: Request payload for POST/PUT requests
            params: Query parameters
            
        Returns:
            Dict containing the API response
            
        Raises:
            GitHubAPIError: For API-related errors
        """
        url = f"{GITHUB_API_BASE_URL}/{endpoint.lstrip('/')}"
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    timeout=DEFAULT_TIMEOUT
                )
                
                if response.status_code == 401:
                    raise GitHubAPIError("Invalid GitHub token")
                elif response.status_code == 403:
                    raise GitHubAPIError("Insufficient permissions or rate limit exceeded")
                elif response.status_code == 404:
                    raise GitHubAPIError("Resource not found")
                
                response.raise_for_status()
                return response.json() if response.content else {}
                
            except (ConnectionError, Timeout) as e:
                if attempt == MAX_RETRIES - 1:
                    raise GitHubAPIError(f"Network error after {MAX_RETRIES} attempts: {e}")
                logger.warning(f"Retry attempt {attempt + 1} for {url}")
                
            except HTTPError as e:
                error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
                raise GitHubAPIError(error_msg)
    
    def create_project(self, config: GitHubProjectConfig) -> ProjectReport:
        """
        Create a new GitHub repository project.
        
        Args:
            config: GitHubProjectConfig instance with project details
            
        Returns:
            ProjectReport with creation results
            
        Raises:
            GitHubAPIError: If project creation fails
        """
        logger.info(f"Creating GitHub project: {config.project_name}")
        
        try:
            # Prepare repository data
            repo_data = {
                "name": config.project_name,
                "description": config.description,
                "private": config.private,
                "auto_init": config.auto_init
            }
            
            if config.gitignore_template:
                repo_data["gitignore_template"] = config.gitignore_template
            
            if config.license_template:
                repo_data["license_template"] = config.license_template
            
            # Determine the endpoint
            if config.organization:
                endpoint = f"orgs/{config.organization}/repos"
            else:
                endpoint = f"user/repos"
            
            # Create repository
            response = self._make_api_request("POST", endpoint, data=repo_data)
            
            return ProjectReport(
                project_name=config.project_name,
                github_username=config.github_username,
                status="created",
                url=response.get("html_url"),
                created_at=response.get("created_at"),
                repository_id=response.get("id")
            )
            
        except GitHubAPIError as e:
            logger.error(f"Failed to create project {config.project_name}: {e}")
            return ProjectReport(
                project_name=config.project_name,
                github_username=config.github_username,
                status="failed",
                error_message=str(e)
            )
    
    def create_project_from_json(self, json_file: str, github_username: str) -> ProjectReport:
        """
        Create a GitHub project from JSON configuration file.
        
        Args:
            json_file: Path to JSON file containing project configuration
            github_username: GitHub username for the project
            
        Returns:
            ProjectReport with creation results
            
        Raises:
            GitHubAPIError: If JSON file is invalid or project creation fails
            FileNotFoundError: If JSON file doesn't exist
        """
        logger.info(f"Creating project from JSON file: {json_file}")
        
        try:
            with open(json_file, 'r') as f:
                project_config = json.load(f)
            
            # Validate required fields
            required_fields = ["project_name", "description"]
            for field in required_fields:
                if field not in project_config:
                    raise GitHubAPIError(f"Missing required field: {field}")
            
            config = GitHubProjectConfig(
                project_name=project_config["project_name"],
                description=project_config["description"],
                github_username=github_username,
                private=project_config.get("private", True),
                auto_init=project_config.get("auto_init", True),
                gitignore_template=project_config.get("gitignore_template"),
                license_template=project_config.get("license_template")
            )
            
            return self.create_project(config)
            
        except (json.JSONDecodeError, IOError) as e:
            raise GitHubAPIError(f"Failed to read JSON file: {e}")
    
    def list_user_repositories(self, username: str) -> List[Dict[str, Any]]:
        """
        List all repositories for a given user.
        
        Args:
            username: GitHub username
            
        Returns:
            List of repository dictionaries
            
        Raises:
            GitHubAPIError: If API request fails
        """
        logger.info(f"Listing repositories for user: {username}")
        
        try:
            response = self._make_api_request("GET", f"users/{username}/repos")
            return response
        except GitHubAPIError as e:
            logger.error(f"Failed to list repositories: {e}")
            raise
    
    def delete_project(self, owner: str, repo_name: str) -> bool:
        """
        Delete a GitHub repository.
        
        Args:
            owner: Repository owner (username or organization)
            repo_name: Repository name
            
        Returns:
            True if deletion was successful
            
        Raises:
            GitHubAPIError: If deletion fails
        """
        logger.warning(f"Deleting repository: {owner}/{repo_name}")
        
        try:
            self._make_api_request("DELETE", f"repos/{owner}/{repo_name}")
            logger.info(f"Successfully deleted repository: {owner}/{repo_name}")
            return True
        except GitHubAPIError as e:
            logger.error(f"Failed to delete repository: {e}")
            return False


class GitHubProjectCLI:
    """
    Command-line interface for GitHub Project Manager.
    
    Provides a user-friendly CLI for creating and managing GitHub projects
    with support for both interactive and batch operations.
    """
    
    def __init__(self):
        """Initialize CLI with argument parser."""
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser."""
        parser = argparse.ArgumentParser(
            description="GitHub Project Manager CLI",
            epilog="Examples:\n"
                   "  github-project create --name my-project --desc 'My awesome project'\n"
                   "  github-project create-from-json config.json --username myuser\n"
                   "  github-project list --username myuser",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Create project command
        create_parser = subparsers.add_parser('create', help='Create a new GitHub project')
        create_parser.add_argument('--name', required=True, help='Project name')
        create_parser.add_argument('--desc', required=True, help='Project description')
        create_parser.add_argument('--username', required=True, help='GitHub username')
        create_parser.add_argument('--org', help='Organization name (optional)')
        create_parser.add_argument('--public', action='store_true', help='Make repository public')
        create_parser.add_argument('--no-init', action='store_true', help='Skip README initialization')
        create_parser.add_argument('--gitignore', help='Gitignore template (e.g., Python, Node)')
        create_parser.add_argument('--license', help='License template (e.g., MIT, Apache-2.0)')
        
        # Create from JSON command
        create_json_parser = subparsers.add_parser('create-from-json', help='Create project from JSON config')
        create_json_parser.add_argument('json_file', help='JSON configuration file')
        create_json_parser.add_argument('--username', required=True, help='GitHub username')
        
        # List repositories command
        list_parser = subparsers.add_parser('list', help='List user repositories')
        list_parser.add_argument('--username', required=True, help='GitHub username')
        
        # Delete repository command
        delete_parser = subparsers.add_parser('delete', help='Delete a repository')
        delete_parser.add_argument('--owner', required=True, help='Repository owner')
        delete_parser.add_argument('--repo', required=True, help='Repository name')
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Run the CLI with provided arguments.
        
        Args:
            args: Command line arguments (defaults to sys.argv[1:])
            
        Returns:
            Exit code (0 for success, 1 for error)
        """
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return 1
        
        try:
            manager = GitHubProjectManager()
            
            if parsed_args.command == 'create':
                config = GitHubProjectConfig(
                    project_name=parsed_args.name,
                    description=parsed_args.desc,
                    github_username=parsed_args.username,
                    organization=parsed_args.org,
                    private=not parsed_args.public,
                    auto_init=not parsed_args.no_init,
                    gitignore_template=parsed_args.gitignore,
                    license_template=parsed_args.license
                )
                report = manager.create_project(config)
                
            elif parsed_args.command == 'create-from-json':
                report = manager.create_project_from_json(
                    parsed_args.json_file,
                    parsed_args.username
                )
                
            elif parsed_args.command == 'list':
                repos = manager.list_user_repositories(parsed_args.username)
                print(json.dumps(repos, indent=2))
                return 0
                
            elif parsed_args.command == 'delete':
                success = manager.delete_project(parsed_args.owner, parsed_args.repo)
                if success:
                    print("Repository deleted successfully")
                    return 0
                else:
                    print("Failed to delete repository")
                    return 1
            
            else:
                print(f"Unknown command: {parsed_args.command}")
                return 1
            
            # Print report for create operations
            if 'report' in locals():
                print(json.dumps({
                    "project_name": report.project_name,
                    "status": report.status,
                    "url": report.url,
                    "error": report.error_message
                }, indent=2))
                
                return 0 if report.status == "created" else 1
                
        except GitHubAPIError as e:
            logger.error(f"GitHub API Error: {e}")
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"Error: {e}", file=sys.stderr)
            return 1


def main():
    """Main entry point for the CLI."""
    cli = GitHubProjectCLI()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
