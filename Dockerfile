# Use official lightweight Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies (optional but can help with psycopg2)
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8080

# Start the app using Gunicorn, pointing to your Flask app factory function
# 'service' is the folder where __init__.py is located and 'create_app' is your factory function
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "service:create_app"]
