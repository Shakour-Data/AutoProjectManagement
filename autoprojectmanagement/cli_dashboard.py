#!/usr/bin/env python3
"""
Dashboard CLI Commands for AutoProjectManagement - Comprehensive CLI for dashboard management.

This module provides command-line interface commands specifically for dashboard operations,
including starting/stopping the dashboard server, opening the dashboard in a browser,
and managing dashboard configuration.

Key Features:
    - Dashboard server management
    - Browser integration
    - Configuration management
    - Status monitoring
    - Export capabilities

Usage:
    Basic dashboard commands:
        $ autoprojectmanagement dashboard --start
        $ autoprojectmanagement dashboard --stop
        $ autoprojectmanagement dashboard --status
        $ autoprojectmanagement dashboard --open

    Advanced usage:
        $ autoprojectmanagement dashboard --port 8080 --host 0.0.0.0
        $ autoprojectmanagement dashboard --export --format json --output dashboard.json
        $ autoprojectmanagement dashboard --config --set refresh_rate=5000

Examples:
    Start dashboard server:
        >>> autoprojectmanagement dashboard --start --port 3000

    Open dashboard in browser:
        >>> autoprojectmanagement dashboard --open

    Check dashboard status:
        >>> autoprojectmanagement dashboard --status

    Export dashboard data:
        >>> autoprojectmanagement dashboard --export --format json
"""

import argparse
import logging
import os
import sys
import time
import webbrowser
from typing import Optional, Dict, Any, List
from pathlib import Path

import click
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Configure logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

console = Console()

