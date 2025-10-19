# Exercise 4: Secrets Management in Docker & Docker Compose (2025)

**Session 8: Security & Best Practices**
**Filename:** `Session8_Exercise4.md`

## Objective
- Understand different types of secrets in containerized applications
- Implement secure secrets management
- Use Docker Compose secrets
- Avoid common secrets management mistakes
- Integrate with external secrets managers

---

## Overview

**Secrets** are sensitive data like passwords, API keys, certificates, and tokens that applications need but must be protected. **Never hardcode secrets in images or commit them to version control!**

---

## Part 1: Understanding Secrets Anti-Patterns

### Step 1: What NOT to Do

**❌ NEVER do any of these:**

```dockerfile
# ❌ 1. Hardcoded in Dockerfile
ENV DATABASE_PASSWORD="super_secret_123"

# ❌ 2. As build argument (visible in docker history)
ARG API_KEY="sk-1234567890"

# ❌ 3. In RUN command
RUN echo "password123" > /app/secret.txt

# ❌ 4. Committed in code
const dbPassword = "hardcoded_password";
```

**❌ Bad docker-compose.yml:**
```yaml
services:
  app:
    image: myapp:latest
    environment:
      DB_PASSWORD: "hardcoded123"  # ❌ Visible in docker inspect!
```

**❌ Committing .env files:**
```bash
# .env (committed to git)  ❌ NEVER!
DB_PASSWORD=secret123
API_KEY=sk-xxxxxx
```

**Why these are dangerous:**
- Visible in image layers
- Exposed in docker history
- Stored in version control
- Accessible via docker inspect
- Can be extracted from images

---

## Part 2: Docker Compose Secrets (Basic)

### Step 2: Using Docker Compose Secrets

**Create project structure:**

```bash
mkdir secrets-demo
cd secrets-demo
mkdir secrets
```

**Create secret files:**

```bash
# Create database password
echo "my_secure_db_password" > secrets/db_password.txt

# Create API key
echo "sk-1234567890abcdef" > secrets/api_key.txt

# IMPORTANT: Never commit secrets directory!
echo "secrets/" > .gitignore
```

**Create `docker-compose.yml`:**

```yaml
services:
  app:
    image: myapp:latest
    secrets:
      - db_password
      - api_key
    environment:
      # Don't put the secret value, just reference where to find it
      DB_PASSWORD_FILE: /run/secrets/db_password
      API_KEY_FILE: /run/secrets/api_key

  db:
    image: postgres:16-alpine
    secrets:
      - db_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_USER: myuser
      POSTGRES_DB: mydb

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

**Application code** (`app.js`):

```javascript
const fs = require('fs');
const path = require('path');

// Read secrets from files (not environment variables!)
function readSecret(secretName) {
  try {
    const secretPath = process.env[`${secretName}_FILE`];
    if (!secretPath) {
      throw new Error(`${secretName}_FILE not set`);
    }
    return fs.readFileSync(secretPath, 'utf8').trim();
  } catch (err) {
    console.error(`Failed to read secret ${secretName}:`, err);
    process.exit(1);
  }
}

// Usage
const dbPassword = readSecret('DB_PASSWORD');
const apiKey = readSecret('API_KEY');

// Use secrets (never log them!)
console.log('Secrets loaded successfully');
// DON'T: console.log('DB Password:', dbPassword);  ❌ Never log secrets!

// Connect to database
const connectionString = `postgresql://myuser:${dbPassword}@db:5432/mydb`;
// ... use connection string
```

**Benefits:**
- ✅ Secrets not in environment variables
- ✅ Secrets not visible in `docker inspect`
- ✅ Secrets mounted as files in `/run/secrets/`
- ✅ Secrets only accessible to services that need them

---

### Step 3: Testing Secrets

**Start services:**
```bash
docker compose up -d
```

**Verify secrets are mounted:**
```bash
# Check secrets directory
docker compose exec app ls -la /run/secrets/

# Output should show:
# db_password
# api_key

