

### **Exercise 3: Tagging Docker Images**

**Filename:** `Session3_Exercise3.md`


# Exercise 3: Tagging Docker Images

## Objective
- Learn how to tag Docker images for better organization and version management.
- Understand how to work with tags and identify images efficiently.

---

## Instructions

### Step 1: Create a Simple Docker Image
1. Create a new directory for the exercise:
   ```bash
   mkdir tagging-exercise
   cd tagging-exercise
   ```

2. Create a `Dockerfile`:
   ```Dockerfile
   # Use a lightweight base image
   FROM alpine:latest

   # Add a simple command to demonstrate functionality
   CMD ["echo", "This is a tagged image!"]
   ```

3. Build the Docker image:
   ```bash
   docker build -t my-image .
   ```

4. Verify the image is built:
   ```bash
   docker images
   ```

   - Note the `my-image` entry without a specific version (defaults to `latest`).

---

### Step 2: Tag the Image
1. Add a version tag to the image:
   ```bash
   docker tag my-image my-image:v1.0
   ```

   - This tags the existing `my-image` as version `v1.0`.

2. Verify the tag:
   ```bash
   docker images
   ```

   - You should see two entries for `my-image`:
     - One tagged as `latest`.
     - One tagged as `v1.0`.

---

### Step 3: Add Additional Tags
1. Add more tags to represent different versions or environments:
   ```bash
   docker tag my-image my-image:stable
   docker tag my-image my-image:testing
   ```

2. Verify the new tags:
   ```bash
   docker images
   ```

   - You should now see additional entries for `my-image` with tags `stable` and `testing`.

---

### Step 4: Run Containers from Specific Tags
1. Run a container from the `v1.0` tag:
   ```bash
   docker run --rm my-image:v1.0
   ```

   - Output: `This is a tagged image!`

2. Run a container from the `stable` tag:
   ```bash
   docker run --rm my-image:stable
   ```

   - Output: `This is a tagged image!`

---

### Step 5: Inspect Image Tags
1. Inspect the `v1.0` tag to view metadata:
   ```bash
   docker inspect my-image:v1.0
   ```

2. Inspect the `stable` tag to confirm it points to the same image:
   ```bash
   docker inspect my-image:stable
   ```

   - Verify that both tags reference the same image ID.

---

## Expected Output
- Multiple tags (`latest`, `v1.0`, `stable`, `testing`) assigned to the same image.
- Containers run successfully from each tag.
- Image inspection shows that all tags point to the same image ID.

---

## Notes
- **Why Tag Images?**
  - Tags provide a way to version and identify images easily.
  - Helps distinguish between environments (e.g., `stable` vs. `testing`).
- **Tags vs. Image IDs:**
  - Tags are human-readable and easier to manage than image IDs.

---

## References
- [Docker Tag Command](https://docs.docker.com/engine/reference/commandline/tag/)
- [Docker Images Command](https://docs.docker.com/engine/reference/commandline/images/)
- [Docker Inspect Command](https://docs.docker.com/engine/reference/commandline/inspect/)

