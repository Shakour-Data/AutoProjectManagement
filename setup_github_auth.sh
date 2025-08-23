#!/bin/bash

# GitHub Authentication Setup Script
# This script sets up multiple authentication methods for GitHub

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== GitHub Authentication Setup ===${NC}"
echo -e "${YELLOW}This script will set up multiple authentication methods for GitHub${NC}"
echo ""

# Get user information
PROJECT_DIR="/home/gravitywaves/GravityProject/AutoProjectManagement"
GITHUB_REPO="https://github.com/Shakour-Data/AutoProjectManagement.git"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Phase 1: Personal Access Token Setup
setup_pat() {
    echo -e "${GREEN}Phase 1: Setting up Personal Access Token (PAT)${NC}"
    
    # Create .git-credentials file template
    cat > "$PROJECT_DIR/.git-credentials-template" << 'EOF'
# GitHub Personal Access Token Configuration
# Replace YOUR_TOKEN_HERE with your actual token
# Format: https://USERNAME:TOKEN@github.com
# Example: https://gravitywaves:ghp_xxxxxxxxxxxxxxxxxxxx@github.com

# To create a token:
# 1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
# 2. Click "Generate new token (classic)"
# 3. Select scopes: repo, workflow, user:email
# 4. Copy the token and replace YOUR_TOKEN_HERE

https://YOUR_USERNAME:YOUR_TOKEN@github.com
EOF

    echo -e "${YELLOW}✓ Created .git-credentials-template${NC}"
    echo -e "${YELLOW}✓ Next step: Create a Personal Access Token on GitHub${NC}"
    echo -e "${YELLOW}  Visit: https://github.com/settings/tokens${NC}"
    echo ""
}

# Phase 2: SSH Key Setup
setup_ssh() {
    echo -e "${GREEN}Phase 2: Setting up SSH Keys${NC}"
    
    # Check if SSH key exists
    if [ ! -f ~/.ssh/id_ed25519 ]; then
        echo -e "${YELLOW}Creating new SSH key...${NC}"
        
        # Generate SSH key
        ssh-keygen -t ed25519 -C "gravitywaves2000@gmail.com" -f ~/.ssh/id_ed25519 -N ""
        
        # Start SSH agent and add key
        eval "$(ssh-agent -s)"
        ssh-add ~/.ssh/id_ed25519
        
        echo -e "${GREEN}✓ SSH key generated: ~/.ssh/id_ed25519${NC}"
    else
        echo -e "${GREEN}✓ SSH key already exists${NC}"
    fi
    
    # Display public key
    if [ -f ~/.ssh/id_ed25519.pub ]; then
        echo -e "${YELLOW}Your SSH public key:${NC}"
        cat ~/.ssh/id_ed25519.pub
        echo ""
        echo -e "${YELLOW}Add this key to GitHub: https://github.com/settings/keys${NC}"
    fi
    
    # Configure SSH for GitHub
    cat >> ~/.ssh/config << 'EOF'

# GitHub configuration
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
EOF
    
    echo -e "${GREEN}✓ SSH config updated${NC}"
}

# Phase 3: GitHub CLI Setup
setup_gh_cli() {
    echo -e "${GREEN}Phase 3: Setting up GitHub CLI${NC}"
    
    if ! command_exists gh; then
        echo -e "${YELLOW}Installing GitHub CLI...${NC}"
        
        # Install GitHub CLI based on system
        if command_exists apt-get; then
            sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0
            sudo apt-add-repository https://cli.github.com/packages
            sudo apt update
            sudo apt install gh
        elif command_exists yum; then
            sudo yum install gh
        elif command_exists brew; then
            brew install gh
        else
            # Download binary
            curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
            sudo apt update
            sudo apt install gh
        fi
        
        echo -e "${GREEN}✓ GitHub CLI installed${NC}"
    else
        echo -e "${GREEN}✓ GitHub CLI already installed${NC}"
    fi
    
    # Authenticate with GitHub CLI
    echo -e "${YELLOW}Authenticating with GitHub CLI...${NC}"
    echo -e "${YELLOW}Run: gh auth login${NC}"
    echo -e "${YELLOW}Choose: HTTPS with Personal Access Token${NC}"
}

# Phase 4: Git Configuration Updates
setup_git_config() {
    echo -e "${GREEN}Phase 4: Updating Git Configuration${NC}"
    
    # Set user information
    git config --global user.name "GravityWavesOrg"
    git config --global user.email "gravitywaves2000@gmail.com"
    
    # Set default branch
    git config --global init.defaultBranch main
    
    # Set up better defaults
    git config --global pull.rebase false
    git config --global push.default simple
    git config --global core.autocrlf input
    
    # Set up credential caching
    git config --global credential.helper 'cache --timeout=3600'
    
    echo -e "${GREEN}✓ Git configuration updated${NC}"
}

# Phase 5: Test Authentication
test_authentication() {
    echo -e "${GREEN}Phase 5: Testing Authentication${NC}"
    
    # Test HTTPS with PAT
    echo -e "${YELLOW}Testing HTTPS authentication...${NC}"
    git ls-remote https://github.com/Shakour-Data/AutoProjectManagement.git HEAD
    
    # Test SSH
    echo -e "${YELLOW}Testing SSH authentication...${NC}"
    ssh -T git@github.com || echo "SSH test completed"
    
    echo -e "${GREEN}✓ Authentication tests completed${NC}"
}

# Main execution
main() {
    echo -e "${BLUE}Starting GitHub Authentication Setup...${NC}"
    
    setup_pat
    setup_ssh
    setup_gh_cli
    setup_git_config
    test_authentication
    
    echo ""
    echo -e "${GREEN}=== Setup Complete! ===${NC}"
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "1. Create Personal Access Token: https://github.com/settings/tokens"
    echo -e "2. Add SSH key to GitHub: https://github.com/settings/keys"
    echo -e "3. Run: gh auth login"
    echo -e "4. Test push: git push origin Documentation"
}

# Run main function
main
