#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AutoProjectManagement - Automated Project Management System
================================================================================
Module: github_actions_automation
File: github_actions_automation.py
Path: autoprojectmanagement/main_modules/quality_commit_management/github_actions_automation.py

Description:
    Github Actions Automation module

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
    >>> from autoprojectmanagement.main_modules.quality_commit_management.github_actions_automation import {main_class}
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
import yaml
from typing import Dict, List, Any
from datetime import datetime
import logging

class GitHubActionsAutomation:
    """
    کلاس جامع برای خودکارسازی کامل GitHub Actions در پروژه‌های مدیریت شده توسط این پکیج
    """
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.workflows_dir = os.path.join(project_root, '.github', 'workflows')
        self.actions_dir = os.path.join(project_root, '.github', 'actions')
        self.logger = logging.getLogger(__name__)
        
    def create_complete_github_actions_setup(self, project_config: Dict[str, Any]) -> bool:
        """
        ایجاد کامل‌ترین ساختار GitHub Actions برای پروژه
        """
        try:
            # ایجاد ساختار دایرکتوری
            self._create_github_structure()
            
            # ایجاد workflowهای اصلی
            self._create_ci_workflow(project_config)
            self._create_cd_workflow(project_config)
            self._create_security_workflow()
            self._create_dependency_workflow()
            self._create_release_workflow()
            self._create_stale_workflow()
            self._create_greetings_workflow()
            self._create_labeler_workflow()
            self._create_size_labeler_workflow()
            self._create_codeql_workflow()
            self._create_dependency_review_workflow()
            
            # ایجاد اکشن‌های سفارشی
            self._create_custom_actions()
            
            # ایجاد issue templates
            self._create_issue_templates()
            
            # ایجاد pull request templates
            self._create_pr_templates()
            
            # ایجاد فایلهای پیکربندی GitHub
            self._create_github_configs()
            
            return True
            
        except Exception as e:
            self.logger.error(f"خطا در ایجاد GitHub Actions: {str(e)}")
            return False
    
    def _create_github_structure(self):
        """ایجاد ساختار دایرکتوری GitHub"""
        os.makedirs(self.workflows_dir, exist_ok=True)
        os.makedirs(self.actions_dir, exist_ok=True)
        os.makedirs(os.path.join(self.project_root, '.github', 'ISSUE_TEMPLATE'), exist_ok=True)
        os.makedirs(os.path.join(self.project_root, '.github', 'pull_request_template.md'), exist_ok=True)
    
    def _create_ci_workflow(self, config: Dict[str, Any]):
        """ایجاد workflow CI/CD پیشرفته"""
        python_versions = config.get('python_versions', ['3.8', '3.9', '3.10', '3.11'])
        
        ci_content = {
            'name': 'CI/CD Pipeline',
            'on': {
                'push': {
                    'branches': ['main', 'develop', 'feature/*', 'hotfix/*']
                },
                'pull_request': {
                    'branches': ['main', 'develop']
                }
            },
            'jobs': {
                'lint': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'uses': 'actions/setup-python@v4', 'with': {'python-version': '3.9'}},
                        {'name': 'Install dependencies', 'run': 'pip install flake8 black isort mypy'},
                        {'name': 'Run flake8', 'run': 'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'},
                        {'name': 'Run black', 'run': 'black --check .'},
                        {'name': 'Run isort', 'run': 'isort --check-only .'},
                        {'name': 'Run mypy', 'run': 'mypy . --ignore-missing-imports'}
                    ]
                },
                'test': {
                    'runs-on': '${{ matrix.os }}',
                    'strategy': {
                        'matrix': {
                            'os': ['ubuntu-latest', 'windows-latest', 'macos-latest'],
                            'python-version': python_versions
                        }
                    },
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'uses': 'actions/setup-python@v4', 'with': {'python-version': '${{ matrix.python-version }}'}},
                        {'name': 'Install dependencies', 'run': 'pip install -r requirements.txt'},
                        {'name': 'Run tests', 'run': 'python -m pytest tests/ --cov=./ --cov-report=xml'},
                        {'name': 'Upload coverage', 'uses': 'codecov/codecov-action@v3'}
                    ]
                },
                'security': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'uses': 'actions/setup-python@v4', 'with': {'python-version': '3.9'}},
                        {'name': 'Install dependencies', 'run': 'pip install safety bandit'},
                        {'name': 'Run safety check', 'run': 'safety check'},
                        {'name': 'Run bandit', 'run': 'bandit -r . -f json -o bandit-report.json'}
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'ci.yml'), 'w') as f:
            yaml.dump(ci_content, f, default_flow_style=False, allow_unicode=True)
    
    def _create_cd_workflow(self, config: Dict[str, Any]):
        """ایجاد workflow deployment پیشرفته"""
        cd_content = {
            'name': 'CD Pipeline',
            'on': {
                'push': {'branches': ['main']},
                'release': {'types': ['published']}
            },
            'jobs': {
                'deploy': {
                    'runs-on': 'ubuntu-latest',
                    'if': "github.ref == 'refs/heads/main'",
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'uses': 'actions/setup-python@v4', 'with': {'python-version': '3.9'}},
                        {'name': 'Install dependencies', 'run': 'pip install -r requirements.txt'},
                        {'name': 'Build package', 'run': 'python setup.py sdist bdist_wheel'},
                        {'name': 'Upload to PyPI', 'uses': 'pypa/gh-action-pypi-publish@release/v1', 'with': {
                            'user': '__token__',
                            'password': '${{ secrets.PYPI_API_TOKEN }}'
                        }}
                    ]
                },
                'docker': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'name': 'Set up Docker Buildx', 'uses': 'docker/setup-buildx-action@v2'},
                        {'name': 'Login to DockerHub', 'uses': 'docker/login-action@v2', 'with': {
                            'username': '${{ secrets.DOCKERHUB_USERNAME }}',
                            'password': '${{ secrets.DOCKERHUB_TOKEN }}'
                        }},
                        {'name': 'Build and push', 'uses': 'docker/build-push-action@v4', 'with': {
                            'push': True,
                            'tags': 'latest,${{ github.sha }}'
                        }}
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'cd.yml'), 'w') as f:
            yaml.dump(cd_content, f, default_flow_style=False, allow_unicode=True)
    
    def _create_security_workflow(self):
        """ایجاد workflow امنیتی پیشرفته"""
        security_content = {
            'name': 'Security Scan',
            'on': {
                'push': {'branches': ['main', 'develop']},
                'pull_request': {'branches': ['main', 'develop']},
                'schedule': [{'cron': '0 2 * * 1'}]
            },
            'jobs': {
                'security': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'name': 'Run Trivy vulnerability scanner', 'uses': 'aquasecurity/trivy-action@master', 'with': {
                            'scan-type': 'fs',
                            'scan-ref': '.',
                            'format': 'sarif',
                            'output': 'trivy-results.sarif'
                        }},
                        {'name': 'Upload Trivy scan results', 'uses': 'github/codeql-action/upload-sarif@v2', 'with': {
                            'sarif_file': 'trivy-results.sarif'
                        }}
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'security.yml'), 'w') as f:
            yaml.dump(security_content, f, default_flow_style=False, allow_unicode=True)
    
    def _create_dependency_workflow(self):
        """ایجاد workflow بررسی وابستگی‌ها"""
        dep_content = {
            'name': 'Dependency Update',
            'on': {
                'schedule': [{'cron': '0 3 * * 1'}],
                'workflow_dispatch': {}
            },
            'jobs': {
                'update': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'uses': 'actions/setup-python@v4', 'with': {'python-version': '3.9'}},
                        {'name': 'Update dependencies', 'run': 'pip install -U pip-tools'},
                        {'name': 'Create Pull Request', 'uses': 'peter-evans/create-pull-request@v5', 'with': {
                            'token': '${{ secrets.GITHUB_TOKEN }}',
                            'commit-message': 'chore: update dependencies',
                            'title': 'Automated dependency updates',
                            'body': 'Automated dependency updates via GitHub Actions',
                            'branch': 'automated/dependency-updates'
                        }}
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'dependencies.yml'), 'w') as f:
            yaml.dump(dep_content, f, default_flow_style=False, allow_unicode=True)
    
    def _create_release_workflow(self):
        """ایجاد workflow انتشار خودکار"""
        release_content = {
            'name': 'Release Automation',
            'on': {
                'push': {'tags': ['v*']}
            },
            'jobs': {
                'release': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'name': 'Generate changelog', 'uses': 'conventional-changelog-action@v3', 'with': {
                            'github-token': '${{ secrets.GITHUB_TOKEN }}'
                        }},
                        {'name': 'Create Release', 'uses': 'actions/create-release@v1', 'with': {
                            'tag_name': '${{ github.ref }}',
                            'release_name': 'Release ${{ github.ref }}',
                            'body': '${{ steps.changelog.outputs.changelog }}',
                            'draft': False,
                            'prerelease': False
                        }}
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'release.yml'), 'w') as f:
            yaml.dump(release_content, f, default_flow_style=False, allow_unicode=True)
    
    def _create_stale_workflow(self):
        """ایجاد workflow مدیریت issueهای قدیمی"""
        stale_content = {
            'name': 'Close stale issues and PRs',
            'on': {
                'schedule': [{'cron': '0 0 * * *'}]
            },
            'jobs': {
                'stale': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/stale@v8', 'with': {
                            'repo-token': '${{ secrets.GITHUB_TOKEN }}',
                            'stale-issue-message': 'This issue is stale because it has been open 30 days with no activity.',
                            'close-issue-message': 'This issue was closed because it has been stalled for 5 days with no activity.',
                            'days-before-stale': 30,
                            'days-before-close': 5,
                            'stale-pr-message': 'This PR is stale because it has been open 30 days with no activity.',
                            'close-pr-message': 'This PR was closed because it has been stalled for 5 days with no activity.'
                        }}
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'stale.yml'), 'w') as f:
            yaml.dump(stale_content, f, default_flow_style=False, allow_unicode=True)
    
    def _create_greetings_workflow(self):
        """ایجاد workflow خوش‌آمدگویی به contributors جدید"""
        greetings_content = {
            'name': 'Greetings',
            'on': {
                'pull_request_target': {'types': ['opened']},
                'issues': {'types': ['opened']}
            },
            'jobs': {
                'greeting': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/first-interaction@v1', 'with': {
                            'repo-token': '${{ secrets.GITHUB_TOKEN }}',
                            'issue-message': 'Welcome! Thanks for opening your first issue. We appreciate your contribution!',
                            'pr-message': 'Welcome! Thanks for opening your first pull request. We appreciate your contribution!'
                        }}
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'greetings.yml'), 'w') as f:
            yaml.dump(greetings_content, f, default_flow_style=False, allow_unicode=True)
    
    def _create_labeler_workflow(self):
        """ایجاد workflow برچسب‌گذاری خودکار PRها"""
        labeler_content = {
            'name': 'Labeler',
            'on': {
                'pull_request_target': {'types': ['opened', 'synchronize']}
            },
            'jobs': {
                'label': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/labeler@v4', 'with': {
                            'repo-token': '${{ secrets.GITHUB_TOKEN }}',
                            'configuration-path': '.github/labeler.yml'
                        }}
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'labeler.yml'), 'w') as f:
            yaml.dump(labeler_content, f, default_flow_style=False, allow_unicode=True)
    
    def _create_size_labeler_workflow(self):
        """ایجاد workflow برچسب‌گذاری بر اساس اندازه PR"""
        size_content = {
            'name': 'Size Labeler',
            'on': {
                'pull_request': {'types': ['opened', 'synchronize']}
            },
            'jobs': {
                'size-label': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'codelytv/pr-size-labeler@v1', 'with': {
                            'GITHUB_TOKEN': '${{ secrets.GITHUB_TOKEN }}',
                            'xs_label': 'size/xs',
                            'xs_max_size': '10',
                            's_label': 'size/s',
                            's_max_size': '100',
                            'm_label': 'size/m',
                            'm_max_size': '500',
                            'l_label': 'size/l',
                            'l_max_size': '1000',
                            'xl_label': 'size/xl'
                        }}
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'size-labeler.yml'), 'w') as f:
            yaml.dump(size_content, f, default_flow_style=False, allow_unicode=True)
    
    def _create_codeql_workflow(self):
        """ایجاد workflow CodeQL برای امنیت کد"""
        codeql_content = {
            'name': 'CodeQL',
            'on': {
                'push': {'branches': ['main', 'develop']},
                'pull_request': {'branches': ['main', 'develop']},
                'schedule': [{'cron': '0 2 * * 1'}]
            },
            'jobs': {
                'analyze': {
                    'runs-on': 'ubuntu-latest',
                    'permissions': {
                        'actions': 'read',
                        'contents': 'read',
                        'security-events': 'write'
                    },
                    'strategy': {
                        'matrix': {'language': ['python']}
                    },
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'uses': 'github/codeql-action/init@v2', 'with': {'languages': '${{ matrix.language }}'}},
                        {'uses': 'github/codeql-action/analyze@v2'}
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'codeql.yml'), 'w') as f:
            yaml.dump(codeql_content, f, default_flow_style=False, allow_unicode=True)
    
    def _create_dependency_review_workflow(self):
        """ایجاد workflow بررسی وابستگی‌ها برای PRها"""
        dep_review_content = {
            'name': 'Dependency Review',
            'on': {
                'pull_request': {'branches': ['main', 'develop']}
            },
            'jobs': {
                'dependency-review': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v4'},
                        {'uses': 'actions/dependency-review-action@v3', 'with': {
                            'fail-on-severity': 'moderate'
                        }}
                    ]
                }
            }
        }
        
        with open(os.path.join(self.workflows_dir, 'dependency-review.yml'), 'w') as f:
            yaml.dump(dep_review_content, f, default_flow_style=False, allow_unicode=True)
    
    def _create_custom_actions(self):
        """ایجاد اکشن‌های سفارشی برای عملیات خاص پروژه"""
        # اکشن برای آپدیت خودکار progress
        progress_action_dir = os.path.join(self.actions_dir, 'update-progress')
        os.makedirs(progress_action_dir, exist_ok=True)
        
        progress_action = {
            'name': 'Update Project Progress',
            'description': 'Update project progress based on commits and changes',
            'runs': {
                'using': 'composite',
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {'name': 'Setup Python', 'uses': 'actions/setup-python@v4', 'with': {'python-version': '3.9'}},
                    {'name': 'Install dependencies', 'run': 'pip install -r requirements.txt', 'shell': 'bash'},
                    {'name': 'Update progress', 'run': 'python -m autoprojectmanagement.main_modules.progress_calculator_refactored', 'shell': 'bash'}
                ]
            }
        }
        
        with open(os.path.join(progress_action_dir, 'action.yml'), 'w') as f:
            yaml.dump(progress_action, f, default_flow_style=False, allow_unicode=True)
    
    def _create_issue_templates(self):
        """ایجاد templateهای issue برای GitHub"""
        bug_template = {
            'name': 'Bug Report',
            'description': 'Report a bug to help us improve',
            'title': '[BUG] ',
            'labels': ['bug'],
            'body': [
                {'type': 'markdown', 'attributes': {'value': '## Bug Description'}},
                {'type': 'textarea', 'id': 'description', 'attributes': {
                    'label': 'Description',
                    'description': 'A clear and concise description of the bug',
                    'placeholder': 'Describe the bug...'
                }},
                {'type': 'textarea', 'id': 'steps', 'attributes': {
                    'label': 'Steps to Reproduce',
                    'description': 'Steps to reproduce the behavior',
                    'placeholder': '1. Go to...\n2. Click on...'
                }},
                {'type': 'textarea', 'id': 'expected', 'attributes': {
                    'label': 'Expected Behavior',
                    'description': 'What you expected to happen',
                    'placeholder': 'Expected behavior...'
                }}
            ]
        }
        
        with open(os.path.join(self.project_root, '.github', 'ISSUE_TEMPLATE', 'bug_report.yml'), 'w') as f:
            yaml.dump(bug_template, f, default_flow_style=False, allow_unicode=True)
    
    def _create_pr_templates(self):
        """ایجاد template برای pull requests"""
        pr_template = """## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Documentation updated

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
"""
        
        with open(os.path.join(self.project_root, '.github', 'pull_request_template.md'), 'w') as f:
            f.write(pr_template)
    
    def _create_github_configs(self):
        """ایجاد فایلهای پیکربندی GitHub"""
        # Dependabot configuration
        dependabot_config = {
            'version': 2,
            'updates': [
                {
                    'package-ecosystem': 'pip',
                    'directory': '/',
                    'schedule': {'interval': 'weekly'},
                    'open-pull-requests-limit': 10
                },
                {
                    'package-ecosystem': 'github-actions',
                    'directory': '/',
                    'schedule': {'interval': 'weekly'}
                }
            ]
        }
        
        with open(os.path.join(self.project_root, '.github', 'dependabot.yml'), 'w') as f:
            yaml.dump(dependabot_config, f, default_flow_style=False, allow_unicode=True)
        
        # Labeler configuration
        labeler_config = {
            'bug': ['bug/*', 'fix/*'],
            'feature': ['feature/*', 'feat/*'],
            'documentation': ['docs/*', 'doc/*'],
            'refactor': ['refactor/*', 'cleanup/*'],
            'test': ['test/*', 'tests/*']
        }
        
        with open(os.path.join(self.project_root, '.github', 'labeler.yml'), 'w') as f:
            yaml.dump(labeler_config, f, default_flow_style=False, allow_unicode=True)
    
    def get_github_actions_summary(self) -> Dict[str, Any]:
        """دریافت خلاصه‌ای از GitHub Actions ایجاد شده"""
        workflows = [
            'ci.yml', 'cd.yml', 'security.yml', 'dependencies.yml',
            'release.yml', 'stale.yml', 'greetings.yml', 'labeler.yml',
            'size-labeler.yml', 'codeql.yml', 'dependency-review.yml'
        ]
        
        return {
            'total_workflows': len(workflows),
            'workflows': workflows,
            'custom_actions': 1,
            'issue_templates': 1,
            'pr_templates': 1,
            'config_files': ['dependabot.yml', 'labeler.yml']
        }
