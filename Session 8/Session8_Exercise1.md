# Exercise 1: Complete Image Security Workflow (2025)

**Session 8: Security & Best Practices**
**Filename:** `Session8_Exercise1.md`

## Objective
- Implement a complete security workflow for Docker images
- Scan, analyze, and remediate vulnerabilities
- Build security into the development process
- Achieve production-ready security standards

---

## Overview

This exercise guides you through a **complete security workflow** from development to production, incorporating all security best practices learned in this course.

**Security Workflow:**
```
1. Choose Secure Base → 2. Scan Image → 3. Fix CVEs → 4. Re-scan → 5. Sign & Push → 6. Monitor
```

---

## Part 1: Baseline Assessment

### Step 1: Build an Insecure Image

Let's start with a deliberately insecure setup to understand what NOT to do.

1. **Create project directory:**
   ```bash
   mkdir security-workflow
   cd security-workflow
   ```

2. **Create `package.json`:**
   ```json
   {
     "name": "security-demo",
     "version": "1.0.0",
     "dependencies": {
       "express": "4.17.0",
       "lodash": "4.17.19",
       "axios": "0.21.0"
     },
     "scripts": {
       "start": "node server.js"
     }
   }
   ```

   **Note:** These are intentionally OLD versions with known vulnerabilities!

3. **Create `server.js`:**
   ```javascript
   const express = require('express');
   const axios = require('axios');
   const _ = require('lodash');

   const app = express();
   const PORT = 3000;

   app.get('/', (req, res) => {
     res.json({
       message: 'Insecure Demo',
       version: process.version
     });
   });

   app.get('/health', (req, res) => {
     res.json({ status: 'healthy' });
   });

   app.listen(PORT, () => {
     console.log(`Server running on port ${PORT}`);
   });
   ```

4. **Create `Dockerfile.insecure`:**
   ```dockerfile
   # ❌ Multiple security issues here!
   FROM node:14

   # ❌ Running as root
   WORKDIR /app

   # ❌ Copying everything (no .dockerignore)
   COPY . .

   # ❌ Using npm install instead of npm ci
   RUN npm install

   # ❌ No healthcheck
   EXPOSE 3000

   # ❌ Still running as root
   CMD ["npm", "start"]
   ```

5. **Build and scan:**
   ```bash
   docker build -t myapp:insecure -f Dockerfile.insecure .
   docker scout cves myapp:insecure
   ```

**❌ Expected Results:**
- 50+ vulnerabilities
- Multiple Critical and High CVEs
- Outdated base image (Node 14 EOL)
- Security warnings

---

## Part 2: Progressive Security Improvements

### Step 2: Fix Base Image and Dependencies

1. **Update `package.json` with latest versions:**
   ```json
   {
     "name": "security-demo",
     "version": "1.0.0",
     "dependencies": {
       "express": "^4.18.2",
       "lodash": "^4.17.21",
       "axios": "^1.6.0"
     },
     "scripts": {
       "start": "node server.js"
     }
   }
   ```

2. **Create `.dockerignore`:**
   ```
   node_modules
   npm-debug.log
   .git
   .env
   .DS_Store
   *.md
   .gitignore
   Dockerfile*
   .dockerignore
   ```

3. **Create `Dockerfile.improved`:**
   ```dockerfile
   # ✅ Use current LTS version
   FROM node:20-alpine

   # ✅ Run as non-root user
   RUN addgroup -S appgroup && adduser -S appuser -G appgroup

   WORKDIR /app

   # ✅ Copy only necessary files
   COPY --chown=appuser:appgroup package*.json ./

   # ✅ Use npm ci for reproducible builds
   RUN npm ci --only=production

   # ✅ Copy application code
   COPY --chown=appuser:appgroup server.js ./

   # ✅ Switch to non-root user
   USER appuser

   # ✅ Add healthcheck
   HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
     CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

   EXPOSE 3000

   CMD ["node", "server.js"]
   ```

4. **Build and scan:**
   ```bash
   docker build -t myapp:improved -f Dockerfile.improved .
   docker scout cves myapp:improved
   ```

**✅ Expected Results:**
- 60-70% reduction in CVEs
- Mostly Low/Medium vulnerabilities
- Better security score

---

### Step 3: Convert to Distroless

1. **Create `Dockerfile.distroless`:**
   ```dockerfile
   # syntax=docker/dockerfile:1

   # Build stage
   FROM node:20-alpine AS builder

   WORKDIR /app

   COPY package*.json ./
   RUN npm ci --only=production

   COPY server.js ./

   # Runtime stage - Distroless
   FROM gcr.io/distroless/nodejs20-debian12

   COPY --from=builder /app /app

   WORKDIR /app

   USER nonroot

   EXPOSE 3000

   CMD ["server.js"]
   ```