# Check permissions (should be 0400 - read-only for owner)
docker compose exec app ls -l /run/secrets/db_password
```

**Verify secrets NOT in environment:**
```bash
docker compose exec app env | grep -i password
# Should NOT show actual password, only _FILE path
```

**Verify secrets NOT in inspect:**
```bash
docker inspect secrets-demo-app-1 | grep -i password
# Should not reveal actual secret value
```

---

## Part 3: Environment Variables vs Secrets

### Step 4: When to Use Each

| Type | Use For | Security Level | Visibility |
|------|---------|----------------|------------|
| **Hardcoded** | Nothing sensitive | ❌ Lowest | Image layers, code |
| **Environment Variables** | Non-sensitive config | 🟡 Low | docker inspect, env |
| **Docker Secrets** | Passwords, tokens | 🟢 Good | Only mounted files |
| **External Secrets Manager** | Production secrets | 🟢🟢 Best | External system |

**Example configuration:**

```yaml
services:
  app:
    image: myapp:latest

    # ✅ OK for environment variables (non-sensitive)
    environment:
      NODE_ENV: production
      LOG_LEVEL: info
      PORT: 3000

    # ✅ Use secrets for sensitive data
    secrets:
      - db_password
      - jwt_secret
      - api_key

    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password
      JWT_SECRET_FILE: /run/secrets/jwt_secret
      API_KEY_FILE: /run/secrets/api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
  api_key:
    file: ./secrets/api_key.txt
```

---

## Part 4: Build-Time Secrets (BuildKit)

### Step 5: Secrets During Image Build

**Problem:** Sometimes you need secrets during build (private npm packages, private repos, etc.)

**❌ WRONG Way:**

```dockerfile
# ❌ Don't do this!
ARG NPM_TOKEN
RUN echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > ~/.npmrc && \
    npm install && \
    rm ~/.npmrc  # ❌ Still in layer history!
```

**✅ CORRECT Way (BuildKit Secret Mounts):**

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

# ✅ Secret only available during THIS command, not in layers
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci --only=production

COPY . .

USER appuser
CMD ["node", "server.js"]
```

**Build with secret:**

```bash
# Create .npmrc file (don't commit!)
echo "//registry.npmjs.org/:_authToken=YOUR_TOKEN" > .npmrc

# Add to .gitignore
echo ".npmrc" >> .gitignore

# Build with secret
DOCKER_BUILDKIT=1 docker build \
  --secret id=npmrc,src=.npmrc \
  -t myapp:latest .

# Secret is NOT in the final image!
docker history myapp:latest
# Won't show .npmrc content
```

---

### Step 6: SSH Secrets for Private Git Repos

**For private repositories:**

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.21-alpine

RUN apk add --no-cache git openssh-client

WORKDIR /app

COPY go.mod go.sum ./

# ✅ Mount SSH key to access private repos
RUN --mount=type=ssh \
    git config --global url."git@github.com:".insteadOf "https://github.com/" && \
    go mod download

COPY . .
RUN go build -o app .

CMD ["./app"]
```

**Build with SSH:**

```bash
# Start ssh-agent and add key
eval $(ssh-agent)
ssh-add ~/.ssh/id_rsa

# Build with SSH forwarding
DOCKER_BUILDKIT=1 docker build \
  --ssh default \
  -t myapp:latest .
```

---

## Part 5: Secrets Rotation

### Step 7: Implementing Secret Rotation

**Problem:** Secrets should be rotated periodically. How to update without downtime?

**Create rotation script** `rotate-secret.sh`:

```bash
#!/bin/bash

set -e

SECRET_NAME=$1
NEW_VALUE=$2

if [ -z "$SECRET_NAME" ] || [ -z "$NEW_VALUE" ]; then
    echo "Usage: ./rotate-secret.sh <secret-name> <new-value>"
    exit 1
fi

echo "🔄 Rotating secret: $SECRET_NAME"

# 1. Update secret file
echo "$NEW_VALUE" > secrets/${SECRET_NAME}.txt

# 2. Restart affected services
echo "📦 Restarting services..."
docker compose up -d --force-recreate

# 3. Verify services started successfully
echo "✅ Checking service health..."
sleep 5
docker compose ps

