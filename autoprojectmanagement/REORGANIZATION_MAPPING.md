# Folder Reorganization Mapping

## Overview
This document maps the reorganization of the AutoProjectManagement folder structure according to the provided categories.

## 📁 Main Modules Reorganization

### Task & Workflow Management
- **Location**: `main_modules/task_workflow_management/`
- **Modules**:
  - `check_progress_dashboard_update.py`
  - `do_important_tasks.py`
  - `do_urgent_tasks.py`
  - `task_management.py`

### Progress & Reporting
- **Location**: `main_modules/progress_reporting/`
- **Modules**:
  - `progress_calculator_refactored.py`
  - `progress_data_generator_refactored.py`
  - `progress_report.py`
  - `dashboards_reports.py`

### Data Collection & Processing
- **Location**: `main_modules/data_collection_processing/`
- **Modules**:
  - `db_data_collector.py`
  - `input_handler.py`
  - `git_progress_updater.py`

### Planning & Estimation
- **Location**: `main_modules/planning_estimation/`
- **Modules**:
  - `estimation_management.py`
  - `gantt_chart_data.py`
  - `feature_weights.py`
  - `wbs_parser.py`
  - `wbs_aggregator.py`
  - `wbs_merger.py`

### Communication & Risk
- **Location**: `main_modules/communication_risk/`
- **Modules**:
  - `communication_management.py`
  - `communication_risk_doc_integration.py`
  - `risk_management.py`

### Resource Management
- **Location**: `main_modules/resource_management/`
- **Modules**:
  - `resource_management.py`
  - `resource_allocation_manager.py`
  - `resource_leveling.py`

### Quality & Commit Management
- **Location**: `main_modules/quality_commit_management/`
- **Modules**:
  - `commit_progress_manager.py`
  - `quality_management.py`

### Utility Modules
- **Location**: `main_modules/utility_modules/`
- **Modules**:
  - `importance_urgency_calculator_refactored.py`
  - `extend_database_for_scrum.py`

## 🔧 Services Reorganization

### Automation Services
- **Location**: `services/automation_services/`
- **Services**:
  - `auto_commit.py`
  - `backup_manager.py`
  - `documentation_automation.py`

### Integration Services
- **Location**: `services/integration_services/`
- **Services**:
  - `github_integration.py`
  - `integration_manager.py`
  - `vscode_extension_installer.py`

### Configuration & CLI
- **Location**: `services/configuration_cli/`
- **Services**:
  - `cli_commands.py`
  - `config_and_token_management.py`
  - `json_data_linker.py`

## Migration Script

To migrate existing files to the new structure, use the following commands:

```bash
# Main Modules Migration
mv autoprojectmanagement/main_modules/check_progress_dashboard_update.py autoprojectmanagement/main_modules/task_workflow_management/
mv autoprojectmanagement/main_modules/do_important_tasks.py autoprojectmanagement/main_modules/task_workflow_management/
mv autoprojectmanagement/main_modules/do_urgent_tasks.py autoprojectmanagement/main_modules/task_workflow_management/
mv autoprojectmanagement/main_modules/task_management.py autoprojectmanagement/main_modules/task_workflow_management/

mv autoprojectmanagement/main_modules/progress_calculator_refactored.py autoprojectmanagement/main_modules/progress_reporting/
mv autoprojectmanagement/main_modules/progress_data_generator_refactored.py autoprojectmanagement/main_modules/progress_reporting/
mv autoprojectmanagement/main_modules/progress_report.py autoprojectmanagement/main_modules/progress_reporting/
mv autoprojectmanagement/main_modules/dashboards_reports.py autoprojectmanagement/main_modules/progress_reporting/

mv autoprojectmanagement/main_modules/db_data_collector.py autoprojectmanagement/main_modules/data_collection_processing/
mv autoprojectmanagement/main_modules/input_handler.py autoprojectmanagement/main_modules/data_collection_processing/
mv autoprojectmanagement/main_modules/git_progress_updater.py autoprojectmanagement/main_modules/data_collection_processing/

mv autoprojectmanagement/main_modules/estimation_management.py autoprojectmanagement/main_modules/planning_estimation/
mv autoprojectmanagement/main_modules/gantt_chart_data.py autoprojectmanagement/main_modules/planning_estimation/
mv autoprojectmanagement/main_modules/feature_weights.py autoprojectmanagement/main_modules/planning_estimation/
mv autoprojectmanagement/main_modules/wbs_parser.py autoprojectmanagement/main_modules/planning_estimation/
mv autoprojectmanagement/main_modules/wbs_aggregator.py autoprojectmanagement/main_modules/planning_estimation/
mv autoprojectmanagement/main_modules/wbs_merger.py autoprojectmanagement/main_modules/planning_estimation/

mv autoprojectmanagement/main_modules/communication_management.py autoprojectmanagement/main_modules/communication_risk/
mv autoprojectmanagement/main_modules/communication_risk_doc_integration.py autoprojectmanagement/main_modules/communication_risk/
mv autoprojectmanagement/main_modules/risk_management.py autoprojectmanagement/main_modules/communication_risk/

mv autoprojectmanagement/main_modules/resource_management.py autoprojectmanagement/main_modules/resource_management/
mv autoprojectmanagement/main_modules/resource_allocation_manager.py autoprojectmanagement/main_modules/resource_management/
mv autoprojectmanagement/main_modules/resource_leveling.py autoprojectmanagement/main_modules/resource_management/

mv autoprojectmanagement/main_modules/commit_progress_manager.py autoprojectmanagement/main_modules/quality_commit_management/
mv autoprojectmanagement/main_modules/quality_management.py autoprojectmanagement/main_modules/quality_commit_management/

# Services Migration
mv autoprojectmanagement/services/auto_commit.py autoprojectmanagement/services/automation_services/
mv autoprojectmanagement/services/backup_manager.py autoprojectmanagement/services/automation_services/
mv autoprojectmanagement/services/documentation_automation.py autoprojectmanagement/services/automation_services/

mv autoprojectmanagement/services/github_integration.py autoprojectmanagement/services/integration_services/
mv autoprojectmanagement/services/integration_manager.py autoprojectmanagement/services/integration_services/
mv autoprojectmanagement/services/vscode_extension_installer.py autoprojectmanagement/services/integration_services/

mv autoprojectmanagement/services/cli_commands.py autoprojectmanagement/services/configuration_cli/
mv autoprojectmanagement/services/config_and_token_management.py autoprojectmanagement/services/configuration_cli/
mv autoprojectmanagement/services/json_data_linker.py autoprojectmanagement/services/configuration_cli/
```

## Import Updates

After migration, update the import statements in the main __init__.py files to reflect the new structure.
