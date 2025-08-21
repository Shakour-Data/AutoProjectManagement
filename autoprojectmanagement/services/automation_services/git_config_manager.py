#!/usr/bin/env python3
"""
Git Configuration Manager for AutoProjectManagement
Purpose: Automatically configure Git settings to prevent RPC errors
Author: AutoProjectManagement System
Version: 1.0.0
License: MIT
"""

import os
import subprocess
import logging
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


class GitConfigManager:
    """Manages Git configuration to prevent RPC and network errors."""
    
    def __init__(self):
        """Initialize the Git configuration manager."""
        self.logger = logging.getLogger(__name__)
        self.config_applied = False
        
    def apply_optimized_config(self) -> bool:
        """Apply optimized Git configuration to prevent RPC errors."""
        try:
            configs = [
                # Memory and buffer configurations
                ["config", "--global", "http.postBuffer", "1048576000"],
                ["config", "--global", "http.maxRequestBuffer", "100M"],
                ["config", "--global", "pack.packSizeLimit", "100m"],
                ["config", "--global", "pack.deltaCacheSize", "512m"],
                ["config", "--global", "pack.windowMemory", "512m"],
                ["config", "--global", "core.packedGitLimit", "512m"],
                ["config", "--global", "core.packedGitWindowSize", "512m"],
                ["config", "--global", "core.bigFileThreshold", "50m"],
                
                # Network configurations
                ["config", "--global", "http.version", "HTTP/1.1"],
                ["config", "--global", "http.lowSpeedLimit", "0"],
                ["config", "--global", "http.lowSpeedTime", "999999"],
                ["config", "--global", "http.sslVerify", "false"],
                ["config", "--global", "sendpack.sideband", "false"],
                
                # Compression and performance
                ["config", "--global", "core.compression", "0"],
                ["config", "--global", "core.preloadIndex", "false"],
                ["config", "--global", "core.fscache", "false"],
                ["config", "--global", "pack.threads", "1"],
                
                # Transfer limits
                ["config", "--global", "transfer.maxPackSize", "100m"],
                ["config", "--global", "transfer.maxPackObjects", "1000"],
                ["config", "--global", "receive.maxInputSize", "100m"],
                
                # Retry and timeout settings
                ["config", "--global", "http.retry", "3"],
                ["config", "--global", "http.timeout", "300"],
            ]
            
            for config in configs:
                success, _ = self.run_git_command(config)
                if not success:
                    self.logger.warning(f"Failed to apply config: {' '.join(config)}")
                    
            self.config_applied = True
            self.logger.info("✅ Git optimized configuration applied successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to apply Git configuration: {e}")
            return False
    
    def check_and_fix_remote_url(self) -> bool:
        """Check and fix remote URL to use optimal protocol."""
        try:
            success, current_url = self.run_git_command(["config", "--get", "remote.origin.url"])
            if not success:
                self.logger.warning("Could not get remote URL")
                return False
                
            # Check if using HTTPS (which has more issues)
            if current_url.startswith("https://"):
                # Convert to SSH for better performance
                ssh_url = current_url.replace("https://github.com/", "git@github.com:")
                success, _ = self.run_git_command(["remote", "set-url", "origin", ssh_url])
                if success:
                    self.logger.info(f"✅ Remote URL changed from HTTPS to SSH: {ssh_url}")
                    return True
                    
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to fix remote URL: {e}")
            return False
    
    def setup_lfs_if_needed(self) -> bool:
        """Setup Git LFS for large files if not already configured."""
        try:
            # Check if LFS is installed
            success, _ = self.run_git_command(["lfs", "version"])
            if not success:
                self.logger.info("Git LFS not installed, skipping LFS setup")
                return True
                
            # Configure LFS tracking for common large file types
            lfs_patterns = [
                "*.pdf", "*.zip", "*.tar.gz", "*.rar", "*.7z",
                "*.docx", "*.xlsx", "*.pptx", "*.mp4", "*.avi",
                "*.mov", "*.jpg", "*.png", "*.gif", "*.psd"
            ]
            
            for pattern in lfs_patterns:
                self.run_git_command(["lfs", "track", pattern])
                
            self.logger.info("✅ Git LFS configured for large files")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to setup LFS: {e}")
            return False
    
    def run_git_command(self, args: List[str], cwd: Optional[str] = None) -> Tuple[bool, str]:
        """Run a git command with error handling."""
        try:
            env = os.environ.copy()
            env.update({
                'GIT_MMAP_LIMIT': '1g',
                'GIT_ALLOC_LIMIT': '1g',
                'GIT_SSL_NO_VERIFY': '1'
            })
            
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd,
                env=env
            )
            return True, result.stdout.strip()
            
        except subprocess.CalledProcessError as e:
            self.logger.debug(f"Git command failed: git {' '.join(args)}")
            return False, e.stderr.strip()
    
    def verify_configuration(self) -> bool:
        """Verify that the configuration is properly applied."""
        try:
            # Check key configurations
            configs_to_check = [
                "http.postBuffer",
                "http.maxRequestBuffer",
                "http.version",
                "core.compression"
            ]
            
            for config in configs_to_check:
                success, value = self.run_git_command(["config", "--get", config])
                if success:
                    self.logger.info(f"✅ {config}: {value}")
                else:
                    self.logger.warning(f"⚠️  {config}: not set")
                    
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to verify configuration: {e}")
            return False
    
    def auto_configure(self) -> bool:
        """Automatically configure Git for optimal performance."""
        self.logger.info("🚀 Starting automatic Git configuration...")
        
        # Apply optimized configuration
        if not self.apply_optimized_config():
            return False
            
        # Fix remote URL
        self.check_and_fix_remote_url()
        
        # Setup LFS
        self.setup_lfs_if_needed()
        
        # Verify configuration
        self.verify_configuration()
        
        self.logger.info("✅ Automatic Git configuration completed")
        return True


# Global instance
git_config_manager = GitConfigManager()


def configure_git_automatically():
    """Automatically configure Git settings to prevent RPC errors."""
    return git_config_manager.auto_configure()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    success = configure_git_automatically()
    if success:
        print("✅ Git configuration completed successfully")
    else:
        print("❌ Git configuration failed")
