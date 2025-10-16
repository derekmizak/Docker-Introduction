
## **Session1_Exercise3.md**


# Exercise 3: Exploring Docker Commands

**Objective:**  
Familiarize yourself with basic Docker commands to explore and understand your Docker environment.

---

## **Instructions**

### 1. Check Docker Version and System Information

- **Docker Version:**

  ```bash
  docker version
  ```

- **Docker System Information:**

  ```bash
  docker info
  ```

### 2. List Available Docker Commands

- Display general help:

  ```bash
  docker help
  ```

### 3. Use the Help Option for Specific Commands

- Get help for the `run` command:

  ```bash
  docker run --help
  ```

- Get help for the `images` command:

  ```bash
  docker images --help
  ```

### 4. Document Key Information

- **Record the Following:**
  - Docker **Client** and **Server** versions.
  - **Storage Driver** in use (e.g., overlay2, aufs).
  - Number of **Images** and **Containers** present.
  - Operating System and Kernel version.

### 5. Explore Additional Docker Commands

- **Monitor Resource Usage:**

  ```bash
  docker stats
  ```

- **Inspect an Image or Container:**

  ```bash
  docker inspect [IMAGE_OR_CONTAINER]
  ```

  - Replace `[IMAGE_OR_CONTAINER]` with an image name or container ID.

- **View Image History:**

  ```bash
  docker history [IMAGE]
  ```

### 6. Optional: Try Running a Detached Container

- Run an Nginx container in detached mode:

  ```bash
  docker run -d -p 8080:80 nginx
  ```

- Access Nginx in your browser at `http://localhost:8080`.

- Stop and remove the container:

  ```bash
  docker stop [CONTAINER_ID]
  docker rm [CONTAINER_ID]
  ```

---

## **Expected Result**

- **Command Proficiency:**
  - You can use Docker commands to retrieve information and manage containers.
- **Environment Understanding:**
  - Awareness of your Docker setup and configuration.
- **Hands-On Experience:**
  - Running and managing containers using various commands.

---

## **Notes**

- **Getting Help:**
  - Use the `--help` flag with any Docker command to learn about its usage.
- **Container IDs and Names:**
  - Use `docker ps` and `docker ps -a` to find container IDs and names.
- **Cleaning Up:**
  - Remove unused containers and images to free up system resources.

---

## **Additional Resources**

- [Docker Command-Line Interface (CLI) Reference](https://docs.docker.com/engine/reference/commandline/docker/)
- [Managing Docker Containers](https://docs.docker.com/config/containers/)

---

