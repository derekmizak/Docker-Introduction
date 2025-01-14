# Docker Introduction

This repository includes course material for the **Docker Introduction** course. The course is designed for beginners.

### **Notes:**
This course is designed to provide hands-on experience with Docker. Make sure to complete all exercises to reinforce your learning.

---

## **Session 1: Introduction to Docker**

### **1.1 What is Docker?**
- Understanding containers vs. virtual machines
- Benefits of containerization

### **1.2 Docker Architecture**
- Docker Engine, Docker Daemon, and Docker Client
- Images, Containers, Registries

### **1.3 Installing Docker**
- Setting up Docker on Windows, macOS, and Linux
- Verifying installation

### **Exercises:**
1. **Exercise 1:** [Install Docker on your local machine.](./Session%201/Session1_Exercise1.md)
2. **Exercise 2:** [Run the "Hello World" Docker container.](./Session%201/Session1_Exercise2.md)
3. **Exercise 3:** [Exploring Docker commands](./Session%201/Session1_Exercise3.md)

---

## **Session 2: Working with Docker Images and Containers**

### **2.1 Docker Images**
- Pulling images from Docker Hub
- Understanding image layers

### **2.2 Docker Containers**
- Running your first container
- Interactive vs. detached modes

### **2.3 Managing Containers**
- Starting, stopping, and restarting containers
- Viewing container logs
- Removing containers and images

### **2.4 Building Custom Images**

### **Exercises:**
1. **Exercise 1:** [Pull and run the official Nginx image.](./Session%202/Session2_Exercise1.md)
2. **Exercise 2:** [Explore container logs and inspect a container.](./Session%202/Session2_Exercise2.md)
3. **Exercise 3:** [Resource Limitation with a Custom Stress Container](./Session%202/Session2_Exercise3.md)
4. **Exercise 4:** [Creating Custom Images](./Session%202/Session2_Exercise4.md)

---

## **Session 3: Building Custom Docker Images**

### **3.1 Introduction to Dockerfile**
- Understanding Dockerfile syntax and commands

### **3.2 Creating a Dockerfile**
- FROM, RUN, CMD, COPY, ENV, EXPOSE instructions

### **3.3 Building Images**
- Using the docker build command
- Tagging images

### **Exercises:**
1. **Exercise 1:** [Write a Dockerfile for a simple Node.js application.](./Session%203/Session3_Exercise1.md)
2. **Exercise 2:** [Build and run your custom Docker image.](./Session%203/Session3_Exercise2.md)
3. **Exercise 3:** [Tag your image appropriately.](./Session%203/Session3_Exercise3.md)
4. **Exercise 4:** [Compare and analyze Docker images on Docker Hub.](./Session%203/Session3_Exercise4.md)


---

## **Session 4: Dockerfile Best Practices and Optimization**

### **4.1 Writing Efficient Dockerfiles**
- Layer caching
- Minimizing the number of layers

### **4.2 Reducing Image Size**
- Using lightweight base images
- Multi-stage builds

### **Exercises:**
1. **Exercise 1:** [Install a Specific Node.js Version on Alpin](./Session%204/Session4_Exercise1.md)
2. **Exercise 2:** [Multi-Stage Builds with Consistent Base and Custom Image](./Session%204/Session4_Exercise2.md)
3. **Exercise 3:** [Comparing Python Images with and Without Multi-Stage Builds](./Session%204/Session4_Exercise3.md)
4. **Exercise 4:** [Using ENTRYPOINT Comman](./Session%203/Session4_Exercise4.md)
5. **Exercise 5:** [Optimize your Dockerfile to reduce image size.](./Session%203/Session4_Exercise5.md)

---

## **Session 5: Data Management with Volumes**

### **5.1 Understanding Volumes**
- Data persistence in Docker

### **5.2 Types of Volumes**
- Named volumes vs. bind mounts

### **5.3 Using Volumes**
- Creating and mounting volumes
- Sharing data between containers

### **Exercises:**
1. **Exercise 1:** [Create a container with a bind mount to your local filesystem.](./Session%205/Session5_Exercise1.md)
2. **Exercise 2:** [Modify data in the volume and observe changes.](./Session%205/Session5_Exercise2.md)
3. **Exercise 3:** [Share a named volume between two containers and test data consistency.](./Session%205/Session5_Exercise3.md)

## **Session 6: Networking and Port Management**
### **6.1 Docker Networking Basics**

- Docker netowrking theory - CNM, Libnetwork, and drivers
- Container communication

### **6.2 Network Drivers**

- Bridge, host, and overlay networks

### **6.3 Managing Ports**

- Exposing and publishing container ports

- Port mapping with -p and -P options

### **6.4 Custom Networks**

- Creating user-defined networks

- Linking containers

### **Exercises:***

Exercise 1: [Create a custom bridge network.](./Session%206/Session6_Exercise1.md)

Exercise 2: [Connect multiple containers on the same network.](./Session%206/Session6_Exercise2.md)

Exercise 3: [Map host ports to container ports and test connectivity.](./Session%206/Session6_Exercise3.md)

Exercise 4: [Testing inter container communication acrose the networks](./Session%206/Session6_Exercise4.md)
