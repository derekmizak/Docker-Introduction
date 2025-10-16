
## **Session2_Exercise1.md**


# Exercise 1: Pulling and Running Images

**Objective:**  
Pull an image from Docker Hub and run a container.

---

## **Instructions**

### 1. Pull the Nginx Image

Download the official Nginx image from Docker Hub.

```bash
docker pull nginx
```

### 2. Run the Nginx Container

Start a new container using the Nginx image.

```bash
docker run --name mynginx -d -p 8080:80 nginx
```

- **`--name mynginx`:** Assigns the name `mynginx` to the container.
- **`-d`:** Runs the container in detached mode (in the background).
- **`-p 8080:80`:** Maps port **80** in the container to port **8080** on the host machine.

### 3. Access Nginx in a Browser

- Open a web browser.
- Navigate to `http://localhost:8080`.
- You should see the Nginx welcome page.

### 4. List Running Containers

Verify that the container is running.

```bash
docker ps
```

- Look for `mynginx` in the list of running containers.

### 5. Stop and Remove the Container

Clean up by stopping and removing the container.

```bash
docker stop mynginx
docker rm mynginx
```

---

## **Expected Result**

- The Nginx container is running and accessible via your web browser.
- You understand how to pull images, run containers, and map ports.
- You can manage containers using basic Docker commands.

---

## **Notes**

- **Port Mapping (`-p`):** Exposes the container's port to the host system, allowing external access.
- **Container Naming:** Assigning a name makes it easier to manage and reference containers.
- **Detached Mode (`-d`):** Allows the container to run in the background without tying up the terminal.

---

## **Additional Resources**

- [Docker Run Reference](https://docs.docker.com/engine/reference/run/)
- [Docker Networking Basics](https://docs.docker.com/network/)

