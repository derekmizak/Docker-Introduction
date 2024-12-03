

## **Session2_Exercise3.md**


# Exercise 3: Resource Limitation with a Custom Stress Container

**Objective:**  
Build a custom stress testing container, limit its CPU and memory usage, and observe the effects.

---

## **Instructions**

### 1. Build a Custom Stress Container

First, create a custom Docker image with the `stress` tool.

1. **Create a `Dockerfile`:**

   ```Dockerfile
   FROM ubuntu:latest
   RUN apt-get update && apt-get install -y stress
   ENTRYPOINT ["stress"]
   ```

2. **Build the Image:**

   ```bash
   docker build -t custom-stress .
   ```

   - This creates an image named `custom-stress` with the `stress` tool installed.

---

### 2. Run a Stress Test Container Without Limits

Start a container from the custom image without any resource limits.

```bash
docker run -d --name stress custom-stress --cpu 2
```

- **`--cpu 2`:** Spawns two workers spinning on `sqrt()` to simulate CPU load.

---

### 3. Run a Stress Test Container with Resource Limits

Now, start another container with resource constraints.

```bash
docker run -d --name limited_stress --cpus="0.5" --memory="256m" custom-stress --cpu 2
```

- **`--cpus="0.5"`:** Limits the container to 50% of a single CPU core.
- **`--memory="256m"`:** Limits the container to 256 MB of RAM.

---

### 4. Monitor Resource Usage

Use Docker's statistics command to monitor resource consumption.

```bash
docker stats
```

- Observe CPU and memory usage for both `stress` and `limited_stress` containers.
- Note the differences in resource utilization.

---

### 5. Observe the Impact

- **Compare Performance:**
  - The `limited_stress` container should use less CPU and memory due to the constraints.
  - The `stress` container may consume more resources, potentially affecting system performance.
- **Optional:** Open another terminal and observe system-wide resource usage with tools like `top` or `htop`.

---

### 6. Clean Up

Stop and remove both containers after the test.

```bash
docker stop stress limited_stress
docker rm stress limited_stress
```

---

## **Expected Result**

- You successfully build and run a custom stress testing container.
- You observe the effects of Docker's CPU and memory limits on container performance.
- You gain insight into managing system resources in a containerized environment.

---

## **Notes**

- **Resource Limitation Flags:**
  - `--cpus`: Limits CPU usage.
  - `--memory`: Sets the maximum memory available to the container.
- **Importance of Resource Management:**
  - Prevents a container from consuming excessive resources.
  - Ensures system stability, especially in multi-container environments.

---

## **Additional Resources**

- [Docker Run Resource Constraints](https://docs.docker.com/config/containers/resource_constraints/)
- [Docker Stats Command](https://docs.docker.com/engine/reference/commandline/stats/)
- [Building a Docker Image](https://docs.docker.com/engine/reference/builder/)

