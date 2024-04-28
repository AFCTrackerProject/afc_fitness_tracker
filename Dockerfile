FROM postgres:latest

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=123
ENV POSTGRES_DB=afcfitness

# Expose the PostgreSQL port
EXPOSE 5432

# Copy the database dump to the container so it will be imported on startup
COPY database_dump.sql /docker-entrypoint-initdb.d/



# When the container starts, it will execute any .sql files in docker-entrypoint-initdb.d




# # Use an official Python runtime as a parent image
# FROM python:3.12-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Make port 5000 available to the world outside this container
# EXPOSE 5000

# # Define environment variable
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# # Run app.py when the container launches
# CMD ["flask", "run"]

