#!/bin/bash
# Comprehensive Docker + Git troubleshooting script

echo "🚀 Docker + Git Troubleshooting Script"
echo "======================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "✅ Docker is running"

# Check current Git remote
echo "📡 Current Git remote:"
git remote -v

# Check network connectivity to GitHub
echo "🔍 Testing GitHub connectivity..."
if curl -s https://api.github.com > /dev/null; then
    echo "✅ GitHub is reachable"
else
    echo "❌ GitHub connectivity issue detected"
fi

# Apply DNS fix
echo "🔄 Applying DNS fix..."
./fix_docker_dns.sh

# Optimize Git
echo "⚙️ Optimizing Git configuration..."
./optimize_git_config.sh

# Test Git push with dry run
echo "🧪 Testing Git push (dry run)..."
git push --dry-run

echo ""
echo "🎯 Next steps:"
echo "1. Run: git push origin main"
echo "2. If still failing, try: git push --set-upstream origin main"
echo "3. For very large files, try: git lfs track '*.large' && git add .gitattributes"
echo ""
echo "💡 Emergency fallback: Use SSH instead of HTTPS"
echo "   git remote set-url origin git@github.com:Shakour-Data/AutoProjectManagement.git"
