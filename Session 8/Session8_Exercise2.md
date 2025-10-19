# Exercise 2: Dockerfile Security Best Practices (2025)

**Session 8: Security & Best Practices**
**Filename:** `Session8_Exercise2.md`

## Objective
- Master secure Dockerfile writing techniques
- Understand security implications of each instruction
- Avoid common security pitfalls
- Build hardened container images

---

## Overview

A Dockerfile is your application's security foundation. **Every instruction has security implications.** This exercise teaches you to write Dockerfiles that are secure by design.

---

## Part 1: Understanding Security-Critical Instructions

### The Security Impact Matrix

| Instruction | Security Risk | Mitigation |
|-------------|---------------|------------|
| `FROM` | Vulnerable base images | Use specific tags, scan images |
| `RUN` | Malicious commands, secrets exposure | Minimize commands, use secrets mounts |
| `COPY/ADD` | Sensitive files copied | Use .dockerignore |
| `USER` | Running as root | Always set non-root user |
| `EXPOSE` | Unnecessary ports exposed | Only expose required ports |
| `ENV` | Secrets in environment | Use build args or runtime secrets |
| `WORKDIR` | Permission issues | Set appropriate ownership |
| `HEALTHCHECK` | No health monitoring | Always include healthchecks |

---

## Part 2: Secure Base Image Selection

### Step 1: Base Image Security Hierarchy

**From MOST secure to LEAST secure:**

```
1. scratch (for static binaries)          - ~0 KB, 0 CVEs
2. distroless (Google)                    - ~2-50MB, minimal CVEs
3. Alpine Linux                           - ~5-50MB, few CVEs
4. Slim variants (debian-slim, etc.)      - ~50-150MB, moderate CVEs
5. Standard images                        - ~100-1000MB, many CVEs
```

**Example: Node.js Base Image Selection**

❌ **INSECURE:**
```dockerfile
FROM node
```
**Issues:** Latest tag, large image (~1GB), many packages

🟡 **BETTER:**
```dockerfile
FROM node:20-slim
```
**Better:** Specific version, smaller (~200MB)

✅ **GOOD:**
```dockerfile
FROM node:20-alpine
```
**Good:** Minimal packages (~150MB), fewer CVEs

🏆 **BEST:**
```dockerfile
FROM gcr.io/distroless/nodejs20-debian12
```
**Best:** Absolute minimum (~100MB), fewest CVEs

---

### Step 2: Verify Base Image Provenance

**Always verify official images:**

```bash
# Check image provenance
docker pull node:20-alpine
docker inspect node:20-alpine

# Verify publisher
# Look for: "io.buildah.version" or official Docker labels

# Scan before using
docker scout cves node:20-alpine
```

**Secure base image checklist:**
- [ ] From official repository (Docker Hub verified)
- [ ] Specific version tag (not `latest`)
- [ ] Scanned for vulnerabilities
- [ ] Minimal size for requirements
- [ ] Actively maintained

---

## Part 3: The USER Instruction (Critical!)

### Step 3: Never Run as Root

**❌ DANGER: Running as Root**

```dockerfile
FROM node:20-alpine

WORKDIR /app
COPY . .
RUN npm install

# ❌ Running as root (default)
CMD ["npm", "start"]
```

**Problems:**
- Container processes have root privileges
- Attackers gain root if they compromise container
- Can modify host system if misconfigured
- Violates principle of least privilege

**✅ SECURE: Non-Root User**

```dockerfile
FROM node:20-alpine

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copy files with correct ownership
COPY --chown=appuser:appgroup package*.json ./
RUN npm ci --only=production

COPY --chown=appuser:appgroup . ./

# Switch to non-root user
USER appuser

# Now running as appuser, not root
CMD ["node", "server.js"]
```

**Verification:**
```bash
docker run -d --name test-app myapp:latest
docker exec test-app whoami
# Should output: appuser (not root)
```

---

### Step 4: User ID Best Practices

**Different approaches for different base images:**

**Alpine Linux:**
```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

**Debian/Ubuntu:**
```dockerfile
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser
```

**Specific UID/GID (for volume permissions):**
```dockerfile
RUN groupadd -r appgroup -g 1000 && \
    useradd -r -u 1000 -g appgroup appuser
USER appuser
```

**Distroless (built-in nonroot user):**
```dockerfile
FROM gcr.io/distroless/nodejs20-debian12
USER nonroot  # UID 65532
```

---

## Part 4: Handling Secrets Securely

### Step 5: NEVER Put Secrets in Layers

**❌ INSECURE APPROACHES:**

```dockerfile
# ❌ DON'T: Hardcoded secrets
ENV API_KEY="secret123"

# ❌ DON'T: Secrets in RUN commands
RUN echo "machine api.github.com login token password ghp_xxxx" > ~/.netrc && \
    npm install && \
    rm ~/.netrc  # ❌ Still in layer history!

