### **Exercise: Create and Inspect Multiple Docker Networks**

**Objective:**  
Understand how to create and use multiple Docker networks, connect containers to them, and inspect their configuration and behavior.

---

#### **Instructions**

### **Step 1: Create Multiple Networks**
1. Create two custom bridge networks:
   ```bash
   docker network create NetworkX
   docker network create NetworkY
   ```

2. Verify the networks are created:
   ```bash
   docker network ls
   ```

---

### **Step 2: Run Containers on Separate Networks**
1. Start two containers on `NetworkX`:
   - Start the first container:
     ```bash
     docker run -dit --name container1 --network NetworkX alpine sh
     ```
   - Start the second container:
     ```bash
     docker run -dit --name container2 --network NetworkX alpine sh
     ```

2. Start another container on `NetworkY`:
   ```bash
   docker run -dit --name container3 --network NetworkY alpine sh
   ```

3. Verify the containers are running:
   ```bash
   docker ps
   ```

---

### **Step 3: Inspect Networks and Containers**
1. Inspect `NetworkX` and `NetworkY`:
   ```bash
   docker network inspect NetworkX
   docker network inspect NetworkY
   ```

   - Observe the containers connected to each network.
   - Take note of the IP addresses assigned to each container.

2. Ping between containers:
   - From `container1`, ping `container2` by name:
     ```bash
     docker exec -it container1 ping container2
     ```
   - Try pinging `container3` (on `NetworkY`) from `container1`:
     ```bash
     docker exec -it container1 ping container3
     ```
     - This should fail because `container1` and `container3` are on separate networks.

---

### **Step 4: Connect a Container to Multiple Networks**
1. Connect `container3` to `NetworkX` as well:
   ```bash
   docker network connect NetworkX container3
   ```

2. Verify the updated network configurations:
   ```bash
   docker network inspect NetworkX
   docker network inspect NetworkY
   ```

3. Test communication:
   - From `container3`, ping `container1` and `container2`:
     ```bash
     docker exec -it container3 ping container1
     docker exec -it container3 ping container2
     ```

---

### **Step 5: Disconnect a Container from a Network**
1. Disconnect `container3` from `NetworkX`:
   ```bash
   docker network disconnect NetworkX container3
   ```

2. Inspect the networks again to confirm:
   ```bash
   docker network inspect NetworkX
   docker network inspect NetworkY
   ```

3. Test connectivity:
   - From `container3`, try pinging `container1` again. It should fail:
     ```bash
     docker exec -it container3 ping container1
     ```

---

### **Expected Outcomes**
1. **Network Separation:** Containers on different networks cannot communicate.
2. **Shared Networks:** Connecting a container to multiple networks allows communication across those networks.
3. **Dynamic Updates:** Adding or removing a container from a network updates the network configuration instantly.

---

### **Learning outcomes**
1. How Docker manages networks and container isolation.
2. Practical usage of Docker commands for creating and inspecting networks.
3. Real-time analysis of how containers interact within and across networks.

---

### **Points to note**
- **Network Inspection:** Use `docker network inspect` to understand how containers are linked to networks.
- **Dynamic Connectivity:** Containers can dynamically join or leave networks using `docker network connect` and `docker network disconnect`.
- **Use Cases:** Understanding these concepts is critical for designing complex, multi-container applications.

