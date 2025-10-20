# Docker Introduction - 2025 Edition

This repository includes course material for the **Docker Introduction** course. The course is designed for beginners and follows **2025 industry best practices** including security, optimization, and production deployment.

### **📋 Course Information:**
- **Duration:** 16+ hours (6+ hours lectures + 10+ hours hands-on exercises)
- **Level:** Beginner to Intermediate
- **Updated:** October 2025
- **Includes:** Security scanning, distroless images, BuildKit optimization, Docker Compose v2, comprehensive quick references

### **🎯 Learning Outcomes:**
By the end of this course, you will be able to:
- Build and deploy production-ready Docker containers
- Implement security best practices and vulnerability scanning
- Optimize Docker images for size and performance
- Create multi-container applications with Docker Compose
- Deploy applications using CI/CD pipelines

### **📚 Important Notes:**
- This course uses **Docker Compose v2** syntax (no `version:` field required)
- All exercises follow **2025 security and optimization best practices**
- Security scanning with **Docker Scout** is integrated throughout
- Make sure to complete all exercises to reinforce your learning

### **📖 Additional Resources:**
- Official Docker Documentation: https://docs.docker.com/

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
4. **Exercise 4 (NEW):** [Docker 2025 Features & Modern Tooling](./Session%201/Session1_Exercise4_2025.md) ⭐

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

## **Session 4: Dockerfile Best Practices and Optimization (2025 Update)**

### **4.1 Writing Efficient Dockerfiles**
- Layer caching strategies
- Minimizing the number of layers
- BuildKit cache optimization

### **4.2 Reducing Image Size**
- Using lightweight base images (Alpine, Slim)
- Multi-stage builds
- Distroless images for production

### **4.3 Security and Performance (NEW)**
- Vulnerability scanning with Docker Scout
- Choosing secure base images
- BuildKit advanced features

### **Exercises:**
1. **Exercise 1:** [Install a Specific Node.js Version on Alpine](./Session%204/Session4_Exercise1.md)
2. **Exercise 2:** [Multi-Stage Builds with Consistent Base and Custom Image](./Session%204/Session4_Exercise2.md)
3. **Exercise 3:** [Comparing Python Images with and Without Multi-Stage Builds](./Session%204/Session4_Exercise3.md)
4. **Exercise 4:** [Using ENTRYPOINT Command](./Session%203/Session3_Exercise4.md)
5. **Exercise 5:** [Optimize your Dockerfile to reduce image size](./Session%204/Session4_Exercise5.md)
6. **Exercise 6 (NEW):** [Vulnerability Scanning with Docker Scout](./Session%204/Session4_Exercise6.md) 🔒
7. **Exercise 7 (NEW):** [Implementing Distroless Images for Maximum Security](./Session%204/Session4_Exercise7.md) 🔒
8. **Exercise 8 (NEW):** [BuildKit Cache Optimization for Faster Builds](./Session%204/Session4_Exercise8.md) ⚡

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
4. **Exercise 4 (NEW):** [Using tmpfs Mounts for Temporary Data](./Session%205/Session5_Exercise4.md) 🔒
5. **Exercise 5 (NEW):** [Volume Backup and Restore Strategies](./Session%205/Session5_Exercise5.md) 💾

## **Session 6: Networking and Port Management**
### **6.1 Docker Networking Basics**

- Docker networking theory - CNM, Libnetwork, and drivers
- Container communication

### **6.2 Network Drivers**

- Bridge, host, and overlay networks

### **6.3 Managing Ports**

- Exposing and publishing container ports

- Port mapping with -p and -P options

### **6.4 Custom Networks**

- Creating user-defined networks

- Linking containers

### **Exercises:**

Exercise 1: [Create a custom bridge network.](./Session6/Session6_Exercise1.md)

Exercise 2: [Connect multiple containers on the same network.](./Session6/Session6_Exercise2.md)

