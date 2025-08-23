#!/bin/bash
# Auto Project Management Startup Script
# This script starts the automatic project management system

set -e  # Exit on any error

echo "🚀 Starting Auto Project Management Environment..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Install required packages if requirements file exists
REQUIREMENTS_FILE=".auto_project/requirements.txt"
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "📦 Installing required packages..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "⚠️  Requirements file not found, skipping package installation"
fi

# Create logs directory if it doesn't exist
mkdir -p .auto_project/logs

# Start auto runner in background
echo "🔄 Starting automatic project management..."
nohup python3 -m autoprojectmanagement.auto_runner     --path "$(pwd)"     > .auto_project/logs/auto_runner.log 2>&1 &

# Save PID for later management
echo $! > .auto_project/auto_runner.pid

echo "✅ Auto project management started successfully!"
echo "📊 Logs: .auto_project/logs/auto_runner.log"
echo "🛑 To stop: ./stop_auto_management.sh"
echo "📈 To check status: ./status_auto_management.sh"
