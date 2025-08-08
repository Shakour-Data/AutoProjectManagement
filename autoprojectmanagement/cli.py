#!/usr/bin/env python3
"""
Command Line Interface for AutoProjectManagement
"""

import click
import sys
from pathlib import Path

from .main_modules.project_management_system import ProjectManagementSystem
from .services.cli_commands import CLICommands


@click.group()
@click.version_option(version="1.0.0", prog_name="AutoProjectManagement")
def main():
    """AutoProjectManagement - Automated Project Management System CLI"""
    pass


@main.command()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def init(config, verbose):
    """Initialize a new project management system"""
    click.echo("🚀 Initializing AutoProjectManagement...")
    
    if verbose:
        click.echo("Configuration file: {}".format(config or "default"))
    
    # Initialize the system
    system = ProjectManagementSystem()
    system.initialize_system()
    
    click.echo("✅ AutoProjectManagement initialized successfully!")


@main.command()
@click.argument('project_name')
@click.option('--description', '-d', help='Project description')
@click.option('--template', '-t', help='Project template to use')
def create_project(project_name, description, template):
    """Create a new project"""
    click.echo(f"📁 Creating project: {project_name}")
    
    # Implementation for project creation
    cli_commands = CLICommands()
    success = cli_commands.create_project(project_name, description, template)
    
    if success:
        click.echo(f"✅ Project '{project_name}' created successfully!")
    else:
        click.echo(f"❌ Failed to create project '{project_name}'", err=True)
        sys.exit(1)


@main.command()
@click.argument('project_id')
@click.option('--format', '-f', type=click.Choice(['json', 'markdown', 'table']), 
              default='table', help='Output format')
def status(project_id, format):
    """Show project status"""
    click.echo(f"📊 Project {project_id} status:")
    
    # Implementation for status display
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
@click.option('--priority', '-p', type=click.Choice(['low', 'medium', 'high', 'urgent']),
              default='medium', help='Task priority')
@click.option('--description', '-d', help='Task description')
def add_task(project_id, task_name, priority, description):
    """Add a new task to a project"""
    click.echo(f"📝 Adding task '{task_name}' to project {project_id}")
    
    cli_commands = CLICommands()
    success = cli_commands.add_task(project_id, task_name, priority, description)
    
    if success:
        click.echo(f"✅ Task '{task_name}' added successfully!")
    else:
        click.echo(f"❌ Failed to add task", err=True)
        sys.exit(1)


@main.command()
@click.argument('project_id')
@click.option('--report-type', '-t', type=click.Choice(['summary', 'detailed', 'gantt']),
              default='summary', help='Type of report to generate')
@click.option('--output', '-o', help='Output file path')
def report(project_id, report_type, output):
    """Generate project reports"""
    click.echo(f"📊 Generating {report_type} report for project {project_id}")
    
    cli_commands = CLICommands()
    report_content = cli_commands.generate_report(project_id, report_type)
    
    if report_content:
        if output:
            Path(output).write_text(report_content)
            click.echo(f"✅ Report saved to {output}")
        else:
            click.echo(report_content)
    else:
        click.echo(f"❌ Failed to generate report", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
