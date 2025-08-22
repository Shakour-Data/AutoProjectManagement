# Advanced Dashboard CLI Commands

## Overview

This document describes the advanced CLI commands for the AutoProjectManagement dashboard system. These commands provide enhanced functionality for creating custom views, sharing dashboards, scheduling reports, analyzing data, and configuring settings.

## Command Reference

### 1. Create Custom View (`create-view`)

Create custom dashboard views with specific widgets, refresh rates, and themes.

**Usage:**
```bash
autoprojectmanagement dashboard create-view --name <name> [--widgets <widgets>] [--refresh-rate <ms>] [--theme <theme>]
```

**Options:**
- `--name, -n`: Name of the custom layout (required)
- `--widgets, -w`: Comma-separated list of widget IDs (optional)
- `--refresh-rate, -r`: Refresh rate in milliseconds (optional, default: 3000)
- `--theme, -t`: Theme name: light/dark (optional, default: light)

**Examples:**
```bash
# Create view with specific widgets
autoprojectmanagement dashboard create-view --name "MyView" --widgets "health,progress,risks"

# Create view with custom refresh rate
autoprojectmanagement dashboard create-view --name "FastView" --refresh-rate 1000

# Interactive creation (prompts for all options)
autoprojectmanagement dashboard create-view --name "InteractiveView"
```

### 2. Share Dashboard View (`share-view`)

Export dashboard views for sharing or backup purposes.

**Usage:**
```bash
autoprojectmanagement dashboard share-view --name <name> [--format <format>]
```

**Options:**
- `--name, -n`: Name of the layout to share (required)
- `--format, -f`: Export format: json/markdown (optional, default: json)

**Examples:**
```bash
# Export as JSON
autoprojectmanagement dashboard share-view --name "standard" --format json

# Export as Markdown
autoprojectmanagement dashboard share-view --name "custom" --format markdown
```

### 3. Schedule Automated Reports (`schedule-report`)

Schedule automated dashboard reports using cron expressions.

**Usage:**
```bash
autoprojectmanagement dashboard schedule-report --type <type> --schedule <cron> [--format <format>]
```

**Options:**
- `--type, -t`: Report type: overview/metrics/health/performance (required)
- `--schedule, -s`: Cron expression (required)
- `--format, -f`: Output format: markdown/json (optional, default: markdown)

**Cron Examples:**
- `0 9 * * *` - Daily at 9 AM
- `*/5 * * * *` - Every 5 minutes
- `0 0 * * 0` - Weekly on Sunday
- `0 12 1 * *` - Monthly on 1st at noon

**Examples:**
```bash
# Daily overview report
autoprojectmanagement dashboard schedule-report --type overview --schedule "0 9 * * *"

# Hourly metrics report
autoprojectmanagement dashboard schedule-report --type metrics --schedule "0 * * * *"

# Weekly performance report in JSON
autoprojectmanagement dashboard schedule-report --type performance --schedule "0 0 * * 0" --format json
```

### 4. Analyze Dashboard Data (`analyze`)

Analyze dashboard data and generate insights.

**Usage:**
```bash
