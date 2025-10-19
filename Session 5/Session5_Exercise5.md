# Exercise 5: Volume Backup and Restore Strategies (2025)

**Session 5: Data Management with Volumes**
**Filename:** `Session5_Exercise5.md`

## Objective
- Implement volume backup strategies
- Restore data from backups
- Migrate volumes between systems
- Automate backup processes
- Handle disaster recovery scenarios

---

## Overview

**Data loss is unacceptable in production.** This exercise teaches you to backup and restore Docker volumes properly, ensuring your data is safe.

---

## Part 1: Understanding Volume Backup Strategies

### Backup Strategy Options

| Method | Pros | Cons | Use Case |
|--------|------|------|----------|
| **Container-based** | Simple, portable | Requires container | Quick backups |
| **Direct volume access** | Fast, efficient | Platform-specific | Automated scripts |
| **Database dumps** | Consistent state | Database-specific | Production databases |
| **Snapshot tools** | Point-in-time | Infrastructure dependent | Cloud environments |

---

## Part 2: Basic Volume Backup

### Step 1: Backup a Named Volume

**Create test data:**

```bash
# Create volume with data
docker volume create app-data

# Create container and add data
docker run --rm \
  -v app-data:/data \
  alpine sh -c 'echo "Important data!" > /data/important.txt'
```

**Backup volume to tar file:**

```bash
# Backup method 1: Using a helper container
docker run --rm \
  -v app-data:/data:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/app-data-backup.tar.gz -C /data .
```

**Explanation:**
- `-v app-data:/data:ro` - Mount volume as read-only
- `-v $(pwd):/backup` - Mount current directory for backup file
- `tar czf` - Create compressed tar archive
- `-C /data .` - Change to /data and backup all contents

**Verify backup:**

```bash
ls -lh app-data-backup.tar.gz
# Should show backup file size

# List contents
tar -tzf app-data-backup.tar.gz
```

---

### Step 2: Restore Volume from Backup

**Create new volume and restore:**

```bash
# Create new empty volume
docker volume create app-data-restored

# Restore from backup
docker run --rm \
  -v app-data-restored:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/app-data-backup.tar.gz -C /data
```

**Verify restored data:**

```bash
docker run --rm \
  -v app-data-restored:/data \
  alpine cat /data/important.txt

# Output: Important data!
```

---

## Part 3: Database Backup Best Practices

### Step 3: PostgreSQL Backup

**Setup PostgreSQL with volume:**

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_USER: testuser
      POSTGRES_DB: testdb
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

**Start database:**

```bash
docker compose up -d
```

**Add test data:**

```bash
docker compose exec postgres psql -U testuser -d testdb -c \
  "CREATE TABLE users (id SERIAL, name TEXT); INSERT INTO users (name) VALUES ('Alice'), ('Bob');"
```

**Backup using pg_dump (CORRECT way):**

```bash
# Create backup directory
mkdir -p backups

# Backup database
docker compose exec -T postgres pg_dump -U testuser testdb > backups/db-backup.sql
```

**Why pg_dump over volume backup?**
- ✅ Ensures consistent state
- ✅ Database not corrupted
- ✅ Can restore to different PostgreSQL version
- ✅ Human-readable SQL

---

### Step 4: Restore PostgreSQL Backup

**Drop and recreate database:**

```bash
# Drop database
docker compose exec postgres psql -U testuser -c "DROP DATABASE testdb;"

# Recreate database
docker compose exec postgres psql -U testuser -c "CREATE DATABASE testdb;"

# Restore from backup
docker compose exec -T postgres psql -U testuser testdb < backups/db-backup.sql
```

**Verify restored data:**

```bash
docker compose exec postgres psql -U testuser -d testdb -c "SELECT * FROM users;"

# Should show Alice and Bob
```

---

## Part 4: Automated Backup Scripts

### Step 5: Create Backup Script

**Create `backup-volumes.sh`:**

```bash
#!/bin/bash

set -e

# Configuration
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d-%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "🔄 Starting volume backup at $(date)"

# Backup named volume
backup_volume() {
    VOLUME_NAME=$1
    BACKUP_FILE="$BACKUP_DIR/${VOLUME_NAME}-${DATE}.tar.gz"

    echo "📦 Backing up volume: $VOLUME_NAME"

    docker run --rm \
        -v "${VOLUME_NAME}:/data:ro" \
        -v "${BACKUP_DIR}:/backup" \
        alpine tar czf "/backup/$(basename $BACKUP_FILE)" -C /data .

    echo "✅ Backup saved: $BACKUP_FILE"
    ls -lh "$BACKUP_FILE"
}

# Backup specific volumes
backup_volume "app-data"
backup_volume "pgdata"

# Keep only last 7 days of backups
echo "🧹 Cleaning old backups (keeping last 7 days)..."
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "🎉 Backup complete at $(date)"
```

**Make executable and run:**

```bash
chmod +x backup-volumes.sh
./backup-volumes.sh
```

---

### Step 6: Restore Script

