# Exercise 8: BuildKit Cache Optimization for Faster Builds (2025)

**Filename:** `Session4_Exercise8.md`

## Objective
- Understand Docker BuildKit and its advantages
- Implement cache mounts for package managers
- Use build-time secrets securely
- Optimize build times by 50-80%
- Apply advanced BuildKit features

---

## What is BuildKit?

**BuildKit** is Docker's modern build engine (default since Docker 23.0) that provides:
- **Parallel build stages** - Multiple stages build simultaneously
- **Cache mounts** - Persistent caches across builds
- **Secret mounts** - Secure build-time secrets
- **SSH forwarding** - Access private repositories
- **Improved caching** - Smarter layer invalidation
- **Better build output** - Clearer progress information

**Enable BuildKit:**
```bash
# Modern Docker (23.0+) - BuildKit is default
docker build .

# Older Docker - enable explicitly
export DOCKER_BUILDKIT=1
docker build .

# Or per-command
DOCKER_BUILDKIT=1 docker build .
```

---

## Part 1: The Problem - Slow Package Installation

### Step 1: Traditional Slow Dockerfile

1. **Create a Node.js project:**
   ```bash
   mkdir buildkit-demo
   cd buildkit-demo
   ```

2. **Create `package.json` with many dependencies:**
   ```json
   {
     "name": "buildkit-demo",
     "version": "1.0.0",
     "dependencies": {
       "express": "^4.18.2",
       "axios": "^1.5.0",
       "lodash": "^4.17.21",
       "moment": "^2.29.4",
       "bcrypt": "^5.1.1",
       "jsonwebtoken": "^9.0.2",
       "mongoose": "^7.5.0",
       "winston": "^3.10.0",
       "dotenv": "^16.3.1",
       "cors": "^2.8.5"
     }
   }
   ```

3. **Create `app.js`:**
   ```javascript
   const express = require('express');
   const app = express();

   app.get('/', (req, res) => {
     res.send('BuildKit Cache Demo');
   });

   app.listen(3000, () => console.log('Server running'));
   ```

4. **Create `Dockerfile.slow` (traditional approach):**
   ```dockerfile
   FROM node:20-alpine

   WORKDIR /app

   COPY package*.json ./

   # Every build re-downloads all packages from npm registry
   RUN npm install

   COPY . .

   CMD ["node", "app.js"]
   ```

5. **Build twice and observe time:**
   ```bash
   # First build
   time docker build -t app:slow -f Dockerfile.slow .

   # Make small change to app.js
   echo "// comment" >> app.js

   # Second build - still slow because npm cache is lost!
   time docker build -t app:slow -f Dockerfile.slow .
   ```

**Problem:** Each build re-downloads packages even though `package.json` hasn't changed, because npm's cache isn't persisted between builds.

---

## Part 2: Solution - BuildKit Cache Mounts

### Step 2: Optimized Dockerfile with Cache Mounts

1. **Create `Dockerfile.cached`:**
   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM node:20-alpine

   WORKDIR /app

   COPY package*.json ./

   # Cache mount persists npm cache between builds
   RUN --mount=type=cache,target=/root/.npm \
       npm ci --only=production

   COPY . .

   CMD ["node", "app.js"]
   ```

   **Key line explained:**
   ```dockerfile
   RUN --mount=type=cache,target=/root/.npm
   ```
   - `--mount=type=cache` - Creates a persistent cache
   - `target=/root/.npm` - npm's cache directory
   - Cache persists across builds
   - Shared between all builds using this cache mount

2. **Build twice and compare:**
   ```bash
   # First build - downloads packages
   time docker build -t app:cached -f Dockerfile.cached .

   # Make small change
   echo "// another comment" >> app.js

   # Second build - uses cached packages (much faster!)
   time docker build -t app:cached -f Dockerfile.cached .
   ```

**Result:** Second build should be 50-80% faster!

---

## Part 3: Cache Mounts for Different Package Managers

### Step 3: Python with pip

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Cache pip downloads
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### Step 4: Go with modules

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.21-alpine

WORKDIR /app

COPY go.mod go.sum ./

# Cache Go modules
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .

RUN --mount=type=cache,target=/go/pkg/mod \
    go build -o server .

CMD ["./server"]
```

