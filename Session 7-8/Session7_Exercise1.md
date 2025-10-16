## **Exercise 1: Create a Multi-Container Application with Docker Compose**

**Objective:**  
- Learn how to define and manage a **multi-container** application using **Docker Compose**.
- Understand **service dependencies** and **networking** between containers.

### **Instructions**
1. **Set up the directory structure**:
   ```bash
   mkdir docker-multi-container
   cd docker-multi-container
   mkdir app
   touch docker-compose.yml .env app/index.js app/package.json
   ```

2. **Create the `docker-compose.yml` file**:
   ```yaml
   version: "3.8"

   services:
     web:
       build: ./app
       container_name: node-app
       ports:
         - "3000:3000"
       depends_on:
         - db
       env_file:
         - .env
       volumes:
         - ./app:/app
         - /app/node_modules

     db:
       image: postgres:latest
       container_name: postgres-db
       ports:
         - "5432:5432"
       environment:
         POSTGRES_USER: ${POSTGRES_USER}
         POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
         POSTGRES_DB: ${POSTGRES_DB}
       volumes:
         - postgres-data:/var/lib/postgresql/data

   volumes:
     postgres-data:
   ```

3. **Create the `.env` file**:
   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=securepassword
   POSTGRES_DB=mydatabase
   ```

4. **Create the `package.json` file inside the `app/` folder**:
   ```json
   {
     "name": "docker-multi-container",
     "version": "1.0.0",
     "main": "index.js",
     "dependencies": {
       "express": "^4.17.1",
       "pg": "^8.7.1"
     },
     "scripts": {
       "start": "node index.js"
     }
   }
   ```

5. **Create the `index.js` file inside `app/` folder**:
   ```javascript
   const express = require("express");
   const { Pool } = require("pg");

   const app = express();
   const pool = new Pool({
     host: process.env.POSTGRES_HOST || "db",
     user: process.env.POSTGRES_USER,
     password: process.env.POSTGRES_PASSWORD,
     database: process.env.POSTGRES_DB,
   });

   app.get("/", async (req, res) => {
     try {
       const result = await pool.query("SELECT NOW()");
       res.send(`Connected! Server time: ${result.rows[0].now}`);
     } catch (err) {
       res.status(500).send("Database connection error");
     }
   });

   app.listen(3000, () => console.log("Server running on port 3000"));
   ```

6. **Build and run the application**:
   ```bash
   docker-compose up -d --build
   ```

7. **Test the application**:  
   Open **`http://localhost:3000`** in a browser.

### **Expected Outcome**
- The web server connects to the database and displays the current time.
- `docker ps` should show both containers running.
- `docker-compose logs` should confirm the successful startup of services.

### **Insights**
- `depends_on` ensures that the database container starts before the web server.
- The `.env` file is used to store **database credentials** securely.

