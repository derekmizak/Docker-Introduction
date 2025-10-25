# Exercise 6b: Database Setup & Data Persistence

**Filename:** `Session6_Exercise6b.md`

---

## Overview

In this exercise, you'll set up the foundation of your Task Manager application: a **PostgreSQL database container** with **persistent storage** and **network isolation**.

### **What You'll Build**

```
┌─────────────────────────────────────┐
│     Custom Network: task-network    │
│                                     │
│   ┌─────────────────────────────┐  │
│   │  Container: task-db         │  │
│   │  Image: postgres:16-alpine  │  │
│   │  Port: 5432                 │  │
│   │                             │  │
│   │  Volume: task-db-data       │  │
│   │  → /var/lib/postgresql/data │  │
│   └─────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## Learning Objectives

By completing this exercise, you will:

### **Session 1 Skills (Fundamentals)**
- ✅ Run containers from Docker Hub images
- ✅ Manage container lifecycle (run, stop, start, rm)
- ✅ Use environment variables for configuration

### **Session 5 Skills (Data Management)**
- ✅ Create and manage named volumes
- ✅ Mount volumes to containers for data persistence
- ✅ Verify data survives container restarts and recreation
- ✅ Inspect volume configuration and location

### **Session 6 Skills (Networking)**
- ✅ Create custom bridge networks
- ✅ Connect containers to specific networks
- ✅ Understand network isolation
- ✅ Inspect network configuration

---

## Prerequisites

Before starting, ensure:
- ✅ You've completed Exercise 6a (Introduction)
- ✅ Docker Desktop is running
- ✅ You're in your working directory (`docker-capstone` or similar)
- ✅ Terminal/PowerShell is open

---

## Step 1: Create a Custom Bridge Network

### **Why Custom Networks?**

Before we create the network, let's understand **why** we need one:

**Default Bridge Network:**
- Containers can only communicate by IP address
- No automatic DNS resolution between containers
- Not recommended for production

**Custom Bridge Network:**
- ✅ Containers can communicate using **container names** (DNS)
- ✅ Better network isolation from other containers
- ✅ Production-ready approach
- ✅ Industry best practice

**Example:**
```bash
# On default bridge: Must use IP (fragile, changes every restart)
psql -h 172.17.0.2 -U postgres