**Create `restore-volume.sh`:**

```bash
#!/bin/bash

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <backup-file> <target-volume>"
    echo "Example: $0 backups/app-data-20251019.tar.gz app-data-new"
    exit 1
fi

BACKUP_FILE=$1
TARGET_VOLUME=$2

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "🔄 Starting restore..."
echo "   Source: $BACKUP_FILE"
echo "   Target: $TARGET_VOLUME"

# Create volume if doesn't exist
docker volume create "$TARGET_VOLUME" > /dev/null 2>&1 || true

# Restore backup
docker run --rm \
    -v "${TARGET_VOLUME}:/data" \
    -v "$(pwd):/backup" \
    alpine sh -c "
        rm -rf /data/* &&
        tar xzf /backup/$BACKUP_FILE -C /data
    "

echo "✅ Restore complete!"
echo "📊 Volume contents:"

docker run --rm -v "${TARGET_VOLUME}:/data" alpine ls -la /data
```

**Usage:**

```bash
chmod +x restore-volume.sh
./restore-volume.sh backups/app-data-20251019-120000.tar.gz app-data-restored
```

---

## Part 5: Advanced Backup Strategies

### Step 7: Incremental Backups (rsync)

**For large volumes, use incremental backups:**

```bash
# First backup (full)
docker run --rm \
  -v app-data:/data:ro \
  -v $(pwd)/backups:/backup \
  instrumentisto/rsync-ssh \
  rsync -av --delete /data/ /backup/app-data-full/

# Subsequent backups (incremental)
docker run --rm \
  -v app-data:/data:ro \
  -v $(pwd)/backups:/backup \
  instrumentisto/rsync-ssh \
  rsync -av --link-dest=/backup/app-data-full \
    /data/ /backup/app-data-$(date +%Y%m%d)/
```

**Benefits:**
- Only changed files copied
- Saves storage space
- Faster backups
- Multiple restore points

---

### Step 8: Cloud Backup Integration

**Backup to AWS S3:**

```bash
#!/bin/bash

VOLUME_NAME="app-data"
S3_BUCKET="my-docker-backups"
BACKUP_FILE="backup-$(date +%Y%m%d).tar.gz"

# Create backup
docker run --rm \
    -v "${VOLUME_NAME}:/data:ro" \
    -v /tmp:/backup \
    alpine tar czf "/backup/${BACKUP_FILE}" -C /data .

# Upload to S3
docker run --rm \
    -v /tmp:/backup \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    amazon/aws-cli \
    s3 cp "/backup/${BACKUP_FILE}" "s3://${S3_BUCKET}/"

# Clean up
rm "/tmp/${BACKUP_FILE}"
```

---

## Part 6: Volume Migration

### Step 9: Migrate Volume Between Hosts

**On source host:**

```bash
# Export volume
docker run --rm \
  -v source-volume:/data:ro \
  alpine tar cz -C /data . > volume-export.tar.gz

# Transfer to new host (example with scp)
scp volume-export.tar.gz user@newhost:/tmp/
```

**On destination host:**

```bash
# Create volume
docker volume create target-volume

# Import data
docker run --rm \
  -v target-volume:/data \
  -i alpine tar xz -C /data < /tmp/volume-export.tar.gz
```

---

### Step 10: Copy Volume Between Containers

**Clone a volume:**

```bash
# Source and destination volumes
SRC_VOLUME="prod-data"
DST_VOLUME="prod-data-clone"

# Create destination volume
docker volume create $DST_VOLUME

# Copy data
docker run --rm \
  -v ${SRC_VOLUME}:/source:ro \
  -v ${DST_VOLUME}:/dest \
  alpine sh -c "cp -av /source/. /dest/"
```

---

## Part 7: Disaster Recovery

### Step 11: Complete DR Scenario

**Disaster recovery plan:**

```bash
#!/bin/bash
# disaster-recovery.sh

set -e

BACKUP_DIR="./dr-backups"
DATE=$(date +%Y%m%d-%H%M%S)

echo "🚨 DISASTER RECOVERY MODE"
echo "📅 Timestamp: $DATE"

# 1. Stop all services
echo "🛑 Stopping services..."
docker compose down

# 2. Backup current state (just in case)
echo "💾 Creating emergency backup..."
mkdir -p "$BACKUP_DIR/emergency-$DATE"

for volume in $(docker volume ls -q); do
    echo "  Backing up: $volume"
    docker run --rm \
        -v "${volume}:/data:ro" \
        -v "${BACKUP_DIR}/emergency-$DATE:/backup" \
        alpine tar czf "/backup/${volume}.tar.gz" -C /data .
done

# 3. Restore from known good backup
echo "🔄 Restoring from backup..."
RESTORE_DATE="20251019-120000"  # Replace with actual backup date

for backup in "$BACKUP_DIR/$RESTORE_DATE"/*.tar.gz; do
    VOLUME_NAME=$(basename "$backup" .tar.gz)
    echo "  Restoring: $VOLUME_NAME"

    docker volume create "$VOLUME_NAME" || true

    docker run --rm \
        -v "${VOLUME_NAME}:/data" \
        -v "$BACKUP_DIR/$RESTORE_DATE:/backup" \
        alpine sh -c "rm -rf /data/* && tar xzf /backup/$(basename $backup) -C /data"
done

# 4. Restart services
echo "🚀 Restarting services..."
docker compose up -d

# 5. Verify
echo "✅ Verifying services..."
sleep 10
docker compose ps

echo "🎉 Disaster recovery complete!"
```