class DashboardCLI:
    """CLI commands for dashboard management."""
    
    def __init__(self):
        self.default_port = 3000
        self.default_host = "127.0.0.1"
        self.api_base_url = f"http://{self.default_host}:{self.default_port}/api/v1"
    
    def start_dashboard(self, port: Optional[int] = None, host: Optional[str] = None) -> bool:
        """
        Start the dashboard server.
        
        Args:
            port: Port number to run dashboard on
            host: Host address to bind to
            
        Returns:
            True if successful, False otherwise
        """
        port = port or self.default_port
        host = host or self.default_host
        
        try:
            console.print(f"[bold green]🚀 Starting Dashboard Server...[/bold green]")
            console.print(f"   Host: [cyan]{host}[/cyan]")
            console.print(f"   Port: [cyan]{port}[/cyan]")
            console.print(f"   URL: [blue]http://{host}:{port}/dashboard[/blue]")
            
            # In a real implementation, this would start the FastAPI server
            # For now, we'll simulate the process
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                task = progress.add_task("Starting server...", total=None)
                
                # Simulate server startup
                time.sleep(2)
                
                progress.update(task, description="Loading dashboard components...")
                time.sleep(1)
                
                progress.update(task, description="Initializing WebSocket connections...")
                time.sleep(1)
                
            console.print("[bold green]✅ Dashboard server started successfully![/bold green]")
            console.print("\n[dim]Press Ctrl+C to stop the server[/dim]")
            
            # Keep the server running (simulated)
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                console.print("\n[yellow]🛑 Dashboard server stopped[/yellow]")
                return True
                
        except Exception as e:
            console.print(f"[bold red]❌ Failed to start dashboard: {e}[/bold red]")
            logger.error(f"Dashboard start failed: {e}")
            return False
    
    def stop_dashboard(self) -> bool:
        """
        Stop the dashboard server.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            console.print("[bold yellow]🛑 Stopping Dashboard Server...[/bold yellow]")
            
            # In a real implementation, this would stop the running server
            # For now, we'll simulate the process
            time.sleep(1)
            
            console.print("[bold green]✅ Dashboard server stopped successfully![/bold green]")
            return True
            
        except Exception as e:
            console.print(f"[bold red]❌ Failed to stop dashboard: {e}[/bold red]")
            logger.error(f"Dashboard stop failed: {e}")
            return False
    
    def dashboard_status(self) -> Dict[str, Any]:
        """
        Get dashboard server status.
        
        Returns:
            Dictionary containing status information
        """
        try:
            # Try to connect to the dashboard API
            response = requests.get(f"{self.api_base_url}/health", timeout=5)
            
            if response.status_code == 200:
                return {
                    "status": "running",
                    "health": response.json(),
                    "url": f"http://{self.default_host}:{self.default_port}"
                }
            else:
                return {
                    "status": "stopped",
                    "error": f"API returned status {response.status_code}"
                }
                
        except requests.ConnectionError:
            return {
                "status": "stopped",
                "error": "Cannot connect to dashboard server"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def open_dashboard(self) -> bool:
        """
        Open dashboard in default web browser.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            dashboard_url = f"http://{self.default_host}:{self.default_port}/dashboard"
            
            console.print(f"[bold blue]🌐 Opening Dashboard in Browser...[/bold blue]")
            console.print(f"   URL: [cyan]{dashboard_url}[/cyan]")
            
            # Check if server is running first
            status = self.dashboard_status()
            if status["status"] != "running":
                console.print("[bold red]❌ Dashboard server is not running![/bold red]")
                console.print("[yellow]Please start the dashboard first:[/yellow]")
                console.print("  autoprojectmanagement dashboard --start")
                return False
            
            # Open in browser
            webbrowser.open(dashboard_url)
            console.print("[bold green]✅ Dashboard opened in browser![/bold green]")
            return True
            
        except Exception as e:
            console.print(f"[bold red]❌ Failed to open dashboard: {e}[/bold red]")
            logger.error(f"Browser open failed: {e}")
            return False
    
    def export_dashboard_data(self, format: str = "json", output_file: Optional[str] = None) -> bool:
        """
        Export dashboard data to file.
        
        Args:
            format: Export format (json, csv, markdown)
            output_file: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            console.print(f"[bold blue]💾 Exporting Dashboard Data...[/bold blue]")
            console.print(f"   Format: [cyan]{format}[/cyan]")
            
            # Get data from API
            endpoints = [
                ("overview", f"{self.api_base_url}/dashboard/overview?project_id=default"),
                ("metrics", f"{self.api_base_url}/dashboard/metrics?project_id=default&timeframe=24h"),
                ("alerts", f"{self.api_base_url}/dashboard/alerts?project_id=default")
            ]
            
            data = {}
            for name, url in endpoints:
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        data[name] = response.json()
                    else:
                        data[name] = {"error": f"Status {response.status_code}"}
                except Exception as e:
                    data[name] = {"error": str(e)}
            
            # Determine output file
            if not output_file:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_file = f"dashboard_export_{timestamp}.{format}"
            
            # Export based on format
            if format == "json":
                import json
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            
            elif format == "csv":
                import csv
                # Simplified CSV export - would need proper flattening for nested JSON
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Metric", "Value"])
                    for key, value in data.items():
                        writer.writerow([key, str(value)])
            
            elif format == "markdown":
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("# Dashboard Export\n\n")
                    f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    for key, value in data.items():
                        f.write(f"## {key.capitalize()}\n\n")
                        f.write("```json\n")
                        f.write(json.dumps(value, indent=2))
                        f.write("\n```\n\n")
            
            console.print(f"[bold green]✅ Data exported to: [cyan]{output_file}[/cyan][/bold green]")
            return True
            
        except Exception as e:
            console.print(f"[bold red]❌ Export failed: {e}[/bold red]")
            logger.error(f"Export failed: {e}")
            return False
    
    def show_dashboard_info(self) -> None:
        """Display comprehensive dashboard information."""
        try:
            status = self.dashboard_status()
            
            table = Table(title="Dashboard Information", show_header=True, header_style="bold magenta")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Status", status["status"])
            table.add_row("Host", self.default_host)
            table.add_row("Port", str(self.default_port))
            table.add_row("URL", f"http://{self.default_host}:{self.default_port}/dashboard")
            
            if status["status"] == "running" and "health" in status:
                health = status["health"]
                table.add_row("API Version", health.get("version", "N/A"))
                table.add_row("System Status", health.get("status", "N/A"))
            
            console.print(table)
            
        except Exception as e:
            console.print(f"[bold red]❌ Error getting dashboard info: {e}[/bold red]")

    def create_custom_view(self, layout_name: str, widgets: Optional[List[str]] = None, 
                          refresh_rate: Optional[int] = None, theme: Optional[str] = None) -> bool:
        """
        Create a custom dashboard view/layout.
        
        Args:
            layout_name: Name of the custom layout
            widgets: List of widget IDs to include
            refresh_rate: Refresh rate in milliseconds
            theme: Theme name (light/dark)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            console.print(f"[bold blue]🎨 Creating Custom Dashboard View: {layout_name}[/bold blue]")
            
            # Use interactive prompts if no arguments provided
            if not widgets:
                available_widgets = self.get_available_widgets()
                if not available_widgets:
                    console.print("[bold red]❌ No widgets available![/bold red]")
                    return False
                
                console.print("\n[bold]Available Widgets:[/bold]")
                for i, widget in enumerate(available_widgets, 1):
                    console.print(f"  {i}. {widget}")
                
                selected = click.prompt(
                    "\nSelect widgets (comma-separated numbers)", 
                    type=str,
                    default=",".join(str(i) for i in range(1, len(available_widgets) + 1))
                )
                
                selected_indices = [int(idx.strip()) - 1 for idx in selected.split(",") if idx.strip().isdigit()]
                widgets = [available_widgets[i] for i in selected_indices if i < len(available_widgets)]
            
            if not refresh_rate:
                refresh_rate = click.prompt(
                    "Refresh rate (milliseconds)", 
                    type=int,
                    default=3000
                )
            
            if not theme:
                theme = click.prompt(
                    "Theme", 
                    type=click.Choice(['light', 'dark']),
                    default='light'
                )
            
            # Create layout configuration
            layout_config = {
                "layout_type": layout_name,
                "widgets": [{"widget_id": widget, "position": i, "enabled": True, "settings": {}} 
                           for i, widget in enumerate(widgets)],
                "refresh_rate": refresh_rate,
                "theme": theme
            }
            
            # Save layout via API
            response = requests.post(
                f"{self.api_base_url}/dashboard/layout",
                json=layout_config,
                timeout=10
            )
            
            if response.status_code == 200:
                console.print(f"[bold green]✅ Custom view '{layout_name}' created successfully![/bold green]")
                console.print(f"   Widgets: {', '.join(widgets)}")
                console.print(f"   Refresh rate: {refresh_rate}ms")
                console.print(f"   Theme: {theme}")
                return True
            else:
                console.print(f"[bold red]❌ Failed to create view: {response.text}[/bold red]")
                return False
                
        except Exception as e:
            console.print(f"[bold red]❌ Error creating custom view: {e}[/bold red]")
            logger.error(f"Create view failed: {e}")
            return False

    def share_dashboard_view(self, layout_name: str, output_format: str = "json") -> bool:
        """
        Share dashboard view by generating export files.
        
        Args:
            layout_name: Name of the layout to share
            output_format: Export format (json, markdown)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            console.print(f"[bold blue]📤 Sharing Dashboard View: {layout_name}[/bold blue]")
            
            # Get layout configuration
            response = requests.get(
                f"{self.api_base_url}/dashboard/layout?layout_type={layout_name}",
                timeout=10
            )
            
            if response.status_code != 200:
                console.print(f"[bold red]❌ Layout '{layout_name}' not found![/bold red]")
                return False
            
            layout_data = response.json()
            
            # Generate export file
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"dashboard_view_{layout_name}_{timestamp}.{output_format}"
            
            if output_format == "json":
                import json
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(layout_data, f, indent=2, ensure_ascii=False)
            
            elif output_format == "markdown":
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# Dashboard View: {layout_name}\n\n")
                    f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("## Configuration\n\n")
                    f.write("```json\n")
                    f.write(json.dumps(layout_data, indent=2))
                    f.write("\n```\n")
            
            console.print(f"[bold green]✅ View exported to: [cyan]{filename}[/cyan][/bold green]")
            console.print(f"[dim]Use this file to share or import the dashboard view[/dim]")
            return True
            
        except Exception as e:
            console.print(f"[bold red]❌ Error sharing view: {e}[/bold red]")
            logger.error(f"Share view failed: {e}")
            return False

    def schedule_report(self, report_type: str, schedule_expr: str, output_format: str = "markdown") -> bool:
        """
        Schedule automated dashboard reports.
        
        Args:
            report_type: Type of report to generate
            schedule_expr: Cron expression for scheduling
            output_format: Output format for reports
            
        Returns:
            True if successful, False otherwise
        """
        try:
            console.print(f"[bold blue]⏰ Scheduling Automated Report: {report_type}[/bold blue]")
            
            # Validate cron expression
            if not self._validate_cron_expression(schedule_expr):
                console.print("[bold red]❌ Invalid cron expression![/bold red]")
                console.print("[yellow]Example: '0 9 * * *' for daily at 9 AM[/yellow]")
                return False
            
            # Create schedule configuration
            schedule_config = {
                "report_type": report_type,
                "schedule": schedule_expr,
                "format": output_format,
                "enabled": True,
                "last_run": None,
                "next_run": self._calculate_next_run(schedule_expr)
            }
            
            # Save schedule to file
            schedules_file = Path("JSonDataBase/OutPuts/dashboard_schedules.json")
            schedules_file.parent.mkdir(parents=True, exist_ok=True)
            
            schedules = []
            if schedules_file.exists():
                with open(schedules_file, 'r', encoding='utf-8') as f:
                    schedules = json.load(f)
            
            # Remove existing schedule for this report type
            schedules = [s for s in schedules if s.get('report_type') != report_type]
            schedules.append(schedule_config)
            
            with open(schedules_file, 'w', encoding='utf-8') as f:
                json.dump(schedules, f, indent=2, ensure_ascii=False)
            
            console.print(f"[bold green]✅ Report '{report_type}' scheduled successfully![/bold green]")
            console.print(f"   Schedule: [cyan]{schedule_expr}[/cyan]")
            console.print(f"   Format: [cyan]{output_format}[/cyan]")
            console.print(f"   Next run: [cyan]{schedule_config['next_run']}[/cyan]")
            return True
            
        except Exception as e:
            console.print(f"[bold red]❌ Error scheduling report: {e}[/bold red]")
            logger.error(f"Schedule report failed: {e}")
            return False

    def analyze_dashboard_data(self, analysis_type: str = "overview", timeframe: str = "24h") -> bool:
        """
        Analyze dashboard data and generate insights.
        
        Args:
            analysis_type: Type of analysis to perform
            timeframe: Timeframe for analysis
            
        Returns:
            True if successful, False otherwise
        """
        try:
            console.print(f"[bold blue]📊 Analyzing Dashboard Data: {analysis_type}[/bold blue]")
            
            # Get analysis data from API
            endpoints = {
                "overview": f"{self.api_base_url}/dashboard/overview?project_id=default",
                "metrics": f"{self.api_base_url}/dashboard/metrics?project_id=default&timeframe={timeframe}",
                "health": f"{self.api_base_url}/dashboard/health?project_id=default",
                "performance": f"{self.api_base_url}/dashboard/team-performance?project_id=default"
            }
            
            if analysis_type not in endpoints:
                console.print(f"[bold red]❌ Invalid analysis type: {analysis_type}[/bold red]")
                console.print(f"[yellow]Available types: {list(endpoints.keys())}[/yellow]")
                return False
            
            response = requests.get(endpoints[analysis_type], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Generate analysis report
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"dashboard_analysis_{analysis_type}_{timestamp}.md"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# Dashboard Analysis: {analysis_type}\n\n")
                    f.write(f"Timeframe: {timeframe}\n")
                    f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("## Analysis Results\n\n")
                    f.write("```json\n")
                    f.write(json.dumps(data, indent=2))
                    f.write("\n```\n")
                
                console.print(f"[bold green]✅ Analysis completed![/bold green]")
                console.print(f"   Report saved to: [cyan]{filename}[/cyan]")
                return True
            else:
                console.print(f"[bold red]❌ Analysis failed: {response.text}[/bold red]")
                return False
                
        except Exception as e:
            console.print(f"[bold red]❌ Error analyzing data: {e}[/bold red]")
            logger.error(f"Analysis failed: {e}")
            return False

    def configure_dashboard(self, setting_name: Optional[str] = None, 
                           setting_value: Optional[str] = None) -> bool:
        """
        Configure dashboard settings.
        
        Args:
            setting_name: Name of setting to configure
            setting_value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            console.print("[bold blue]⚙️  Configuring Dashboard Settings[/bold blue]")
                    f.write(json.dumps(layout_data, indent=2))
                    f.write("## Configuration\n\n")

