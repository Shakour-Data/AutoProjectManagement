"""
path: autoprojectmanagement/main_modules/utility_modules/setup_automation.py
File: setup_automation.py
Purpose: Automated setup and configuration management for GitHub Actions and project initialization
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Provides comprehensive automation for setting up GitHub Actions workflows,
           project configuration, and standardized project initialization processes.
           Includes support for CI/CD pipelines, security scanning, and automated
           project documentation generation.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from autoprojectmanagement.main_modules.quality_commit_management.github_actions_automation import (
    GitHubActionsAutomation
)

# Constants
DEFAULT_PYTHON_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
MAX_LINE_LENGTH = 79
GITHUB_WORKFLOWS_DIR = '.github/workflows'
README_FILE = 'GITHUB_ACTIONS.md'
GUIDE_FILE = 'GITHUB_ACTIONS_GUIDE.md'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SetupAutomation:
    """
    Automated setup and configuration management for GitHub Actions and project initialization.
    
    This class provides comprehensive automation for setting up GitHub Actions workflows,
    project configuration, and standardized project initialization processes.
    
    Attributes:
        project_root: The root directory of the project
        github_actions: Instance of GitHubActionsAutomation for workflow management
        logger: Configured logger instance for logging activities
        
    Example:
        >>> setup = SetupAutomation('/path/to/project')
        >>> setup.run_full_setup()
        True
    """
    
    def __init__(self, project_root: Optional[str] = None) -> None:
        """
        Initialize SetupAutomation with project root directory.
        
        Args:
            project_root: Path to the project root directory.
                         If None, uses current working directory.
        
        Raises:
            ValueError: If project_root is not a valid directory path
        """
        if project_root is None:
            self.project_root = Path.cwd()
        else:
            self.project_root = Path(project_root)
            
        if not self.project_root.exists():
            raise ValueError(f"Project root does not exist: {self.project_root}")
            
        self.github_actions = GitHubActionsAutomation(str(self.project_root))
        self.logger = logging.getLogger(__name__)
        
    def get_standard_response(self, question: str) -> str:
        """
        Provide standard responses for common setup questions.
        
        This method returns pre-defined responses for frequently asked questions
        about project setup, GitHub Actions, and development workflows.
        
        Args:
            question: The question to get a standard response for
            
        Returns:
            Standard response string, or "No standard response available"
            if the question is not recognized
            
        Examples:
            >>> setup = SetupAutomation()
            >>> setup.get_standard_response("What is the git flow used?")
            'main'
        """
        standard_responses: Dict[str, str] = {
            "What is the git flow used in this project?": "main",
            "What naming conventions should be followed?": (
                "Use lowercase with hyphens for branches and snake_case for files."
            ),
            "Does this project support GitHub Actions?": (
                "Yes, full GitHub Actions automation is included with comprehensive "
                "CI/CD, security scanning, and automated workflows."
            ),
            "What GitHub Actions workflows are included?": (
                "CI/CD, security scanning, dependency updates, release automation, "
                "stale issue management, greetings, labeling, and more."
            ),
            "Is GitHub Actions setup automatic?": (
                "Yes, complete GitHub Actions setup is automated with zero-touch "
                "configuration."
            )
        }
        
        # Ensure question is a string
        if not isinstance(question, str):
            self.logger.warning("Question must be a string")
            return "No standard response available."
            
        return standard_responses.get(
            question, 
            "No standard response available."
        )

    def setup_github_actions(
        self, 
        project_config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Set up complete GitHub Actions automation for the project.
        
        This method configures comprehensive GitHub Actions workflows including
        CI/CD pipelines, security scanning, dependency management, and automated
        releases based on the provided project configuration.
        
        Args:
            project_config: Configuration dictionary for GitHub Actions setup.
                           If None, uses default configuration.
        
        Returns:
            bool: True if setup completed successfully, False otherwise
            
        Raises:
            Exception: If GitHub Actions setup fails catastrophically
            
        Example:
            >>> config = {'project_name': 'My Project', 'enable_docker': True}
            >>> success = setup.setup_github_actions(config)
            >>> print(f"Setup successful: {success}")
            Setup successful: True
        """
        if project_config is None:
            project_config = self._get_default_project_config()
            
        self.logger.info("Starting GitHub Actions setup...")
        
        try:
            success = self.github_actions.create_complete_github_actions_setup(
                project_config
            )
            
            if success:
                summary = self.github_actions.get_github_actions_summary()
                self.logger.info("GitHub Actions setup completed successfully")
                self.logger.info(f"Created {summary['total_workflows']} workflows")
                self.logger.info(f"Workflows: {', '.join(summary['workflows'])}")
                self.logger.info(f"Custom actions: {summary['custom_actions']}")
                self.logger.info(f"Issue templates: {summary['issue_templates']}")
                self.logger.info(f"PR templates: {summary['pr_templates']}")
                
                # Create documentation files
                self._create_github_actions_readme()
                self._create_github_actions_guide()
                
            else:
                self.logger.error("Failed to setup GitHub Actions")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Error during GitHub Actions setup: {str(e)}")
            raise
    
    def _get_default_project_config(self) -> Dict[str, Any]:
        """
        Get default project configuration for GitHub Actions setup.
        
        Returns:
            Dictionary containing default configuration parameters for
            GitHub Actions automation setup.
            
        Configuration includes:
            - project_name: Display name for the project
            - description: Project description
            - python_versions: Supported Python versions
            - enable_docker: Whether to include Docker workflows
            - enable_security_scan: Whether to include security scanning
            - enable_dependency_updates: Whether to enable Dependabot
            - enable_release_automation: Whether to automate releases
            - enable_stale_management: Whether to manage stale issues
            - enable_greetings: Whether to greet new contributors
            - enable_labeling: Whether to auto-label PRs
        """
        return {
            'project_name': 'Auto Managed Project',
            'description': 'Project managed by AutoProjectManagement package',
            'python_versions': DEFAULT_PYTHON_VERSIONS,
            'enable_docker': True,
            'enable_security_scan': True,
            'enable_dependency_updates': True,
            'enable_release_automation': True,
            'enable_stale_management': True,
            'enable_greetings': True,
            'enable_labeling': True
        }
    
    def run_full_setup(
        self, 
        project_config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Execute complete project setup with GitHub Actions automation.
        
        This method performs a comprehensive project setup including:
        - GitHub Actions workflow configuration
        - Documentation generation
        - Project structure validation
        - Initial configuration setup
        
        Args:
            project_config: Configuration dictionary for the setup.
                           If None, uses default configuration.
        
        Returns:
            bool: True if complete setup was successful, False otherwise
            
        Example:
            >>> setup = SetupAutomation()
            >>> success = setup.run_full_setup()
            >>> print(f"Full setup completed: {success}")
            Full setup completed: True
        """
        self.logger.info("Starting complete project setup...")
        
        try:
            # Validate project structure
            self._validate_project_structure()
            
            # Setup GitHub Actions
            github_success = self.setup_github_actions(project_config)
            
            if not github_success:
                self.logger.error("GitHub Actions setup failed")
                return False
                
            # Create additional documentation
            self._create_project_documentation()
            
            self.logger.info("Complete setup finished successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during full setup: {str(e)}")
            return False
    
    def _validate_project_structure(self) -> None:
        """Validate that the project has required structure."""
        required_dirs = ['.github', 'tests', 'docs']
        
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                self.logger.warning(f"Missing directory: {dir_name}")
                
    def _create_github_actions_readme(self) -> None:
        """Create comprehensive README for GitHub Actions."""
        readme_content = """# GitHub Actions Automation

This project includes comprehensive GitHub Actions automation powered by 
AutoProjectManagement package.

## 🚀 Included Workflows

### CI/CD Pipeline (`ci.yml`)
- **Linting**: flake8, black, isort, mypy
- **Testing**: pytest with coverage
- **Security**: safety, bandit
- **Multi-platform**: Ubuntu, Windows, macOS
- **Multi-python**: 3.8, 3.9, 3.10, 3.11, 3.12

### CD Pipeline (`cd.yml`)
- **PyPI deployment** on releases
- **Docker image** building and pushing
- **Automated releases** with changelogs

### Security Workflows
- **CodeQL analysis** for security vulnerabilities
- **Trivy scanning** for container security
- **Dependency review** for PRs
- **Bandit** for Python security scanning

### Automation Workflows
- **Stale issue/PR management**
- **Greetings** for new contributors
- **Automatic labeling** based on file changes
- **Size labeling** for PRs
- **Dependency updates** via Dependabot

### Custom Actions
- **Progress updater**: Updates project progress based on commits
- **Auto-commit**: Automated commit management
- **Wiki sync**: Synchronizes documentation with wiki

## 🔧 Configuration

All workflows are automatically configured and require no manual setup.
Environment variables and secrets are automatically managed.

## 📊 Monitoring

- **Codecov** integration for coverage reports
- **Security alerts** via GitHub Security tab
- **Performance monitoring** via GitHub Insights
- **Project metrics** via GitHub Projects

## 🎯 Usage

### Manual Triggers
1. Go to Actions tab in GitHub
2. Select desired workflow
3. Click "Run workflow"
4. Select branch and options
5. Run workflow

### Skip CI
Add `[skip ci]` to commit message to skip CI/CD pipeline.

### Force Deployment
Create a release tag to trigger deployment workflows.

## 🔐 Required Secrets

| Secret | Purpose | Required |
|--------|---------|----------|
| `PYPI_API_TOKEN` | PyPI deployment | Optional |
| `DOCKERHUB_USERNAME` | Docker Hub | Optional |
| `DOCKERHUB_TOKEN` | Docker Hub | Optional |
| `CODECOV_TOKEN` | Coverage reports | Optional |
| `GH_TOKEN` | GitHub API access | Optional |

## 🛠️ Customization

Edit `.github/workflows/` files to customize behavior:
- Modify `ci.yml` for testing/linting changes
- Update `cd.yml` for deployment configuration
- Adjust `security.yml` for security scanning
- Configure `dependabot.yml` for dependency updates

## 📈 Performance

- **Average build time**: 3-5 minutes
- **Parallel jobs**: Up to 10 concurrent
- **Cache usage**: Optimized for Python packages
- **Resource usage**: Minimal for standard workflows

## 🐛 Troubleshooting

### Common Issues
1. **Workflow not triggering**: Check branch protection rules
2. **Permission denied**: Verify GitHub token permissions
3. **Build failures**: Check Python version compatibility
4. **Security alerts**: Review security scanning results

### Debug Mode
Enable debug logging by setting `ACTIONS_STEP_DEBUG` to `true` in repository secrets.

## 📞 Support

For issues with GitHub Actions:
1. Check [GitHub Actions documentation](https://docs.github.com/en/actions)
2. Review workflow logs in Actions tab
3. Create issue in project repository
4. Contact maintainers via GitHub discussions
"""
        
        readme_path = self.project_root / README_FILE
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            self.logger.info(f"Created {README_FILE}")
        except IOError as e:
            self.logger.error(f"Failed to create {README_FILE}: {str(e)}")
    
    def _create_github_actions_guide(self) -> None:
        """Create comprehensive usage guide for GitHub Actions."""
        guide_content = """# GitHub Actions Usage Guide

## 🚀 Quick Start

### 1. Initial Setup
```bash
# Clone repository
git clone <repository-url>
cd <project-name>

# Install dependencies
pip install -r requirements.txt

# Run tests locally
pytest tests/
```

### 2. First Push
```bash
# Create feature branch
git checkout -b feature/my-new-feature

# Make changes
git add .
git commit -m "Add new feature"

# Push to trigger CI
git push origin feature/my-new-feature
```

### 3. Monitor Results
- Check Actions tab in GitHub
- Review build logs
- Fix any issues
- Create pull request

## 🎯 Available Commands

### Manual Workflow Triggers
```bash
# Via GitHub UI
1. Go to Actions tab
2. Select workflow
3. Click "Run workflow"
4. Choose options
5. Run

# Via GitHub CLI
gh workflow run ci.yml --ref main
```

### Skip CI/CD
```bash
# Skip all workflows
git commit -m "Update docs [skip ci]"

# Skip specific workflows
git commit -m "Minor fix [skip actions]"
```

### Force Actions
```bash
# Create release (triggers CD)
git tag v1.0.0
git push origin v1.0.0

# Manual deployment
gh workflow run cd.yml --ref main
```

## 🔧 Configuration Files

### Workflow Configuration
- `.github/workflows/ci.yml` - CI pipeline
- `.github/workflows/cd.yml` - CD pipeline
- `.github/workflows/security.yml` - Security scanning
- `.github/dependabot.yml` - Dependency updates

### Templates
- `.github/pull_request_template.md` - PR template
- `.github/issue_template/` - Issue templates

## 📊 Monitoring & Alerts

### GitHub Security
- **Security tab**: Vulnerability alerts
- **Dependabot**: Dependency updates
- **Code scanning**: Security analysis

### Performance Metrics
- **Actions tab**: Build times
- **Insights tab**: Contribution graphs
- **Projects tab**: Progress tracking

## 🛠️ Advanced Usage

### Custom Workflows
```yaml
# .github/workflows/custom.yml
name: Custom Workflow
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  custom-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run custom script
        run: python scripts/custom.py
```

### Environment Variables
```yaml
env:
  PYTHON_VERSION: 3.9
  PROJECT_NAME: my-project
```

### Matrix Builds
```yaml
strategy:
  matrix:
    python-version: [3.8, 3.9, 3.10]
    os: [ubuntu-latest, windows-latest, macos-latest]
```

## 🔐 Security Best Practices

### Secrets Management
1. Never commit secrets to repository
2. Use GitHub Secrets for sensitive data
3. Rotate secrets regularly
4. Use least privilege principle

### Workflow Security
- Pin actions to specific versions
- Use official actions when possible
- Review third-party actions
- Enable security scanning

## 📈 Optimization Tips

### Speed Improvements
1. **Caching**: Use actions/cache for dependencies
2. **Parallel jobs**: Run tests in parallel
3. **Conditional runs**: Skip unnecessary workflows
4. **Smaller images**: Use alpine-based containers

### Resource Usage
- Monitor build minutes usage
- Optimize for cost efficiency
- Use self-hosted runners for heavy workloads

## 🐛 Troubleshooting Guide

### Build Failures
```bash
# Check logs
gh run view --log

# Re-run failed jobs
gh run rerun --failed

# Debug locally
act -j test
```

### Common Issues
| Issue | Solution |
|-------|----------|
| Permission denied | Check GitHub token permissions |
| Workflow not found | Verify file path and syntax |
| Slow builds | Check caching configuration |
| Test failures | Run tests locally first |

### Debug Mode
```bash
# Enable debug logging
export ACTIONS_STEP_DEBUG=true

# Run with debug
gh workflow run ci.yml --debug
```

## 📞 Getting Help

### Resources
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows)
- [Community Forum](https://github.community/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/github-actions)

### Support Channels
1. **GitHub Issues**: Report bugs
2. **Discussions**: Ask questions
3. **Documentation**: Read guides
4. **Community**: Join forums

## 🔄 Maintenance

### Regular Tasks
- [ ] Update action versions monthly
- [ ] Review security alerts weekly
- [ ] Update dependencies via Dependabot
- [ ] Monitor build performance
- [ ] Review and update workflows

### Version Updates
```bash
# Update actions
gh actions-upgrade

# Check for updates
gh actions-check-updates
```
"""
        
        guide_path = self.project_root / GUIDE_FILE
        try:
            with open(guide_path, 'w', encoding='utf-8') as f:
                f.write(guide_content)
            self.logger.info(f"Created {GUIDE_FILE}")
        except IOError as e:
            self.logger.error(f"Failed to create {GUIDE_FILE}: {str(e)}")
    
    def _create_project_documentation(self) -> None:
        """Create additional project documentation."""
        self.logger.info("Creating project documentation...")
        
        # Create docs directory if it doesn't exist
        docs_dir = self.project_root / 'docs'
        docs_dir.mkdir(exist_ok=True)
        
        # Create setup documentation
        setup_doc = docs_dir / 'setup_automation.md'
        setup_content = """# Setup Automation Documentation

## Overview
This project uses SetupAutomation for comprehensive GitHub Actions setup and project initialization.

## Features
- Automated GitHub Actions configuration
- Security scanning setup
- CI/CD pipeline creation
- Documentation generation
- Project structure validation

## Usage
```python
from autoprojectmanagement.main_modules.utility_modules.setup_automation import SetupAutomation

# Initialize
setup = SetupAutomation('/path/to/project')

# Run full setup
setup.run_full_setup()

# Or setup specific components
setup.setup_github_actions()
```

## Configuration
See `GITHUB_ACTIONS.md` for detailed GitHub Actions documentation.
"""
        
        try:
            with open(setup_doc, 'w', encoding='utf-8') as f:
                f.write(setup_content)
            self.logger.info("Created setup documentation")
        except IOError as e:
            self.logger.error(f"Failed to create setup documentation: {str(e)}")
    
    def run(self) -> bool:
        """
        Execute automated setup with GitHub Actions.
        
        This is the main entry point for automated setup. It performs
        complete project initialization including GitHub Actions setup,
        documentation creation, and project structure validation.
        
        Returns:
            bool: True if setup completed successfully, False otherwise
            
        Example:
            >>> setup = SetupAutomation()
            >>> success = setup.run()
            >>> print(f"Setup completed: {success}")
            Setup completed: True
        """
        self.logger.info("Starting automated setup...")
        
        try:
            return self.run_full_setup()
        except Exception as e:
            self.logger.error(f"Setup failed: {str(e)}")
            return False


def main() -> None:
    """Main entry point for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Setup automation for AutoProjectManagement'
    )
    parser.add_argument(
        '--project-root',
        type=str,
        help='Project root directory (default: current directory)'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file (JSON)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        setup = SetupAutomation(args.project_root)
        
        # Load config if provided
        config = None
        if args.config:
            import json
            with open(args.config, 'r') as f:
                config = json.load(f)
        
        success = setup.run_full_setup(config)
        
        if success:
            print("✅ Setup completed successfully!")
            sys.exit(0)
        else:
            print("❌ Setup failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