---

## Part 8: Backup Validation

### Step 12: Test Your Backups

**Always test backups! Untested backups = no backups**

```bash
#!/bin/bash
# test-backup.sh

BACKUP_FILE=$1
TEST_VOLUME="test-restore-$(date +%s)"

echo "🧪 Testing backup: $BACKUP_FILE"

# Create test volume
docker volume create "$TEST_VOLUME"

# Restore backup
docker run --rm \
    -v "${TEST_VOLUME}:/data" \
    -v "$(pwd):/backup" \
    alpine tar xzf "/backup/$BACKUP_FILE" -C /data

# Verify contents
echo "📋 Backup contents:"
docker run --rm -v "${TEST_VOLUME}:/data" alpine ls -laR /data

# Cleanup
docker volume rm "$TEST_VOLUME"

echo "✅ Backup test complete!"
```

---

## Part 9: Backup Automation with Cron

### Step 13: Schedule Automatic Backups

**Crontab entry (Linux/Mac):**

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/backup-volumes.sh >> /var/log/docker-backup.log 2>&1

# Add weekly cleanup
0 3 * * 0 find /path/to/backups -name "*.tar.gz" -mtime +30 -delete
```

**Docker container for scheduled backups:**

```yaml
# docker-compose.yml
services:
  backup:
    image: alpine:latest
    volumes:
      - app-data:/data:ro
      - ./backups:/backup
      - ./scripts:/scripts:ro
    command: >
      sh -c "
        while true; do
          /scripts/backup-volumes.sh
          sleep 86400
        done
      "
```

---

## Expected Outcomes

After completing this exercise, you should:

✅ Backup Docker volumes reliably
✅ Restore data from backups
✅ Implement database-specific backup strategies
✅ Automate backup processes
✅ Migrate volumes between systems
✅ Handle disaster recovery scenarios
✅ Validate backups regularly

---

## Backup Best Practices Checklist

```markdown
## Volume Backup Checklist

### Planning
- [ ] Identify critical volumes
- [ ] Determine backup frequency (daily, hourly, etc.)
- [ ] Calculate storage requirements
- [ ] Define retention policy (how long to keep backups)

### Implementation
- [ ] Use database-specific tools (pg_dump, mysqldump)
- [ ] Test backups regularly
- [ ] Automate backup process
- [ ] Monitor backup success/failure
- [ ] Store backups off-site or in cloud

### Security
- [ ] Encrypt backups if they contain sensitive data
- [ ] Secure backup storage location
- [ ] Control access to backup files
- [ ] Document backup procedures

### Recovery
- [ ] Test restore procedure regularly
- [ ] Document restore steps
- [ ] Measure Recovery Time Objective (RTO)
- [ ] Measure Recovery Point Objective (RPO)
- [ ] Have disaster recovery plan ready
```

---

## Common Backup Scenarios

### Scenario 1: Development Environment
**Frequency:** Weekly
**Method:** Simple tar backups
**Retention:** 4 weeks

### Scenario 2: Staging Environment
**Frequency:** Daily
**Method:** Database dumps + volume backups
**Retention:** 2 weeks

### Scenario 3: Production Environment
**Frequency:** Hourly (incremental) + Daily (full)
**Method:** Database dumps + cloud backup
**Retention:** 90 days minimum

---

## Challenge Exercise

**Create a complete backup and recovery system:**

**Requirements:**
1. Backup script for all volumes
2. Database dump integration
3. Automated scheduling (cron or container)
4. Retention policy (delete old backups)
5. Restore script with verification
6. Cloud storage integration (S3, Azure Blob, or GCS)

**Bonus:**
- Encrypt backups
- Send notifications on success/failure
- Create monitoring dashboard
- Implement incremental backups

---

## Additional Resources

- [Docker Volume Documentation](https://docs.docker.com/storage/volumes/)
- [PostgreSQL Backup Documentation](https://www.postgresql.org/docs/current/backup.html)
- [MySQL Backup Best Practices](https://dev.mysql.com/doc/refman/8.0/en/backup-and-recovery.html)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)

---

## Summary

**The 3-2-1 Backup Rule:**
- **3** copies of data
- **2** different media types
- **1** off-site backup

**Remember:**
- 💾 Backup regularly and automatically
- ✅ Test restores frequently
- 🔒 Secure backup storage
- 📊 Monitor backup health
- 📚 Document procedures

**Your data is only as safe as your last tested backup!**

---

**Session 5 Complete! You now have comprehensive data management skills for Docker.**
