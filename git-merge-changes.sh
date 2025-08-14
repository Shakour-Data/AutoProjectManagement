#!/bin/bash

# Script: git-merge-changes.sh
# Description: Automates merging changes from one branch to another
# Usage: ./git-merge-changes.sh [source_branch] [target_branch]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Set trap to cleanup on script exit
trap cleanup EXIT

# Check if required arguments are provided
if [ $# -ne 2 ]; then
    print_message $RED "Usage: $0 <source_branch> <target_branch>"
    print_message $RED "Example: $0 shakour2 Documentation"
    exit 1
fi

SOURCE_BRANCH=$1
TARGET_BRANCH=$2
TEMP_BRANCH="temp-merge-$(date +%s)"

print_message $GREEN "Starting merge process..."
print_message $GREEN "Source branch: $SOURCE_BRANCH"
print_message $GREEN "Target branch: $TARGET_BRANCH"

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

# Merge changes from source branch
print_message $YELLOW "Merging changes from $SOURCE_BRANCH..."
if git merge "origin/$SOURCE_BRANCH" --no-edit; then
    print_message $GREEN "Merge successful!"
else
    print_message $RED "Merge conflicts detected!"
    print_message $YELLOW "Please resolve conflicts manually, then run:"
    print_message $YELLOW "  git add ."
    print_message $YELLOW "  git commit"
    print_message $YELLOW "  git push origin $TEMP_BRANCH:$TARGET_BRANCH"
    print_message $YELLOW "  git checkout $TARGET_BRANCH"
    print_message $YELLOW "  git merge $SOURCE_BRANCH"
    exit 1
fi

# Push changes to remote
print_message $YELLOW "Pushing changes to remote..."
if git push origin "$TEMP_BRANCH:$TARGET_BRANCH"; then
    print_message $GREEN "Changes pushed successfully to $TARGET_BRANCH!"
else
    print_message $RED "Failed to push changes"
    exit 1
fi

# Switch to target branch and merge
print_message $YELLOW "Switching to $TARGET_BRANCH and merging..."
git checkout "$TARGET_BRANCH"
git pull origin "$TARGET_BRANCH"

# Clean up
print_message $GREEN "Cleaning up..."
git branch -D "$TEMP_BRANCH" 2>/dev/null || true

print_message $GREEN "Process completed successfully!"
print_message $GREEN "Changes from $SOURCE_BRANCH have been applied to $TARGET_BRANCH"
