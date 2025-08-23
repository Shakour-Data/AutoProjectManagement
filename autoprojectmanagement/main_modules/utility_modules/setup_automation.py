import os
import sys
from typing import Dict, Any
from .github_actions_automation import GitHubActionsAutomation

class SetupAutomation:
    def __init__(self, project_root: str = None):
        self.project_root = project_root or os.getcwd()
        self.github_actions = GitHubActionsAutomation(self.project_root)
        
    def get_standard_response(self, question):
        # Provide standard responses for common setup questions
        standard_responses = {
            "What is the git flow used in this project?": "main",
            "What naming conventions should be followed?": "Use lowercase with hyphens for branches and snake_case for files.",
            "Does this project support GitHub Actions?": "Yes, full GitHub Actions automation is included with comprehensive CI/CD, security scanning, and automated workflows.",
            "What GitHub Actions workflows are included?": "CI/CD, security scanning, dependency updates, release automation, stale issue management, greetings, labeling, and more.",
            "Is GitHub Actions setup automatic?": "Yes, complete GitHub Actions setup is automated with zero-touch configuration."
        }
        
        # Ensure question is a string
        if not isinstance(question, str):
            return "No standard response available."
            
        return standard_responses.get(question, "No standard response available.")

    def setup_github_actions(self, project_config: Dict[str, Any] = None) -> bool:
        """
        راه‌اندازی کامل GitHub Actions برای پروژه
        
        Args:
            project_config: تنظیمات پروژه برای GitHub Actions
            
        Returns:
            bool: موفقیت عملیات
        """
        if project_config is None:
            project_config = self._get_default_project_config()
            
        print("🔧 Setting up complete GitHub Actions automation...")
        
        success = self.github_actions.create_complete_github_actions_setup(project_config)
        
        if success:
            summary = self.github_actions.get_github_actions_summary()
            print(f"✅ GitHub Actions setup completed successfully!")
            print(f"📊 Created {summary['total_workflows']} workflows")
            print(f"🎯 Workflows: {', '.join(summary['workflows'])}")
            print(f"⚙️  Custom actions: {summary['custom_actions']}")
            print(f"📋 Issue templates: {summary['issue_templates']}")
            print(f"📝 PR templates: {summary['pr_templates']}")
        else:
            print("❌ Failed to setup GitHub Actions")
            
        return success
    
    def _get_default_project_config(self) -> Dict[str, Any]:
        """دریافت تنظیمات پیش‌فرض پروژه برای GitHub Actions"""
        return {
            'project_name': 'Auto Managed Project',
            'description': 'Project managed by AutoProjectManagement package',
            'python_versions': ['3.8', '3.9', '3.10', '3.11', '3.12'],
            'enable_docker': True,
            'enable_security_scan': True,
            'enable_dependency_updates': True,
            'enable_release_automation': True,
            'enable_stale_management': True,
            'enable_greetings': True,
            'enable_labeling': True
        }
    
    def run_full_setup(self, project_config: Dict[str, Any] = None):
        """اجرای کامل راه‌اندازی پروژه با GitHub Actions"""
        print("🚀 Starting complete project setup with GitHub Actions...")
        
        # راه‌اندازی GitHub Actions
        github_success = self.setup_github_actions(project_config)
        
        # ایجاد فایل README برای GitHub Actions
        self._create_github_actions_readme()
        
        # ایجاد فایل راهنما
        self._create_github_actions_guide()
        
        print("🎉 Complete setup finished!")
        return github_success
    
    def _create_github_actions_readme(self):
        """ایجاد README برای GitHub Actions"""
        readme_content = """# GitHub Actions Automation

This project includes comprehensive GitHub Actions automation powered by AutoProjectManagement package.

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

## 🔧 Configuration

All workflows are automatically configured and require no manual setup. 
Environment variables and secrets are automatically managed.

## 📊 Monitoring

- **Codecov** integration for coverage reports
- **Security alerts** via GitHub Security tab
- **Performance monitoring** via GitHub Insights
"""
        
        with open(os.path.join(self.project_root, 'GITHUB_ACTIONS.md'), 'w') as f:
            f.write(readme_content)
    
    def _create_github_actions_guide(self):
        """ایجاد راهنمای استفاده از GitHub Actions"""
        guide_content = """# GitHub Actions Usage Guide

## Quick Start
1. Push code to any branch
2. GitHub Actions will automatically:
   - Run tests
   - Check code quality
   - Scan for security issues
   - Update dependencies
   - Deploy releases

## Available Commands
- **Manual trigger**: Go to Actions tab → Select workflow → Run workflow
- **Skip CI**: Add `[skip ci]` to commit message
- **Force deployment**: Create a release tag

## Secrets Required
- `PYPI_API_TOKEN`: For PyPI deployment
- `DOCKERHUB_USERNAME`: For Docker Hub
- `DOCKERHUB_TOKEN`: For Docker Hub
- `CODECOV_TOKEN`: For coverage reports

## Customization
Edit `.github/workflows/` files to customize behavior.
"""
        
        with open(os.path.join(self.project_root, 'GITHUB_ACTIONS_GUIDE.md'), 'w') as f:
            f.write(guide_content)

    def run(self):
        """اجرای راه‌اندازی خودکار با GitHub Actions"""
        print("SetupAutomation: Starting complete automation setup...")
        return self.run_full_setup()
