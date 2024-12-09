

### **Exercise 1: Writing a Dockerfile for a Simple Node.js Application**

**Filename:** `Session3_Exercise1.md`


# Exercise 1: Writing a Dockerfile for a Simple Node.js Application

## Objective
- Create a minimal Node.js application with a single console log statement.
- Containerize the application using a Dockerfile.
- Run the container interactively to observe console output.
- Inspect logs, image layers, and the structure of the resulting image.

---

## Instructions

### Step 1: Create a Node.js Application
1. Create a new directory for your project:
   ```bash
   mkdir my-simple-node-app
   cd my-simple-node-app
   ```

2. Initialize a new Node.js project:
   ```bash
   npm init -y
   ```

   - This creates a `package.json` file with default values. Please inspect the file content.

3. Create a JavaScript file named `app.js` with the following content:
   ```javascript
   // app.js
   console.log("Hi from the Node.js application!");
   ```

---

### Step 2: Write a Dockerfile
Create a `Dockerfile` in the same directory as `app.js`:

```Dockerfile
# Use a lightweight Node.js base image
FROM node:alpine

# Set the working directory
WORKDIR /app

# Copy package.json (if exists) and the application code
COPY package*.json ./
RUN npm install

# Copy the application code
COPY . .

# Command to run the Node.js application
CMD ["node", "app.js"]
```

---

### Step 3: Build the Docker Image
Build the Docker image using the following command:

```bash
docker build -t simple-node-app .
```

- **`-t simple-node-app`:** Tags the image as `simple-node-app`.

---

### Step 4: Run the Docker Container Interactively
Run the container using the `-it` flag to see the console output directly:

```bash
docker run -it --rm simple-node-app
```

- **`-it`:** Runs the container interactively, attaching your terminal to it.
- **`--rm`:** Automatically removes the container after it stops.

---

### Step 5: Run the Container in Detached Mode (Optional)
Run the container in detached mode and view logs afterward:

1. Start the container in the background:
   ```bash
   docker run -d --name node-app-container simple-node-app
   ```

2. View the logs from the running container:
   ```bash
   docker logs node-app-container
   ```

3. Stop and remove the container:
   ```bash
   docker stop node-app-container
   docker rm node-app-container
   ```

---

### Step 6: Inspect Layers and Image Structure
1. **Inspect Image Layers:**
   ```bash
   docker history simple-node-app
   ```

   - Review the layers created for each Dockerfile instruction.

2. **Inspect Image Metadata:**
   ```bash
   docker inspect simple-node-app
   ```

   - Explore metadata such as environment variables, working directory, and entry point.

---

## Expected Output
- **Interactive Mode:** Console output displays:
  ```
  Hi from the Node.js application!
  ```
- **Logs:** When running in detached mode, logs show the same output.
- **Image Inspection:** Gain insights into the layers and metadata of the image.

---

## Notes
- **Interactive Mode:** Use `-it` for real-time interaction with containers.
- **Lightweight Images:** The `node:alpine` base image keeps the container size minimal.
- **Logs and Debugging:** Logs are essential for verifying application behavior.

---

## References
- [Node.js Documentation](https://nodejs.org/en/docs/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Logs Command](https://docs.docker.com/engine/reference/commandline/logs/)

---
