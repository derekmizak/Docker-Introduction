

### **Exercise 4: Using ENTRYPOINT Command**

**Filename:** `Session4_Exercise4.md`


# Exercise 4: Using ENTRYPOINT Command

## Objective
- Learn how to configure a Docker container as an executable tool using `ENTRYPOINT`.
- Understand how to use `CMD` with `ENTRYPOINT` to provide default arguments that can be overridden.

---

## Instructions

### Step 1: Create a Simple Curl-Based Dockerfile
1. Create a directory for your project:
   ```bash
   mkdir entrypoint-example
   cd entrypoint-example
   ```

2. Write a `Dockerfile`:
   ```Dockerfile
   FROM alpine:latest

   # Install curl
   RUN apk add --no-cache curl

   # Set ENTRYPOINT
   ENTRYPOINT ["curl"]
   ```

3. Build the image:
   ```bash
   docker build -t curl-tool .
   ```

---

### Step 2: Run the Container with Arguments
1. Test the container by passing arguments to `curl`:
   - Make a simple HTTP request:
     ```bash
     docker run --rm curl-tool https://example.com
     ```
     **What happens?**  
     The container runs `curl https://example.com`.

   - Fetch only the headers of a URL:
     ```bash
     docker run --rm curl-tool -I https://example.com
     ```
     **What happens?**  
     The container runs `curl -I https://example.com`.

2. Observe how the arguments passed to `docker run` are appended to the `ENTRYPOINT` command.

---

### Step 3: Add Default Arguments Using CMD
1. Modify the `Dockerfile` to include `CMD`:
   ```Dockerfile
   FROM alpine:latest

   # Install curl
   RUN apk add --no-cache curl

   # Set ENTRYPOINT
   ENTRYPOINT ["curl"]

   # Provide default arguments
   CMD ["https://example.com"]
   ```

2. Build the image again:
   ```bash
   docker build -t curl-tool-with-cmd .
   ```

3. Run the container:
   - Without overriding `CMD` (uses the default argument):
     ```bash
     docker run --rm curl-tool-with-cmd
     ```
     **What happens?**  
     The container runs `curl https://example.com`.

   - With overriding `CMD`:
     ```bash
     docker run --rm curl-tool-with-cmd -I https://google.com
     ```
     **What happens?**  
     The container runs `curl -I https://google.com`.

---

## Discussion Points
1. **How ENTRYPOINT Works:**
   - ENTRYPOINT sets the main command that the container will execute.
   - Additional arguments passed to `docker run` are appended to the `ENTRYPOINT` command.

2. **ENTRYPOINT vs. CMD:**
   - `ENTRYPOINT` defines the core behavior of the container.
   - `CMD` provides default arguments to `ENTRYPOINT` but can be overridden.

3. **Real-World Example:**
   - Use `ENTRYPOINT` for containers designed as tools (e.g., `curl`, `wget`, or custom scripts).
   - Combine `CMD` to provide sensible defaults while retaining flexibility.

---

## Expected Outcome
- Students understand how to configure `ENTRYPOINT` to make containers behave like executables.
- They see how `CMD` provides default arguments while allowing overrides.

---

## Notes
- The `ENTRYPOINT` and `CMD` combination is ideal for containers that need predictable behavior with optional flexibility.
- This pattern is commonly used for CLI-based container tools or automated tasks.