echo "🎉 Secret rotation complete!"
```

**Usage:**

```bash
chmod +x rotate-secret.sh
./rotate-secret.sh db_password "new_secure_password_456"
```

---

## Part 6: External Secrets Managers

### Step 8: Integrating with External Secrets

**For production, use dedicated secrets managers:**

| Provider | Use Case |
|----------|----------|
| **AWS Secrets Manager** | AWS environments |
| **Google Secret Manager** | GCP environments |
| **Azure Key Vault** | Azure environments |
| **HashiCorp Vault** | Multi-cloud, on-premise |
| **Kubernetes Secrets** | Kubernetes clusters |

**Example: Using AWS Secrets Manager**

**Create `get-secret.sh`:**

```bash
#!/bin/bash
# Fetch secret from AWS Secrets Manager

SECRET_NAME=$1
SECRET_VALUE=$(aws secretsmanager get-secret-value \
  --secret-id $SECRET_NAME \
  --query SecretString \
  --output text)

echo "$SECRET_VALUE" > /run/secrets/${SECRET_NAME}
```

**Updated Dockerfile:**

```dockerfile
FROM node:20-alpine

# Install AWS CLI
RUN apk add --no-cache aws-cli

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
COPY get-secret.sh /usr/local/bin/

# Fetch secrets on startup
ENTRYPOINT ["sh", "-c", "/usr/local/bin/get-secret.sh db_password && node server.js"]
```

**Docker Compose with AWS:**

```yaml
services:
  app:
    image: myapp:latest
    environment:
      AWS_REGION: us-east-1
      # Use AWS credentials from host or IAM role
    volumes:
      - ~/.aws:/root/.aws:ro
```

---

## Part 7: Secrets Best Practices

### Step 9: Complete Secrets Checklist

```markdown
## Secrets Management Checklist

### Never Do
- [ ] ❌ Hardcode secrets in Dockerfile or source code
- [ ] ❌ Use ARG for secrets (visible in docker history)
- [ ] ❌ Put secrets in ENV (visible in docker inspect)
- [ ] ❌ Commit secrets to version control
- [ ] ❌ Log secret values
- [ ] ❌ Leave secrets in build layers

### Always Do
- [ ] ✅ Use Docker Compose secrets for local development
- [ ] ✅ Use BuildKit secret mounts for build-time secrets
- [ ] ✅ Use external secrets manager for production
- [ ] ✅ Read secrets from files, not environment variables
- [ ] ✅ Set appropriate file permissions (0400)
- [ ] ✅ Rotate secrets regularly
- [ ] ✅ Add secrets files to .gitignore
- [ ] ✅ Use strong, unique secrets for each environment
- [ ] ✅ Audit secret access
- [ ] ✅ Delete secrets when no longer needed

### Code Practices
- [ ] ✅ Read secrets at runtime, not build time
- [ ] ✅ Never log secret values
- [ ] ✅ Clear secrets from memory after use (if applicable)
- [ ] ✅ Validate secrets format before use
- [ ] ✅ Handle missing secrets gracefully
```

---

## Part 8: Complete Example Project

### Step 10: Production-Ready Secrets Setup

**Project structure:**

```
my-secure-app/
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .gitignore
├── secrets/
│   ├── .gitkeep
│   └── (secret files go here - not committed)
├── app/
│   ├── Dockerfile
│   ├── package.json
│   └── server.js
└── scripts/
    ├── setup-secrets.sh
    └── rotate-secret.sh
