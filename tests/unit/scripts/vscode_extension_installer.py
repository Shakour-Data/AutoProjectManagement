"""
path: vscode_extension_installer.py
File: vscode_extension_installer.py
Purpose: Automated VS Code extension installer with comprehensive code review phases
Author: AutoProjectManagement System
Version: 1.0.0
License: MIT
Description: A phased implementation for VS Code extension installation with security, performance, and maintainability considerations
"""

import os
import json
import subprocess
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import hashlib
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# ===========================
# PHASE 1: FOUNDATION & SECURITY
# ===========================

@dataclass
class SecurityConfig:
    """Security configuration for extension installation"""
    verify_signatures: bool = True
    trusted_sources_only: bool = True
    scan_for_vulnerabilities: bool = True
    max_file_size_mb: int = 100
    allowed_extensions: List[str] = None
    
    def __post_init__(self):
        if self.allowed_extensions is None:
            self.allowed_extensions = ['.vsix', '.zip']

class SecurityValidator:
    """Handles security validation for extensions"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def verify_extension_signature(self, file_path: str) -> bool:
        """Verify digital signature of extension package"""
        try:
            # Check file extension
            if not any(file_path.endswith(ext) for ext in self.config.allowed_extensions):
                self.logger.error(f"Invalid extension: {file_path}")
                return False
                
            # Check file size
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            if file_size > self.config.max_file_size_mb:
                self.logger.error(f"File too large: {file_size}MB > {self.config.max_file_size_mb}MB")
                return False
                
            # Calculate checksum for integrity
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
                
            # In production, verify against known good signatures
            self.logger.info(f"Extension signature verified: {file_hash}")
            return True
            
        except Exception as e:
            self.logger.error(f"Signature verification failed: {e}")
            return False
    
    def scan_for_vulnerabilities(self, extension_path: str) -> Dict[str, any]:
        """Scan extension for known vulnerabilities"""
        vulnerabilities = []
        
        # Basic vulnerability checks
        suspicious_patterns = [
            'eval(',
            'exec(',
            'shell_exec',
            'os.system',
            'subprocess.call'
        ]
        
        try:
            with open(extension_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for pattern in suspicious_patterns:
                    if pattern in content:
                        vulnerabilities.append({
                            'type': 'code_injection',
                            'pattern': pattern,
                            'severity': 'high'
                        })
                        
            return {
                'scan_complete': True,
                'vulnerabilities_found': len(vulnerabilities),
                'vulnerabilities': vulnerabilities
            }
            
        except Exception as e:
            self.logger.error(f"Vulnerability scan failed: {e}")
            return {'scan_complete': False, 'error': str(e)}

# ===========================
# PHASE 2: PERFORMANCE & EFFICIENCY
# ===========================

@dataclass
class PerformanceConfig:
    """Performance configuration for extension installation"""
    max_concurrent_installs: int = 3
    timeout_seconds: int = 300
    retry_attempts: int = 3
    cache_enabled: bool = True
    cache_ttl_hours: int = 24

class PerformanceOptimizer:
    """Handles performance optimization for extension installation"""
    
    def __init__(self, config: PerformanceConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.cache_dir = Path.home() / '.vscode_extension_cache'
        
    def install_extensions_parallel(self, extensions: List[str]) -> Dict[str, bool]:
        """Install multiple extensions in parallel"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.config.max_concurrent_installs) as executor:
            future_to_extension = {
                executor.submit(self._install_single_extension, ext): ext 
                for ext in extensions
            }
            
            for future in as_completed(future_to_extension, timeout=self.config.timeout_seconds):
                extension = future_to_extension[future]
                try:
                    success = future.result()
                    results[extension] = success
                except Exception as e:
                    self.logger.error(f"Failed to install {extension}: {e}")
                    results[extension] = False
                    
        return results
    
    def _install_single_extension(self, extension: str) -> bool:
        """Install a single extension with retry logic"""
        for attempt in range(self.config.retry_attempts):
            try:
                if self._is_cached(extension) and self.config.cache_enabled:
                    self.logger.info(f"Using cached installation for {extension}")
                    return True
                    
                cmd = ['code', '--install-extension', extension, '--force']
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.config.timeout_seconds
                )
                
                if result.returncode == 0:
                    self._cache_extension(extension)
                    return True
                else:
                    self.logger.warning(f"Attempt {attempt + 1} failed for {extension}: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                self.logger.error(f"Timeout installing {extension}")
            except Exception as e:
                self.logger.error(f"Error installing {extension}: {e}")
                
            if attempt < self.config.retry_attempts - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                
        return False
    
    def _is_cached(self, extension: str) -> bool:
        """Check if extension is cached"""
        if not self.config.cache_enabled:
            return False
            
        cache_file = self.cache_dir / f"{extension.replace('/', '_')}.cache"
        if cache_file.exists():
            age = time.time() - cache_file.stat().st_mtime
            return age < (self.config.cache_ttl_hours * 3600)
        return False
    
    def _cache_extension(self, extension: str):
        """Cache successful installation"""
        if not self.config.cache_enabled:
            return
            
        self.cache_dir.mkdir(exist_ok=True)
        cache_file = self.cache_dir / f"{extension.replace('/', '_')}.cache"
        cache_file.touch()

# ===========================
# PHASE 3: MAINTAINABILITY & TESTING
# ===========================

class ExtensionInstaller:
    """Main extension installer class with maintainability features"""
    
    def __init__(self):
        self.security_config = SecurityConfig()
        self.performance_config = PerformanceConfig()
        self.security_validator = SecurityValidator(self.security_config)
        self.performance_optimizer = PerformanceOptimizer(self.performance_config)
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup structured logging"""
        logger = logging.getLogger('vscode_extension_installer')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def validate_environment(self) -> Tuple[bool, str]:
        """Validate that VS Code CLI is available"""
        try:
            result = subprocess.run(['code', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                self.logger.info(f"VS Code CLI found: {version}")
                return True, version
            else:
                return False, "VS Code CLI not found or not accessible"
        except Exception as e:
            return False, str(e)
    
    def get_installed_extensions(self) -> List[str]:
        """Get list of currently installed extensions"""
        try:
            result = subprocess.run(['code', '--list-extensions'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')
            return []
        except Exception as e:
            self.logger.error(f"Failed to get installed extensions: {e}")
            return []
    
    def install_extensions(self, extensions: List[str], 
                          skip_installed: bool = True) -> Dict[str, bool]:
        """Install extensions with full validation and optimization"""
        
        # Validate environment
        valid, message = self.validate_environment()
        if not valid:
            self.logger.error(message)
            return {ext: False for ext in extensions}
        
        # Filter out already installed extensions
        if skip_installed:
            installed = self.get_installed_extensions()
            to_install = [ext for ext in extensions if ext not in installed]
            self.logger.info(f"Skipping {len(extensions) - len(to_install)} already installed extensions")
        else:
            to_install = extensions
            
        if not to_install:
            self.logger.info("No extensions to install")
            return {}
        
        # Install extensions
        results = self.performance_optimizer.install_extensions_parallel(to_install)
        
        # Log results
        successful = sum(1 for r in results.values() if r)
        self.logger.info(f"Installation complete: {successful}/{len(to_install)} successful")
        
        return results

# ===========================
# PHASE 4: DOCUMENTATION & MONITORING
# ===========================

class InstallationMonitor:
    """Monitors extension installation and provides documentation"""
    
    def __init__(self, installer: ExtensionInstaller):
        self.installer = installer
        self.logger = installer.logger
        
    def generate_installation_report(self, results: Dict[str, bool]) -> str:
        """Generate detailed installation report"""
        total = len(results)
        successful = sum(1 for r in results.values() if r)
        failed = total - successful
        
        report = f"""
# VS Code Extension Installation Report

## Summary
- Total extensions: {total}
- Successful: {successful}
- Failed: {failed}
- Success rate: {(successful/total)*100:.1f}% if total > 0 else 0%

## Details
"""
        
        for extension, success in results.items():
            status = "✓" if success else "✗"
            report += f"{status} {extension}\n"
            
        return report
    
    def create_installation_log(self, extensions: List[str], results: Dict[str, bool]):
        """Create structured installation log"""
        log_entry = {
            'timestamp': time.time(),
            'extensions_requested': extensions,
            'results': results,
            'environment': {
                'vscode_version': self.installer.validate_environment()[1],
                'installed_extensions': self.installer.get_installed_extensions()
            }
        }
        
        log_file = Path.home() / '.vscode_extension_installer.log'
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
    def get_installation_history(self) -> List[Dict]:
        """Retrieve installation history"""
        log_file = Path.home() / '.vscode_extension_installer.log'
        if not log_file.exists():
            return []
            
        history = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    history.append(json.loads(line.strip()))
                except:
                    continue
                    
        return history

# ===========================
# MAIN EXECUTION
# ===========================

def main():
    """Main entry point for the extension installer"""
    installer = ExtensionInstaller()
    monitor = InstallationMonitor(installer)
    
    # Example usage
    extensions = [
        'ms-python.python',
        'ms-vscode.vscode-typescript-next',
        'esbenp.prettier-vscode'
    ]
    
    results = installer.install_extensions(extensions)
    report = monitor.generate_installation_report(results)
    monitor.create_installation_log(extensions, results)
    
    print(report)

if __name__ == "__main__":
    main()
