

### **Exercise 2: Share a Named Volume Between Two Containers**

**Filename:** `Session5_Exercise2.md`


# Exercise 2: Share a Named Volume Between Two Containers

## Objective
- Learn to share a named volume between two containers.
- Verify data consistency by accessing the same data from both containers.

---

## Instructions

### Step 1: Create a Named Volume
1. Create a named volume:
   ```bash
   docker volume create shared-volume
   ```

2. Verify the volume creation:
   ```bash
   docker volume ls
   ```

---

### Step 2: Start the First Container
1. Run the first container and attach the shared volume:
   ```bash
   docker run -it --name container-a -v shared-volume:/shared-data alpine
   ```

2. Inside the container, create a file in the `/shared-data` directory:
   ```bash
   echo "Hello from Container A" > /shared-data/file.txt
   ```

3. Exit the container:
   ```bash
   exit
   ```

---

### Step 3: Start the Second Container
1. Run the second container and attach the same shared volume:
   ```bash
   docker run -it --name container-b -v shared-volume:/shared-data alpine
   ```

2. Inside the container, list the contents of the `/shared-data` directory:
   ```bash
   ls /shared-data
   ```

3. View the content of the shared file:
   ```bash
   cat /shared-data/file.txt
   ```

4. Add a new file:
   ```bash
   echo "Hello from Container B" > /shared-data/file-b.txt
   ```

5. Exit the container:
   ```bash
   exit
   ```

---

### Step 4: Verify Data from the First Container
1. Start the first container again:
   ```bash
   docker start -i container-a
   ```

2. Check the `/shared-data` directory to confirm the new file exists:
   ```bash
   ls /shared-data
   ```

3. View the content of the new file:
   ```bash
   cat /shared-data/file-b.txt
   ```

4. Exit the container:
   ```bash
   exit
   ```

---

## Expected Outcome
- Data written by one container is visible to the other container, demonstrating data consistency with shared volumes.

---

## Notes
- Named volumes are useful for sharing persistent data between containers, such as configuration files or databases.
- Always use appropriate permissions and security controls when sharing volumes.

