# Exercise 6d: Running & Integrating Services

**Filename:** `Session6_Exercise6d.md`

---

## Overview

In this exercise, you'll **bring everything together**! You'll run your Task Manager API container, connect it to the PostgreSQL database, and test the complete application end-to-end.

### **What You'll Complete**

```
┌─────────────────────────────────────────────────────────┐
│                  Complete Application                   │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │       Custom Network: task-network                │ │
│  │                                                   │ │
│  │  ┌────────────────┐      ┌────────────────────┐  │ │
│  │  │   task-api     │◄────►│     task-db        │  │ │
│  │  │   (Node.js)    │ DNS  │   (PostgreSQL)     │  │ │
│  │  │                │      │                    │  │ │
│  │  │  Port: 3000    │      │  Volume: Persisted │  │ │
│  │  │  CPU: 0.5      │      │  CPU: 1.0          │  │ │
│  │  │  RAM: 512MB    │      │  RAM: 1GB          │  │ │
│  │  └────────────────┘      └────────────────────┘  │ │
│  │          │                                        │ │
│  └──────────┼────────────────────────────────────────┘ │
│             │                                          │
│     Port Mapping: 3000:3000                           │
│             │                                          │
│             ▼                                          │
│    ┌─────────────────┐                                │
│    │  Your Browser   │                                │
│    │  curl/Postman   │                                │
│    └─────────────────┘                                │
└─────────────────────────────────────────────────────────┘
```

---

## Learning Objectives

By completing this exercise, you will:

### **Session 2 Skills (Container Management)**
- ✅ Run containers in detached mode
- ✅ Set resource limits (CPU, memory)
- ✅ Configure environment variables
- ✅ Monitor container resource usage with `docker stats`
- ✅ View and follow container logs

### **Session 5 Skills (Data Management)**
- ✅ Use bind mounts for development workflow
- ✅ Enable hot-reloading for code changes
- ✅ Understand when to use bind mounts vs volumes

### **Session 6 Skills (Networking)**
- ✅ Connect multiple containers on same network
- ✅ Use DNS-based service discovery
- ✅ Test inter-container communication
- ✅ Map ports for external access
- ✅ Verify network isolation

---

## Prerequisites

Before starting, ensure:
- ✅ You've completed Exercise 6c (Built task-api:1.0 image)
- ✅ Database container `task-db` is running
- ✅ You're in the `task-api` directory
- ✅ You have `docker images | grep task-api:1.0` showing the image

---

## Step 1: Verify Database is Running

Before we start the API, let's confirm the database is ready.

```bash
docker ps | grep task-db
```

**Expected Output:**
```
CONTAINER ID   IMAGE                 STATUS         PORTS                    NAMES
b3c4d5e6f7a8   postgres:16-alpine   Up 2 hours     0.0.0.0:5432->5432/tcp   task-db
```

**If task-db is not running:**

```bash
# Start the database
docker start task-db

# Wait 5 seconds for it to fully start
sleep 5

# Verify it's healthy
docker logs task-db | grep "ready to accept connections"
```

✅ Database is ready!

---

## Step 2: Run the API Container (Production Mode)

Let's run the API container with **all production configurations**.

### **The Complete Command**

**Linux/macOS:**
```bash
docker run -d \
  --name task-api \
  --network task-network \
  -e DB_HOST=task-db \
  -e DB_PORT=5432 \
  -e DB_NAME=taskmanager \
  -e DB_USER=taskuser \
  -e DB_PASSWORD=taskpass123 \
  -e PORT=3000 \
  -p 3000:3000 \
  --cpus="0.5" \
  --memory="512m" \
  --restart unless-stopped \
  task-api:1.0
```

**Windows PowerShell:**
```powershell
docker run -d `
  --name task-api `
  --network task-network `
  -e DB_HOST=task-db `
  -e DB_PORT=5432 `
  -e DB_NAME=taskmanager `
  -e DB_USER=taskuser `
  -e DB_PASSWORD=taskpass123 `
  -e PORT=3000 `
  -p 3000:3000 `
  --cpus="0.5" `
  --memory="512m" `
  --restart unless-stopped `
  task-api:1.0
