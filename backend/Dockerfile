# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt ./requirements.txt
RUN ls -la  # This will help debug if the file is copied
RUN pip install --no-cache-dir -r requirements.txt uvicorn || cat requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Add environment variables
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Command to run the application
CMD ["uvicorn", "main:socket_app", "--host", "0.0.0.0", "--port", "8000"] 