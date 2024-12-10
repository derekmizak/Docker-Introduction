FROM alpine:latest

   # Install required dependencies
   RUN apk add --no-cache curl bash

   # Install Node.js v22.11.0 LTS
   RUN curl -fsSL https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz | tar -xJ -C /usr/local --strip-components=1

   # Verify Node.js installation
   RUN node -v && npm -v

   # Set the working directory
   WORKDIR /app

   # Copy application files
   COPY package.json ./
   RUN npm install
   COPY . .

   # Expose the application port
   EXPOSE 3000

   # Default command
   CMD ["npm", "start"]