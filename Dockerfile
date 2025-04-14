# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for database URI (you can override this at runtime)
ENV DATABASE_URI=postgresql://postgres:postgres@postgresql:5432/postgres

# Expose the port the app runs on
EXPOSE 8080

# Command to run the app with Gunicorn
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:8080"]
