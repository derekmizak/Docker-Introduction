# Exercise 7: Implementing Distroless Images for Maximum Security (2025)

**Filename:** `Session4_Exercise7.md`

## Objective
- Understand what distroless images are and why they matter
- Convert a traditional Docker image to distroless
- Compare security and size benefits
- Learn when to use distroless vs. alpine vs. standard images

---

## What Are Distroless Images?

**Distroless images** contain **only your application and its runtime dependencies**—nothing else:
- ❌ No package managers (apt, yum, apk)
- ❌ No shells (bash, sh)
- ❌ No system utilities
- ✅ Only runtime (Node.js, Python, Java, etc.)
- ✅ Your application code
- ✅ Required libraries

**Benefits:**
- **Smallest attack surface** - Fewer components = fewer vulnerabilities
- **Minimal size** - Often 50-80% smaller than alpine
- **Better security** - Can't exec into container (no shell)
- **Compliance** - Easier to pass security audits

**Trade-offs:**
- **Debugging is harder** - Can't `docker exec -it container sh`
- **Not for all apps** - Some apps need system tools
- **More complex builds** - Requires multi-stage builds

---

## Part 1: Understanding the Distroless Ecosystem

### Available Distroless Base Images (Google Container Tools)

| Image | Best For | Size |
|-------|----------|------|
| `gcr.io/distroless/static-debian12` | Static binaries (Go, Rust) | ~2MB |
| `gcr.io/distroless/base-debian12` | C/C++ applications | ~20MB |
| `gcr.io/distroless/cc-debian12` | Apps needing glibc | ~20MB |
| `gcr.io/distroless/python3-debian12` | Python applications | ~50MB |
| `gcr.io/distroless/nodejs20-debian12` | Node.js applications | ~100MB |
| `gcr.io/distroless/java17-debian12` | Java applications | ~180MB |

All images come in two variants:
- **Regular:** e.g., `gcr.io/distroless/nodejs20-debian12`
- **Debug:** e.g., `gcr.io/distroless/nodejs20-debian12:debug` (includes busybox shell for debugging)

---

## Part 2: Node.js Application - Traditional vs. Distroless

### Step 1: Create a Sample Application

1. **Set up project:**
   ```bash
   mkdir distroless-demo
   cd distroless-demo
   ```

2. **Create `package.json`:**
   ```json
   {
     "name": "distroless-demo",
     "version": "1.0.0",
     "main": "server.js",
     "dependencies": {
       "express": "^4.18.2"
     },
     "scripts": {
       "start": "node server.js"
     }
   }
   ```

3. **Create `server.js`:**
   ```javascript
   const express = require('express');
   const app = express();
   const PORT = 3000;

   app.get('/', (req, res) => {
     res.json({
       message: 'Running in Distroless!',
       node: process.version,
       platform: process.platform
     });
   });

   app.get('/health', (req, res) => {
     res.json({ status: 'healthy' });
   });

   app.listen(PORT, () => {
     console.log(`Server running on port ${PORT}`);
   });
   ```

---

### Step 2: Traditional Dockerfile (Alpine Base)

1. **Create `Dockerfile.alpine`:**
   ```dockerfile
   FROM node:20-alpine

   WORKDIR /app

   COPY package*.json ./
   RUN npm ci --only=production

   COPY . .

   EXPOSE 3000
   CMD ["node", "server.js"]
   ```

2. **Build and test:**
   ```bash
   docker build -t myapp:alpine -f Dockerfile.alpine .
   docker run -d -p 3000:3000 --name app-alpine myapp:alpine
   curl http://localhost:3000
   docker stop app-alpine && docker rm app-alpine
   ```

---

### Step 3: Distroless Dockerfile

1. **Create `Dockerfile.distroless`:**
   ```dockerfile
   # Build stage - Use full Node.js image to install dependencies
   FROM node:20-alpine AS builder

   WORKDIR /app

   # Copy package files
   COPY package*.json ./

   # Install dependencies (including devDependencies for build)
   RUN npm ci --only=production

   # Copy application source
   COPY . .

   # Runtime stage - Use distroless image
   FROM gcr.io/distroless/nodejs20-debian12

   # Copy node_modules and application from builder
   COPY --from=builder /app /app

   # Set working directory
   WORKDIR /app

   # Expose port
   EXPOSE 3000

   # Run as non-root user (distroless runs as nonroot by default)
   USER nonroot

   # Start application
   CMD ["server.js"]
   ```

