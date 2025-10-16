

## **Exercise 2: Implement Environment-Specific Configurations in Docker Compose**

**Objective:**  
- Learn how to manage **different environments (development, production)** using Docker Compose.
- Understand how to use **override files** and **.env files**.

### **Instructions**
1. **Create a new directory**:
   ```bash
   mkdir docker-environments
   cd docker-environments
   mkdir app
   touch docker-compose.yml docker-compose.override.yml .env app/index.js app/package.json
   ```

2. **Define the base `docker-compose.yml`**:
   ```yaml
   version: "3.8"

   services:
     web:
       build: ./app
       ports:
         - "3000:3000"
       env_file:
         - .env
       volumes:
         - ./app:/app
         - /app/node_modules
   ```

3. **Create the `.env` file**:
   ```
   NODE_ENV=development
   DEBUG=true
   ```

4. **Define the override file `docker-compose.override.yml` for production**:
   ```yaml
   version: "3.8"

   services:
     web:
       environment:
         NODE_ENV: production
         DEBUG: false
       ports:
         - "8080:3000"
   ```

5. **Modify `index.js` inside `app/` folder to use environment variables**:
   ```javascript
   const express = require("express");
   const app = express();

   const environment = process.env.NODE_ENV || "development";
   const debugMode = process.env.DEBUG === "true";

   app.get("/", (req, res) => {
     res.send(`Running in ${environment} mode. Debug: ${debugMode}`);
   });

   app.listen(3000, () => console.log("Server running"));
   ```

6. **Run in Development Mode**:
   ```bash
   docker-compose up -d
   ```

7. **Run in Production Mode (with Override File)**:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
   ```

8. **Test the application**:
   - **Development mode:** Open `http://localhost:3000`
   - **Production mode:** Open `http://localhost:8080`

### **Expected Outcome**
- The application responds differently based on the **NODE_ENV** variable.
- Development mode runs on port **3000**; production mode runs on **8080**.

### **Insights**
- **Override files** allow flexible configuration for different environments.
- This approach prevents **modifying the main `docker-compose.yml`** for different setups.

