# Exercise 4: Analyze and Improve an Existing Dockerfile


**Filename:** `Session4_Exercise5.md`

## Objective

* Analyze an inefficient Dockerfile and identify areas for improvement.
* Apply Dockerfile best practices to optimize for size and build time.

## Description

This exercise challenges you to critically evaluate a Dockerfile and apply your knowledge of optimization techniques to improve it.

Content for this excercise is provided in the [./app](./app/) directory. The directory contains the following files:
```
./app
    ├── app.py
    ├── Dockerfile.inefficient
    ├── Dockerfile.optimized
    ├── requirements.txt
```

The `app.py` file is a simple Python application that start a number guessing game. The `requirements.txt` file lists the dependencies for the application.

## Steps

### 1. Analyze the Inefficient Dockerfile

*   **`Dockerfile.inefficient`:**

    ```dockerfile
    FROM ubuntu

# Update package lists
RUN apt-get update

# Install Python and necessary tools
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv

# Create the application directory
RUN mkdir -p /app

# Copy application files (separate layers for inefficiency)
COPY ./app.py /app
COPY ./requirements.txt /app

# Set the working directory
WORKDIR /app

# Create a virtual environment
RUN python3 -m venv /app/venv

# Install dependencies in the virtual environment
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Set the default command to use the virtual environment's Python
CMD ["/app/venv/bin/python", "app.py"]

    ```

### 2. Identify Areas for Improvement

1.  What are the potential issues with this Dockerfile in terms of efficiency and best practices?
2.  How can it be improved by applying the concepts learned in the session?

### 3. Rewrite the Dockerfile

*   Create a new Dockerfile named `Dockerfile.optimized` with the following improvements:

    *   Use a smaller base image e.g. `python:3.10-slim`.
    *   Combine multiple `RUN` commands to reduce layers.
    *   Use a `.dockerignore` file to exclude unnecessary files.
    *   (Optional) Implement multi-stage builds if applicable.


### 4. Build and Compare Images

1.  Build both images:

    ```bash
    docker build -t inefficient-image -f Dockerfile.inefficient .
    docker build -t optimized-image -f Dockerfile.optimized .
    ```

2.  Compare the image sizes and build times:

    ```bash
    docker images
    ```

## Expected Outcome

*   The `optimized-image` should be smaller and have a faster build time compared to the `inefficient-image`.

## Notes

*   Experiment with different optimization techniques and compare the results.
*   Discuss the trade-offs between image size, build time, and maintainability.