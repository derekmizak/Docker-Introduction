FROM alpine:latest

# Install Node.js and npm, and clean up cache in a single step
RUN apk add --no-cache curl bash nodejs npm && \
    rm -rf /var/cache/apk/* && npm -v && node -v

# Set the working directory
WORKDIR /app


# Copy application files and install dependencies
COPY package.json ./
RUN npm install && \
    rm -rf /var/cache/apk/* ~/.npm

# Copy source code
COPY . .

# Expose the application port
EXPOSE 3000

# Default command
CMD ["npm", "start"]
