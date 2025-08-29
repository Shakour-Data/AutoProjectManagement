#!/usr/bin/env python3
"""
Script to restart the auto-commit service with real git operations
"""

import os
import subprocess
import signal
import time

def restart_auto_commit():
    """Restart the auto-commit service"""
    print("🔄 Restarting auto-commit service with real git operations...")
    
    # Kill any existing auto_file_watcher processes
    try:
        subprocess.run(["pkill", "-f", "auto_file_watcher.py"], check=False)
        time.sleep(2)
        print("✅ Stopped existing auto-commit service")
    except:
        pass
    
    # Start new service in background
    cmd = [
        "python", 
        "autoprojectmanagement/services/automation_services/auto_file_watcher.py",
        "--path", os.getcwd()
    ]
    
    print("🚀 Starting new auto-commit service...")
    print("💡 The service will now perform REAL git commits and pushes!")
    print("📊 Monitor the terminal for commit logs...")
    
    # Run in background
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("✅ Auto-commit service restarted successfully")
    print("📝 Make some file changes to test real commits...")

if __name__ == "__main__":
    restart_auto_commit()
