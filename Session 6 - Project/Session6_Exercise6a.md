# Exercise 6a: Capstone Project - Introduction & Architecture

**Filename:** `Session6_Exercise6a.md`

---

## Welcome to Your Docker Capstone Project!

Congratulations on reaching the capstone exercise! Over the past six sessions, you've built a comprehensive foundation in Docker. Now it's time to put everything together into a **real-world, production-ready application**.

This capstone is designed to:
- **Integrate all skills** you've learned from Sessions 1-6
- **Build something practical** that you could deploy to production
- **Reinforce best practices** through hands-on implementation
- **Work on all platforms** (Windows, macOS, and Linux)

---

## What You'll Build

### **Task Manager API with PostgreSQL Database**

You'll create a complete, containerized task management system consisting of:

1. **PostgreSQL Database Container**
   - Stores task data persistently
   - Uses Docker volumes for data persistence
   - Isolated on a custom network

2. **Node.js REST API Container**
   - Provides HTTP endpoints for task management
   - Built using multi-stage Dockerfile
   - Optimized for security and performance
   - Connects to PostgreSQL via Docker networking

### **Real-World Application Features**

Your Task Manager will support:
- ✅ Create new tasks with title, description, and status
- ✅ List all tasks
- ✅ Update task details
- ✅ Delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Persist data across container restarts
- ✅ Production-ready deployment

---

## Architecture Overview

### **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                         HOST MACHINE                        │
│                    (Windows/macOS/Linux)                    │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              Docker Custom Network                     │ │
│  │              Name: task-network                        │ │
│  │                                                        │ │
│  │  ┌──────────────────────┐  ┌──────────────────────┐  │ │
│  │  │   API Container      │  │  Database Container  │  │ │
│  │  │                      │  │                      │  │ │
│  │  │  Name: task-api      │  │  Name: task-db       │  │ │
│  │  │  Image: task-api:1.0 │  │  Image: postgres:16  │  │ │
│  │  │  Port: 3000          │  │  Port: 5432          │  │ │
│  │  │                      │  │                      │  │ │
│  │  │  ┌────────────────┐ │  │  ┌────────────────┐  │  │ │
│  │  │  │  Node.js API   │ │  │  │  PostgreSQL    │  │  │ │
│  │  │  │  (Express)     │ │  │  │  Database      │  │  │ │
│  │  │  └────────────────┘ │  │  └────────────────┘  │  │ │
│  │  │         │            │  │         │           │  │ │
│  │  └─────────┼────────────┘  └─────────┼───────────┘  │ │
│  │            │                          │              │ │
│  │            └──────SQL Queries─────────┘              │ │
│  │              (DNS: task-db:5432)                     │ │
│  └───────────────────────────────────────────────────────┘ │
│                          │                                  │
│                  Port Mapping 3000:3000                     │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
                   ┌───────────────┐
                   │  Your Browser │
                   │  or curl/     │
                   │  Postman      │
                   └───────────────┘
              http://localhost:3000/tasks
