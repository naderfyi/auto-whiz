# Use Python slim image as the base
FROM python:3.11-slim-buster

RUN apt-get update && \
    apt-get clean;

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg unzip && \
    rm -rf /var/lib/apt/lists/*

# Update the package list, install additional dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*
    
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME AutoWhiz

# Copy the Python requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the rest of your application code
COPY . .

# Set Port
ARG PORT=5000

# Expose the port the app runs on
EXPOSE $PORT

# Use Gunicorn to serve the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]