```

**Windows CMD:**
```cmd
docker run -d ^
  --name task-api ^
  --network task-network ^
  -e DB_HOST=task-db ^
  -e DB_PORT=5432 ^
  -e DB_NAME=taskmanager ^
  -e DB_USER=taskuser ^
  -e DB_PASSWORD=taskpass123 ^
  -e PORT=3000 ^
  -p 3000:3000 ^
  --cpus="0.5" ^
  --memory="512m" ^
  --restart unless-stopped ^
  task-api:1.0
```

---

### **Command Explanation (Flag by Flag)**

| Flag | Purpose | Session |
|------|---------|---------|
| `-d` | Detached mode (run in background) | Session 2 |
| `--name task-api` | Container name for easy reference | Session 2 |
| `--network task-network` | Connect to custom network | Session 6 |
| `-e DB_HOST=task-db` | Database hostname (DNS name!) | Session 6 |
| `-e DB_PORT=5432` | Database port | Session 2 |
| `-e DB_NAME=taskmanager` | Database name | Session 2 |
| `-e DB_USER=taskuser` | Database user | Session 2 |
| `-e DB_PASSWORD=taskpass123` | Database password | Session 2 |
| `-e PORT=3000` | API server port | Session 2 |
| `-p 3000:3000` | Port mapping (host:container) | Session 1 |
| `--cpus="0.5"` | CPU limit (0.5 cores) | Session 2 |
| `--memory="512m"` | Memory limit (512 MB) | Session 2 |
| `--restart unless-stopped` | Auto-restart policy | Session 2 |
| `task-api:1.0` | Image to run | Session 3 |

**Key Concept (Session 6):**
- `DB_HOST=task-db` uses the **container name** (not IP!)
- Docker's custom network DNS resolves `task-db` automatically
- This is why we created a custom network! ✅

---

### **Expected Output**

```
c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
```

(Container ID hash)

---

### **Verify Container is Running**

```bash
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE            STATUS         PORTS                    NAMES
c5d6e7f8a9b0   task-api:1.0    Up 3 seconds   0.0.0.0:3000->3000/tcp   task-api
b3c4d5e6f7a8   postgres:16-alpine  Up 2 hours     0.0.0.0:5432->5432/tcp   task-db
```

**What to Verify:**
- ✅ `STATUS`: "Up X seconds" (if "Exited", check logs)
- ✅ `PORTS`: Shows `0.0.0.0:3000->3000/tcp`
- ✅ Both containers running

---

### **Check Container Logs**

```bash
docker logs task-api
```

**Expected Output:**
```
✅ Successfully connected to PostgreSQL database
🚀 Task Manager API running on port 3000
📝 API Endpoints:
   GET    /health       - Health check
   GET    /tasks        - List all tasks
   GET    /tasks/:id    - Get single task
   POST   /tasks        - Create new task
   PUT    /tasks/:id    - Update task
   DELETE /tasks/:id    - Delete task
