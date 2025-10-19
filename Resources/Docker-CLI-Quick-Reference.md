# Docker CLI Quick Reference (2025 Edition)

**Last Updated:** October 2025
**Docker Version:** 25.0+

---

## 📋 Table of Contents

- [Essential Commands](#essential-commands)
- [Image Management](#image-management)
- [Container Management](#container-management)
- [Volume Management](#volume-management)
- [Network Management](#network-management)
- [Docker Compose](#docker-compose)
- [System Management](#system-management)
- [Security & Scanning](#security--scanning)
- [Debugging & Troubleshooting](#debugging--troubleshooting)
- [Tips & Tricks](#tips--tricks)

---

## Essential Commands

### Getting Help
```bash
docker --help                    # General help
docker <command> --help          # Command-specific help
docker version                   # Show Docker version
docker info                      # System-wide information
```

### Quick Start
```bash
docker run hello-world           # Test Docker installation
docker run -it ubuntu bash       # Interactive Ubuntu container
docker run -d nginx              # Run Nginx in background
docker ps                        # List running containers
docker stop <container>          # Stop a container
```

---

## Image Management

### Pulling Images
```bash
docker pull <image>              # Pull latest
docker pull <image>:<tag>        # Pull specific version
docker pull nginx:1.25-alpine    # Example: specific version

# Pull from specific registry
docker pull ghcr.io/owner/image
docker pull gcr.io/distroless/nodejs20-debian12
```

### Listing Images
```bash
docker images                    # List all images
docker image ls                  # Same as above (modern syntax)
docker images -a                 # Include intermediate images
docker images --filter "dangling=true"  # Unused images
```

### Building Images
```bash
docker build -t myapp:latest .                    # Build with tag
docker build -t myapp:v1 -f Dockerfile.prod .    # Custom Dockerfile
docker build --no-cache -t myapp:latest .         # Force rebuild

# BuildKit features (2025)
DOCKER_BUILDKIT=1 docker build -t myapp:latest .
docker build --secret id=npmrc,src=.npmrc .      # Build-time secrets
docker build --platform linux/amd64,linux/arm64 . # Multi-arch
```

### Inspecting Images
```bash
docker inspect <image>           # Detailed image info
docker history <image>           # Show image layers
docker image inspect <image>     # Modern syntax
```

### Removing Images
```bash
docker rmi <image>               # Remove one image
docker rmi $(docker images -q)   # Remove all images
docker image rm <image>          # Modern syntax
docker image prune               # Remove dangling images
docker image prune -a            # Remove all unused images
```

### Tagging Images
```bash
docker tag <image> <new-name>:<tag>
docker tag myapp:latest myapp:v1.0.0
docker tag myapp:latest username/myapp:latest  # For registry
```

### Pushing Images
```bash
docker login                     # Login to Docker Hub
docker push username/myapp:latest

# Push to other registries
docker tag myapp:latest ghcr.io/username/myapp:latest
docker push ghcr.io/username/myapp:latest
```

---

## Container Management

### Running Containers
```bash
# Basic run
docker run <image>               # Run and attach
docker run -d <image>            # Detached (background)
docker run -it <image> sh        # Interactive with shell

# With options
docker run -d \
  --name my-container \          # Custom name
  -p 8080:80 \                   # Port mapping
  -v /host/path:/container/path \# Volume mount
  -e KEY=value \                 # Environment variable
  --restart unless-stopped \     # Restart policy
  nginx:alpine

# Resource limits
docker run -d \
  --cpus="0.5" \                 # CPU limit
  --memory="512m" \              # Memory limit
  --pids-limit=100 \             # Process limit
  myapp:latest

# Security options
docker run -d \
  --user 1000:1000 \             # Non-root user
  --read-only \                  # Read-only filesystem
  --tmpfs /tmp:rw,size=100m \    # tmpfs mount
  --cap-drop=ALL \               # Drop all capabilities
  --cap-add=NET_BIND_SERVICE \   # Add specific capability
  --security-opt no-new-privileges:true \
  myapp:latest
```

### Listing Containers
```bash
docker ps                        # Running containers
docker ps -a                     # All containers
docker ps -q                     # Only container IDs
docker ps --filter "status=exited"  # Filter by status
docker ps --format "table {{.Names}}\t{{.Status}}"  # Custom format
```

### Container Lifecycle
```bash
docker start <container>         # Start stopped container
docker stop <container>          # Graceful stop (SIGTERM)
docker kill <container>          # Force stop (SIGKILL)
docker restart <container>       # Restart container
docker pause <container>         # Pause processes
docker unpause <container>       # Resume processes
```

### Executing Commands
```bash
docker exec -it <container> sh   # Interactive shell
docker exec <container> ls /app  # Run command
docker exec -u root <container> sh  # Exec as specific user
```

### Inspecting Containers
```bash
docker inspect <container>       # Full container details
docker logs <container>          # View logs
docker logs -f <container>       # Follow logs (tail -f)
docker logs --tail 100 <container>  # Last 100 lines
docker logs --since 10m <container> # Last 10 minutes
docker top <container>           # Running processes
docker stats                     # Resource usage (all)
docker stats <container>         # Resource usage (specific)
```

### Copying Files
```bash
docker cp <container>:/path/file ./local/  # Container to host
docker cp ./local/file <container>:/path/  # Host to container
```

### Removing Containers
```bash
docker rm <container>            # Remove stopped container
docker rm -f <container>         # Force remove (even if running)
docker rm $(docker ps -aq)       # Remove all containers
docker container prune           # Remove all stopped containers
```

---

## Volume Management

### Creating Volumes
```bash
docker volume create my-volume   # Create named volume
docker volume create \
  --driver local \
  --opt type=nfs \               # Custom driver options
  nfs-volume
```

### Listing Volumes
```bash
docker volume ls                 # List all volumes
docker volume ls -f dangling=true  # Unused volumes
```

### Inspecting Volumes
```bash
docker volume inspect my-volume  # Volume details
```

### Using Volumes
```bash
# Named volume
docker run -v my-volume:/data <image>

# Bind mount
docker run -v /host/path:/container/path <image>
docker run -v $(pwd):/app <image>  # Current directory

# Read-only mount
docker run -v my-volume:/data:ro <image>

# tmpfs (temporary, in-memory)
docker run --tmpfs /tmp:rw,size=100m <image>
```

### Removing Volumes
```bash
docker volume rm my-volume       # Remove specific volume
docker volume prune              # Remove unused volumes
```

### Backup & Restore
```bash
# Backup volume
docker run --rm \
  -v my-volume:/data:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .

# Restore volume
docker run --rm \
  -v my-volume:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /data
```

---

## Network Management

### Creating Networks
```bash
docker network create my-network              # Default bridge
docker network create --driver bridge my-net  # Explicit bridge
docker network create --driver host host-net  # Host networking
docker network create --internal private-net  # No external access
```

### Listing Networks
```bash
docker network ls                # List all networks
docker network ls --filter driver=bridge
```

### Inspecting Networks
```bash
docker network inspect my-network  # Network details
```

### Connecting Containers
```bash
# At runtime
docker run --network my-network <image>

# Connect existing container
docker network connect my-network <container>
docker network disconnect my-network <container>
```

### Removing Networks
```bash
docker network rm my-network     # Remove network
docker network prune             # Remove unused networks
```

---

## Docker Compose

### Basic Commands
```bash
docker compose up                # Start services
docker compose up -d             # Start in background
docker compose up --build        # Rebuild and start
docker compose down              # Stop and remove
docker compose down -v           # Also remove volumes

docker compose start             # Start stopped services
docker compose stop              # Stop services
docker compose restart           # Restart services
```

### Service Management
```bash
docker compose ps                # List services
docker compose logs              # View logs
docker compose logs -f service   # Follow specific service
docker compose exec service sh   # Exec into service

docker compose build             # Build services
docker compose pull              # Pull images
docker compose push              # Push images
```

### Scaling
```bash
docker compose up -d --scale web=3  # Run 3 instances of web
```

### Validation
```bash
docker compose config            # Validate and view config
docker compose config --services # List services
```

---

## System Management

### System Information
```bash
docker info                      # System-wide information
docker version                   # Client and server versions
docker system df                 # Disk usage
docker system df -v              # Detailed disk usage
```

### Cleanup Commands
```bash
# Remove everything unused
docker system prune              # Containers, networks, images (dangling)
docker system prune -a           # Also unused images
docker system prune -a --volumes # Also unused volumes

# Individual cleanup
docker container prune           # Remove stopped containers
docker image prune               # Remove dangling images
docker image prune -a            # Remove unused images
docker volume prune              # Remove unused volumes
docker network prune             # Remove unused networks
```

### Events
```bash
docker events                    # Real-time events
docker events --since 1h         # Events from last hour
docker events --filter type=container
```

---

## Security & Scanning

### Docker Scout (2025)
```bash
docker scout version             # Check Scout version
docker scout quickview <image>   # Quick security overview
docker scout cves <image>        # Detailed CVE report
docker scout recommendations <image>  # Get recommendations
docker scout compare <img1> --to <img2>  # Compare images
```

### Image Scanning
```bash
# Scan image before running
docker scout cves nginx:latest

# Scan local image
docker scout cves myapp:latest

# Get recommendations
docker scout recommendations myapp:latest
```

---

## Debugging & Troubleshooting

### Viewing Logs
```bash
docker logs <container>          # All logs
docker logs -f <container>       # Follow logs
docker logs --tail 50 <container>  # Last 50 lines
docker logs --since 10m <container>  # Last 10 minutes
docker logs --timestamps <container>  # With timestamps
```

### Inspecting Containers
```bash
docker inspect <container>       # Full details (JSON)
docker inspect --format '{{.State.Status}}' <container>
docker inspect --format '{{.NetworkSettings.IPAddress}}' <container>
```

### Resource Monitoring
```bash
docker stats                     # All containers
docker stats <container>         # Specific container
docker top <container>           # Processes in container
```

### Container Shell Access
```bash
docker exec -it <container> sh   # Alpine/minimal
docker exec -it <container> bash # Ubuntu/Debian
docker exec -it <container> /bin/sh  # Explicit path

# As root (if needed)
docker exec -it -u root <container> sh
```

### Checking Container Status
```bash
docker ps -a                     # All containers with status
docker inspect --format '{{.State.Health.Status}}' <container>
```

---

## Tips & Tricks

### Useful Aliases
```bash
# Add to ~/.bashrc or ~/.zshrc
alias d='docker'
alias dc='docker compose'
alias dps='docker ps'
alias dpsa='docker ps -a'
alias di='docker images'
alias dex='docker exec -it'
alias dlog='docker logs -f'
alias dclean='docker system prune -af --volumes'
```

### One-Liners
```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Get container IP address
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container>

# Follow logs of multiple containers
docker compose logs -f service1 service2

# Remove exited containers
docker rm $(docker ps -q -f status=exited)

# Remove untagged images
docker rmi $(docker images -f "dangling=true" -q)
```

### Formatting Output
```bash
# Custom table format
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"

# JSON format
docker inspect --format='{{json .}}' <container> | jq

# Specific field
docker inspect --format='{{.Config.Image}}' <container>
```

### BuildKit Environment Variables
```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# BuildKit progress output
export BUILDKIT_PROGRESS=plain  # Detailed output
export BUILDKIT_PROGRESS=tty    # Default progress bar
```

### Useful Flags
```bash
--rm                             # Auto-remove container when it exits
-it                              # Interactive with TTY
-d                               # Detached mode
--name                           # Assign container name
-p 8080:80                       # Port mapping
-v /host:/container              # Volume mount
-e VAR=value                     # Environment variable
--network                        # Specify network
--restart unless-stopped         # Restart policy
```

---

## Quick Troubleshooting

### Container Won't Start
```bash
docker logs <container>          # Check logs
docker inspect <container>       # Check config
docker events                    # Monitor events
```

### Port Already in Use
```bash
# Find process using port (Mac/Linux)
lsof -i :8080
# Kill it
kill -9 <PID>
```

### Container Can't Connect to Network
```bash
docker network inspect bridge   # Check network
docker exec <container> ping google.com  # Test connectivity
```

### Out of Disk Space
```bash
docker system df                 # Check usage
docker system prune -a --volumes # Clean up
```

### Permission Denied
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
# Then logout and login again
```

---

## Command Syntax Comparison

### Old Style vs New Style (Modern)

| Old | New (Modern) | Notes |
|-----|--------------|-------|
| `docker ps` | `docker container ls` | Both work |
| `docker images` | `docker image ls` | Both work |
| `docker rmi` | `docker image rm` | Both work |
| `docker rm` | `docker container rm` | Both work |
| `docker-compose` | `docker compose` | v2 uses space! |

**Recommendation:** Use new style for consistency, but both are valid in 2025.

---

## Environment Variables

```bash
DOCKER_HOST                      # Docker daemon socket
DOCKER_BUILDKIT                  # Enable BuildKit (1 or 0)
BUILDKIT_PROGRESS               # BuildKit output (plain or tty)
DOCKER_DEFAULT_PLATFORM         # Default platform (linux/amd64)
```

---

## Related Commands

```bash
docker buildx                    # Multi-platform builds
docker scan                      # Deprecated (use scout)
docker scout                     # Security scanning (2025)
docker context                   # Manage Docker contexts
docker plugin                    # Manage plugins
```

---

## Resources

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Docker Scout Documentation](https://docs.docker.com/scout/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

---

**Print this page and keep it handy while learning Docker!**

**Version:** 2025.1 | **Maintained By:** Docker Course Team
