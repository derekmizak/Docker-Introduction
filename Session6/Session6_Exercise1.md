Here are the activities for **Session 6: Networking and Port Management** presented in plain text format:
### **Exercise 1: Create a Custom Bridge Network**

**Objective:**  
Learn how to create and use a custom Docker network for container communication.

**Instructions:**

1. **Create a Custom Bridge Network:**
   - Run the following command to create a custom bridge network:
     ```bash
     docker network create my-bridge-network
     ```

   - Verify that the network was created by listing all networks:
     ```bash
     docker network ls
     ```

2. **Run Containers on the Custom Network:**
   - Run a container on the custom network:
     ```bash
     docker run -it --rm --network my-bridge-network --name container1 alpine sh
     ```

   - Run another container on the same network:
     ```bash
     docker run -it --rm --network my-bridge-network --name container2 alpine sh
     ```

3. **Test Communication:**
   - From `container1`, ping `container2` using its container name:
     ```bash
     ping container2
     ```

   - Exit the containers after testing:
     ```bash
     exit
     ```

**Expected Outcome:**  
Containers on the same network can communicate using their names.

**Notes:**  
Custom networks provide better isolation and container-to-container communication than the default bridge network.

