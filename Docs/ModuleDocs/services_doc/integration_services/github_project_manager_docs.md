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
