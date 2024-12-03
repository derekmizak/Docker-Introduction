

## **Session2_Exercise2.md**


# Exercise 2: Exploring Containers

**Objective:**  
Run a container in interactive mode and explore its filesystem.

---

## **Instructions**

### 1. Run an Ubuntu Container in Interactive Mode

Start an Ubuntu container with an interactive shell.

```bash
docker run -it ubuntu /bin/bash
```

- **`-i`:** Keeps STDIN open even if not attached.
- **`-t`:** Allocates a pseudo-TTY.
- **`/bin/bash`:** Starts Bash shell inside the container.

### 2. Inside the Container

You are now inside the container's shell. Perform the following:

- **List Directory Contents:**

  ```bash
  ls
  ```

- **Check OS Version:**

  ```bash
  cat /etc/os-release
  ```

- **Update Package Lists:**

  ```bash
  apt update
  ```

- **Install `curl`:**

  ```bash
  apt install -y curl
  ```

  - The `-y` flag automatically answers 'yes' to prompts.

- **Verify `curl` Installation:**

  ```bash
  curl --version
  ```

### 3. Exit the Container

Type `exit` or press `CTRL+D` to leave the container shell.

```bash
exit
```

### 4. List Containers

List all containers, including those that have exited.

```bash
docker ps -a
```

- Note the **CONTAINER ID** of your Ubuntu container.

### 5. Restart and Attach to the Container

- **Start the Container:**

  ```bash
  docker start [CONTAINER_ID]
  ```

- **Attach to the Container:**

  ```bash
  docker attach [CONTAINER_ID]
  ```

- Replace `[CONTAINER_ID]` with the actual ID from `docker ps -a`.

### 6. Verify Persistence

- Check if `curl` is still installed:

  ```bash
  curl --version
  ```

- **Note:** Changes made inside the container are preserved as long as the container exists.

### 7. Clean Up

- **Exit the Container:**

  ```bash
  exit
  ```

- **Remove the Container:**

  ```bash
  docker rm [CONTAINER_ID]
  ```

---

## **Expected Result**

- You have experience running containers interactively.
- You understand that changes persist within the container until it is removed.
- You can start, stop, attach to, and remove containers.

---

## **Notes**

- **Interactive Mode (`-it`):** Useful for debugging and exploration.
- **Ephemeral Changes:** Unless changes are committed to a new image, they will be lost when the container is removed.
- **Container Lifecycle:** Stopped containers can be restarted, and changes remain intact until removal.

---

## **Additional Resources**

- [Docker Attach Command](https://docs.docker.com/engine/reference/commandline/attach/)
- [Docker Interactive Shells](https://docs.docker.com/engine/reference/run/#foreground)

