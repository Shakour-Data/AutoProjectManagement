"""
AutoProjectManagement Configuration Module

This module provides centralized configuration management for the AutoProjectManagement
system, including API settings, database connections, GitHub integration, and system-wide
configuration options.

Author: AutoProjectManagement System
Version: 1.0.0
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =============================================================================
# BASE CONFIGURATION
# =============================================================================

@dataclass
class BaseConfig:
    """Base configuration class with common functionality."""
    
    @classmethod
    def from_env(cls, prefix: str = "") -> 'BaseConfig':
        """Create configuration instance from environment variables."""
        raise NotImplementedError("Subclasses must implement from_env method")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

# =============================================================================
# API CONFIGURATION
# =============================================================================

@dataclass
class APIConfig(BaseConfig):
    """API server configuration."""
    
    # Server settings
    host: str = field(default="127.0.0.1")
    port: int = field(default=8000)
    reload: bool = field(default=True)
    debug: bool = field(default=False)
    
    # API metadata
    title: str = field(default="AutoProjectManagement API")
    description: str = field(default="RESTful API for automated project management")
    version: str = field(default="1.0.0")
    
    # URL configuration
    prefix: str = field(default="/api/v1")
    docs_url: str = field(default="/docs")
    redoc_url: str = field(default="/redoc")
    openapi_url: str = field(default="/openapi.json")
    
    # CORS settings
    cors_origins: list = field(default_factory=lambda: ["*"])
    cors_credentials: bool = field(default=True)
    
    # Rate limiting
    rate_limit: str = field(default="100/minute")
    
    @classmethod
    def from_env(cls, prefix: str = "API_") -> 'APIConfig':
        """Create API configuration from environment variables."""
        return cls(
            host=os.getenv(f"{prefix}HOST", "127.0.0.1"),
            port=int(os.getenv(f"{prefix}PORT", "8000")),
            reload=os.getenv(f"{prefix}RELOAD", "true").lower() == "true",
            debug=os.getenv(f"{prefix}DEBUG", "false").lower() == "true",
            title=os.getenv(f"{prefix}TITLE", "AutoProjectManagement API"),
            description=os.getenv(f"{prefix}DESCRIPTION", "RESTful API for automated project management"),
            version=os.getenv(f"{prefix}VERSION", "1.0.0"),
            prefix=os.getenv(f"{prefix}PREFIX", "/api/v1"),
            docs_url=os.getenv(f"{prefix}DOCS_URL", "/docs"),
            redoc_url=os.getenv(f"{prefix}REDOC_URL", "/redoc"),
            openapi_url=os.getenv(f"{prefix}OPENAPI_URL", "/openapi.json"),
            cors_origins=os.getenv(f"{prefix}CORS_ORIGINS", "*").split(","),
            cors_credentials=os.getenv(f"{prefix}CORS_CREDENTIALS", "true").lower() == "true",
            rate_limit=os.getenv(f"{prefix}RATE_LIMIT", "100/minute")
        )

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

@dataclass
class DatabaseConfig(BaseConfig):
    """Database configuration."""
    
    # Database type
    type: str = field(default="sqlite")
    
    # SQLite settings
    sqlite_path: str = field(default="autoproject.db")
    
    # PostgreSQL settings (if using PostgreSQL)
    postgres_host: str = field(default="localhost")
    postgres_port: int = field(default=5432)
    postgres_db: str = field(default="autoproject")
    postgres_user: str = field(default="autoproject")
    postgres_password: str = field(default="")
    
    # Connection settings
    pool_size: int = field(default=10)
    max_overflow: int = field(default=20)
    pool_timeout: int = field(default=30)
    pool_recycle: int = field(default=3600)
    
    @property
    def connection_string(self) -> str:
        """Generate database connection string."""
        if self.type.lower() == "sqlite":
            return f"sqlite:///{self.sqlite_path}"
        elif self.type.lower() == "postgresql":
            return (
                f"postgresql://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
            )
        else:
            raise ValueError(f"Unsupported database type: {self.type}")
    
    @classmethod
    def from_env(cls, prefix: str = "DB_") -> 'DatabaseConfig':
        """Create database configuration from environment variables."""
        return cls(
            type=os.getenv(f"{prefix}TYPE", "sqlite"),
            sqlite_path=os.getenv(f"{prefix}SQLITE_PATH", "autoproject.db"),
            postgres_host=os.getenv(f"{prefix}POSTGRES_HOST", "localhost"),
            postgres_port=int(os.getenv(f"{prefix}POSTGRES_PORT", "5432")),
            postgres_db=os.getenv(f"{prefix}POSTGRES_DB", "autoproject"),
            postgres_user=os.getenv(f"{prefix}POSTGRES_USER", "autoproject"),
            postgres_password=os.getenv(f"{prefix}POSTGRES_PASSWORD", ""),
            pool_size=int(os.getenv(f"{prefix}POOL_SIZE", "10")),
            max_overflow=int(os.getenv(f"{prefix}MAX_OVERFLOW", "20")),
            pool_timeout=int(os.getenv(f"{prefix}POOL_TIMEOUT", "30")),
            pool_recycle=int(os.getenv(f"{prefix}POOL_RECYCLE", "3600"))
        )

# =============================================================================
# GITHUB INTEGRATION CONFIGURATION
# =============================================================================

@dataclass
class GitHubConfig(BaseConfig):
    """GitHub integration configuration."""
    
    # Authentication
    token: str = field(default="")
    username: str = field(default="")
    
    # Repository settings
    default_repo: str = field(default="")
    default_branch: str = field(default="main")
    
    # API settings
    api_base_url: str = field(default="https://api.github.com")
    api_version: str = field(default="2022-11-28")
    
    # Rate limiting
    requests_per_hour: int = field(default=5000)
    
    # Webhook settings
    webhook_secret: str = field(default="")
    webhook_url: str = field(default="")
    
    @classmethod
    def from_env(cls, prefix: str = "GITHUB_") -> 'GitHubConfig':
        """Create GitHub configuration from environment variables."""
        return cls(
            token=os.getenv(f"{prefix}TOKEN", ""),
            username=os.getenv(f"{prefix}USERNAME", ""),
            default_repo=os.getenv(f"{prefix}DEFAULT_REPO", ""),
            default_branch=os.getenv(f"{prefix}DEFAULT_BRANCH", "main"),
            api_base_url=os.getenv(f"{prefix}API_BASE_URL", "https://api.github.com"),
            api_version=os.getenv(f"{prefix}API_VERSION", "2022-11-28"),
            requests_per_hour=int(os.getenv(f"{prefix}REQUESTS_PER_HOUR", "5000")),
            webhook_secret=os.getenv(f"{prefix}WEBHOOK_SECRET", ""),
            webhook_url=os.getenv(f"{prefix}WEBHOOK_URL", "")
        )

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

@dataclass
class LoggingConfig(BaseConfig):
    """Logging configuration."""
    
    level: str = field(default="INFO")
    format: str = field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_path: Optional[str] = field(default=None)
    max_file_size: str = field(default="10MB")
    backup_count: int = field(default=5)
    
    # Structured logging
    json_format: bool = field(default=False)
    include_extra: bool = field(default=True)
    
    @classmethod
    def from_env(cls, prefix: str = "LOG_") -> 'LoggingConfig':
        """Create logging configuration from environment variables."""
        return cls(
            level=os.getenv(f"{prefix}LEVEL", "INFO"),
            format=os.getenv(
                f"{prefix}FORMAT",
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            ),
            file_path=os.getenv(f"{prefix}FILE_PATH", None),
            max_file_size=os.getenv(f"{prefix}MAX_FILE_SIZE", "10MB"),
            backup_count=int(os.getenv(f"{prefix}BACKUP_COUNT", "5")),
            json_format=os.getenv(f"{prefix}JSON_FORMAT", "false").lower() == "true",
            include_extra=os.getenv(f"{prefix}INCLUDE_EXTRA", "true").lower() == "true"
        )

# =============================================================================
# PROJECT CONFIGURATION
# =============================================================================

@dataclass
class ProjectConfig(BaseConfig):
    """Project-specific configuration."""
    
    # Project paths
    base_path: str = field(default=str(Path.cwd()))
    data_path: str = field(default="JSonDataBase")
    output_path: str = field(default="JSonDataBase/OutPuts")
    backup_path: str = field(default="project_management/PM_Backups")
    
    # File settings
    max_file_size: int = field(default=10 * 1024 * 1024)  # 10MB
    allowed_extensions: list = field(
        default_factory=lambda: [".json", ".md", ".py", ".txt", ".yml", ".yaml"]
    )
    
    # Processing settings
    max_workers: int = field(default=4)
    timeout_seconds: int = field(default=300)
    
    # Feature flags
    enable_auto_commit: bool = field(default=True)
    enable_risk_analysis: bool = field(default=True)
    enable_progress_tracking: bool = field(default=True)
    enable_github_integration: bool = field(default=True)
    
    @classmethod
    def from_env(cls, prefix: str = "PROJECT_") -> 'ProjectConfig':
        """Create project configuration from environment variables."""
        return cls(
            base_path=os.getenv(f"{prefix}BASE_PATH", str(Path.cwd())),
            data_path=os.getenv(f"{prefix}DATA_PATH", "JSonDataBase"),
            output_path=os.getenv(f"{prefix}OUTPUT_PATH", "JSonDataBase/OutPuts"),
            backup_path=os.getenv(f"{prefix}BACKUP_PATH", "project_management/PM_Backups"),
            max_file_size=int(os.getenv(f"{prefix}MAX_FILE_SIZE", str(10 * 1024 * 1024))),
            allowed_extensions=os.getenv(
                f"{prefix}ALLOWED_EXTENSIONS",
                ".json,.md,.py,.txt,.yml,.yaml"
            ).split(","),
            max_workers=int(os.getenv(f"{prefix}MAX_WORKERS", "4")),
            timeout_seconds=int(os.getenv(f"{prefix}TIMEOUT_SECONDS", "300")),
            enable_auto_commit=os.getenv(f"{prefix}ENABLE_AUTO_COMMIT", "true").lower() == "true",
            enable_risk_analysis=os.getenv(f"{prefix}ENABLE_RISK_ANALYSIS", "true").lower() == "true",
            enable_progress_tracking=os.getenv(f"{prefix}ENABLE_PROGRESS_TRACKING", "true").lower() == "true",
            enable_github_integration=os.getenv(f"{prefix}ENABLE_GITHUB_INTEGRATION", "true").lower() == "true"
        )

# =============================================================================
# SECURITY CONFIGURATION
# =============================================================================

@dataclass
class SecurityConfig(BaseConfig):
    """Security configuration."""
    
    # JWT settings
    jwt_secret_key: str = field(default="your-secret-key-change-this")
    jwt_algorithm: str = field(default="HS256")
    jwt_expiration_minutes: int = field(default=60)
    
    # API key settings
    api_key_header: str = field(default="X-API-Key")
    api_key_required: bool = field(default=False)
    
    # CORS settings
    cors_allowed_origins: list = field(default_factory=lambda: ["*"])
    
    # SSL/TLS
    ssl_cert_path: Optional[str] = field(default=None)
    ssl_key_path: Optional[str] = field(default=None)
    
    @classmethod
    def from_env(cls, prefix: str = "SECURITY_") -> 'SecurityConfig':
        """Create security configuration from environment variables."""
        return cls(
            jwt_secret_key=os.getenv(f"{prefix}JWT_SECRET_KEY", "your-secret-key-change-this"),
            jwt_algorithm=os.getenv(f"{prefix}JWT_ALGORITHM", "HS256"),
            jwt_expiration_minutes=int(os.getenv(f"{prefix}JWT_EXPIRATION_MINUTES", "60")),
            api_key_header=os.getenv(f"{prefix}API_KEY_HEADER", "X-API-Key"),
            api_key_required=os.getenv(f"{prefix}API_KEY_REQUIRED", "false").lower() == "true",
            cors_allowed_origins=os.getenv(f"{prefix}CORS_ALLOWED_ORIGINS", "*").split(","),
            ssl_cert_path=os.getenv(f"{prefix}SSL_CERT_PATH", None),
            ssl_key_path=os.getenv(f"{prefix}SSL_KEY_PATH", None)
        )

# =============================================================================
# MAIN CONFIGURATION CLASS
# =============================================================================

class Config:
    """Main configuration class that aggregates all configuration sections."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.api = APIConfig.from_env()
        self.database = DatabaseConfig.from_env()
        self.github = GitHubConfig.from_env()
        self.logging = LoggingConfig.from_env()
        self.project = ProjectConfig.from_env()
        self.security = SecurityConfig.from_env()
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        errors = []
        
        # Validate required fields
        if not self.github.token and self.project.enable_github_integration:
            errors.append("GitHub token is required when GitHub integration is enabled")
        
        if not self.security.jwt_secret_key or self.security.jwt_secret_key == "your-secret-key-change-this":
            errors.append("JWT secret key must be changed from default")
        
        if self.database.type == "postgresql" and not self.database.postgres_password:
            errors.append("PostgreSQL password is required")
        
        if errors:
            raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire configuration to dictionary."""
        return {
            "api": self.api.to_dict(),
            "database": self.database.to_dict(),
            "github": self.github.to_dict(),
            "logging": self.logging.to_dict(),
            "project": self.project.to_dict(),
            "security": self.security.to_dict()
        }
    
    def save_to_file(self, file_path: str) -> None:
        """Save configuration to JSON file."""
        import json
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, file_path: str) -> 'Config':
        """Load configuration from JSON file."""
        import json
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        config = cls()
        for section, values in data.items():
            if hasattr(config, section):
                section_config = getattr(config, section)
                for key, value in values.items():
                    if hasattr(section_config, key):
                        setattr(section_config, key, value)
        
        return config

# =============================================================================
# GLOBAL CONFIGURATION INSTANCE
# =============================================================================

# Create global configuration instance
config = Config()

# Validate configuration on import
try:
    config.validate()
except ValueError as e:
    import warnings
    warnings.warn(str(e))

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_config() -> Config:
    """Get the global configuration instance."""
    return config

def reload_config() -> None:
    """Reload configuration from environment variables."""
    global config
    config = Config()
    config.validate()

def print_config() -> None:
    """Print current configuration (excluding sensitive data)."""
    import json
    safe_config = config.to_dict()
    
    # Remove sensitive information
    if "github" in safe_config and "token" in safe_config["github"]:
        safe_config["github"]["token"] = "***"
    if "security" in safe_config and "jwt_secret_key" in safe_config["security"]:
        safe_config["security"]["jwt_secret_key"] = "***"
    
    print(json.dumps(safe_config, indent=2))

# =============================================================================
# ENVIRONMENT-SPECIFIC CONFIGURATIONS
# =============================================================================

class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    def __init__(self):
        super().__init__()
        self.api.debug = True
        self.api.reload = True
        self.logging.level = "DEBUG"

class ProductionConfig(Config):
    """Production environment configuration."""
    
    def __init__(self):
        super().__init__()
        self.api.debug = False
        self.api.reload = False
        self.logging.level = "INFO"
        self.security.api_key_required = True

class TestingConfig(Config):
    """Testing environment configuration."""
    
    def __init__(self):
        super().__init__()
        self.api.debug = True
        self.database.type = "sqlite"
        self.database.sqlite_path = ":memory:"
        self.logging.level = "DEBUG"
        self.project.enable_github_integration = False

# =============================================================================
# CONFIGURATION FACTORY
# =============================================================================

def get_config_by_env(env: str = None) -> Config:
    """
    Get configuration based on environment.
    
    Args:
        env: Environment name ('development', 'production', 'testing')
            If None, uses ENVIRONMENT environment variable.
    
    Returns:
        Config instance for the specified environment.
    """
    if env is None:
        env = os.getenv("ENVIRONMENT", "development").lower()
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
        "dev": DevelopmentConfig,
        "prod": ProductionConfig,
        "test": TestingConfig
    }
    
    config_class = config_map.get(env, DevelopmentConfig)
    return config_class()

# =============================================================================
# EXPORTED SYMBOLS
# =============================================================================

__all__ = [
    "Config",
    "APIConfig",
    "DatabaseConfig",
    "GitHubConfig",
    "LoggingConfig",
    "ProjectConfig",
    "SecurityConfig",
    "config",
    "get_config",
    "reload_config",
    "print_config",
    "get_config_by_env"
]
