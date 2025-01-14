


### **Exercise 2: Multi-Stage Builds with Consistent Base and Custom Image**

**Filename:** `Session4_Exercise2.md`


# Exercise 2: Multi-Stage Builds with Node.js

## Objective
- Use multi-stage builds to separate the build environment from the runtime environment.
- Build a custom Node.js image.

---

## Instructions

### Step 1: Multi-Stage Build with `node:lts-slim`
1. Create a `Dockerfile` with a consistent runtime and build base:
   ```Dockerfile
   # Build stage
   FROM node:lts-slim AS build-stage
   WORKDIR /app
   COPY package.json ./
   RUN npm install
   COPY . .

   # Runtime stage
   FROM node:lts-slim
   WORKDIR /app
   COPY --from=build-stage /app /app
   CMD ["node", "app.js"]
   ```

2. Build the image:
   ```bash
   docker build -t multi-stage-node-app .
   ```

3. Run the container:
   ```bash
   docker run -it --rm multi-stage-node-app
   ```

---

### Step 2: Build Your Own Custom Node.js Image from `alpine:slim`
1. Write a new multi-stage `Dockerfile`:
   ```Dockerfile
   # Build stage
   FROM alpine:slim AS build-stage

   # Install dependencies
   RUN apk add --no-cache curl bash libc6-compat && \
       curl -fsSL https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz | tar -xJ -C /usr/local --strip-components=1

   # Set the working directory
   WORKDIR /app

   # Copy application files
   COPY package.json ./
   RUN npm install
   COPY . .

   # Runtime stage
   FROM alpine:slim
   WORKDIR /app
   COPY --from=build-stage /app /app
   CMD ["node", "app.js"]
   ```

2. Build the custom image:
   ```bash
   docker build -t custom-node-alpine .
   ```

3. Run the container:
   ```bash
   docker run -it --rm custom-node-alpine
   ```

Confirm that the Node.js application runs successfully. There is no need to expose a port for this exercise. In case if the application requires a port, you can add the `EXPOSE` instruction in the `Dockerfile`. In case if container didnt start successfully, you can use `docker logs <container_id>` to view the logs and troubleshoot. Possibly the node architecture might not be compatible with the host machine, in such case adjust acordingly.

---

### Step 3: Compare the Images
1. Compare the size of the following images:
   - Official `node:lts-slim`
   - Multi-stage `multi-stage-node-app`
   - Custom `custom-node-alpine`

2. Use `docker images` to list sizes:
   ```bash
   docker images
   ```

3. Discuss:
   - How does the size of the custom Alpine-based image compare to `node:lts-slim`?
   - What are the trade-offs of using a custom base versus an official image?

---

## Expected Outcome
- Successfully build own Node.js image starting from `alpine:slim`.
- Observation how multi-stage builds and a minimal base reduce image size.
- Understanding the trade-offs between custom images and official images.
