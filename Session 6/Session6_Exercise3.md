### **Exercise 3: Map Host Ports to Container Ports**

**Objective:**  
Learn how to map host ports to container ports and test external access to a containerized application.

**Instructions:**

1. **Run a Container with Port Mapping:**
   - Start an Nginx container with a mapped port:
     ```bash
     docker run -d -p 8080:80 --name web nginx
     ```

   - List running containers and verify port mapping:
     ```bash
     docker ps
     ```

2. **Test External Access:**
   - Open a browser and navigate to `http://localhost:8080`.
   - Verify that the Nginx welcome page is displayed.

3. **Test Port Binding with Another Port:**
   - Stop the current container:
     ```bash
     docker stop web
     ```

   - Run the Nginx container with a different host port:
     ```bash
     docker run -d -p 9090:80 --name web2 nginx
     ```

   - Access the Nginx welcome page at `http://localhost:9090`.

**Expected Outcome:**  
The Nginx container is accessible through the mapped host ports.

**Notes:**  
Port mapping allows external systems to access containerized services.