```

**`.gitignore`:**

```
secrets/*.txt
secrets/*.key
secrets/*.pem
.env
.env.local
.npmrc
```

**`.env.example`:**

```
# Copy this file to .env and fill in values
# Never commit .env!

# Database
POSTGRES_USER=myuser
POSTGRES_DB=mydb

# Application
NODE_ENV=production
PORT=3000

# Note: Actual secrets go in secrets/ directory files
```

**`setup-secrets.sh`:**

```bash
#!/bin/bash

set -e

echo "🔐 Setting up secrets..."

mkdir -p secrets

# Check if secrets already exist
if [ -f "secrets/db_password.txt" ]; then
    read -p "Secrets exist. Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

# Generate secure random passwords
openssl rand -base64 32 > secrets/db_password.txt
openssl rand -base64 32 > secrets/jwt_secret.txt
openssl rand -base64 32 > secrets/api_key.txt

# Set appropriate permissions
chmod 0400 secrets/*.txt

echo "✅ Secrets created in secrets/ directory"
echo "⚠️  Remember: Never commit these files!"
```

**`docker-compose.yml`:**

```yaml
services:
  app:
    build: ./app
    ports:
      - "3000:3000"
    secrets:
      - db_password
      - jwt_secret
      - api_key
    environment:
      NODE_ENV: production
      DB_PASSWORD_FILE: /run/secrets/db_password
      JWT_SECRET_FILE: /run/secrets/jwt_secret
      API_KEY_FILE: /run/secrets/api_key
      DB_HOST: db
      DB_USER: myuser
      DB_NAME: mydb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    secrets:
      - db_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_USER: myuser
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U myuser"]
      interval: 10s
      timeout: 5s
      retries: 5

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
  api_key:
    file: ./secrets/api_key.txt

volumes:
  pgdata:
```

**`app/server.js`:**

```javascript
const fs = require('fs');
const express = require('express');
const { Pool } = require('pg');

// Secure secret reader
function readSecret(envVarName) {
  const secretPath = process.env[envVarName];

  if (!secretPath) {
    throw new Error(`${envVarName} not set`);
  }

  if (!fs.existsSync(secretPath)) {
    throw new Error(`Secret file not found: ${secretPath}`);
  }

  return fs.readFileSync(secretPath, 'utf8').trim();
}

// Read secrets
const dbPassword = readSecret('DB_PASSWORD_FILE');
const jwtSecret = readSecret('JWT_SECRET_FILE');
const apiKey = readSecret('API_KEY_FILE');

// Initialize database pool
const pool = new Pool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: dbPassword,  // From secret file
  database: process.env.DB_NAME,
});

const app = express();

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.get('/', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.json({
      message: 'Secure app running!',
      timestamp: result.rows[0].now
    });
  } catch (err) {
    console.error('Database error:', err.message);
    res.status(500).json({ error: 'Database connection failed' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
  console.log('✅ Secrets loaded successfully');
});
```

**Setup and run:**

```bash
# 1. Generate secrets
./scripts/setup-secrets.sh

# 2. Copy environment template
cp .env.example .env

# 3. Start services
docker compose up -d

# 4. Test
curl http://localhost:3000
curl http://localhost:3000/health
```

---

## Expected Outcomes

After completing this exercise, you should:

✅ Never hardcode secrets in images or code
✅ Use Docker Compose secrets for local development
✅ Implement BuildKit secret mounts for build-time secrets
✅ Read secrets from files, not environment variables
✅ Rotate secrets safely
✅ Integrate with external secrets managers for production
✅ Follow industry best practices for secrets management

---

## Challenge Exercise

**Build a complete secure application:**

**Requirements:**
1. No secrets in Dockerfile or docker-compose.yml
2. All secrets in separate files
3. Secret files in .gitignore
4. Application reads secrets from files
5. Implements secret rotation
6. Proper error handling for missing secrets
7. Logging never exposes secrets

**Bonus:**
- Integrate with AWS Secrets Manager or HashiCorp Vault
- Implement automatic secret rotation
- Add secret versioning

---

## Additional Resources

- [Docker Secrets Documentation](https://docs.docker.com/engine/swarm/secrets/)
- [BuildKit Secret Mounts](https://docs.docker.com/build/building/secrets/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [HashiCorp Vault](https://www.vaultproject.io/)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

## Summary

**The Golden Rules of Secrets:**

1. **Never commit secrets** to version control
2. **Never hardcode secrets** in images or code
3. **Never log secrets** in application logs
4. **Always use dedicated secrets management** for production
5. **Always rotate secrets** regularly
6. **Always use least privilege** - only grant access to secrets that are needed
7. **Always audit secret access** - know who accessed what and when

**Security is a journey, not a destination. Keep learning and improving! 🔒**

---

**Congratulations! You've completed Session 8: Security & Best Practices!**
