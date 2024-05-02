# old dockerfile, pre supervisord

# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to specify the Flask application entry
ENV FLASK_APP=app.py

# Run Gunicorn when the container launches
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app"]

# Instructions
# To build docker image
# docker build -t <name of image, not surrounded by the bracket things> .
# don't forget the period at the end!

# To run docker image
# docker run -p 5000:5000 <name of image, not surrounded by the bracket things>


# # Use an official Python runtime as a parent image
# FROM python:3.12-slim

# # Install supervisord
# RUN apt-get update && apt-get install -y supervisor

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Configuration for supervisord to manage multiple processes
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# # Expose the ports the apps run on
# EXPOSE 5000 5001

# # Run supervisord
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]






# cloud hosting docker attempt

# # Use an official Python runtime as a parent image
# FROM python:3.12-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Make port 8003 available to the world outside this container
# EXPOSE 8003

# # Define environment variable
# ENV FLASK_APP=main.py
# ENV FLASK_RUN_HOST=0.0.0.0

# # Run Gunicorn when the container launches
# CMD ["gunicorn", "--bind", "0.0.0.0:8003", "main:app"]


