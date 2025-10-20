# Distroless Container Images - Complete Guide (2025 Edition)

**Last Updated:** October 2025
**Version:** 1.0

---

## 📋 Table of Contents

- [What Are Distroless Images](#what-are-distroless-images)
- [Why Use Distroless](#why-use-distroless)
- [Distroless Providers](#distroless-providers)
- [Size and Security Comparison](#size-and-security-comparison)
- [When to Use What](#when-to-use-what)
- [Practical Examples](#practical-examples)
- [Debugging Distroless Containers](#debugging-distroless-containers)
- [Migration Guide](#migration-guide)
- [Learning Resources](#learning-resources)

---

## What Are Distroless Images?

**Distroless images contain only your application and its runtime dependencies.**

They **exclude:**
- ❌ Package managers (apt, yum, apk)
- ❌ Shell (/bin/sh, /bin/bash)
- ❌ Common utilities (curl, wget, tar)
- ❌ Everything not required to run your app

They **include:**
- ✅ Your application code
- ✅ Runtime dependencies (Node.js, Python, Java, etc.)
- ✅ Essential libraries (glibc, SSL certificates)
- ✅ Minimal OS files

### Key Characteristics:

```
Traditional Image:          Distroless Image:
┌───────────────────┐      ┌───────────────────┐
│ Your Application  │      │ Your Application  │
│ ───────────────── │      │ ───────────────── │
│ Shell & Utilities │      │ Runtime Only      │
│ Package Manager   │  →   │ (No extras!)      │
│ Full OS Distro    │      │                   │
│ (Debian/Ubuntu)   │      │ Minimal OS Files  │
└───────────────────┘      └───────────────────┘
  1 GB - 1.5 GB              50 MB - 200 MB
```

---

## Why Use Distroless?

### **🔒 Security Benefits:**

1. **Reduced Attack Surface**
   - Fewer packages = fewer vulnerabilities
   - No shell = harder for attackers to execute commands
   - No package manager = can't install malicious tools

2. **Fewer CVEs**
   - 50-80% reduction in Common Vulnerabilities and Exposures
   - Eliminates most high and critical severity issues
   - Only runtime dependencies scanned

3. **Compliance**
   - Meets security requirements (PCI, HIPAA, SOC 2)
   - Easier security audits
   - Clear software bill of materials (SBOM)

### **⚡ Performance Benefits:**

1. **Smaller Image Size**
   - 30-70% smaller than equivalent Alpine images
   - Faster pulls from registry
   - Faster deployments

2. **Faster Container Startup**
   - Less to initialize
   - Quicker in Kubernetes environments

3. **Reduced Network Transfer**
   - Important in CI/CD pipelines
   - Saves bandwidth costs

### **📊 Operational Benefits:**

1. **Immutability**
   - No tools to modify container at runtime
   - Enforces container best practices
   - Prevents configuration drift

2. **Simplified Compliance**
   - Fewer components to track
   - Clear dependency chain
   - Reproducible builds

---

## Distroless Providers

### **1. Google Distroless (gcr.io) - Original & Most Popular**

**Registry:** `gcr.io/distroless/*`

**Background:**
- Created by Google
- Based on Debian
- **Note:** Google Container Registry (GCR) deprecated March 18, 2025
- **Still works!** Backend migrated to Artifact Registry, domain unchanged

**Available Images:**

| Image | Base Size | Use Case |
|-------|-----------|----------|
| `gcr.io/distroless/static-debian12` | ~2.45 MB | Go, Rust (no glibc needed) |
| `gcr.io/distroless/base-debian12` | ~29 MB | Apps needing glibc |
| `gcr.io/distroless/cc-debian12` | ~30 MB | C/C++ apps |
| `gcr.io/distroless/nodejs20-debian12` | ~150 MB | Node.js applications |
| `gcr.io/distroless/python3-debian12` | ~52 MB | Python applications |
| `gcr.io/distroless/java17-debian12` | ~231 MB | Java 17 applications |

**Pros:**
- ✅ Most widely used and tested
- ✅ Good documentation
- ✅ Multiple language variants
- ✅ Stable and reliable

**Cons:**
- ❌ Hard to customize/extend
- ❌ Based on Debian (slower security patches than Ubuntu)
- ❌ No built-in versioning/tagging strategy

**Example:**
```dockerfile
# Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Distroless runtime
FROM gcr.io/distroless/nodejs20-debian12
COPY --from=builder /app /app
WORKDIR /app
USER nonroot
CMD ["server.js"]
```

---

### **2. Chainguard Images (cgr.dev) - Modern Alternative**

**Registry:** `cgr.dev/chainguard/*`

**Background:**
- Created by Chainguard (container security company)
- Based on Wolfi (custom distro, not Debian)
- Designed for security-first workflows

**Available Images:**

| Image | Base Size | Use Case |
|-------|-----------|----------|
| `cgr.dev/chainguard/static` | ~2 MB | Static binaries (Go, Rust) |
| `cgr.dev/chainguard/glibc-dynamic` | ~15 MB | Apps needing glibc |
| `cgr.dev/chainguard/node:latest` | ~140 MB | Node.js applications |
| `cgr.dev/chainguard/python:latest` | ~50 MB | Python applications |
| `cgr.dev/chainguard/jre:latest` | ~200 MB | Java applications |

**Pros:**
- ✅ Often **fewer CVEs** than Google distroless
- ✅ **Easier to extend** (built with apko)
- ✅ Signed **SBOMs** included
- ✅ Multi-layer approach (70% size reduction in catalog)
- ✅ Better for supply chain security

**Cons:**
- ❌ Newer, less battle-tested
- ❌ Smaller community
- ❌ Some images require paid subscription

**Example:**
```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o app main.go

# Chainguard static
FROM cgr.dev/chainguard/static:latest
COPY --from=builder /app/app /app
CMD ["/app"]
```

---

### **3. Red Hat UBI Micro - Enterprise Choice**

**Registry:** `registry.access.redhat.com/ubi9/*`

**Background:**
- Red Hat Universal Base Images
- Based on RHEL (Red Hat Enterprise Linux)
- Preferred in enterprise environments

**Available Images:**

| Image | Base Size | Use Case |
|-------|-----------|----------|
| `ubi9/ubi-micro` | ~30 MB | Minimal RHEL-based |
| `ubi9/ubi-minimal` | ~90 MB | With microdnf package manager |
| `ubi9/nodejs-18` | ~300 MB | Node.js with UBI base |
| `ubi9/python-39` | ~350 MB | Python with UBI base |

**Pros:**
- ✅ **Enterprise support** from Red Hat
- ✅ RHEL-based (preferred by many organizations)
- ✅ Long-term support
- ✅ Compliance certifications

**Cons:**
- ❌ **Larger** than Google distroless or Chainguard
- ❌ RHEL dependency (not pure minimalism)
- ❌ Slower innovation cycle

**Example:**
```dockerfile
FROM registry.access.redhat.com/ubi9/nodejs-18:latest AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

FROM registry.access.redhat.com/ubi9/ubi-micro:latest
COPY --from=builder /app /app
WORKDIR /app
CMD ["node", "server.js"]
```

---

### **4. Chiseled Ubuntu - Canonical's Solution**

**Registry:** Ubuntu OCI images

**Background:**
- Created by Canonical (Ubuntu makers)
- Built with "Chisel" package slicer
- Combines Ubuntu reliability with distroless philosophy

**Available Images:**

| Image | Use Case |
|-------|----------|
| Chiseled Ubuntu base | General purpose |
| .NET chiseled images | **Adopted by Microsoft** |
| Various language runtimes | Growing ecosystem |

**Pros:**
- ✅ **6x smaller attack surface** than standard Ubuntu
- ✅ Ubuntu ecosystem and tooling
- ✅ **Adopted by Microsoft** for .NET
- ✅ Developer-friendly build process

**Cons:**
- ❌ Newer offering (less mature)
- ❌ Smaller selection of pre-built images
- ❌ Limited documentation

**Example:**
```dockerfile
# Using Microsoft's .NET chiseled image
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app
COPY . .
RUN dotnet publish -c Release -o out

FROM mcr.microsoft.com/dotnet/runtime:8.0-jammy-chiseled
COPY --from=build /app/out .
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

---

## Size and Security Comparison

### **Base Image Sizes (Real Numbers):**

```
┌────────────────────────────────────┬──────────┬────────────┐
│ Image                              │ Size     │ CVEs (avg) │
├────────────────────────────────────┼──────────┼────────────┤
│ FROM scratch                       │ 0 MB     │ 0          │
│ cgr.dev/chainguard/static          │ 2.0 MB   │ 0-2        │
│ gcr.io/distroless/static-debian12  │ 2.45 MB  │ 0-5        │
│ alpine:3.19                        │ 5.54 MB  │ 5-15       │
│ ubi9/ubi-micro                     │ 30 MB    │ 10-20      │
│ ubuntu:22.04                       │ 77 MB    │ 50-100     │
│ debian:12                          │ 124 MB   │ 80-150     │
│ node:20 (full)                     │ 1.1 GB   │ 200+       │
└────────────────────────────────────┴──────────┴────────────┘
```

### **Language-Specific Comparison:**

#### **Node.js:**
```
node:20                                → 1.1 GB, 200+ CVEs
node:20-alpine                         → 150 MB, 30-50 CVEs
gcr.io/distroless/nodejs20-debian12    → 150 MB, 5-15 CVEs ✅
cgr.dev/chainguard/node:latest         → 140 MB, 0-5 CVEs ✅✅
```

#### **Python:**
```
python:3.11                            → 1.0 GB, 180+ CVEs
python:3.11-alpine                     → 50 MB, 20-30 CVEs
gcr.io/distroless/python3-debian12     → 52 MB, 5-10 CVEs ✅
cgr.dev/chainguard/python:latest       → 50 MB, 0-5 CVEs ✅✅
```

#### **Go (compiled):**
```
golang:1.21 (for runtime)              → 800 MB, 150+ CVEs
alpine:3.19                            → 5.5 MB, 5-10 CVEs
gcr.io/distroless/static-debian12      → 2.45 MB, 0-3 CVEs ✅
cgr.dev/chainguard/static              → 2.0 MB, 0-2 CVEs ✅✅
FROM scratch                           → 0 MB, 0 CVEs ✅✅✅
```

---

## When to Use What?

### **Decision Tree:**

```
START: What's your app language?
│
├─ Compiled (Go, Rust, C/C++)
│  └─> Can use static binaries?
│     ├─ YES → FROM scratch (0 MB, 0 CVEs) ⭐⭐⭐
│     └─ NO (need glibc) → gcr.io/distroless/static or cgr.dev/chainguard/static ⭐⭐
│
├─ Node.js
│  └─> Is this production?
│     ├─ YES → cgr.dev/chainguard/node or gcr.io/distroless/nodejs20 ⭐⭐
│     └─ NO (dev) → node:20-alpine ⭐
│
├─ Python
│  └─> Is this production?
│     ├─ YES → cgr.dev/chainguard/python or gcr.io/distroless/python3 ⭐⭐
│     └─ NO (dev) → python:3.11-alpine ⭐
│
├─ Java
│  └─> Need enterprise support?
│     ├─ YES → ubi9/java or gcr.io/distroless/java17 ⭐⭐
│     └─ NO → cgr.dev/chainguard/jre ⭐⭐
│
└─ .NET
   └─> Microsoft's chiseled images! ⭐⭐
      mcr.microsoft.com/dotnet/runtime:8.0-jammy-chiseled
```

### **Use Case Matrix:**

| Scenario | Recommended Choice | Why |
|----------|-------------------|-----|
| **Startup/Small Team** | Chainguard (cgr.dev) | Fewest CVEs, easy to use |
| **Enterprise** | Red Hat UBI Micro | Support, compliance, RHEL |
| **Google Cloud** | Google distroless (gcr.io) | Native integration |
| **Open Source** | Google distroless | Most documented |
| **Microsoft Stack** | Chiseled Ubuntu (.NET) | Official Microsoft choice |
| **Maximum Security** | Chainguard | Best CVE record |
| **Go/Rust Apps** | FROM scratch | Smallest, zero CVEs |

---

## Practical Examples

### **Example 1: Node.js API (Google Distroless)**

```dockerfile
# syntax=docker/dockerfile:1

# Build stage
FROM node:20-alpine AS builder
WORKDIR /app

# Copy dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application
COPY . .

# Production stage
FROM gcr.io/distroless/nodejs20-debian12:nonroot

# Copy from builder
COPY --from=builder /app /app
WORKDIR /app

# Already running as nonroot user
CMD ["server.js"]
```

**Result:**
- Size: ~150 MB (vs 1.1 GB with node:20)
- CVEs: 5-10 (vs 200+ with node:20)
- No shell for attackers

---

### **Example 2: Python FastAPI (Chainguard)**

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.11-slim AS builder
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application
COPY . .

# Distroless runtime
FROM cgr.dev/chainguard/python:latest

# Copy from builder
COPY --from=builder /root/.local /home/nonroot/.local
COPY --from=builder /app /app

WORKDIR /app
ENV PATH=/home/nonroot/.local/bin:$PATH

# Run as non-root
USER nonroot
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Result:**
- Size: ~100 MB
- CVEs: 0-3 (Chainguard's best-in-class)
- Supply chain security with SBOM

---

### **Example 3: Go Service (FROM scratch)**

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.21-alpine AS builder
WORKDIR /app

# Dependencies
COPY go.mod go.sum ./
RUN go mod download

# Build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

# Distroless (smallest possible)
FROM scratch

# Copy binary
COPY --from=builder /app/app /app

# Copy CA certificates for HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080
CMD ["/app"]
```

**Result:**
- Size: ~10-20 MB (just your binary!)
- CVEs: 0 (nothing to scan!)
- Ultimate minimalism

---

### **Example 4: Java Spring Boot (Multi-Platform)**

```dockerfile
# syntax=docker/dockerfile:1

FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app

# Copy and build
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Distroless runtime
FROM gcr.io/distroless/java17-debian12:nonroot

# Copy JAR
COPY --from=builder /app/target/*.jar /app/app.jar

WORKDIR /app
EXPOSE 8080

CMD ["app.jar"]
```

**Result:**
- Size: ~250 MB (vs 600+ MB with full JDK)
- CVEs: 10-20 (vs 100+ with full image)
- Production-ready

---

## Debugging Distroless Containers

### **Challenge: No Shell!**

Distroless images have **no shell**, which makes debugging tricky.

### **Solution 1: Use :debug Tag**

Most distroless images have a `:debug` variant with busybox:

```bash
# Regular (no shell)
docker run gcr.io/distroless/nodejs20-debian12

# Debug variant (has shell)
docker run -it gcr.io/distroless/nodejs20-debian12:debug sh
```

**For development only!** Never use `:debug` in production.

---

### **Solution 2: Use cdebug Tool**

**cdebug** attaches a debug container to running distroless containers:

```bash
# Install cdebug
brew install cdebug

# Debug running container without changing it
cdebug exec -it mycontainer sh
```

**Benefits:**
- Don't modify production image
- Attach/detach debugging tools
- Production image stays minimal

---

### **Solution 3: kubectl debug (Kubernetes)**

For Kubernetes deployments:

```bash
# Attach ephemeral debug container
kubectl debug mypod -it --image=busybox --target=mycontainer
```

---

### **Solution 4: Build-Time Debugging**

Debug in builder stage before copying to distroless:

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY . .

# Debug here (has shell)
RUN ls -la
RUN node --version

FROM gcr.io/distroless/nodejs20-debian12
COPY --from=builder /app /app
# ...
```

---

## Migration Guide

### **Step-by-Step: Alpine → Distroless**

#### **Before (Alpine):**
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "server.js"]
```

#### **After (Distroless):**
```dockerfile
# Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Distroless runtime
FROM gcr.io/distroless/nodejs20-debian12:nonroot
COPY --from=builder /app /app
WORKDIR /app
CMD ["server.js"]
```

**Changes:**
1. ✅ Split into multi-stage build
2. ✅ Install dependencies in builder
3. ✅ Copy only needed files to runtime
4. ✅ Use :nonroot variant (runs as UID 65532)

**Result:**
- Same functionality
- 50-80% fewer CVEs
- Slightly smaller image
- More secure

---

## Learning Resources

### **Official Documentation:**

1. **Google Distroless:**
   - GitHub: https://github.com/GoogleContainerTools/distroless
   - Examples: https://github.com/GoogleContainerTools/distroless/tree/main/examples

2. **Chainguard Academy:**
   - Getting Started: https://edu.chainguard.dev/chainguard/chainguard-images/about/getting-started-distroless/
   - Debugging: https://edu.chainguard.dev/chainguard/chainguard-images/debugging-distroless-images/

3. **Docker Official:**
   - Distroless Docs: https://docs.docker.com/dhi/core-concepts/distroless/

4. **Red Hat UBI:**
   - Documentation: https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/building_running_and_managing_containers/

5. **Chiseled Ubuntu:**
   - Overview: https://ubuntu.com/containers/chiseled
   - Blog: https://ubuntu.com/blog/combining-distroless-and-ubuntu-chiselled-containers

### **Hands-On Tutorials:**

1. **"What's Inside Distroless?"** (iximiuz Labs)
   - https://labs.iximiuz.com/tutorials/gcr-distroless-container-images
   - Interactive exploration

2. **"Distroless Docker Images Guide"** (Bell SW)
   - https://bell-sw.com/blog/distroless-containers-for-security-and-size/
   - Comprehensive overview

3. **"How to Build Your Own Distroless Images"** (INNOQ)
   - https://www.innoq.com/en/blog/2023/02/how-to-use-and-build-your-own-distroless-images/
   - Custom image creation

### **Comparison Articles:**

1. **"Alpine, Distroless, or Scratch?"** (Google Cloud)
   - https://medium.com/google-cloud/alpine-distroless-or-scratch-caac35250e0b
   - Real migration experience from Google engineer

2. **"In Pursuit of Better Container Images"** (iximiuz)
   - https://iximiuz.com/en/posts/containers-making-images-better/
   - Deep dive comparison

3. **"Is Your Container Image Really Distroless?"** (Docker Blog)
   - https://www.docker.com/blog/is-your-container-image-really-distroless/
   - Best practices

### **Video Resources:**

- Search for "distroless containers" on YouTube
- Chainguard webinars
- DockerCon presentations on minimal images

---

## Quick Reference Card

```
DISTROLESS QUICK REFERENCE (2025)

PROVIDERS:
├─ Google (gcr.io) - Original, most popular
├─ Chainguard (cgr.dev) - Fewest CVEs, easiest to extend
├─ Red Hat (UBI Micro) - Enterprise support
└─ Canonical (Chiseled) - Ubuntu-based

WHEN TO USE:
✅ Production deployments
✅ Security-critical applications
✅ Kubernetes/cloud-native apps
✅ Compliance requirements

WHEN NOT TO USE:
❌ Development (need shell)
❌ Need package manager at runtime
❌ Heavy debugging required

SIZE COMPARISON:
FROM scratch:        0 MB
Chainguard static:   2 MB    ⭐⭐⭐
Google static:       2.45 MB ⭐⭐
Alpine:              5.5 MB  ⭐
UBI Micro:           30 MB

DEBUGGING:
- Use :debug tags in dev
- Use cdebug tool
- kubectl debug for K8s
- Debug in builder stage

BEST PRACTICE:
Use full/Alpine for dev
Use distroless for prod
```

---

## Frequently Asked Questions

### **Q: Can I install packages in distroless images?**
**A:** No, that's the point! No package manager. Install everything in the builder stage.

### **Q: How do I debug without a shell?**
**A:** Use `:debug` tags (dev only), cdebug tool, or debug in builder stage.

### **Q: Is distroless slower?**
**A:** No! Usually faster due to smaller size and fewer components to initialize.

### **Q: Can I use distroless with Docker Compose?**
**A:** Yes! Works exactly the same as any other image.

### **Q: Which provider should I use?**
**A:**
- **Startup:** Chainguard (best security)
- **Enterprise:** Red Hat UBI (support)
- **General:** Google distroless (most tested)

### **Q: Are distroless images suitable for all apps?**
**A:** Not if you need to install packages at runtime or require interactive debugging. Best for stateless, well-tested production apps.

---

**Version:** 1.0 | **Last Updated:** October 2025
**Maintained by:** Docker Course Team

**Keep this guide handy when choosing base images for production!**
