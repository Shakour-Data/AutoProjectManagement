# AutoProjectManagement Configuration Guide - Complete

## GitHub Integration (Continued)

#### 2. Configure Environment Variables
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
export GITHUB_USERNAME=yourusername
export GITHUB_DEFAULT_REPO=username/repository
```

#### 3. Configuration Example
```json
{
  "github": {
    "token": "ghp_xxxxxxxxxxxxxxxxxxxx",
    "username": "yourusername",
    "default_repo": "username/repository",
    "default_branch": "main",
    "auto_sync": true,
    "sync_interval": 300
  }
}
```

---

## Security Configuration

### Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        A[Authentication]
        B[Authorization]
        C[Encryption]
        D[Rate Limiting]
    end
    
    subgraph "Security Components"
        E[JWT Tokens]
        F[API Keys]
        G[SSL/TLS]
        H[CORS Policies]
    end
    
    subgraph "Security Configuration"
        I[JWT Config]
        J[API Key Config]
        K[SSL Config]
        L[CORS Config]
    end
    
    A --> E
    A --> F
    B --> E
    B --> F
    C --> G
    D --> H
    
    I --> E
    J --> F
    K --> G
    L --> H
    
    style A fill:#ffebee
    style B fill:#fff3e0
    style C fill:#e8f5e9
    style D fill:#e3f2fd
```

### Security Configuration Options

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `jwt_secret_key` | string | change-this | JWT signing secret key |
| `jwt_algorithm` | string | HS256 | JWT algorithm (HS256/RS256) |
| `jwt_expiration_minutes` | integer | 60 | Token expiration time |
| `api_key_header` | string | X-API-Key | API key header name |
| `api_key_required` | boolean | false | Require API key |
| `cors_allowed_origins` | list | ["*"] | CORS allowed origins |
| `ssl_cert_path` | string | - | SSL certificate file path |
| `ssl_key_path` | string | - | SSL private key file path |

### Security Best Practices

#### 1. JWT Configuration
```json
{
  "security": {
    "jwt_secret_key": "your-super-secret-key-change-this",
    "jwt_algorithm": "HS256",
    "jwt_expiration_minutes": 60
  }
}
```

#### 2. API Key Configuration
```json
{
  "security": {
    "api_key_required": true,
    "api_key_header": "X-API-Key"
  }
}
```

#### 3. SSL/TLS Configuration
```json
{
  "security": {
    "ssl_cert_path": "/certs/server.crt",
    "ssl_key_path": "/certs/server.key"
  }
}
```

---

## Logging Configuration

### Logging Architecture

```mermaid
flowchart TD
    A[Application] --> B[Logging Config]
    B --> C[Log Handlers]
    C --> D[Console Handler]
    C --> E[File Handler]
    C --> F[Rotating File Handler]
    
    D --> G[Console Output]
    E --> H[Log File]
    F --> I[Rotated Files]
    
    B --> J[Log Format]
    J --> K[Standard Format]
    J --> L[JSON Format]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#e8f5e9
    style G fill:#f3e5f5
    style H fill:#e3f2fd
```

### Logging Configuration Options

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `level` | string | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `format` | string | standard | Log format string |
| `file_path` | string | - | Log file path |
| `max_file_size` | string | 10MB | Maximum log file size |
| `backup_count` | integer | 5 | Number of backup files |
| `json_format` | boolean | false | Use JSON format |
| `include_extra` | boolean | true | Include extra fields |

### Logging Configuration Examples

#### 1. Basic Console Logging
```json
{
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  }
}
```

#### 2. File Logging with Rotation
```json
{
  "logging": {
    "level": "DEBUG",
    "file_path": "logs/autoproject.log",
    "max_file_size": "10MB",
    "backup_count": 5
  }
}
```

#### 3. JSON Structured Logging
```json
{
  "logging": {
    "level": "INFO",
    "json_format": true,
    "include_extra": true
  }
}
```

---

## Project Configuration

### Project Configuration Structure

