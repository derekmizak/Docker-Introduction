# Build stage
FROM alpine:latest AS build-stage

# Install Python, pip, and build dependencies
RUN apk add --no-cache python3 py3-pip gcc musl-dev

# Set the working directory
WORKDIR /app

# Copy the Python application
COPY app.py ./

# Runtime stage
FROM alpine:latest

# Install only the Python runtime
RUN apk add --no-cache python3

# Copy the application files
WORKDIR /app
COPY --from=build-stage /app /app

# Set the default command
CMD ["python3", "app.py"]