#!/usr/bin/env python3
"""
Git Progress Updater Module - All 4 Phases Implementation
==========================================================

This module implements a comprehensive Git progress tracking system with:
- Phase 1: Basic Structure & Documentation
- Phase 2: Error Handling & Validation
- Phase 3: Performance & Security
- Phase 4: Testing & Monitoring

Author: AutoProjectManagement System
Version: 2.0.0
"""

import os
import json
import logging
import subprocess
import re
import hashlib
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Union
from pathlib import Path
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
import functools
import warnings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# PHASE 1: BASIC STRUCTURE & DOCUMENTATION
# ============================================================================

class GitProgressError(Exception):
    """Base exception for Git progress operations."""
    pass

class GitCommandError(GitProgressError):
    """Raised when Git command execution fails."""
    pass

class ValidationError(GitProgressError):
    """Raised when data validation fails."""
    pass

class ProgressFileError(GitProgressError):
    """Raised when progress file operations fail."""
    pass

class SecurityError(GitProgressError):
    """Raised when security validation fails."""
    pass

class ProgressStatus(Enum):
    """Enum for progress tracking status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class CommitInfo:
    """Data class for commit information."""
    hash: str
    message: str
    author: str
    email: str
    timestamp: int
    branch: str
    files: List[str]

@dataclass
class ProgressMetrics:
    """Data class for progress metrics."""
    total_commits: int
    completed_tasks: int
    total_tasks: int
    completion_percentage: float
    last_update: str

class GitProgressUpdater:
    """
    Git Progress Updater - Complete 4-Phase Implementation
    
    This class provides comprehensive Git progress tracking with:
    - Robust error handling and validation
    - Performance optimization and caching
    - Security measures and input sanitization
    - Comprehensive testing support
    - Monitoring and metrics collection
    
    Usage:
        updater = GitProgressUpdater('/path/to/repo')
        progress = updater.update_progress()
        summary = updater.get_progress_summary()
    """
    
    def __init__(self, 
                 repo_path: str,
                 progress_file: Optional[str] = None,
                 backup_dir: Optional[str] = None,
                 max_retries: int = 3,
                 timeout: int = 30,
                 enable_caching: bool = True,
                 enable_monitoring: bool = True):
        """
        Initialize GitProgressUpdater with comprehensive configuration.
        
        Args:
            repo_path: Path to Git repository
            progress_file: Custom progress file path (optional)
            backup_dir: Custom backup directory (optional)
            max_retries: Maximum retry attempts for operations
            timeout: Operation timeout in seconds
            enable_caching: Enable result caching for performance
            enable_monitoring: Enable metrics collection
            
        Raises:
            ValidationError: If configuration is invalid
        """
        self.repo_path = Path(repo_path).resolve()
        self.max_retries = max_retries
        self.timeout = timeout
        self.enable_caching = enable_caching
        self.enable_monitoring = enable_monitoring
        
        # ============================================================================
        # PHASE 2: ERROR HANDLING & VALIDATION
        # ============================================================================
        
        # Validate repository
        self._validate_repository()
        
        # Set up paths with validation
        self.progress_file = self._setup_progress_file(progress_file)
        self.backup_dir = self._setup_backup_dir(backup_dir)
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Thread safety
        self._lock = threading.RLock()
        self._cache = {}
        self._cache_lock = threading.Lock()
        
        # Monitoring
        if self.enable_monitoring:
            self._metrics = {
                'operations_count': 0,
                'errors_count': 0,
                'last_operation_time': 0,
                'total_operation_time': 0
            }
        
        logger.info(f"GitProgressUpdater initialized for {self.repo_path}")
    
    def _validate_repository(self) -> None:
        """Comprehensive repository validation."""
        if not self.repo_path.exists():
            raise ValidationError(f"Repository path does not exist: {self.repo_path}")
        
        if not self.repo_path.is_dir():
            raise ValidationError(f"Repository path is not a directory: {self.repo_path}")
        
        git_dir = self.repo_path / '.git'
        if not git_dir.exists():
            raise ValidationError(f"Not a Git repository: {self.repo_path}")
        
        # Check Git availability
        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=str(self.repo_path)
            )
            if result.returncode != 0:
                raise ValidationError("Git is not available")
        except subprocess.TimeoutExpired:
            raise ValidationError("Git command timeout")
        except FileNotFoundError:
            raise ValidationError("Git not found in PATH")
    
    def _setup_progress_file(self, progress_file: Optional[str]) -> Path:
        """Setup and validate progress file path."""
        if progress_file:
            file_path = Path(progress_file).resolve()
            if not file_path.parent.exists():
                raise ValidationError(f"Progress file directory does not exist: {file_path.parent}")
            return file_path
        
        return self.repo_path / '.git' / 'progress.json'
    
    def _setup_backup_dir(self, backup_dir: Optional[str]) -> Path:
        """Setup and validate backup directory."""
        if backup_dir:
            dir_path = Path(backup_dir).resolve()
            return dir_path
        
        return self.repo_path / '.git' / 'progress_backups'
    
    def _ensure_directories(self) -> None:
        """Ensure all required directories exist with proper permissions."""
        try:
            self.progress_file.parent.mkdir(parents=True, exist_ok=True)
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Set secure permissions
            os.chmod(self.progress_file.parent, 0o755)
            os.chmod(self.backup_dir, 0o755)
            
        except Exception as e:
            raise ProgressFileError(f"Failed to create directories: {str(e)}")
    
    # ============================================================================
    # PHASE 3: PERFORMANCE & SECURITY
    # ============================================================================
    
    def _secure_execute(self, func):
        """Decorator for secure execution with retry logic."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(self.max_retries):
                try:
                    with self._lock:
                        return func(*args, **kwargs)
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise
                    logger.warning(f"Retry {attempt + 1}/{self.max_retries} for {func.__name__}: {str(e)}")
                    time.sleep(2 ** attempt)
            raise GitProgressError(f"Operation failed after {self.max_retries} attempts")
        return wrapper
    
    def _sanitize_input(self, data: str) -> str:
        """Sanitize input data to prevent injection attacks."""
        if not isinstance(data, str):
            return str(data)
        
        sanitized = re.sub(r'[^\w\s\-_\.@]', '', data)
        return sanitized.strip()
    
    def _hash_data(self, data: str) -> str:
        """Generate secure hash for data integrity."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @contextmanager
    def _timer(self, operation_name: str):
        """Context manager for timing operations."""
        start_time = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start_time
            if self.enable_monitoring:
                self._metrics['operations_count'] += 1
                self._metrics['total_operation_time'] += elapsed
                self._metrics['last_operation_time'] = elapsed
                logger.debug(f"Operation {operation_name} took {elapsed:.2f}s")
    
    def _cache_result(self, key: str, result: Any, ttl: int = 300):
        """Cache result with TTL."""
        if not self.enable_caching:
            return
        
        with self._cache_lock:
            self._cache[key] = {
                'result': result,
                'timestamp': time.time(),
                'ttl': ttl
            }
    
    def _get_cached_result(self, key: str) -> Optional[Any]:
        """Get cached result if valid."""
        if not self.enable_caching:
            return None
        
        with self._cache_lock:
            if key in self._cache:
                cached = self._cache[key]
                if time.time() - cached['timestamp'] < cached['ttl']:
                    return cached['result']
                else:
                    del self._cache[key]
        return None
    
    def _execute_git_command(self, command: List[str]) -> Tuple[str, str, int]:
        """Execute Git command with security and performance measures."""
        for attempt in range(self.max_retries):
            try:
                with self._timer('git_command'):
                    sanitized_command = [self._sanitize_input(arg) for arg in command]
                    
                    result = subprocess.run(
                        sanitized_command,
                        cwd=str(self.repo_path),
                        capture_output=True,
                        text=True,
                        timeout=self.timeout,
                        env={**os.environ, 'GIT_PAGER': 'cat'}
                    )
                    
                    return result.stdout, result.stderr, result.returncode
                    
            except subprocess.TimeoutExpired:
                if attempt == self.max_retries - 1:
                    raise GitCommandError(f"Git command timeout after {self.timeout}s")
                logger.warning(f"Retry {attempt + 1}/{self.max_retries} for git command: timeout")
                time.sleep(2 ** attempt)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise GitCommandError(f"Git command failed: {str(e)}")
                logger.warning(f"Retry {attempt + 1}/{self.max_retries} for git command: {str(e)}")
                time.sleep(2 ** attempt)
        
        raise GitCommandError(f"Git command failed after {self.max_retries} attempts")
    
    # ============================================================================
    # PHASE 4: TESTING & MONITORING
    # ============================================================================
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for monitoring."""
        if not self.enable_monitoring:
            return {}
        
        return {
            **self._metrics,
            'repository_path': str(self.repo_path),
            'progress_file': str(self.progress_file)
        }
    
    def health_check(self) -> Dict[str, bool]:
        """Perform health check of the system."""
        checks = {
            'repository_accessible': self.repo_path.exists(),
            'git_available': self._check_git_health(),
            'progress_file_writable': self._check_file_permissions(),
            'backup_dir_accessible': self.backup_dir.exists(),
            'monitoring_enabled': self.enable_monitoring
        }
        
        all_healthy = all(checks.values())
        checks['overall_health'] = all_healthy
        
        return checks
    
    def _check_git_health(self) -> bool:
        """Check Git health status."""
        try:
            stdout, _, code = self._execute_git_command(['git', 'status', '--porcelain'])
            return code == 0
        except:
            return False
    
    def _check_file_permissions(self) -> bool:
        """Check file permissions for progress operations."""
        try:
            test_file = self.progress_file.with_suffix('.test')
            test_file.touch()
            test_file.unlink()
            return True
        except:
            return False
    
    # Main functionality methods
    
    def get_current_commit_info(self) -> CommitInfo:
        """Get current commit information."""
        cache_key = f"commit_info_{self._hash_data(str(self.repo_path))}"
        cached = self._get_cached_result(cache_key)
        if cached:
            return cached
        
        stdout, _, _ = self._execute_git_command(['git', 'log', '-1', '--pretty=format:%H|%s|%an|%ae|%at'])
        stdout_branch, _, _ = self._execute_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        
        parts = stdout.strip().split('|')
        if len(parts) != 5:
            raise ValidationError("Invalid commit format")
        
        commit_info = CommitInfo(
            hash=parts[0],
            message=parts[1],
            author=parts[2],
            email=parts[3],
            timestamp=int(parts[4]),
            branch=stdout_branch.strip(),
            files=[]
        )
        
        self._cache_result(cache_key, commit_info)
        return commit_info
    
    def load_progress(self) -> Dict[str, Any]:
        """Load progress data with caching."""
        cache_key = f"progress_{self._hash_data(str(self.progress_file))}"
        cached = self._get_cached_result(cache_key)
        if cached:
            return cached
        
        if not self.progress_file.exists():
            progress = self._create_default_progress()
        else:
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                self._validate_progress_data(progress)
            except (json.JSONDecodeError, ValidationError):
                progress = self._create_default_progress()
        
        self._cache_result(cache_key, progress, ttl=60)
        return progress
    
    def _create_default_progress(self) -> Dict[str, Any]:
        """Create default progress structure."""
        return {
            'version': '2.0.0',
            'last_updated': datetime.now().isoformat(),
            'total_commits': 0,
            'commits': [],
            'branches': {},
            'metrics': {
                'average_commit_size': 0,
                'files_per_commit': 0,
                'commit_frequency': 0
            },
            'metadata': {
                'repository': str(self.repo_path),
                'created_at': datetime.now().isoformat(),
                'updater_version': '2.0.0'
            }
        }
    
    def _validate_progress_data(self, data: Dict[str, Any]) -> None:
        """Validate progress data structure."""
        required_keys = {'version', 'last_updated', 'total_commits', 'commits'}
        if not all(key in data for key in required_keys):
            raise ValidationError("Invalid progress data structure")
        
        if not isinstance(data.get('total_commits'), int) or data.get('total_commits') < 0:
            raise ValidationError("Invalid total_commits value")
    
    def update_progress(self) -> Dict[str, Any]:
        """Update progress with current commit information."""
        try:
            commit_info = self.get_current_commit_info()
            progress = self.load_progress()
            
            # Check for duplicate
            existing_hashes = {c['hash'] for c in progress['commits']}
            if commit_info.hash in existing_hashes:
                return progress
            
            # Add new commit
            commit_data = {
                'hash': commit_info.hash,
                'message': commit_info.message,
                'author': commit_info.author,
                'email': commit_info.email,
                'timestamp': commit_info.timestamp,
                'branch': commit_info.branch,
                'files': []
            }
            
            progress['commits'].append(commit_data)
            progress['total_commits'] = len(progress['commits'])
            progress['last_updated'] = datetime.now().isoformat()
            
            # Update branch tracking
            branch = commit_info.branch
            if branch not in progress['branches']:
                progress['branches'][branch] = {
                    'first_commit': commit_info.timestamp,
                    'last_commit': commit_info.timestamp,
                    'commit_count': 0
                }
            
            progress['branches'][branch]['last_commit'] = commit_info.timestamp
            progress['branches'][branch]['commit_count'] += 1
            
            self.save_progress(progress)
            return progress
            
        except Exception as e:
            if self.enable_monitoring:
                self._metrics['errors_count'] += 1
            raise GitProgressError(f"Failed to update progress: {str(e)}")
    
    def save_progress(self, progress: Dict[str, Any]) -> None:
        """Save progress data with atomic operations."""
        with self._lock:
            try:
                self._validate_progress_data(progress)
                
                # Create backup
                if self.progress_file.exists():
                    self._create_backup()
                
                # Atomic write
                temp_file = self.progress_file.with_suffix('.tmp')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(progress, f, indent=2, ensure_ascii=False)
                
                temp_file.replace(self.progress_file)
                
            except Exception as e:
                raise ProgressFileError(f"Failed to save progress: {str(e)}")
    
    def _create_backup(self) -> None:
        """Create timestamped backup of progress file."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f"progress_{timestamp}.json"
            
            import shutil
            shutil.copy2(self.progress_file, backup_file)
            
            # Cleanup old backups (keep last 10)
            backups = sorted(self.backup_dir.glob('progress_*.json'))
            for backup in backups[:-10]:
                backup.unlink()
                
        except Exception as e:
            logger.warning(f"Failed to create backup: {str(e)}")
    
    def get_progress_summary(self) -> ProgressMetrics:
        """Get progress summary for reporting."""
        progress = self.load_progress()
        
        total_tasks = len(progress['commits'])
        completed_tasks = sum(1 for c in progress['commits'] if c.get('completed', False))
        
        return ProgressMetrics(
            total_commits=progress['total_commits'],
            completed_tasks=completed_tasks,
            total_tasks=total_tasks,
            completion_percentage=(completed_tasks / max(total_tasks, 1)) * 100,
            last_update=progress['last_updated']
        )
    
    def reset_all_progress(self) -> bool:
        """Reset all progress data."""
        try:
            progress = self._create_default_progress()
            self.save_progress(progress)
            return True
        except Exception as e:
            logger.error(f"Failed to reset progress: {str(e)}")
            return False

# ============================================================================
# BACKWARD COMPATIBILITY - Legacy functions
# ============================================================================

def _get_global_git_progress_updater():
    """Get global instance for backward compatibility."""
    global _global_git_progress_updater
    if _global_git_progress_updater is None:
        _global_git_progress_updater = GitProgressUpdater(os.getcwd())
    return _global_git_progress_updater

def update_progress(commit_data: dict) -> bool:
    """Legacy function for backward compatibility."""
    updater = _get_global_git_progress_updater()
    return updater.update_progress_for_commit(commit_data)

def get_progress(commit_id: str) -> dict:
    """Legacy function for backward compatibility."""
    updater = _get_global_git_progress_updater()
    return updater.get_progress(commit_id)

def reset_progress(commit_id: str) -> bool:
    """Legacy function for backward compatibility."""
    updater = _get_global_git_progress_updater()
    return updater.reset_progress(commit_id)

# ============================================================================
# TESTING UTILITIES
# ============================================================================

class GitProgressTester:
    """Testing utilities for GitProgressUpdater."""
    
    @staticmethod
    def create_test_repo(tmp_path: str) -> str:
        """Create a test Git repository."""
        repo_path = Path(tmp_path) / "test_repo"
        repo_path.mkdir()
        
        # Initialize git repo
        subprocess.run(['git', 'init'], cwd=repo_path, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=repo_path, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=repo_path, check=True)
        
        # Create initial commit
        (repo_path / 'README.md').write_text('# Test Repository')
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=repo_path, check=True)
        
        return str(repo_path)
    
    @staticmethod
    def run_tests():
        """Run basic tests."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_path = GitProgressTester.create_test_repo(tmp_dir)
            updater = GitProgressUpdater(repo_path)
            
            # Test health check
            health = updater.health_check()
            print("Health check:", health)
            
            # Test progress update
            progress = updater.update_progress()
            print("Progress:", progress)
            
            # Test metrics
            metrics = updater.get_metrics()
            print("Metrics:", metrics)
            
            return all(health.values())

if __name__ == "__main__":
    # Run tests if executed directly
    GitProgressTester.run_tests()
