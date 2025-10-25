# Exercise 6c: Building the Application Image

**Filename:** `Session6_Exercise6c.md`

---

## Overview

In this exercise, you'll create a **production-ready Node.js Task Manager API** and build an **optimized Docker image** using advanced techniques from Sessions 3 and 4.

### **What You'll Build**

```
┌───────────────────────────────────────────────────┐
│         Docker Image: task-api:1.0                │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │  Stage 1: Builder (node:20-alpine)          │ │
│  │  - Install dependencies                     │ │
│  │  - Use BuildKit cache mounts                │ │
│  └─────────────────────────────────────────────┘ │
│                      │                            │
│                      ▼                            │
│  ┌─────────────────────────────────────────────┐ │
│  │  Stage 2: Production (node:20-alpine)       │ │
│  │  - Copy only production dependencies        │ │
│  │  - Run as non-root user                     │ │
│  │  - Minimal layers                           │ │
│  │  - Optimized for size & security            │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  Final Size: ~150 MB (vs ~300 MB unoptimized)    │
│  Vulnerabilities: Scanned with Docker Scout       │
└───────────────────────────────────────────────────┘
```

---

## Learning Objectives

By completing this exercise, you will:

### **Session 3 Skills (Image Building)**
- ✅ Create a complete application with dependencies
- ✅ Write Dockerfiles with proper instructions
- ✅ Build Docker images with `docker build`
- ✅ Tag and version images appropriately
- ✅ Optimize Dockerfiles for layer caching
- ✅ Use `.dockerignore` to exclude files

### **Session 4 Skills (Advanced Building)**
- ✅ Implement multi-stage builds for optimization
- ✅ Use BuildKit cache mounts for faster builds
- ✅ Apply security best practices (non-root user)
- ✅ Scan images with Docker Scout
- ✅ Compare image sizes before/after optimization
- ✅ Analyze image layers with `docker history`

---

## Prerequisites

Before starting, ensure:
- ✅ You've completed Exercise 6b (Database is running)
- ✅ Database container `task-db` is running
- ✅ You're in your working directory
- ✅ You have a text editor ready (VS Code, Notepad++, nano, etc.)

---

## Step 1: Create Application Directory Structure

Let's create a proper directory structure for our application.

```bash
# Create main application directory
mkdir -p task-api

# Navigate into it
cd task-api

# Create subdirectories
mkdir -p scripts
```

**Directory Structure:**
```
task-api/
├── package.json          # Node.js dependencies and scripts
├── server.js             # Express API application code
├── init-db.sql          # Database schema (CREATE TABLE)
├── Dockerfile           # Multi-stage build file
├── .dockerignore        # Files to exclude from build
└── scripts/
    └── wait-for-db.sh   # Helper script to wait for database
```

---

## Step 2: Create the Application Code

### **File 1: package.json**

Create `package.json` (Node.js dependencies and metadata):

```bash
# Use your preferred editor
# Windows: notepad package.json
# macOS/Linux: nano package.json
# Or use VS Code: code package.json
```

**Contents of `package.json`:**

```json
{
  "name": "task-manager-api",
  "version": "1.0.0",
  "description": "Task Manager REST API with PostgreSQL",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "keywords": [
    "docker",
    "nodejs",
    "postgresql",
    "rest-api"
  ],
  "author": "Docker Capstone Student",
  "license": "MIT",
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.3",
    "body-parser": "^1.20.2",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

**What This Defines:**
- **express**: Web framework for building REST APIs
- **pg**: PostgreSQL client for Node.js
- **body-parser**: Parse JSON request bodies
- **cors**: Enable cross-origin requests
- **nodemon**: Development tool for auto-restart (dev only)

---

### **File 2: server.js**

Create `server.js` (the main application code):

```javascript
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// PostgreSQL connection pool
const pool = new Pool({
  host: process.env.DB_HOST || 'task-db',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'taskmanager',
  user: process.env.DB_USER || 'taskuser',
  password: process.env.DB_PASSWORD || 'taskpass123',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Test database connection on startup
pool.connect((err, client, release) => {
  if (err) {
    console.error('Error connecting to database:', err.stack);
    process.exit(1);
  }
  console.log('✅ Successfully connected to PostgreSQL database');
  release();
});

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'healthy', database: 'connected' });
  } catch (error) {
    res.status(503).json({ status: 'unhealthy', database: 'disconnected', error: error.message });
  }
});

