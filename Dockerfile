# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8003 available to the world outside this container
EXPOSE 8003

# Define environment variable
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run Gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8003", "main:app"]


# To build docker image
# docker build -t <name of image, not surrounded by the bracket things> .
# dont forget the period at the end!

#To run docker image
# docker run -p 5000:5000 <name of image, not surrounded by the bracket things>

