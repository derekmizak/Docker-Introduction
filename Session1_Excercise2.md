---

## **Session1_Exercise2.md**


# Exercise 2: Running "Hello World"

**Objective:**  
Run the "Hello World" Docker container and understand the steps involved in its execution.

---

## **Instructions**

### 1. Run the Container

Open your terminal or command prompt and execute:

```bash
docker run hello-world
```

### 2. Observe the Output

- Read the messages displayed in the terminal carefully.
- **Note:** The output explains what Docker did to run the container.

### 3. Understand the Process

Answer the following questions:

- **Q1:** What did Docker do when you ran the `docker run hello-world` command?
  - *Hint:* Consider image pulling, container creation, and execution.
- **Q2:** Where did the "hello-world" image come from?
  - *Hint:* Think about Docker Hub and image registries.
- **Q3:** What is the difference between an image and a container?
  - *Hint:* Define both terms and explain their relationship.

### 4. List Images and Containers

- **List Downloaded Images:**

  ```bash
  docker images
  ```

- **List All Containers (Running and Exited):**

  ```bash
  docker ps -a
  ```

### 5. Clean Up (Optional)

- Remove the "hello-world" image:

  ```bash
  docker rmi hello-world
  ```

- Remove the exited container:

  ```bash
  docker rm [CONTAINER_ID]
  ```

  - Replace `[CONTAINER_ID]` with the actual ID from `docker ps -a`.

---

## **Expected Result**

- **Successful Execution:**
  - The terminal displays "Hello from Docker!" along with additional information.
- **Understanding Achieved:**
  - You comprehend how Docker pulls images and runs containers.
- **Commands Familiarity:**
  - You can list images and containers using Docker commands.

---

## **Explanation**

- **Docker Pulls the Image:**
  - If the "hello-world" image is not found locally, Docker downloads it from Docker Hub.
- **Container Creation and Execution:**
  - Docker creates a new container from the image and executes the default command.
- **Image vs. Container:**
  - An **image** is a read-only template.
  - A **container** is a running instance of an image.

---

## **Additional Resources**

- [Docker Images Documentation](https://docs.docker.com/engine/reference/commandline/images/)
- [Docker Containers Overview](https://docs.docker.com/get-started/overview/)

---