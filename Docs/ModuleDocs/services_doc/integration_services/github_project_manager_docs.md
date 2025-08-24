# GitHub Project Manager Service Documentation

*Last updated: 2025-08-14*
*Version: 2.0.0*

## Overview

The `GitHubProjectManager` service provides comprehensive GitHub repository management with both CLI and programmatic interfaces. This service enables automated creation, configuration, and management of GitHub repositories with support for JSON templates, error handling, and batch operations.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Functionality](#core-functionality)
3. [CLI Interface](#cli-interface)
4. [JSON Configuration](#json-configuration)
5. [API Integration](#api-integration)
6. [Error Handling](#error-handling)
7. [Usage Examples](#usage-examples)
8. [API Reference](#api-reference)
9. [Performance Optimization](#performance-optimization)
10. [Troubleshooting Guide](#troubleshooting-guide)

## Architecture Overview

### System Context Diagram

```mermaid
flowchart TD
    A[GitHubProjectManager] --> B[GitHub REST API]
    A --> C[CLI Interface]
    A --> D[JSON Configuration]
    A --> E[Authentication Service]
    
    B --> F[Repository Operations]
    B --> G[Project Creation]
    B --> H[Repository Management]
    
    C --> I[Command Processing]
    C --> J[User Interaction]
    
    D --> K[Template Processing]
    D --> L[Configuration Validation]
    
    E --> M[Token Authentication]
    E --> N[Permission Management]
```

### Component Architecture

```mermaid
classDiagram
    class GitHubProjectManager {
        -github_token: str
        -session: Session
        -config: Dict
        +__init__(github_token)
        +create_project(config)
        +create_project_from_json(json_file, github_username)
        +list_user_repositories(username)
        +delete_project(owner, repo_name)
        +_make_api_request(method, endpoint, data, params)
        +_load_config()
        +_save_config(config)
    }
    
    class GitHubProjectCLI {
        -parser: ArgumentParser
        +__init__()
        +run(args)
        +_create_parser()
    }
    
    class GitHubProjectConfig {
        +project_name: str
        +description: str
        +github_username: str
        +github_token: Optional[str]
        +organization: Optional[str]
        +private: bool
        +auto_init: bool
        +gitignore_template: Optional[str]
        +license_template: Optional[str]
    }
    
    class ProjectReport {
        +project_name: str
        +github_username: str
        +status: str
        +url: Optional[str]
        +error_message: Optional[str]
        +created_at: Optional[str]
        +repository_id: Optional[int]
    }
    
    GitHubProjectManager --> GitHubProjectConfig : uses
    GitHubProjectManager --> ProjectReport : generates
    GitHubProjectCLI --> GitHubProjectManager : orchestrates
```

## Core Functionality

### Repository Creation Process

```mermaid
flowchart TD
    A[Start Creation] --> B{Input Source?}
    B -->|CLI Args| C[Parse Arguments]
    B -->|JSON File| D[Load JSON Config]
    
    C --> E[Create Config Object]
    D --> E
    
    E --> F[Validate Configuration]
    F --> G[API Request]
    G --> H{Success?}
    H -->|Yes| I[Create Repository]
    H -->|No| J[Error Handling]
    
    I --> K[Generate Report]
    J --> K
    K --> L[Return Result]
```

### Supported Operations

| Operation | API Endpoint | Method | Description |
|-----------|-------------|--------|-------------|
| Create Repository | `/user/repos` or `/orgs/{org}/repos` | POST | Create new repository |
| List Repositories | `/users/{username}/repos` | GET | List user repositories |
| Delete Repository | `/repos/{owner}/{repo}` | DELETE | Delete repository |
| Get Repository | `/repos/{owner}/{repo}` | GET | Get repository details |

## CLI Interface

### Command Structure

```mermaid
flowchart TD
    A[github-project] --> B[create]
    A --> C[create-from-json]
    A --> D[list]
    A --> E[delete]
    A --> F[help]
    
    B --> G[--name, --desc, --username, etc.]
    C --> H[json_file --username]
    D --> I[--username]
    E --> J[--owner --repo]
```

### Command Reference

#### create command
```bash
github-project create \
  --name "project-name" \
  --desc "Project description" \
  --username "github-user" \
  [--org "organization"] \
  [--public] \
  [--no-init] \
  [--gitignore "template"] \
  [--license "license-type"]
```

#### create-from-json command
```bash
github-project create-from-json config.json --username "github-user"
```

#### list command
```bash
github-project list --username "github-user"
```

#### delete command
```bash
github-project delete --owner "owner" --repo "repository-name"
```

### Exit Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 0 | Success | Operation completed successfully |
| 1 | Error | Operation failed with error |
| 2 | Usage Error | Invalid command or arguments |

## JSON Configuration

### Configuration Schema

```json
{
  "project_name": "string (required)",
  "description": "string (required)",
  "private": "boolean (default: true)",
  "auto_init": "boolean (default: true)",
  "gitignore_template": "string (optional)",
  "license_template": "string (optional)"
}
```

### Supported Gitignore Templates

| Template | Description | Use Case |
|----------|-------------|----------|
| `Python` | Python-specific ignores | Python projects |
| `Node` | Node.js ignores | JavaScript/Node projects |
| `Java` | Java ignores | Java projects |
| `C++` | C++ ignores | C++ projects |
| `Go` | Go ignores | Go projects |

### Supported License Templates

| License | Description | Use Case |
|---------|-------------|----------|
| `MIT` | MIT License | Permissive open source |
| `Apache-2.0` | Apache 2.0 | Enterprise open source |
| `GPL-3.0` | GPL v3 | Copyleft license |
| `BSD-3-Clause` | BSD 3-Clause | Permissive license |

### Example JSON Configuration

```json
{
  "project_name": "awesome-project",
  "description": "An awesome project with automated setup",
  "private": false,
  "auto_init": true,
  "gitignore_template": "Python",
  "license_template": "MIT"
}
```

## API Integration

### GitHub API Endpoints

| Endpoint | Purpose | Authentication | Rate Limit |
|----------|---------|----------------|------------|
| `POST /user/repos` | Create user repository | Token required | 5000/hr |
| `POST /orgs/{org}/repos` | Create org repository | Token + permissions | 5000/hr |
| `GET /users/{user}/repos` | List user repositories | Optional | 60/hr (unauth) |
| `DELETE /repos/{owner}/{repo}` | Delete repository | Token + permissions | 5000/hr |

### Request Flow

```mermaid
sequenceDiagram
    participant CLI
    participant Manager
    participant GitHubAPI
    participant Config
    
    CLI->>Manager: create_project(config)
    Manager->>Config: Validate config
    Config-->>Manager: Validated config
    Manager->>GitHubAPI: POST /repos
    GitHubAPI-->>Manager: Response data
    Manager->>Manager: Generate report
    Manager-->>CLI: ProjectReport
```

### Response Handling

```python
# Successful response structure
{