Exercise 3: [Map host ports to container ports and test connectivity.](./Session6/Session6_Exercise3.md)

Exercise 4: [Testing inter container communication across the networks](./Session6/Session6_Exercise4.md)

---

## **Session 7: Docker Compose for Multi-Container Applications (2025 Update)**

### **7.1 Introduction to Docker Compose**
- What is Docker Compose?
- When to use Docker Compose
- Docker Compose v2 (Modern Syntax - No `version:` field)

### **7.2 docker-compose.yml Structure**
- Services, networks, and volumes
- Environment variables and .env files
- Service dependencies with conditions

### **7.3 Production-Ready Configurations (NEW)**
- Health checks and service readiness
- Resource limits and reservations
- Logging configuration
- Restart policies

### **7.4 Managing Multi-Container Applications**
- Building and running services
- Scaling services
- Viewing logs and debugging

### **Exercises:**

Exercise 1: [Create a Multi-Container Application with Docker Compose](./Session%207-8/Session7_Exercise1.md)

Exercise 2: [Implement Environment-Specific Configurations](./Session%207-8/Session7_Exercise2.md)

Exercise 3: [Scaling Services in Docker Compose](./Session%207-8/Session7_Exercise3.md)

Exercise Final: [Complete Production-Ready Application with Node.js and PostgreSQL](./Session%207-8/Session7_Exercise_final.md) ⭐

**Sample Project:** [docker-sample/](./Session%207-8/docker-sample/) - Complete working example with production best practices

---

## **Session 8: Security & Best Practices (NEW - 2025)**

### **8.1 Container Security Fundamentals**
- Attack surface reduction
- Defense in depth
- Security by design principles

### **8.2 Image Security**
- Vulnerability scanning workflows
- Distroless and minimal images
- Secure base image selection
- SBOM (Software Bill of Materials)

### **8.3 Dockerfile Security**
- Running as non-root user
- Handling secrets securely
- Minimizing attack surface
- Security linting

### **8.4 Runtime Security**
- Linux capabilities management
- Read-only filesystems
- Seccomp and AppArmor
- Resource limits as security

### **8.5 Secrets Management**
- Docker Compose secrets
- BuildKit secret mounts
- External secrets managers
- Secret rotation strategies

### **Exercises:**

Exercise 1: [Complete Image Security Workflow](./Session%208/Session8_Exercise1.md) 🔐

Exercise 2: [Dockerfile Security Best Practices](./Session%208/Session8_Exercise2.md) 🛡️

Exercise 3: [Runtime Security and Container Hardening](./Session%208/Session8_Exercise3.md) 🔒

Exercise 4: [Secrets Management in Docker Compose](./Session%208/Session8_Exercise4.md) 🔑

**Key Outcomes:**
- ✅ Scan and fix image vulnerabilities
- ✅ Write production-grade secure Dockerfiles
- ✅ Harden containers at runtime
- ✅ Manage secrets properly
- ✅ Achieve 80-90% CVE reduction

---

## **📖 Quick Reference Resources (NEW)**

Comprehensive guides and templates to help you master Docker:

### **Essential Reference Guides:**

1. **[Docker CLI Quick Reference](./Resources/Docker-CLI-Quick-Reference.md)** 📝
   - All essential Docker commands organized by category
   - Modern syntax (2025 edition)
   - Includes troubleshooting quick reference
   - One-liners and useful aliases

2. **[Dockerfile Best Practices Checklist](./Resources/Dockerfile-Best-Practices-Checklist.md)** ✅
   - Security checklist (non-root users, secrets, scanning)
   - Performance optimization checklist (multi-stage, caching)
   - Production reliability checklist (healthchecks, signals)
   - Complete production-ready example

3. **[Docker Compose Syntax Guide](./Resources/Docker-Compose-Syntax-Guide.md)** 🔧
   - Complete docker-compose.yml reference (v2 syntax)
   - All service configuration options explained
   - Production-ready examples
   - Common patterns and best practices