```mermaid
classDiagram
    class ProjectConfig {
        +str base_path
        +str data_path
        +str output_path
        +str backup_path
        +int max_file_size
        +list allowed_extensions
        +int max_workers
        +int timeout_seconds
        +bool enable_auto_commit
        +bool enable_risk_analysis
        +from_env()
    }
    
    class ProjectManager {
        +setup_directories()
        +validate_paths()
        +configure_features()
    }
    
    class FileManager {
        +check_file_size()
        +validate_extensions()
        +manage_backups()
    }
    
    ProjectConfig --> ProjectManager
    ProjectManager --> FileManager
```

### Project Configuration Options

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `base_path` | string | current directory | Project base directory |
| `data_path` | string | JSonDataBase | Data directory path |
| `output_path` | string | JSonDataBase/OutPuts | Output directory path |
| `backup_path` | string | project_management/PM_Backups | Backup directory path |
| `max_file_size` | integer | 10485760 | Maximum file size (10MB) |
| `allowed_extensions` | list | [...] | Allowed file extensions |
| `max_workers` | integer | 4 | Maximum worker threads |
| `timeout_seconds` | integer | 300 | Operation timeout |
| `enable_auto_commit` | boolean | true | Enable automatic commits |
| `enable_risk_analysis` | boolean | true | Enable risk analysis |
| `enable_progress_tracking` | boolean | true | Enable progress tracking |
| `enable_github_integration` | boolean | true | Enable GitHub integration |

### Project Configuration Example

```json
{
  "project": {
    "base_path": "/path/to/project",
    "data_path": "JSonDataBase",
    "output_path": "JSonDataBase/OutPuts",
    "backup_path": "project_management/PM_Backups",
    "max_file_size": 10485760,
    "allowed_extensions": [".py", ".js", ".json", ".md"],
    "max_workers": 8,
    "timeout_seconds": 300,
    "enable_auto_commit": true,
    "enable_risk_analysis": true,
    "enable_progress_tracking": true,
    "enable_github_integration": true
  }
}
```

---

## Environment-Specific Configurations

### Environment Configuration Matrix

| Feature | Development | Production | Testing |
|---------|-------------|------------|---------|
| **API Debug** | true | false | true |
| **Database** | SQLite | PostgreSQL | SQLite (memory) |
| **Logging Level** | DEBUG | INFO | DEBUG |
| **GitHub Integration** | true | true | false |
| **SSL Required** | false | true | false |
| **Rate Limiting** | relaxed | strict | disabled |

### Environment Configuration Examples

#### Development Configuration
```json
{
  "api": {
    "host": "127.0.0.1",
    "port": 8000,
    "debug": true,
    "reload": true
  },
  "database": {
    "type": "sqlite",
    "sqlite_path": "dev.db"
  },
  "logging": {
    "level": "DEBUG"
  },
  "security": {
    "api_key_required": false
  }
}
```

#### Production Configuration
```json
{
  "api": {
    "host": "0.0.0.0",
    "port": 8080,
    "debug": false,
    "reload": false
  },
  "database": {
    "type": "postgresql",
    "postgres_host": "prod-db.example.com",
    "postgres_port": 5432,
    "postgres_db": "autoproject_prod",
    "pool_size": 20
  },
  "logging": {
    "level": "INFO",
    "file_path": "/var/log/autoproject.log"
  },
  "security": {
    "api_key_required": true,
    "ssl_cert_path": "/certs/server.crt",
    "ssl_key_path": "/certs/server.key"
  }
}
```

#### Testing Configuration
```json
{
  "api": {
    "host": "127.0.0.1",
    "port": 8001,
    "debug": true,
    "reload": true
  },
  "database": {
    "type": "sqlite",
    "sqlite_path": ":memory:"
  },
  "logging": {
    "level": "DEBUG"
  },
  "project": {
    "enable_github_integration": false
  }
}
```

### Environment Detection