```

### **Data Persistence Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Volumes                           │
│                                                             │
│  ┌──────────────────────────┐  ┌──────────────────────────┐│
│  │  task-db-data (volume)   │  │  Backup Volume (tmpfs)   ││
│  │  Stores PostgreSQL data  │  │  Temporary backup storage││
│  │                          │  │                          ││
│  │  Mounted to:             │  │  Mounted to:             ││
│  │  /var/lib/postgresql/    │  │  /tmp/backups            ││
│  │        data               │  │                          ││
│  └──────────────────────────┘  └──────────────────────────┘│
│              │                              │               │
│              └──────────────┬───────────────┘               │
│                             │                               │
│                   Backup & Restore Scripts                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Skills Integration Map

This capstone integrates **every skill** you've learned. Here's exactly where each session's knowledge is applied:

### **Session 1: Docker Fundamentals**
**Skills Used:**
- Running containers with `docker run`
- Managing container lifecycle (`docker ps`, `docker stop`, `docker start`)
- Port mapping (`-p` flag)
- Working with Docker images
- Using Docker Hub registry

**Where in Capstone:**
- Exercise 6b: Running PostgreSQL container
- Exercise 6d: Running API container with port mapping
- Exercise 6e: Managing complete application lifecycle

---

### **Session 2: Container Management**
**Skills Used:**
- Detached mode (`-d` flag)
- Interactive mode (`-it` flag)
- Container naming (`--name`)
- Resource limits (`--cpus`, `--memory`)
- Monitoring with `docker stats`
- Environment variables (`-e` flag)

**Where in Capstone:**
- Exercise 6b: Database container with environment variables
- Exercise 6d: Setting resource limits on both containers
- Exercise 6d: Interactive debugging and logs inspection
- Exercise 6e: Monitoring resource usage

---

### **Session 3: Docker Images**
**Skills Used:**
- Writing Dockerfiles
- Basic instructions (FROM, RUN, COPY, WORKDIR, CMD)
- Image building with `docker build`
- Image tagging and versioning
- Layer optimization
- Using `docker history`

**Where in Capstone:**
- Exercise 6c: Writing complete Dockerfile for API
- Exercise 6c: Building and tagging custom images
- Exercise 6c: Analyzing image layers
- Exercise 6c: Comparing image sizes

---

### **Session 4: Advanced Image Building**
**Skills Used:**
- Multi-stage builds
- BuildKit cache mounts
- Docker Scout vulnerability scanning
- Security best practices (non-root user)
- Distroless images (optional)
- Image optimization techniques
- ENTRYPOINT vs CMD

**Where in Capstone:**
- Exercise 6c: Multi-stage build for API (build + production stages)
- Exercise 6c: Using BuildKit cache for npm dependencies
- Exercise 6c: Scanning with Docker Scout
- Exercise 6c: Running as non-root user
- Exercise 6e: Security hardening review

---

### **Session 5: Data Management**
**Skills Used:**
- Named volumes creation and management
- Volume mounting (`-v` flag)
- Data persistence verification
- Bind mounts for development
- tmpfs mounts for temporary data
- Backup and restore strategies
- Volume inspection

**Where in Capstone:**
- Exercise 6b: Creating named volume for database
- Exercise 6b: Verifying data persistence
- Exercise 6d: Using bind mounts for development
- Exercise 6e: Implementing backup procedures
- Exercise 6e: Using tmpfs for logs/cache
- Exercise 6e: Testing disaster recovery

---

### **Session 6: Networking**
**Skills Used:**
- Creating custom bridge networks
- Container-to-container communication
- DNS-based service discovery
- Network isolation
- Port mapping to host
- Network inspection
- Multi-network connectivity

**Where in Capstone:**
- Exercise 6b: Creating custom network (task-network)
- Exercise 6b: Connecting database to network
- Exercise 6d: DNS-based connection (task-api → task-db)
- Exercise 6d: Port mapping for external access
- Exercise 6d: Testing network connectivity
- Exercise 6e: Verifying network isolation

---

## Project Structure

You'll work with the following files and components:

### **Exercise 6b: Database Setup**
```
task-network (custom bridge network)
task-db (PostgreSQL container)
task-db-data (named volume)
```

### **Exercise 6c: Application Build**
```
task-api/
├── package.json          # Node.js dependencies
├── server.js             # Express API code
├── init-db.sql          # Database schema
├── Dockerfile           # Multi-stage build
└── .dockerignore        # Build optimization
```

### **Exercise 6d: Integration**
```
Both containers running:
- task-db (database)
- task-api (application)

Connected via task-network
API accessible at http://localhost:3000
```

### **Exercise 6e: Production Operations**
```
backup-scripts/
├── backup.sh            # Automated backup
└── restore.sh           # Disaster recovery