# On custom bridge: Use container name (reliable, DNS-based)
psql -h task-db -U postgres  # ✅ Much better!
```

### **Create the Network**

Run this command on **any platform** (Windows PowerShell/CMD/Git Bash, macOS, Linux):

```bash
docker network create task-network
```

**What This Command Does:**
- Creates a new custom bridge network named `task-network`
- Enables automatic DNS resolution for containers on this network
- Isolates containers on this network from others
- Uses Docker's default bridge driver

**Expected Output:**
```
a7f3c9e1b2d4f5a6c7b8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9
```
(A long hash indicating the network was created successfully)

---

### **Verify Network Creation**

List all networks:

```bash
docker network ls
```

**Expected Output:**
```
NETWORK ID     NAME           DRIVER    SCOPE
a7f3c9e1b2d4   task-network   bridge    local
xxxxxxxxxxxx   bridge         bridge    local
xxxxxxxxxxxx   host           host      local
xxxxxxxxxxxx   none           null      local
```

**What You're Seeing:**
- `task-network`: Your custom network (you just created this!)
- `bridge`: Docker's default network
- `host`: Network with no isolation (rarely used)
- `none`: Network with no connectivity

---

### **Inspect the Network**

Get detailed information about your network:

```bash
docker network inspect task-network
```

**Expected Output (abbreviated):**
```json
[
    {
        "Name": "task-network",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Containers": {}
    }
]
```

**Key Fields to Notice:**
- `"Name": "task-network"`: Your network name
- `"Driver": "bridge"`: Using bridge networking (isolated, but containers can communicate)
- `"Containers": {}`: Empty right now (we'll add containers soon!)
- `"Subnet"`: Docker assigned an IP range (you don't need to memorize this)

---

## Step 2: Create a Named Volume for Database Data

### **Why Named Volumes?**

**Without Volume:**
- Database data stored inside container filesystem
- ❌ Data **lost** when container is deleted
- ❌ Can't share data between containers
- ❌ Not production-ready

**With Named Volume:**
- ✅ Data persists even if container is deleted
- ✅ Can be backed up independently
- ✅ Can be shared across containers
- ✅ Managed by Docker (optimal performance)
- ✅ Production-ready

### **Create the Volume**

Run this command on **any platform**:

```bash
docker volume create task-db-data
```

**What This Command Does:**
- Creates a named volume called `task-db-data`
- Docker manages the storage location (different per platform)
- Volume is empty initially
- Persists until explicitly deleted

**Expected Output:**
```
task-db-data
```
(Simple confirmation of the volume name)

---

### **Verify Volume Creation**

List all volumes:

```bash
docker volume ls
```

**Expected Output:**
```
DRIVER    VOLUME NAME
local     task-db-data
```

---

### **Inspect the Volume**

Get detailed information:

```bash
docker volume inspect task-db-data
```

**Expected Output:**
```json
[
    {
        "CreatedAt": "2025-10-25T10:30:00Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/task-db-data/_data",
        "Name": "task-db-data",
        "Options": null,
        "Scope": "local"
    }
]
```

**Platform-Specific Notes:**

**Linux:**
- `Mountpoint` is directly accessible at `/var/lib/docker/volumes/task-db-data/_data`
- Can use `sudo ls` to view contents

**macOS/Windows (Docker Desktop):**
- `Mountpoint` is inside Docker's Linux VM
- **NOT directly accessible** from host Terminal/PowerShell
- Must use containers to access data (see Exercise 6e for how)

---

## Step 3: Run PostgreSQL Container

Now we'll run the PostgreSQL container with **all the configurations** we've prepared.

### **Understanding the Command**

We'll use a complex `docker run` command. Let's break it down piece by piece before running it:

```bash
docker run -d \
  --name task-db \
  --network task-network \
  -e POSTGRES_DB=taskmanager \
  -e POSTGRES_USER=taskuser \
  -e POSTGRES_PASSWORD=taskpass123 \
  -v task-db-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16-alpine
```

**Flag-by-Flag Explanation:**

| Flag | Explanation | Session |
|------|-------------|---------|
| `-d` | **Detached mode** - Run in background | Session 2 |
| `--name task-db` | **Container name** - Call it "task-db" for easy reference | Session 2 |
| `--network task-network` | **Custom network** - Connect to our isolated network | Session 6 |
| `-e POSTGRES_DB=taskmanager` | **Environment variable** - Create database named "taskmanager" | Session 2 |
| `-e POSTGRES_USER=taskuser` | **Environment variable** - Create user "taskuser" | Session 2 |
| `-e POSTGRES_PASSWORD=taskpass123` | **Environment variable** - Set password (production: use secrets!) | Session 2 |
| `-v task-db-data:/var/lib/postgresql/data` | **Volume mount** - Persist data in our named volume | Session 5 |
| `-p 5432:5432` | **Port mapping** - Map host:container for external access | Session 1 |
| `postgres:16-alpine` | **Image** - PostgreSQL 16 on Alpine Linux (small, efficient) | Session 3 |

---

### **Run the Command**

**For Linux/macOS (Terminal):**
```bash
docker run -d \
  --name task-db \
  --network task-network \
  -e POSTGRES_DB=taskmanager \
  -e POSTGRES_USER=taskuser \
  -e POSTGRES_PASSWORD=taskpass123 \
  -v task-db-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16-alpine
```

**For Windows PowerShell:**
```powershell
docker run -d `
  --name task-db `
  --network task-network `
  -e POSTGRES_DB=taskmanager `
  -e POSTGRES_USER=taskuser `
  -e POSTGRES_PASSWORD=taskpass123 `
  -v task-db-data:/var/lib/postgresql/data `
  -p 5432:5432 `
  postgres:16-alpine
```

**For Windows CMD:**
```cmd
docker run -d ^
  --name task-db ^
  --network task-network ^
  -e POSTGRES_DB=taskmanager ^
  -e POSTGRES_USER=taskuser ^
  -e POSTGRES_PASSWORD=taskpass123 ^
  -v task-db-data:/var/lib/postgresql/data ^
  -p 5432:5432 ^
  postgres:16-alpine
