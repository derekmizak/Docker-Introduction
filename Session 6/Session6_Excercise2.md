### **Exercise 2: Connect Multiple Containers**

**Objective:**  
Connect multiple containers to a shared network and test communication.

**Instructions:**

1. **Create a Custom Network:**
   - Create a shared custom network:
     ```bash
     docker network create shared-network
     ```

   - Verify the network was created:
     ```bash
     docker network inspect shared-network
     ```

2. **Start Containers:**
   - Run an Nginx container on the shared network:
     ```bash
     docker run -d --name web --network shared-network nginx
     ```

   - Run an Alpine container on the same network:
     ```bash
     docker run -it --rm --network shared-network alpine sh
     ```

3. **Test Connectivity:**
   - From the Alpine container, test the connection to the Nginx container:
     ```bash
     curl web
     ```

   - Verify the response from the Nginx default page.

**Expected Outcome:**  
The Alpine container can connect to the Nginx container and retrieve its default page.

**Notes:**  
This exercise demonstrates container communication on a custom network.

