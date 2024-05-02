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