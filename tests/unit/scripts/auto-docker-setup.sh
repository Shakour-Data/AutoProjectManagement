#!/bin/bash
# AutoProjectManagement - Fully Automated Docker Setup
# This script provides zero-configuration Docker deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        OS="windows"
    else
        OS="unknown"
    fi
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Installing Docker..."
        install_docker
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        error "Docker Compose is not installed. Installing..."
        install_docker_compose
    fi
}

# Install Docker based on OS
install_docker() {
    detect_os
    case $OS in
        linux)
            log "Installing Docker for Linux..."
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
            sudo usermod -aG docker $USER
            rm get-docker.sh
            ;;
        macos)
            log "Installing Docker for macOS..."
            # This will prompt user to install Docker Desktop
            open "https://docs.docker.com/desktop/mac/install/"
            error "Please install Docker Desktop and run this script again"
            exit 1
            ;;
        windows)
            log "Installing Docker for Windows..."
            # This will prompt user to install Docker Desktop
            start "https://docs.docker.com/desktop/windows/install/"
            error "Please install Docker Desktop and run this script again"
            exit 1
            ;;
    esac
}

# Auto-detect environment
detect_environment() {
    if [[ "$1" == "--prod" ]] || [[ "$1" == "production" ]]; then
        ENV="production"
        COMPOSE_FILE="docker-compose.prod.yml"
    elif [[ "$1" == "--dev" ]] || [[ "$1" == "development" ]]; then
        ENV="development"
        COMPOSE_FILE="docker-compose.dev.yml"
    else
        # Auto-detect based on git branch or hostname
        if git rev-parse --git-dir > /dev/null 2>&1; then
            BRANCH=$(git rev-parse --abbrev-ref HEAD)
            if [[ "$BRANCH" == "main" ]] || [[ "$BRANCH" == "master" ]]; then
                ENV="production"
                COMPOSE_FILE="docker-compose.prod.yml"
            else
                ENV="development"
                COMPOSE_FILE="docker-compose.dev.yml"
            fi
        else
            # Default to development
            ENV="development"
            COMPOSE_FILE="docker-compose.dev.yml"
        fi
    fi
    
    log "Detected environment: $ENV"
}

# Generate .env file if it doesn't exist
setup_environment() {
    if [[ ! -f .env ]]; then
        info "Creating .env file..."
        cat > .env << EOF
# Auto-generated environment configuration
ENVIRONMENT=$ENV
DEBUG=$([ "$ENV" == "development" ] && echo "true" || echo "false")
LOG_LEVEL=$([ "$ENV" == "development" ] && echo "DEBUG" || echo "INFO")

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=$([ "$ENV" == "development" ] && echo "2" || echo "4")

# Database Configuration
DATA_PATH=/app/data
BACKUP_INTERVAL=3600
MAX_BACKUPS=10

# Redis Configuration
REDIS_URL=redis://redis:6379
REDIS_DB=0

# Security Configuration
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)
ALLOWED_HOSTS=localhost,127.0.0.1

# SSL Configuration (Production)
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem
EOF
        log ".env file created successfully"
    else
        info ".env file already exists, skipping creation"
    fi
}

# Generate SSL certificates for production
setup_ssl() {
    if [[ "$ENV" == "production" ]]; then
        SSL_DIR="./docker/nginx/ssl"
        if [[ ! -d "$SSL_DIR" ]]; then
            mkdir -p "$SSL_DIR"
        fi
        
        if [[ ! -f "$SSL_DIR/cert.pem" ]]; then
            info "Generating self-signed SSL certificates..."
            openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
                -keyout "$SSL_DIR/key.pem" \
                -out "$SSL_DIR/cert.pem" \
                -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
            log "SSL certificates generated"
        fi
    fi
}

# Build and start services
deploy_services() {
    log "Building and starting services..."
    
    # Pull latest images
    docker-compose -f $COMPOSE_FILE pull
    
    # Build services
    docker-compose -f $COMPOSE_FILE build --no-cache
    
    # Start services
    docker-compose -f $COMPOSE_FILE up -d
    
    # Wait for services to be healthy
    wait_for_health
    
    log "Deployment completed successfully!"
}

# Wait for services to be healthy
wait_for_health() {
    log "Waiting for services to be healthy..."
    
    local services=("api" "worker-1" "worker-2" "monitor")
    local max_attempts=30
    local attempt=1
    
    for service in "${services[@]}"; do
        info "Checking health of $service..."
        while [[ $attempt -le $max_attempts ]]; do
            if docker-compose -f $COMPOSE_FILE ps $service | grep -q "healthy"; then
                log "$service is healthy"
                break
            fi
            sleep 10
            ((attempt++))
        done
        
        if [[ $attempt -gt $max_attempts ]]; then
            warning "$service health check timed out"
        fi
    done
}

# Display service status
show_status() {
    log "Service Status:"
    docker-compose -f $COMPOSE_FILE ps
    
    log "\nAccess URLs:"
    echo "API: http://localhost:8000"
    echo "Monitor: http://localhost:8080"
    
    if [[ "$ENV" == "production" ]]; then
        echo "Web Interface: https://localhost"
    else
        echo "Web Interface: http://localhost:8080"
    fi
}

# Setup monitoring
setup_monitoring() {
    log "Setting up monitoring..."
    
    # Create monitoring directories
    mkdir -p monitoring/prometheus
    mkdir -p monitoring/grafana
    
    # Setup log rotation
    docker exec autoprojectmanagement-api-1 sh -c "cat > /etc/logrotate.d/apm << EOF
/app/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 apm apm
    postrotate
        docker kill -s USR1 \$(docker ps -q -f name=autoprojectmanagement-api-1)
    endscript
}
EOF"
}

# Main execution
main() {
    log "Starting AutoProjectManagement Docker Setup..."
    
    detect_os
    check_docker
    detect_environment "$1"
    setup_environment
    setup_ssl
    deploy_services
    setup_monitoring
    show_status
    
    log "Setup completed! Your AutoProjectManagement system is now running."
    log "For logs, run: docker-compose -f $COMPOSE_FILE logs -f"
    log "To stop, run: docker-compose -f $COMPOSE_FILE down"
}

# Handle script arguments
case "$1" in
    --help|-h)
        echo "Usage: $0 [environment]"
        echo ""
        echo "Environments:"
        echo "  --dev, development    Development environment"
        echo "  --prod, production    Production environment"
        echo "  (no argument)        Auto-detect environment"
        echo ""
        echo "Examples:"
        echo "  $0                   Auto-detect and setup"
        echo "  $0 --prod            Setup production environment"
        echo "  $0 --dev             Setup development environment"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
