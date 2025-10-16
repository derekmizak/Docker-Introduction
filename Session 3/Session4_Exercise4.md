

### **Exercise 4: Comparing Docker Images**

**Filename:** `Session3_Exercise4.md`

# Exercise 4: Comparing Docker Images

## Objective
- Compare the size, number of packages, and vulnerabilities of three popular Docker images.
- Discuss the purpose and best use cases for each image.

---

## Instructions

### Step 1: Pull the Images
1. Pull the following images from Docker Hub:
   ```bash
   docker pull alpine:latest
   docker pull ubuntu:latest
   docker pull debian:stable-slim
   ```

2. Verify the images have been pulled:
   ```bash
   docker images
   ```

---

### Step 2: Compare Image Sizes
1. Note the size of each image from the `docker images` output.
2. Record your findings in a table like this:

| Image            | Size       |
|-------------------|------------|
| `alpine:latest`  | XX MB      |
| `ubuntu:latest`  | XX MB      |
| `debian:stable-slim` | XX MB  |

---

### Step 3: Inspect Installed Packages
1. Run a container from each image interactively:
   ```bash
   docker run -it --rm alpine:latest sh
   docker run -it --rm ubuntu:latest bash
   docker run -it --rm debian:stable-slim bash
   ```

2. Inside each container, list the installed packages:
   - For Alpine:
     ```bash
     apk list
     ```
   - For Ubuntu and Debian:
     ```bash
     dpkg -l
     ```

3. Record the approximate number of packages installed in each image:

| Image            | Approx. Number of Packages |
|-------------------|----------------------------|
| `alpine:latest`  | XX                         |
| `ubuntu:latest`  | XX                         |
| `debian:stable-slim` | XX                     |

---

### Step 4: Check Vulnerabilities on Docker Hub
1. Open the Docker Hub website in your browser:
   - [Alpine](https://hub.docker.com/_/alpine)
   - [Ubuntu](https://hub.docker.com/_/ubuntu)
   - [Debian](https://hub.docker.com/_/debian)

2. Navigate to the **Tags** section for each image.

3. Look for security-related metrics, including the number of vulnerabilities associated with each tag.

4. Record your findings in a table:

| Image            | Number of Vulnerabilities |
|-------------------|---------------------------|
| `alpine:latest`  | XX                        |
| `ubuntu:latest`  | XX                        |
| `debian:stable-slim` | XX                    |

---

### Step 5: Discuss the Purpose of Each Image
Based on your findings, discuss in small groups or individually:
1. What are the likely use cases for each image?
   - **Alpine:** Minimal base image, often used for microservices or lightweight applications.
   - **Ubuntu:** General-purpose base image, suitable for applications requiring more dependencies.
   - **Debian Slim:** Smaller Debian-based image, balancing minimalism with compatibility.

2. Consider:
   - How image size impacts performance and storage.
   - Whether the number of installed packages affects security.
   - When to prioritize minimalism versus feature-richness.

---

## Expected Output
1. A completed table comparing image sizes, installed packages, and vulnerabilities.
2. A summary of the likely use cases for each image.

---

## Notes
- **Image Size Matters:**
  - Smaller images reduce build and pull times.
  - Large images may be necessary for complex applications.
- **Packages and Security:**
  - More packages can increase functionality but also introduce vulnerabilities.
- **Purpose of Comparison:**
  - Helps choose the right base image for your application needs.

---

## References
- [Alpine Docker Hub](https://hub.docker.com/_/alpine)
- [Ubuntu Docker Hub](https://hub.docker.com/_/ubuntu)
- [Debian Docker Hub](https://hub.docker.com/_/debian)

