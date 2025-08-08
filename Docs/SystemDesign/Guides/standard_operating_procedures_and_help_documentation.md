# Standard Operating Procedures and Help Documentation

*Last updated: 2025-07-27*

## Overview

The ProjectManagement system is a Python-based automation tool designed to streamline software project management. It integrates with GitHub and Visual Studio Code (VS Code) to automate task management, progress tracking, resource allocation, and reporting.

## Installation

- Install the package using pip or from source.
- Use the provided setup scripts (`scripts/setup_env.sh` and `scripts/setup_interactive.py`) to prepare the environment and input data.
- The frontend Setup Wizard guides users through project initialization, including Git repository setup, virtual environment creation, and dependency installation.

## Usage

- Use the CLI commands to install, setup, start, and check the status of the project management system.
- Provide JSON input files defining the Work Breakdown Structure (WBS), workflow, resources, and allocations.
- Interact with the system via the VS Code chat interface for natural language task management.
- The JSON File Upload Wizard assists users in uploading and validating required JSON input files.
- The system automatically aggregates WBS parts and generates Gantt chart data.

## Commands

- `install`: Sets up the project directory and input files.
- `setup`: Validates inputs and prepares the environment.
- `start`: Starts the automation processes.
- `status`: Displays the current status of the project management system.
- `help`: Displays this help document.

## Input Files

Required JSON files include:

- detailed_wbs.json
- workflow_definition.json
- resource_allocation.json
- task_resource_allocation.json
- wbs_data.json
- wbs_scores.json
- human_resources.json (created interactively)

## Reports and Outputs

- The system generates progress reports, dashboards, and changelogs.
- Outputs are saved in designated directories for review.
- Reports and dashboards are accessible via the VS Code extension and GitHub Projects.

## Troubleshooting

- Ensure all required JSON input files are present and valid.
- Use the interactive setup script to enter human resources data.
- Check the virtual environment is activated before running commands.
- Review logs for errors during automation.
- Verify JSON files conform to defined standards.

## Support

For further assistance, refer to the comprehensive documentation in the `Docs/` directory or contact the development team.