2. **Build and scan:**
   ```bash
   docker build -t myapp:distroless -f Dockerfile.distroless .
   docker scout cves myapp:distroless
   ```

**✅ Expected Results:**
- 80-90% reduction in CVEs from original
- Smallest image size
- Minimal attack surface

---

## Part 3: Security Comparison Analysis

### Step 4: Create Comparison Report

1. **Scan all versions:**
   ```bash
   echo "=== INSECURE VERSION ===" > security-report.txt
   docker scout cves myapp:insecure >> security-report.txt 2>&1

   echo "" >> security-report.txt
   echo "=== IMPROVED VERSION ===" >> security-report.txt
   docker scout cves myapp:improved >> security-report.txt 2>&1

   echo "" >> security-report.txt
   echo "=== DISTROLESS VERSION ===" >> security-report.txt
   docker scout cves myapp:distroless >> security-report.txt 2>&1
   ```

2. **Compare image sizes:**
   ```bash
   docker images | grep myapp
   ```

3. **Fill in this comparison table:**

   | Metric | Insecure | Improved | Distroless |
   |--------|----------|----------|------------|
   | Base Image | node:14 | node:20-alpine | distroless/nodejs20 |
   | Image Size | ~900MB | ~150MB | ~110MB |
   | Critical CVEs | ? | ? | ? |
   | High CVEs | ? | ? | ? |
   | Total CVEs | ? | ? | ? |
   | Runs as root? | ✅ Yes | ❌ No | ❌ No |
   | Has shell? | ✅ Yes | ✅ Yes | ❌ No |
   | Healthcheck? | ❌ No | ✅ Yes | ❌ No* |
   | Production Ready? | ❌ No | 🟡 Mostly | ✅ Yes |

   *Note: Distroless doesn't support HEALTHCHECK in Dockerfile, but can be added in docker-compose

---

## Part 4: Automated Security Scanning

### Step 5: Create Pre-Push Security Script

1. **Create `security-check.sh`:**
   ```bash
   #!/bin/bash

   set -e

   IMAGE_NAME=$1
   MAX_CRITICAL=0
   MAX_HIGH=0

   if [ -z "$IMAGE_NAME" ]; then
       echo "Usage: ./security-check.sh <image-name>"
       exit 1
   fi

   echo "🔍 Running security checks on $IMAGE_NAME..."
   echo ""

   # Quick view
   echo "📊 Quick Security Overview:"
   docker scout quickview $IMAGE_NAME

   echo ""
   echo "🔐 Detailed CVE Analysis:"
   docker scout cves $IMAGE_NAME

   # Get CVE counts
   echo ""
   echo "📈 Analyzing CVE counts..."

   CRITICAL=$(docker scout cves $IMAGE_NAME 2>&1 | grep -i "critical" | head -1 | grep -oE '[0-9]+' | head -1 || echo "0")
   HIGH=$(docker scout cves $IMAGE_NAME 2>&1 | grep -i "high" | head -1 | grep -oE '[0-9]+' | head -1 || echo "0")

   echo "Critical CVEs: $CRITICAL"
   echo "High CVEs: $HIGH"

   echo ""
   if [ "$CRITICAL" -gt "$MAX_CRITICAL" ]; then
       echo "❌ FAILED: $CRITICAL Critical CVEs found (max allowed: $MAX_CRITICAL)"
       exit 1
   fi

   if [ "$HIGH" -gt "$MAX_HIGH" ]; then
       echo "⚠️  WARNING: $HIGH High CVEs found (max allowed: $MAX_HIGH)"
       echo "Consider fixing these before production deployment"
   fi

   echo ""
   echo "✅ Security check passed!"
   echo ""
   echo "💡 Recommendations:"
   docker scout recommendations $IMAGE_NAME

   exit 0
   ```

2. **Make executable and test:**
   ```bash
   chmod +x security-check.sh
   ./security-check.sh myapp:distroless
   ```

---

## Part 5: CI/CD Integration Pattern

### Step 6: GitHub Actions Security Workflow

Create `.github/workflows/docker-security.yml`:

```yaml
name: Docker Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Build Docker image
      run: |
        docker build -t myapp:${{ github.sha }} .

    - name: Run Docker Scout
      uses: docker/scout-action@v1
      with:
        command: cves
        image: myapp:${{ github.sha }}
        exit-code: true  # Fail if critical CVEs found
        only-severities: critical,high

    - name: Get recommendations
      run: |
        docker scout recommendations myapp:${{ github.sha }}

    - name: Upload scan results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: security-scan-results
        path: scout-results.json
```

