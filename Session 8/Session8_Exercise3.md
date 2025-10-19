# Exercise 3: Runtime Security and Container Hardening (2025)

**Session 8: Security & Best Practices**
**Filename:** `Session8_Exercise3.md`

## Objective
- Secure containers at runtime
- Implement security options and capabilities
- Use read-only filesystems
- Apply the principle of least privilege
- Understand container isolation mechanisms

---

## Overview

Building a secure image is only half the battle. **Runtime security ensures containers run with minimal privileges** and maximum isolation. This exercise covers essential runtime hardening techniques.

---

## Part 1: Understanding Container Security Context

### The Container Security Model

```
┌─────────────────────────────────────────┐
│           Host Operating System         │
│  ┌────────────────────────────────────┐ │
│  │  Kernel (Shared by all containers) │ │
│  └────────────────────────────────────┘ │
│                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐│
│  │Container│  │Container│  │Container││
│  │   #1    │  │   #2    │  │   #3    ││
│  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ ││
│  │ │ App │ │  │ │ App │ │  │ │ App │ ││
│  │ └─────┘ │  │ └─────┘ │  │ └─────┘ ││
│  └─────────┘  └─────────┘  └─────────┘│
└─────────────────────────────────────────┘
```

**Security Layers:**
1. **Namespaces** - Isolation (PID, network, mount, etc.)
2. **Cgroups** - Resource limits
3. **Capabilities** - Fine-grained permissions
4. **Seccomp** - System call filtering
5. **AppArmor/SELinux** - Mandatory access control

---

## Part 2: Running as Non-Root (Runtime)

### Step 1: Verify and Enforce Non-Root Execution

**Check if container runs as root:**

```bash
# Run container
docker run -d --name test-app myapp:latest

# Check process user
docker exec test-app id
# Good: uid=1000(appuser) gid=1000(appgroup)
# Bad:  uid=0(root) gid=0(root)

# Check from host
docker top test-app
# Should show non-root user
```

**Enforce non-root at runtime (extra security layer):**

```bash
# Docker will refuse to run if image tries to use root
docker run --user 1000:1000 myapp:latest

# Even better: Use explicit non-root user from image
docker run myapp:latest
# If Dockerfile has USER appuser, this is already non-root
```

---

### Step 2: User Namespace Remapping

**For extra isolation, remap container root to non-root on host:**

1. **Configure Docker daemon** (`/etc/docker/daemon.json`):
   ```json
   {
     "userns-remap": "default"
   }
   ```

2. **Restart Docker:**
   ```bash
   sudo systemctl restart docker
   ```

3. **Now container "root" maps to unprivileged user on host:**
   ```bash
   docker run --rm alpine id
   # Shows uid=0(root) inside container
   # But on host, it's actually uid=100000+
   ```

**Benefits:**
- Container root cannot access host root resources
- Additional layer of defense
- Prevents privilege escalation attacks

---

## Part 3: Dropping Linux Capabilities

### Step 3: Understanding Capabilities

**Linux Capabilities** allow fine-grained privilege control instead of all-or-nothing root access.

**Docker's default capabilities:**
```bash
# View default capabilities
docker run --rm alpine sh -c 'apk add --no-cache libcap && capsh --print'
```

**Common dangerous capabilities to drop:**

| Capability | Risk if Granted |
|------------|----------------|
| `CAP_SYS_ADMIN` | Full system administration |
| `CAP_NET_ADMIN` | Network configuration changes |
| `CAP_SYS_MODULE` | Load kernel modules |
| `CAP_SYS_RAWIO` | Direct I/O operations |
| `CAP_DAC_OVERRIDE` | Bypass file permissions |

**✅ Drop all capabilities, add only what's needed:**

```bash
# Drop ALL capabilities
docker run --rm \
  --cap-drop=ALL \
  alpine sh -c 'echo "Minimal privileges!"'

# Add only specific capabilities if needed
docker run --rm \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  myapp:latest
# Now can bind to port 80, but nothing else
```

**In Docker Compose:**

```yaml
services:
  app:
    image: myapp:latest
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if needed
      - CHOWN             # Only if needed
```

