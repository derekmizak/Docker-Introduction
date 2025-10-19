# Exercise 6: Vulnerability Scanning with Docker Scout (2025)

**Filename:** `Session4_Exercise6.md`

## Objective
- Learn to use Docker Scout for vulnerability scanning
- Understand Common Vulnerabilities and Exposures (CVEs)
- Compare security postures of different base images
- Implement fixes for identified vulnerabilities

---

## Prerequisites
- Docker Desktop installed (Docker Scout is built-in)
- Basic understanding of Docker images
- Completed previous Session 4 exercises

---

## What is Docker Scout?

Docker Scout is a built-in tool (2025) that analyzes container images for:
- **Known vulnerabilities (CVEs)** - Security flaws in packages
- **Base image recommendations** - Suggestions for more secure alternatives
- **Outdated packages** - Dependencies that should be updated
- **Policy violations** - Compliance and best practice issues

---

## Part 1: Scanning Your First Image

### Step 1: Pull and Scan a Public Image

1. **Pull a popular image:**
   ```bash
   docker pull nginx:latest
   ```

2. **Scan with Docker Scout:**
   ```bash
   docker scout quickview nginx:latest
   ```

3. **Get detailed CVE report:**
   ```bash
   docker scout cves nginx:latest
   ```

4. **Get recommendations:**
   ```bash
   docker scout recommendations nginx:latest
   ```

### Step 2: Understand the Output

The scout output shows:
- **Critical/High/Medium/Low vulnerabilities** - Severity classification
- **CVE identifiers** - e.g., CVE-2024-12345
- **Affected packages** - Which packages have vulnerabilities
- **Fixed versions** - Available patches
- **Base image recommendations** - Safer alternatives

**Example Output:**
```
Image: nginx:latest
CVEs: 42 total (5 Critical, 12 High, 15 Medium, 10 Low)

Critical vulnerabilities:
  - CVE-2024-XXXXX: openssl 3.0.2 → Fix: upgrade to 3.0.8
  - CVE-2024-YYYYY: curl 7.81.0 → Fix: upgrade to 7.88.1

Recommendation: Use nginx:1.25-alpine (18 fewer CVEs)
```

---

## Part 2: Compare Base Images Security

### Step 3: Scan Different Node.js Base Images

1. **Pull various Node.js base images:**
   ```bash
   docker pull node:20
   docker pull node:20-alpine
   docker pull node:20-slim
   ```

2. **Scan each one:**
   ```bash
   docker scout quickview node:20
   docker scout quickview node:20-alpine
   docker scout quickview node:20-slim
   ```

3. **Create a comparison table:**

| Base Image | Size | Critical CVEs | High CVEs | Total CVEs | Recommendation |
|------------|------|---------------|-----------|------------|----------------|
| node:20 | ~1GB | ? | ? | ? | Development |
| node:20-slim | ~200MB | ? | ? | ? | Production (basic) |
| node:20-alpine | ~150MB | ? | ? | ? | Production (minimal) |

Fill in the `?` marks with actual scan results.

---

## Part 3: Build and Scan Your Own Image

### Step 4: Create a Simple Node.js Application

1. **Create project directory:**
   ```bash
   mkdir security-scan-demo
   cd security-scan-demo
   ```

2. **Create `package.json`:**
   ```json
   {
     "name": "security-demo",
     "version": "1.0.0",
     "dependencies": {
       "express": "^4.18.0"
     },
     "scripts": {
       "start": "node app.js"
     }
   }
   ```

3. **Create `app.js`:**
   ```javascript
   const express = require('express');
   const app = express();

   app.get('/', (req, res) => {
     res.send('Security Scanning Demo');
   });

   app.listen(3000, () => {
     console.log('Server running on port 3000');
   });
   ```

### Step 5: Build with Insecure Base Image

1. **Create `Dockerfile.insecure`:**
   ```dockerfile
   FROM node:14

   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .

   EXPOSE 3000
   CMD ["npm", "start"]
   ```

2. **Build the image:**
   ```bash
   docker build -t myapp:insecure -f Dockerfile.insecure .
   ```

3. **Scan it:**
   ```bash
   docker scout cves myapp:insecure
   docker scout recommendations myapp:insecure
   ```

**Note:** Node 14 is outdated (EOL April 2023) and will have many vulnerabilities!

---

