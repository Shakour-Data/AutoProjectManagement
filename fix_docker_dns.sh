#!/bin/bash
# Fix Docker DNS configuration to prevent Git push failures

echo "🔧 Fixing Docker DNS configuration..."

# Create backup of current Docker config
cp ~/.docker/daemon.json ~/.docker/daemon.json.backup 2>/dev/null || echo "No existing config found"

# Create new Docker daemon configuration with DNS fix
cat > ~/.docker/daemon.json << 'EOF'
{
  "dns": ["8.8.8.8", "8.8.4.4", "1.1.1.1"],
  "experimental": false,
  "features": {
    "buildkit": true
  }
}
EOF

echo "✅ DNS configuration updated to use Google and Cloudflare DNS"
echo "🔄 Restarting Docker to apply changes..."

# Restart Docker service
sudo systemctl restart docker 2>/dev/null || echo "Please restart Docker Desktop manually"

echo "🎉 Docker DNS fix applied!"
echo "💡 Test with: git push origin main"