```mermaid
flowchart TD
    A[Environment Detection] --> B{ENVIRONMENT variable}
    B -->|development| C[Development Config]
    B -->|production| D[Production Config]
    B -->|testing| E[Testing Config]
    B -->|default| C
    
    C --> F[Load dev settings]
    D --> G[Load prod settings]
    E --> H[Load test settings]
    
    style A fill:#e1f5fe
    style C fill:#e8f5e9
    style D fill:#ffebee
    style E fill:#fff3e0
```

---

## Configuration Validation

### Validation Process

```mermaid
flowchart TD
    A[Configuration Input] --> B[Load Configuration]
    B --> C[Validate Required Fields]
    C --> D[Validate Data Types]
    D --> E[Validate Security Settings]
    E --> F[Validate Dependencies]
    
    F --> G{Validation Result}
    G -->|Valid| H[Accept Configuration]
    G -->|Invalid| I[Collect Errors]
    I --> J[Display Error Messages]
    J --> K[Exit with Error]
    
    style A fill:#e1f5fe
    style H fill:#e8f5e9
    style K fill:#ffebee
```

### Validation Rules

| Section | Required Fields | Validation Rules |
|---------|-----------------|------------------|
| **API** | host, port | host must be valid IP/domain, port 1-65535 |
| **Database** | type | must be 'sqlite' or 'postgresql' |
| **GitHub** | token (if enabled) | must be valid GitHub token format |
| **Security** | jwt_secret_key | must not be default value |
| **Logging** | level | must be valid log level |
| **Project** | base_path | must be valid directory path |

### Validation Error Examples

```json
{
  "errors": [
    {
      "field": "github.token",
      "message": "GitHub token is required when GitHub integration is enabled",
      "type": "missing_required"
    },
    {
      "field": "security.jwt_secret_key",
      "message": "JWT secret key must be changed from default value",
      "type": "security_risk"
    },
    {
      "field": "api.port",
      "message": "Port must be between 1 and 65535",
      "type": "invalid_value"
    }
  ]
}
```

### Validation Methods

#### 1. Programmatic Validation
```python
from autoproject_configuration import Config

config = Config()
try:
    config.validate()
    print("Configuration is valid")
except ValueError as e:
    print(f"Configuration error: {e}")
```

#### 2. Command Line Validation
```bash
python -c "from autoproject_configuration import config; config.validate()"
```

#### 3. Configuration Checker Script
```bash
python -m autoprojectmanagement.configuration.check_config --config config.json
```

---

## Configuration Management

### Configuration Management Commands

| Command | Description | Example |
|---------|-------------|---------|
| `config.validate()` | Validate current configuration | Python API |
| `print_config()` | Display current configuration | Python API |
| `reload_config()` | Reload configuration from files | Python API |
| `--config` | Specify configuration file | CLI argument |
| `--validate` | Validate configuration | CLI argument |

### Configuration Management Tools

#### 1. Configuration CLI
```bash
# Validate configuration
python -m autoprojectmanagement.configuration validate --config config.json

# Show current configuration
python -m autoprojectmanagement.configuration show

# Reload configuration
python -m autoprojectmanagement.configuration reload

# Generate sample configuration
python -m autoprojectmanagement.configuration generate --env development
```

#### 2. Configuration Management Script
```python
from autoprojectmanagement.configuration.manager import ConfigManager

manager = ConfigManager()
manager.load_config('config.json')
manager.validate_config()
manager.apply_config()
```

### Configuration Hot-Reload

```mermaid
sequenceDiagram
    participant Admin as Administrator
    participant CM as Config Manager
    participant App as Application
    participant FS as File System
    
    Admin->>FS: Update config.json
    FS->>CM: File change detected
    CM->>CM: Validate new configuration
    CM->>App: Apply new configuration
    App->>Admin: Configuration updated successfully
```

### Configuration Backup and Restore

#### Backup Configuration
```bash
# Backup current configuration
cp config.json config.backup.json

# Backup with timestamp
cp config.json config.backup.$(date +%Y%m%d_%H%M%S).json
```

#### Restore Configuration
```bash
# Restore from backup
cp config.backup.json config.json

# Validate after restore
python -m autoprojectmanagement.configuration validate
```

