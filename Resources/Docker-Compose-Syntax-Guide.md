# Docker Compose Syntax Guide (2025 Edition)

**Last Updated:** October 2025
**Compose Version:** v2.24+
**Format Version:** Compose Specification (no version field needed)

---

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Basic Structure](#basic-structure)
- [Services Configuration](#services-configuration)
- [Volumes](#volumes)
- [Networks](#networks)
- [Secrets](#secrets)
- [Configs](#configs)
- [Complete Examples](#complete-examples)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)

---

## Getting Started

### Important: Docker Compose v2 Changes

**CRITICAL: No `version:` field in 2025!**

```yaml
# ❌ OUTDATED (pre-2024)
version: "3.8"
services:
  web:
    image: nginx

# ✅ CORRECT (2025)
services:
  web:
    image: nginx
```

**Why the change?**
- `version:` field is obsolete in Docker Compose v2
- Compose now uses Compose Specification (versionless)
- Modern Docker installations include Compose v2 by default

### Command Syntax

```bash
# ✅ Modern (Docker Compose v2)
docker compose up
docker compose down

# ⚠️ Legacy (Docker Compose v1)
docker-compose up
docker-compose down

# Note the space vs hyphen!
```

---

## Basic Structure

### Minimal Compose File

```yaml
services:
  app:
    image: nginx:alpine
    ports:
      - "8080:80"
```

### Complete Structure

```yaml
# Top-level elements
services:    # Define containers
  # service definitions

volumes:     # Define named volumes (optional)
  # volume definitions

networks:    # Define custom networks (optional)
  # network definitions

secrets:     # Define secrets (optional)
  # secret definitions

configs:     # Define configs (optional)
  # config definitions
```

---

## Services Configuration

### Basic Service Options

```yaml
services:
  myapp:
    # Image to use
    image: nginx:alpine

    # OR build from Dockerfile
    build: ./app

    # Container name (optional, auto-generated if omitted)
    container_name: my-nginx

    # Restart policy
    restart: unless-stopped
    # Options: "no", "always", "on-failure", "unless-stopped"

    # Environment variables
    environment:
      - NODE_ENV=production
      - PORT=3000

    # OR from file
    env_file:
      - .env
      - .env.production

    # Port mapping
    ports:
      - "8080:80"        # host:container
      - "443:443"

    # Volume mounts
    volumes:
      - ./data:/app/data              # Bind mount
      - app-logs:/var/log             # Named volume
      - /tmp                           # Anonymous volume

    # Network connections
    networks:
      - frontend
      - backend

    # Depends on other services
    depends_on:
      - db
      - redis
```

### Build Configuration

```yaml
services:
  app:
    build:
      context: ./app              # Build context directory
      dockerfile: Dockerfile.prod # Custom Dockerfile name
      args:                       # Build arguments
        - VERSION=1.0.0
        - BUILD_ENV=production
      target: production          # Multi-stage build target
      cache_from:                 # Cache sources
        - myapp:latest
      platforms:                  # Multi-platform builds
        - linux/amd64
        - linux/arm64
      labels:                     # Image labels
        com.example.version: "1.0.0"
```

### Advanced Image Options

```yaml
services:
  app:
    image: myapp:latest
    pull_policy: always          # always, never, if_not_present, build
    platform: linux/amd64        # Force specific platform
```

### Environment Variables (Detailed)

```yaml
services:
  app:
    # Method 1: Inline array
    environment:
      - NODE_ENV=production
      - DEBUG=false
      - PORT=3000

    # Method 2: Map format
    environment:
      NODE_ENV: production
      DEBUG: "false"  # Quote booleans/numbers to ensure strings
      PORT: 3000

    # Method 3: From file
    env_file:
      - .env.common
      - .env.production

    # Variable substitution from host environment
    environment:
      - API_URL=${API_URL}           # From host env or .env file
      - VERSION=${VERSION:-1.0.0}    # With default value
```

### Port Mapping (Detailed)

```yaml
services:
  app:
    ports:
      # Short syntax
      - "8080:80"              # host:container
      - "443:443"
      - "3000"                 # Random host port -> container 3000
      - "127.0.0.1:8080:80"   # Bind to specific interface

      # Long syntax
      - target: 80             # Container port
        published: 8080        # Host port
        protocol: tcp          # tcp or udp
        mode: host             # host or ingress

    # Expose ports without publishing (internal network only)
    expose:
      - "3000"
      - "8080"
```

### Volume Mounts (Detailed)

```yaml
services:
  app:
    volumes:
      # Short syntax
      - ./app:/app                    # Bind mount
      - data-volume:/data             # Named volume
      - /var/log                      # Anonymous volume
      - ./config:/config:ro           # Read-only bind mount

      # Long syntax
      - type: bind
        source: ./app
        target: /app
        read_only: false

      - type: volume
        source: data-volume
        target: /data
        volume:
          nocopy: true              # Don't copy data from container

      - type: tmpfs
        target: /tmp
        tmpfs:
          size: 100000000           # 100MB
          mode: 1777                # Permissions
```

### Resource Limits

```yaml
services:
  app:
    # CPU and memory limits (2025 syntax)
    deploy:
      resources:
        limits:
          cpus: '0.5'        # 50% of 1 CPU
          memory: 512M        # Max 512MB
        reservations:
          cpus: '0.25'       # Minimum 25% of 1 CPU
          memory: 256M        # Minimum 256MB

    # Process limits
    pids_limit: 100          # Max 100 processes

    # Memory swap
    mem_swappiness: 0        # Disable swap
```

### Healthchecks (Production-Ready)

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "node", "healthcheck.js"]
      # OR
      test: ["CMD-SHELL", "curl -f http://localhost:3000/health || exit 1"]
      # OR (disable healthcheck)
      disable: true

      interval: 30s          # Check every 30 seconds
      timeout: 10s           # Command must complete within 10s
      retries: 3             # Retry 3 times before marking unhealthy
      start_period: 40s      # Grace period for slow startup

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
```

### Dependencies (Modern Syntax)

```yaml
services:
  web:
    image: nginx
    depends_on:
      db:
        condition: service_healthy    # Wait for healthcheck
        restart: true                 # Restart if db restarts
      redis:
        condition: service_started    # Just wait for start
      migration:
        condition: service_completed_successfully  # Wait for completion

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s

  redis:
    image: redis:alpine

  migration:
    image: myapp:latest
    command: npm run migrate
```

### Logging Configuration

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"        # Max 10MB per log file
        max-file: "3"          # Keep max 3 files
        labels: "production"
        env: "NODE_ENV"

    # Alternative drivers
    # logging:
    #   driver: "syslog"
    # logging:
    #   driver: "journald"
    # logging:
    #   driver: "gelf"
```

### Security Options

```yaml
services:
  app:
    # Run as specific user
    user: "1000:1000"          # UID:GID
    # OR
    user: "appuser"

    # Read-only root filesystem
    read_only: true

    # tmpfs mounts for writes when read-only
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=100m

    # Security options
    security_opt:
      - no-new-privileges:true
      - apparmor:docker-default
      - seccomp:unconfined      # Use with caution

    # Capabilities
    cap_drop:
      - ALL                     # Drop all capabilities
    cap_add:
      - NET_BIND_SERVICE        # Add specific capability

    # Privileged mode (avoid if possible!)
    privileged: false
```

### Networking

```yaml
services:
  app:
    # Connect to networks
    networks:
      - frontend
      - backend

    # Advanced network configuration
    networks:
      frontend:
        ipv4_address: 172.16.238.10
        aliases:
          - api.local
      backend:
        priority: 1000

    # DNS configuration
    dns:
      - 8.8.8.8
      - 8.8.4.4
    dns_search:
      - example.com

    # Extra hosts (like /etc/hosts)
    extra_hosts:
      - "host.docker.internal:host-gateway"
      - "api.example.com:192.168.1.100"

    # Hostname
    hostname: api-server
    domainname: example.com
```

### Command and Entrypoint

```yaml
services:
  app:
    # Override CMD from Dockerfile
    command: ["npm", "start"]
    # OR
    command: npm start

    # Override ENTRYPOINT from Dockerfile
    entrypoint: ["/app/docker-entrypoint.sh"]
    # OR
    entrypoint: /app/docker-entrypoint.sh

    # Both together
    entrypoint: ["node"]
    command: ["server.js"]
```

### Working Directory

```yaml
services:
  app:
    working_dir: /app
```

### Labels and Metadata

```yaml
services:
  app:
    labels:
      com.example.description: "My Application"
      com.example.version: "1.0.0"
      com.example.team: "backend-team"
      traefik.enable: "true"        # For Traefik reverse proxy
```

### Profiles (Environment-Specific Services)

```yaml
services:
  app:
    image: myapp:latest
    # Always runs

  debug-tools:
    image: nicolaka/netshoot
    profiles:
      - debug                   # Only runs with --profile debug

  test-db:
    image: postgres:16-alpine
    profiles:
      - testing                 # Only runs with --profile testing

# Start with: docker compose --profile debug up
```

---

## Volumes

### Named Volumes

```yaml
services:
  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:                       # Simple named volume
    name: my-app-data          # Custom name (optional)

  # With options
  app-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/app

  # External volume (created outside compose)
  legacy-data:
    external: true
    name: old-app-data
```

### Volume Labels

```yaml
volumes:
  data:
    labels:
      com.example.description: "Application data"
      com.example.backup: "daily"
```

---

## Networks

### Network Configuration

```yaml
services:
  web:
    networks:
      - frontend
  api:
    networks:
      - frontend
      - backend
  db:
    networks:
      - backend

networks:
  frontend:
    driver: bridge              # Default

  backend:
    driver: bridge
    internal: true              # No external access

  # Custom bridge with subnet
  custom:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
          gateway: 172.28.0.1

  # External network (created outside compose)
  existing-network:
    external: true
    name: my-existing-network
```

### Network Drivers

```yaml
networks:
  # Bridge (default) - single host
  app-network:
    driver: bridge

  # Host networking (no isolation)
  host-net:
    driver: host

  # None (no networking)
  no-net:
    driver: none
```

---

## Secrets

### Secrets (for sensitive data)

```yaml
services:
  app:
    secrets:
      - db_password
      - api_key
    environment:
      # Read secrets from files
      DB_PASSWORD_FILE: /run/secrets/db_password
      API_KEY_FILE: /run/secrets/api_key

secrets:
  # From file
  db_password:
    file: ./secrets/db_password.txt

  # From environment variable
  api_key:
    environment: API_KEY

  # External (Docker Swarm)
  external_secret:
    external: true
    name: prod-api-key
```

**How to use in application:**

```javascript
// Node.js example
const fs = require('fs');
const dbPassword = fs.readFileSync('/run/secrets/db_password', 'utf8').trim();
```

---

## Configs

### Configuration Files

```yaml
services:
  app:
    configs:
      - source: nginx_config
        target: /etc/nginx/nginx.conf
        mode: 0440              # File permissions

configs:
  nginx_config:
    file: ./config/nginx.conf

  # External config
  app_config:
    external: true
    name: production-app-config
```

---

## Complete Examples

### Example 1: Simple Web Application

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Example 2: Full-Stack Application

```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8080
    depends_on:
      backend:
        condition: service_healthy

  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

### Example 3: Production-Ready Configuration

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      app:
        condition: service_healthy
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - frontend

  app:
    build:
      context: ./app
      dockerfile: Dockerfile.prod
    environment:
      - NODE_ENV=production
      - DATABASE_URL_FILE=/run/secrets/db_url
    secrets:
      - db_url
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD", "node", "healthcheck.js"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - frontend
      - backend

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=appuser
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
      - POSTGRES_DB=production
    secrets:
      - db_password
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - backend

  redis:
    image: redis:alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true

volumes:
  pgdata:
  redis-data:

secrets:
  db_url:
    file: ./secrets/db_url.txt
  db_password:
    file: ./secrets/db_password.txt
```

---

## Best Practices

### ✅ DO

```yaml
services:
  app:
    # ✅ Use specific image tags
    image: node:20.10.0-alpine

    # ✅ Use healthchecks
    healthcheck:
      test: ["CMD", "node", "healthcheck.js"]

    # ✅ Set restart policies
    restart: unless-stopped

    # ✅ Use depends_on with conditions
    depends_on:
      db:
        condition: service_healthy

    # ✅ Set resource limits
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

    # ✅ Configure logging
    logging:
      driver: "json-file"
      options:
        max-size: "10m"

    # ✅ Use secrets for sensitive data
    secrets:
      - db_password
```

### ❌ DON'T

```yaml
services:
  app:
    # ❌ Don't use 'latest' tag
    image: node:latest

    # ❌ Don't add version field (obsolete)
    version: "3.8"

    # ❌ Don't hardcode secrets
    environment:
      - DB_PASSWORD=secretpassword

    # ❌ Don't use restart: always (use unless-stopped)
    restart: always

    # ❌ Don't forget healthchecks for critical services
    # (no healthcheck defined)

    # ❌ Don't expose ports unnecessarily
    ports:
      - "5432:5432"  # Database port exposed to world!
```

---

## Common Patterns

### Pattern 1: Development vs Production

**docker-compose.yml** (base):
```yaml
services:
  app:
    build: ./app
    volumes:
      - app-data:/data

volumes:
  app-data:
```

**docker-compose.override.yml** (development, automatically loaded):
```yaml
services:
  app:
    volumes:
      - ./app:/app              # Mount source code
    environment:
      - DEBUG=true
    command: npm run dev        # Dev server with hot reload
```

**docker-compose.prod.yml** (production):
```yaml
services:
  app:
    restart: unless-stopped
    environment:
      - NODE_ENV=production
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

# Start with: docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Pattern 2: Variable Substitution

**.env file**:
```bash
# Application
APP_VERSION=1.0.0
APP_PORT=3000

# Database
POSTGRES_VERSION=16-alpine
POSTGRES_PASSWORD=changeme
```

**docker-compose.yml**:
```yaml
services:
  app:
    image: myapp:${APP_VERSION}
    ports:
      - "${APP_PORT}:3000"
    environment:
      - VERSION=${APP_VERSION}

  db:
    image: postgres:${POSTGRES_VERSION}
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
```

### Pattern 3: Extension Fields (DRY)

```yaml
# Define reusable configurations
x-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

x-healthcheck: &default-healthcheck
  interval: 30s
  timeout: 10s
  retries: 3

services:
  app1:
    image: myapp:latest
    logging: *default-logging
    healthcheck:
      <<: *default-healthcheck
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]

  app2:
    image: myapp:latest
    logging: *default-logging
    healthcheck:
      <<: *default-healthcheck
      test: ["CMD", "curl", "-f", "http://localhost:4000/health"]
```

---

## Useful Commands

```bash
# Start services
docker compose up
docker compose up -d               # Detached mode
docker compose up --build          # Rebuild images
docker compose up --force-recreate # Force recreate containers

# Stop services
docker compose stop                # Stop without removing
docker compose down                # Stop and remove
docker compose down -v             # Also remove volumes
docker compose down --rmi all      # Also remove images

# View status
docker compose ps                  # List services
docker compose ps -a               # List all (including stopped)

# Logs
docker compose logs                # All services
docker compose logs -f app         # Follow logs for 'app'
docker compose logs --tail=100     # Last 100 lines

# Execute commands
docker compose exec app sh         # Shell in 'app' service
docker compose exec app npm test   # Run command in 'app'

# Build
docker compose build               # Build all services
docker compose build app           # Build specific service
docker compose build --no-cache    # Build without cache

# Scale services
docker compose up -d --scale app=3 # Run 3 instances of 'app'

# Validate
docker compose config              # Validate and view config
docker compose config --services   # List services
```

---

## Troubleshooting

### Validation

```bash
# Check if compose file is valid
docker compose config

# Check specific service
docker compose config --services

# View resolved configuration
docker compose config --resolve-image-digests
```

### Common Issues

**Issue: Port already in use**
```bash
# Find what's using the port
lsof -i :8080

# Change port in compose file
ports:
  - "8081:80"  # Use different host port
```

**Issue: Service unhealthy**
```bash
# Check health status
docker compose ps

# View healthcheck logs
docker inspect <container> | grep -A 10 Health

# Test healthcheck manually
docker compose exec app curl -f http://localhost/health
```

**Issue: Cannot connect to other service**
```bash
# Services must be on same network
# Use service name as hostname
DATABASE_URL=postgresql://db:5432/myapp
#                         ^^
#                     service name, not IP
```

---

## Migration from v1 to v2

### Key Changes

1. **Remove version field**
   ```yaml
   # Remove this:
   version: "3.8"
   ```

2. **Update command syntax**
   ```bash
   # Old: docker-compose
   # New: docker compose
   ```

3. **depends_on conditions now work in non-swarm mode**
   ```yaml
   depends_on:
     db:
       condition: service_healthy  # Now works everywhere!
   ```

4. **Profiles for conditional services**
   ```yaml
   services:
     debug:
       profiles: ["debug"]
   ```

---

## Additional Resources

- [Compose Specification](https://github.com/compose-spec/compose-spec)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose v2 CLI](https://docs.docker.com/compose/cli-command/)
- [Environment Variables](https://docs.docker.com/compose/environment-variables/)

---

**Version:** 1.0 | **Last Updated:** October 2025
**Maintained by:** Docker Course Team

**Keep this guide handy when writing docker-compose.yml files!**
