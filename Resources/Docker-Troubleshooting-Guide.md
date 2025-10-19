# Docker Troubleshooting Guide (2025 Edition)

**Last Updated:** October 2025
**Target:** Common issues students and developers face with Docker

---

## 📋 Table of Contents

- [General Debugging Approach](#general-debugging-approach)
- [Installation & Setup Issues](#installation--setup-issues)
- [Container Issues](#container-issues)
- [Image Building Issues](#image-building-issues)
- [Networking Issues](#networking-issues)
- [Volume & Permission Issues](#volume--permission-issues)
- [Docker Compose Issues](#docker-compose-issues)
- [Performance Issues](#performance-issues)
- [Security Issues](#security-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Debugging Tools & Commands](#debugging-tools--commands)

---

## General Debugging Approach

### Step-by-Step Debugging Process

1. **Check container status**
   ```bash
   docker ps -a
   ```

2. **View logs**
   ```bash
   docker logs <container>
   docker logs -f <container>  # Follow logs
   ```

3. **Inspect container details**
   ```bash
   docker inspect <container>
   ```

4. **Exec into container** (if running)
   ```bash
   docker exec -it <container> sh
   ```

5. **Check resource usage**
   ```bash
   docker stats
   ```

6. **View system events**
   ```bash
   docker events
   ```

---

## Installation & Setup Issues

### Issue: Docker daemon not running

**Symptoms:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solutions:**

**On Mac/Windows:**
```bash
# Open Docker Desktop application
# Wait for "Docker Desktop is running" status
```

**On Linux:**
```bash
# Start Docker daemon
sudo systemctl start docker

# Enable on boot
sudo systemctl enable docker

# Check status
sudo systemctl status docker
```

---

### Issue: Permission denied accessing Docker socket (Linux)

**Symptoms:**
```
permission denied while trying to connect to Docker daemon socket
```

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in, then verify
groups
# Should show 'docker' in the list

# Alternative: Run with sudo (not recommended for regular use)
sudo docker ps
```

---

### Issue: WSL 2 not enabled (Windows)

**Symptoms:**
```
WSL 2 installation is incomplete
```

**Solution:**
```powershell
# Run in PowerShell as Administrator
wsl --install

# Or enable specific distribution
wsl --set-default-version 2

# Restart computer
```

---

## Container Issues

### Issue: Container exits immediately

**Symptoms:**
```bash
docker ps    # Container not listed
docker ps -a # Container shows "Exited (0)" or "Exited (1)"
```

**Diagnosis:**
```bash
# Check exit code and logs
docker ps -a
docker logs <container>
```

**Common Causes & Solutions:**

**1. No long-running process**
```dockerfile
# ❌ BAD - Container exits after echo
CMD echo "Hello"

# ✅ GOOD - Long-running process
CMD ["nginx", "-g", "daemon off;"]
# OR
CMD ["node", "server.js"]
```

**2. Application crashes on startup**
```bash
# Check logs for error messages
docker logs <container>

# Common issues:
# - Missing environment variables
# - Failed to connect to database
# - Port already in use
# - Missing dependencies
```

**3. Wrong entrypoint/command**
```bash
# Try running interactively to debug
docker run -it <image> sh

# Then manually run your command to see errors
node server.js
```

---

### Issue: Container stuck in "Restarting" state

**Symptoms:**
```bash
docker ps
# STATUS: Restarting (1) Less than a second ago
```

**Cause:**
- Container crashes immediately after starting
- Restart policy keeps retrying

**Solution:**
```bash
# Stop the container
docker stop <container>

# Check logs
docker logs <container>

# Remove restart policy temporarily
docker update --restart=no <container>

# Fix the underlying issue, then restart
docker start <container>
```

---

### Issue: Cannot remove container

**Symptoms:**
```
Error response from daemon: You cannot remove a running container
```

**Solutions:**

**Method 1: Stop then remove**
```bash
docker stop <container>
docker rm <container>
```

**Method 2: Force remove**
```bash
docker rm -f <container>
```

**Method 3: Container won't stop**
```bash
# Force kill
docker kill <container>
docker rm <container>
```

---

### Issue: Container using too much memory/CPU

**Diagnosis:**
```bash
# View resource usage
docker stats

# Inspect resource limits
docker inspect <container> | grep -i memory
docker inspect <container> | grep -i cpu
```

**Solutions:**

**Set limits when running:**
```bash
docker run -d \
  --memory="512m" \
  --cpus="0.5" \
  myapp:latest
```

**Update existing container:**
```bash
docker update --memory="512m" --cpus="0.5" <container>
```

**In docker-compose.yml:**
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

---

### Issue: Cannot access container (health check failing)

**Symptoms:**
```
docker ps
# STATUS: (unhealthy)
```

**Diagnosis:**
```bash
# View health check details
docker inspect <container> | grep -A 20 Health

# Check specific health check logs
docker inspect <container> --format='{{json .State.Health}}' | jq
```

**Common Solutions:**

**1. Increase timeouts**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost/health"]
  interval: 30s
  timeout: 10s        # Increase if too low
  retries: 3
  start_period: 60s   # Increase for slow-starting apps
```

**2. Fix health check command**
```bash
# Test health check manually
docker exec <container> curl -f http://localhost/health

# Common issues:
# - curl not installed (use native language check)
# - Wrong port/path
# - App not listening yet
```

**3. Application not ready**
```bash
# Check if app is listening
docker exec <container> netstat -tulpn
# OR
docker exec <container> ss -tulpn
```

---

## Image Building Issues

### Issue: Build context too large / slow

**Symptoms:**
```
Sending build context to Docker daemon  2.5GB
```

**Solution: Use .dockerignore**

**.dockerignore:**
```
# Dependencies
node_modules
venv
__pycache__

# Build outputs
dist
build
*.log

# Version control
.git
.gitignore

# IDE
.vscode
.idea
*.swp

# OS files
.DS_Store
Thumbs.db

# Temporary files
tmp/
temp/
*.tmp
```

**Verify reduction:**
```bash
# Check build context size
docker build --no-cache -t test . 2>&1 | grep "Sending build context"
```

---

### Issue: Cache not working / slow rebuilds

**Problem:**
```bash
# Every build reinstalls all dependencies
```

**Solution: Optimize layer order**

```dockerfile
# ❌ BAD - Code changes invalidate npm install
COPY . /app
WORKDIR /app
RUN npm install

# ✅ GOOD - Dependencies cached separately
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
```

**Enable BuildKit for better caching:**
```bash
export DOCKER_BUILDKIT=1
docker build -t myapp:latest .
```

---

### Issue: Build fails with "no space left on device"

**Symptoms:**
```
ERROR: failed to solve: failed to copy: no space left on device
```

**Solutions:**

**Clean up Docker resources:**
```bash
# Remove dangling images
docker image prune

# Remove all unused images
docker image prune -a

# Remove all unused containers, volumes, networks
docker system prune -a --volumes

# Check disk usage
docker system df
```

**Increase disk space (Docker Desktop):**
1. Open Docker Desktop Settings
2. Resources → Advanced
3. Increase "Disk image size"
4. Apply & Restart

---

### Issue: Multi-stage build not reducing image size

**Problem:**
```dockerfile
# Still getting large image despite multi-stage
FROM node:20 AS builder
RUN npm install
RUN npm run build

FROM node:20
COPY --from=builder /app /app
# Image still large!
```

**Solutions:**

**1. Use smaller final image:**
```dockerfile
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ✅ Use alpine or distroless
FROM node:20-alpine
# OR
FROM gcr.io/distroless/nodejs20-debian12

WORKDIR /app
# Only copy necessary files
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./

CMD ["node", "dist/server.js"]
```

**2. Verify what's copied:**
```bash
# Explore image layers
dive myapp:latest
```

---

### Issue: BuildKit secret mount not working

**Symptoms:**
```
ERROR: failed to solve: failed to load LLB
```

**Solution:**

**Enable BuildKit:**
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine

RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci --only=production
```

**Build with secret:**
```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Pass secret file
docker build --secret id=npmrc,src=.npmrc -t myapp:latest .
```

---

## Networking Issues

### Issue: Cannot access container from host

**Symptoms:**
```bash
curl localhost:8080
# Connection refused
```

**Diagnosis:**
```bash
# Check if container is running
docker ps

# Check port mappings
docker port <container>

# Check if app is listening
docker exec <container> netstat -tulpn
```

**Common Solutions:**

**1. Port not mapped:**
```bash
# ❌ Missing -p flag
docker run myapp:latest

# ✅ Map port
docker run -p 8080:3000 myapp:latest
#          ^^^^^ ^^^^^
#          host  container
```

**2. App listening on wrong interface:**
```javascript
// ❌ BAD - Only listens on localhost
app.listen(3000, 'localhost')

// ✅ GOOD - Listens on all interfaces
app.listen(3000, '0.0.0.0')
```

**3. Port already in use on host:**
```bash
# Find what's using the port
lsof -i :8080

# Kill the process or use different port
docker run -p 8081:3000 myapp:latest
```

---

### Issue: Containers cannot communicate with each other

**Symptoms:**
```bash
# From container A:
curl http://container-b:3000
# Could not resolve host: container-b
```

**Diagnosis:**
```bash
# Check if containers are on same network
docker inspect <container-a> | grep NetworkMode
docker inspect <container-b> | grep NetworkMode
```

**Solutions:**

**1. Put containers on same network:**
```bash
# Create network
docker network create mynetwork

# Run containers on network
docker run -d --name container-a --network mynetwork image-a
docker run -d --name container-b --network mynetwork image-b

# Now they can communicate using container names
docker exec container-a ping container-b
```

**2. Using Docker Compose (automatic network):**
```yaml
services:
  app:
    image: myapp:latest
    environment:
      - DB_HOST=db  # Use service name as hostname
  db:
    image: postgres:16-alpine

# Docker Compose creates network automatically
```

**3. Test connectivity:**
```bash
# From container A, ping container B
docker exec container-a ping container-b

# Check DNS resolution
docker exec container-a nslookup container-b

# Test port connectivity
docker exec container-a telnet container-b 3000
```

---

### Issue: Cannot reach external network from container

**Symptoms:**
```bash
docker exec <container> curl google.com
# Could not resolve host: google.com
```

**Solutions:**

**1. Check Docker DNS:**
```bash
docker run --rm alpine nslookup google.com
```

**2. Configure DNS servers:**
```bash
docker run --dns 8.8.8.8 --dns 8.8.4.4 myapp:latest
```

**In docker-compose.yml:**
```yaml
services:
  app:
    image: myapp:latest
    dns:
      - 8.8.8.8
      - 8.8.4.4
```

**3. Check network mode:**
```bash
# Make sure not using 'none' network
docker inspect <container> | grep NetworkMode
```

---

## Volume & Permission Issues

### Issue: Permission denied in mounted volume

**Symptoms:**
```
EACCES: permission denied, open '/data/file.txt'
```

**Cause:**
- Container user UID doesn't match host file UID
- Common on Linux hosts

**Diagnosis:**
```bash
# Check file ownership on host
ls -la ./data

# Check user in container
docker exec <container> id

# Check file ownership in container
docker exec <container> ls -la /data
```

**Solutions:**

**Solution 1: Run container as same UID as host**
```bash
docker run -d --user $(id -u):$(id -g) \
  -v ./data:/data \
  myapp:latest
```

**Solution 2: Fix ownership in Dockerfile**
```dockerfile
FROM node:20-alpine

# Create user with specific UID/GID
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -s /bin/sh -D appuser

# Set ownership when copying
COPY --chown=appuser:appgroup . /app

USER appuser
```

**Solution 3: Use COPY --chown in bind mounts**
```yaml
# docker-compose.yml
services:
  app:
    image: myapp:latest
    user: "1000:1000"  # Match host UID:GID
    volumes:
      - ./data:/data
```

**Solution 4: Fix permissions on host**
```bash
# Change ownership of host directory
sudo chown -R $(id -u):$(id -g) ./data

# OR make it writable by all (less secure)
chmod -R 777 ./data
```

---

### Issue: Volume data not persisting

**Symptoms:**
```bash
# Data disappears after container restart
```

**Common Causes:**

**1. Using anonymous volumes:**
```bash
# ❌ Anonymous volume - gets deleted
docker run -v /data myapp:latest

# ✅ Named volume - persists
docker run -v mydata:/data myapp:latest
```

**2. Removing container with -v flag:**
```bash
# ❌ Removes volumes
docker rm -v <container>

# ✅ Keeps volumes
docker rm <container>
```

**3. Using tmpfs instead of volume:**
```bash
# tmpfs is temporary (RAM-based)
docker run --tmpfs /data myapp:latest

# Use volume for persistence
docker run -v mydata:/data myapp:latest
```

**Verify volume:**
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect mydata

# Check if volume has data
docker run --rm -v mydata:/data alpine ls -la /data
```

---

### Issue: Cannot remove volume

**Symptoms:**
```
Error response from daemon: volume is in use
```

**Solution:**
```bash
# Find which container is using the volume
docker ps -a --filter volume=myvolume

# Stop and remove containers
docker rm -f <container>

# Now remove volume
docker volume rm myvolume

# Force remove all unused volumes
docker volume prune
```

---

## Docker Compose Issues

### Issue: "version is obsolete" warning

**Symptoms:**
```
WARN[0000] version is obsolete
```

**Solution:**
```yaml
# ❌ Remove this line
version: "3.8"

# ✅ Start directly with services
services:
  app:
    image: myapp:latest
```

---

### Issue: Service dependencies not working

**Symptoms:**
```
# App starts before database is ready
Error: connect ECONNREFUSED
```

**Solution: Use healthcheck with depends_on**

```yaml
services:
  app:
    image: myapp:latest
    depends_on:
      db:
        condition: service_healthy  # Wait for health
    environment:
      - DB_HOST=db

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
```

---

### Issue: Environment variables not loading

**Symptoms:**
```javascript
// process.env.API_KEY is undefined
```

**Solutions:**

**1. Check .env file location:**
```bash
# Must be in same directory as docker-compose.yml
ls -la .env

# Verify contents
cat .env
```

**2. Check .env file format:**
```bash
# ✅ CORRECT
API_KEY=abc123
DB_HOST=localhost

# ❌ WRONG - No spaces around =
API_KEY = abc123

# ❌ WRONG - No export keyword
export API_KEY=abc123
```

**3. Explicit env_file:**
```yaml
services:
  app:
    env_file:
      - .env
      - .env.production
```

**4. Verify in container:**
```bash
docker compose exec app env | grep API_KEY
```

---

### Issue: Compose file not found

**Symptoms:**
```
Can't find a suitable configuration file in this directory
```

**Solutions:**

**1. File naming:**
```bash
# Docker looks for these files (in order):
# - docker-compose.yml
# - docker-compose.yaml
# - compose.yml
# - compose.yaml
```

**2. Specify file explicitly:**
```bash
docker compose -f my-compose.yml up
```

**3. Check current directory:**
```bash
pwd
ls -la docker-compose.yml
```

---

### Issue: Service cannot be scaled

**Symptoms:**
```
Error: Cannot create container for service app: Conflict
```

**Cause:**
- Fixed container name prevents scaling
- Port conflicts when scaling

**Solution:**
```yaml
services:
  app:
    image: myapp:latest
    # ❌ Don't set container_name when scaling
    # container_name: my-app

    # ❌ Don't fix host port when scaling
    # ports:
    #   - "8080:3000"

    # ✅ Let Docker assign ports
    expose:
      - "3000"

    # OR use port range
    ports:
      - "8080-8082:3000"
```

**Scale services:**
```bash
docker compose up -d --scale app=3
```

---

## Performance Issues

### Issue: Slow image builds

**Diagnosis:**
```bash
# Time the build
time docker build -t myapp:latest .
```

**Solutions:**

**1. Use BuildKit cache mounts:**
```dockerfile
# syntax=docker/dockerfile:1

FROM node:20-alpine

WORKDIR /app
COPY package*.json ./

# Cache npm packages
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

COPY . .
CMD ["node", "server.js"]
```

**2. Optimize layer order:**
```dockerfile
# Copy dependencies first (change less frequently)
COPY package*.json ./
RUN npm ci

# Copy code last (changes frequently)
COPY . .
```

**3. Use smaller base images:**
```dockerfile
# node:20 → 1GB
# node:20-alpine → 150MB
# gcr.io/distroless/nodejs20 → 100MB
FROM node:20-alpine
```

**4. Multi-stage builds:**
```dockerfile
FROM node:20 AS builder
RUN npm install && npm run build

FROM node:20-alpine
COPY --from=builder /app/dist /app/dist
```

---

### Issue: Container using too much disk space

**Diagnosis:**
```bash
# Check disk usage
docker system df

# Detailed view
docker system df -v
```

**Solutions:**
```bash
# Remove dangling images
docker image prune

# Remove all unused images
docker image prune -a

# Remove all unused resources
docker system prune -a --volumes

# Configure log rotation
docker run -d \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  myapp:latest
```

---

## Security Issues

### Issue: Container running as root

**Diagnosis:**
```bash
docker exec <container> whoami
# Output: root  ← ❌ Bad!
```

**Solution:**
```dockerfile
FROM node:20-alpine

# Create non-root user
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

# Set ownership
WORKDIR /app
COPY --chown=appuser:appgroup . /app

# Switch to non-root user
USER appuser

CMD ["node", "server.js"]
```

**Verify:**
```bash
docker run --rm myapp:latest whoami
# Output: appuser  ← ✅ Good!
```

---

### Issue: High severity vulnerabilities in image

**Diagnosis:**
```bash
docker scout cves myapp:latest
# 15 Critical, 42 High vulnerabilities
```

**Solutions:**

**1. Update base image:**
```dockerfile
# Update to latest patch version
FROM node:20.10.0-alpine3.18
```

**2. Use distroless:**
```dockerfile
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

FROM gcr.io/distroless/nodejs20-debian12
COPY --from=builder /app /app
WORKDIR /app
CMD ["server.js"]
```

**3. Scan and fix:**
```bash
docker scout recommendations myapp:latest
# Follow recommendations
```

---

## Platform-Specific Issues

### Mac (Apple Silicon M1/M2/M3)

**Issue: Platform mismatch warnings**
```
WARNING: The requested image's platform (linux/amd64) does not match
```

**Solutions:**

**1. Build for correct platform:**
```bash
docker build --platform linux/arm64 -t myapp:latest .
```

**2. Use multi-platform:**
```bash
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

**3. Specify in Dockerfile:**
```dockerfile
FROM --platform=linux/arm64 node:20-alpine
```

---

### Windows

**Issue: Line ending problems**
```bash
# Script fails with: command not found
```

**Cause:**
- Windows CRLF line endings (\r\n)
- Linux expects LF line endings (\n)

**Solution:**

**.gitattributes:**
```
# Force LF line endings
*.sh text eol=lf
Dockerfile text eol=lf
```

**Convert existing files:**
```bash
# Using dos2unix
dos2unix script.sh

# Using PowerShell
(Get-Content script.sh) -replace "`r`n", "`n" | Set-Content script.sh -NoNewline
```

---

## Debugging Tools & Commands

### Essential Debugging Commands

```bash
# Container status
docker ps -a
docker inspect <container>
docker logs <container>
docker logs -f --tail 100 <container>

# Execute commands in container
docker exec -it <container> sh
docker exec <container> ps aux
docker exec <container> env

# Resource usage
docker stats
docker top <container>

# Network debugging
docker network inspect <network>
docker exec <container> ping <other-container>
docker exec <container> netstat -tulpn

# System information
docker info
docker version
docker system df

# Events monitoring
docker events
docker events --filter container=<container>

# Image inspection
docker history <image>
docker inspect <image>
```

### Advanced Debugging Tools

**Dive - Explore image layers:**
```bash
# Install
brew install dive  # Mac
# OR https://github.com/wagoodman/dive

# Explore image
dive myapp:latest
```

**Ctop - Container metrics:**
```bash
# Install
brew install ctop  # Mac

# Run
ctop
```

**Lazydocker - Terminal UI:**
```bash
# Install
brew install lazydocker  # Mac

# Run
lazydocker
```

---

## Quick Troubleshooting Checklist

When something goes wrong:

- [ ] **Check container status**
  ```bash
  docker ps -a
  ```

- [ ] **Read logs**
  ```bash
  docker logs <container>
  ```

- [ ] **Inspect configuration**
  ```bash
  docker inspect <container>
  ```

- [ ] **Test network connectivity**
  ```bash
  docker exec <container> ping google.com
  docker exec <container> ping <other-container>
  ```

- [ ] **Check resource usage**
  ```bash
  docker stats
  ```

- [ ] **Verify environment variables**
  ```bash
  docker exec <container> env
  ```

- [ ] **Test manually in container**
  ```bash
  docker exec -it <container> sh
  ```

- [ ] **Check Docker daemon status**
  ```bash
  docker info
  ```

- [ ] **Clean up and retry**
  ```bash
  docker system prune
  docker compose down -v
  docker compose up --build
  ```

---

## Getting Help

### Documentation Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Forums](https://forums.docker.com/)
- [Stack Overflow - docker tag](https://stackoverflow.com/questions/tagged/docker)

### Debug Mode

```bash
# Enable debug logging
export DOCKER_BUILDKIT=1
export BUILDKIT_PROGRESS=plain
docker build -t myapp:latest .

# Docker daemon debug mode
# Edit /etc/docker/daemon.json
{
  "debug": true
}
# Restart Docker daemon
```

---

**Version:** 1.0 | **Last Updated:** October 2025
**Maintained by:** Docker Course Team

**Keep this guide handy for quick troubleshooting!**