2. **Build and test:**
   ```bash
   docker build -t myapp:distroless -f Dockerfile.distroless .
   docker run -d -p 3001:3000 --name app-distroless myapp:distroless
   curl http://localhost:3001
   ```

---

### Step 4: Compare Images

1. **Check image sizes:**
   ```bash
   docker images | grep myapp
   ```

   **Expected Results:**
   ```
   myapp:alpine       150-180 MB
   myapp:distroless   100-120 MB  (30-40% smaller!)
   ```

2. **Scan for vulnerabilities:**
   ```bash
   docker scout cves myapp:alpine
   docker scout cves myapp:distroless
   ```

   **Expected:** Distroless will have significantly fewer CVEs (often 50-70% reduction)

3. **Try to exec into containers:**
   ```bash
   # This works (Alpine has shell)
   docker exec -it app-distroless sh
   # Output: OCI runtime exec failed: exec failed: unable to start container process:
   #         exec: "sh": executable file not found in $PATH

   # Distroless has NO SHELL - this is a security feature!
   ```

---

## Part 3: Debugging Distroless Containers

### Step 5: Using Debug Variant

When you need to debug, use the `:debug` tag:

1. **Create `Dockerfile.distroless-debug`:**
   ```dockerfile
   FROM node:20-alpine AS builder
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci --only=production
   COPY . .

   # Use debug variant (includes busybox shell)
   FROM gcr.io/distroless/nodejs20-debian12:debug

   COPY --from=builder /app /app
   WORKDIR /app
   USER nonroot
   CMD ["server.js"]
   ```

2. **Build and exec into it:**
   ```bash
   docker build -t myapp:distroless-debug -f Dockerfile.distroless-debug .
   docker run -d -p 3002:3000 --name app-debug myapp:distroless-debug

   # Now this works!
   docker exec -it app-debug sh
   ```

⚠️ **Never use debug variants in production!**

---

### Step 6: Alternative Debugging Techniques

Without shell access, use these methods:

1. **Check logs:**
   ```bash
   docker logs app-distroless
   docker logs -f app-distroless  # Follow logs
   ```

2. **Inspect container:**
   ```bash
   docker inspect app-distroless
   ```

3. **Health checks:**
   ```bash
   curl http://localhost:3001/health
   ```

4. **Copy files out for inspection:**
   ```bash
   docker cp app-distroless:/app/package.json ./package.json
   ```

5. **Use ephemeral debug container (Kubernetes):**
   ```bash
   # In Kubernetes
   kubectl debug -it pod-name --image=busybox --target=container-name
   ```

---

## Part 4: Python Distroless Example

### Step 7: Convert Python App to Distroless

1. **Create `app.py`:**
   ```python
   from http.server import HTTPServer, BaseHTTPRequestHandler
   import json

   class SimpleHandler(BaseHTTPRequestHandler):
       def do_GET(self):
           self.send_response(200)
           self.send_header('Content-type', 'application/json')
           self.end_headers()
           response = {'message': 'Python Distroless!', 'path': self.path}
           self.wfile.write(json.dumps(response).encode())

   if __name__ == '__main__':
       server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
       print('Server running on port 8080')
       server.serve_forever()
   ```

2. **Create `Dockerfile.python-distroless`:**
   ```dockerfile
   # Build stage
   FROM python:3.12-slim AS builder

   WORKDIR /app

   # Install dependencies if you have any
   # COPY requirements.txt .
   # RUN pip install --no-cache-dir --user -r requirements.txt

   COPY app.py .

   # Runtime stage
   FROM gcr.io/distroless/python3-debian12

   COPY --from=builder /app /app

   WORKDIR /app

   CMD ["app.py"]
   ```

