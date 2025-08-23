#!/bin/bash
# One-command deployment script for AutoProjectManagement
# Usage: ./one-command-deploy.sh [environment]

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# Check if running from correct directory
if [[ ! -f "docker-compose.yml" ]]; then
    error "Please run this script from the AutoProjectManagement root directory"
    exit 1
fi

# Make setup script executable
chmod +x scripts/auto-docker-setup.sh

# Run automated setup
log "Starting automated deployment..."
./scripts/auto-docker-setup.sh "$@"

# Create convenience commands
create_aliases() {
    cat > scripts/apm-dev.sh << 'EOF'
#!/bin/bash
# Development commands
case "$1" in
    logs)
        docker-compose -f docker-compose.dev.yml logs -f "${@:2}"
        ;;
    restart)
        docker-compose -f docker-compose.dev.yml restart "${@:2}"
        ;;
    stop)
        docker-compose -f docker-compose.dev.yml down
        ;;
    status)
        docker-compose -f docker-compose.dev.yml ps
        ;;
    shell)
        docker-compose -f docker-compose.dev.yml exec api bash
        ;;
    *)
        echo "Usage: ./apm-dev.sh {logs|restart|stop|status|shell} [service]"
        echo ""
        echo "Examples:"
        echo "  ./apm-dev.sh logs api     - View API logs"
        echo "  ./apm-dev.sh shell        - Access API container shell"
        echo "  ./apm-dev.sh status       - Show service status"
        exit 1
        ;;
esac
EOF

    cat > scripts/apm-prod.sh << 'EOF'
#!/bin/bash
# Production commands
case "$1" in
    logs)
        docker-compose -f docker-compose.prod.yml logs -f "${@:2}"
        ;;
    restart)
        docker-compose -f docker-compose.prod.yml restart "${@:2}"
        ;;
    stop)
        docker-compose -f docker-compose.prod.yml down
        ;;
    status)
        docker-compose -f docker-compose.prod.yml ps
        ;;
    update)
        docker-compose -f docker-compose.prod.yml pull
        docker-compose -f docker-compose.prod.yml up -d
        ;;
    backup)
        ./scripts/backup.sh
        ;;
    *)
        echo "Usage: ./apm-prod.sh {logs|restart|stop|status|update|backup} [service]"
        echo ""
        echo "Examples:"
        echo "  ./apm-prod.sh logs api    - View API logs"
        echo "  ./apm-prod.sh update      - Update production services"
        echo "  ./apm-prod.sh backup      - Create backup"
        exit 1
        ;;
esac
EOF

    chmod +x scripts/apm-dev.sh
    chmod +x scripts/apm-prod.sh
}

# Create backup script
create_backup_script() {
    cat > scripts/backup.sh << 'EOF'
#!/bin/bash
# Backup script for AutoProjectManagement

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Creating backup in $BACKUP_DIR..."

# Backup data volumes
docker run --rm -v autoprojectmanagement_apm_data:/data -v "$BACKUP_DIR":/backup alpine \
    tar czf /backup/data_backup.tar.gz -C /data .

docker run --rm -v autoprojectmanagement_apm_config:/config -v "$BACKUP_DIR":/backup alpine \
    tar czf /backup/config_backup.tar.gz -C /config .

# Backup logs
docker run --rm -v autoprojectmanagement_apm_logs:/logs -v "$BACKUP_DIR":/backup alpine \
    tar czf /backup/logs_backup.tar.gz -C /logs .

# Backup environment
cp .env "$BACKUP_DIR/env_backup"

log "Backup completed: $BACKUP_DIR"
EOF

    chmod +x scripts/backup.sh
}

# Create Windows batch file for Windows users
create_windows_scripts() {
    cat > scripts/auto-docker-setup.bat << 'EOF'
@echo off
REM AutoProjectManagement Windows Docker Setup
REM This script provides automated Docker deployment for Windows

echo Starting AutoProjectManagement Docker Setup...

REM Check if Docker is running
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed or not running. Please install Docker Desktop.
    pause
    exit /b 1
)

REM Detect environment
if "%1"=="" (
    set ENV=development
) else if "%1"=="--prod" (
    set ENV=production
) else if "%1"=="--dev" (
    set ENV=development
) else (
    set ENV=%1
)

echo Detected environment: %ENV%

REM Setup based on environment
if "%ENV%"=="production" (
    set COMPOSE_FILE=docker-compose.prod.yml
) else (
    set COMPOSE_FILE=docker-compose.dev.yml
)

REM Check if .env exists
if not exist .env (
    echo Creating .env file...
    echo # Auto-generated environment configuration > .env
    echo ENVIRONMENT=%ENV% >> .env
    echo DEBUG=true >> .env
    echo LOG_LEVEL=DEBUG >> .env
    echo API_HOST=0.0.0.0 >> .env
    echo API_PORT=8000 >> .env
    echo PYTHONPATH=/app >> .env
)

REM Build and start services
echo Building and starting services...
docker-compose -f %COMPOSE_FILE% build
docker-compose -f %COMPOSE_FILE% up -d

echo.
echo Setup completed! Your services are now running.
echo Access URLs:
echo   API: http://localhost:8000
echo   Monitor: http://localhost:8080
echo.
pause
EOF
}

# Create PowerShell script for Windows PowerShell users
create_powershell_scripts() {
    cat > scripts/auto-docker-setup.ps1 << 'EOF'
# AutoProjectManagement PowerShell Docker Setup
param(
    [Parameter()]
    [ValidateSet("development", "production", "dev", "prod")]
    [string]$Environment = "development"
)

Write-Host "Starting AutoProjectManagement Docker Setup..." -ForegroundColor Green

# Check if Docker is running
try {
    docker --version | Out-Null
} catch {
    Write-Error "Docker is not installed or not running. Please install Docker Desktop."
    exit 1
}

# Convert environment names
if ($Environment -eq "prod") { $Environment = "production" }
if ($Environment -eq "dev") { $Environment = "development" }

Write-Host "Detected environment: $Environment" -ForegroundColor Blue

# Set compose file based on environment
$composeFile = if ($Environment -eq "production") { "docker-compose.prod.yml" } else { "docker-compose.dev.yml" }

# Create .env file if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    @"
# Auto-generated environment configuration
ENVIRONMENT=$Environment
DEBUG=$($Environment -eq "development")
LOG_LEVEL=$($Environment -eq "development" ? "DEBUG" : "INFO")
API_HOST=0.0.0.0
API_PORT=8000
PYTHONPATH=/app
"@ | Out-File -FilePath .env -Encoding UTF8
}

# Build and start services
Write-Host "Building and starting services..." -ForegroundColor Green
docker-compose -f $composeFile build
docker-compose -f $composeFile up -d

Write-Host "`nSetup completed! Your services are now running." -ForegroundColor Green
Write-Host "Access URLs:"
Write-Host "  API: http://localhost:8000"
Write-Host "  Monitor: http://localhost:8080"
EOF
}

# Execute all setup functions
create_aliases
create_backup_script
create_windows_scripts
create_powershell_scripts

log "One-command deployment setup completed!"
log "Usage:"
log "  Linux/macOS: ./scripts/one-command-deploy.sh"
log "  Windows: Double-click scripts/auto-docker-setup.bat"
log "  PowerShell: .\scripts\auto-docker-setup.ps1"
