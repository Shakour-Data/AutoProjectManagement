#!/bin/bash
# Setup script for AutoProjectManagement Status Bar

echo "Setting up AutoProjectManagement Status Bar..."

# Make the status bar script executable
chmod +x autoprojectmanagement/vscode_extension_status_bar.py

# Create necessary directories
mkdir -p .vscode/out
mkdir -p .vscode/web
mkdir -p JSonDataBase/OutPuts

# Run the status bar setup
python autoprojectmanagement/vscode_extension_status_bar.py

echo ""
echo "✅ Status Bar Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Reload VS Code window (Ctrl+Shift+P → 'Developer: Reload Window')"
echo "2. Look for the status bar item on the bottom right"
echo "3. Use Ctrl+Shift+P and search for 'AutoPM' commands"
echo "4. Start the API server: python -m autoprojectmanagement.api.main"
echo "5. Visit http://localhost:8000/web/status.html for web status"
echo ""
echo "🔧 Status Bar Features:"
echo "- Real-time project progress in VS Code status bar"
echo -e "- \U0001F504 Auto-refresh every 30 seconds"
echo -e "- \U0001F4CA Progress percentage and task completion"
echo -e "- \U0001F4CB Click to view detailed project report"
echo -e "- \U0001F310 Web interface available at /web/status.html"
