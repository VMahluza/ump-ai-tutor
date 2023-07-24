# Use an official Python runtime as a base image
FROM python:3.11.4

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

# Expose the port that the ASGI server will run on (adjust this if needed)
EXPOSE 8000

# Start the ASGI server (adjust this if needed)
CMD ["daphne", "config.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
