# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN chmod +x /app/wait-for-it.sh

# Upgrade pip
RUN pip install --upgrade pip


RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000
