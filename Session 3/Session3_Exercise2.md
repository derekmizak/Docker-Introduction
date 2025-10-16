

### **Exercise 2: Optimizing a Custom Docker Image**

**Filename:** `Session3_Exercise2.md`


# Exercise 2: Optimizing a Custom Docker Image

## Objective
- Create a custom Docker image with multiple layers by running separate commands.
- Optimize the Dockerfile by combining commands to reduce the number of layers.
- Compare the layers of both images and understand the benefits of fewer layers.

---

## Instructions

### Step 1: Build an Initial Docker Image with Separate Commands
1. Create a new directory for your project:
   ```bash
   mkdir layered-image
   cd layered-image
   ```

2. Create a `Dockerfile` with the following content:
   ```Dockerfile
   # Use a lightweight base image
   FROM debian:stable-slim

   # Update package lists
   RUN apt-get update

   # Install curl
   RUN apt-get install -y curl

   # Install vim
   RUN apt-get install -y vim
   ```

Go to Docker Hub and review the [Debian Docker image](https://hub.docker.com/_/debian) to understand the available tags and options.
Please review status of the Debian image on Docker Hub to ensure the tag `stable-slim` is available.
Please note when the image was last updated by the minatainer. What is the size of the image? What status doe the image has - is it miantained by a reputable entity? Are there any vunerabilities reported for the image?

3. Build the image:
   ```bash
   docker build -t layered-image .
   ```

4. Inspect the layers of the image:
   ```bash
   docker history layered-image
   ```

   - Note the number of layers created by separate `RUN` commands.

---

### Step 2: Optimize the Dockerfile by Combining Commands
1. Edit the `Dockerfile` to combine the `RUN` instructions:
   ```Dockerfile
   # Use a lightweight base image
   FROM debian:stable-slim

   # Combine commands to minimize layers
   RUN apt-get update && \
       apt-get install -y curl vim && \
       rm -rf /var/lib/apt/lists/*
   ```

   **Explanation:**
   - **`&&`:** Chains commands together to execute in a single layer.
   - **`rm -rf /var/lib/apt/lists/*`:** Cleans up unnecessary files to reduce image size.

2. Build the optimized image:
   ```bash
   docker build -t optimized-image .
   ```

3. Inspect the layers of the optimized image:
   ```bash
   docker history optimized-image
   ```

---

### Step 3: Compare the Two Images
1. List both images:
   ```bash
   docker images
   ```

   - Observe the difference in image sizes.

2. Inspect the layers of both images:
   ```bash
   docker history layered-image
   docker history optimized-image
   ```

   - Note the reduced number of layers in the optimized image.

---

### Step 4: Run a Container from the Optimized Image

1. Start a container from the optimized image:
   ```bash
   docker run -it --rm optimized-image bash
   ```

2. Verify that `curl` and `vim` are installed:
   ```bash
   curl --version
   vim --version
   ```

---

## Expected Output
- The initial image (`layered-image`) has more layers and a larger size.
- The optimized image (`optimized-image`) has fewer layers and a smaller size.
- Both images function identically, with `curl` and `vim` installed.

---

## Notes
- **Why Reduce Layers?**
  - Fewer layers result in smaller images, faster builds, and quicker downloads.
  - Simplifies image maintenance by consolidating related commands.
- **Cleanup:** Always remove temporary files to avoid bloating the image.

---

## References
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Inspecting Docker Images](https://docs.docker.com/engine/reference/commandline/inspect/)
- [Docker History Command](https://docs.docker.com/engine/reference/commandline/history/)