// Get all tasks
app.get('/tasks', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM tasks ORDER BY created_at DESC');
    res.json({ success: true, count: result.rows.length, data: result.rows });
  } catch (error) {
    console.error('Error fetching tasks:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get single task by ID
app.get('/tasks/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query('SELECT * FROM tasks WHERE id = $1', [id]);

    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Task not found' });
    }

    res.json({ success: true, data: result.rows[0] });
  } catch (error) {
    console.error('Error fetching task:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Create new task
app.post('/tasks', async (req, res) => {
  try {
    const { title, description, status } = req.body;

    if (!title) {
      return res.status(400).json({ success: false, error: 'Title is required' });
    }

    const result = await pool.query(
      'INSERT INTO tasks (title, description, status) VALUES ($1, $2, $3) RETURNING *',
      [title, description || '', status || 'pending']
    );

    res.status(201).json({ success: true, data: result.rows[0] });
  } catch (error) {
    console.error('Error creating task:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Update task
app.put('/tasks/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { title, description, status } = req.body;

    const result = await pool.query(
      'UPDATE tasks SET title = COALESCE($1, title), description = COALESCE($2, description), status = COALESCE($3, status), updated_at = CURRENT_TIMESTAMP WHERE id = $4 RETURNING *',
      [title, description, status, id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Task not found' });
    }

    res.json({ success: true, data: result.rows[0] });
  } catch (error) {
    console.error('Error updating task:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Delete task
app.delete('/tasks/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query('DELETE FROM tasks WHERE id = $1 RETURNING *', [id]);

    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Task not found' });
    }

    res.json({ success: true, message: 'Task deleted successfully' });
  } catch (error) {
    console.error('Error deleting task:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Task Manager API running on port ${PORT}`);
  console.log(`📝 API Endpoints:`);
  console.log(`   GET    /health       - Health check`);
  console.log(`   GET    /tasks        - List all tasks`);
  console.log(`   GET    /tasks/:id    - Get single task`);
  console.log(`   POST   /tasks        - Create new task`);
  console.log(`   PUT    /tasks/:id    - Update task`);
  console.log(`   DELETE /tasks/:id    - Delete task`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, closing server...');
  await pool.end();
  process.exit(0);
});
```

**What This Application Does:**
- ✅ Connects to PostgreSQL database using environment variables
- ✅ Provides RESTful API for task management (CRUD operations)
- ✅ Includes health check endpoint
- ✅ Handles errors gracefully
- ✅ Supports graceful shutdown
- ✅ Production-ready code structure

---

### **File 3: init-db.sql**

Create `init-db.sql` (database schema):

```sql
-- Task Manager Database Schema
-- Creates tasks table with indexes

-- Drop table if exists (for clean restarts)
DROP TABLE IF EXISTS tasks;

-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'in-progress', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Insert sample data for testing
INSERT INTO tasks (title, description, status) VALUES
('Setup Docker Environment', 'Install Docker Desktop and verify installation', 'completed'),
('Learn Docker Networking', 'Understand custom bridge networks and DNS resolution', 'completed'),
('Build REST API', 'Create Node.js application with Express and PostgreSQL', 'in-progress'),
('Deploy to Production', 'Apply security best practices and deploy application', 'pending');

-- Display confirmation
SELECT 'Database schema created successfully!' AS message;
SELECT COUNT(*) || ' sample tasks inserted' AS message FROM tasks;
```

**What This Does:**
- ✅ Creates `tasks` table with appropriate columns
- ✅ Adds indexes for query performance
- ✅ Includes data validation (status constraint)
- ✅ Inserts sample data for testing
- ✅ Can be run multiple times safely (DROP TABLE IF EXISTS)

---

### **File 4: .dockerignore**

Create `.dockerignore` (exclude unnecessary files from build):

```
# Node modules (will be installed in container)
node_modules/
npm-debug.log*

# Development files
.git/
.gitignore
.env
.env.*

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# Operating system files
.DS_Store
Thumbs.db

# Documentation
README.md
*.md

# Test files
test/
tests/
*.test.js
*.spec.js

# Build artifacts
dist/
build/
coverage/

# Logs
logs/
*.log
```

**Why .dockerignore is Important:**
- ✅ **Faster builds** (smaller context sent to Docker)
- ✅ **Smaller images** (no unnecessary files)
- ✅ **Security** (don't include .env files with secrets)
- ✅ **Reproducibility** (no local dev files)

**Session 4 Best Practice**: Always use `.dockerignore`! ✅

---

## Step 3: Create the Database Schema

Before we build the image, let's initialize the database with our schema.

**Run the SQL script on the database:**

```bash
# From the task-api directory, run:
docker exec -i task-db psql -U taskuser -d taskmanager < init-db.sql
```

**Expected Output:**
```
DROP TABLE
CREATE TABLE
CREATE INDEX
CREATE INDEX
INSERT 0 4
           message
---------------------------------
 Database schema created successfully!
(1 row)

         message
--------------------------
 4 sample tasks inserted
(1 row)
```

**Verify the schema:**

```bash
docker exec -it task-db psql -U taskuser -d taskmanager -c "\dt"
```

**Expected Output:**
```
         List of relations
 Schema |  Name | Type  |  Owner
--------+-------+-------+----------
 public | tasks | table | taskuser
(1 row)
```

**View sample data:**

```bash
docker exec -it task-db psql -U taskuser -d taskmanager -c "SELECT id, title, status FROM tasks;"
```

**Expected Output:**
```
 id |           title            |   status
----+----------------------------+--------------
  1 | Setup Docker Environment   | completed
  2 | Learn Docker Networking    | completed
  3 | Build REST API             | in-progress
  4 | Deploy to Production       | pending
(4 rows)
```

Perfect! Database is ready. ✅

---

## Step 4: Write the Dockerfile (Multi-Stage Build)

Now for the main event: creating an optimized Dockerfile!

Create `Dockerfile`:

```dockerfile
# =============================================================================
# Stage 1: Builder
# Purpose: Install dependencies using BuildKit cache mounts
# =============================================================================
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files first (better layer caching)
COPY package*.json ./

# Install ALL dependencies (including devDependencies for potential build steps)
# Use BuildKit cache mount for npm cache (Session 4 skill!)
RUN --mount=type=cache,target=/root/.npm \
    npm ci --prefer-offline --no-audit

# =============================================================================
# Stage 2: Production
# Purpose: Create minimal production image with only necessary files
# =============================================================================
FROM node:20-alpine

# Add metadata labels (good practice)
LABEL maintainer="student@docker-course.com"
LABEL description="Task Manager REST API"
LABEL version="1.0.0"

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user for security (Session 4 best practice!)
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ONLY production dependencies (no devDependencies)
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production --prefer-offline --no-audit && \
    npm cache clean --force

# Copy application code
COPY --chown=nodejs:nodejs server.js ./
COPY --chown=nodejs:nodejs init-db.sql ./

# Switch to non-root user (security!)
USER nodejs

# Expose port (documentation - doesn't actually open port)
EXPOSE 3000

# Health check (Docker can monitor if container is healthy)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start the application
CMD ["node", "server.js"]
```

---

### **Dockerfile Explanation (Line by Line)**

Let's break down every important section:

#### **Stage 1: Builder (Lines 1-14)**

```dockerfile
FROM node:20-alpine AS builder
```
- **What**: Base image for building
- **Why**: Alpine is small (~50 MB vs ~300 MB for full Debian)
- **Session 3**: FROM instruction, choosing base images

```dockerfile
WORKDIR /app
```
- **What**: Sets working directory to `/app`
- **Why**: All subsequent commands run from here
- **Session 3**: WORKDIR instruction

```dockerfile
COPY package*.json ./
```
- **What**: Copy only package files first
- **Why**: Better layer caching! Dependencies don't change often
- **Session 3**: Layer optimization, COPY instruction

```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci --prefer-offline --no-audit
```
- **What**: Install dependencies with cache mount
- **Why**: BuildKit caches npm downloads between builds (huge speed boost!)
- **Session 4**: BuildKit cache mounts ✅
- **Speed improvement**: 2nd build: 2 seconds (vs 30+ seconds without cache)

#### **Stage 2: Production (Lines 16-61)**

```dockerfile
FROM node:20-alpine
```
- **What**: Fresh base image for production
- **Why**: Doesn't include builder stage files (smaller image)
- **Session 4**: Multi-stage build ✅

```dockerfile
LABEL maintainer="..." description="..." version="..."
```
- **What**: Metadata about the image
- **Why**: Documentation, searchability, versioning
- **Best Practice**: Always label production images

```dockerfile
RUN apk add --no-cache dumb-init
```
- **What**: Install dumb-init (tiny init system)
- **Why**: Proper signal handling (SIGTERM, SIGINT)
- **Production**: Ensures graceful shutdown ✅

```dockerfile
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
```
- **What**: Create non-root user
- **Why**: **Security best practice** - never run as root!
- **Session 4**: Security hardening ✅

```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production --prefer-offline --no-audit
```
- **What**: Install only production dependencies
- **Why**: Smaller image (no nodemon, no test frameworks)
- **Session 4**: BuildKit cache, production optimization ✅

```dockerfile
COPY --chown=nodejs:nodejs server.js ./
```
- **What**: Copy application code with correct ownership
- **Why**: Non-root user needs to own the files
- **Session 3**: COPY instruction with ownership

```dockerfile
USER nodejs
```
- **What**: Switch to non-root user
- **Why**: **Critical security practice!**
- **Session 4**: Running as non-root ✅

```dockerfile
EXPOSE 3000
```
- **What**: Documents that app listens on port 3000
- **Why**: Documentation (doesn't actually open port)
- **Session 1**: Port mapping concepts

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s ...
```
- **What**: Docker monitors application health
- **Why**: Production reliability (automatic restart if unhealthy)
- **Session 7**: Healthchecks (if covered) or advanced best practice

```dockerfile
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]
```
- **What**: Start app via dumb-init
- **Why**: Proper signal handling for graceful shutdown
- **Session 4**: ENTRYPOINT vs CMD ✅

---

## Step 5: Build the Docker Image

Now let's build our optimized image!

### **Enable BuildKit (Required for Cache Mounts)**

**Linux/macOS:**
```bash
export DOCKER_BUILDKIT=1
```

**Windows PowerShell:**
```powershell
$env:DOCKER_BUILDKIT=1
```

**Windows CMD:**
```cmd
set DOCKER_BUILDKIT=1
```

**Note**: Docker Desktop 23.0+ has BuildKit enabled by default, but this ensures it's on.

---

### **Build the Image**

```bash
docker build -t task-api:1.0 .
```

**Command Breakdown:**
- `docker build`: Build a Docker image
- `-t task-api:1.0`: Tag the image (name:version)
- `.`: Use current directory as build context

**Expected Output (abbreviated):**

```
[+] Building 45.2s (16/16) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/node:20-alpine
 => [builder 1/4] FROM docker.io/library/node:20-alpine
 => [internal] load build context
 => [builder 2/4] WORKDIR /app
 => [builder 3/4] COPY package*.json ./
 => [builder 4/4] RUN --mount=type=cache,target=/root/.npm npm ci
 => [stage-1 2/8] RUN apk add --no-cache dumb-init
 => [stage-1 3/8] RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
 => [stage-1 4/8] WORKDIR /app
 => [stage-1 5/8] COPY package*.json ./
 => [stage-1 6/8] RUN --mount=type=cache,target=/root/.npm npm ci --only=production
 => [stage-1 7/8] COPY --chown=nodejs:nodejs server.js ./
 => [stage-1 8/8] COPY --chown=nodejs:nodejs init-db.sql ./
 => exporting to image
 => => exporting layers
 => => writing image sha256:a1b2c3d4e5f6...
 => => naming to docker.io/library/task-api:1.0
```

**What Happened:**
- ✅ Downloaded base image (if not cached)
- ✅ Built in two stages (builder, production)
- ✅ Used cache mounts for npm install (fast!)
- ✅ Created non-root user
- ✅ Copied application files
- ✅ Tagged as `task-api:1.0`

**First build**: ~45 seconds
**Subsequent builds (with cache)**: ~2-5 seconds! 🚀

---

### **Verify the Image**

```bash
docker images | grep task-api
```

**Expected Output:**
```
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
task-api     1.0       a1b2c3d4e5f6   2 minutes ago    152MB
```

**Size Analysis:**
- **Our optimized image**: ~150 MB
- **Unoptimized (single-stage, all deps)**: ~300 MB
- **Savings**: 50% reduction! ✅

---

## Step 6: Analyze Image Layers

Let's inspect what's inside our image.

```bash
docker history task-api:1.0
```

**Expected Output (abbreviated):**
```
IMAGE          CREATED         CREATED BY                                      SIZE
a1b2c3d4e5f6   3 minutes ago   CMD ["node" "server.js"]                        0B
b2c3d4e5f6a7   3 minutes ago   ENTRYPOINT ["dumb-init" "--"]                   0B
c3d4e5f6a7b8   3 minutes ago   HEALTHCHECK &{["CMD-SHELL" "node -e ..."}       0B
d4e5f6a7b8c9   3 minutes ago   EXPOSE map[3000/tcp:{}]                         0B
e5f6a7b8c9d0   3 minutes ago   USER nodejs                                     0B
f6a7b8c9d0e1   3 minutes ago   COPY server.js init-db.sql ./                   15kB
a7b8c9d0e1f2   3 minutes ago   RUN npm ci --only=production                    25MB
b8c9d0e1f2a3   3 minutes ago   COPY package*.json ./                           2.5kB
c9d0e1f2a3b4   3 minutes ago   WORKDIR /app                                    0B
d0e1f2a3b4c5   3 minutes ago   RUN addgroup -g 1001 -S nodejs && adduser...    5kB
e1f2a3b4c5d6   3 minutes ago   RUN apk add --no-cache dumb-init                1.2MB
f2a3b4c5d6e7   2 weeks ago     /bin/sh -c #(nop)  CMD ["node"]                 0B
```

**Key Observations:**
- ✅ Most layers are 0B (metadata only)
- ✅ Largest layer: npm dependencies (~25 MB)
- ✅ Application code: tiny! (~15 KB)
- ✅ Base image: node:20-alpine (~125 MB)

**Total**: ~152 MB (very efficient!)

---

## Step 7: Scan for Vulnerabilities with Docker Scout

Let's scan our image for security vulnerabilities!

### **Run Docker Scout Scan**

```bash
docker scout cves task-api:1.0
```

**Expected Output (example):**
```
Analyzing image task-api:1.0
    ✓ Image stored for indexing
    ✓ Indexed 142 packages

## Overview

                    │        Analyzed Image
────────────────────┼─────────────────────────
  Target            │  task-api:1.0
    digest          │  a1b2c3d4e5f6
    platform        │ linux/amd64
    provenance      │ none
    vulnerabilities │    0C     2H     8M    15L
    size            │ 152 MB
    packages        │ 142

## Packages and Vulnerabilities

   0C     2H     8M    15L  express 4.18.2
   0C     0H     0M     3L  pg 8.11.3
   0C     0H     0M     1L  body-parser 1.20.2
   ...
```

**Vulnerability Severity Levels:**
- **C**: Critical (fix immediately!)
- **H**: High (fix soon)
- **M**: Medium (fix when possible)
- **L**: Low (monitor)

**Our Image Results:**
- ✅ **0 Critical vulnerabilities** (excellent!)
- ✅ **2 High** (mostly in transitive dependencies)
- ✅ **8 Medium**
- ✅ **15 Low**

**Action Items:**
- Critical/High: Upgrade packages if fixes available
- Medium/Low: Monitor for updates

---

### **Get Recommendations**

```bash
docker scout recommendations task-api:1.0
```

**Expected Output:**
```
Recommended fixes:

Base image updates available:
  node:20-alpine → node:20.10-alpine (reduces 2 vulnerabilities)

Package updates available:
  express 4.18.2 → 4.19.0 (reduces 1 HIGH vulnerability)
```

**Session 4 Skill**: Scanning and remediating vulnerabilities ✅

---

## Step 8: Compare Optimized vs Unoptimized Builds

Let's prove that our multi-stage build really makes a difference!

### **Create Unoptimized Dockerfile**

Create `Dockerfile.unoptimized`:

```dockerfile
# Single-stage, unoptimized build
FROM node:20

WORKDIR /app

# Copy everything (no .dockerignore)
COPY . .

# Install all dependencies (including dev)
RUN npm install

# Run as root (insecure!)
# No healthcheck
# No dumb-init

EXPOSE 3000

CMD ["node", "server.js"]
```

### **Build Unoptimized Version**

```bash
docker build -f Dockerfile.unoptimized -t task-api:unoptimized .
```

---

### **Compare Sizes**

```bash
docker images | grep task-api
```

**Expected Output:**
```
REPOSITORY   TAG            IMAGE ID       SIZE
task-api     1.0            a1b2c3d4e5f6   152MB    ← Optimized ✅
task-api     unoptimized    b2c3d4e5f6a7   324MB    ← Unoptimized ❌
```

**Comparison:**

| Metric | Optimized | Unoptimized | Improvement |
|--------|-----------|-------------|-------------|
| **Size** | 152 MB | 324 MB | **53% smaller** ✅ |
| **Layers** | 16 | 8 | Better caching ✅ |
| **Security** | Non-root user | Root user | **Much safer** ✅ |
| **Build time (cached)** | 2-5 sec | 30+ sec | **6x faster** ✅ |
| **Production deps only** | Yes ✅ | No ❌ | Smaller attack surface ✅ |

**Session 4 Skills Demonstrated:**
- ✅ Multi-stage builds
- ✅ Image size optimization
- ✅ Security hardening
- ✅ BuildKit cache mounts

---

## Step 9: Test the Image Locally (Quick Test)

Before integrating with the database in Exercise 6d, let's do a quick standalone test.

**Run a container from our image:**

```bash
docker run --rm -e DB_HOST=host.docker.internal -p 3000:3000 task-api:1.0
```

**Note**: This will fail to connect to the database (expected), but shows the app starts correctly.

**Expected Output:**
```
🚀 Task Manager API running on port 3000
📝 API Endpoints:
   GET    /health       - Health check
   GET    /tasks        - List all tasks
   ...
Error connecting to database: connection refused
```

**Press Ctrl+C to stop.**

**What This Proved:**
- ✅ Image runs successfully
- ✅ Application starts correctly
- ✅ Ports are exposed properly
- ✅ Ready for integration with database!

---

## Summary: What You've Accomplished

### **Skills Demonstrated**

✅ **Session 3 (Image Building):**
- Created complete Node.js application
- Wrote Dockerfiles with proper instructions
- Built and tagged Docker images
- Optimized layer caching with proper COPY order
- Used `.dockerignore` to exclude unnecessary files

✅ **Session 4 (Advanced Building):**
- Implemented multi-stage builds (53% size reduction!)
- Used BuildKit cache mounts (6x faster builds!)
- Applied security best practices (non-root user)
- Scanned images with Docker Scout
- Compared optimized vs unoptimized approaches
- Analyzed image layers with `docker history`

---

### **Image Comparison Results**

| Feature | Our Image | Industry Standard |
|---------|-----------|-------------------|
| Size | 152 MB | ✅ Excellent (Alpine-based) |
| Build Speed | 2-5 sec (cached) | ✅ Excellent (BuildKit) |
| Security | Non-root, scanned | ✅ Production-ready |
| Vulnerabilities | 0 Critical | ✅ Excellent |
| Dependencies | Production only | ✅ Best practice |
| Healthcheck | Included | ✅ Best practice |

---

## Next Steps

You now have a production-ready Docker image for your Task Manager API!

**In Exercise 6d, you'll:**
- Run the API container connected to the database
- Configure environment variables for integration
- Set resource limits (CPU, memory)
- Use bind mounts for development workflow
- Test the complete application end-to-end
- Access the API from your browser

---

## Quick Reference Commands

```bash
# Build image
docker build -t task-api:1.0 .

# View images
docker images | grep task-api

# Analyze layers
docker history task-api:1.0

# Scan for vulnerabilities
docker scout cves task-api:1.0

# Get recommendations
docker scout recommendations task-api:1.0

# Remove unoptimized image
docker rmi task-api:unoptimized
```

---

**Estimated Time for Exercise 6c:** 60-75 minutes
**Recommended Break:** 10-15 minutes before Exercise 6d

**Total Progress:** Exercise 6a ✅ | 6b ✅ | 6c ✅ | 6d ⬜ | 6e ⬜

---

**Next: Exercise 6d - Running & Integrating Services**

Excellent work! You've built a professional, optimized Docker image. Now let's bring it all together!

---
