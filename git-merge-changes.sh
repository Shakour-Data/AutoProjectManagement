#!/bin/bash

# Script: git-merge-unrelated-histories-fixed.sh
# Description: Handles merging branches with unrelated histories with source branch priority
# Usage: ./git-merge-unrelated-histories-fixed.sh [source_branch] [target_branch]
# Note: When conflicts occur, changes from the source branch take priority

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if branch exists
branch_exists() {
    git show-ref --verify --quiet "refs/heads/$1" || git show-ref --verify --quiet "refs/remotes/origin/$1"
}

# Function to cleanup on exit
cleanup() {
    if [ -n "$TEMP_BRANCH" ] && git branch | grep -q "$TEMP_BRANCH"; then
        print_message $YELLOW "Cleaning up temporary branch..."
        git checkout - >/dev/null 2>&1 || git checkout main >/dev/null 2>&1
        git branch -D "$TEMP_BRANCH" >/dev/null 2>&1 || true
    fi
}

# Function to force merge with source branch priority
force_merge_with_source_priority() {
    print_message $YELLOW "Forcing merge with source branch priority..."
    
    # Get current branch
    local current_branch=$(git rev-parse --abbrev-ref HEAD)
    
    # Create a new branch from source
    local source_temp="source-temp-$(date +%s)"
    git checkout -b "$source_temp" "origin/$SOURCE_BRANCH"
    
    # Merge target branch with ours strategy (keep source changes)
    print_message $YELLOW "Merging target branch with source branch priority..."
    git merge "origin/$TARGET_BRANCH" --allow-unrelated-histories --no-edit --strategy=ours || {
        print_message $YELLOW "Using alternative merge approach..."
        
        # Reset to source branch state
        git reset --hard "origin/$SOURCE_BRANCH"
        
        # Create empty commit with merge message
        git merge "origin/$TARGET_BRANCH" --allow-unrelated-histories --no-edit --strategy=ours --no-commit || true
        
        # Force source branch files
        git checkout "origin/$SOURCE_BRANCH" -- .
        git add .
        git commit -m "Merge $TARGET_BRANCH into $SOURCE_BRANCH with source branch priority" || true
    }
    
    # Switch back to target branch
    git checkout "$current_branch"
    
    # Reset target branch to the merged source branch
    git reset --hard "$source_temp"
    
    # Clean up temporary branch
    git branch -D "$source_temp" 2>/dev/null || true
    
    print_message $GREEN "Successfully applied source branch changes with priority"
}

# Set trap to cleanup on script exit
trap cleanup EXIT

# Check if required arguments are provided
if [ $# -ne 2 ]; then
    print_message $RED "Usage: $0 <source_branch> <target_branch>"
    print_message $RED "Example: $0 Documentation main"
    exit 1
fi

SOURCE_BRANCH=$1
TARGET_BRANCH=$2
TEMP_BRANCH="temp-merge-$(date +%s)"

print_message $GREEN "Starting merge process for unrelated histories..."
print_message $GREEN "Source branch: $SOURCE_BRANCH"
print_message $GREEN "Target branch: $TARGET_BRANCH"
print_message $BLUE "Note: When conflicts occur, source branch changes will take priority"

# Ensure we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_message $RED "Error: Not in a git repository"
    exit 1
fi

# Fetch latest changes from origin
print_message $YELLOW "Fetching latest changes from origin..."
git fetch origin

# Check if source branch exists
if ! branch_exists "$SOURCE_BRANCH"; then
    print_message $RED "Error: Source branch '$SOURCE_BRANCH' does not exist"
    exit 1
fi

# Check if target branch exists
if ! branch_exists "$TARGET_BRANCH"; then
    print_message $RED "Error: Target branch '$TARGET_BRANCH' does not exist"
    exit 1
fi

# Create and checkout temporary branch from target
print_message $YELLOW "Creating temporary branch from $TARGET_BRANCH..."
git checkout -b "$TEMP_BRANCH" "origin/$TARGET_BRANCH"

# Perform merge with source branch priority
print_message $YELLOW "Applying source branch changes with priority..."

# Use a different approach: create source branch and merge target with ours strategy
force_merge_with_source_priority

# Push changes to remote
print_message $YELLOW "Pushing changes to remote..."
if git push origin "$TEMP_BRANCH:$TARGET_BRANCH" --force-with-lease; then
    print_message $GREEN "Changes pushed successfully to $TARGET_BRANCH!"
else
    print_message $RED "Failed to push changes"
    exit 1
fi

# Switch to target branch and pull latest
print_message $YELLOW "Switching to $TARGET_BRANCH and pulling latest..."
git checkout "$TARGET_BRANCH"
git pull origin "$TARGET_BRANCH"

# Clean up
print_message $GREEN "Cleaning up..."
git branch -D "$TEMP_BRANCH" 2>/dev/null || true

print_message $GREEN "Process completed successfully!"
print_message $GREEN "Changes from $SOURCE_BRANCH have been applied to $TARGET_BRANCH"
print_message $BLUE "All conflicts were resolved with source branch ($SOURCE_BRANCH) taking priority"
