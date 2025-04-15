# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application contents
COPY service/ ./service/

# Set environment variable for database URI (you can override this at runtime)
ENV DATABASE_URI=postgresql://postgres:postgres@postgresql:5432/postgres

# Switch to a non-root user
RUN useradd --uid 1000 theia && chown -R theia /app
USER theia

# Expose the port the app runs on
EXPOSE 8080

# Command to run the app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "service:create_app"]

