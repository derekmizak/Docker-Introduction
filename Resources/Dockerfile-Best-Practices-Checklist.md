# Dockerfile Best Practices Checklist (2025 Edition)

**Last Updated:** October 2025
**Version:** 1.0

---

## 📋 How to Use This Checklist

Use this checklist when writing or reviewing Dockerfiles to ensure you're following 2025 best practices for security, performance, and maintainability.

**Legend:**
- 🔒 Security-critical
- ⚡ Performance optimization
- 🛡️ Production reliability
- 📝 Maintainability

---

## 🔒 Security Checklist

### Base Image Security

- [ ] **Use specific image tags** (not `latest`)
  ```dockerfile
  # ❌ BAD
  FROM node:latest

  # ✅ GOOD
  FROM node:20.10.0-alpine
  ```

- [ ] **Choose minimal base images**
  - Alpine Linux for small footprint
  - Distroless for production (Google's gcr.io/distroless)
  - Scratch for compiled languages (Go, Rust)

- [ ] **Scan base image for vulnerabilities**
  ```bash
  docker scout cves node:20.10.0-alpine
  ```

- [ ] **Use official or verified images only**
  - Check for "Official Image" or "Verified Publisher" badge on Docker Hub
  - Prefer images from trusted sources (Docker Official, Google, etc.)

### User and Permissions

- [ ] **🔒 Run as non-root user (CRITICAL)**
  ```dockerfile
  # Create user and group
  RUN addgroup -S appgroup && adduser -S appuser -G appgroup

  # Switch to non-root user
  USER appuser
  ```

- [ ] **Set proper file ownership**
  ```dockerfile
  COPY --chown=appuser:appgroup . /app
  ```

- [ ] **Avoid sudo or privilege escalation**
  - Never install sudo in containers
  - Never use SUID/SGID bits

### Secrets and Sensitive Data

- [ ] **🔒 NEVER hardcode secrets in Dockerfile**
  ```dockerfile
  # ❌ NEVER DO THIS
  ENV API_KEY="secret123"
  ENV DB_PASSWORD="password"
  RUN echo "secret" > /app/secret.txt
  ```

- [ ] **Use BuildKit secret mounts for build-time secrets**
  ```dockerfile
  # syntax=docker/dockerfile:1
  RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
      npm ci --only=production
  ```

- [ ] **Use Docker secrets for runtime secrets**
  - Reference in docker-compose.yml
  - Never commit secrets to version control

- [ ] **No secrets in environment variables**
  - Use secret files instead
  - Read from `/run/secrets/` at runtime

### Image Layers and History

- [ ] **No secrets in any layer** (they persist in history!)
  ```dockerfile
  # ❌ BAD - Secret remains in layer history
  RUN echo "secret" > /tmp/secret && \
      use_secret.sh && \
      rm /tmp/secret  # Too late, already in layer!

  # ✅ GOOD - Use secret mount (not persisted)
  RUN --mount=type=secret,id=mysecret \
      use_secret.sh
  ```

- [ ] **Verify no sensitive data in built image**
  ```bash
  docker history myapp:latest
  dive myapp:latest  # Explore layers
  ```

### Security Scanning

- [ ] **Scan image for vulnerabilities before deployment**
  ```bash
  docker scout cves myapp:latest
  docker scout recommendations myapp:latest
  ```

- [ ] **Address Critical and High severity CVEs**
  - Target: 0 Critical, minimize High
  - Update base images regularly

- [ ] **Use .dockerignore to exclude sensitive files**
  ```dockerignore
  .git
  .env
  .env.local
  secrets/
  *.pem
  *.key
  ```

---

## ⚡ Performance Optimization Checklist

### Multi-Stage Builds

- [ ] **Use multi-stage builds for compiled apps**
  ```dockerfile
  # Build stage
  FROM node:20-alpine AS builder
  WORKDIR /app
  COPY package*.json ./
  RUN npm ci
  COPY . .
  RUN npm run build

  # Production stage
  FROM node:20-alpine
  WORKDIR /app
  COPY --from=builder /app/dist ./dist
  COPY --from=builder /app/node_modules ./node_modules
  CMD ["node", "dist/server.js"]
  ```

- [ ] **Only copy necessary files to final stage**
  - Don't copy build tools, dev dependencies, source code

### Layer Caching

- [ ] **Order instructions from least to most frequently changing**
  ```dockerfile
  # ✅ GOOD ORDER
  FROM node:20-alpine
  WORKDIR /app

  # 1. Copy dependency files first (changes rarely)
  COPY package*.json ./
  RUN npm ci --only=production

  # 2. Copy application code last (changes frequently)
  COPY . .

  CMD ["node", "server.js"]
  ```

- [ ] **Combine related RUN commands**
  ```dockerfile
  # ❌ BAD - Multiple layers
  RUN apk add --no-cache git
  RUN apk add --no-cache curl
  RUN apk add --no-cache wget

  # ✅ GOOD - Single layer
  RUN apk add --no-cache \
      git \
      curl \
      wget
  ```

### BuildKit Cache Mounts

- [ ] **Use cache mounts for package managers**
  ```dockerfile
  # syntax=docker/dockerfile:1

  # npm
  RUN --mount=type=cache,target=/root/.npm \
      npm ci --only=production

  # pip
  RUN --mount=type=cache,target=/root/.cache/pip \
      pip install -r requirements.txt

  # apt
  RUN --mount=type=cache,target=/var/cache/apt \
      apt-get update && apt-get install -y package
  ```

- [ ] **Enable BuildKit for builds**
  ```bash
  export DOCKER_BUILDKIT=1
  docker build -t myapp:latest .
  ```

### Image Size Optimization

- [ ] **Target image size goals**
  - Compiled apps (Go, Rust): <20MB
  - Node.js apps: <100MB
  - Python apps: <150MB

- [ ] **Remove package manager cache in same layer**
  ```dockerfile
  # Alpine
  RUN apk add --no-cache package

  # Debian/Ubuntu
  RUN apt-get update && \
      apt-get install -y --no-install-recommends package && \
      rm -rf /var/lib/apt/lists/*
  ```

- [ ] **Use .dockerignore to reduce build context**
  ```dockerignore
  node_modules
  npm-debug.log
  .git
  .gitignore
  README.md
  .vscode
  .idea
  *.md
  ```

- [ ] **Remove unnecessary files in same layer**
  ```dockerfile
  RUN npm ci --only=production && \
      npm cache clean --force && \
      rm -rf /tmp/*
  ```

---

## 🛡️ Production Reliability Checklist

### Health Checks

- [ ] **Add HEALTHCHECK instruction**
  ```dockerfile
  HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD node healthcheck.js
  ```

- [ ] **Avoid using curl/wget for healthchecks**
  ```dockerfile
  # ❌ BAD - Adds unnecessary dependencies
  HEALTHCHECK CMD curl -f http://localhost:3000/health || exit 1

  # ✅ GOOD - Use language-native check
  HEALTHCHECK CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"
  ```

- [ ] **Set appropriate start_period for slow-starting apps**
  - Database: 30-60s
  - Large Java apps: 60-120s
  - Small Node.js apps: 20-30s

### Signal Handling

- [ ] **Use exec form for CMD/ENTRYPOINT** (for proper signal handling)
  ```dockerfile
  # ❌ BAD - Shell form (PID 1 is shell, not your app)
  CMD node server.js

  # ✅ GOOD - Exec form (PID 1 is your app)
  CMD ["node", "server.js"]
  ```

- [ ] **Handle SIGTERM for graceful shutdown**
  - Ensure application handles signals properly
  - Set STOPSIGNAL if needed (default is SIGTERM)

### Resource Documentation

- [ ] **Document expected resource requirements**
  ```dockerfile
  LABEL org.opencontainers.image.documentation="Requires: 512MB RAM, 0.5 CPU"
  ```

- [ ] **Document expected volumes**
  ```dockerfile
  # Document volumes needed
  VOLUME ["/data", "/logs"]

  # Add comments
  # /data - Application data (persistent)
  # /logs - Application logs (can be tmpfs)
  ```

- [ ] **Document exposed ports**
  ```dockerfile
  EXPOSE 3000
  # Port 3000: HTTP API
  ```

### Metadata and Labels

- [ ] **Add OCI standard labels**
  ```dockerfile
  LABEL org.opencontainers.image.title="My Application"
  LABEL org.opencontainers.image.description="Production-ready Node.js API"
  LABEL org.opencontainers.image.version="1.0.0"
  LABEL org.opencontainers.image.authors="your-email@example.com"
  LABEL org.opencontainers.image.source="https://github.com/user/repo"
  LABEL org.opencontainers.image.licenses="MIT"
  ```

---

## 📝 Maintainability Checklist

### Code Quality

- [ ] **Use consistent formatting**
  - Indent with 2 or 4 spaces
  - One instruction per line when practical
  - Group related instructions

- [ ] **Add comments for complex instructions**
  ```dockerfile
  # Install system dependencies required for bcrypt
  RUN apk add --no-cache \
      python3 \
      make \
      g++

  # Build native dependencies
  RUN npm ci --only=production
  ```

- [ ] **Use ARG for build-time customization**
  ```dockerfile
  ARG NODE_VERSION=20
  FROM node:${NODE_VERSION}-alpine

  ARG APP_VERSION=1.0.0
  LABEL version="${APP_VERSION}"
  ```

### Instruction Best Practices

- [ ] **COPY vs ADD: Use COPY unless you need ADD**
  ```dockerfile
  # ✅ GOOD - Use COPY for regular files
  COPY package.json /app/

  # ✅ OK - Use ADD for tar extraction
  ADD app.tar.gz /app/

  # ❌ BAD - Don't use ADD for regular files
  ADD package.json /app/
  ```

- [ ] **Set WORKDIR instead of cd**
  ```dockerfile
  # ❌ BAD
  RUN cd /app && npm install

  # ✅ GOOD
  WORKDIR /app
  RUN npm install
  ```

- [ ] **Use ENV for runtime, ARG for build-time**
  ```dockerfile
  # Build-time variable
  ARG BUILD_ENV=production
  RUN npm run build --env=${BUILD_ENV}

  # Runtime variable
  ENV NODE_ENV=production
  ENV PORT=3000
  ```

### Reproducibility

- [ ] **Pin all versions explicitly**
  ```dockerfile
  # ✅ GOOD
  FROM node:20.10.0-alpine3.18

  # In package.json, use exact versions
  # "express": "4.18.2" not "^4.18.2"
  ```

- [ ] **Use `--no-install-recommends` with apt-get**
  ```dockerfile
  RUN apt-get update && \
      apt-get install -y --no-install-recommends \
        package1 \
        package2 && \
      rm -rf /var/lib/apt/lists/*
  ```

- [ ] **Lock file committed for reproducible builds**
  - package-lock.json (npm)
  - yarn.lock (Yarn)
  - poetry.lock (Python Poetry)
  - go.sum (Go)

---

## 🎯 Complete Example: Production-Ready Dockerfile

Here's a complete example incorporating all best practices:

```dockerfile
# syntax=docker/dockerfile:1

# Build stage
FROM node:20.10.0-alpine3.18 AS builder

# Add build metadata
ARG VERSION=1.0.0
ARG BUILD_DATE
LABEL stage=builder

# Install build dependencies
RUN apk add --no-cache \
    python3 \
    make \
    g++

# Set working directory
WORKDIR /app

# Copy dependency files
COPY package.json package-lock.json ./

# Install dependencies with cache mount
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Copy application code
COPY . .

# Build application (if needed)
# RUN npm run build

# Production stage
FROM gcr.io/distroless/nodejs20-debian12

# Add metadata
LABEL org.opencontainers.image.title="My Application" \
      org.opencontainers.image.description="Production-ready Node.js API" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.authors="team@example.com" \
      org.opencontainers.image.source="https://github.com/user/repo" \
      org.opencontainers.image.licenses="MIT"

# Set environment variables
ENV NODE_ENV=production \
    PORT=3000

# Set working directory
WORKDIR /app

# Copy from builder (as non-root user)
COPY --from=builder --chown=nonroot:nonroot /app /app

# Switch to non-root user (distroless provides nonroot user)
USER nonroot

# Document port
EXPOSE 3000

# Health check (using Node.js, no curl needed)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD ["node", "-e", "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"]

# Run application (exec form for proper signal handling)
CMD ["server.js"]
```

---

## ✅ Pre-Deployment Checklist

Before deploying your Docker image to production:

### Security Verification

- [ ] **Scan image for vulnerabilities**
  ```bash
  docker scout cves myapp:latest
  ```

- [ ] **Verify running as non-root**
  ```bash
  docker run --rm myapp:latest whoami
  # Should NOT be 'root'
  ```

- [ ] **Check for secrets in layers**
  ```bash
  docker history myapp:latest
  dive myapp:latest
  ```

### Performance Verification

- [ ] **Check image size**
  ```bash
  docker images myapp:latest
  # Should be <100MB for Node.js apps
  ```

- [ ] **Test build cache**
  ```bash
  # Rebuild without changes
  docker build -t myapp:latest .
  # Should use cache, be fast
  ```

### Functionality Verification

- [ ] **Test container starts successfully**
  ```bash
  docker run -d --name test myapp:latest
  docker logs test
  ```

- [ ] **Verify healthcheck works**
  ```bash
  docker inspect test | grep -A 10 Health
  # Should show "healthy" after start_period
  ```

- [ ] **Test graceful shutdown**
  ```bash
  docker stop test
  # Should stop within 10 seconds
  ```

### Documentation Verification

- [ ] **README includes:**
  - How to build image
  - Required environment variables
  - Volume mount points
  - Port mappings
  - Resource requirements

- [ ] **.dockerignore exists and is complete**

- [ ] **Image metadata is complete**
  ```bash
  docker inspect myapp:latest
  ```

---

## 🚨 Common Mistakes to Avoid

### Security Mistakes

❌ **Using root user**
```dockerfile
# No USER instruction = runs as root
```

❌ **Hardcoding secrets**
```dockerfile
ENV DB_PASSWORD="secret123"
```

❌ **Using latest tag**
```dockerfile
FROM node:latest
```

❌ **Installing unnecessary packages**
```dockerfile
RUN apt-get install -y curl wget git vim nano
```

### Performance Mistakes

❌ **Not using multi-stage builds**
```dockerfile
# Single stage with build tools in production
FROM node:20
RUN npm install  # Includes devDependencies
```

❌ **Wrong layer order**
```dockerfile
COPY . .  # Application code first
RUN npm install  # Dependencies second
# Every code change invalidates npm install cache!
```

❌ **Not cleaning up in same layer**
```dockerfile
RUN apt-get update
RUN apt-get install -y package
RUN rm -rf /var/lib/apt/lists/*
# Too late, cache already in previous layers!
```

### Reliability Mistakes

❌ **No healthcheck**
```dockerfile
# Container considered healthy even if app crashes
```

❌ **Shell form CMD**
```dockerfile
CMD node server.js
# PID 1 is shell, not app - signals don't work
```

❌ **No graceful shutdown handling**
```javascript
// Application doesn't handle SIGTERM
```

---

## 📚 Additional Resources

### Tools

- **Docker Scout**: Built-in vulnerability scanning
  ```bash
  docker scout quickview <image>
  docker scout cves <image>
  docker scout recommendations <image>
  ```

- **Dive**: Explore image layers
  ```bash
  dive <image>
  ```

- **Hadolint**: Dockerfile linter
  ```bash
  hadolint Dockerfile
  ```

- **Trivy**: Vulnerability scanner
  ```bash
  trivy image <image>
  ```

### Best Practice Guides

- [Official Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Google Distroless Images](https://github.com/GoogleContainerTools/distroless)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

### Standards

- [OCI Image Specification](https://github.com/opencontainers/image-spec)
- [OCI Labels](https://github.com/opencontainers/image-spec/blob/main/annotations.md)

---

## 📝 Quick Reference Card

Print this section for quick reference:

```
DOCKERFILE BEST PRACTICES QUICK CARD

🔒 SECURITY
✅ Specific tags (node:20.10.0-alpine)
✅ Non-root USER
✅ No secrets in layers
✅ Scan with docker scout
✅ Use .dockerignore

⚡ PERFORMANCE
✅ Multi-stage builds
✅ Order: dependencies before code
✅ BuildKit cache mounts
✅ Combine RUN commands
✅ Clean cache in same layer

🛡️ RELIABILITY
✅ HEALTHCHECK instruction
✅ Exec form CMD ["app"]
✅ Pin all versions
✅ Document ports/volumes
✅ Add metadata labels

📝 MAINTAINABILITY
✅ Comments for complex parts
✅ Consistent formatting
✅ COPY not ADD
✅ WORKDIR not cd
✅ ARG for build, ENV for runtime
```

---

**Version:** 1.0 | **Last Updated:** October 2025
**Maintained by:** Docker Course Team

**Print this checklist and keep it handy when writing Dockerfiles!**
