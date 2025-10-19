# Exercise 4: Using tmpfs Mounts for Temporary Data (2025)

**Session 5: Data Management with Volumes**
**Filename:** `Session5_Exercise4.md`

## Objective
- Understand tmpfs mounts and when to use them
- Implement tmpfs for temporary and sensitive data
- Compare performance of different mount types
- Use tmpfs in production scenarios

---

## What is tmpfs?

**tmpfs** (temporary filesystem) stores data in the host's memory (RAM), not on disk.

**Key characteristics:**
- ⚡ **Fastest** - Stored in RAM, not disk
- 🔒 **Secure** - Data never touches disk (good for secrets)
- ⏱️ **Temporary** - Data lost when container stops
- 💾 **Limited** - Size limited by available RAM

---

## Part 1: Understanding Mount Types

### Comparison Table

| Mount Type | Storage | Persistence | Speed | Use Case |
|------------|---------|-------------|-------|----------|
| **Named Volume** | Docker-managed | ✅ Persistent | Fast | Databases, app data |
| **Bind Mount** | Host filesystem | ✅ Persistent | Fast | Development, config files |
| **tmpfs** | RAM | ❌ Temporary | ⚡ Fastest | Temp files, sensitive data |

---

## Part 2: Basic tmpfs Usage

### Step 1: Run Container with tmpfs

**Simple tmpfs mount:**

```bash
docker run -d \
  --name tmpfs-test \
  --tmpfs /tmp:rw,size=100m \
  alpine sleep 3600
```

**Parameters explained:**
- `--tmpfs /tmp` - Mount tmpfs at /tmp
- `rw` - Read-write access
- `size=100m` - Limit to 100MB

**Verify tmpfs is mounted:**

```bash
# Exec into container
docker exec -it tmpfs-test sh

# Check mount type
df -h | grep tmpfs

# Should show something like:
# tmpfs         100.0M      0    100.0M   0% /tmp
```

**Test tmpfs:**

```bash
# Inside container
echo "This is in RAM" > /tmp/test.txt
cat /tmp/test.txt

# Exit
exit
```

**Restart container and verify data is GONE:**

```bash
# Restart container
docker restart tmpfs-test

# Check if file exists (it won't)
docker exec tmpfs-test ls /tmp
# Empty! Data was in RAM only
```

---

### Step 2: tmpfs vs Regular Filesystem

**Create comparison test:**

```bash
# Container with tmpfs AND regular filesystem
docker run -d \
  --name tmpfs-vs-disk \
  --tmpfs /tmp-ram:rw,size=100m \
  alpine sleep 3600

# Write to tmpfs (RAM)
docker exec tmpfs-vs-disk sh -c 'echo "RAM data" > /tmp-ram/file.txt'

# Write to regular filesystem
docker exec tmpfs-vs-disk sh -c 'echo "Disk data" > /file.txt'

# Restart container
docker restart tmpfs-vs-disk

# Check both
docker exec tmpfs-vs-disk ls /tmp-ram
# Empty! RAM data lost

docker exec tmpfs-vs-disk cat /file.txt
# Still there! Disk data persisted
```

---

## Part 3: tmpfs for Sensitive Data

### Step 3: Using tmpfs for Security

**Why use tmpfs for secrets?**
- Secrets never written to disk
- Can't be recovered from disk forensics
- Automatically cleared when container stops
- Meets compliance requirements (PCI, HIPAA, etc.)

**Example: Application using tmpfs for credentials:**

```bash
# Run app with tmpfs for secrets
docker run -d \
  --name secure-app \
  --tmpfs /run/secrets:rw,noexec,nosuid,size=10m \
  alpine sleep 3600
```

**tmpfs security options:**
- `noexec` - Cannot execute binaries from tmpfs
- `nosuid` - Ignore setuid/setgid bits
- `size=10m` - Limit to 10MB

**Write sensitive data to tmpfs:**

```bash
# Simulate loading secret
docker exec secure-app sh -c 'echo "password123" > /run/secrets/db_password'

# App can read it
docker exec secure-app cat /run/secrets/db_password

# But it's in RAM only!
```

---

### Step 4: tmpfs in Docker Compose

**docker-compose.yml with tmpfs:**

```yaml
services:
  app:
    image: myapp:latest
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=100m
      - /run:rw,noexec,nosuid,size=50m

  # Example: Read-only container with tmpfs for writes
  immutable-app:
    image: myapp:latest
    read_only: true  # Root filesystem is read-only
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=100m
      - /var/run:rw,noexec,nosuid,size=50m
      - /var/cache:rw,noexec,nosuid,size=200m
```

**Why this works:**
- Root filesystem is immutable (security)
- Application can still write to tmpfs directories
- Perfect for stateless apps

---

## Part 4: Performance Testing

### Step 5: Benchmark tmpfs vs Disk

**Create performance test script:**

```bash
# Test tmpfs performance
docker run --rm \
  --tmpfs /tmp-ram:rw,size=500m \
  alpine sh -c '
    echo "Testing tmpfs (RAM) performance..."
    time dd if=/dev/zero of=/tmp-ram/test.dat bs=1M count=100
    rm /tmp-ram/test.dat
  '

# Test regular disk performance
docker run --rm alpine sh -c '
    echo "Testing disk performance..."
    time dd if=/dev/zero of=/test.dat bs=1M count=100
    rm /test.dat
  '
```