### Step 5: Maven (Java)

```dockerfile
# syntax=docker/dockerfile:1
FROM maven:3.9-eclipse-temurin-17

WORKDIR /app

COPY pom.xml .

# Cache Maven dependencies
RUN --mount=type=cache,target=/root/.m2 \
    mvn dependency:go-offline

COPY src ./src

RUN --mount=type=cache,target=/root/.m2 \
    mvn package

CMD ["java", "-jar", "target/app.jar"]
```

---

## Part 4: Advanced BuildKit Features

### Step 6: Build-Time Secrets (Secure!)

**Problem:** Don't put secrets in Dockerfile layers!

❌ **NEVER do this:**
```dockerfile
# BAD - Secret ends up in image layer!
RUN echo "machine github.com login token password ${GITHUB_TOKEN}" > ~/.netrc && \
    npm install && \
    rm ~/.netrc
```

✅ **DO this instead:**
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

# Secret is only available during build, not in final image
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    --mount=type=cache,target=/root/.npm \
    npm ci

COPY . .

CMD ["node", "app.js"]
```

**Build with secret:**
```bash
# Create secret file (don't commit this!)
echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc

# Build with secret
docker build \
  --secret id=npmrc,src=.npmrc \
  -t app:secure \
  -f Dockerfile.secure .

# Secret is NOT in final image!
```

---

### Step 7: SSH Mount for Private Repositories

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.21-alpine

# Install git and openssh
RUN apk add --no-cache git openssh-client

WORKDIR /app

COPY go.mod go.sum ./

# Mount SSH key to access private repos
RUN --mount=type=ssh \
    --mount=type=cache,target=/go/pkg/mod \
    git config --global url."git@github.com:".insteadOf "https://github.com/" && \
    go mod download

COPY . .

RUN go build -o server .

CMD ["./server"]
```

**Build with SSH:**
```bash
# Ensure ssh-agent is running with your key
eval $(ssh-agent)
ssh-add ~/.ssh/id_rsa

# Build with SSH forwarding
docker build \
  --ssh default \
  -t app:ssh \
  -f Dockerfile.ssh .
```

---

## Part 5: Measuring Build Performance

### Step 8: Create Build Benchmark

1. **Create `benchmark.sh`:**
   ```bash
   #!/bin/bash

   echo "🧪 BuildKit Cache Benchmark"
   echo "================================"

   # Clean all build cache
   docker builder prune -af

   echo ""
   echo "📊 Test 1: Traditional (no cache mount)"
   echo "----------------------------------------"
   time docker build -t app:slow -f Dockerfile.slow . 2>&1 | tail -1

   echo ""
   echo "🔄 Rebuilding (change app.js)..."
   echo "// rebuild" >> app.js
   time docker build -t app:slow -f Dockerfile.slow . 2>&1 | tail -1

   # Clean cache again
   docker builder prune -af

   echo ""
   echo "📊 Test 2: BuildKit with cache mount"
   echo "----------------------------------------"
   time docker build -t app:cached -f Dockerfile.cached . 2>&1 | tail -1

   echo ""
   echo "🔄 Rebuilding (change app.js)..."
   echo "// rebuild2" >> app.js
   time docker build -t app:cached -f Dockerfile.cached . 2>&1 | tail -1

   echo ""
   echo "✅ Benchmark complete!"
   ```

2. **Run benchmark:**
   ```bash
   chmod +x benchmark.sh
   ./benchmark.sh
   ```

---

## Part 6: Cache Storage Backends

### Step 9: Using External Cache Storage

For CI/CD, you can use remote cache storage:

**Local cache (default):**
```bash
docker build .
```

**Inline cache (embed in image):**
```bash
docker build \
  --cache-to type=inline \
  --tag myimage:latest .
```

**Registry cache:**
```bash
# Push cache to registry
docker build \
  --cache-to type=registry,ref=myregistry.com/myimage:cache \
  --tag myimage:latest .

# Pull cache from registry
docker build \
  --cache-from type=registry,ref=myregistry.com/myimage:cache \
  --tag myimage:latest .
```

**GitHub Actions cache:**
```bash
# In GitHub Actions workflow
docker build \
  --cache-from type=gha \
  --cache-to type=gha,mode=max \
  -t myimage:latest .
```

