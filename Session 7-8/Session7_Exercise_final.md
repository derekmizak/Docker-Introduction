# Sample Application: Docker Compose with Node.js and PostgreSQL

## Overview
We are going to build a **sample application** using **Docker Compose** with two resources:
- A **Node.js web server**
- A **PostgreSQL database**

We will configure **Node.js and PostgreSQL** using a `.env` file to manage sensitive values such as usernames, passwords, and database names.

---

## ✅ Instructions for the Project
This guide walks you through setting up a **Node.js web server with PostgreSQL** using Docker Compose. 
You'll also implement a **Dockerfile for production deployments**.

---

## 📌 Step 1: Project Structure
After completing all steps, your project should look like this:

```
.
├── app/                        # Node.js Application Code
│   ├── package.json
│   ├── package-lock.json
│   ├── index.js
│   ├── Dockerfile               # Dockerfile for Node.js app
├── postgres-data/               # PostgreSQL Volume Data (Auto-created)
├── docker-compose.yml           # Docker Compose Configuration
├── .env                         # Environment Variables
├── .env.example                 # Example .env File (For Documentation)
```

---

## 📌 Step 2: Environment Variables
Create a `.env` file in the root directory and define the database credentials:

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=DB1
DB_HOST=db
```

🔹 Also, create a `.env.example` file (without actual values) to document required environment variables.

---

## 📌 Step 3: Production-Ready `docker-compose.yml` (2025 Best Practices)
This version implements 2025 best practices: proper healthchecks, conditional dependencies, resource limits, and logging configuration.

```yaml
services:
  node:
    build: ./app  # ✅ Build using a Dockerfile in the ./app directory
    container_name: node-app
    working_dir: /app
    volumes:
      - ./app:/app  # ✅ Sync application source code
      - /app/node_modules  # ✅ Anonymous volume for node_modules
    ports:
      - "3000:3000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy  # ✅ Wait for DB to be healthy, not just started
        restart: true
    restart: unless-stopped  # ✅ Restart automatically unless manually stopped
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s  # ✅ Give app time to start before checking health
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine  # ✅ Use specific version and alpine for smaller size
    container_name: postgres-db
    restart: unless-stopped
    volumes:
      - postgres-data:/var/lib/postgresql/data  # ✅ Persistent data storage
      - ./postgres-init:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    env_file:
      - .env
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

volumes:
  postgres-data:  # ✅ Persistent PostgreSQL data
```

### **2025 Updates Explained:**

1. **No `version:` field** - Docker Compose v2 automatically detects the format
2. **Conditional `depends_on`** - Waits for database to be healthy, not just started
3. **Production restart policy** - `unless-stopped` is better than `always` for production
4. **Resource limits** - Prevents containers from consuming all system resources
5. **Logging configuration** - Prevents logs from filling up disk space
6. **Health check with start_period** - Gives containers time to start before health checks count as failures
7. **Specific image tags** - `postgres:16-alpine` instead of `postgres:latest` for reproducibility
8. **Better node healthcheck** - Uses Node.js directly instead of requiring curl in the container

---

## 📌 Step 4: Final `Dockerfile` for Node.js
Create a `Dockerfile` inside the `app/` folder:

```dockerfile
# Use Node.js LTS image
FROM node:lts

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application source code
COPY . .

# Expose application port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
```

---

## 📌 Step 5: Setting Up Your Node.js Application
Navigate to your project folder and create the `app/` directory:

```sh
mkdir app && cd app
```

✅ **Initialize a Node.js Project**
```sh
npm init -y
```

✅ **Install Dependencies**
```sh
npm install pg cors express body-parser dotenv
```

✅ **Create `index.js`**
Inside `app/`, create `index.js` and add the following:

```javascript
const express = require("express");
const { Pool } = require("pg");
const bodyParser = require("body-parser");
const cors = require("cors");
const app = express();
const PORT = 3000;

// ✅ Enable CORS for API access
app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));

// ✅ Use Connection Pooling
const pool = new Pool({
  host: process.env.DB_HOST || "localhost",
  port: 5432,
  user: process.env.POSTGRES_USER || "postgres",
  password: process.env.POSTGRES_PASSWORD || "password",
  database: process.env.POSTGRES_DB || "postgres",
  max: 10,
  idleTimeoutMillis: 30000,
});

// ✅ Serve API Endpoint
app.get("/", async (req, res) => {
  res.send("Hello, Dockerized Node.js with PostgreSQL!");
});

// ✅ Start Express Server
app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
```

---

## 📌 Step 6: Running the Project

Before starting the application for the first time, update `package.json` with the following script:

```json
"scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "start": "node index.js"
  }
```

✅ **Run the following command to start the application:**
```sh
docker-compose up -d
```

✅ **Verify services:**
```sh
docker ps
```

✅ **Visit the Web App:**
- **Web App:** [http://localhost:3000](http://localhost:3000)
- **PostgreSQL (DBeaver):** `localhost:5432` (use `.env` credentials)

---

## 📌 Benefits of Using `.env` Files
- **Centralized management of sensitive configuration values**.
- **Prevents hardcoding of credentials in `docker-compose.yml`**.
- **Makes it easier to switch environments by swapping `.env` files**.

---

🚀 Now you have a fully functional **Dockerized Node.js app with PostgreSQL!** 🎉
