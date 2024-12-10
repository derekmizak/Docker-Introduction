

### **Exercise 1: Install a Specific Node.js Version on Alpine**

**Filename:** `Session4_Exercise1.md`


# Exercise 1: Install a Specific Node.js Version on Alpine

## Objective
- Install a specific version of Node.js (v22.11.0 LTS) on an extremely lightweight base image (Alpine).
- Optimize the Dockerfile for minimal size and efficiency.

---

## Instructions

### Step 1: Create a Simple Node.js Application
1. Create a directory for your project:
   ```bash
   mkdir alpine-node-specific
   cd alpine-node-specific
   ```

2. Create the following files:
   - **`app.js`:**
     ```javascript
     console.log("Hello from a specific Node.js version (v22.11.0 LTS) running on Alpine!");
     ```
   - **`package.json`:**
     ```json
     {
       "name": "specific-node-app",
       "version": "1.0.0",
       "main": "app.js",
       "scripts": {
         "start": "node app.js"
       }
     }
     ```

---

### Step 2: Write a Dockerfile to Install Node.js v22.11.0
1. Create a `Dockerfile`:
   ```Dockerfile
   FROM alpine:latest

   # Install required dependencies
   RUN apk add --no-cache curl bash

   # Install Node.js v22.11.0 LTS
   RUN curl -fsSL https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz | tar -xJ -C /usr/local --strip-components=1

   # Ensure Node.js binaries are in PATH
   ENV PATH="/usr/local/bin:$PATH"

   # Verify Node.js installation
   RUN node -v && npm -v

   # Set the working directory
   WORKDIR /app

   # Copy application files
   COPY package.json ./
   RUN npm install
   COPY . .

   # Expose the application port
   EXPOSE 3000

   # Default command
   CMD ["npm", "start"]
   ```

2. Build the image:
   ```bash
   docker build -t alpine-node-lts .
   ```

3. Run the container:
   ```bash
   docker run -it --rm -p 3000:3000 alpine-node-lts
   ```

Verify that container is runnig and accessible at `http://localhost:3000`. If not review logs and troubleshoot. There is a possiblity that either port is already in use or the node archtecture is not compatible with the host machine - in that case adjust the `Dockerfile` to use the correct archtecture.

After succesful test stop the container.

---

### Step 3: Optimize the Dockerfile
1. Update the `Dockerfile`:
   ```Dockerfile
   FROM alpine:latest

   # Install required dependencies
   RUN apk add --no-cache curl bash && \
       curl -fsSL https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz | tar -xJ -C /usr/local --strip-components=1 && \
       rm -rf /var/cache/apk/*


   # Ensure Node.js binaries are in PATH
   ENV PATH="/usr/local/bin:$PATH"
   
   # Verify Node.js installation
   RUN node -v && npm -v

   # Set the working directory
   WORKDIR /app

   # Copy files and install dependencies
   COPY package.json ./
   RUN npm install && rm -rf /var/cache/apk/*

   # Copy source code
   COPY . .

   # Expose the application port
   EXPOSE 3000

   # Default command
   CMD ["npm", "start"]
   ```

2. Rebuild the image and compare sizes:
   ```bash
   docker images
   ```

---

## Expected Outcome
- Successfully install of Node.js v22.11.0 LTS on Alpine.
- The difference in size and efficiency before and after optimization is observed.


