FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy configuration
COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/nginx/ssl /etc/nginx/ssl

# Create necessary directories
RUN mkdir -p /var/log/nginx /var/www/html

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
