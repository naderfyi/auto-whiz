# Use an official Node runtime as a parent image
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install any dependencies
RUN npm install

# Copy the rest of the client application
COPY . ./

# Build the app
RUN npm run build

# Install serve to serve the build folder
RUN npm install -g serve

# Make port 3000 available outside this container
EXPOSE 3000

# Serve the build directory on port 3000
CMD ["serve", "-s", "build", "-l", "3000"]
