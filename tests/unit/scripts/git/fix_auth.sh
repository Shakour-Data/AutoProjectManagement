#!/bin/bash

# Quick Git Authentication Fix Script
# This script will help fix the git push authentication issue

set -e

echo "=== Git Authentication Fix ==="
echo "This will set up Personal Access Token authentication"

# Get current directory
PROJECT_DIR="/home/gravitywaves/GravityProject/AutoProjectManagement"

# Check if .git-credentials exists
if [ ! -f "$PROJECT_DIR/.git-credentials" ]; then
    echo "Creating .git-credentials file..."
    
    echo "Please enter your GitHub username:"
    read USERNAME
    
    echo "Please enter your GitHub Personal Access Token:"
    read -s TOKEN
    
    # Create .git-credentials file
    echo "https://${USERNAME}:${TOKEN}@github.com" > "$PROJECT_DIR/.git-credentials"
    
    # Configure git to use the credentials file
    git config --global credential.helper 'store --file ~/.git-credentials'
    
    echo "✓ .git-credentials created and configured"
else
    echo "✓ .git-credentials already exists"
fi

# Configure git to use the credentials
git config --global credential.helper store
git config --global url."https://github.com/".insteadOf git@github.com:

echo "Testing authentication..."
if git ls-remote https://github.com/Shakour-Data/AutoProjectManagement.git HEAD > /dev/null 2>&1; then
    echo "✓ Authentication successful!"
    echo "You can now push with: git push origin Documentation"
else
    echo "✗ Authentication failed"
    echo "Please check your Personal Access Token"
fi
