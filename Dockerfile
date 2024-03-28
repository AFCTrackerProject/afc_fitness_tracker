# Use an existing Docker image as a base
FROM ubuntu:20.04

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory (where your project files are) into the container at /app
COPY . .

# Install any dependencies your project requires
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose the port your app runs on
EXPOSE 8080

# Command to run your application
CMD ["python3", "app.py"]
