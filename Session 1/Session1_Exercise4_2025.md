# Exercise 4: Docker 2025 Features & Modern Tooling

**Session 1: Introduction to Docker**
**Filename:** `Session1_Exercise4_2025.md`

## Objective
- Explore Docker's latest 2025 features
- Understand Docker Desktop AI capabilities
- Verify modern tooling (BuildKit, Docker Scout)
- Learn about Docker Compose v2
- Understand container ecosystem in 2025

---

## Part 1: Docker Desktop 2025 Features

### Step 1: Verify Docker Desktop Version

Check you're running a modern Docker Desktop version:

```bash
docker version
```

**Look for:**
- Docker Engine: 25.0+ (or Docker Desktop 4.27+)
- Compose: v2.24+
- BuildKit: Enabled by default

**Expected output (2025):**
```
Client:
 Version:           25.0.0
 API version:       1.44
 Go version:        go1.21.0
 Git commit:        ...
 Built:             ...
 OS/Arch:           darwin/arm64
 Context:           desktop-linux

Server: Docker Desktop
 Engine:
  Version:          25.0.0
  API version:      1.44 (minimum version 1.24)
```

---

### Step 2: Docker Desktop AI Agent (Beta - 2025)

**Docker Desktop AI** helps you write Dockerfiles, troubleshoot issues, and learn Docker.

**Note:** This feature requires Docker Desktop 4.38+ and may need enabling in Settings.

**To enable:**
1. Open Docker Desktop
2. Go to Settings → Features
3. Enable "Docker AI Agent (Beta)"
4. Restart Docker Desktop

**Try the AI Assistant:**
```bash
# Ask Docker AI for help (if available)
docker ai "How do I build a Node.js application?"
```

**Benefits of Docker AI (2025):**
- 🤖 Natural language Dockerfile generation
- 🔍 Error explanation and troubleshooting
- 📚 Best practices suggestions
- ⚡ Quick command assistance

---

### Step 3: Docker Scout Integration

**Docker Scout** is built into Docker Desktop for vulnerability scanning.

**Check Scout availability:**
```bash
docker scout version
```

**Quick image scan:**
```bash
# Pull an image
docker pull nginx:latest

# Scan it with Scout
docker scout quickview nginx:latest
```

**What Scout shows you:**
- Number of vulnerabilities (Critical, High, Medium, Low)
- Recommendations for safer base images
- CVE details

**Example output:**
```
   Target     nginx:latest
   Digest     sha256:abc123...
   Platform   linux/amd64

Vulnerabilities:
  5 Critical
  12 High
  15 Medium
  10 Low

Recommendation: Use nginx:1.25-alpine (18 fewer CVEs)
```

---

### Step 4: BuildKit - Modern Build Engine

**BuildKit** is Docker's modern build engine (default since Docker 23.0).

**Verify BuildKit is enabled:**
```bash
docker buildx version
```

**Check BuildKit status:**
```bash
docker info | grep BuildKit
# Should show: BuildKit: enabled
```

**BuildKit benefits (2025)standard):**
- ⚡ Faster builds with better caching
- 🔒 Secret mounts for secure builds
- 🌐 Multi-architecture builds
- 📦 Cache mounts for package managers

**Simple BuildKit test:**
```bash
# Create a simple Dockerfile
echo 'FROM alpine
RUN echo "BuildKit test"' > Dockerfile.test

# Build with BuildKit (automatic in modern Docker)
docker build -f Dockerfile.test -t buildkit-test .

# Clean up
rm Dockerfile.test
docker rmi buildkit-test
```

---

## Part 2: Docker Compose v2

### Step 5: Verify Docker Compose v2

**Docker Compose v2** is integrated into Docker CLI (no separate install needed).

**Check version:**
```bash
docker compose version
```

**Expected (2025):**
```
Docker Compose version v2.24.0
```

**Key differences from v1:**
- ✅ `docker compose` (space) not `docker-compose` (hyphen)
- ✅ Integrated into Docker CLI
- ✅ Written in Go (faster than Python v1)
- ✅ No `version:` field needed in compose files

