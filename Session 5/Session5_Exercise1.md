

### **Exercise 1: Create and Use a Named Volume**

**Filename:** `Session5_Exercise1.md`


# Exercise 1: Create and Use a Named Volume

## Objective
- Learn to create and attach a named volume to a container.
- Observe data persistence by restarting and stopping the container.

---

## Instructions

### Step 1: Create a Named Volume
1. Create a named volume:
   ```bash
   docker volume create my-named-volume
   ```

2. Verify that the volume was created:
   ```bash
   docker volume ls
   ```

---

### Step 2: Run a Container with the Named Volume
1. Start a container with the volume:
   ```bash
   docker run -it --name volume-test -v my-named-volume:/data alpine
   ```

2. Inside the container’s shell, create a file in the `/data` directory:
   ```bash
   echo "Hello from Container A" > /data/file.txt
   ```

3. Exit the container:
   ```bash
   exit
   ```

---

### Step 3: Verify Data Persistence After Stopping the Container
1. Stop the container:
   ```bash
   docker stop volume-test
   ```

2. Confirm the container has stopped:
   ```bash
   docker ps -a
   ```

3. Inspect the volume to understand where Docker stores the data:
   ```bash
   docker volume inspect my-named-volume
   ```
   - Look for the `"Mountpoint"` field in the output, which shows where the volume is stored.

   **Platform-Specific Notes:**
   - **Linux:** The mountpoint path (e.g., `/var/lib/docker/volumes/my-named-volume/_data`) is directly accessible from the host terminal.
   - **macOS with Docker Desktop:** The path is inside the Docker VM (Linux VM) and **NOT accessible** from macOS Terminal.
   - **Windows with Docker Desktop:** The path is inside the Docker VM (WSL2 or Hyper-V) and **NOT accessible** from PowerShell/CMD. Even if you're using WSL2, the path shown is inside Docker's internal VM.

4. Verify the volume data using a temporary container (**Recommended - works on ALL platforms**):
   ```bash
   docker run --rm -v my-named-volume:/data alpine ls -la /data
   ```
   - This command mounts the volume to a temporary Alpine container and lists its contents.
   - The `--rm` flag automatically removes the container after it exits.
   - **Works identically on:** Windows (PowerShell/CMD/Git Bash), macOS (Terminal), Linux (any shell)

5. View the content of the file using a temporary container:
   ```bash
   docker run --rm -v my-named-volume:/data alpine cat /data/file.txt
   ```
   - You should see: `Hello from Container A`
   - **Windows users:** This command works in PowerShell, CMD, and Git Bash exactly as shown

**Alternative (Linux only):** If you're on a native Linux Docker installation (not Docker Desktop), you can access the volume directly:
   ```bash
   # Linux only - direct filesystem access
   sudo ls -la /var/lib/docker/volumes/my-named-volume/_data
   sudo cat /var/lib/docker/volumes/my-named-volume/_data/file.txt
   ```
   - **Note:** This does NOT work on Windows or macOS, even with Docker Desktop running Linux containers

---

### Step 4: Restart the Container and Verify Data
1. Restart the container:
   ```bash
   docker start -i volume-test
   ```

2. Inside the container, check the `/data` directory to confirm the file still exists:
   ```bash
   cat /data/file.txt
   ```

3. Exit the container:
   ```bash
   exit
   ```

---

## Expected Outcome
- Students will observe that:
  1. Data persists in the Docker-managed volume directory on the host even when the container is stopped.
  2. Restarting the container allows access to the same data without any loss.

---

## Notes
- The ability to persist data in volumes ensures reliability across container lifecycles.
- Be cautious when accessing Docker-managed volume directories directly on the host, as unintended changes could affect container behavior.

