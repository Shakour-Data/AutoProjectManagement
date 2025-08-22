#!/usr/bin/env python3
"""
Command Line Interface for AutoProjectManagement - Comprehensive CLI for automated project management.

This module provides a complete command-line interface for the AutoProjectManagement system,
offering intuitive commands for project initialization, task management, progress tracking,
and system administration. The CLI is built using Click framework for robust argument parsing
and user-friendly interaction.

Key Features:
    - Project initialization and setup
    - Task and resource management
    - Progress tracking and reporting
    - Git integration and automation
    - Configuration management
    - System status monitoring
    - Export/import capabilities

Usage:
    Basic CLI usage:
        $ autoprojectmanagement --help
        $ autoprojectmanagement init --path /path/to/project
        $ autoprojectmanagement create-project "My New Project"
        $ autoprojectmanagement status --project-id 12345

    Advanced usage:
        $ autoprojectmanagement add-task --project-id 12345 --task-name "Implement feature" --priority high
        $ autoprojectmanagement report --project-id 12345 --format markdown --output report.md

Configuration:
    The CLI supports configuration through:
    - Environment variables (AUTO_* prefix)
    - Configuration files (.auto_project/config/cli_config.json)
    - Command line arguments

Examples:
    Initialize a new project:
        >>> autoprojectmanagement init --path ./my-project --verbose

    Create and manage tasks:
        >>> autoprojectmanagement create-project "Web Application"
        >>> autoprojectmanagement add-task --project-id 1 --task-name "Setup database" --priority high

    Generate reports:
        >>> autoprojectmanagement report --project-id 1 --format json --output progress.json

For more information, visit: https://github.com/AutoProjectManagement/AutoProjectManagement
"""

import argparse
import logging
import os
import sys
import time
from typing import Optional, Dict, Any, List
from pathlib import Path

import click

from .main_modules.project_management_system import ProjectManagementSystem
from autoprojectmanagement.services.configuration_cli.cli_commands import CLICommands


# Configure logging for CLI
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version="1.0.0", prog_name="AutoProjectManagement")
def main() -> None:
    """
    AutoProjectManagement - Automated Project Management System CLI
    
    A comprehensive command-line interface for automated project management,
    task tracking, and workflow optimization for software development teams.
    
    Features:
    - Project initialization and setup
    - Task and resource management
    - Progress tracking and reporting
    - Git integration and automation
    - Configuration management
    
    Examples:
        autoprojectmanagement init --path /path/to/project
        autoprojectmanagement create-project "My New Project"
        autoprojectmanagement status --project-id 12345
    """
    pass


@main.command()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def init(config: Optional[str], verbose: bool) -> None:
    """
    Initialize a new project management system.
    
    This command sets up a new AutoProjectManagement system with all necessary
    configurations, directories, and initial settings for automated project
    management.
    
    Args:
        config: Path to configuration file (optional)
        verbose: Enable verbose output for detailed setup information
    
    Examples:
        autoprojectmanagement init
        autoprojectmanagement init --path ./my-project
        autoprojectmanagement init --config custom_config.json --verbose
    
    Returns:
        None
    
    Raises:
        ValueError: If configuration is invalid
        OSError: If unable to create required directories
    """
    click.echo("🚀 Initializing AutoProjectManagement...")
    
    if verbose:
        click.echo(f"Configuration file: {config or 'default'}")
    
    # Initialize the system
    system = ProjectManagementSystem()
    system.initialize_system()
    
    click.echo("✅ AutoProjectManagement initialized successfully!")


@main.command()
@click.argument('project_name')
@click.option('--description', '-d', help='Project description')
@click.option('--template', '-t', help='Project template to use')
def create_project(
    project_name: str,
    description: Optional[str],
    template: Optional[str]
) -> None:
    """
    Create a new project with automated management capabilities.
    
    This command creates a new project with all necessary structure and
    configurations for automated project management.
    
    Args:
        project_name: Name of the project to create
        description: Optional project description
        template: Optional template to use for project structure
    
    Examples:
        autoprojectmanagement create-project "Web Application"
        autoprojectmanagement create-project "API Service" --description "RESTful API for mobile app"
        autoprojectmanagement create-project "Data Pipeline" --template python
    
    Returns:
        None
    
    Raises:
        ValueError: If project name is invalid
        OSError: If unable to create project directory
    """
    click.echo(f"📁 Creating project: {project_name}")
    
    cli_commands = CLICommands()
    success = cli_commands.create_project(
        project_name,
        description,
        template
    )
    
    if success:
        click.echo(f"✅ Project '{project_name}' created successfully!")
    else:
        click.echo(
            f"❌ Failed to create project '{project_name}'",
            err=True
        )
        sys.exit(1)


@main.command()
@click.argument('project_id')
@click.option(
    '--format',
    '-f',
    type=click.Choice(['json', 'markdown', 'table']),
    default='table',
    help='Output format for status display'
)
def status(project_id: str, format: str) -> None:
    """
    Show comprehensive project status and progress.
    
    This command displays detailed information about project progress,
    task completion, resource allocation, and overall health.
    
    Args:
        project_id: ID of the project to check
        format: Output format (json, markdown, or table)
    
    Examples:
        autoprojectmanagement status 12345
        autoprojectmanagement status 12345 --format json
        autoprojectmanagement status 12345 --format markdown
    
    Returns:
        None
    
    Raises:
        ValueError: If project ID is invalid
        OSError: If unable to access project data
    """
    click.echo(f"📊 Project {project_id} status:")
    
    cli_commands = CLICommands()
    status_data = cli_commands.get_project_status(project_id, format)
    
    if status_data:
        click.echo(status_data)
    else:
        click.echo(f"❌ Project {project_id} not found", err=True)
        sys.exit(1)