tmpfs mounts for performance
Security verification
Resource monitoring
```

---

## Platform Compatibility

This capstone is designed to work **identically** on all platforms:

### **Windows Users**
- ✅ **PowerShell** (recommended)
- ✅ **Command Prompt (CMD)**
- ✅ **Git Bash**
- All commands tested on Windows 11 with Docker Desktop
- Special notes provided where Windows differs (e.g., line endings, paths)

### **macOS Users**
- ✅ **Terminal** (any shell: zsh, bash)
- All commands tested on macOS (Intel and Apple Silicon)
- Docker Desktop required (we'll use platform-agnostic approaches)

### **Linux Users**
- ✅ Any distribution with Docker installed
- Native Docker or Docker Desktop
- All commands work as-is

### **Important Platform Notes**

1. **Commands are universal**: All `docker` commands work identically on all platforms
2. **API testing**: We'll provide both `curl` (all platforms) and PowerShell `Invoke-WebRequest` examples
3. **Line endings**: When creating files, Windows users should use LF (not CRLF) - we'll explain how
4. **Paths**: We use forward slashes `/` which work on all platforms inside containers

---

## Learning Objectives

By completing this capstone, you will:

### **Technical Objectives**
- ✅ Build a complete containerized application from scratch
- ✅ Apply multi-stage build patterns to real applications
- ✅ Implement production-grade data persistence
- ✅ Configure secure container networking
- ✅ Set up automated backup and recovery procedures
- ✅ Monitor and optimize container resources
- ✅ Scan and remediate security vulnerabilities

### **Conceptual Objectives**
- ✅ Understand how containers work together to form applications
- ✅ Recognize when to use volumes vs bind mounts vs tmpfs
- ✅ Appreciate the importance of network isolation
- ✅ Apply security-first thinking to container deployments
- ✅ Make informed decisions about image optimization trade-offs

### **Professional Objectives**
- ✅ Deploy production-ready containerized applications
- ✅ Document deployment procedures professionally
- ✅ Implement disaster recovery plans
- ✅ Follow industry best practices throughout
- ✅ Build confidence in your Docker skills

---

## Prerequisites Check

Before starting, ensure you have:

### **Required Software**
- ✅ **Docker Desktop** (version 4.0+) or Docker Engine
  - Verify: `docker --version`
  - Expected: Docker version 24.0+ or newer

- ✅ **Docker Compose v2** integration
  - Verify: `docker compose version`
  - Expected: Docker Compose version v2.0+ or newer

### **Required Knowledge**
You should be comfortable with:
- ✅ Running containers (`docker run`)
- ✅ Building images (`docker build`)
- ✅ Managing volumes (`docker volume`)
- ✅ Creating networks (`docker network`)
- ✅ Writing Dockerfiles
- ✅ Basic command line usage

### **Disk Space**
- ✅ At least **2 GB** free disk space for:
  - PostgreSQL image (~150 MB)
  - Node.js base images (~100 MB)
  - Application images and layers
  - Database data and backups

### **Time Commitment**
- ✅ **Exercise 6a** (this): 15-20 minutes (reading and setup)
- ✅ **Exercise 6b**: 45-60 minutes (database setup)
- ✅ **Exercise 6c**: 60-75 minutes (building application)
- ✅ **Exercise 6d**: 60-75 minutes (integration)
- ✅ **Exercise 6e**: 45-60 minutes (production readiness)
- **Total**: 4-6 hours (can be split across multiple sessions)

---

## How to Approach This Capstone

### **Recommended Approach**

1. **Read All Instructions First**
   - Don't rush! Each exercise builds on the previous one
   - Understand the "why" not just the "how"

2. **Follow the Order**
   - Complete exercises in sequence: 6a → 6b → 6c → 6d → 6e
   - Each exercise assumes completion of previous ones

3. **Type Commands Yourself**
   - Don't copy-paste blindly
   - Understand what each command does
   - Read the explanations provided

4. **Experiment and Explore**
   - Try variations of commands
   - Inspect containers, images, volumes, networks
   - Break things and fix them (great learning!)

5. **Take Notes**
   - Document what you learn
   - Note any platform-specific issues
   - Save successful commands for reference

### **If You Get Stuck**

1. **Read Error Messages Carefully**
   - Docker error messages are usually informative
   - Look for keywords like "not found", "connection refused", "permission denied"

2. **Use Inspection Commands**
   - `docker ps -a` (see all containers)
   - `docker logs <container>` (view container logs)
   - `docker inspect <container>` (detailed info)
   - `docker network inspect <network>` (network details)

3. **Check Platform-Specific Notes**
   - Each exercise has platform-specific guidance
   - Windows users: pay attention to path and line ending notes

4. **Start Fresh If Needed**
   - Clean up: `docker stop $(docker ps -aq)`
   - Remove containers: `docker rm $(docker ps -aq)`
   - Remove volumes: `docker volume prune`
   - Remove networks: `docker network prune`

---

## Expected Outcomes

### **What You'll Have at the End**

After completing all 5 exercises, you will have:

1. **Running Production Application**
   - Task Manager API accessible at http://localhost:3000
   - PostgreSQL database with persistent data
   - Both containers on isolated custom network
   - Resource limits configured
   - Security best practices applied

2. **Optimized Docker Images**
   - Multi-stage build for minimal image size
   - BuildKit cache for faster rebuilds
   - Non-root user for security
   - Vulnerability-scanned and remediated
   - Properly tagged and versioned

3. **Data Management System**
   - Named volume for database persistence
   - Bind mounts for development workflow
   - tmpfs for temporary data
   - Automated backup scripts
   - Tested disaster recovery procedure

4. **Complete Documentation**
   - Deployment runbook
   - Architecture documentation
   - Backup/restore procedures
   - Troubleshooting guide
   - Security checklist

5. **Portfolio-Ready Project**
   - Demonstrates production-ready skills
   - Shows security-first approach
   - Proves understanding of Docker fundamentals
   - Can be shown to potential employers

---

## API Endpoints Reference

Your completed Task Manager API will support these endpoints:

### **Health Check**
```
GET /health
Returns: {"status": "healthy", "database": "connected"}
```

### **List All Tasks**
```
GET /tasks
Returns: Array of all tasks
```

### **Get Single Task**
```
GET /tasks/:id
Returns: Single task by ID
```

### **Create Task**
```
POST /tasks
Body: {
  "title": "Task title",
  "description": "Task description",
  "status": "pending"
}
Returns: Created task with ID
```

### **Update Task**
```
PUT /tasks/:id
Body: {
  "title": "Updated title",
  "description": "Updated description",
  "status": "completed"
}
Returns: Updated task
```

### **Delete Task**
```
DELETE /tasks/:id
Returns: Success message
```

---

## Database Schema

Your PostgreSQL database will have this simple schema:

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_status ON tasks(status);
CREATE INDEX idx_created_at ON tasks(created_at);
```

