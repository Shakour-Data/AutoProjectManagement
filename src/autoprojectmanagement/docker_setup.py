#!/usr/bin/env python3
"""
Docker setup automation module for AutoProjectManagement
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

class DockerSetup:
    """Automated Docker setup and management"""
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path(__file__).parent.parent
        self.script_path = self.project_root / "scripts" / "auto-docker-setup.sh"
        
    def check_docker_installed(self) -> bool:
        """Check if Docker is installed and available"""
        try:
            subprocess.run(["docker", "--version"], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def check_docker_compose(self) -> bool:
        """Check if Docker Compose is available"""
        try:
            # Try both docker-compose and docker compose
            subprocess.run(["docker-compose", "--version"], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(["docker", "compose", "version"], 
                             capture_output=True, check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
    
    def detect_environment(self) -> str:
        """Auto-detect the appropriate environment"""
        # Check git branch
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            branch = result.stdout.strip()
            if branch in ["main", "master"]:
                return "production"
            else:
                return "development"
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Default to development
            return "development"
    
    def setup_docker(self, environment: Optional[str] = None, auto: bool = True) -> bool:
        """Set up Docker environment automatically"""
        if environment is None:
            environment = self.detect_environment()
        
        print(f"Setting up Docker for {environment} environment...")
        
        if not self.check_docker_installed():
            print("Docker is not installed. Please install Docker first.")
            return False
        
        if not self.check_docker_compose():
            print("Docker Compose is not available. Please install Docker Compose.")
            return False
        
        # Run the setup script
        try:
            cmd = ["bash", str(self.script_path)]
            if environment:
                cmd.append(environment)
            
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"Docker setup failed: {e}")
            return False
    
    def get_compose_file(self, environment: str) -> str:
        """Get the appropriate docker-compose file for environment"""
        compose_files = {
            "development": "docker-compose.dev.yml",
            "production": "docker-compose.prod.yml"
        }
        return compose_files.get(environment, "docker-compose.yml")
    
    def start_services(self, environment: Optional[str] = None) -> bool:
        """Start Docker services"""
        if environment is None:
            environment = self.detect_environment()
        
        compose_file = self.get_compose_file(environment)
        compose_path = self.project_root / compose_file
        
        if not compose_path.exists():
            print(f"Docker compose file not found: {compose_file}")
            return False
        
        try:
            cmd = ["docker-compose", "-f", str(compose_path), "up", "-d"]
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"Failed to start services: {e}")
            return False
    
    def stop_services(self, environment: Optional[str] = None) -> bool:
        """Stop Docker services"""
        if environment is None:
            environment = self.detect_environment()
        
        compose_file = self.get_compose_file(environment)
        compose_path = self.project_root / compose_file
        
        try:
            cmd = ["docker-compose", "-f", str(compose_path), "down"]
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"Failed to stop services: {e}")
            return False
    
    def show_status(self, environment: Optional[str] = None) -> None:
        """Show Docker services status"""
        if environment is None:
            environment = self.detect_environment()
        
        compose_file = self.get_compose_file(environment)
        compose_path = self.project_root / compose_file
        
        try:
            cmd = ["docker-compose", "-f", str(compose_path), "ps"]
            subprocess.run(cmd, cwd=self.project_root)
        except subprocess.CalledProcessError as e:
            print(f"Failed to show status: {e}")
    
    def install_docker_cli(self) -> bool:
        """Install Docker CLI tools if not available"""
        system = platform.system().lower()
        
        if system == "linux":
            # Ubuntu/Debian
            if shutil.which("apt-get"):
                try:
                    subprocess.run([
                        "sudo", "apt-get", "update"
                    ], check=True)
                    subprocess.run([
                        "sudo", "apt-get", "install", "-y", "docker.io", "docker-compose"
                    ], check=True)
                    subprocess.run([
                        "sudo", "usermod", "-aG", "docker", os.getenv("USER", "user")
                    ], check=True)
                    return True
                except subprocess.CalledProcessError:
                    return False
            # CentOS/RHEL
            elif shutil.which("yum"):
                try:
                    subprocess.run([
                        "sudo", "yum", "install", "-y", "docker", "docker-compose"
                    ], check=True)
                    subprocess.run([
                        "sudo", "systemctl", "start", "docker"
                    ], check=True)
                    subprocess.run([
                        "sudo", "usermod", "-aG", "docker", os.getenv("USER", "user")
                    ], check=True)
                    return True
                except subprocess.CalledProcessError:
                    return False
        
        return False

# Post-installation hook
def post_install_setup():
    """Run automatic Docker setup after package installation"""
    setup = DockerSetup()
    
    print("\n" + "="*60)
    print("AutoProjectManagement Docker Setup")
    print("="*60)
    
    if setup.check_docker_installed():
        print("✓ Docker is already installed")
    else:
        print("✗ Docker is not installed")
        if platform.system().lower() == "linux":
            print("Installing Docker...")
            if setup.install_docker_cli():
                print("✓ Docker installed successfully")
            else:
                print("✗ Failed to install Docker automatically")
                print("Please install Docker manually and run: apm docker setup")
                return
    
    # Auto-setup Docker environment
    print("\nSetting up Docker environment...")
    if setup.setup_docker(auto=True):
        print("✓ Docker environment setup completed!")
        print("\nYour AutoProjectManagement system is now running!")
        print("Access URLs:")
        print("  - API: http://localhost:8000")
        print("  - Monitor: http://localhost:8080")
    else:
        print("✗ Docker setup failed")
        print("Run 'apm docker setup' to retry setup")

if __name__ == "__main__":
    post_install_setup()