**This workflow:**
- ✅ Runs on every push and PR
- ✅ Builds the image
- ✅ Scans for CVEs
- ✅ Fails build if Critical/High CVEs found
- ✅ Uploads results as artifacts

---

## Part 6: Runtime Security Verification

### Step 7: Verify Non-Root Execution

1. **Run container and check user:**
   ```bash
   docker run -d --name security-test myapp:distroless

   # Try to exec as root (should fail in distroless)
   docker exec security-test whoami 2>&1
   # Expected: Error (no shell)

   # Check container processes
   docker top security-test
   # Expected: Process running as 'nonroot' user (UID 65532)
   ```

2. **Verify filesystem permissions:**
   ```bash
   # This should fail (read-only behavior)
   docker exec security-test touch /test.txt 2>&1
   ```

---

## Part 7: Production Deployment Checklist

### Step 8: Final Security Checklist

Before deploying to production, verify:

```markdown
## Pre-Production Security Checklist

### Image Security
- [ ] Using specific image tag (not 'latest')
- [ ] Scanned with Docker Scout (0 Critical, 0 High CVEs)
- [ ] Using minimal base image (Alpine or Distroless)
- [ ] Multi-stage build implemented
- [ ] Image size optimized (<200MB for Node.js apps)
- [ ] .dockerignore file configured

### Dockerfile Security
- [ ] Running as non-root user
- [ ] No secrets in image layers
- [ ] COPY instead of ADD (unless needed)
- [ ] Minimal packages installed
- [ ] HEALTHCHECK defined (or in compose)
- [ ] Only necessary ports exposed

### Runtime Security
- [ ] Resource limits configured
- [ ] Read-only root filesystem (if applicable)
- [ ] Capabilities dropped (if applicable)
- [ ] Security options configured
- [ ] Secrets via environment or files (not hardcoded)

### Monitoring & Maintenance
- [ ] Logging configured
- [ ] Health checks working
- [ ] Update strategy defined
- [ ] Vulnerability monitoring enabled
- [ ] Incident response plan ready

### Compliance
- [ ] Security scan results documented
- [ ] Image provenance tracked
- [ ] SBOM (Software Bill of Materials) available
- [ ] Compliant with organizational policies
```

---

## Expected Outcomes

After completing this exercise, you should:

✅ **Understand** the complete security workflow
✅ **Reduce** CVEs by 80-90% through best practices
✅ **Implement** automated security scanning
✅ **Create** production-ready, secure images
✅ **Integrate** security into CI/CD pipeline
✅ **Verify** runtime security measures

---

## Key Metrics

### Security Improvement Goals:
- **Image Size:** Reduce by 70-80%
- **CVEs:** 0 Critical, 0 High for production
- **Attack Surface:** Minimal (distroless preferred)
- **Build Time:** Optimized with BuildKit cache
- **Scan Time:** <30 seconds per image

---

## Challenge Exercise

**Goal:** Build a "perfect" security score image

**Requirements:**
1. Zero Critical CVEs
2. Zero High CVEs
3. Running as non-root
4. Distroless base image
5. Size under 100MB (for Node.js app)
6. Automated scanning in CI/CD
7. Healthcheck configured

**Success Criteria:**
- All 7 requirements met
- Application runs correctly
- Passes security-check.sh script

---

## Troubleshooting

### "Too many CVEs found"
- Update dependencies to latest versions
- Switch to newer base image
- Consider distroless images
- Check for false positives

### "Image too large"
- Use multi-stage builds
- Switch to alpine or distroless
- Remove unnecessary files with .dockerignore
- Minimize installed packages

### "Can't exec into distroless container"
- This is expected and desired for security
- Use `:debug` variant for debugging
- Use `docker logs` instead
- Debug in non-production environments

---

## Additional Resources

- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Docker Scout Documentation](https://docs.docker.com/scout/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)

---

## Summary

This exercise demonstrates a **production-grade security workflow**:

1. 🔍 **Scan** - Identify vulnerabilities
2. 🔧 **Fix** - Update dependencies and base images
3. 🛡️ **Harden** - Use distroless, non-root, minimal packages
4. ✅ **Verify** - Re-scan and validate improvements
5. 🚀 **Automate** - Integrate into CI/CD pipeline
6. 📊 **Monitor** - Continuous security checking

**Security is not a one-time task—it's an ongoing process!**

---

**Next:** Exercise 2 - Dockerfile Security Best Practices
