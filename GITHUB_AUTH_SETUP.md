# GitHub Authentication Setup Guide

## 🚀 Quick Start - Immediate Fix

### Step 1: Create Personal Access Token (PAT)

1. **Go to GitHub Settings**: https://github.com/settings/tokens
2. **Click "Generate new token (classic)"**
3. **Select these scopes**:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `user:email` (Access user email addresses)
4. **Copy the generated token** (starts with `ghp_`)

### Step 2: Configure Git with PAT

```bash
# Run this script with your token
./setup_github_auth.sh
```

Or manually configure:

```bash
# Set up credential helper
git config --global credential.helper store

# When prompted for password, use your PAT
git push origin Documentation
```

## 🔧 Alternative Methods

### Method 2: SSH Keys (Recommended for long-term use)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "gravitywaves2000@gmail.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key and add to GitHub
cat ~/.ssh/id_ed25519.pub
# Then visit: https://github.com/settings/keys
```

### Method 3: GitHub CLI (Easiest setup)

```bash
# Install GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Authenticate
gh auth login
```

## 🎯 Immediate Action Plan

1. **Run the setup script**:
   ```bash
   ./setup_github_auth.sh
   ```

2. **Choose your preferred method**:
   - **PAT**: Most secure, works immediately
   - **SSH**: Best for long-term use
   - **GitHub CLI**: Easiest setup

3. **Test your connection**:
   ```bash
   git push origin Documentation
   ```

## 📋 Troubleshooting

### Common Issues:

1. **"Permission denied"**:
   - Check token permissions
   - Verify SSH key is added to GitHub

2. **"Authentication failed"**:
   - Clear credential cache: `git credential-cache exit`
   - Re-enter credentials

3. **"Connection timeout"**:
   - Check internet connection
   - Verify GitHub status

### Quick Fixes:

```bash
# Reset credentials
git config --global --unset credential.helper
git config --global credential.helper store

# Test connection
git ls-remote https://github.com/Shakour-Data/AutoProjectManagement.git HEAD
```

## 🔄 Verification Commands

```bash
# Check current configuration
git config --list | grep -E "(user|remote|credential)"

# Test authentication
git push origin Documentation --dry-run

# Verify SSH
ssh -T git@github.com
```

## 📞 Support

If issues persist:
1. Check GitHub status: https://www.githubstatus.com/
2. Review GitHub docs: https://docs.github.com/en/authentication
3. Contact support if needed