3. **Build and run:**
   ```bash
   docker build -t pyapp:distroless -f Dockerfile.python-distroless .
   docker run -d -p 8080:8080 --name pyapp pyapp:distroless
   curl http://localhost:8080
   ```

---

## Part 5: When to Use Each Image Type

### Decision Matrix

| Scenario | Recommended Base | Reason |
|----------|------------------|--------|
| **Local development** | Standard (e.g., `node:20`) | Full tooling, easy debugging |
| **CI/CD testing** | Alpine (e.g., `node:20-alpine`) | Small, fast builds, shell access |
| **Production (web services)** | Distroless | Maximum security, minimal attack surface |
| **Production (needs tools)** | Alpine | Good balance of size and functionality |
| **Compliance-heavy environments** | Distroless | Minimal components = easier audits |
| **Static binaries (Go, Rust)** | `distroless/static` | Smallest possible size (~2MB) |
| **Quick prototypes** | Standard | Faster setup, full tooling |

---

## Part 6: Best Practices for Distroless

### ✅ DO:
- Use multi-stage builds (builder + distroless runtime)
- Test thoroughly before deploying distroless to production
- Implement comprehensive logging (you can't shell in to debug!)
- Use health checks to monitor application status
- Keep `:debug` variant ready for emergency debugging
- Document your Dockerfile well
- Use specific tags, not `latest`

### ❌ DON'T:
- Deploy debug variants to production
- Expect to exec into distroless containers
- Use distroless if your app needs shell scripts
- Skip testing on distroless before deployment
- Forget about dependencies (they must be copied from builder)

---

## Expected Outcomes

After completing this exercise, you should be able to:
- ✅ Explain what distroless images are
- ✅ Convert traditional Dockerfiles to use distroless
- ✅ Achieve 30-70% reduction in image size
- ✅ Reduce CVEs by 50-80%
- ✅ Debug distroless containers using alternative methods
- ✅ Choose appropriate base images for different scenarios

---

## Comparison Table (Fill this in during exercise)

| Metric | node:20 | node:20-alpine | Distroless Node.js |
|--------|---------|----------------|-------------------|
| Image Size | ~1100 MB | ~150 MB | ~100 MB |
| Critical CVEs | ? | ? | ? |
| Total CVEs | ? | ? | ? |
| Has shell? | ✅ Yes | ✅ Yes | ❌ No |
| Package manager? | ✅ Yes | ✅ Yes | ❌ No |
| Debug ease | 🟢 Easy | 🟢 Easy | 🟡 Moderate |
| Security | 🔴 Lower | 🟡 Medium | 🟢 Highest |
| Production ready? | ❌ Too large | ✅ Yes | ✅ Best choice |

Fill in the `?` marks using `docker scout cves <image>`.

---

## Challenge: Ultra-Minimal Go Application

**Goal:** Create a Go web server in a distroless image under 10MB.

1. **Create `main.go`:**
   ```go
   package main

   import (
       "fmt"
       "net/http"
   )

   func main() {
       http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
           fmt.Fprintf(w, "Minimal Go + Distroless!")
       })
       http.ListenAndServe(":8080", nil)
   }
   ```

2. **Create Dockerfile:**
   ```dockerfile
   FROM golang:1.21-alpine AS builder
   WORKDIR /app
   COPY main.go .
   RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o server .

   FROM gcr.io/distroless/static-debian12
   COPY --from=builder /app/server /server
   CMD ["/server"]
   ```

3. **Build and verify size:**
   ```bash
   docker build -t goapp:distroless .
   docker images goapp:distroless
   # Should be < 10MB!
   ```

---

## Additional Resources

- [Google Distroless GitHub](https://github.com/GoogleContainerTools/distroless)
- [Distroless Best Practices](https://github.com/GoogleContainerTools/distroless#best-practices)
- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Is Your Container Image Really Distroless?](https://www.docker.com/blog/is-your-container-image-really-distroless/)

---

## Key Takeaway

> **Distroless images = Production-grade security through radical minimalism**

By removing everything except your app and its runtime, you eliminate entire classes of vulnerabilities and create containers that are truly immutable and secure.

---

**Remember:** Distroless is not about making development harder—it's about making production safer. Use appropriate tools for each environment!