**Test Compose v2:**
```bash
# Create a simple compose file
cat > docker-compose-test.yml <<'EOF'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
EOF

# Use modern compose command (with space)
docker compose -f docker-compose-test.yml up -d

# Check it's running
curl http://localhost:8080

# Clean up
docker compose -f docker-compose-test.yml down
rm docker-compose-test.yml
```

---

## Part 3: Modern Docker Ecosystem (2025)

### Step 6: Understanding the Container Ecosystem

**Container ecosystem in 2025:**

```
┌─────────────────────────────────────┐
│      Docker Desktop (2025)          │
│  ┌───────────────────────────────┐  │
│  │   Docker Engine 25.0+         │  │
│  │   - BuildKit (default)        │  │
│  │   - containerd                │  │
│  │   - runc                      │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │   Docker Compose v2           │  │
│  │   - Integrated in CLI         │  │
│  │   - Modern syntax             │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │   Docker Scout                │  │
│  │   - Vulnerability scanning    │  │
│  │   - Recommendations           │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │   Docker AI (Beta)            │  │
│  │   - Natural language help     │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**OCI Standards (Open Container Initiative):**
- Docker images are OCI-compliant
- Can run on Docker, Kubernetes, Podman, etc.
- Ensures portability across platforms

---

### Step 7: Container Standards & Compatibility

**Check OCI compliance:**
```bash
docker info | grep -i "runtime"
# Should show: runc
```

**What is runc?**
- Low-level container runtime
- OCI-compliant
- Used by Docker, Kubernetes, and others

**Container image standards:**
- Images follow OCI Image Format
- Portable across different container platforms
- Layer-based architecture

---

## Part 4: Docker Hub & Registries (2025)

### Step 8: Working with Docker Hub

**Docker Hub statistics (2025):**
- 15+ billion image pulls
- 13+ million developers
- Official images verified by Docker
- Free for personal use

**Search Docker Hub:**
```bash
# Search for Node.js images
docker search node --limit 5

# Pull specific version
docker pull node:20-alpine

# Inspect image
docker inspect node:20-alpine | grep -i author
```

**Understanding image tags:**

| Tag | Meaning | Use Case |
|-----|---------|----------|
| `latest` | ❌ Avoid - unstable | Never in production |
| `20` | Major version | Development |
| `20.10` | Minor version | Staging |
| `20.10.0` | Exact version | ✅ Production |
| `20-alpine` | Minimal variant | ✅ Production (smaller) |
| `20.10.0-alpine` | Best practice | ✅ Production (ideal) |

---

### Step 9: Alternative Registries

**Other container registries (2025):**

| Registry | Best For | URL |
|----------|----------|-----|
| Docker Hub | Public images | hub.docker.com |
| GitHub Container Registry | GitHub projects | ghcr.io |
| AWS ECR | AWS deployments | AWS |
| Google GCR | Google Cloud | gcr.io |
| Azure ACR | Azure deployments | azurecr.io |
| Harbor | Self-hosted | goharbor.io |

**Pull from alternative registry:**
```bash
# GitHub Container Registry
docker pull ghcr.io/actions/runner:latest

# Google Container Registry (distroless)
docker pull gcr.io/distroless/nodejs20-debian12
```

---

## Part 5: Docker Licensing (2025 Update)

### Step 10: Understanding Docker Licensing

**Docker Desktop licensing (as of 2025):**

**FREE for:**
- ✅ Personal use
- ✅ Small businesses (<250 employees AND <$10M revenue)
- ✅ Education and non-commercial open source

**REQUIRES subscription for:**
- Organizations with 250+ employees
- OR $10M+ annual revenue

**Docker Engine (Linux) is always free:**
- Open source
- No license restrictions
- Used in production servers

**Check your license:**
```bash
docker info | grep -i "license\|subscription"
```

---

## Part 6: Best Practices from Day One

### Step 11: Essential Commands to Know (2025)

**Information & Inspection:**
```bash
# System info
docker info
docker version
docker system df              # Disk usage

