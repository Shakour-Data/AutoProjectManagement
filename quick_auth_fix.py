#!/usr/bin/env python3
"""
Quick Git Authentication Fix
Purpose: Immediate fix for Git authentication issues
Author: AutoProjectManagement System
Version: 1.0.0
"""

import os
import subprocess
import sys

def run_command(cmd, cwd=None):
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    """Main authentication fix function."""
    project_dir = "/home/gravitywaves/GravityProject/AutoProjectManagement"
    
    print("🔧 Quick Git Authentication Fix")
    print("=" * 40)
    
    # Check current remote URL
    success, stdout, stderr = run_command("git remote -v", cwd=project_dir)
    if success:
        print("Current remote URLs:")
        print(stdout)
    
    # Switch to HTTPS (immediate fix)
    print("\n🔄 Switching to HTTPS authentication...")
    https_url = "https://github.com/Shakour-Data/AutoProjectManagement.git"
    success, stdout, stderr = run_command(f"git remote set-url origin {https_url}", cwd=project_dir)
    
    if success:
        print("✅ Switched to HTTPS authentication")
    else:
        print(f"❌ Failed to switch: {stderr}")
    
    # Test authentication
    print("\n🧪 Testing authentication...")
    success, stdout, stderr = run_command("git ls-remote https://github.com/Shakour-Data/AutoProjectManagement.git HEAD", cwd=project_dir)
    
    if success:
        print("✅ HTTPS authentication working!")
    else:
        print("❌ HTTPS authentication failed")
        print("You need to set up a Personal Access Token")
        print("Run: ./fix_git_auth.sh")
    
    # Provide instructions
    print("\n📋 Next Steps:")
    print("1. Create Personal Access Token: https://github.com/settings/tokens")
    print("2. Run: ./fix_git_auth.sh")
    print("3. Test: git push origin Documentation")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