---

### Step 4: Testing Capability Restrictions

**Create test to verify capabilities are dropped:**

```bash
# Try to change system time (requires CAP_SYS_TIME)
docker run --rm \
  --cap-drop=ALL \
  alpine date -s "2025-01-01 00:00:00"
# Should fail: date: can't set date: Operation not permitted

# Try with capability
docker run --rm \
  --cap-drop=ALL \
  --cap-add=SYS_TIME \
  alpine date -s "2025-01-01 00:00:00"
# Should succeed (but don't actually do this!)
```

---

## Part 4: Read-Only Root Filesystem

### Step 5: Implement Read-Only Filesystem

**Why read-only?**
- Prevents malware from writing to filesystem
- Immutable infrastructure principle
- Forces proper volume usage for persistent data

**❌ Without read-only:**
```bash
docker run --rm -it alpine sh -c \
  'echo "malware" > /etc/malicious && cat /etc/malicious'
# Works - attacker can modify filesystem
```

**✅ With read-only:**
```bash
docker run --rm -it \
  --read-only \
  alpine sh -c 'echo "malware" > /etc/malicious'
# Fails: sh: can't create /etc/malicious: Read-only file system
```

---

### Step 6: Read-Only with Temporary Writable Volumes

**Most apps need some writable space. Use tmpfs:**

```bash
docker run -d \
  --name app-readonly \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=100m \
  --tmpfs /var/run:rw,noexec,nosuid,size=50m \
  myapp:latest
```

**Explanation:**
- `--read-only` - Root filesystem is read-only
- `--tmpfs /tmp` - Temporary writable space
- `noexec` - Cannot execute binaries from tmpfs
- `nosuid` - Cannot use setuid
- `size=100m` - Limit tmpfs size

**In Docker Compose:**

```yaml
services:
  app:
    image: myapp:latest
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=100m
      - /var/run:rw,noexec,nosuid,size=50m
```

---

### Step 7: Testing Read-Only Filesystem

**Create a Node.js app that respects read-only:**

```javascript
// server.js
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Use /tmp for writable data (mounted as tmpfs)
const TMP_DIR = '/tmp/app-data';

// Create tmp directory if doesn't exist
if (!fs.existsSync(TMP_DIR)) {
  fs.mkdirSync(TMP_DIR, { recursive: true });
}

app.get('/', (req, res) => {
  res.json({ message: 'Read-only filesystem demo' });
});

app.post('/write', (req, res) => {
  try {
    // This works - writing to tmpfs
    fs.writeFileSync(path.join(TMP_DIR, 'test.txt'), 'data');
    res.json({ success: true, message: 'Written to /tmp' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => console.log(`Server on port ${PORT}`));
```

**Run with read-only:**
```bash
docker run -d -p 3000:3000 \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid \
  myapp:readonly

# Test write endpoint
curl -X POST http://localhost:3000/write
# Should succeed (writing to /tmp tmpfs)
```

---

## Part 5: Security Options (Seccomp, AppArmor)

### Step 8: Seccomp Profiles

**Seccomp** filters system calls to reduce attack surface.

**Docker's default seccomp profile** blocks ~44 dangerous syscalls.

**View default profile:**
```bash
docker run --rm -it \
  --security-opt seccomp=unconfined \
  alpine sh
# Dangerous! Allows all syscalls
```

**✅ Use default seccomp (recommended):**
```bash
docker run --rm -it alpine sh
# Uses default Docker seccomp profile (secure)
```

**Custom seccomp profile** (advanced):

Create `seccomp-profile.json`:
```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": ["read", "write", "open", "close", "stat", "fstat"],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

**Apply custom profile:**
```bash
docker run --rm \
  --security-opt seccomp=./seccomp-profile.json \
  alpine sh
# Only allows specified syscalls
```

---

### Step 9: AppArmor/SELinux

**On Ubuntu/Debian (AppArmor):**

```bash
# Check if AppArmor is active
docker run --rm alpine sh -c \
  'cat /proc/self/attr/current 2>/dev/null || echo "Not available"'