# ❌ DON'T: ARG for secrets (visible in docker history)
ARG SECRET_TOKEN
RUN curl -H "Authorization: Bearer $SECRET_TOKEN" https://api.example.com
```

**Why these are bad:**
- Secrets remain in image layers even if deleted
- Visible in `docker history`
- Can be extracted from image
- Compromises security

**✅ SECURE APPROACHES:**

**Option 1: Build-Time Secrets (BuildKit)**

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

# ✅ Secret only available during build, NOT in image
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci --only=production

COPY . .

USER appuser
CMD ["node", "server.js"]
```

**Build command:**
```bash
docker build --secret id=npmrc,src=.npmrc -t myapp:secure .
```

**Option 2: Runtime Secrets (Docker Compose)**

```yaml
services:
  app:
    image: myapp:latest
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

**In application:**
```javascript
const fs = require('fs');
const dbPassword = fs.readFileSync('/run/secrets/db_password', 'utf8').trim();
```

---

## Part 5: Secure COPY and ADD

### Step 6: Use COPY, Not ADD (Usually)

**COPY vs ADD Security:**

```dockerfile
# ✅ SECURE: Use COPY for normal files
COPY app.js /app/

# ⚠️  CAREFUL: ADD has extra features (security risk)
ADD https://example.com/file.tar.gz /app/  # Downloads from internet!
ADD archive.tar.gz /app/                    # Auto-extracts archives
```

**Why COPY is safer:**
- Explicit behavior only
- No automatic extraction
- No URL downloading
- Easier to audit

**When to use ADD:**
- Only when you need auto-extraction
- Document why you're using it
- Verify source integrity

---

### Step 7: The .dockerignore File (Critical!)

**Create `.dockerignore`:**

```
# Version control
.git
.gitignore
.gitattributes

# Dependencies
node_modules
bower_components

# Build output
dist
build
*.log

# Environment files
.env
.env.local
.env.*.local

# IDE files
.vscode
.idea
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db

# Documentation
*.md
README*
LICENSE

# Docker files
Dockerfile*
docker-compose*
.dockerignore

# Secrets and sensitive files
*.key
*.pem
*.p12
secrets/
credentials/

# Test files
test/
tests/
*.test.js
*.spec.js
coverage/

# CI/CD files
.github/
.gitlab-ci.yml
.travis.yml
```

**Why .dockerignore is critical:**
- ✅ Prevents secrets from being copied
- ✅ Reduces image size
- ✅ Faster build context transfer
- ✅ Avoids unnecessary file exposure

**Test it:**
```bash
# Build and check what was copied
docker build -t test-ignore .
docker run --rm test-ignore ls -la /app
# Should NOT see .env, .git, node_modules, etc.
```

---

## Part 6: Minimize Attack Surface

### Step 8: Install Only What You Need

**❌ BAD: Installing everything**

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    nano \
    git \
    build-essential \
    python3 \
    python3-pip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*
```

**Problems:**
- Huge attack surface
- Many unnecessary packages
- More CVEs to track
- Larger image size

**✅ GOOD: Minimal installation**

```dockerfile
FROM node:20-alpine

# Only install what's absolutely necessary
RUN apk add --no-cache \
    dumb-init

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

COPY . .

USER appuser
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]
```

**✅ BEST: Multi-stage with distroless**

```dockerfile
# Build stage - has build tools
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Runtime stage - minimal
FROM gcr.io/distroless/nodejs20-debian12
COPY --from=builder /app /app
WORKDIR /app
USER nonroot
CMD ["server.js"]
```

---

### Step 9: Clean Up in Same Layer

**❌ INEFFICIENT: Cleanup in separate layers**

```dockerfile
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2
RUN rm -rf /var/lib/apt/lists/*  # ❌ Too late, already in previous layers!
```

**✅ EFFICIENT: Single RUN with cleanup**

```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        package1 \
        package2 && \
    rm -rf /var/lib/apt/lists/*  # ✅ Cleaned in same layer
```

---

## Part 7: Security Headers and Metadata

### Step 10: Add Security Labels

**Add metadata for security tracking:**

```dockerfile
FROM node:20-alpine

LABEL org.opencontainers.image.title="My Secure App"
LABEL org.opencontainers.image.description="Production-ready secure application"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="Your Company"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/yourorg/yourapp"
LABEL security.scan.date="2025-10-19"
LABEL security.base.image="node:20-alpine"
LABEL security.non-root="true"

# ... rest of Dockerfile
```

**Benefits:**
- Track image provenance
- Document security measures
- Enable automated policy enforcement
- Facilitate security audits

---

## Part 8: Complete Secure Dockerfile Template

### Step 11: Production-Ready Secure Dockerfile

**For Node.js Application:**

```dockerfile
# syntax=docker/dockerfile:1

###############################
# Stage 1: Build
###############################
FROM node:20-alpine AS builder

# Install build dependencies if needed
RUN apk add --no-cache python3 make g++

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with cache mount
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Copy source code
COPY . .

###############################
# Stage 2: Production
###############################
FROM gcr.io/distroless/nodejs20-debian12

# Metadata
LABEL org.opencontainers.image.title="Secure Node App"
LABEL org.opencontainers.image.version="1.0.0"
LABEL security.non-root="true"
LABEL security.distroless="true"

# Copy from builder
COPY --from=builder --chown=nonroot:nonroot /app /app

WORKDIR /app

# Run as non-root (distroless includes nonroot user)
USER nonroot

# Expose only necessary port
EXPOSE 3000

# Start application
CMD ["server.js"]
```