---

## Part 7: Complete Optimized Dockerfile

### Step 10: All Best Practices Combined

```dockerfile
# syntax=docker/dockerfile:1

#################################
# Stage 1: Builder
#################################
FROM node:20-alpine AS builder

# Install build dependencies if needed
RUN apk add --no-cache python3 make g++

WORKDIR /app

# Copy package files
COPY package*.json ./

# Cache mount for npm + install dependencies
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Copy source code
COPY . .

#################################
# Stage 2: Production
#################################
FROM gcr.io/distroless/nodejs20-debian12

# Copy app from builder
COPY --from=builder /app /app

WORKDIR /app

# Run as non-root
USER nonroot

# Expose port
EXPOSE 3000

# Start app
CMD ["server.js"]
```

**Features:**
- ✅ Multi-stage build
- ✅ Cache mount for faster builds
- ✅ Distroless for security
- ✅ Non-root user
- ✅ Minimal final image

**Build command:**
```bash
DOCKER_BUILDKIT=1 docker build -t app:optimized .
```

---

## Expected Outcomes

After completing this exercise, you should be able to:
- ✅ Enable and use BuildKit for faster builds
- ✅ Implement cache mounts for package managers (npm, pip, maven, go)
- ✅ Reduce build times by 50-80% on subsequent builds
- ✅ Use build-time secrets securely
- ✅ Forward SSH keys for private repositories
- ✅ Configure cache backends for CI/CD
- ✅ Combine all optimization techniques

---

## Performance Comparison Table

| Build Type | First Build | Second Build | Cache Hit | Improvement |
|------------|-------------|--------------|-----------|-------------|
| Traditional | 120s | 115s | ❌ | 0% |
| with `npm ci` | 110s | 105s | 🟡 Layer cache | ~10% |
| **BuildKit cache mount** | **110s** | **25s** | **✅ Full cache** | **~80%** |

---

## Common Cache Mount Targets

| Tool | Cache Target | Example |
|------|--------------|---------|
| npm | `/root/.npm` | `RUN --mount=type=cache,target=/root/.npm npm ci` |
| pip | `/root/.cache/pip` | `RUN --mount=type=cache,target=/root/.cache/pip pip install` |
| Go modules | `/go/pkg/mod` | `RUN --mount=type=cache,target=/go/pkg/mod go mod download` |
| Maven | `/root/.m2` | `RUN --mount=type=cache,target=/root/.m2 mvn package` |
| Gradle | `/root/.gradle` | `RUN --mount=type=cache,target=/root/.gradle gradle build` |
| apt | `/var/cache/apt` | `RUN --mount=type=cache,target=/var/cache/apt apt-get install` |
| apk | `/var/cache/apk` | `RUN --mount=type=cache,target=/var/cache/apk apk add` |

---

## Troubleshooting

### Cache not being used?
- Ensure BuildKit is enabled: `export DOCKER_BUILDKIT=1`
- Add `# syntax=docker/dockerfile:1` at top of Dockerfile
- Check cache directory path is correct

### Permission errors?
- Cache mounts default to root user
- Match user in RUN command if using non-root

### CI/CD not benefiting?
- Use external cache backend (`type=registry` or `type=gha`)
- Ensure cache is being pushed and pulled

---

## Additional Resources

- [BuildKit Documentation](https://docs.docker.com/build/buildkit/)
- [Cache Mount Reference](https://docs.docker.com/build/cache/optimize/)
- [Secret Mounts](https://docs.docker.com/build/building/secrets/)
- [SSH Mounts](https://docs.docker.com/build/building/secrets/#ssh-mounts)

---

## Key Takeaway

> **BuildKit cache mounts = Game-changer for build performance**

By persisting package manager caches between builds, you can reduce build times from minutes to seconds, saving developer time and CI/CD costs.

**Best Practice:** Always use cache mounts for package installation in production Dockerfiles!

---

## Challenge

**Goal:** Optimize a real-world application build

1. Take an existing project with many dependencies
2. Add BuildKit cache mounts
3. Measure before/after build times
4. Document improvements

**Target:** Achieve 70%+ build time reduction on second build