# Images
docker images
docker image ls
docker image inspect <image>  # Detailed info
docker scout cves <image>     # Security scan (NEW)

# Containers
docker ps                     # Running containers
docker ps -a                  # All containers
docker inspect <container>    # Detailed info
docker logs <container>       # View logs
docker stats                  # Resource usage

# Cleanup
docker system prune           # Remove unused data
docker image prune            # Remove unused images
docker container prune        # Remove stopped containers
```

**Modern command structure (2025):**
```bash
# Old style (still works)
docker ps
docker images
docker rm

# New style (recommended - more consistent)
docker container ls
docker image ls
docker container rm

# Both work, but new style is clearer!
```

---

### Step 12: Docker Desktop Features Tour

**Explore Docker Desktop GUI:**

1. **Dashboard**
   - View running containers
   - See resource usage
   - Quick container actions

2. **Images**
   - Manage local images
   - Pull new images
   - View image details

3. **Volumes**
   - Manage persistent data
   - See volume usage

4. **Settings**
   - Resources (CPU, Memory)
   - Docker Engine configuration
   - Extensions marketplace

5. **Extensions (2025 Feature)**
   - Add functionality to Docker Desktop
   - Popular: Disk usage analyzers, security scanners

---

## Expected Outcomes

After completing this exercise, you should:

✅ Understand Docker's 2025 feature set
✅ Know about Docker Desktop AI capabilities
✅ Be familiar with Docker Scout for security
✅ Understand BuildKit and its benefits
✅ Use Docker Compose v2 syntax correctly
✅ Understand Docker licensing (2025)
✅ Know container ecosystem standards (OCI)
✅ Be aware of modern registries beyond Docker Hub

---

## Key Takeaways (2025 Edition)

### What's New in Docker (2025):
1. **Docker Desktop AI** - Natural language Docker assistance
2. **Docker Scout** - Built-in vulnerability scanning
3. **BuildKit** - Default build engine (faster, more secure)
4. **Compose v2** - Integrated, no separate install needed
5. **Enhanced performance** - Faster builds and container startup

### What Changed:
- ❌ `docker-compose` (hyphen) → ✅ `docker compose` (space)
- ❌ `version:` field in compose → ✅ Not needed anymore
- ❌ Manual BuildKit enabling → ✅ Enabled by default
- ❌ Separate Scout install → ✅ Built into Docker Desktop

### Best Practices from Day 1:
1. Always use specific image tags (not `latest`)
2. Scan images with Docker Scout before deploying
3. Use modern `docker compose` command (v2)
4. Enable BuildKit features in your Dockerfiles
5. Keep Docker Desktop updated for latest security patches

---

## Challenge Exercise

**Explore and document:**

1. What version of Docker are you running?
2. Is BuildKit enabled?
3. What's the Docker Scout version?
4. Scan the `hello-world` image - how many CVEs?
5. Try pulling an image from `ghcr.io` or `gcr.io`
6. Compare image sizes: `node:20` vs `node:20-alpine` vs `gcr.io/distroless/nodejs20`

**Document your findings and share with classmates!**

---

## Additional Resources

- [Docker Desktop Release Notes](https://docs.docker.com/desktop/release-notes/)
- [Docker Scout Documentation](https://docs.docker.com/scout/)
- [BuildKit Documentation](https://docs.docker.com/build/buildkit/)
- [Docker Compose v2](https://docs.docker.com/compose/compose-v2/)
- [OCI Standards](https://opencontainers.org/)

---

## Summary

Docker in 2025 is more than just containers:
- 🤖 AI-powered assistance
- 🔒 Built-in security scanning
- ⚡ Faster builds with BuildKit
- 🚀 Modern, integrated tooling

**Welcome to the modern container ecosystem!**

---

**Next:** Session 2 - Working with Docker Images and Containers