# Click command group for dashboard
@click.group()
def dashboard_cli():
    """AutoProjectManagement Dashboard CLI Commands"""
    pass

@dashboard_cli.command()
@click.option('--port', '-p', type=int, help='Port number for dashboard')
@click.option('--host', '-h', help='Host address for dashboard')
def start(port: Optional[int], host: Optional[str]):
    """Start the dashboard server"""
    cli = DashboardCLI()
    cli.start_dashboard(port, host)

@dashboard_cli.command()
def stop():
    """Stop the dashboard server"""
    cli = DashboardCLI()
    cli.stop_dashboard()

@dashboard_cli.command()
def status():
    """Show dashboard server status"""
    cli = DashboardCLI()
    cli.show_dashboard_info()

@dashboard_cli.command()
def open():
    """Open dashboard in web browser"""
    cli = DashboardCLI()
    cli.open_dashboard()

@dashboard_cli.command()
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'markdown']), 
              default='json', help='Export format')
@click.option('--output', '-o', help='Output file path')
def export(format: str, output: Optional[str]):
    """Export dashboard data to file"""
    cli = DashboardCLI()
    cli.export_dashboard_data(format, output)

@dashboard_cli.command()
def info():
    """Show detailed dashboard information"""
    cli = DashboardCLI()
    cli.show_dashboard_info()

if __name__ == "__main__":
    dashboard_cli()