## Part 4: Fix Vulnerabilities

### Step 6: Create Secure Version

1. **Create `Dockerfile.secure`:**
   ```dockerfile
   FROM node:20-alpine

   # Run as non-root user for security
   RUN addgroup -S appgroup && adduser -S appuser -G appgroup

   WORKDIR /app

   # Copy package files with correct ownership
   COPY --chown=appuser:appgroup package*.json ./

   # Install dependencies
   RUN npm ci --only=production

   # Copy application files
   COPY --chown=appuser:appgroup . .

   # Switch to non-root user
   USER appuser

   EXPOSE 3000
   CMD ["npm", "start"]
   ```

2. **Build secure version:**
   ```bash
   docker build -t myapp:secure -f Dockerfile.secure .
   ```

3. **Scan secure version:**
   ```bash
   docker scout cves myapp:secure
   ```

4. **Compare results:**
   ```bash
   docker scout compare myapp:insecure --to myapp:secure
   ```

---

## Part 5: Continuous Scanning in Development

### Step 7: Set Up Automated Scanning

1. **Enable Docker Scout in Docker Desktop:**
   - Open Docker Desktop
   - Go to Settings → Features
   - Enable "Docker Scout"
   - Enable "Vulnerability scanning"

2. **Scan on build (recommended workflow):**
   ```bash
   # Build and immediately scan
   docker build -t myapp:v1 . && docker scout cves myapp:v1
   ```

3. **Create a scanning script `scan.sh`:**
   ```bash
   #!/bin/bash

   IMAGE_NAME=$1

   echo "🔍 Scanning $IMAGE_NAME for vulnerabilities..."
   docker scout cves $IMAGE_NAME

   echo ""
   echo "💡 Getting recommendations..."
   docker scout recommendations $IMAGE_NAME

   echo ""
   echo "📊 Quick view summary:"
   docker scout quickview $IMAGE_NAME
   ```

4. **Make it executable and use it:**
   ```bash
   chmod +x scan.sh
   ./scan.sh myapp:secure
   ```

---

## Part 6: Understanding Vulnerability Severity

### Critical Vulnerabilities
- **Immediate action required**
- Can lead to complete system compromise
- Examples: Remote code execution, privilege escalation

### High Vulnerabilities
- **Address urgently**
- Significant security impact
- Examples: SQL injection, authentication bypass

### Medium Vulnerabilities
- **Plan remediation**
- Moderate risk
- Examples: Information disclosure, weak encryption

### Low Vulnerabilities
- **Monitor and address when updating**
- Minimal immediate risk
- Examples: Minor information leaks

---

## Expected Outcomes

After completing this exercise, you should be able to:
- ✅ Scan Docker images for vulnerabilities using Docker Scout
- ✅ Interpret CVE reports and understand severity levels
- ✅ Compare security postures of different base images
- ✅ Identify and fix common vulnerabilities
- ✅ Implement secure Dockerfile practices
- ✅ Reduce CVE counts in your images by 70%+ through base image selection

---

## Key Takeaways

1. **Always scan before deploying** - Don't deploy vulnerable images to production
2. **Prefer specific tags** - Avoid `:latest`, use versioned tags like `:20-alpine`
3. **Smaller is often safer** - Alpine and slim variants usually have fewer vulnerabilities
4. **Keep images updated** - Regularly rebuild with newer base images
5. **Layer security** - Scanning is one part; also run as non-root, limit capabilities

---

## Challenge Exercise

**Goal:** Achieve zero Critical and High CVEs in a Node.js application image.

1. Start with `node:20-alpine`
2. Keep dependencies minimal
3. Use `npm audit fix` to update packages
4. Run as non-root user
5. Scan and verify

**Success Criteria:**
- 0 Critical CVEs
- 0 High CVEs
- Image size < 200MB
- Application runs correctly

---

## Additional Resources

- [Docker Scout Documentation](https://docs.docker.com/scout/)
- [CVE Database](https://cve.mitre.org/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

---

## Notes for Students

- Docker Scout is **free for personal use** and small teams
- Enterprise features require Docker Business subscription
- Scanning adds minimal time to builds (~5-10 seconds)
- Some CVEs may be false positives or not applicable to your use case
- **Security is a continuous process**, not a one-time check

---

**⚠️ Important:** Never ignore Critical or High vulnerabilities in production images. Always update or find alternatives.
