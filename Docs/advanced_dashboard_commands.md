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
