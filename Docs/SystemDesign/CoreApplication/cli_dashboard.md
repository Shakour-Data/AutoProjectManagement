# CLI Dashboard Module Documentation

## Overview
The `cli_dashboard.py` module provides a comprehensive command-line interface for managing the AutoProjectManagement dashboard system. This module enables users to start, stop, monitor, and configure the dashboard through intuitive CLI commands built with the Click framework.

## Architecture

### Class Structure
```mermaid
classDiagram
    class DashboardCLI {
        -default_port: int = 3000
        -default_host: str = "127.0.0.1"
        -api_base_url: str
        +start_dashboard(port, host): bool
        +stop_dashboard(): bool
        +dashboard_status(): Dict[str, Any]
        +open_dashboard(): bool
        +export_dashboard_data(format, output_file): bool
        +show_dashboard_info(): None
        +create_custom_view(layout_name, widgets, refresh_rate, theme): bool
        +share_dashboard_view(layout_name, output_format): bool
        +schedule_report(report_type, schedule_expr, output_format): bool
        +analyze_dashboard_data(analysis_type, timeframe): bool
        +configure_dashboard(setting_name, setting_value): bool
        +get_available_widgets(): List[str]
        -_validate_cron_expression(cron_expr): bool
        -_validate_cron_field_simple(field, min_val, max_val): bool
        -_validate_cron_field(field, min_val, max_val): bool
        -_calculate_next_run(cron_expr): str
    }
```

### Command Structure
```mermaid
flowchart TD
    A[dashboard_cli command group] --> B[start]
    A --> C[stop]
    A --> D[status]
    A --> E[open]
    A --> F[export]
    A --> G[info]
    A --> H[create_view]
    A --> I[share_view]
