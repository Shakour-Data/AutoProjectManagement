#!/usr/bin/env python3
"""
One-command Docker setup for AutoProjectManagement
Usage: python scripts/one-command-docker-setup.py
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    """Main setup function"""
    print("🚀 AutoProjectManagement - One-Command Docker Setup")
    print("=" * 50)
    
    # Get project root
    project_root = Path(__file__).parent.parent
    
    # Install the package
    print("📦 Installing AutoProjectManagement package...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", str(project_root)
        ], check=True)
        print("✅ Package installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install package")
        return False
    
    # Run Docker setup
    print("\n🐳 Setting up Docker environment...")
    try:
        # Add the project root to Python path
        sys.path.insert(0, str(project_root))
        from autoprojectmanagement.docker_setup import post_install_setup
        post_install_setup()
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Visit http://localhost:8000 for API")
        print("2. Visit http://localhost:8080 for monitoring")
        print("3. Run 'apm docker status' to check service status")
    else:
        print("\n💡 Manual setup available:")
        print("1. Install package: pip install -e .")
        print("2. Setup Docker: apm docker setup")
        sys.exit(1)