```

**Note the Line Continuation Characters:**
- Linux/macOS/Git Bash: `\` (backslash)
- PowerShell: `` ` `` (backtick)
- CMD: `^` (caret)

---

### **What Happens When You Run This**

1. **Image Pull** (if not already present):
   ```
   Unable to find image 'postgres:16-alpine' locally
   16-alpine: Pulling from library/postgres
   ...
   Status: Downloaded newer image for postgres:16-alpine
   ```

2. **Container Creation**:
   - Docker creates container named `task-db`
   - Connects it to `task-network`
   - Sets up environment variables
   - Mounts volume to `/var/lib/postgresql/data`
   - Maps port 5432

3. **PostgreSQL Initialization**:
   - Creates database `taskmanager`
   - Creates user `taskuser` with password `taskpass123`
   - Initializes data directory in volume

4. **Output**:
   ```
   b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3
   ```
   (Container ID hash)

---

### **Verify Container is Running**

```bash
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE                 COMMAND                  CREATED         STATUS         PORTS                    NAMES
b3c4d5e6f7a8   postgres:16-alpine   "docker-entrypoint.s…"   10 seconds ago  Up 8 seconds   0.0.0.0:5432->5432/tcp   task-db
```

**What to Verify:**
- ✅ `STATUS`: Should be "Up" (if "Exited", there's an error)
- ✅ `PORTS`: Should show `0.0.0.0:5432->5432/tcp`
- ✅ `NAMES`: Should be `task-db`

---

### **Check Container Logs**

View the startup logs to confirm PostgreSQL initialized successfully:

```bash
docker logs task-db
```

**Expected Output (last few lines):**
```
...
PostgreSQL init process complete; ready for start up.

2025-10-25 10:35:00.123 UTC [1] LOG:  starting PostgreSQL 16.0 on x86_64-pc-linux-musl
2025-10-25 10:35:00.456 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2025-10-25 10:35:00.789 UTC [1] LOG:  database system is ready to accept connections
```

**Key Messages to Look For:**
- ✅ `PostgreSQL init process complete`
- ✅ `database system is ready to accept connections`
- ✅ `listening on IPv4 address "0.0.0.0", port 5432`

If you see these messages, PostgreSQL is running successfully!

---

## Step 4: Verify Network Connection

Let's verify the container is connected to our custom network.

### **Inspect the Network Again**

```bash
docker network inspect task-network
```

**Look for the "Containers" section:**
```json
"Containers": {
    "b3c4d5e6f7a8...": {
        "Name": "task-db",
        "EndpointID": "a1b2c3d4e5f6...",
        "MacAddress": "02:42:ac:12:00:02",
        "IPv4Address": "172.18.0.2/16",
        "IPv6Address": ""
    }
}
```

**What This Shows:**
- ✅ Container `task-db` is connected to `task-network`
- ✅ Docker assigned an IP address (e.g., `172.18.0.2`)
- ✅ DNS name `task-db` will resolve to this container

**Important Concept:**
Other containers on `task-network` can reach this database using either:
- **Container name (DNS)**: `task-db` ✅ **Recommended**
- **IP address**: `172.18.0.2` ❌ Not recommended (can change)

---

## Step 5: Test Database Connectivity

Now let's verify we can actually connect to the database!

### **Method 1: Using psql Inside the Container**

We'll use PostgreSQL's command-line client (`psql`) that's already installed inside the container.

**Run psql interactively:**

```bash
docker exec -it task-db psql -U taskuser -d taskmanager
```

**Command Breakdown:**
- `docker exec`: Execute a command in a running container
- `-it`: Interactive terminal mode
- `task-db`: Container name
- `psql`: PostgreSQL client program
- `-U taskuser`: Connect as user "taskuser"
- `-d taskmanager`: Connect to database "taskmanager"

**Expected Output:**
```
psql (16.0)
Type "help" for help.

taskmanager=#
```

You're now inside the PostgreSQL interactive shell!

---

### **Run Test Commands**

Try these SQL commands:

**1. List all databases:**
```sql
\l
```

**Expected Output:**
```
                                                      List of databases
    Name     |  Owner   | Encoding | Locale Provider |   Collate   |    Ctype    | ICU Locale | Access privileges
-------------+----------+----------+-----------------+-------------+-------------+------------+-------------------
 postgres    | taskuser | UTF8     | libc            | en_US.utf8  | en_US.utf8  |            |
 taskmanager | taskuser | UTF8     | libc            | en_US.utf8  | en_US.utf8  |            |
```

You should see `taskmanager` database! ✅

**2. List all tables (should be empty for now):**
```sql
\dt
```

**Expected Output:**
```
Did not find any relations.
```

This is correct - we haven't created any tables yet!

**3. Create a test table:**
```sql
CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    message TEXT
);
```

**Expected Output:**
```
CREATE TABLE
```

**4. Insert test data:**
```sql
INSERT INTO test_table (message) VALUES ('Hello from PostgreSQL!');
```

**Expected Output:**
```
INSERT 0 1
```

**5. Query the data:**
```sql
SELECT * FROM test_table;
```

**Expected Output:**
```
 id |        message
----+-------------------------
  1 | Hello from PostgreSQL!
(1 row)
```

Perfect! The database is working! ✅

**6. Exit psql:**
```sql
\q
```

You're back at your terminal prompt.

---

### **Method 2: Using psql from Host (Alternative)**

If you have PostgreSQL client installed on your host machine, you can connect directly:

**Linux/macOS:**
```bash
psql -h localhost -p 5432 -U taskuser -d taskmanager
```

**Windows PowerShell (if you have psql installed):**
```powershell
psql -h localhost -p 5432 -U taskuser -d taskmanager
```

**When prompted, enter password:** `taskpass123`

**Note:** This method requires PostgreSQL client installed on your host. If you don't have it, Method 1 (using `docker exec`) always works!

---

## Step 6: Verify Data Persistence

This is the **critical test**: Does our data survive container restarts and recreation?

### **Test 1: Survive Container Stop/Start**

**Stop the container:**
```bash
docker stop task-db
```

**Verify it stopped:**
```bash
docker ps -a
```

You should see `task-db` with status `Exited`.

**Start the container again:**
```bash
docker start task-db
```

**Wait a few seconds for PostgreSQL to start, then check the test data:**
```bash
docker exec -it task-db psql -U taskuser -d taskmanager -c "SELECT * FROM test_table;"
```

**Expected Output:**
```
 id |        message
----+-------------------------
  1 | Hello from PostgreSQL!
(1 row)
```

✅ **Success!** Data survived stop/start!

---

### **Test 2: Survive Container Deletion (The Ultimate Test)**

This is the real test - can data survive complete container destruction?

**1. Stop and remove the container:**
```bash
docker stop task-db
docker rm task-db
```

**2. Verify container is gone:**
```bash
docker ps -a
```

`task-db` should not appear in the list.

**3. Verify volume still exists:**
```bash
docker volume ls
```

You should see `task-db-data` - the volume persists even though container is gone! ✅

**4. Create a new container with the same volume:**

**Linux/macOS:**
```bash
docker run -d \
  --name task-db \
  --network task-network \
  -e POSTGRES_DB=taskmanager \
  -e POSTGRES_USER=taskuser \
  -e POSTGRES_PASSWORD=taskpass123 \
  -v task-db-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16-alpine
```

**Windows PowerShell:**
```powershell
docker run -d `
  --name task-db `
  --network task-network `
  -e POSTGRES_DB=taskmanager `
  -e POSTGRES_USER=taskuser `
  -e POSTGRES_PASSWORD=taskpass123 `
  -v task-db-data:/var/lib/postgresql/data `
  -p 5432:5432 `
  postgres:16-alpine
```

**5. Wait a few seconds, then check if our test data is still there:**

```bash
docker exec -it task-db psql -U taskuser -d taskmanager -c "SELECT * FROM test_table;"
```

**Expected Output:**
```
 id |        message
----+-------------------------
  1 | Hello from PostgreSQL!
(1 row)
```

✅ **Amazing!** Data survived complete container deletion and recreation!

**What Just Happened:**
- We completely destroyed the container
- Created a brand new container from scratch
- PostgreSQL reused the existing data in the volume
- All our data was preserved perfectly

This is the **power of Docker volumes**! 🎉

---

## Step 7: Clean Up Test Data

Now that we've verified persistence, let's clean up our test table to prepare for the real application.

**Drop the test table:**
```bash
docker exec -it task-db psql -U taskuser -d taskmanager -c "DROP TABLE test_table;"
```

**Expected Output:**
```
DROP TABLE
```

**Verify it's gone:**
```bash
docker exec -it task-db psql -U taskuser -d taskmanager -c "\dt"
```

**Expected Output:**
```
Did not find any relations.
```

Perfect! Database is clean and ready for our application.

---

## Step 8: Understanding What You've Built

Let's review what you now have running:

### **Infrastructure Components**

**1. Custom Network: `task-network`**
```bash
docker network ls | grep task-network
```
- Provides isolated networking
- Enables DNS-based container communication
- Production-ready setup

**2. Named Volume: `task-db-data`**
```bash
docker volume ls | grep task-db-data
```
- Stores PostgreSQL data persistently
- Survives container lifecycle
- Can be backed up independently

**3. PostgreSQL Container: `task-db`**
```bash
docker ps | grep task-db
```
- Running PostgreSQL 16 on Alpine Linux
- Connected to `task-network`
- Data stored in `task-db-data` volume
- Accessible on port 5432
- Ready for application connections

---

### **Architecture Diagram (Current State)**

```
┌──────────────────────────────────────────────────────┐
│                   Host Machine                       │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │  Docker Network: task-network                  │ │
│  │  Subnet: 172.18.0.0/16 (Docker assigned)       │ │
│  │                                                 │ │
│  │  ┌──────────────────────────────────────────┐  │ │
│  │  │  Container: task-db                      │  │ │
│  │  │  Image: postgres:16-alpine               │  │ │
│  │  │  Status: Up                              │  │ │
│  │  │  DNS Name: task-db                       │  │ │
│  │  │                                          │  │ │
│  │  │  Environment:                            │  │ │
│  │  │  - POSTGRES_DB=taskmanager               │  │ │
│  │  │  - POSTGRES_USER=taskuser                │  │ │
│  │  │  - POSTGRES_PASSWORD=taskpass123         │  │ │
│  │  │                                          │  │ │
│  │  │  Volume Mount:                           │  │ │
│  │  │  task-db-data → /var/lib/postgresql/data │  │ │
│  │  │                                          │  │ │
│  │  │  Port: 5432 (accessible from host)       │  │ │
│  │  └──────────────────────────────────────────┘  │ │
│  │                                                 │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │  Volume: task-db-data                          │ │
│  │  Driver: local                                 │ │
│  │  Contains: PostgreSQL database files           │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## Step 9: Inspection and Verification Commands

Here are useful commands to inspect your setup:

### **Container Information**

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# Detailed container info
docker inspect task-db

# View container logs
docker logs task-db

# View last 20 log lines
docker logs --tail 20 task-db

# Follow logs in real-time
docker logs -f task-db
```

### **Network Information**

```bash
# List networks
docker network ls

# Inspect task-network
docker network inspect task-network

# See which containers are on task-network
docker network inspect task-network --format='{{range .Containers}}{{.Name}} {{end}}'
```

### **Volume Information**

```bash
# List volumes
docker volume ls

# Inspect task-db-data
docker volume inspect task-db-data

# See volume size (Linux only - requires jq)
docker system df -v | grep task-db-data
```

### **Resource Usage**

```bash
# View real-time stats
docker stats task-db

# View stats once (no streaming)
docker stats --no-stream task-db
```

---

## Troubleshooting Common Issues

### **Issue 1: Container Exits Immediately**

**Symptoms:**
```bash
docker ps  # task-db not shown
docker ps -a  # task-db shows "Exited (1)"
```

**Solution:**
Check logs for errors:
```bash
docker logs task-db
```

Common causes:
- Port 5432 already in use (another PostgreSQL running?)
- Permission issues with volume
- Invalid environment variables

**Fix port conflict:**
```bash
# Stop any other PostgreSQL instances
docker stop $(docker ps -aq --filter ancestor=postgres)

# Or use a different port
docker run -d --name task-db ... -p 5433:5432 postgres:16-alpine
```

---

### **Issue 2: Can't Connect to Database**

**Symptoms:**
```bash
docker exec -it task-db psql -U taskuser -d taskmanager
# Error: psql: error: connection to server ... failed
```

**Solution:**
1. Check if container is running:
   ```bash
   docker ps | grep task-db
   ```

2. Check logs for startup errors:
   ```bash
   docker logs task-db
   ```

3. Wait longer (PostgreSQL takes 5-10 seconds to start):
   ```bash
   sleep 10
   docker exec -it task-db psql -U taskuser -d taskmanager
   ```

---

### **Issue 3: Data Not Persisting**

**Symptoms:**
Data disappears after container restart.

**Solution:**
Verify volume is mounted correctly:
```bash
docker inspect task-db --format='{{range .Mounts}}{{.Name}} → {{.Destination}}{{end}}'
```

Should show: `task-db-data → /var/lib/postgresql/data`

If wrong, recreate container with correct `-v` flag.

---

### **Issue 4: Network Connection Issues**

**Symptoms:**
Container not reachable by name from other containers.

**Solution:**
Verify container is on correct network:
```bash
docker inspect task-db --format='{{range .NetworkSettings.Networks}}{{.NetworkID}}{{end}}'
```

Reconnect to network if needed:
```bash
docker network connect task-network task-db
```

---

## Platform-Specific Notes

### **Windows Users**

**Line Endings:**
- If creating SQL files on Windows, use **LF** (not CRLF)
- Configure your editor (VS Code, Notepad++) to use Unix line endings

**PowerShell Commands:**
- Use backtick `` ` `` for line continuation (not `\`)
- Some commands may require quotes around volume names

**Path Issues:**
- Always use forward slashes `/` in container paths
- Works identically: `-v task-db-data:/var/lib/postgresql/data`

### **macOS Users**

**Apple Silicon (M1/M2/M3):**
- PostgreSQL images are multi-arch (works on ARM64)
- No special configuration needed
- Performance is excellent on Apple Silicon

**Volume Access:**
- Cannot directly access `/var/lib/docker/volumes/` (in VM)
- Use temporary containers to inspect volumes (Exercise 6e)

### **Linux Users**

**Direct Volume Access:**
- Can access volumes at `/var/lib/docker/volumes/task-db-data/_data`
- Requires `sudo` permissions

**Example:**
```bash
sudo ls -la /var/lib/docker/volumes/task-db-data/_data
```

---

## Summary: What You've Accomplished

### **Skills Demonstrated**

✅ **Session 1 (Fundamentals):**
- Ran PostgreSQL container from Docker Hub
- Managed container lifecycle
- Used environment variables for configuration

✅ **Session 5 (Data Management):**
- Created named volume for persistence
- Mounted volume to container
- Verified data survives container deletion
- Understood platform-specific volume differences

✅ **Session 6 (Networking):**
- Created custom bridge network
- Connected container to network
- Enabled DNS-based communication
- Inspected network configuration

---

### **Production-Ready Features Implemented**

✅ **Data Persistence:** Volume ensures no data loss
✅ **Network Isolation:** Custom network separates from other containers
✅ **DNS Resolution:** Container accessible by name (`task-db`)
✅ **Configuration:** Environment variables for database setup
✅ **Accessibility:** Port mapping allows external connections

---

## Next Steps

You now have a fully functional, persistent PostgreSQL database ready for your application!

**In Exercise 6c, you'll:**
- Create a Node.js Task Manager API
- Write an optimized multi-stage Dockerfile
- Use BuildKit cache mounts
- Scan for vulnerabilities with Docker Scout
- Build a production-ready application image

---

## Quick Reference Commands

```bash
# Start database
docker start task-db

# Stop database
docker stop task-db

# View logs
docker logs task-db

# Connect to database
docker exec -it task-db psql -U taskuser -d taskmanager

# Check if running
docker ps | grep task-db

# View stats
docker stats task-db --no-stream
```

---

**Estimated Time for Exercise 6b:** 45-60 minutes
**Recommended Break:** 10 minutes before Exercise 6c

**Total Progress:** Exercise 6a ✅ | 6b ✅ | 6c ⬜ | 6d ⬜ | 6e ⬜

---

**Next: Exercise 6c - Building the Application Image**

Great work! You've built a solid foundation. Now let's create the application that will use this database!

---
