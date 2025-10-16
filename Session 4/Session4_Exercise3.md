

### **Exercise 3: Comparing Python Images with and Without Multi-Stage Builds**

**Filename:** `Session4_Exercise3.md`


# Exercise 3: Comparing Python Images with and Without Multi-Stage Builds

## Objective
- Build a lightweight Python image using both non-multi-stage and multi-stage builds.
- Compare the sizes of the custom-built images with the official `python:slim` image.

---

## Instructions

### Step 1: Create a Simple Python Application
1. Create a directory for your project:
   ```bash
   mkdir compare-python-images
   cd compare-python-images
   ```

2. Create the following file:
   - **`app.py`:**
     ```python
     print("Hello from a Python app running on Alpine!")
     ```

---

### Step 2: Pull the Official `python:slim` Image
1. Pull the official `python:slim` image:
   ```bash
   docker pull python:slim
   ```

2. Verify the image size:
   ```bash
   docker images python:slim
   ```

---

### Step 3: Create a Non-Multi-Stage Dockerfile
1. Write a `Dockerfile` for a non-multi-stage build:
   ```Dockerfile
   FROM alpine:latest

   # Install Python and build dependencies
   RUN apk add --no-cache python3 py3-pip

   # Set the working directory
   WORKDIR /app

   # Copy the Python application
   COPY app.py ./

   # Set the default command
   CMD ["python3", "app.py"]
   ```

2. Build the image:
   ```bash
   docker build -t alpine-python-nonmultistage .
   ```

3. Run the container:
   ```bash
   docker run -it --rm alpine-python-nonmultistage
   ```

---

### Step 4: Create a Multi-Stage Dockerfile
1. Write a `Dockerfile` for a multi-stage build:
   ```Dockerfile
   # Build stage
    FROM alpine:latest AS build-stage

    # Install Python, pip, and build dependencies
    RUN apk add --no-cache python3

    # Set the working directory
    WORKDIR /app

    # Copy the Python application
    COPY app.py ./

    # Runtime stage
    FROM alpine:latest

    # Install only the Python runtime
    RUN apk add --no-cache python3

    # Copy the application files
    WORKDIR /app
    COPY --from=build-stage /app /app

    # Set the default command
    CMD ["python3", "app.py"]

    ```
2. Build the image:
   ```bash
   docker build -t alpine-python-multistage .
   ```

3. Run the container:
   ```bash
   docker run -it --rm alpine-python-multistage
   ```
---

### Step 5: Compare Image Sizes
1. Compare the sizes of the following images:
   - Official `python:slim`
   - Custom `alpine-python-nonmultistage`
   - Custom `alpine-python-multistage`

2. Use the `docker images` command:
   ```bash
   docker images
   ```

3. Record your findings in a table:

| **Image**                 | **Size**  |
|---------------------------|-----------|
| `python:slim`             | XX MB     |
| `alpine-python-nonmultistage` | XX MB     |
| `alpine-python-multistage`    | XX MB     |

---

### Step 6: Analyze Image Layers
1. Inspect the layers of each image:
   - For the official image:
     ```bash
     docker history python:slim
     ```
   - For the non-multi-stage image:
     ```bash
     docker history alpine-python-nonmultistage
     ```
   - For the multi-stage image:
     ```bash
     docker history alpine-python-multistage
     ```

2. Discuss:
   - How many layers are in each image?
   - How does the use of a multi-stage build affect the number of layers and overall size?

---

## Expected Outcome
- **Official `python:slim`:**
  - Larger size but includes pre-configured tools for convenience.
- **Custom `alpine-python-nonmultistage`:**
  - Smaller than `python:slim` but larger than the multi-stage build due to included build dependencies.
- **Custom `alpine-python-multistage`:**
  - Smallest size by excluding build-time dependencies.

---

## Discussion Points
- **Trade-Offs:**
  - **Convenience:** `python:slim` is ready-to-use and suitable for general-purpose tasks.
  - **Customizability:** Custom Alpine-based images provide flexibility and smaller sizes but require additional setup.
- **Optimization Techniques:**
  - Multi-stage builds demonstrate effective optimization by separating build and runtime environments.

---

## Notes
- Multi-stage builds are particularly beneficial for applications with complex dependencies, such as compiled languages or frameworks.
- Always evaluate the trade-offs between convenience, size, and customization when choosing a base image.

---
```

---

### **Key Learning Points**
1. **Size Analysis:** Students directly compare and understand size differences between official and custom images.
2. **Optimization Techniques:** Multi-stage builds effectively reduce image size by excluding unnecessary dependencies.
3. **Trade-Offs:** This exercise highlights the balance between convenience (`python:slim`) and minimalism (custom Alpine images).

Let me know if you'd like further adjustments!