#!/bin/bash
# Optimize Git configuration for large repositories with Docker

echo "⚙️ Optimizing Git configuration for Docker environment..."

# Increase Git buffer sizes for large files
git config --global http.postBuffer 524288000
git config --global http.maxRequestBuffer 100M
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999
git config --global http.version HTTP/1.1
git config --global http.timeout 300

# Disable SSL verification for local development (optional)
git config --global http.sslVerify false

# Increase retry attempts
git config --global http.retry 3

# Set compression level
git config --global core.compression 0

# Enable long paths (for Windows compatibility)
git config --global core.longpaths true

# Set SSH as default for GitHub
git config --global url."git@github.com:".insteadOf "https://github.com/"

echo "✅ Git configuration optimized!"
echo "📊 Current Git settings:"
git config --list | grep -E "http|core|url"