@main.command()
@click.argument('project_id')
@click.option('--task-name', '-n', required=True, help='Task name')
@click.option(
    '--priority',
    '-p',
    type=click.Choice(['low', 'medium', 'high', 'urgent']),
    default='medium',
    help='Task priority level'
)
@click.option('--description', '-d', help='Task description')
@click.option('--assignee', '-a', help='Task assignee')
@click.option('--due-date', help='Task due date (YYYY-MM-DD)')
def add_task(
    project_id: str,
    task_name: str,
    priority: str,
    description: Optional[str],
    assignee: Optional[str],
    due_date: Optional[str]
) -> None:
    """
    Add a new task to an existing project.
    
    This command adds a new task with specified properties to an existing
    project, enabling automated task management and tracking.
    
    Args:
        project_id: ID of the project to add task to
        task_name: Name of the task to add
        priority: Priority level (low, medium, high, urgent)
        description: Optional task description
        assignee: Optional task assignee
        due_date: Optional due date in YYYY-MM-DD format
    
    Examples:
        autoprojectmanagement add-task 12345 --task-name "Implement feature" --priority high
        autoprojectmanagement add-task 12345 --task-name "Fix bug" --priority urgent --assignee "John Doe"
        autoprojectmanagement add-task 12345 --task-name "Update docs" --priority medium --due-date 2024-12-31
    
    Returns:
        None
    
    Raises:
        ValueError: If task parameters are invalid
        OSError: If unable to add task to project
    """
    click.echo(f"📝 Adding task '{task_name}' to project {project_id}")
    
    cli_commands = CLICommands()
    success = cli_commands.add_task(
        project_id,
        task_name,
        priority,
        description,
        assignee,
        due_date
    )
    
    if success:
        click.echo(f"✅ Task '{task_name}' added successfully!")
    else:
        click.echo("❌ Failed to add task", err=True)
        sys.exit(1)


@main.command()
@click.argument('project_id')
@click.option(
    '--report-type',
    '-t',
    type=click.Choice(['summary', 'detailed', 'gantt', 'burndown']),
    default='summary',
    help='Type of report to generate'
)
@click.option('--output', '-o', help='Output file path (optional)')
@click.option('--format', '-f', type=click.Choice(['json', 'markdown', 'html']), default='markdown', help='Report format')
def report(
    project_id: str,
    report_type: str,
    output: Optional[str],
    format: str
) -> None:
    """
    Generate comprehensive project reports.
    
    This command generates detailed reports about project progress,
    task completion, resource utilization, and overall project health.
    
    Args:
        project_id: ID of the project to generate report for
        report_type: Type of report (summary, detailed, gantt, burndown)
        output: Optional output file path
        format: Report format (json, markdown, or html)
    
    Examples:
        autoprojectmanagement report 12345
        autoprojectmanagement report 12345 --type detailed --format json
        autoprojectmanagement report 12345 --type gantt --output gantt_report.html
    
    Returns:
        None
    
    Raises:
        ValueError: If report parameters are invalid
        OSError: If unable to generate report
    """
    click.echo(
        f"📊 Generating {report_type} report for project {project_id}"
    )
    
    cli_commands = CLICommands()
    report_content = cli_commands.generate_report(project_id, report_type, format)
    
    if report_content:
        if output:
            from pathlib import Path
            Path(output).write_text(report_content)
            click.echo(f"✅ Report saved to {output}")
        else:
            click.echo(report_content)
    else:
        click.echo("❌ Failed to generate report", err=True)
        sys.exit(1)


@main.command()
@click.argument('project_id')
@click.argument('task_id')
@click.option('--new-status', type=click.Choice(['todo', 'in_progress', 'done', 'blocked']), required=True)
def update_task_status(project_id: str, task_id: str, new_status: str) -> None:
    """
    Update the status of an existing task.
    
    This command allows updating the status of tasks within a project,
    enabling dynamic task management and progress tracking.
    
    Args:
        project_id: ID of the project containing the task
        task_id: ID of the task to update
        new_status: New status (todo, in_progress, done, blocked)
    
    Examples:
        autoprojectmanagement update-task-status 12345 67890 --new-status done
        autoprojectmanagement update-task-status 12345 67891 --new-status in_progress
    
    Returns:
        None
    
    Raises:
        ValueError: If status is invalid
        OSError: If unable to update task
    """
    click.echo(f"🔄 Updating task {task_id} status to {new_status}")
    
    cli_commands = CLICommands()
    success = cli_commands.update_task_status(project_id, task_id, new_status)
    
    if success:
        click.echo(f"✅ Task {task_id} status updated to {new_status}")
    else:
        click.echo("❌ Failed to update task status", err=True)
        sys.exit(1)


@main.command()
@click.option('--list', '-l', is_flag=True, help='List all available commands')
@click.option('--help', '-h', isflag=True, help='Show this help message')
def help_command(list_commands: bool, help_flag: bool) -> None:
    """
    Show help information for the CLI.
    
    This command provides detailed help information about available commands
    and their usage.
    
    Args:
        list_commands: List all available commands
        help_flag: Show help message
    
    Examples:
        autoprojectmanagement help
        autoprojectmanagement help --list
    
    Returns:
        None
    """
    if list_commands:
        click.echo("Available commands:")
        click.echo("  init              - Initialize new project management system")
        click.echo("  create-project    - Create new project")
        click.echo("  status            - Show project status")
        click.echo("  add-task          - Add new task to project")
        click.echo("  report            - Generate project reports")
        click.echo("  update-task-status - Update task status")
        click.echo("  dashboard         - Manage dashboard (start, stop, open, status)")
        click.echo("  help              - Show help information")


if __name__ == "__main__":
    main()
