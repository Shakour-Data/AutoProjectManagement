# Project Restructuring Plan - Detailed Tasks

## 1. Root Level Structure Reorganization

### Current Issues:
- Mixed configuration files, scripts, and source code at root level
- Inconsistent naming conventions
- No clear separation of concerns

### Tasks:
- [x] Create `src/` directory for all source code
- [x] Create `config/` directory for configuration files
- [x] Create `scripts/` directory for utility scripts
- [x] Create `docs/` directory for documentation
- [x] Create `tests/` directory for test files
- [x] Create `deploy/` directory for deployment-related files

## 2. Source Code Organization (`src/`)

### Current Structure Issues:
- Mixed Python packages with different naming conventions
- Inconsistent module organization

### Tasks:
- [x] Move `autoprojectmanagement/` to `src/autoprojectmanagement/`
- [x] Move `autopro极management/` to `src/autopro_management/` (with proper ASCII naming)
- [x] Standardize package naming to use underscores instead of mixed case
- [x] Create clear module boundaries:
  - `src/core/` - Core functionality
  - `src/api/` - API endpoints and services
  - `src/services/` - Business logic services
  - `src/models/` - Data models
  - `src/utils/` - Utility functions
  - `src/cli/` - Command-line interface
- [x] Refactor code as necessary after each move to ensure functionality

## 3. Configuration Files Organization (`config/`)

### Files to Move:
- [x] `backup_config.yaml` → `config/backup.yaml`
- [x] `monitoring_setup.yaml` → `config/monitoring.yaml`
- [x] `pyproject.toml` → Keep at root (standard for Python projects)
- [x] `requirements.txt` → Keep at root (standard for Python projects)
- [x] `requirements-dev.txt` → Keep at root
- [x] Create `config/database.yaml` for database configurations
- [x] Create `config/api.yaml` for API configurations
- [x] Refactor code as necessary after each move to ensure functionality

## 4. Scripts Organization (`scripts/`)

### Files to Move:
- [x] `setup_env.sh` → `scripts/setup/env.sh`
- [x] `setup_github_auth.sh` → `scripts/setup/github_auth.sh`
- [x] `setup_status_bar.sh` → `scripts/setup/status_bar.sh`
- [x] `start_auto_management.sh` → `scripts/management/start.sh`
- [x] `status_auto_management.sh` → `scripts/management/status.sh`
- [x] `stop_auto_management.sh` → `scripts/management/stop.sh`
- [x] `docker_git_troubleshoot.sh` → `scripts/docker/troubleshoot.sh`
- [x] `fix_docker_dns.sh` → `scripts/docker/fix_dns.sh`
- [x] `fix_git_auth.sh` → `scripts/git/fix_auth.sh`
- [x] `git-merge-changes.sh` → `scripts/git/merge_changes.sh`
- [x] `optimize_git_config.sh` → `scripts/git/optimize_config.sh`
- [x] Refactor code as necessary after each move to ensure functionality

## 5. Documentation Organization (`docs/`)

### Current Structure Issues:
- Mixed documentation files in multiple locations

### Tasks:
- [x] Move all `Docs/` content to `docs/`
- [x] Organize documentation by category:
  - `docs/architecture/` - System architecture
  - `docs/api/` - API documentation
  - `docs/deployment/` - Deployment guides
  - `docs/design/` - Design documentation
  - `docs/development/` - Development guides
  - `docs/modules/` - Module documentation
  - `docs/requirements/` - Requirements documentation
  - `docs/testing/` - Testing documentation

## 6. Test Organization (`tests/`)

### Current Structure Issues:
- Mixed test files with different naming conventions

### Tasks:
- [x] Organize tests by module:
  - `tests/unit/` - Unit tests
  - `tests/integration/` - Integration tests
  - `tests/e2e/` - End-to-end tests
  - `tests/fixtures/` - Test fixtures
- [x] Use consistent naming: `test_*.py` for test files

## 7. Data Storage Organization

### Current Issues:
- Mixed data files in multiple locations

### Tasks:
- [x] Move `user_data/` to `data/user/`
- [x] Move `JSonDataBase/` to `data/json/`
- [x] Move `backups/` to `data/backups/`
- [x] Create `data/temp/` for temporary files
- [x] Create `data/logs/` for log files

## 8. Docker Organization (`docker/`)

### Current Structure is good, but needs cleanup:
- [x] Standardize Dockerfile naming conventions
- [x] Create `docker/nginx/` for nginx configurations
- [x] Create `docker/compose/` for docker-compose files
- [x] Move docker-compose files to `docker/compose/`

## 9. Virtual Environment Management

### Tasks:
- [x] Ensure `venv/` is in `.gitignore`
- [x] Create `requirements/` directory with:
  - `requirements/base.txt` - Core dependencies
  - `requirements/dev.txt` - Development dependencies
  - `requirements/prod.txt` - Production dependencies
  - `requirements/test.txt` - Test dependencies

## 10. Git and Version Control

### Tasks:
- [x] Review and update `.gitignore` for new structure
- [x] Ensure all configuration templates are properly handled
- [x] Create `.github/` directory for GitHub-specific files
- [x] Organize GitHub workflows in `.github/workflows/`

## 11. Naming Convention Standardization

### Rules to Implement:
- Use lowercase with underscores for file names: `file_name.py`
- Use PascalCase for class names: `ClassName`
- Use snake_case for function and variable names: `function_name`
- Use descriptive names that indicate purpose
- Avoid special characters in file names

## 12. Implementation Priority

### Phase 1 (High Priority):
- Create new directory structure
- Move configuration files
- Organize scripts
- Update import paths

### Phase 2 (Medium Priority):
- Reorganize source code
- Standardize naming conventions
- Update documentation

### Phase 3 (Low Priority):
- Optimize Docker setup
- Enhance test organization
- Final cleanup and verification

## 13. Verification Steps

After restructuring:
- [ ] Run all tests to ensure functionality
- [ ] Verify all imports work correctly
- [ ] Check that all scripts execute properly
- [ ] Ensure documentation links are updated
- [ ] Verify deployment still works

This comprehensive restructuring will create a professional, maintainable codebase that follows industry best practices.
