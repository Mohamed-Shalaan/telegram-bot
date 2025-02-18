# Use official Python image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the contents of the local directory to the working directory in the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run when container starts
CMD ["python", "paybot.py"]
