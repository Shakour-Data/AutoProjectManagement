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
autoprojectmanagement dashboard analyze [--type <type>] [--timeframe <timeframe>]
```

**Options:**
- `--type, -t`: Analysis type: overview/metrics/health/performance (optional, default: overview)
- `--timeframe, -tf`: Timeframe for analysis (optional, default: 24h)

**Examples:**
```bash
# Basic overview analysis
autoprojectmanagement dashboard analyze

# Metrics analysis for 7 days
autoprojectmanagement dashboard analyze --type metrics --timeframe 7d

# Health analysis
autoprojectmanagement dashboard analyze --type health
```

### 5. Configure Dashboard (`config`)

Configure dashboard settings interactively or via command line.

**Usage:**
```bash
autoprojectmanagement dashboard config [--setting <name>] [--value <value>]
```

**Options:**
- `--setting, -s`: Setting name to configure (optional)
- `--value, -v`: Value to set (optional)

**Available Settings:**
- `refresh_rate`: Refresh rate in milliseconds (1000-60000)
- `theme`: Interface theme (light/dark)
- `auto_refresh`: Enable auto-refresh (true/false)
- `notifications`: Enable notifications (true/false)

**Examples:**
```bash
# Interactive configuration
autoprojectmanagement dashboard config

# Set specific setting
autoprojectmanagement dashboard config --setting refresh_rate --value 5000

# Enable dark theme
autoprojectmanagement dashboard config --setting theme --value dark
```

## Configuration Files

### Dashboard Layouts
Location: `JSonDataBase/OutPuts/dashboard_layouts/`
Format: JSON files containing layout configurations

### Scheduled Reports
Location: `JSonDataBase/OutPuts/dashboard_schedules.json`
Format: JSON array of scheduled report configurations

### Dashboard Configuration
Location: `JSonDataBase/OutPuts/dashboard_config.json`
Format: JSON object with key-value settings

## API Integration

All commands integrate with the dashboard API endpoints:

- `POST /api/v1/dashboard/layout` - Create/update layouts
- `GET /api/v1/dashboard/layout` - Retrieve layouts
- `GET /api/v1/dashboard/overview` - Overview data
- `GET /api/v1/dashboard/metrics` - Metrics data
- `GET /api/v1/dashboard/health` - Health status
- `GET /api/v1/dashboard/team-performance` - Performance data

## Error Handling

The CLI provides comprehensive error handling with:
- Clear error messages
- Validation of inputs
- Graceful fallbacks
- Detailed logging

## Best Practices

1. **Naming Conventions**: Use descriptive names for custom views
2. **Cron Expressions**: Test expressions using online validators
3. **Backup**: Regularly export important views
4. **Testing**: Test configurations in development before production
5. **Documentation**: Document custom views and schedules

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Ensure dashboard server is running
   - Check host and port configuration

2. **Invalid Cron Expressions**
   - Use valid cron syntax
   - Test expressions with `crontab.guru`

3. **File Permission Issues**
   - Ensure write permissions to output directories
   - Check disk space

4. **Widget Availability**
   - Verify available widgets with API endpoint
   - Check dashboard server logs

### Debug Mode

Enable debug logging for detailed troubleshooting:
```bash
export LOG_LEVEL=DEBUG
autoprojectmanagement dashboard <command>
```

## Examples

### Complete Workflow Example

```bash
# Create a custom view
autoprojectmanagement dashboard create-view --name "ExecutiveDashboard" --widgets "health,progress,metrics"

# Schedule daily reports
autoprojectmanagement dashboard schedule-report --type overview --schedule "0 8 * * *"

# Configure settings
autoprojectmanagement dashboard config --setting refresh_rate --value 2000
autoprojectmanagement dashboard config --setting theme --value dark

# Share the view
autoprojectmanagement dashboard share-view --name "ExecutiveDashboard" --format json

# Analyze data
autoprojectmanagement dashboard analyze --type metrics --timeframe 7d
```

## Support

For additional support:
- Check the main documentation
- Review API documentation
- Check server logs for detailed errors
- Contact the development team

---

*Last Updated: $(date +%Y-%m-%d)*
