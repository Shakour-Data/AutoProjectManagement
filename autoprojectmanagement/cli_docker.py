#!/usr/bin/env python3
"""
Docker-specific CLI commands for AutoProjectManagement
"""

import click
import sys
from pathlib import Path

from autoprojectmanagement.docker_setup import DockerSetup


@click.group()
@click.version_option(version="1.0.0", prog_name="AutoProjectManagement Docker")
def docker_cli():
    """AutoProjectManagement Docker Management CLI"""
    pass


@docker_cli.command()
@click.option('--env', type=click.Choice(['development', 'production']), 
              help='Environment to setup')
@click.option('--auto/--no-auto', default=True, 
              help='Auto-detect environment if not specified')
def setup(env, auto):
    """Setup Docker environment automatically"""
    docker_setup = DockerSetup()
    
    if not env and auto:
        env = docker_setup.detect_environment()
    
    click.echo(f"Setting up Docker for {env} environment...")
    
    if docker_setup.setup_docker(env):
        click.echo("✓ Docker setup completed successfully!")
    else:
        click.echo("✗ Docker setup failed", err=True)
        sys.exit(1)


@docker_cli.command()
@click.option('--env', type=click.Choice(['development', 'production']), 
              help='Environment to start')
def start(env):
    """Start Docker services"""
    docker_setup = DockerSetup()
    
    if not env:
        env = docker_setup.detect_environment()
    
    if docker_setup.start_services(env):
        click.echo(f"✓ Services started for {env} environment")
    else:
        click.echo("✗ Failed to start services", err=True)
        sys.exit(1)


@docker_cli.command()
@click.option('--env', type=click.Choice(['development', 'production']), 
              help='Environment to stop')
def stop(env):
    """Stop Docker services"""
    docker_setup = DockerSetup()
    
    if not env:
        env = docker_setup.detect_environment()
    
    if docker_setup.stop_services(env):
        click.echo(f"✓ Services stopped for {env} environment")
    else:
        click.echo("✗ Failed to stop services", err=True)
        sys.exit(1)


@docker_cli.command()
@click.option('--env', type=click.Choice(['development', 'production']), 
              help='Environment to check')
def status(env):
    """Show Docker services status"""
    docker_setup = DockerSetup()
    
    if not env:
        env = docker_setup.detect_environment()
    
    docker_setup.show_status(env)


@docker_cli.command()
def install():
    """Install Docker CLI tools"""
    docker_setup = DockerSetup()
    
    if docker_setup.install_docker_cli():
        click.echo("✓ Docker CLI tools installed successfully")
    else:
        click.echo("✗ Failed to install Docker CLI tools", err=True)
        click.echo("Please install Docker manually from https://docs.docker.com/get-docker/")


if __name__ == "__main__":
    docker_cli()