# Load custom AppArmor profile
docker run --rm \
  --security-opt apparmor=docker-default \
  alpine sh
```

**On RHEL/CentOS (SELinux):**

```bash
# Use SELinux label
docker run --rm \
  --security-opt label=type:container_runtime_t \
  alpine sh
```

**In Docker Compose:**
```yaml
services:
  app:
    image: myapp:latest
    security_opt:
      - apparmor:docker-default
      - no-new-privileges:true
```

---

## Part 6: No New Privileges

### Step 10: Prevent Privilege Escalation

**The `no-new-privileges` flag** prevents processes from gaining additional privileges:

```bash
# Without flag - setuid binaries can escalate
docker run --rm -it alpine sh

# With flag - setuid binaries cannot escalate
docker run --rm -it \
  --security-opt no-new-privileges:true \
  alpine sh
```

**Why this matters:**
- Prevents setuid/setgid exploits
- Stops privilege escalation attacks
- Defense in depth

**In Docker Compose:**
```yaml
services:
  app:
    image: myapp:latest
    security_opt:
      - no-new-privileges:true
```

---

## Part 7: Network Security

### Step 11: Network Isolation

**Disable network entirely if not needed:**

```bash
docker run --rm \
  --network none \
  myapp:batch-job
# No network access at all
```

**Use custom networks for isolation:**

```bash
# Create isolated network
docker network create --driver bridge isolated-net

# Run containers on isolated network
docker run -d --name app1 --network isolated-net myapp:v1
docker run -d --name app2 --network isolated-net myapp:v2

# These can communicate with each other but not external
```

**Restrict outbound connections with firewall rules** (advanced):

```yaml
services:
  app:
    image: myapp:latest
    networks:
      - backend
    dns:
      - 1.1.1.1  # Only allow specific DNS
    extra_hosts:
      - "api.example.com:10.0.0.5"  # Only specific hosts
```

---

## Part 8: Resource Limits (Security Perspective)

### Step 12: Prevent Resource Exhaustion Attacks

**CPU limits:**
```bash
docker run -d \
  --cpus="0.5" \
  --cpu-shares=512 \
  myapp:latest
# Limits CPU usage to prevent DoS
```

**Memory limits:**
```bash
docker run -d \
  --memory="512m" \
  --memory-reservation="256m" \
  --memory-swap="1g" \
  --oom-kill-disable=false \
  myapp:latest
# Prevents memory exhaustion attacks
```

**PIDs limit:**
```bash
docker run -d \
  --pids-limit=100 \
  myapp:latest
# Prevents fork bombs
```

**In Docker Compose:**
```yaml
services:
  app:
    image: myapp:latest
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
          pids: 100
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

## Part 9: Complete Hardened Container

### Step 13: Production-Ready Hardened Configuration

**Docker Compose with all security features:**

```yaml
services:
  app:
    image: myapp:distroless

    # User security
    user: "65532:65532"  # nonroot UID:GID

    # Filesystem security
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=100m

    # Capability restrictions
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to port <1024

    # Security options
    security_opt:
      - no-new-privileges:true
      - apparmor:docker-default

    # Resource limits (prevent DoS)
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
          pids: 50
        reservations:
          cpus: '0.5'
          memory: 256M

    # Network security
    networks:
      - backend

    # Health monitoring
    healthcheck:
      test: ["CMD", "node", "healthcheck.js"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

    # Restart policy
    restart: unless-stopped

    # Logging limits
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  backend:
    driver: bridge
    internal: true  # No external access
```

**Start hardened stack:**
```bash
docker compose up -d

# Verify security settings
docker inspect app | grep -i "security\|cap\|user"
```

---

## Part 10: Security Testing and Validation

### Step 14: Automated Security Testing

**Create security test script** `test-security.sh`:

```bash
#!/bin/bash

set -e

CONTAINER_NAME="security-test"
IMAGE_NAME="myapp:latest"

echo "🔒 Running Container Security Tests..."
echo ""

# Test 1: Non-root user
echo "Test 1: Checking if running as non-root..."
USER_ID=$(docker run --rm $IMAGE_NAME id -u)
if [ "$USER_ID" -eq "0" ]; then
    echo "❌ FAIL: Container running as root (UID 0)"
    exit 1
else
    echo "✅ PASS: Running as UID $USER_ID (non-root)"
fi

# Test 2: Read-only filesystem
echo ""
echo "Test 2: Checking read-only filesystem..."
docker run --rm --read-only $IMAGE_NAME \
    sh -c 'touch /test 2>/dev/null && echo "WRITABLE" || echo "READ-ONLY"' | \
    grep -q "READ-ONLY" && \
    echo "✅ PASS: Filesystem is read-only" || \
    echo "❌ FAIL: Filesystem is writable"

# Test 3: No dangerous capabilities
echo ""
echo "Test 3: Checking capabilities..."
CAPS=$(docker run --rm --cap-drop=ALL $IMAGE_NAME \
    sh -c 'cat /proc/self/status | grep CapEff')
echo "Effective capabilities: $CAPS"
echo "✅ INFO: Review capabilities above"

# Test 4: Image scan
echo ""
echo "Test 4: Scanning image for CVEs..."
CRITICAL=$(docker scout cves $IMAGE_NAME 2>&1 | \
    grep -i "critical" | grep -oE '[0-9]+' | head -1 || echo "0")
HIGH=$(docker scout cves $IMAGE_NAME 2>&1 | \
    grep -i "high" | grep -oE '[0-9]+' | head -1 || echo "0")

if [ "$CRITICAL" -gt "0" ]; then
    echo "❌ FAIL: $CRITICAL Critical CVEs found"
    exit 1
elif [ "$HIGH" -gt "5" ]; then
    echo "⚠️  WARNING: $HIGH High CVEs found"
else
    echo "✅ PASS: No Critical CVEs, $HIGH High CVEs"
fi

echo ""
echo "🎉 Security tests completed!"
```

**Run tests:**
```bash
chmod +x test-security.sh
./test-security.sh
```

---

## Expected Outcomes

After completing this exercise, you should:

✅ Understand container isolation mechanisms
✅ Drop unnecessary Linux capabilities
✅ Implement read-only root filesystems
✅ Configure seccomp and AppArmor profiles
✅ Prevent privilege escalation
✅ Apply defense-in-depth security
✅ Test and validate container security

---

## Security Hardening Checklist

```markdown
## Runtime Security Checklist

### User & Permissions
- [ ] Container runs as non-root user
- [ ] User namespace remapping enabled (if applicable)
- [ ] No-new-privileges flag set

### Capabilities
- [ ] All capabilities dropped (--cap-drop=ALL)
- [ ] Only necessary capabilities added back
- [ ] No CAP_SYS_ADMIN granted

### Filesystem
- [ ] Read-only root filesystem enabled
- [ ] Tmpfs mounted for writable needs
- [ ] Tmpfs has noexec and nosuid flags

### Security Options
- [ ] Default seccomp profile active
- [ ] AppArmor/SELinux profile loaded
- [ ] No privileged mode

### Resources
- [ ] CPU limits configured
- [ ] Memory limits configured
- [ ] PIDs limit set
- [ ] Prevents resource exhaustion

### Network
- [ ] Minimal network exposure
- [ ] Custom networks for isolation
- [ ] No unnecessary ports published

### Monitoring
- [ ] Health checks configured
- [ ] Logging with rotation
- [ ] Restart policy set
```

---

## Challenge Exercise

**Create a maximally hardened container:**

**Requirements:**
1. Non-root user (UID > 1000)
2. Read-only filesystem
3. All capabilities dropped
4. No-new-privileges enabled
5. Resource limits set
6. Passes all security tests
7. Application still functions correctly

**Test with:**
```bash
./test-security.sh
docker scout cves myapp:hardened
```

---

## Additional Resources

- [Docker Security Documentation](https://docs.docker.com/engine/security/)
- [Linux Capabilities Man Page](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [Seccomp Documentation](https://docs.docker.com/engine/security/seccomp/)
- [AppArmor Docker Profile](https://docs.docker.com/engine/security/apparmor/)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)

---

**Next:** Exercise 4 - Secrets Management in Docker Compose
