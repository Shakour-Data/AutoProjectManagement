#!/bin/bash
# Auto Project Management Status Script
# This script displays comprehensive status information

set -e  # Exit on any error

echo "📊 Auto Project Management Status"
echo "================================"
echo ""

# Check if process is running
PID_FILE=".auto_project/auto_runner.pid"
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 $PID 2>/dev/null; then
        echo "✅ Status: Running (PID: $PID)"
        
        # Get process information
        if command -v ps &> /dev/null; then
            echo "📋 Process details:"
            ps -p $PID -o pid,ppid,cmd,etime 2>/dev/null || echo "  Unable to get process details"
        fi
    else
        echo "❌ Status: Process not running (stale PID file)"
        rm -f "$PID_FILE"
    fi
else
    echo "❌ Status: Not running"
fi

# Display recent log entries
LOG_FILE=".auto_project/logs/auto_runner.log"
if [ -f "$LOG_FILE" ]; then
    echo ""
    echo "📋 Last 10 log entries:"
    echo "------------------------"
    tail -10 "$LOG_FILE" 2>/dev/null || echo "  Unable to read log file"
else
    echo ""
    echo "⚠️  No log file found"
fi

# Display project structure
echo ""
echo "📁 Project Structure:"
echo "---------------------"
if [ -d ".auto_project" ]; then
    find .auto_project -type d -name ".*" -prune -o -type f -print | head -20
else
    echo "  .auto_project directory not found"
fi

# Check disk usage
echo ""
echo "💾 Disk Usage:"
echo "-------------"
if command -v du &> /dev/null; then
    du -sh .auto_project 2>/dev/null || echo "  Unable to check disk usage"
else
    echo "  du command not available"
fi