4. **[Docker Troubleshooting Guide](./Resources/Docker-Troubleshooting-Guide.md)** 🔍
   - Common issues and solutions
   - Debugging step-by-step approach
   - Container, networking, volume issues
   - Platform-specific troubleshooting

5. **[.dockerignore Templates](./Resources/dockerignore-template.md)** 🚫
   - Universal template for all projects
   - Language-specific templates (Node.js, Python, Go, Java, .NET, PHP)
   - Framework-specific templates (React, Vue, Django)
   - Security-focused template

6. **[Distroless Images Complete Guide](./Resources/Distroless-Images-Guide.md)** 🔐
   - All distroless providers (Google, Chainguard, Red Hat, Canonical)
   - Size and security comparisons
   - When to use what (decision trees)
   - Practical examples for all languages
   - Debugging distroless containers
   - Migration guide from Alpine

**These resources are designed to be printed and kept handy while working with Docker!**

---

## **🔐 Security & Best Practices (Integrated Throughout)**

The 2025 edition of this course integrates security and best practices across all sessions:

### **Security Topics Covered:**
- ✅ Vulnerability scanning with Docker Scout (Session 4)
- ✅ Distroless images for minimal attack surface (Session 4)
- ✅ Running containers as non-root users (Sessions 3-4)
- ✅ Secrets management in Docker Compose (Session 7-8)
- ✅ Resource limits and isolation (Sessions 2, 7-8)
- ✅ Secure base image selection (Session 4)

### **Optimization Topics Covered:**
- ✅ BuildKit cache optimization (Session 4)
- ✅ Multi-stage builds (Session 4)
- ✅ Image size reduction techniques (Session 4)
- ✅ Build performance improvement (Session 4)
- ✅ Production-grade healthchecks (Session 7-8)
- ✅ Logging and monitoring setup (Session 7-8)

---

## **📊 Course Improvements (2025 Edition)**

This course has been updated with modern Docker practices:

### **✨ What's New:**

1. **Docker Compose v2 Syntax** - All compose files updated to remove obsolete `version:` field
2. **Security Integration** - 3 new exercises on vulnerability scanning, distroless images, and Docker Scout
3. **Production Best Practices** - Enhanced health checks, resource limits, logging configuration
4. **BuildKit Optimization** - New exercise on cache mounts and build performance
5. **Modern Image Security** - Distroless images, non-root users, minimal attack surface
6. **Updated Dependencies** - Using specific versions (e.g., `postgres:16-alpine` instead of `latest`)

### **🔄 Updated Content:**

| Session | Updates | New Exercises |
|---------|---------|---------------|
| Session 1 | 2025 context, Docker Scout, AI, licensing | **+1 exercise** (2025 Features) |
| Session 2 | Resource limits emphasis | 0 |
| Session 3 | Security best practices | 0 |
| Session 4 | **Major update** | **+3 exercises** (Scout, Distroless, BuildKit) |
| Session 5 | Enhanced volume management | **+2 exercises** (tmpfs, backup/restore) |
| Session 6 | DNS and networking details | 0 |
| Session 7 | **Major update** - Healthchecks, compose v2 | Updated all exercises |
| **Session 8 (NEW)** | **Complete security session** | **+4 exercises** (Comprehensive security) |
| **Resources (NEW)** | **Quick reference guides & templates** | **5 comprehensive guides** |

### **📈 Learning Hours:**
- **Lectures:** 6+ hours
- **Hands-on Exercises:** 10+ hours
- **Quick References:** Self-paced (always accessible)
- **Total:** 16+ hours of comprehensive Docker education

---

## **🚀 Getting Started**

### **Prerequisites:**
- Computer running Windows 10/11, macOS, or Linux
- At least 4GB RAM available for Docker
- Basic command line familiarity
- Text editor or IDE

