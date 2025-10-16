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

## 📌 Step 3: Final `docker-compose.yml`
This version binds volumes, adds restart policies, and properly configures environment variables.

```yaml
services:
  node:
    build: ./app  # ✅ Build using a Dockerfile in the ./app directory
    container_name: node-app
    working_dir: /app
    volumes:
      - ./app:/app  # ✅ Sync application source code
    ports:
      - "3000:3000"
    command: ["sh", "-c", "sleep 5 && npm start"]  # ✅ Delay startup to ensure DB readiness
    env_file:
      - .env
    depends_on:
      - db
    restart: always  # ✅ Restart if the container crashes

  db:
    image: postgres:latest
    container_name: postgres-db
    restart: always
    volumes:
      - postgres-data:/var/lib/postgresql/data  # ✅ Persistent data storage
      - ./postgres-init:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    env_file:
      - .env
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:  # ✅ Persistent PostgreSQL data
```

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
