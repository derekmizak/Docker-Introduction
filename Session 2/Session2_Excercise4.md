
## **Session2_Exercise4.md**

# Exercise 4: Creating Custom Images

**Objective:**  
Create a custom Docker image from a modified container using `docker commit`.

---

## **Instructions**

### 1. Run a Base Ubuntu Container

Start a new container from the Ubuntu image.

```bash
docker run -it --name myubuntu ubuntu /bin/bash
```

- **`--name myubuntu`:** Names the container for easy reference.
- **`/bin/bash`:** Starts a Bash shell inside the container.

### 2. Install Nginx Inside the Container

Inside the container shell, execute the following commands:

- **Update Package Lists:**

  ```bash
  apt update
  ```

- **Install Nginx:**

  ```bash
  apt install -y nginx
  ```

- **Verify Nginx Installation:**

  ```bash
  nginx -v
  ```

### 3. Exit the Container

Leave the container shell.

```bash
exit
```

### 4. Commit the Container to a New Image

Create a new image from the modified container.

```bash
docker commit myubuntu myubuntu:nginx
```

- **`myubuntu`:** The name of the container.
- **`myubuntu:nginx`:** The name and tag for the new image.

### 5. Verify the New Image

List your Docker images to confirm the new image exists.

```bash
docker images
```

- Look for `myubuntu` with the tag `nginx`.

### 6. Run a Container from the New Image

Start a new container using your custom image.

```bash
docker run -d -p 8081:80 --name mynginx myubuntu:nginx nginx -g "daemon off;"
```

- **`-p 8081:80`:** Maps port **80** in the container to port **8081** on the host.
- **`nginx -g "daemon off;"`:** Runs Nginx in the foreground to keep the container running.

### 7. Test the Nginx Server

- Open a web browser.
- Navigate to `http://localhost:8081`.
- You should see the default Nginx welcome page.

### 8. Clean Up

- **Stop and Remove Containers:**

  ```bash
  docker stop mynginx myubuntu
  docker rm mynginx myubuntu
  ```

- **Remove the Custom Image (Optional):**

  ```bash
  docker rmi myubuntu:nginx
  ```

---

## **Expected Result**

- You have created a custom Docker image with Nginx installed.
- You understand how `docker commit` captures changes from a container.
- You can run containers from custom images.

---

## **Notes**

- **`docker commit`:** Creates a new image from a container's changes.
- **Best Practices:**
  - While `docker commit` is useful, it's better to use a `Dockerfile` for reproducibility.
  - Using `Dockerfile` allows you to version control your image build instructions.
- **Running Nginx in the Foreground:**
  - The `-g "daemon off;"` argument is necessary to prevent Nginx from running as a daemon, which would cause the container to exit.

---

## **Additional Resources**

- [Docker Commit Command](https://docs.docker.com/engine/reference/commandline/commit/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