### **Installation:**
1. Follow [Session 1 Exercise 1](./Session%201/Session1_Exercise1.md) for Docker installation
2. Verify installation: `docker --version` and `docker compose version`
3. Ensure BuildKit is enabled (default in Docker 23+)

### **Recommended Path:**
1. Complete sessions in order (1 → 8)
2. Do all exercises for each session before moving forward
3. Experiment with variations of exercises
4. Build your own projects to reinforce learning

---

## **💡 Tips for Success**

1. **Practice Regularly** - Docker skills improve with hands-on experience
2. **Read Error Messages** - Docker provides helpful error messages
3. **Use Documentation** - Official Docker docs are excellent
4. **Scan Your Images** - Always run `docker scout cves` before deploying
5. **Start Small** - Master basics before moving to complex setups
6. **Ask Questions** - Engage with the Docker community

---

## **🎓 After This Course**

After completing this course, you'll be ready to:
- Deploy real-world applications with Docker
- Implement CI/CD pipelines with Docker
- Understand container orchestration concepts (Kubernetes basics)
- Apply Docker to various programming languages and frameworks
- Pass Docker-related technical interviews

### **Next Steps:**
- Explore Kubernetes for container orchestration
- Learn about CI/CD with GitHub Actions and Docker
- Study advanced networking and service mesh concepts
- Investigate cloud-native deployment patterns
- Build and deploy your own containerized projects

---

## **📚 Additional Learning Resources**

### **Course Resources (Essential):**
- **[Docker CLI Quick Reference](./Resources/Docker-CLI-Quick-Reference.md)** - All commands at your fingertips
- **[Dockerfile Best Practices Checklist](./Resources/Dockerfile-Best-Practices-Checklist.md)** - Production-ready Dockerfiles
- **[Docker Compose Syntax Guide](./Resources/Docker-Compose-Syntax-Guide.md)** - Complete compose reference
- **[Troubleshooting Guide](./Resources/Docker-Troubleshooting-Guide.md)** - Fix common issues quickly
- **[.dockerignore Templates](./Resources/dockerignore-template.md)** - For all project types
- **[Distroless Images Guide](./Resources/Distroless-Images-Guide.md)** - All distroless providers & best practices
- **[Course Improvement Plan](./Docker-material-improvement-plan.md)** - 2025 updates explained

### **External Resources:**
- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/) - Explore official images
- [Docker Scout](https://docs.docker.com/scout/) - Learn more about security scanning
- [Play with Docker](https://labs.play-with-docker.com/) - Free online Docker playground
- [Distroless Images GitHub](https://github.com/GoogleContainerTools/distroless)
- [Docker Community Slack](https://dockr.ly/slack)

---

## **🤝 Contributing & Feedback**

This is a living course that evolves with Docker technology. If you find issues or have suggestions:
- Review the [improvement plan](./Docker-material-improvement-plan.md)
- Test all exercises and report any issues
- Suggest additional topics or exercises
- Share your learning experiences

---

## **📄 License & Usage**

This course material is designed for educational purposes. Students are encouraged to:
- Use materials for learning Docker
- Practice exercises and create variations
- Reference materials in their studies
- Share knowledge with peers

---

## **🏆 Course Completion Checklist**

Track your progress through the course:

- [ ] Session 1: Docker basics and installation
- [ ] Session 2: Images and containers management
- [ ] Session 3: Building custom Docker images
- [ ] Session 4: Optimization and security (including 3 new exercises)
- [ ] Session 5: Data management with volumes
- [ ] Session 6: Networking and ports
- [ ] Session 7: Docker Compose multi-container apps
- [ ] Session 8: Security & best practices (NEW)
- [ ] Final Project: Deploy production-ready multi-tier application

**Congratulations on completing the Docker Introduction course! You're now ready to build and deploy containerized applications! 🎉**

---

**Course Version:** 2025.1
**Last Updated:** October 2025
**Maintained By:** Course Instructor Team