**Expected results:**
- tmpfs: ~0.1-0.5 seconds
- disk: ~1-3 seconds
- **tmpfs is typically 5-10x faster!**

---

## Part 5: Real-World Use Cases

### Step 6: Application Cache Example

**Node.js app with tmpfs cache:**

```yaml
services:
  nodejs-app:
    image: node:20-alpine
    tmpfs:
      # Node.js cache and temp files
      - /root/.npm:rw,noexec,nosuid,size=500m
      - /tmp:rw,noexec,nosuid,size=200m

    environment:
      NPM_CONFIG_CACHE: /root/.npm
      TMPDIR: /tmp
```

---

### Step 7: Build Cache Example

**Using tmpfs for Docker builds:**

```bash
# Use tmpfs as build cache directory
docker run --rm \
  --tmpfs /cache:rw,size=2g \
  -v $(pwd):/app \
  -w /app \
  node:20-alpine \
  sh -c 'npm config set cache /cache && npm install'
```

**Benefits:**
- Faster builds (RAM speed)
- No disk wear
- Automatically cleaned up

---

## Part 6: tmpfs Best Practices

### Step 8: Size Limits and Monitoring

**Set appropriate sizes:**

```bash
# Too small - may cause errors
--tmpfs /tmp:size=1m  # ❌ Too small for most apps

# Reasonable - most apps
--tmpfs /tmp:size=100m  # ✅ Good for general use

# Large - for build caches
--tmpfs /cache:size=2g  # ✅ Good for build operations

# Too large - wastes RAM
--tmpfs /tmp:size=10g  # ⚠️ May impact system memory
```

**Monitor tmpfs usage:**

```bash
# Inside container
df -h | grep tmpfs

# From host
docker exec <container> df -h | grep tmpfs
```

---

### Step 9: tmpfs Limitations

**When NOT to use tmpfs:**

❌ **Don't use for:**
- Persistent data (databases, user files)
- Large files (>1GB typically)
- Data that must survive restarts
- Shared data between containers

✅ **DO use for:**
- Temporary files
- Build caches
- Session data
- Sensitive data (passwords, tokens)
- Application temp directories
- Lock files and PIDs

---

## Part 7: Production Configuration

### Step 10: Complete Production Example

**Production-ready compose with tmpfs:**

```yaml
services:
  web:
    image: myapp:latest

    # Read-only root filesystem (security)
    read_only: true

    # tmpfs for necessary write operations
    tmpfs:
      # Application temp directory
      - /tmp:rw,noexec,nosuid,size=100m

      # Process runtime files
      - /var/run:rw,noexec,nosuid,size=50m

      # Application cache
      - /var/cache/app:rw,noexec,nosuid,size=200m

    # Volume for persistent data only
    volumes:
      - app-data:/data:rw

    # Environment variables pointing to tmpfs
    environment:
      TEMP: /tmp
      TMPDIR: /tmp
      CACHE_DIR: /var/cache/app

volumes:
  app-data:
```

---

## Expected Outcomes

After completing this exercise, you should:

✅ Understand when to use tmpfs vs other mount types
✅ Configure tmpfs with security options
✅ Use tmpfs for temporary and sensitive data
✅ Implement read-only containers with tmpfs
✅ Set appropriate tmpfs size limits
✅ Monitor tmpfs usage

---

## Key Takeaways

### tmpfs Advantages:
- ⚡ **Fastest storage** - RAM speed
- 🔒 **Most secure** - Never touches disk
- 🧹 **Self-cleaning** - Data gone on stop
- 💪 **Perfect for stateless** apps

### tmpfs Limitations:
- ❌ Data not persistent
- 💾 Limited by RAM
- 📊 Not shared between containers
- ⚠️ Can cause OOM if too large

### Best Practices:
1. Use tmpfs for temp files and caches
2. Set size limits to prevent RAM exhaustion
3. Use `noexec,nosuid` for security
4. Combine with read-only root filesystem
5. Monitor tmpfs usage in production

---

## Challenge Exercise

**Create a production-ready application configuration:**

**Requirements:**
1. Read-only root filesystem
2. tmpfs for /tmp, /var/run, and /var/cache
3. Named volume for persistent data only
4. Size limits on all tmpfs mounts
5. Security flags (noexec, nosuid)

**Bonus:**
- Measure performance difference
- Calculate RAM requirements
- Test what happens when tmpfs fills up

---

## Additional Resources

- [Docker tmpfs Documentation](https://docs.docker.com/storage/tmpfs/)
- [Linux tmpfs Documentation](https://www.kernel.org/doc/html/latest/filesystems/tmpfs.html)
- [Container Security Best Practices](https://docs.docker.com/engine/security/)

---

## Summary

**tmpfs is a powerful tool for:**
- 🚀 Performance-critical temporary data
- 🔐 Sensitive information security
- 📦 Stateless application design
- 🛡️ Immutable infrastructure

**Use it wisely and your containers will be faster, more secure, and more resilient!**

---

**Next:** Exercise 5 - Volume Backup and Restore Strategies
