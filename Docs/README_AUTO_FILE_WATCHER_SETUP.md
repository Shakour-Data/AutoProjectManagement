# AutoFileWatcherService Setup and Usage

This document provides instructions for setting up and running the AutoFileWatcherService and UnifiedAutoCommit services in the AutoProjectManagement project.

## Overview

- **AutoFileWatcherService**: Monitors file changes in a project directory and triggers automatic git commits.
- **UnifiedAutoCommit**: Handles git commit and push operations with enhanced authentication and guaranteed push.

## Prerequisites

- Python 3.8 or higher
- Git installed and configured on your system
- Proper Git authentication setup (SSH keys, HTTPS credentials, or Personal Access Token)
- Required Python packages (e.g., watchdog) installed (see `requirements.txt`)

## Setup

1. Ensure your Python environment is activated.
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Verify Git authentication:
   - SSH: Ensure your SSH keys are added to your GitHub account.
   - HTTPS: Ensure credentials are cached or configured.
   - PAT: Ensure Personal Access Token is configured if used.

## Running the Service

A startup script is provided to launch the AutoFileWatcherService:

```bash
python scripts/start_auto_file_watcher.py --path /path/to/project --interval 15
```

- `--path`: Path to the project directory to monitor (default: current directory).
- `--interval`: Scheduled commit interval in minutes (default: 15).

The service will monitor file changes and perform automatic commits and scheduled backups.

## Stopping the Service

- Use `Ctrl+C` to gracefully stop the service.

## Logs and Monitoring

- The service outputs logs to the console.
- Logs include file change events, commit status, and error messages.

## Troubleshooting

- Check Git authentication if commits or pushes fail.
- Ensure the project directory is accessible and has proper permissions.
- Review logs for detailed error messages.

## Extending and Customizing

- Modify debounce intervals and monitored file types in `auto_file_watcher.py`.
- Customize commit message formats in `auto_commit.py`.
- Integrate with real-time event services as needed.

## Support

For questions or issues, contact the AutoProjectManagement Team at team@autoprojectmanagement.com.

---