---

## Troubleshooting

### Common Configuration Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| **Invalid JSON** | JSON parsing error | Use JSON validator |
| **Missing required field** | Validation error | Add missing configuration |
| **Invalid port** | Port already in use | Change port number |
| **Database connection failed** | Connection timeout | Check database settings |
| **GitHub token invalid** | 401 Unauthorized | Regenerate GitHub token |
| **SSL certificate error** | SSL handshake failed | Check certificate paths |

### Configuration Debugging

#### 1. Enable Debug Logging
```json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

#### 2. Configuration Test Script
```python
import json
from autoproject_configuration import Config

# Test configuration loading
config = Config()
print("Configuration loaded successfully")

# Test validation
try:
    config.validate()
    print("Configuration is valid")
except ValueError as e:
    print(f"Validation error: {e}")

# Test database connection
print(f"Database: {config.database.connection_string}")
```

#### 3. Environment Variable Check
```bash
# Check environment variables
env | grep -E "(API_|DB_|GITHUB_|SECURITY_|LOG_|PROJECT_)"

# Check specific variable
echo $API_PORT
echo $GITHUB_TOKEN
```

### Configuration Diagnostic Commands

```bash
# Check configuration syntax
python -m json.tool config.json

# Validate configuration
python -c "from autoproject_configuration import config; config.validate()"

# Test database connection
python -c "from autoproject_configuration import config; print(config.database.connection_string)"

# Test GitHub integration
python -c "from autoprojectmanagement.services.github_integration import GitHubIntegration; print('GitHub ready')"
```

### Getting Help

#### 1. Configuration Documentation
- Full configuration reference: [Configuration Guide](Configuration_Guide.md)
- API documentation: [API Reference](API_Reference.md)
- Environment setup: [Installation Guide](Installation_Guide.md)

#### 2. Community Support
- GitHub Issues: [Report configuration issues](https://github.com/autoprojectmanagement/autoprojectmanagement/issues)
- Discussions: [Configuration discussions](https://github.com/autoprojectmanagement/autoprojectmanagement/discussions)
- Documentation: [Wiki pages](https://github.com/autoprojectmanagement/autoprojectmanagement/wiki)

#### 3. Professional Support
- Email: support@autoprojectmanagement.com
- Documentation: docs@autoprojectmanagement.com
- Consulting: consulting@autoprojectmanagement.com

---

## Quick Reference

### Configuration File Template

```json
{
  "api": {
    "host": "127.0.0.1",
    "port": 8000,
    "debug": false,
    "reload": true,
    "cors_origins": ["http://localhost:3000"]
  },
  "database": {
    "type": "sqlite",
    "sqlite_path": "autoproject.db"
  },
  "github": {
    "token": "your-github-token",
    "default_repo": "username/repository",
    "default_branch": "main"
  },
  "security": {
    "jwt_secret_key": "your-secret-key",
    "jwt_expiration_minutes": 60
  },
  "logging": {
    "level": "INFO",
    "file_path": "logs/autoproject.log"
  },
  "project": {
    "base_path": "/path/to/project",
    "enable_auto_commit": true,
    "enable_risk_analysis": true
  }
}
```

### Environment Variables Quick Setup

```bash
# Development
export API_HOST=127.0.0.1
export API_PORT=8000
export API_DEBUG=true
export DB_TYPE=sqlite
export GITHUB_TOKEN=your-token

# Production
export API_HOST=0.0.0.0
export API_PORT=8080
export API_DEBUG=false
export DB_TYPE=postgresql
export DB_POSTGRES_HOST=prod-db.example.com
```

### Configuration Validation Checklist

- [ ] JSON syntax is valid
- [ ] All required fields are present
- [ ] Database connection string is correct
- [ ] GitHub token has correct permissions
- [ ] Security settings are properly configured
- [ ] File paths exist and are accessible
- [ ] Port numbers are available
- [ ] Environment variables are set

---

*This configuration guide is continuously updated. For the latest information, please check the [official documentation](https://autoprojectmanagement.com/docs).*
