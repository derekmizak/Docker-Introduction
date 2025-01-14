

### **Exercise 3: Use a Bind Mount for Real-Time Host Access**

**Filename:** `Session5_Exercise3.md`


# Exercise 3: Use a Bind Mount for Real-Time Host Access

## Objective
- Use a bind mount to map a host directory to a container directory.
- Demonstrate real-time synchronization between the host and container.

---

## Instructions

### Step 1: Prepare the Host Directory
1. Create a directory on the host:
   ```bash
   mkdir ~/bind-mount-test
   ```

2. Add a file to the directory:
   ```bash
   echo "Hello from the Host" > ~/bind-mount-test/host-file.txt
   ```

---

### Step 2: Run a Container with the Bind Mount
1. Start a container and map the host directory to the container:
   ```bash
   docker run -it --name bind-container -v ~/bind-mount-test:/container-data alpine
   ```

2. Inside the container, list the contents of the `/container-data` directory:
   ```bash
   ls /container-data
   ```

3. View the content of the file from the host:
   ```bash
   cat /container-data/host-file.txt
   ```

---

### Step 3: Add Data from the Container
1. Inside the container, create a new file in the `/container-data` directory:
   ```bash
   echo "Hello from the Container" > /container-data/container-file.txt
   ```

2. Exit the container:
   ```bash
   exit
   ```

---

### Step 4: Verify Data on the Host
1. Check the host directory to confirm the new file exists:
   ```bash
   ls ~/bind-mount-test
   ```

2. View the content of the file added by the container:
   ```bash
   cat ~/bind-mount-test/container-file.txt
   ```

---

## Expected Outcome
- Data written to the bind mount by the container is immediately visible on the host and vice versa.

---

## Notes
- Bind mounts are useful for development, where you need real-time synchronization between the host and the container.
- Be cautious with bind mounts in production, as changes on the host directly impact the container.

