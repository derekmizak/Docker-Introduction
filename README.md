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
1. **Exercise 1:** [Install Docker on your local machine.](./Session%201/Session1_Excercise1.md) 
2. **Exercise 2:** [Run the "Hello World" Docker container.](./Session%201/Session1_Excercise2.md)  
3. **Exercise 3:** [Exploring Docker commands](./Session%201/Session1_Excercise3.md)  

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
1. **Exercise 1:** [Pull and run the official Nginx image.](./Session%202/Session2_Excercise1.md)  
2. **Exercise 2:** [Explore container logs and inspect a container.](./Session%202//Session2_Excercise2.md)  
3. **Exercise 3:** [Resource Limitation with a Custom Stress Container](./Session2_Excercise3.md)  
4. **Exercise 4:** [Creating Custom Images](./Session%202//Session2_Excercise4.md)

---

## Session 3: Building Custom Docker Images

### **3.1 Introduction to Dockerfile**

Understanding Dockerfile syntax and commands

### **3.2 Creating a Dockerfile**

FROM, RUN, CMD, COPY, ENV, EXPOSE instructions

### **3.3 Building Images**

Using the docker build command

Tagging images

### Exercises:

1. **Exercise 1:** Write a Dockerfile for a simple Node.js application.
2. **Exercise 2:** Build and run your custom Docker image.
3. **Exercise 3:** Tag your image appropriately.
4. **Exercise 4:** Compre and analyze docker images on Docker Hub.


## Session 4: Dockerfile Best Practices and Optimization
### **4.1 Writing Efficient Dockerfiles**

Layer caching

Minimizing the number of layers

### **4.2 Reducing Image Size**

Using lightweight base images

Multi-stage builds

### Exercises:

1. **Exercise 1:** Optimize your Dockerfile to reduce image size.
2. **Exercise 2:** Implement multi-stage builds in your Dockerfile.
3. **Exercise 3:** Compare and analyze image sizes before and after optimization.