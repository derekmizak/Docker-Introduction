---

## **Exercise 3: Scaling Services in Docker Compose**

**Objective:**  
- Learn how to **scale** services using `docker-compose up --scale`.
- Understand the **service discovery** feature in Docker Compose.

### **Instructions**
1. **Create a directory**:
   ```bash
   mkdir docker-scaling
   cd docker-scaling
   mkdir app
   touch docker-compose.yml app/index.js app/package.json
   ```

2. **Define the `docker-compose.yml`**:
   ```yaml
   version: "3.8"

   services:
     web:
       build: ./app
       ports:
         - "8000-8005:3000"
       depends_on:
         - db
       environment:
         DB_HOST: db
         DB_USER: postgres
         DB_PASSWORD: password
         DB_NAME: mydatabase

     db:
       image: postgres:latest
       environment:
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: password
         POSTGRES_DB: mydatabase
   ```

3. **Modify `index.js` to display container information**:
   ```javascript
   const express = require("express");
   const os = require("os");

   const app = express();
   const PORT = 3000;

   app.get("/", (req, res) => {
     res.send(`Container Name: ${os.hostname()} is responding on port ${PORT}`);
   });

   app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
   ```

4. **Build and scale up the application**:
   ```bash
   docker-compose up -d --build
   docker-compose up -d --scale web=3
   ```

5. **Test the scaling**:
   - Open **http://localhost:8000**, **http://localhost:8001**, **http://localhost:8002**.
   - Refresh the page and observe how requests are distributed among multiple containers.

### **Expected Outcome**
- Requests will be served by different instances of the `web` service.
- `docker ps` should show three running instances of `web`.

### **Insights**
- **Scaling is done using `--scale`**, but there is **no built-in load balancing**.
- A proper **reverse proxy (e.g., Nginx, Traefik)** is needed for full load balancing.