**Fields:**
- `id`: Auto-incrementing primary key
- `title`: Task title (required, max 255 characters)
- `description`: Detailed description (optional)
- `status`: Task status (`pending`, `in-progress`, `completed`)
- `created_at`: When task was created
- `updated_at`: When task was last modified

---

## Success Criteria

You'll know you've successfully completed the capstone when:

- ✅ You can create a task via API and see it persisted in the database
- ✅ Database data survives container restarts (`docker stop` + `docker start`)
- ✅ API container can communicate with database using DNS name
- ✅ Application is accessible from your browser at http://localhost:3000
- ✅ Image is optimized (multi-stage build, minimal size)
- ✅ Docker Scout shows no critical vulnerabilities
- ✅ Resource limits are enforced (CPU, memory)
- ✅ You can successfully backup and restore the database
- ✅ All containers run on isolated custom network
- ✅ You understand every command you've executed

---

## Let's Get Started!

You're now ready to begin building your containerized Task Manager application!

### **Next Steps**

1. **Proceed to Exercise 6b** - Database Setup & Data Persistence
   - Create custom network
   - Set up PostgreSQL container
   - Configure persistent volume
   - Verify data persistence

2. **What to Expect**
   - Step-by-step instructions with explanations
   - Commands for all platforms (Windows/macOS/Linux)
   - Verification steps to ensure success
   - Clear learning objectives for each section

3. **Preparation**
   - Open a terminal (PowerShell/Terminal/Bash)
   - Ensure Docker Desktop is running
   - Create a working directory: `mkdir docker-capstone && cd docker-capstone`
   - You're ready to go!

---

## Tips for Success

### **Before Each Exercise**
- ✅ Read the entire exercise before starting
- ✅ Understand the learning objectives
- ✅ Have Docker Desktop running

### **During Each Exercise**
- ✅ Follow steps in order
- ✅ Read all explanations, not just commands
- ✅ Verify each step before proceeding
- ✅ Take notes on what you learn

### **After Each Exercise**
- ✅ Test that everything works
- ✅ Review what you built
- ✅ Connect it to previous sessions' concepts
- ✅ Take a short break before the next exercise

---

## Instructor Notes

This capstone is designed to be:
- **Comprehensive**: Covers all Sessions 1-6 skills
- **Practical**: Builds a real, deployable application
- **Educational**: Extensive explanations for deep learning
- **Professional**: Follows industry best practices
- **Accessible**: Works on all platforms identically

Students who complete this capstone will have demonstrated:
- Mastery of Docker fundamentals
- Ability to build production-ready applications
- Understanding of security and optimization
- Professional deployment skills

---

## Ready?

**You've completed Exercise 6a!**

You now understand:
- ✅ What you're building (Task Manager API + Database)
- ✅ How it integrates all Sessions 1-6 skills
- ✅ The architecture and components
- ✅ What success looks like
- ✅ How to approach the capstone

**Next: Exercise 6b - Database Setup & Data Persistence**

Let's build something amazing!

---

**Estimated Time for Exercise 6a:** 15-20 minutes (reading)
**Recommended Break:** 5 minutes before Exercise 6b

**Total Progress:** Exercise 6a ✅ | 6b ⬜ | 6c ⬜ | 6d ⬜ | 6e ⬜

---