**Security Features:**
- ✅ Multi-stage build
- ✅ Distroless base (minimal CVEs)
- ✅ Non-root user
- ✅ BuildKit cache optimization
- ✅ Proper metadata
- ✅ Minimal attack surface

---

## Part 9: Security Scanning Integration

### Step 12: Automated Security Checks

**Create `Dockerfile.security-check`:**

```dockerfile
# This Dockerfile includes security validation

FROM node:20-alpine AS security-scan

# Install security tools
RUN apk add --no-cache curl

WORKDIR /scan

# Copy Dockerfile for analysis
COPY Dockerfile .

# Validate Dockerfile with hadolint
RUN curl -sL -o /usr/local/bin/hadolint \
    https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64 && \
    chmod +x /usr/local/bin/hadolint

RUN hadolint Dockerfile || true
```

**Run hadolint locally:**

```bash
# Install hadolint
docker run --rm -i hadolint/hadolint < Dockerfile

# Or with make
echo 'lint:' > Makefile
echo '	docker run --rm -i hadolint/hadolint < Dockerfile' >> Makefile

make lint
```

---

## Part 10: Security Best Practices Checklist

### Final Security Review

Before deploying any Dockerfile, verify:

```markdown
## Dockerfile Security Checklist

### Base Image
- [ ] Using official or verified base image
- [ ] Specific version tag (not latest)
- [ ] Minimal base image (Alpine/Distroless preferred)
- [ ] Base image scanned for CVEs
- [ ] FROM instruction at top of file

### User & Permissions
- [ ] Running as non-root user (USER instruction)
- [ ] User created explicitly (not using default users)
- [ ] Files owned by correct user (--chown in COPY)
- [ ] No SUID/SGID binaries (if applicable)

### Secrets & Sensitive Data
- [ ] No hardcoded secrets in ENV or RUN
- [ ] Using BuildKit secret mounts for build secrets
- [ ] Runtime secrets via environment or files
- [ ] .dockerignore prevents secret files being copied

### Minimize Attack Surface
- [ ] Only necessary packages installed
- [ ] Package cache cleaned in same RUN layer
- [ ] Using multi-stage builds to separate build/runtime
- [ ] Unnecessary files excluded via .dockerignore

### Instructions
- [ ] COPY preferred over ADD (unless extraction needed)
- [ ] HEALTHCHECK defined (or in compose)
- [ ] Only necessary ports EXPOSEd
- [ ] WORKDIR set appropriately
- [ ] Single application per container

### Optimization
- [ ] Layers ordered from least to most frequently changing
- [ ] BuildKit cache mounts for package managers
- [ ] Image size minimized
- [ ] Build cache utilized effectively

### Documentation
- [ ] LABELs for metadata and tracking
- [ ] Comments explain non-obvious decisions
- [ ] README documents build and security considerations

### Validation
- [ ] Dockerfile linted with hadolint
- [ ] Image scanned with Docker Scout
- [ ] No Critical or High CVEs in production images
- [ ] Tested in staging environment
```

---

## Expected Outcomes

After completing this exercise, you should:

✅ Write production-grade secure Dockerfiles
✅ Understand security implications of each instruction
✅ Avoid common security pitfalls
✅ Implement defense-in-depth strategies
✅ Create minimal, hardened container images

---

## Common Security Anti-Patterns to Avoid

### ❌ Don't Do This:

```dockerfile
# Multiple security issues!
FROM node

WORKDIR /app

# Running as root (no USER instruction)
# Copying everything (no .dockerignore)
COPY . .

# Secrets in environment
ENV API_KEY=secret123
ENV DB_PASSWORD=password

# Installing unnecessary tools
RUN apt-get update && apt-get install -y \
    curl wget vim nano git

# npm install instead of npm ci
RUN npm install

# Exposing unnecessary ports
EXPOSE 22 3000 8080 9000

# Still running as root
CMD ["npm", "start"]
```

**Problems:** 10+ security issues!

### ✅ Do This Instead:

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

COPY . .

FROM gcr.io/distroless/nodejs20-debian12
COPY --from=builder /app /app
WORKDIR /app
USER nonroot
EXPOSE 3000
CMD ["server.js"]
```

**Result:** Secure, minimal, production-ready!

---

## Challenge Exercise

**Create the most secure Dockerfile possible:**

**Requirements:**
1. Distroless base image
2. Non-root user
3. Zero unnecessary packages
4. Proper .dockerignore
5. Security labels
6. Passes hadolint
7. Passes Docker Scout with 0 Critical/High CVEs

**Bonus:**
- Multi-stage build
- BuildKit cache mounts
- Size under 100MB

---

## Additional Resources

- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Hadolint - Dockerfile Linter](https://github.com/hadolint/hadolint)
- [Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Distroless Images](https://github.com/GoogleContainerTools/distroless)

---

**Next:** Exercise 3 - Runtime Security and Container Hardening
