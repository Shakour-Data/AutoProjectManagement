# AutoCommit File Consolidation Plan

## Goal: Create a unified auto_commit.py that combines the best features from both versions

### Steps to Complete:

1. [ ] Create unified version in automation_services/auto_commit.py
   - [ ] Keep robust authentication from new version
   - [ ] Keep guaranteed push execution from new version
   - [ ] Migrate project management integration from old version
   - [ ] Migrate WBS integration from old version
   - [ ] Migrate progress tracking from old version

2. [ ] Update test file to test unified version
   - [ ] Update imports in test_auto_commit.py
   - [ ] Update test cases for new unified class

3. [ ] Remove old file
   - [ ] Delete services/auto_commit.py
   - [ ] Verify no other dependencies

4. [ ] Testing
   - [ ] Run tests to ensure functionality
   - [ ] Verify authentication works
   - [ ] Verify project management integration works

### Features to Migrate from Old Version:
- format_commit_message function
- WBS resource loading and task finding
- Progress change calculation
- Importance and urgency calculation
- Commit task database updating
- Progress data collection and JSON writing

### Features to Keep from New Version:
- Authentication setup (SSH/HTTPS/PAT)
- Guaranteed push execution with multiple strategies
- Better error handling and logging
- Simplified staging and committing
