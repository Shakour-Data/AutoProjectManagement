#!/bin/bash
# Auto Project Management Stop Script
# This script gracefully stops the automatic project management system

set -e  # Exit on any error

echo "🛑 Stopping Auto Project Management Environment..."

PID_FILE=".auto_project/auto_runner.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 $PID 2>/dev/null; then
        echo "📋 Stopping process with PID: $PID"
        kill $PID
        rm "$PID_FILE"
        echo "✅ Auto project management stopped successfully!"
    else
        echo "⚠️  Process not found or already stopped"
        rm -f "$PID_FILE"
    fi
else
    echo "⚠️  No PID file found. Process may not be running."
fi

# Kill any remaining Python processes related to auto_runner
pkill -f "auto_runner.py" 2>/dev/null || true

# Clean up any stale lock files
rm -f .auto_project/*.lock 2>/dev/null || true

echo "🧹 Cleanup complete!"
