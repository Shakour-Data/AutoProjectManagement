# Organization Plan for AutoProjectManagement

## Current Issues Identified:
1. **Duplicate files** - Many files exist both in main_modules root and subdirectories
2. **Inconsistent naming** - Some files have "_refactored" suffix while others don't
3. **Mixed organization** - Some modules are organized in subdirectories while others are in root
4. **Backup files** - project_management_system.py.backup should be removed or archived

## Phase 1: File Cleanup and Consolidation

### Remove Duplicate Files:
- [ ] Remove duplicate files from main_modules root that exist in subdirectories:
  - `check_progress_dashboard_update.py` (exists in progress_reporting/)
  - `commit_progress_manager.py` (exists in quality_commit_management/)
  - `communication_management.py` (exists in communication_risk/)
  - `communication_risk_doc_integration.py` (exists in communication_risk/)
  - `dashboards_reports.py` (exists in progress_reporting/)
  - `db_data_collector.py` (exists in data_collection_processing/)
  - `do_important_tasks.py` (exists in task_workflow_management/)
  - `do_urgent_tasks.py` (exists in task_workflow_management/)
  - `estimation_management.py` (exists in planning_estimation/)
  - `git_progress_updater.py` (exists in quality_commit_management/)
  - `github_actions_automation.py` (exists in quality_commit_management/)
  - `input_handler.py` (exists in data_collection_processing/)
  - `progress_report.py` (exists in progress_reporting/)
  - `quality_management.py` (exists in quality_commit_management/)
  - `reporting.py` (exists in progress_reporting/)
  - `resource_allocation_manager.py` (exists in resource_management/)
  - `resource_leveling.py` (exists in resource_management/)
  - `resource_management.py` (exists in resource_management/)
  - `risk_management.py` (exists in communication_risk/)
  - `scheduler.py` (exists in planning_estimation/)
  - `scope_management.py` (exists in planning_estimation/)
  - `task_executor.py` (exists in task_workflow_management/)
  - `task_management_integration.py` (exists in task_workflow_management/)
  - `task_management.py` (exists in task_workflow_management/)
  - `wbs_aggregator.py` (exists in planning_estimation/)
  - `wbs_merger.py` (exists in planning_estimation/)
  - `wbs_parser.py` (exists in planning_estimation/)
  - `workflow_data_collector.py` (exists in data_collection_processing/)

### Remove Backup Files:
- [ ] Remove `project_management_system.py.backup`

### Standardize Naming:
- [ ] Rename refactored files to remove "_refactored" suffix:
  - `importance_urgency_calculator_refactored.py` → `importance_urgency_calculator.py`
  - `progress_calculator_refactored.py` → `progress_calculator.py`
  - `progress_data_generator_refactored.py` → `progress_data_generator.py`

## Phase 2: Directory Structure Optimization

### Organize Remaining Root Files:
- [ ] Move remaining files to appropriate subdirectories:
  - `feature_weights.py` → `utility_modules/`
  - `gantt_chart_data.py` → `planning_estimation/`
  - `project_views_generator.py` → `utility_modules/`
  - `setup_automation.py` → `utility_modules/`
  - `setup_initialization.py` → `utility_modules/`
  - `time_management.py` → `utility_modules/`

### Create Missing Subdirectories:
- [ ] Create `project_management/` directory for core project management files
- [ ] Move `project_management_system.py` to `project_management/`

### Services Organization:
- [ ] Review services structure and ensure consistent organization
- [ ] Move core services to appropriate subdirectories

## Phase 3: Import Updates and Testing

### Update Imports:
- [ ] Update all import statements to reflect new file locations
- [ ] Check for circular imports and resolve them

### Comprehensive Testing:
- [ ] Run all tests to ensure functionality is preserved
- [ ] Fix any broken references
- [ ] Verify no functionality loss

## Phase 4: Documentation and Cleanup

### Update Documentation:
- [ ] Update README.md with new file structure
- [ ] Ensure all modules have proper docstrings
- [ ] Create architecture documentation

### Final Cleanup:
- [ ] Remove empty directories
- [ ] Clean up __pycache__ directories
- [ ] Verify all file paths in configuration files

## Priority Order:
1. Remove duplicate files (highest priority - reduces confusion)
2. Remove backup files
3. Standardize naming
4. Organize remaining files
5. Update imports
6. Test functionality
7. Update documentation

## Notes:
- Always backup before making changes
- Test each change incrementally
- Use git to track changes and revert if needed
- Document any breaking changes
