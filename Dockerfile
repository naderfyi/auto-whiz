# Use Python slim image as the base
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the Python requirements file first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the rest of your application code
COPY . .

# Define environment variable
ENV NAME AutoWhiz

# Set Port
ARG PORT=5004
ENV PORT $PORT

# Expose the port the app runs on
EXPOSE $PORT

# Use Gunicorn to serve the Flask application
CMD ["gunicorn", "--workers=1", "--bind", "0.0.0.0:$PORT", "app:app"]
