# Use Ubuntu as the base image
FROM ubuntu:latest

# Set the working directory (optional)
WORKDIR /app

# Default command to keep the container running
CMD ["/bin/bash"]
