#!/usr/bin/env python3
"""
Startup script to launch the AutoFileWatcherService for AutoProjectManagement.

This script initializes and starts the AutoFileWatcherService with default or
custom configuration. It is intended to be used to run the file watcher service
continuously for project monitoring and automatic commits.

Usage:
    python scripts/start_auto_file_watcher.py --path /path/to/project --interval 15

Arguments:
    --path: Path to the project directory to monitor (default: current directory)
    --interval: Scheduled commit interval in minutes (default: 15)

The service runs until interrupted by Ctrl+C.
"""

import argparse
import sys
import os

# Add project root to sys.path for imports
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from autoprojectmanagement.services.automation_services.auto_file_watcher import AutoFileWatcherService
except ImportError as e:
    print(f"Failed to import AutoFileWatcherService: {e}")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Start AutoFileWatcherService for AutoProjectManagement")
    parser.add_argument('--path', type=str, default=os.getcwd(), help='Project path to monitor (default: current directory)')
    parser.add_argument('--interval', type=int, default=15, help='Scheduled commit interval in minutes (default: 15)')
    args = parser.parse_args()

    service = AutoFileWatcherService(project_path=args.path, interval_minutes=args.interval)
    try:
        service.start()
    except KeyboardInterrupt:
        print("Shutting down AutoFileWatcherService...")
        service.stop()

if __name__ == "__main__":
    main()