```

✅ **Perfect!** The API connected to the database successfully!

---

## Step 3: Test API Endpoints

Now let's test every endpoint to ensure everything works!

### **Test 1: Health Check**

**Using curl (Linux/macOS/Windows Git Bash):**
```bash
curl http://localhost:3000/health
```

**Using PowerShell (Windows):**
```powershell
(Invoke-WebRequest -Uri http://localhost:3000/health).Content
```

**Expected Output:**
```json
{"status":"healthy","database":"connected"}
```

✅ **Application is healthy and connected to database!**

---

### **Test 2: List All Tasks**

**Using curl:**
```bash
curl http://localhost:3000/tasks
```

**Using PowerShell:**
```powershell
(Invoke-WebRequest -Uri http://localhost:3000/tasks).Content
```

**Expected Output:**
```json
{
  "success": true,
  "count": 4,
  "data": [
    {
      "id": 4,
      "title": "Deploy to Production",
      "description": "Apply security best practices and deploy application",
      "status": "pending",
      "created_at": "2025-10-25T12:00:00.000Z",
      "updated_at": "2025-10-25T12:00:00.000Z"
    },
    {
      "id": 3,
      "title": "Build REST API",
      "description": "Create Node.js application with Express and PostgreSQL",
      "status": "in-progress",
      "created_at": "2025-10-25T12:00:00.000Z",
      "updated_at": "2025-10-25T12:00:00.000Z"
    },
    ...
  ]
}
```

✅ **API can read from the database!**

---

### **Test 3: Create a New Task**

**Using curl:**
```bash
curl -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete Docker Capstone", "description": "Finish all 5 exercises", "status": "in-progress"}'
```

**Using PowerShell:**
```powershell
$body = @{
    title = "Complete Docker Capstone"
    description = "Finish all 5 exercises"
    status = "in-progress"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:3000/tasks `
  -Method POST `
  -Body $body `
  -ContentType "application/json" | Select-Object -ExpandProperty Content
```

**Expected Output:**
```json
{
  "success": true,
  "data": {
    "id": 5,
    "title": "Complete Docker Capstone",
    "description": "Finish all 5 exercises",
    "status": "in-progress",
    "created_at": "2025-10-25T14:30:00.000Z",
    "updated_at": "2025-10-25T14:30:00.000Z"
  }
}
```

✅ **API can write to the database!**

---

### **Test 4: Get Single Task**

**Using curl:**
```bash
curl http://localhost:3000/tasks/5
```

**Using PowerShell:**
```powershell
(Invoke-WebRequest -Uri http://localhost:3000/tasks/5).Content
```

**Expected Output:**
```json
{
  "success": true,
  "data": {
    "id": 5,
    "title": "Complete Docker Capstone",
    "description": "Finish all 5 exercises",
    "status": "in-progress",
    ...
  }
}
```

✅ **Can retrieve specific tasks!**

---

### **Test 5: Update a Task**

**Using curl:**
```bash
curl -X PUT http://localhost:3000/tasks/5 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

**Using PowerShell:**
```powershell
$body = @{ status = "completed" } | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:3000/tasks/5 `
  -Method PUT `
  -Body $body `
  -ContentType "application/json" | Select-Object -ExpandProperty Content
```

**Expected Output:**
```json
{
  "success": true,
  "data": {
    "id": 5,
    "title": "Complete Docker Capstone",
    "description": "Finish all 5 exercises",
    "status": "completed",
    ...
  }
}
```

✅ **Can update tasks!**

---

### **Test 6: Delete a Task**

**Using curl:**
```bash
curl -X DELETE http://localhost:3000/tasks/5
```

**Using PowerShell:**
```powershell
Invoke-WebRequest -Uri http://localhost:3000/tasks/5 -Method DELETE | Select-Object -ExpandProperty Content
```

**Expected Output:**
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

✅ **Can delete tasks!**

---

### **Test 7: Browser Access**

Open your browser and visit:

```
http://localhost:3000/tasks
```

You should see JSON data displayed in the browser! ✅

**Try this too:**
```
http://localhost:3000/health
```

---

## Step 4: Verify DNS-Based Communication

Let's prove that containers are communicating via DNS (container names), not IP addresses!

### **Test from Inside the API Container**

**Execute a shell inside the API container:**
```bash
docker exec -it task-api /bin/sh
```

**Inside the container, test DNS resolution:**
```sh
# Ping the database by name (DNS)
ping -c 3 task-db

# Check if task-db resolves to an IP
nslookup task-db

# Exit the container
exit
```

**Expected Output:**
```
PING task-db (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=0 ttl=64 time=0.123 ms
64 bytes from 172.18.0.2: seq=1 ttl=64 time=0.089 ms
64 bytes from 172.18.0.2: seq=2 ttl=64 time=0.095 ms

--- task-db ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
```

**What This Proves:**
- ✅ Container name `task-db` resolves to IP `172.18.0.2`
- ✅ Containers can communicate via custom network
- ✅ DNS-based service discovery works perfectly!
- ✅ **Session 6 skill demonstrated!** ✅

---

## Step 5: Monitor Resource Usage

Let's verify our resource limits are working.

### **View Real-Time Stats**

```bash
docker stats task-api task-db
```

**Expected Output:**
```
CONTAINER ID   NAME       CPU %    MEM USAGE / LIMIT   MEM %    NET I/O         BLOCK I/O
c5d6e7f8a9b0   task-api   0.12%    45.2MB / 512MB      8.83%    1.2kB / 856B    0B / 0B
b3c4d5e6f7a8   task-db    0.50%    120MB / 1GB         12.0%    856B / 1.2kB    8.19kB / 0B
```

**Press Ctrl+C to exit.**

**What to Notice:**
- ✅ `task-api` limited to **512 MB** RAM (using ~45 MB)
- ✅ `task-db` limited to **1 GB** RAM (using ~120 MB)
- ✅ CPU usage is low (application is idle)
- ✅ **Session 2 skill: Resource limits** ✅

---

### **View Stats Once (No Streaming)**

```bash
docker stats --no-stream task-api task-db
```

This shows one snapshot instead of continuous updates.

---

## Step 6: Development Workflow with Bind Mounts

For development, we want code changes to reflect immediately without rebuilding the image!

### **Stop the Production Container**

```bash
docker stop task-api
docker rm task-api
```

---

### **Run with Bind Mount (Development Mode)**

**Linux/macOS:**
```bash
docker run -d \
  --name task-api \
  --network task-network \
  -e DB_HOST=task-db \
  -e DB_PORT=5432 \
  -e DB_NAME=taskmanager \
  -e DB_USER=taskuser \
  -e DB_PASSWORD=taskpass123 \
  -e PORT=3000 \
  -p 3000:3000 \
  -v "$(pwd):/app" \
  --cpus="0.5" \
  --memory="512m" \
  task-api:1.0
```

**Windows PowerShell:**
```powershell
docker run -d `
  --name task-api `
  --network task-network `
  -e DB_HOST=task-db `
  -e DB_PORT=5432 `
  -e DB_NAME=taskmanager `
  -e DB_USER=taskuser `
  -e DB_PASSWORD=taskpass123 `
  -e PORT=3000 `
  -p 3000:3000 `
  -v "${PWD}:/app" `
  --cpus="0.5" `
  --memory="512m" `
  task-api:1.0
```

**Windows CMD:**
```cmd
docker run -d ^
  --name task-api ^
  --network task-network ^
  -e DB_HOST=task-db ^
  -e DB_PORT=5432 ^
  -e DB_NAME=taskmanager ^
  -e DB_USER=taskuser ^
  -e DB_PASSWORD=taskpass123 ^
  -e PORT=3000 ^
  -p 3000:3000 ^
  -v "%cd%:/app" ^
  --cpus="0.5" ^
  --memory="512m" ^
  task-api:1.0
```

**New Flag:**
- `-v "$(pwd):/app"`: Bind mount current directory to `/app` in container
- **Session 5**: Bind mounts for development! ✅

---

### **Test Code Hot-Reloading**

**1. Make a change to server.js:**

Edit `server.js` and modify the health check response:

```javascript
// Change this line:
res.json({ status: 'healthy', database: 'connected' });

// To:
res.json({ status: 'healthy', database: 'connected', version: '1.0.1' });
```

**2. Restart the container (to reload code):**

```bash
docker restart task-api
```

**3. Test the change:**

```bash
curl http://localhost:3000/health
```

**Expected Output:**
```json
{"status":"healthy","database":"connected","version":"1.0.1"}
```

✅ **Code changes reflected without rebuilding the image!**

**Bind Mount Workflow:**
- Development: Use bind mounts for instant updates
- Production: Use image (no bind mounts)

---

### **Revert to Production Mode**

Stop and remove the development container:

```bash
docker stop task-api
docker rm task-api
```

Run the production container again (without bind mount):

**Linux/macOS:**
```bash
docker run -d \
  --name task-api \
  --network task-network \
  -e DB_HOST=task-db \
  -e DB_PORT=5432 \
  -e DB_NAME=taskmanager \
  -e DB_USER=taskuser \
  -e DB_PASSWORD=taskpass123 \
  -e PORT=3000 \
  -p 3000:3000 \
  --cpus="0.5" \
  --memory="512m" \
  --restart unless-stopped \
  task-api:1.0
```

(Use PowerShell or CMD variants from Step 2 if on Windows)

---

## Step 7: Verify Data Persistence Across API Restarts

Let's prove that data persists even when the API container restarts!

**1. Create a new task:**
```bash
curl -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Persistence", "description": "This task should survive API restart", "status": "pending"}'
```

**2. Note the task ID (e.g., 6)**

**3. Restart the API container:**
```bash
docker restart task-api
```

**4. Wait 5 seconds, then retrieve the task:**
```bash
curl http://localhost:3000/tasks/6
```

**Expected Output:**
```json
{
  "success": true,
  "data": {
    "id": 6,
    "title": "Test Persistence",
    "description": "This task should survive API restart",
    ...
  }
}
```

✅ **Data persisted!** (Because it's in the PostgreSQL volume, not in the API container!)

---

## Step 8: Test Network Isolation

Let's verify that our containers are properly isolated!

### **Create a Test Container NOT on task-network**

```bash
docker run --rm -it alpine:latest /bin/sh
```

**Inside this container, try to ping task-db:**
```sh
ping task-db
```

**Expected Output:**
```
ping: bad address 'task-db'
```

**Why it fails:**
- ❌ This container is on the **default bridge network**
- ❌ Cannot reach containers on `task-network`
- ✅ **Network isolation is working!**

**Exit the container:**
```sh
exit
```

---

### **Test from a Container ON task-network**

```bash
docker run --rm -it --network task-network alpine:latest /bin/sh
```

**Inside this container:**
```sh
ping -c 3 task-db
ping -c 3 task-api
exit
```

**Expected Output:**
```
PING task-db (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=0 ttl=64 time=0.123 ms
...

PING task-api (172.18.0.3): 56 data bytes
64 bytes from 172.18.0.3: seq=0 ttl=64 time=0.089 ms
...
```

✅ **Containers on the same network can communicate!**

**Session 6 Skills:**
- ✅ Network isolation
- ✅ DNS-based communication
- ✅ Custom bridge networks

---

## Step 9: View Complete System Status

Let's see our complete architecture in action!

### **View All Running Containers**

```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
```

**Expected Output:**
```
NAMES        IMAGE                STATUS         PORTS
task-api     task-api:1.0        Up 5 minutes   0.0.0.0:3000->3000/tcp
task-db      postgres:16-alpine  Up 3 hours     0.0.0.0:5432->5432/tcp
```

---

### **View Network Configuration**

```bash
docker network inspect task-network --format='{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{println}}{{end}}'
```

**Expected Output:**
```
task-api: 172.18.0.3/16
task-db: 172.18.0.2/16
```

---

### **View Volumes**

```bash
docker volume ls | grep task
```

**Expected Output:**
```
local     task-db-data
```

---

## Troubleshooting Common Issues

### **Issue 1: API Can't Connect to Database**

**Symptoms:**
```bash
docker logs task-api
# Shows: Error connecting to database: connection refused
```

**Solutions:**

**1. Verify both containers are on the same network:**
```bash
docker network inspect task-network
```

Both `task-api` and `task-db` should appear in the "Containers" section.

**2. Check database is actually running:**
```bash
docker ps | grep task-db
```

**3. Verify environment variables are correct:**
```bash
docker inspect task-api --format='{{range .Config.Env}}{{println .}}{{end}}' | grep DB_
```

Should show:
```
DB_HOST=task-db
DB_PORT=5432
DB_NAME=taskmanager
DB_USER=taskuser
DB_PASSWORD=taskpass123
```

---

### **Issue 2: Port Already in Use**

**Symptoms:**
```
Error: Bind for 0.0.0.0:3000 failed: port is already allocated
```

**Solutions:**

**1. Check what's using port 3000:**

**Linux/macOS:**
```bash
lsof -i :3000
```

**Windows PowerShell:**
```powershell
Get-NetTCPConnection -LocalPort 3000
```

**2. Use a different port:**
```bash
docker run ... -p 3001:3000 ... task-api:1.0
```

(Then access via `http://localhost:3001`)

---

### **Issue 3: Resource Limits Too Restrictive**

**Symptoms:**
- API is slow or crashes
- `docker stats` shows memory at 100%

**Solution:**

Increase limits:
```bash
docker stop task-api
docker rm task-api

docker run -d --name task-api ... --cpus="1.0" --memory="1g" ... task-api:1.0
```

---

### **Issue 4: Changes Not Reflecting (Bind Mount)**

**Symptoms:**
- Modified code but changes don't appear

**Solutions:**

**1. Verify bind mount is active:**
```bash
docker inspect task-api --format='{{range .Mounts}}{{.Source}} → {{.Destination}}{{println}}{{end}}'
```

Should show: `/full/path/to/task-api → /app`

**2. Restart container:**
```bash
docker restart task-api
```

**3. Check file permissions (Linux):**
```bash
ls -la server.js
```

Ensure the `nodejs` user (UID 1001) can read the files.

---

## Summary: What You've Accomplished

### **Skills Demonstrated**

✅ **Session 2 (Container Management):**
- Ran containers in detached mode
- Set CPU and memory limits
- Configured environment variables
- Monitored resource usage with `docker stats`
- Implemented restart policies

✅ **Session 5 (Data Management):**
- Used bind mounts for development workflow
- Understood when to use bind mounts vs volumes
- Verified data persistence across container lifecycle

✅ **Session 6 (Networking):**
- Connected multiple containers on custom network
- Used DNS-based service discovery (task-db)
- Tested inter-container communication
- Verified network isolation
- Mapped ports for external access

---

### **Complete Application Architecture**

You now have:
- ✅ **2 containers** running and communicating
- ✅ **1 custom network** for isolation
- ✅ **1 persistent volume** for database
- ✅ **Resource limits** for stability
- ✅ **External access** via port mapping
- ✅ **Production-ready** configuration

---

## Next Steps

Your Task Manager application is now **fully functional and production-ready**!

**In Exercise 6e, you'll:**
- Implement automated backup procedures
- Use tmpfs for temporary data
- Apply final security hardening
- Create operational runbooks
- Test disaster recovery
- Document the complete deployment

---

## Quick Reference Commands

```bash
# View running containers
docker ps

# View logs
docker logs task-api
docker logs -f task-api  # Follow mode

# View stats
docker stats --no-stream task-api task-db

# Restart containers
docker restart task-api

# Stop containers
docker stop task-api task-db

# Test API
curl http://localhost:3000/health
curl http://localhost:3000/tasks

# Execute commands in container
docker exec -it task-api /bin/sh
```

---

**Estimated Time for Exercise 6d:** 60-75 minutes
**Recommended Break:** 15 minutes before Exercise 6e

**Total Progress:** Exercise 6a ✅ | 6b ✅ | 6c ✅ | 6d ✅ | 6e ⬜

---

**Next: Exercise 6e - Production Deployment & Operations**

Fantastic work! Your application is alive and working beautifully. Now let's make it production-bulletproof!

---
